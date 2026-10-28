#!/usr/bin/env python3
"""Run the model-mesh superloop: a bounded outer loop that drives omo workers for one goal,
asks a typed decision model at fixed forks, and accepts work only on evidence.

Usage:
  python scripts/mm-superloop.py --goal GOAL.json --controller CONTROLLER.json \
      --worktree PATH --out runs/RUN_ID
  python scripts/mm-superloop.py --self-test

The worktree must be a git checkout with a clean HEAD; the run never commits, pushes or merges.
Create runs/RUN_ID/STOP to stop a run at the next iteration boundary.
Exit codes: 0 verified (pending the owner's merge), 2 stopped without success, 3 refused at
admission, 1 internal error.

The self-test runs every scenario offline: a temporary git repository, fake workers, fake
reviewers and recorded decision answers. MM_OFFLINE=1 is set, so no request can leave the machine.
"""
import argparse, copy, json, os, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from superloop import control, decide, ledger, qualify, state as statemod  # noqa: E402

ROOT = control.ROOT


def run(goal, controller, worktree, out, deps=None):
    return control.Run(goal, controller, worktree, out, deps).run()


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal")
    ap.add_argument("--controller")
    ap.add_argument("--worktree")
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not all([a.goal, a.controller, a.worktree, a.out]):
        ap.error("--goal, --controller, --worktree and --out are required")
    goal = json.load(open(a.goal, encoding="utf-8"))
    ctl = json.load(open(a.controller, encoding="utf-8"))
    res = run(goal, ctl, a.worktree, a.out)
    print(json.dumps({k: res[k] for k in ("status", "success", "detail", "reserved_usd")}, indent=2))
    if res["success"]:
        return 0
    return 3 if res["status"] == "policy_denied" else 2


# ---------------------------------------------------------------------------
# offline self-test

CHECK = ["python3", "-c", "import pathlib,sys; sys.exit(0 if pathlib.Path('{f}').exists() else 1)"]


def make_repo(tmp):
    wt = os.path.join(tmp, "wt")
    os.makedirs(os.path.join(wt, "tests"))
    open(os.path.join(wt, "tests", "spec.txt"), "w").write("protected\n")
    open(os.path.join(wt, "README.md"), "w").write("demo\n")
    for args in (["init", "-q"], ["config", "user.email", "t@example.invalid"], ["config", "user.name", "t"],
                 ["add", "-A"], ["commit", "-q", "-m", "init"]):
        subprocess.run(["git", "-C", wt] + args, check=True, capture_output=True)
    return wt


def base_goal():
    return {"id": "t", "objective": "Create a.txt and b.txt.", "situation": "A02", "profile": "hybrid",
            "option": "primary", "protected_paths": ["tests"], "owner_approval_required": True,
            "acceptance": [{"name": "a", "description": "a.txt exists", "argv": [x.format(f="a.txt") for x in CHECK], "timeout_seconds": 30},
                           {"name": "b", "description": "b.txt exists", "argv": [x.format(f="b.txt") for x in CHECK], "timeout_seconds": 30}]}


def seat_harnesses():
    """Reviewer harnesses and families from the matrix, so the test names no vendor."""
    m = control.assign.load_matrix()
    a02 = control.assign.assignment(m, "A02", "hybrid", "primary")
    a06 = control.assign.assignment(m, "A06", "hybrid", "primary")
    return a02["reviewers"][0], a06["reviewers"][1]


def base_controller():
    first, second = seat_harnesses()
    c = json.load(open(os.path.join(ROOT, "examples", "superloop", "controller.rules.example.json"), encoding="utf-8"))
    c["worker"] = {"kind": "fake", "name": "worker"}
    c["reviewers"] = [{"harness": first["harness"], "kind": "fake", "name": "reviewer"},
                      {"harness": second["harness"], "kind": "fake", "name": "reviewer2"}]
    c["materialize"] = {"fragment": "profiles/hybrid.example.json", "disabled_hooks": ["goal", "todo-continuation-enforcer", "start-work", "atlas"], "always": True}
    return c


def writer(steps):
    """Fake worker: steps maps iteration -> list of (path, text) to write; missing means no-op."""
    def fn(wt, prompt, it, extra):
        for path, text in steps.get(it, []):
            full = os.path.join(wt, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, "w").write(text)
        return {"exit_code": 0, "reported": {"agent": "sisyphus"}}
    return fn


def reviewer(findings_by_call):
    calls = {"n": 0}

    def fn(wt, prompt, it, extra):
        calls["n"] += 1
        items = findings_by_call(calls["n"], it)
        json.dump(items, open(extra["findings_out"], "w"))
        return {"exit_code": 0}
    return fn


def clean(*_):
    return []


def blocker_once(n, it):
    if n == 1:
        return [{"id": "1", "lens": "contract-fit", "harness": "goose", "family": "fam-r", "severity": "blocker",
                 "category": "correctness", "path": "a.txt", "line_start": 1, "line_end": 1,
                 "claim": "a.txt is hollow", "evidence": "line 1"}]
    return []


def recording(answers, default=None):
    return {"kind": "replay", "model": "rec-1.0", "recording": {"answers": answers, "default": default or {}}}


def self_test():
    os.environ["MM_OFFLINE"] = "1"
    fails = 0
    results = {}

    def scenario(label, want, steps=None, rev=clean, goal_mut=None, ctl_mut=None, deps_mut=None, check=None):
        nonlocal fails
        tmp = tempfile.mkdtemp()
        try:
            wt = make_repo(tmp)
            g, c = base_goal(), base_controller()
            if goal_mut:
                goal_mut(g)
            if ctl_mut:
                ctl_mut(c)
            deps = {"fakes": {"worker": writer(steps or {}), "reviewer": reviewer(rev), "reviewer2": reviewer(clean)}}
            if deps_mut:
                deps_mut(deps, tmp)
            out = os.path.join(tmp, "run")
            res = run(g, c, wt, out, deps)
            ok = res["status"] == want and (check is None or check(res, out, wt))
            ok = ok and ledger.verify_chain(os.path.join(out, "events.jsonl")) if os.path.exists(os.path.join(out, "events.jsonl")) else ok
            results[label] = res
            print(("  ok   " if ok else "  FAIL ") + f"{label}: {res['status']} ({res['detail']})")
            fails += 0 if ok else 1
        finally:
            shutil.rmtree(tmp)

    done2 = {1: [("a.txt", "a\n")], 2: [("b.txt", "b\n")]}

    def events(out, kind):
        return [json.loads(l) for l in open(os.path.join(out, "events.jsonl")) if json.loads(l)["kind"] == kind]

    def omo_config_ok(res, out, wt):
        cfg = json.load(open(os.path.join(wt, ".omo", "omo.jsonc")))
        b = cfg["[opencode]"]
        return b["goal"] == {"enabled": False} and {"goal", "todo-continuation-enforcer", "start-work"} <= set(b["disabled_hooks"])

    scenario("converges after two batches, review clean", "verified_pending_owner", done2, check=omo_config_ok)
    scenario("never converges, stops at the iteration cap", "cap_iterations",
             {i: [(f"n{i}.txt", "x")] for i in range(1, 30)}, ctl_mut=lambda c: c["caps"].update(max_iterations=4, fix_verify_cycles=20))
    scenario("worker claims done while checks fail", "no_progress",
             {1: [(".superloop/status.json", '{"status": "done"}'), ("claim.md", "ALL GOALS MET")]})
    scenario("worker edits a protected test", "blocked_human", {1: [("tests/spec.txt", "weakened\n")]})
    scenario("hollow pass: checks green, reviewer blocker, then fixed", "verified_pending_owner",
             {1: [("a.txt", "a\n"), ("b.txt", "b\n")], 2: [("a.txt", "a real\n")]}, rev=blocker_once)
    scenario("no progress for two batches", "no_progress", {})
    scenario("same failure three times", "fix_cycles_exhausted",
             {i: [(f"n{i}.txt", "x")] for i in range(1, 30)}, ctl_mut=lambda c: c["caps"].update(max_iterations=20, fix_verify_cycles=3))
    scenario("worker reports blocked", "blocked_human", {1: [(".superloop/status.json", '{"status": "blocked", "reason": "credential"}')]})
    scenario("stop file", "cancelled", done2, deps_mut=lambda d, tmp: (os.makedirs(os.path.join(tmp, "run")), open(os.path.join(tmp, "run", "STOP"), "w").close()))

    def slow_clock(d, tmp):
        t = {"v": 0.0}

        def clock():
            t["v"] += 400.0
            return t["v"]
        d["clock"] = clock
    scenario("wall clock cap", "cap_wall_clock", {i: [(f"n{i}.txt", "x")] for i in range(1, 30)},
             ctl_mut=lambda c: c["caps"].update(fix_verify_cycles=20), deps_mut=slow_clock)
    scenario("budget cap before dispatch", "cap_budget", done2, ctl_mut=lambda c: c["caps"].update(budget_usd=0.5))
    scenario("worker ran as an unexpected agent", "policy_denied", done2,
             ctl_mut=lambda c: c["worker"].update(expect_agents=["prometheus"]))
    scenario("option not on opencode-omo", "policy_denied", done2, goal_mut=lambda g: g.update(situation="A05"),
             ctl_mut=lambda c: c["worker"].update(kind="omo", binary="./x", pinned_version="4.19.4", agent="sisyphus"))
    scenario("ultimate with a remote decision endpoint", "policy_denied", done2,
             goal_mut=lambda g: g.update(profile="ultimate"),
             ctl_mut=lambda c: c["decision"].update(backend={"kind": "http", "base_url": "https://example.invalid", "path": "/v1/x",
                                                             "model": "m-1.0", "api_key_env": "X_KEY"},
                                                    egress={"hk_reachable_verified": False}))
    scenario("advisory mode without qualification is refused", "policy_denied", done2,
             ctl_mut=lambda c: c.update(mode="advisory"))

    def no_independent_reviewer(c):
        c["reviewers"] = [{"harness": "opencode-omo-shadow", "kind": "fake", "name": "reviewer"}]
    scenario("no reviewer seat matches the assignment", "review_unavailable", done2, ctl_mut=no_independent_reviewer)

    def lineage_conflict(g):
        g["prior_lineage"] = [{"harness": "dsh", "families": list(seat_harnesses()[0]["families"]),
                               "note": "an earlier segment under another profile"}]
    scenario("reviewer family authored earlier in the lineage", "review_unavailable", done2,
             goal_mut=lineage_conflict, ctl_mut=lambda c: c.update(reviewers=[c["reviewers"][0]]))

    # decision-model scenarios
    shadow_rec = recording({"1": {"blocked": {"type": "noul", "noul": 0.99},
                                  "progress": {"type": "choice", "choice": "stalled", "probabilities": {"stalled": 0.97, "regressing": 0.01, "drifting": 0.01, "progressing": 0.01}}}})

    def shadow(c):
        c["decision"]["backend"] = shadow_rec
    scenario("shadow: a confident brake changes nothing", "verified_pending_owner", done2, ctl_mut=shadow,
             check=lambda r, o, w: r["disagreements"] >= 2)

    def advisory(c, qid="blocked", thr=0.9, model="rec-1.0"):
        c["decision"]["backend"] = shadow_rec
        c["mode"] = "advisory"
        c["decision"]["lineage"] = {"provider": "test", "model": "rec-1.0", "base_family": "fam-decider"}
        c["qualifications"] = [{"question_id": qid, "revision": 1, "method": "learn-then-test-fixed-sequence",
                                "labelled": 150, "alpha": 0.05, "delta": 0.05, "threshold": thr, "model": model, "locale": "en"}]
    scenario("advisory: a qualified brake pauses for a person", "blocked_human", done2, ctl_mut=advisory)
    scenario("advisory: an unqualified question cannot act", "verified_pending_owner", done2,
             ctl_mut=lambda c: (advisory(c, qid="needs_human")))
    scenario("advisory: a brake below its qualified threshold cannot act", "verified_pending_owner", done2,
             ctl_mut=lambda c: advisory(c, thr=0.995))
    done_rec = recording({}, default={"goal_met": {"type": "noul", "noul": 0.99}})
    scenario("decision says done while checks fail: no effect", "no_progress", {},
             ctl_mut=lambda c: c["decision"].update(backend=done_rec))
    smoke_rec = recording({}, default={"goal_met": {"type": "noul", "noul": 0.05}})

    def smoke(c):
        advisory(c, qid="goal_met")
        c["decision"]["backend"] = smoke_rec
    scenario("advisory smoke detector adds every reviewer seat", "verified_pending_owner", done2, ctl_mut=smoke,
             goal_mut=lambda g: g.update(situation="A06"),
             check=lambda r, o, w: len(r.get("review", [])) == 2)
    outage = recording({}, default={"_outage": True})
    scenario("decision outage falls back to rules", "verified_pending_owner", done2,
             ctl_mut=lambda c: c["decision"].update(backend=outage))
    scenario("offline guard blocks a real endpoint", "verified_pending_owner", done2,
             ctl_mut=lambda c: c["decision"].update(backend={"kind": "http", "base_url": "https://example.invalid", "path": "/v1/x",
                                                             "model": "m-1.0", "api_key_env": "X_KEY"}),
             check=lambda r, o, w: any((e.get("model") or {}).get("error", "") and "MM_OFFLINE" in e["model"]["error"]
                                       for e in events(o, "decision")))
    bad = recording({}, default={"progress": {"type": "choice", "choice": "teleport", "probabilities": {"teleport": 1.0}},
                                 "blocked": {"type": "noul", "noul": 7}})
    scenario("malformed answers become abstentions", "verified_pending_owner", done2,
             ctl_mut=lambda c: c["decision"].update(backend=bad),
             check=lambda r, o, w: all(e["model"]["answers"]["blocked"]["type"] == "abstain" for e in events(o, "decision") if "blocked" in e["model"]["answers"]))

    # unit checks on the parts
    def ok(label, cond):
        nonlocal fails
        print(("  ok   " if cond else "  FAIL ") + label)
        fails += 0 if cond else 1
    tmp = tempfile.mkdtemp()
    try:
        p = os.path.join(tmp, "log.txt")
        open(p, "w", encoding="utf-8").write("ok\n錯誤 E42 at line 3\n")
        text = open(p, encoding="utf-8").read()
        s = text.index("E42")
        ok("char span accepted", statemod.verify_span(tmp, {"path": "log.txt", "start": s, "end": s + 3, "text": "E42", "unit": "char"})[0])
        bs = open(p, "rb").read().index(b"E42")
        ok("byte span accepted", statemod.verify_span(tmp, {"path": "log.txt", "start": bs, "end": bs + 3, "text": "E42", "unit": "byte"})[0])
        ok("byte offsets read as chars rejected", not statemod.verify_span(tmp, {"path": "log.txt", "start": bs, "end": bs + 3, "text": "E42", "unit": "char"})[0])
        ok("span outside the worktree rejected", not statemod.verify_span(tmp, {"path": "../x", "start": 0, "end": 1, "text": "x", "unit": "char"})[0])
        g = base_goal()
        st, rep = statemod.build(g, {"checks_failed": 1}, {"status": "done"}, [{"path": "log.txt", "start": 0, "end": 2, "text": "no", "unit": "char"}], tmp)
        ok("mismatched span is never sent", st["evidence_spans"] == [] and rep["spans_rejected"])
        ok("worker narrative is not a fact", st["claims"]["untrusted"] and "worker_status" in st["claims"] and "status" not in st["facts"])
        st2, _ = statemod.build(g, {"note": "key sk-abcdefghijklmnop1234"}, root=tmp)
        ok("secrets are redacted", "sk-" not in json.dumps(st2))
        try:
            statemod.build(g, {"failing_checks": ["x" * 50] * 10}, root=tmp, budget_tokens=50)
            ok("over-budget required facts fail closed", False)
        except ValueError:
            ok("over-budget required facts fail closed", True)
    finally:
        shutil.rmtree(tmp)
    wire = decide.wire_questions({"q": {"type": "choice", "instructions": "x", "criteria": {"a": "", "b": "", "c": ""}}}, ["q"], {"q": ["a", "b"]})
    ok("menus remove options the host does not allow", list(wire["q"]["criteria"]) == ["a", "b"])
    n = decide.normalize({"q": {"type": "choice", "choice": "b", "probabilities": {"a": 0.7, "b": 0.3}}}, wire)
    ok("a choice that is not the most probable abstains", n["q"]["type"] == "abstain")
    n = decide.normalize({"q": {"type": "choice", "choice": "a", "probabilities": {"a": 0.61, "b": 0.38}}}, wire)
    ok("rounded probabilities are accepted with margin", n["q"]["type"] == "choice" and abs(n["q"]["margin"] - 0.23) < 1e-9)
    sw = {"s": {"type": "score", "instructions": "x", "criteria": ["lo", "mid", "hi"]}}
    n = decide.normalize({"s": {"type": "score", "score": 1.2, "probabilities": {"0": 0.2, "1": 0.4, "2": 0.4}}}, sw)
    ok("score with a legend-keyed distribution", n["s"]["type"] == "score")
    hb = decide.HttpBackend({"model": "m", "state_encoding": "text"})
    ok("text encoding serializes the whole state", json.loads(hb.payload({"a": 1}, {})["state"]["text"]) == {"a": 1})
    labelled = [{"score": 0.99, "correct": True}] * 140 + [{"score": 0.6, "correct": False}] * 20 + [{"score": 0.97, "correct": False}] * 2
    q = qualify.qualify(labelled, alpha=0.05, delta=0.05, grid=[0.99, 0.95, 0.9, 0.5])
    ok("learn-then-test stops at the first threshold it cannot certify", q["threshold"] == 0.9 and q["errors"] == 2
       and q["tested"][-1]["threshold"] == 0.5 and not q["tested"][-1]["rejected"])
    q2 = qualify.qualify([{"score": 0.99, "correct": False}] * 50, alpha=0.05, delta=0.05, grid=[0.9])
    ok("a wrong model qualifies nothing", q2["threshold"] is None)
    ok("binomial tail sanity", abs(qualify.binom_cdf(0, 10, 0.1) - 0.9 ** 10) < 1e-12)
    print("self-test " + ("passed" if not fails else f"FAILED ({fails})"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
