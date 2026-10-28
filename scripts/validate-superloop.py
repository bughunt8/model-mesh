#!/usr/bin/env python3
"""Validate superloop goal files, controller configs and the decision question catalog.

These are run-configuration rules. They do not add a decision seat to the orchestration matrix:
no decision model is adopted, so the matrix rules O1 to O18 stay as they are.

Rules:
  L1  question catalog: unique ids, the six required questions, known types and rules, choice
      criteria 2 to 255, score criteria 2 to 10, a revision number, and an authority of shadow,
      brake or smoke. Brake effects are pause_human, stop_no_progress or add_review only, and a
      choice brake names options that exist. No question may carry a threshold.
  L2  goal: id, objective, a situation A01 to A12, one of the four profiles, an option name, at
      least one acceptance check given as an argv list with a timeout, and protected paths.
  L3  caps: max_iterations 1 to 50, wall_clock_seconds 60 to 86400, no_progress_streak and
      fix_verify_cycles at least 1, per_call_seconds positive, and a positive budget_usd.
  L4  mode is shadow or advisory. There is no control mode.
  L5  decision backend: rules, replay, http or dual. An http backend uses https, a path, a
      pinned model ID (no latest or preview alias) and the name of an environment variable for
      the key, never a key. dual needs a consequential question list.
  L6  advisory mode needs a disclosed decision base family and at least one qualification record
      for a brake or smoke question, made by learn-then-test on at least 100 labelled decisions,
      with alpha and delta at most 0.1 and a model ID equal to the backend's pinned model.
  L7  the ultimate profile admits a remote decision endpoint only when it is marked verified as
      Hong Kong reachable and policy eligible.
  L8  worker: an omo worker names a local binary and an agent, pins omo 4.19.4, and the
      materialized config disables the goal, todo-continuation-enforcer and start-work hooks.
  L9  reviewers: argv lists, never on opencode-omo, and each names a harness.
  L10 reservations: worker_call above zero, every reservation non-negative. Missing usage is not
      zero cost.

Usage:
  python scripts/validate-superloop.py                      check the committed examples
  python scripts/validate-superloop.py GOAL CONTROLLER      check one pair
  python scripts/validate-superloop.py --self-test
"""
import copy, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUESTIONS = os.path.join(ROOT, "examples", "superloop", "questions.json")
EXAMPLES = [("examples/superloop/goal.example.json", "examples/superloop/controller.example.json"),
            ("examples/superloop/goal.example.json", "examples/superloop/controller.rules.example.json")]
REQUIRED_Q = {"situation", "progress", "blocked", "needs_human", "goal_met", "next_action"}
RULE_NAMES = {"situation", "progress", "blocked", "needs_human", "goal_met", "next_action"}
BRAKE_EFFECTS = {"pause_human", "stop_no_progress", "add_review"}
PROFILES = {"ultimate", "hybrid", "b4b", "global"}
SITUATIONS = {f"A{i:02d}" for i in range(1, 13)}
REQUIRED_HOOKS = {"goal", "todo-continuation-enforcer", "start-work"}
ALIAS = re.compile(r"(latest|preview)", re.I)
ENV_NAME = re.compile(r"^[A-Z][A-Z0-9_]{2,}$")


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def validate_catalog(cat):
    e = []
    qs = cat.get("questions") if isinstance(cat, dict) else None
    if not isinstance(qs, list):
        return ["L1 catalog needs a questions list"]
    ids = [q.get("id") for q in qs]
    if len(set(ids)) != len(ids):
        e.append("L1 duplicate question ids")
    if not REQUIRED_Q <= set(ids):
        e.append(f"L1 missing questions {sorted(REQUIRED_Q - set(ids))}")
    for q in qs:
        w = f"L1 {q.get('id')}"
        if q.get("type") not in ("choice", "noul", "score"):
            e.append(f"{w}: unknown type")
            continue
        if not isinstance(q.get("instructions"), str) or not q["instructions"].strip():
            e.append(f"{w}: instructions required")
        if not isinstance(q.get("revision"), int) or q["revision"] < 1:
            e.append(f"{w}: revision must be a positive integer")
        if q.get("rule") not in RULE_NAMES:
            e.append(f"{w}: rule must be one of {sorted(RULE_NAMES)}")
        if any(k in q for k in ("threshold", "thresholds", "cutoff")):
            e.append(f"{w}: thresholds belong in qualification records, not the catalog")
        crit = q.get("criteria")
        if q["type"] == "choice" and (not isinstance(crit, dict) or not 2 <= len(crit) <= 255):
            e.append(f"{w}: choice needs 2 to 255 criteria")
        if q["type"] == "score" and (not isinstance(crit, list) or not 2 <= len(crit) <= 10):
            e.append(f"{w}: score needs 2 to 10 ordered criteria")
        auth = q.get("authority")
        if auth not in ("shadow", "brake", "smoke"):
            e.append(f"{w}: authority must be shadow, brake or smoke")
        if auth == "brake":
            eff = q.get("effect", {})
            if eff.get("effect") not in BRAKE_EFFECTS:
                e.append(f"{w}: brake effect must be one of {sorted(BRAKE_EFFECTS)}")
            if q["type"] == "choice" and (not eff.get("on_options") or not set(eff["on_options"]) <= set(crit or {})):
                e.append(f"{w}: a choice brake must name existing options")
        elif "effect" in q:
            e.append(f"{w}: only brake questions carry an effect")
    return e


def validate_goal(g):
    e = []
    for k in ("id", "objective", "option"):
        if not isinstance(g.get(k), str) or not g[k].strip():
            e.append(f"L2 goal.{k} required")
    if g.get("situation") not in SITUATIONS:
        e.append("L2 goal.situation must be A01 to A12")
    if g.get("profile") not in PROFILES:
        e.append(f"L2 goal.profile must be one of {sorted(PROFILES)}")
    acc = g.get("acceptance")
    if not isinstance(acc, list) or not acc:
        e.append("L2 goal.acceptance needs at least one check")
    else:
        names = [c.get("name") for c in acc]
        if len(set(names)) != len(names):
            e.append("L2 acceptance check names must be unique")
        for c in acc:
            if not isinstance(c.get("argv"), list) or not c["argv"] or not all(isinstance(a, str) for a in c["argv"]):
                e.append(f"L2 check {c.get('name')}: argv must be a non-empty list of strings, not a shell string")
            if not _num(c.get("timeout_seconds")) or c["timeout_seconds"] <= 0:
                e.append(f"L2 check {c.get('name')}: timeout_seconds required")
            if not isinstance(c.get("description"), str) or not c["description"].strip():
                e.append(f"L2 check {c.get('name')}: description required")
    if not isinstance(g.get("protected_paths"), list):
        e.append("L2 goal.protected_paths must be a list (it may be empty)")
    for pl in g.get("prior_lineage", []):
        if not isinstance(pl, dict) or not pl.get("harness") or not isinstance(pl.get("families"), list):
            e.append("L2 prior_lineage entries need a harness and a families list")
    return e


def validate_controller(c, g=None, catalog=None):
    e = []
    if c.get("mode") not in ("shadow", "advisory"):
        e.append("L4 mode must be shadow or advisory")
    caps = c.get("caps", {})
    lim = {"max_iterations": (1, 50), "wall_clock_seconds": (60, 86400), "no_progress_streak": (1, 20),
           "fix_verify_cycles": (1, 20), "per_call_seconds": (1, 86400)}
    for k, (lo, hi) in lim.items():
        if not _num(caps.get(k)) or not lo <= caps[k] <= hi:
            e.append(f"L3 caps.{k} must be between {lo} and {hi}")
    if not _num(caps.get("budget_usd")) or caps["budget_usd"] <= 0:
        e.append("L3 caps.budget_usd must be a positive number")
    d = c.get("decision", {})
    b = d.get("backend", {})
    e += _backend(b)
    if catalog is None:
        try:
            catalog = json.load(io.open(os.path.join(ROOT, d.get("questions", "")), encoding="utf-8"))
        except (OSError, ValueError):
            e.append("L1 decision.questions must name a readable catalog")
            catalog = {"questions": []}
    e += validate_catalog(catalog)
    qmap = {q.get("id"): q for q in catalog.get("questions", [])}
    if c.get("mode") == "advisory":
        fam = d.get("lineage", {}).get("base_family")
        if not fam or fam in ("undisclosed", "unknown"):
            e.append("L6 advisory mode needs decision.lineage.base_family")
        quals = c.get("qualifications", [])
        if not quals:
            e.append("L6 advisory mode needs at least one qualification record")
        pinned = _models(b)
        for qr in quals:
            q = qmap.get(qr.get("question_id"), {})
            if q.get("authority") not in ("brake", "smoke"):
                e.append(f"L6 qualification for {qr.get('question_id')}: not a brake or smoke question")
            if qr.get("revision") != q.get("revision"):
                e.append(f"L6 qualification for {qr.get('question_id')}: revision does not match the catalog")
            if qr.get("method") != "learn-then-test-fixed-sequence":
                e.append("L6 qualification method must be learn-then-test-fixed-sequence")
            if not _num(qr.get("labelled")) or qr["labelled"] < 100:
                e.append("L6 qualification needs at least 100 labelled decisions")
            for k in ("alpha", "delta"):
                if not _num(qr.get(k)) or not 0 < qr[k] <= 0.1:
                    e.append(f"L6 qualification {k} must be in (0, 0.1]")
            t = qr.get("threshold")
            if not _num(t) or not 0 < t <= 1:
                e.append("L6 qualification threshold must be in (0, 1]")
            if qr.get("model") not in pinned:
                e.append(f"L6 qualification model {qr.get('model')} is not the backend's pinned model")
            if not isinstance(qr.get("locale"), str):
                e.append("L6 qualification needs a locale")
    if g and g.get("profile") == "ultimate" and b.get("kind") in ("http", "dual") \
            and not d.get("egress", {}).get("hk_reachable_verified"):
        e.append("L7 ultimate profile: decision endpoint not verified as Hong Kong reachable and policy eligible")
    w = c.get("worker", {})
    if w.get("kind") == "omo":
        if not isinstance(w.get("binary"), str) or w["binary"].startswith(("bunx", "npx")):
            e.append("L8 omo worker needs a local pinned binary path, not a runtime package download")
        if w.get("pinned_version") != "4.19.4":
            e.append("L8 omo worker must pin 4.19.4")
        if not w.get("agent"):
            e.append("L8 omo worker needs an agent")
        hooks = set(c.get("materialize", {}).get("disabled_hooks", []))
        if not REQUIRED_HOOKS <= hooks:
            e.append(f"L8 materialize.disabled_hooks must include {sorted(REQUIRED_HOOKS)}")
    elif w.get("kind") not in ("command", "fake"):
        e.append("L8 worker kind must be omo, command or fake")
    for r in c.get("reviewers", []):
        if r.get("harness") in (None, "", "opencode-omo"):
            e.append("L9 reviewer needs a harness other than opencode-omo")
        if r.get("kind") == "command" and (not isinstance(r.get("argv"), list) or not r["argv"]):
            e.append(f"L9 reviewer {r.get('harness')}: argv must be a list")
        if r.get("kind") not in ("command", "fake"):
            e.append(f"L9 reviewer {r.get('harness')}: kind must be command or fake")
    res = c.get("reservations_usd", {})
    if not _num(res.get("worker_call")) or res["worker_call"] <= 0:
        e.append("L10 reservations_usd.worker_call must be above zero")
    for k, v in res.items():
        if not _num(v) or v < 0:
            e.append(f"L10 reservations_usd.{k} must be non-negative")
    return e


def _backend(b):
    e = []
    k = b.get("kind")
    if k == "http":
        if not str(b.get("base_url", "")).startswith("https://"):
            e.append("L5 http backend needs an https base_url")
        if not str(b.get("path", "")).startswith("/"):
            e.append("L5 http backend needs a path")
        if not b.get("model") or ALIAS.search(str(b.get("model"))):
            e.append("L5 http backend needs a pinned model ID, not an alias")
        if not ENV_NAME.match(str(b.get("api_key_env", ""))):
            e.append("L5 api_key_env must name an environment variable")
        if b.get("state_encoding", "object") not in ("object", "text"):
            e.append("L5 state_encoding must be object or text")
    elif k == "dual":
        if not b.get("consequential"):
            e.append("L5 dual backend needs consequential questions")
        e += _backend(b.get("first", {})) + _backend(b.get("second", {}))
    elif k not in ("rules", "replay"):
        e.append("L5 backend kind must be rules, replay, http or dual")
    return e


def _models(b):
    if b.get("kind") == "http":
        return {b.get("model")}
    if b.get("kind") == "dual":
        return _models(b.get("first", {})) | _models(b.get("second", {}))
    return {b.get("model", b.get("kind"))}


def check_pair(gp, cp):
    g = json.load(io.open(os.path.join(ROOT, gp), encoding="utf-8"))
    c = json.load(io.open(os.path.join(ROOT, cp), encoding="utf-8"))
    return validate_goal(g) + validate_controller(c, g)


def self_test():
    fails = 0
    g0 = json.load(io.open(os.path.join(ROOT, EXAMPLES[0][0]), encoding="utf-8"))
    c0 = json.load(io.open(os.path.join(ROOT, EXAMPLES[0][1]), encoding="utf-8"))
    cat0 = json.load(io.open(QUESTIONS, encoding="utf-8"))

    def expect(label, mutate, rule, target="controller"):
        nonlocal fails
        g, c, cat = copy.deepcopy(g0), copy.deepcopy(c0), copy.deepcopy(cat0)
        mutate({"goal": g, "controller": c, "catalog": cat})
        errs = validate_goal(g) + validate_controller(c, g, cat)
        hit = any(x.startswith(rule + " ") for x in errs)
        print(("  ok   " if hit else "  FAIL ") + f"{label} -> {rule}")
        fails += 0 if hit else 1

    def q(cat, i):
        return next(x for x in cat["questions"] if x["id"] == i)

    def advisory(m, **over):
        c = m["controller"]
        c["mode"] = "advisory"
        c["decision"]["lineage"]["base_family"] = "example-family"
        rec = {"question_id": "blocked", "revision": 1, "method": "learn-then-test-fixed-sequence", "labelled": 150,
               "alpha": 0.05, "delta": 0.05, "threshold": 0.9, "model": c["decision"]["backend"]["model"], "locale": "en"}
        rec.update(over)
        c["qualifications"] = [rec]

    base = validate_goal(g0) + validate_controller(c0, g0, cat0)
    print(("  ok   " if not base else "  FAIL ") + "committed examples are valid " + str(base[:3]))
    fails += 1 if base else 0
    expect("missing required question", lambda m: m["catalog"]["questions"].pop(), "L1")
    expect("threshold in the catalog", lambda m: q(m["catalog"], "blocked").__setitem__("threshold", 0.8), "L1")
    expect("authority over success", lambda m: q(m["catalog"], "goal_met").__setitem__("authority", "done"), "L1")
    expect("brake that succeeds", lambda m: q(m["catalog"], "blocked")["effect"].__setitem__("effect", "succeed"), "L1")
    expect("brake on a missing option", lambda m: q(m["catalog"], "progress")["effect"].__setitem__("on_options", ["nope"]), "L1")
    expect("one-option choice", lambda m: q(m["catalog"], "next_action").__setitem__("criteria", {"repair": "x"}), "L1")
    expect("shell string check", lambda m: m["goal"]["acceptance"][0].__setitem__("argv", "make test"), "L2")
    expect("bad situation", lambda m: m["goal"].__setitem__("situation", "A13"), "L2")
    expect("no acceptance", lambda m: m["goal"].__setitem__("acceptance", []), "L2")
    expect("endless iterations", lambda m: m["controller"]["caps"].__setitem__("max_iterations", 10 ** 6), "L3")
    expect("no budget", lambda m: m["controller"]["caps"].pop("budget_usd"), "L3")
    expect("control mode", lambda m: m["controller"].__setitem__("mode", "control"), "L4")
    expect("alias model", lambda m: m["controller"]["decision"]["backend"].__setitem__("model", "jev-latest"), "L5")
    expect("literal key", lambda m: m["controller"]["decision"]["backend"].__setitem__("api_key_env", "sk-abc123"), "L5")
    expect("plain http", lambda m: m["controller"]["decision"]["backend"].__setitem__("base_url", "http://x"), "L5")
    expect("advisory without lineage", lambda m: (advisory(m), m["controller"]["decision"]["lineage"].__setitem__("base_family", "undisclosed")), "L6")
    expect("advisory without qualification", lambda m: (advisory(m), m["controller"].__setitem__("qualifications", [])), "L6")
    expect("qualification on too few labels", lambda m: advisory(m, labelled=40), "L6")
    expect("qualification for another model", lambda m: advisory(m, model="other-1.0"), "L6")
    expect("qualification for a shadow question", lambda m: advisory(m, question_id="next_action"), "L6")
    expect("qualification on an old revision", lambda m: advisory(m, revision=9), "L6")
    expect("ultimate with unverified endpoint", lambda m: m["goal"].__setitem__("profile", "ultimate"), "L7")
    expect("runtime package download", lambda m: m["controller"]["worker"].__setitem__("binary", "bunx oh-my-openagent"), "L8")
    expect("omo continuation left on", lambda m: m["controller"]["materialize"]["disabled_hooks"].remove("todo-continuation-enforcer"), "L8")
    expect("unpinned omo", lambda m: m["controller"]["worker"].__setitem__("pinned_version", "5.1.48"), "L8")
    expect("reviewer on omo", lambda m: m["controller"]["reviewers"][0].__setitem__("harness", "opencode-omo"), "L9")
    expect("zero worker reservation", lambda m: m["controller"]["reservations_usd"].__setitem__("worker_call", 0), "L10")
    print("self-test " + ("passed" if not fails else f"FAILED ({fails})"))
    return 1 if fails else 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    pairs = [tuple(argv[:2])] if len(argv) >= 2 else EXAMPLES
    errs = []
    for gp, cp in pairs:
        errs += [f"{cp}: {x}" for x in check_pair(gp, cp)]
    for x in errs:
        print("  FAIL", x)
    print("superloop checks " + ("passed" if not errs else f"FAILED ({len(errs)})"))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
