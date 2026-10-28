"""Build the state a decision model sees, from host facts only.

Rules:
  1. Facts come from the controller: check exit codes, failing check names, tree hashes,
     protected-path hashes, review cluster counts, counters and budget. Nothing a worker
     wrote about itself enters as a fact. A worker's own status file is kept under
     "claims", labelled untrusted, and only its "blocked" value is used, because a false
     "blocked" can only stop the run.
  2. Owner text (objective and acceptance criteria) is included as written.
  3. Optional evidence spans from any extractor are admitted only when the text at the
     stated offsets of the original file equals the span. Offsets may be characters or
     bytes; the unit must be stated. Rejected spans are logged, never sent.
  4. The state must fit the backend's token budget. Spans are dropped first. If required
     facts still do not fit, building fails and the driver treats every answer as an
     abstention.
  5. Secrets that look like API keys are redacted from every string.
"""
import json, os, re

SECRET = re.compile(r"(sk-[A-Za-z0-9_-]{12,}|(?i:bearer)\s+[A-Za-z0-9._-]{16,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{20,})")
MAX_SPANS = 20
MAX_SPAN_CHARS = 600
MAX_FAILING = 30


def tokens(obj):
    """Rough token estimate: 4 characters per token. Deliberately conservative for code."""
    return len(json.dumps(obj, ensure_ascii=False)) // 4 + 1


def redact(x):
    if isinstance(x, str):
        return SECRET.sub("[redacted]", x)
    if isinstance(x, list):
        return [redact(v) for v in x]
    if isinstance(x, dict):
        return {k: redact(v) for k, v in x.items()}
    return x


def verify_span(root, span):
    """Return (ok, reason). span = {"path", "start", "end", "text", "unit": "char"|"byte"}."""
    path = os.path.normpath(os.path.join(root, span.get("path", "")))
    if not path.startswith(os.path.normpath(root) + os.sep) or not os.path.isfile(path):
        return False, "path outside the worktree or missing"
    s, e, unit = span.get("start"), span.get("end"), span.get("unit")
    if not isinstance(s, int) or not isinstance(e, int) or s < 0 or e <= s:
        return False, "bad offsets"
    if unit not in ("char", "byte"):
        return False, "unit must be char or byte"
    raw = open(path, "rb").read()
    if unit == "byte":
        got = raw[s:e].decode("utf-8", errors="strict") if e <= len(raw) else None
    else:
        text = raw.decode("utf-8", errors="replace")
        got = text[s:e] if e <= len(text) else None
    if got is None:
        return False, "offsets past the end of the file"
    if got != span.get("text"):
        return False, "text at the offsets differs from the span"
    if len(got) > MAX_SPAN_CHARS:
        return False, "span too long"
    return True, "ok"


def build(goal, facts, claims=None, spans=None, root=None, budget_tokens=30000):
    """Return (state, report). report lists dropped spans and truncations."""
    report = {"spans_rejected": [], "spans_dropped": 0, "truncated": []}
    f = dict(facts)
    if len(f.get("failing_checks", [])) > MAX_FAILING:
        f["failing_checks"] = sorted(f["failing_checks"])[:MAX_FAILING]
        f["failing_checks_truncated"] = True
        report["truncated"].append("failing_checks")
    ok_spans = []
    for sp in (spans or [])[:MAX_SPANS]:
        good, why = verify_span(root, sp) if root else (False, "no root")
        if good:
            ok_spans.append({k: sp[k] for k in ("path", "start", "end", "unit", "text")})
        else:
            report["spans_rejected"].append({"path": sp.get("path"), "reason": why})
    state = {
        "goal": {"id": goal["id"], "situation": goal["situation"], "objective": goal["objective"],
                 "acceptance": [c["description"] for c in goal["acceptance"]]},
        "facts": f,
        "claims": {"untrusted": True, "worker_status": (claims or {}).get("status", "none")},
        "evidence_spans": ok_spans,
    }
    state = redact(state)
    while tokens(state) > budget_tokens and state["evidence_spans"]:
        state["evidence_spans"].pop()
        report["spans_dropped"] += 1
    if tokens(state) > budget_tokens:
        raise ValueError("required facts do not fit the decision budget")
    return state, report
