"""Decision client for the superloop: typed questions in, normalized typed answers out.

A decision model answers bounded questions about a state with probabilities and writes no text.
This module sends one request shape (state plus questions with choice, noul and score types) to a
configured backend and normalizes the answer, so the driver never depends on one vendor's field
names. It never decides what happens next: the driver turns answers into actions with code.

Backends:
  rules      deterministic answers from host facts. Always available. The baseline to beat.
  replay     answers recorded in a JSON file, keyed by question id and iteration. For tests.
  fake       answers computed by a Python callable. For tests.
  http       any endpoint that accepts the shared request shape. The controller config gives
             base_url, path, model, the API key environment variable and the state encoding.
             "object" sends the state as a JSON object. "text" serializes it into state.text,
             for endpoints that read only a text field.
  dual       two backends. A consequential question is answered only when both agree, else
             the answer is an abstention.

Normalized answer per question id:
  choice  {"type": "choice", "choice": id, "probabilities": {...}, "top": p, "margin": p1 - p2}
  noul    {"type": "noul", "p": p}
  score   {"type": "score", "score": x, "probabilities": [...], "levels": n}
  abstain {"type": "abstain", "reason": "..."}

An answer that names an unknown option, carries a non-finite number or probabilities that do not
sum to about 1 becomes an abstention. A transport error makes every answer an abstention. The
driver treats an abstention as "no information" and falls back to its rules.

Set MM_OFFLINE=1 to make every http call fail before it opens a socket.
"""
import hashlib, json, math, os, time, urllib.error, urllib.request

SUM_TOLERANCE = 0.03  # some endpoints round probabilities to two decimals


class OfflineError(RuntimeError):
    pass


def question_hash(questions):
    return hashlib.sha256(json.dumps(questions, sort_keys=True).encode()).hexdigest()[:16]


def state_hash(state):
    return hashlib.sha256(json.dumps(state, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]


def wire_questions(catalog, ids, menus):
    """Build the request questions for the given ids. menus maps a question id to the option
    ids the host allows right now; options outside the menu are never offered."""
    out = {}
    for qid in ids:
        q = catalog[qid]
        w = {"type": q["type"], "instructions": q["instructions"]}
        if q["type"] == "choice":
            allowed = menus.get(qid, list(q["criteria"]))
            w["criteria"] = {k: q["criteria"][k] for k in q["criteria"] if k in allowed}
        elif q["type"] == "score":
            w["criteria"] = list(q["criteria"])
        elif q.get("criteria"):
            w["criteria"] = dict(q["criteria"])
        out[qid] = w
    return out


def _finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def normalize(raw_answers, wire):
    """Turn a raw answers object into normalized answers, abstaining on anything malformed."""
    out = {}
    for qid, q in wire.items():
        a = raw_answers.get(qid) if isinstance(raw_answers, dict) else None
        if not isinstance(a, dict):
            out[qid] = {"type": "abstain", "reason": "missing answer"}
            continue
        t = q["type"]
        if t == "noul":
            p = a.get("noul", a.get("p"))
            out[qid] = {"type": "noul", "p": float(p)} if _finite(p) and 0 <= p <= 1 else \
                {"type": "abstain", "reason": "noul probability missing or out of range"}
        elif t == "choice":
            opts = list(q["criteria"])
            probs = a.get("probabilities")
            pick = a.get("choice")
            if pick not in opts:
                out[qid] = {"type": "abstain", "reason": f"unknown option {pick!r}"}
                continue
            if not isinstance(probs, dict) or set(probs) - set(opts) or not all(_finite(v) and v >= 0 for v in probs.values()):
                out[qid] = {"type": "abstain", "reason": "choice probabilities missing or malformed"}
                continue
            probs = {k: float(probs.get(k, 0.0)) for k in opts}
            if abs(sum(probs.values()) - 1.0) > SUM_TOLERANCE:
                out[qid] = {"type": "abstain", "reason": "choice probabilities do not sum to 1"}
                continue
            ranked = sorted(probs.values(), reverse=True)
            if probs[pick] + 1e-9 < ranked[0]:
                out[qid] = {"type": "abstain", "reason": "choice is not the most probable option"}
                continue
            out[qid] = {"type": "choice", "choice": pick, "probabilities": probs, "top": ranked[0],
                        "margin": ranked[0] - (ranked[1] if len(ranked) > 1 else 0.0)}
        elif t == "score":
            n = len(q["criteria"])
            probs = a.get("probabilities")
            if isinstance(probs, dict):
                try:
                    probs = [float(probs.get(str(i), 0.0)) for i in range(n)]
                except (TypeError, ValueError):
                    probs = None
            s = a.get("score")
            if not _finite(s) or not 0 <= s <= n - 1 or not isinstance(probs, list) or len(probs) != n \
                    or not all(_finite(v) and v >= 0 for v in probs) or abs(sum(probs) - 1.0) > SUM_TOLERANCE:
                out[qid] = {"type": "abstain", "reason": "score or level probabilities malformed"}
                continue
            out[qid] = {"type": "score", "score": float(s), "probabilities": probs, "levels": n}
        else:
            out[qid] = {"type": "abstain", "reason": f"unsupported type {t}"}
    return out


class Backend:
    name = "base"

    def answer(self, state, wire, context):
        raise NotImplementedError


class RulesBackend(Backend):
    """Deterministic answers from host facts in the state. Every question in the catalog names
    a rule; a question without one abstains."""
    name = "rules"

    def __init__(self, catalog):
        self.catalog = catalog

    def answer(self, state, wire, context):
        out = {}
        for qid in wire:
            rule = self.catalog[qid].get("rule")
            fn = RULES.get(rule)
            out[qid] = fn(state, wire[qid]) if fn else {"type": "abstain", "reason": "no rule"}
        return out, {"model": "rules", "usage": {"input_tokens": 0, "output_tokens": 0}}


def _choice(pick, opts):
    return {"type": "choice", "choice": pick, "probabilities": {k: (1.0 if k == pick else 0.0) for k in opts},
            "top": 1.0, "margin": 1.0}


def _rule_progress(state, q):
    opts = list(q["criteria"])
    f = state.get("facts", {})
    if f.get("regressed"):
        pick = "regressing"
    elif f.get("unchanged_streak", 0) >= 1:
        pick = "stalled"
    else:
        pick = "progressing"
    return _choice(pick if pick in opts else opts[0], opts)


def _rule_blocked(state, q):
    f = state.get("facts", {})
    return {"type": "noul", "p": 1.0 if f.get("worker_reported_blocked") or f.get("permission_denied") else 0.0}


def _rule_goal_met(state, q):
    f = state.get("facts", {})
    ok = f.get("checks_failed", 1) == 0 and f.get("checks_run", 0) > 0
    return {"type": "noul", "p": 1.0 if ok else 0.0}


def _rule_situation(state, q):
    opts = list(q["criteria"])
    want = state.get("goal", {}).get("situation")
    return _choice(want if want in opts else opts[-1], opts)


def _rule_next_action(state, q):
    opts = list(q["criteria"])
    f = state.get("facts", {})
    if f.get("checks_failed", 0) > 0 and "repair" in opts:
        return _choice("repair", opts)
    if f.get("checks_failed", 1) == 0 and "request_review" in opts:
        return _choice("request_review", opts)
    return _choice("continue" if "continue" in opts else opts[0], opts)


def _rule_needs_human(state, q):
    f = state.get("facts", {})
    return {"type": "noul", "p": 1.0 if f.get("touches_protected") or f.get("outward_action") else 0.0}


RULES = {"progress": _rule_progress, "blocked": _rule_blocked, "goal_met": _rule_goal_met,
         "situation": _rule_situation, "next_action": _rule_next_action, "needs_human": _rule_needs_human}


class ReplayBackend(Backend):
    """Answers from a recording: {"answers": {"<iteration>": {"<qid>": raw answer}}, "default": {...}}.
    A missing entry abstains, so a short recording cannot invent decisions."""
    name = "replay"

    def __init__(self, recording, model="replay"):
        self.rec = recording
        self.model = model

    def answer(self, state, wire, context):
        it = str(context.get("iteration", 0))
        pool = dict(self.rec.get("default", {}))
        pool.update(self.rec.get("answers", {}).get(it, {}))
        if pool.get("_outage"):
            raise ConnectionError("recorded outage")
        return {q: pool[q] for q in wire if q in pool}, {"model": self.model, "usage": {"input_tokens": 0, "output_tokens": 0}}


class FakeBackend(Backend):
    name = "fake"

    def __init__(self, fn, model="fake"):
        self.fn = fn
        self.model = model

    def answer(self, state, wire, context):
        return self.fn(state, wire, context), {"model": self.model, "usage": {"input_tokens": 0, "output_tokens": 0}}


class HttpBackend(Backend):
    """Any endpoint that accepts {"model", "state", "questions"} and returns {"model", "answers",
    "usage"}. The key is read from an environment variable named in the config, never stored."""
    name = "http"

    def __init__(self, cfg):
        self.cfg = cfg

    def payload(self, state, wire):
        s = state
        if self.cfg.get("state_encoding") == "text":
            s = {"text": json.dumps(state, sort_keys=True, ensure_ascii=False)}
        return {"model": self.cfg["model"], "state": s, "questions": wire}

    def answer(self, state, wire, context):
        if os.environ.get("MM_OFFLINE") == "1":
            raise OfflineError("MM_OFFLINE=1 forbids network calls")
        key = os.environ.get(self.cfg["api_key_env"], "")
        if not key:
            raise PermissionError(f"environment variable {self.cfg['api_key_env']} is not set")
        body = json.dumps(self.payload(state, wire)).encode()
        req = urllib.request.Request(self.cfg["base_url"].rstrip("/") + self.cfg["path"], data=body, method="POST",
                                     headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        timeout = float(self.cfg.get("timeout_seconds", 10))
        tries = int(self.cfg.get("retries", 2)) + 1
        last = None
        for i in range(tries):
            try:
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    data = json.loads(r.read().decode())
                return data.get("answers", {}), {"model": data.get("model", self.cfg["model"]), "usage": data.get("usage", {})}
            except urllib.error.HTTPError as ex:
                last = ex
                if ex.code not in (429, 500, 502, 503, 529):
                    break
            except (urllib.error.URLError, TimeoutError, ValueError) as ex:
                last = ex
            time.sleep(min(2 ** i, 8))
        raise ConnectionError(f"decision endpoint failed: {last}")


class DualBackend(Backend):
    """Two backends. For a question listed as consequential, keep the answer only when both pick
    the same option (choice), or both land on the same side of 0.5 (noul). Other questions take
    the first backend's answer. Agreement between two models is not independence; it is a
    stricter filter whose value has to be measured."""
    name = "dual"

    def __init__(self, first, second, consequential):
        self.a, self.b, self.cons = first, second, set(consequential)

    def answer(self, state, wire, context):
        ra, ma = self.a.answer(state, wire, context)
        rb, mb = self.b.answer(state, wire, context)
        na, nb = normalize(ra, wire), normalize(rb, wire)
        out = {}
        for qid in wire:
            x, y = na[qid], nb[qid]
            if qid not in self.cons:
                out[qid] = ra.get(qid)
                continue
            agree = x["type"] == y["type"] and (
                (x["type"] == "choice" and x["choice"] == y["choice"]) or
                (x["type"] == "noul" and (x["p"] >= 0.5) == (y["p"] >= 0.5)) or
                (x["type"] == "score" and round(x["score"]) == round(y["score"])))
            if agree:
                out[qid] = ra.get(qid)
            else:
                out[qid] = None  # becomes an abstention in normalize
        meta = {"model": f"{ma.get('model')}+{mb.get('model')}",
                "usage": {"input_tokens": ma.get("usage", {}).get("input_tokens", 0) + mb.get("usage", {}).get("input_tokens", 0),
                          "output_tokens": 0}}
        return out, meta


def build_backend(spec, catalog, recordings=None):
    kind = spec["kind"]
    if kind == "rules":
        return RulesBackend(catalog)
    if kind == "replay":
        rec = spec.get("recording")
        if isinstance(rec, str):
            rec = json.load(open(rec, encoding="utf-8"))
        return ReplayBackend(rec or (recordings or {}), spec.get("model", "replay"))
    if kind == "http":
        return HttpBackend(spec)
    if kind == "dual":
        return DualBackend(build_backend(spec["first"], catalog, recordings),
                           build_backend(spec["second"], catalog, recordings), spec.get("consequential", []))
    raise ValueError(f"unknown backend kind {kind}")


def ask(backend, catalog, ids, menus, state, context):
    """Ask the questions. Returns (normalized answers, record for the decision log)."""
    wire = wire_questions(catalog, ids, menus)
    t0 = time.time()
    error = None
    try:
        raw, meta = backend.answer(state, wire, context)
    except Exception as ex:  # outage, offline guard, missing key: all become abstentions
        raw, meta, error = {}, {"model": None, "usage": {}}, f"{type(ex).__name__}: {ex}"
    answers = normalize(raw, wire)
    rec = {"backend": backend.name, "model": meta.get("model"), "question_hash": question_hash(wire),
           "state_hash": state_hash(state), "latency_ms": int((time.time() - t0) * 1000),
           "usage": meta.get("usage", {}), "error": error, "answers": answers}
    return answers, rec
