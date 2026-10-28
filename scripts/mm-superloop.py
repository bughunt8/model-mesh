#!/usr/bin/env python3
"""Run the model-mesh superloop: a bounded outer loop that drives omo workers for one goal,
asks a typed decision model at fixed forks, and accepts work only on evidence.

Usage:
  python scripts/mm-superloop.py --goal GOAL.json --controller CONTROLLER.json \
      --worktree PATH --out runs/RUN_ID
  python scripts/mm-superloop.py --init-registry [PATH]
  python scripts/mm-superloop.py --self-test

Before the first run, the owner creates the lineage registry once (--init-registry; default
~/.local/state/model-mesh/superloop-lineage.jsonl or MM_SUPERLOOP_REGISTRY) and writes the tools
registry (~/.config/model-mesh/superloop-tools.json or MM_SUPERLOOP_TOOLS; template in
examples/superloop/tools.example.json). Both live outside every worktree.

The worktree must be a git checkout with a clean HEAD; the run never commits, pushes or merges.
Create runs/RUN_ID/STOP to stop a run at the next iteration boundary.
Exit codes: 0 verified (pending the owner's merge), 2 stopped without success, 3 refused at
admission, 1 internal error.

The self-test runs every scenario offline: a temporary git repository, fake workers, fake
reviewers and recorded decision answers. MM_OFFLINE=1 is set, so no request can leave the machine.
"""
import argparse, copy, json, os, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from superloop import control, decide, ledger, qualify, state as statemod, workers  # noqa: E402

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
    ap.add_argument("--init-registry", nargs="?", const="", default=None)
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.init_registry is not None:
        reg = ledger.Registry(a.init_registry or ledger.default_registry())
        made = reg.init()
        print(("created " if made else "already exists: ") + reg.path)
        return 0
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


def check_for(name, f):
    return {"name": name, "description": f"{f} exists", "argv": [x.format(f=f) for x in CHECK], "timeout_seconds": 30}


def base_goal():
    return {"id": "t", "objective": "Create a.txt and b.txt.", "situation": "A02", "profile": "hybrid",
            "option": "primary", "protected_paths": ["tests"], "owner_approval_required": True,
            "acceptance": [check_for("a", "a.txt"), check_for("b", "b.txt")]}


def cell():
    return control.assign.assignment(control.assign.load_matrix(), "A02", "hybrid", "primary")


def seat_harnesses():
    """Reviewer harnesses from the matrix, so the test names no vendor."""
    m = control.assign.load_matrix()
    a06 = control.assign.assignment(m, "A06", "hybrid", "primary")
    return cell()["reviewers"][0], a06["reviewers"][1]


def worker_model():
    return cell()["orchestrator"]["model_ids"][0]


def base_controller():
    first, _ = seat_harnesses()
    c = json.load(open(os.path.join(ROOT, "examples", "superloop", "controller.rules.example.json"), encoding="utf-8"))
    c["worker"] = {"kind": "fake", "name": "worker", "agent": "sisyphus", "expect_agents": ["sisyphus"], "isolation": "container"}
    c["reviewers"] = [{"harness": first["harness"], "kind": "fake", "name": "reviewer"}]
    return c


def two_seat_matrix():
    """Test-only matrix: A02 hybrid primary gains a second reviewer seat on a family no author uses."""
    m = copy.deepcopy(control.assign.load_matrix())
    _, second = seat_harnesses()
    key = next(k for k, v in m["models"]["hybrid"].items() if control.assign.family_of(v["id"]) == "openai")
    opt = next(s for s in m["situations"] if s["id"] == "A02")["profiles"]["hybrid"]["options"][0]
    opt["reviewers"].append({"role": "reviewer-2", "harness": second["harness"], "chain": [key],
                             "lenses": ["contract-fit"], "seat": "reviewer-2"})
    return m


def writer(steps, report=None):
    """Fake worker: steps maps iteration -> list of (path, text); text None deletes the path."""
    def fn(wt, prompt, it, extra):
        for path, text in steps.get(it, []):
            full = os.path.join(wt, path)
            if text is None:
                os.remove(full)
                continue
            os.makedirs(os.path.dirname(full), exist_ok=True)
            open(full, "w").write(text)
        return {"exit_code": 0, "reported": report if report is not None else
                {"agents": ["sisyphus"], "models": [worker_model()]}}
    return fn


def finding(sev, path="a.txt", n="1", extra=None):
    f = {"id": n, "lens": "contract-fit", "harness": "goose", "family": "fam-r", "severity": sev,
         "category": "correctness", "path": path, "line_start": 1, "line_end": 1,
         "claim": f"{path} is hollow", "evidence": "line 1"}
    f.update(extra or {})
    return f


def reviewer(findings_by_call, side=None):
    calls = {"n": 0}

    def fn(rdir, prompt, it, extra):
        calls["n"] += 1
        if side:
            r = side(rdir, calls["n"], extra)
            if r is not None:
                return r
        return {"exit_code": 0, "stdout": "review done\n" + json.dumps(findings_by_call(calls["n"], it))}
    return fn


def clean(*_):
    return []


def blocker_once(n, it):
    return [finding("blocker")] if n == 1 else []


def recording(answers, default=None):
    return {"kind": "replay", "model": "rec-1.0", "recording": {"answers": answers, "default": default or {}}}


def make_record(tmp, question, scores, grid):
    ds = os.path.join(tmp, f"labels-{question}.json")
    json.dump([{"score": scores, "correct": True, "label_source": "human"}] * 150, open(ds, "w"))
    rec = qualify.make_record(ds, 0.05, 0.05, grid, "rec-1.0", question, 1, "en")
    path = os.path.join(tmp, f"record-{question}.json")
    json.dump(rec, open(path, "w"))
    return path


def self_test():
    os.environ["MM_OFFLINE"] = "1"
    fails = 0

    def scenario(label, want, steps=None, rev=clean, goal_mut=None, ctl_mut=None, deps_mut=None, check=None,
                 report=None, rev2=clean, pre=None):
        nonlocal fails
        tmp = tempfile.mkdtemp()
        try:
            wt = make_repo(tmp)
            g, c = base_goal(), base_controller()
            ctx = {"tmp": tmp, "wt": wt, "out": os.path.join(tmp, "run")}
            if goal_mut:
                goal_mut(g)
            if ctl_mut:
                ctl_mut(c) if ctl_mut.__code__.co_argcount == 1 else ctl_mut(c, ctx)
            ledger.Registry(os.path.join(tmp, "lineage.jsonl")).init()
            deps = {"allow_fakes": True, "registry": os.path.join(tmp, "lineage.jsonl"),
                    "fakes": {"worker": writer(steps or {}, report),
                              "reviewer": rev(ctx) if rev.__code__.co_varnames[:1] == ("ctx",) else reviewer(rev),
                              "reviewer2": reviewer(rev2)}}
            if ctx.get("tools_data") is not None:
                json.dump(ctx["tools_data"], open(os.path.join(tmp, "tools.json"), "w"))
                deps["tools"] = os.path.join(tmp, "tools.json")
            if deps_mut:
                deps_mut(deps, ctx)
            if pre:
                pre(g, c, deps, ctx)
            res = run(g, c, wt, ctx["out"], deps)
            ok = res["status"] == want and (check is None or check(res, ctx["out"], wt))
            ev = os.path.join(ctx["out"], "events.jsonl")
            if os.path.exists(ev):
                ok = ok and ledger.verify_chain(ev)
            print(("  ok   " if ok else "  FAIL ") + f"{label}: {res['status']} ({str(res['detail'])[:110]})")
            fails += 0 if ok else 1
        finally:
            shutil.rmtree(tmp)

    done2 = {1: [("a.txt", "a\n")], 2: [("b.txt", "b\n")]}
    both = {1: [("a.txt", "a\n"), ("b.txt", "b\n")]}

    def events(out, kind):
        return [json.loads(l) for l in open(os.path.join(out, "events.jsonl")) if json.loads(l)["kind"] == kind]

    def omo_config_ok(res, out, wt):
        cfg = json.load(open(os.path.join(wt, ".omo", "omo.jsonc")))
        b = cfg["[opencode]"]
        fams = {control.assign.family_of(x) for x in control.config_models(cfg)}
        allowed = set().union(*[set(s["families"]) for s in cell()["authors"]]) | set(cell()["orchestrator"]["families"])
        return b["goal"] == {"enabled": False} and set(control.REQUIRED_HOOKS) <= set(b["disabled_hooks"]) \
            and {"goal", "start-work"} <= set(b["disabled_commands"]) and b["runtime_fallback"] == {"enabled": False} \
            and b["team_mode"]["enabled"] is False and fams <= allowed and "hephaestus" in b["disabled_agents"]

    # -- the loop works --------------------------------------------------------------------------
    scenario("converges after two batches, review clean, config restricted to the cell", "verified_pending_owner",
             done2, check=omo_config_ok)
    scenario("never converges, stops at the iteration cap", "cap_iterations",
             {i: [(f"n{i}.txt", "x")] for i in range(1, 30)}, ctl_mut=lambda c: c["caps"].update(max_iterations=4, fix_verify_cycles=20),
             check=lambda r, o, w: r["iterations"] == 4)
    scenario("worker claims done while checks fail", "no_progress",
             {1: [(".superloop/status.json", '{"status": "done"}'), ("claim.md", "ALL GOALS MET")]})
    scenario("worker edits a protected test", "blocked_human", {1: [("tests/spec.txt", "weakened\n")]})
    scenario("hollow pass: checks green, reviewer blocker, then fixed", "verified_pending_owner",
             {1: [("a.txt", "a\n"), ("b.txt", "b\n")], 2: [("a.txt", "a real\n")]}, rev=blocker_once)
    scenario("no progress: stops after exactly two idle batches", "no_progress", {},
             check=lambda r, o, w: r["iterations"] == 2 and "2 batches" in r["detail"])
    scenario("same failure three times", "fix_cycles_exhausted",
             {i: [(f"n{i}.txt", "x")] for i in range(1, 30)}, ctl_mut=lambda c: c["caps"].update(max_iterations=20, fix_verify_cycles=3))
    scenario("worker reports blocked", "blocked_human", {1: [(".superloop/status.json", '{"status": "blocked", "reason": "credential"}')]})
    scenario("stop file", "cancelled", done2, pre=lambda g, c, d, x: (os.makedirs(x["out"]),
             open(os.path.join(x["out"], "STOP"), "w").close()))

    def slow_clock(d, x):
        t = {"v": 0.0}

        def clock():
            t["v"] += 40.0
            return t["v"]
        d["clock"] = clock
    scenario("wall clock cap", "cap_wall_clock", {i: [(f"n{i}.txt", "x")] for i in range(1, 30)},
             ctl_mut=lambda c: c["caps"].update(fix_verify_cycles=20, max_iterations=50), deps_mut=slow_clock)
    scenario("budget cap before dispatch", "cap_budget", done2, ctl_mut=lambda c: c["caps"].update(budget_usd=0.5))
    scenario("worker ran as an unexpected agent", "policy_denied", done2,
             ctl_mut=lambda c: c["worker"].update(expect_agents=["prometheus"]))
    scenario("option not on opencode-omo", "policy_denied", done2, goal_mut=lambda g: g.update(situation="A05"))
    scenario("ultimate with a remote decision endpoint", "policy_denied", done2,
             goal_mut=lambda g: g.update(profile="ultimate"),
             ctl_mut=lambda c: c["decision"].update(backend={"kind": "http", "base_url": "https://example.invalid", "path": "/v1/x",
                                                             "model": "m-1.0", "api_key_env": "X_KEY"},
                                                    egress={"hk_reachable_verified": True}))
    scenario("advisory mode without qualification is refused", "policy_denied", done2,
             ctl_mut=lambda c: c.update(mode="advisory"))

    def no_independent_reviewer(c):
        c["reviewers"] = [{"harness": "opencode-omo-shadow", "kind": "fake", "name": "reviewer"}]
    scenario("no reviewer seat matches the assignment", "review_unavailable", done2, ctl_mut=no_independent_reviewer)

    def lineage_conflict(g):
        g["prior_lineage"] = [{"harness": "dsh", "families": list(seat_harnesses()[0]["families"]),
                               "note": "an earlier segment under another profile"}]
    scenario("reviewer family authored earlier in the lineage", "review_unavailable", done2, goal_mut=lineage_conflict)

    # -- forgeries from the independent review must fail --------------------------------------------
    def deleting_reviewer(ctx):
        def side(rdir, n, extra):
            os.remove(os.path.join(ctx["wt"], "a.txt"))
            return None
        return reviewer(clean, side)
    scenario("reviewer deletes a file after the checks", "policy_denied", both, rev=deleting_reviewer)

    def exit2_reviewer(ctx):
        return reviewer(clean, lambda rdir, n, extra: {"exit_code": 2, "timed_out": True})
    scenario("reviewer fails and writes nothing", "review_unavailable", both, rev=exit2_reviewer)

    def silent_reviewer(ctx):
        return reviewer(clean, lambda rdir, n, extra: {"exit_code": 0, "stdout": "looks fine to me\n"})
    scenario("a reviewer that prints no findings list", "review_unavailable", both, rev=silent_reviewer)

    def file_and_stdout(ctx):
        def side(rdir, n, extra):
            json.dump([], open(os.path.join(rdir, "findings.json"), "w"))
            return {"exit_code": 0, "stdout": json.dumps([finding("blocker")])}
        return reviewer(clean, side)
    scenario("a findings file in the review folder is ignored; the output stream counts", "fix_cycles_exhausted",
             {i: [(f"n{i}.txt", "x"), ("a.txt", "a\n"), ("b.txt", "b\n")] for i in range(1, 30)}, rev=file_and_stdout)

    def diff_has(text):
        def chk(r, o, w):
            p = os.path.join(o, "scratch", "review-001", "change.patch")
            return os.path.exists(p) and text in open(p).read()
        return chk
    scenario("files under .superloop are hashed and reviewed", "verified_pending_owner",
             {1: [("a.txt", "a\n"), ("b.txt", "b\n"), (".superloop/win", "PAYLOAD-W\n")]}, check=diff_has("PAYLOAD-W"))
    scenario("ignored files are hashed and reviewed", "verified_pending_owner",
             {1: [("a.txt", "a\n"), ("b.txt", "b\n"), (".gitignore", "secret.local\n"), ("secret.local", "PAYLOAD-I\n")]},
             check=diff_has("PAYLOAD-I"))
    scenario("worker rewrites the omo config", "policy_denied", {1: [(".omo/omo.jsonc", "{}\n")]})

    def jump_clock(d, x):
        t = {"v": 1000.0}
        d["clock"] = lambda: t["v"]
        inner = d["fakes"]["worker"]

        def fn(wt, prompt, it, extra):
            r = inner(wt, prompt, it, extra)
            t["v"] += 1825.0
            return r
        d["fakes"]["worker"] = fn
    scenario("clock runs out inside a batch that made the checks green", "cap_wall_clock", both, deps_mut=jump_clock)
    scenario("missing review reservation is refused", "policy_denied", both,
             ctl_mut=lambda c: c["reservations_usd"].pop("review_call"))
    scenario("a reused output directory is refused", "policy_denied", both,
             pre=lambda g, c, d, x: (os.makedirs(x["out"]), open(os.path.join(x["out"], "events.jsonl"), "w").close()))

    def registry_entry(g, c, d, x):
        wt = x["wt"]
        common = os.path.realpath(os.path.join(wt, control.git(wt, "rev-parse", "--git-common-dir")))
        ledger.Registry(d["registry"]).append({"repo_key": common, "goal": "earlier", "run": "r0",
                                               "status": "no_progress", "harnesses": ["dsh"],
                                               "families": list(seat_harnesses()[0]["families"])})
    scenario("an earlier run in the repository is inherited without prior_lineage", "review_unavailable", both, pre=registry_entry)
    scenario("renaming the branch and the goal does not drop the lineage", "review_unavailable", both,
             goal_mut=lambda g: g.update(id="renamed-goal"),
             pre=lambda g, c, d, x: (registry_entry(g, c, d, x), control.git(x["wt"], "branch", "-m", "hidden-branch")))
    scenario("a deleted lineage registry stops the run", "policy_denied", both,
             pre=lambda g, c, d, x: os.remove(d["registry"]))
    scenario("a lone major blocks success", "fix_cycles_exhausted", {i: [(f"n{i}.txt", "x"), ("a.txt", "a\n"), ("b.txt", "b\n")] for i in range(1, 30)},
             rev=lambda n, it: [finding("major")], ctl_mut=lambda c: c["caps"].update(fix_verify_cycles=3),
             check=lambda r, o, w: r["iterations"] == 3 and r["open_findings"])
    scenario("a defect that moves path each round still exhausts the cycles", "fix_cycles_exhausted",
             {i: [(f"n{i}.txt", "x"), ("a.txt", "a\n"), ("b.txt", "b\n")] for i in range(1, 30)},
             rev=lambda n, it: [finding("blocker", path=f"p{n}.txt")], ctl_mut=lambda c: c["caps"].update(fix_verify_cycles=3, max_iterations=6),
             check=lambda r, o, w: r["iterations"] == 3)
    scenario("missing agent report is refused", "policy_denied", both, report={})
    scenario("worker model outside the cell's families is refused", "policy_denied", both,
             report={"agents": ["sisyphus"], "models": [next(v["id"] for v in control.assign.load_matrix()["models"]["hybrid"].values()
                                                              if control.assign.family_of(v["id"]) == "openai")]})
    scenario("invalid findings with a blocker stop the run", "review_unavailable", both,
             rev=lambda n, it: [finding("blocker", extra={"note": "x"})] if n == 1 else [])
    scenario("a decision state over budget abstains without crashing", "verified_pending_owner", both,
             ctl_mut=lambda c: c["decision"].update(budget_tokens=1),
             check=lambda r, o, w: len(events(o, "decision_skipped")) >= 2)
    scenario("omo version mismatch is refused", "policy_denied", both,
             deps_mut=lambda d, x: d["fakes"].__setitem__("worker@version", "5.1.48"))

    def tools(x, section, key, value):
        x.setdefault("tools_data", {"reviewers": {}, "workers": {}, "qualifications": {}})[section][key] = value

    def command_reviewer(c, x, tamper=False, pin_script=True, findings="[]"):
        script = os.path.join(x["tmp"], "review.py")
        open(script, "w").write(f"import sys\nprint('reviewed', sys.argv[1])\nprint({findings!r})\n")
        exe = os.path.realpath(sys.executable)
        pins = {exe: workers.sha256_file(exe)}
        if pin_script:
            pins[script] = "0" * 64 if tamper else workers.sha256_file(script)
        x["review_script"] = script
        tools(x, "reviewers", "r1", {"harness": c["reviewers"][0]["harness"], "argv": [exe, script, "{diff_file}"], "pins": pins})
        c["reviewers"] = [{"harness": c["reviewers"][0]["harness"], "kind": "command", "ref": "r1"}]
    scenario("pinned command reviewer from the owner's tools registry", "verified_pending_owner", both,
             ctl_mut=lambda c, x: command_reviewer(c, x))
    scenario("command reviewer whose pin does not match is refused", "policy_denied", both,
             ctl_mut=lambda c, x: command_reviewer(c, x, tamper=True))
    scenario("a reviewer with only its interpreter pinned is refused", "policy_denied", both,
             ctl_mut=lambda c, x: command_reviewer(c, x, pin_script=False))

    def swap_reviewer(d, x):
        inner = d["fakes"]["worker"]

        def fn(wt, prompt, it, extra):
            open(x["review_script"], "w").write("print('[]')\n")
            return inner(wt, prompt, it, extra)
        d["fakes"]["worker"] = fn
    scenario("a reviewer replaced after admission is refused at the call", "policy_denied", both,
             ctl_mut=lambda c, x: command_reviewer(c, x, findings=json.dumps([finding("blocker")])), deps_mut=swap_reviewer)

    # -- hidden bytes and vacuous checks ---------------------------------------------------------
    def only_check(argv):
        return lambda g: g.update(acceptance=[{"name": "w", "description": "win", "argv": argv, "timeout_seconds": 30}])
    win_in = ["python3", "-c", "import sys,os; p=os.path.join(*sys.argv[1:]); "
              "sys.exit(0 if os.path.exists(p) and 'WIN' in open(p).read() else 1)"]
    scenario("a check that reads under .git cannot pass", "no_progress", {1: [(".git/superloop-win", "WIN\n")]},
             goal_mut=only_check(win_in + [".git", "superloop-win"]))
    scenario("a check that reads the status file through a split path cannot pass", "no_progress",
             {1: [(".superloop/status.json", "WIN\n"), ("a.txt", "a\n")]},
             goal_mut=only_check(win_in + [".superloop", "status.json"]))
    scenario("a git filter in the worktree is refused", "policy_denied", both,
             pre=lambda g, c, d, x: control.git(x["wt"], "config", "filter.benign.clean", "cat"))

    def filter_later(d, x):
        inner = d["fakes"]["worker"]

        def fn(wt, prompt, it, extra):
            control.git(wt, "config", "filter.benign.clean", "sed s/SECRET/ok/")
            return inner(wt, prompt, it, extra)
        d["fakes"]["worker"] = fn
    scenario("a git filter added by a batch is refused", "policy_denied", both, deps_mut=filter_later)
    scenario("checks that already pass on the baseline are refused", "policy_denied", both,
             goal_mut=only_check(["test", "1", "-eq", "1"]))

    def nested(committed):
        def fn(wt, prompt, it, extra):
            n = os.path.join(wt, "nested")
            os.makedirs(n, exist_ok=True)
            subprocess.run(["git", "-C", n, "init", "-q"], check=True, capture_output=True)
            if committed:
                open(os.path.join(n, "win.txt"), "w").write("WIN\n")
                for a in (["-c", "user.email=t@x", "-c", "user.name=t", "add", "-A"],
                          ["-c", "user.email=t@x", "-c", "user.name=t", "commit", "-q", "-m", "x"]):
                    subprocess.run(["git", "-C", n] + a, check=True, capture_output=True)
            for f in ("a.txt", "b.txt"):
                open(os.path.join(wt, f), "w").write("x\n")
            return {"exit_code": 0, "reported": {"agents": ["sisyphus"], "models": [worker_model()]}}
        return fn
    scenario("a committed nested repository is refused", "policy_denied", {},
             deps_mut=lambda d, x: d["fakes"].__setitem__("worker", nested(True)))
    scenario("an empty nested repository is refused, not a crash", "policy_denied", {},
             deps_mut=lambda d, x: d["fakes"].__setitem__("worker", nested(False)))

    def escaping_link(d, x):
        inner = d["fakes"]["worker"]

        def fn(wt, prompt, it, extra):
            os.symlink("/etc/hostname", os.path.join(wt, "a.txt"))
            open(os.path.join(wt, "b.txt"), "w").write("b\n")
            return inner(wt, prompt, it, extra)
        d["fakes"]["worker"] = fn
    scenario("a symlink out of the tree is refused", "policy_denied", {}, deps_mut=escaping_link)

    def stub_omo(c, x, model=None, swap_export=False):
        """Real omo adapter, no fakes: stub binaries stand in for oh-my-openagent and opencode export."""
        command_reviewer(c, x)
        prov, mid = (model or worker_model()).split("/", 1)
        omo = os.path.join(x["tmp"], "omo-stub")
        exp = os.path.join(x["tmp"], "export-stub")
        swap = f"open({exp!r},'w').write('#!{sys.executable}\\nprint(1)\\n')\n" if swap_export else ""
        open(omo, "w").write("#!" + sys.executable + "\n"
                             "import json,os,sys\n"
                             "a=sys.argv[1:]\n"
                             "if a==['--version']: print('oh-my-openagent 4.19.4'); sys.exit(0)\n"
                             "wt=a[a.index('--directory')+1]\n"
                             "for f in ('a.txt','b.txt'): open(os.path.join(wt,f),'w').write('x\\n')\n" + swap +
                             "print(json.dumps({'sessionId':'ses_stub','success':True,'durationMs':1,'messageCount':2,'summary':'done'}))\n")
        open(exp, "w").write("#!" + sys.executable + "\n"
                             "import json\n"
                             f"print(json.dumps({{'info':{{'id':'ses_stub','agent':'sisyphus','providerID':{prov!r},'modelID':{mid!r}}}}}))\n")
        for f in (omo, exp):
            os.chmod(f, 0o755)
        tools(x, "workers", "stub", {"version": "4.19.4", "argv": [omo], "export_argv": [exp, "{session_id}"],
                                     "pins": {omo: workers.sha256_file(omo), exp: workers.sha256_file(exp)}})
        c["worker"] = {"kind": "omo", "ref": "stub", "agent": "sisyphus", "expect_agents": ["sisyphus"],
                       "isolation": "container", "env": {}}

    def no_fakes(d, x):
        d["allow_fakes"] = False
        d["fakes"] = {}
    scenario("omo adapter end to end with stub binaries, no fakes", "verified_pending_owner", {},
             ctl_mut=lambda c, x: stub_omo(c, x), deps_mut=no_fakes,
             check=lambda r, o, w: os.path.exists(os.path.join(w, ".omo", "omo.jsonc")))
    scenario("omo adapter: an export naming a model outside the cell is refused", "policy_denied", {},
             ctl_mut=lambda c, x: stub_omo(c, x, model=next(v["id"] for v in control.assign.load_matrix()["models"]["hybrid"].values()
                                                            if control.assign.family_of(v["id"]) == "openai")),
             deps_mut=no_fakes)
    scenario("omo adapter: an export program replaced during the batch is refused", "policy_denied", {},
             ctl_mut=lambda c, x: stub_omo(c, x, swap_export=True), deps_mut=no_fakes)

    # -- decision-model scenarios ----------------------------------------------------------------
    shadow_rec = recording({"1": {"blocked": {"type": "noul", "noul": 0.99},
                                  "progress": {"type": "choice", "choice": "stalled", "probabilities": {"stalled": 0.97, "regressing": 0.01, "drifting": 0.01, "progressing": 0.01}}}})
    scenario("shadow: a confident brake changes nothing", "verified_pending_owner", done2,
             ctl_mut=lambda c: c["decision"].update(backend=shadow_rec), check=lambda r, o, w: r["disagreements"] >= 2)

    def advisory(c, x, qid="blocked", scores=0.99, grid=(0.99, 0.95), pin=True):
        c["decision"]["backend"] = shadow_rec
        c["mode"] = "advisory"
        c["decision"]["lineage"] = {"provider": "test", "model": "rec-1.0", "base_family": "meta"}
        rec = make_record(x["tmp"], qid, scores, list(grid))
        c["qualifications"] = [{"question_id": qid, "model": "rec-1.0", "locale": "en", "record": rec}]
        if pin:
            tools(x, "qualifications", rec, workers.sha256_file(rec))
    scenario("advisory: a qualified brake pauses for a person", "blocked_human", done2, ctl_mut=lambda c, x: advisory(c, x))
    scenario("advisory: an unqualified question cannot act", "verified_pending_owner", done2,
             ctl_mut=lambda c, x: advisory(c, x, qid="needs_human"))
    scenario("advisory: a brake below its qualified threshold cannot act", "verified_pending_owner", done2,
             ctl_mut=lambda c, x: advisory(c, x, scores=0.999, grid=(0.999, 0.995)))

    def edited_record(c, x):
        advisory(c, x)
        p = c["qualifications"][0]["record"]
        r = json.load(open(p))
        r["threshold"] = 0.01
        json.dump(r, open(p, "w"))
    scenario("advisory: a hand-edited threshold is refused", "policy_denied", done2, ctl_mut=edited_record)
    scenario("advisory: a record the owner did not pin is refused", "policy_denied", done2,
             ctl_mut=lambda c, x: advisory(c, x, pin=False))
    done_rec = recording({}, default={"goal_met": {"type": "noul", "noul": 0.99}})
    scenario("decision says done while checks fail: no effect", "no_progress", {},
             ctl_mut=lambda c: c["decision"].update(backend=done_rec))
    smoke_rec = recording({}, default={"goal_met": {"type": "noul", "noul": 0.05}})

    def smoke(c, x):
        advisory(c, x, qid="goal_met")
        c["decision"]["backend"] = smoke_rec
        c["reviewers"].append({"harness": seat_harnesses()[1]["harness"], "kind": "fake", "name": "reviewer2"})
    scenario("advisory smoke detector adds every reviewer seat", "verified_pending_owner", done2, ctl_mut=smoke,
             deps_mut=lambda d, x: d.__setitem__("matrix", two_seat_matrix()),
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

    # -- unit checks on the parts ----------------------------------------------------------------
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
        keys = ["sk-abcdefghijklmnop1234", "sk_live_abcdefghijkl", "xoxb-1234567890-abcdefgh",
                "github_pat_11AAAAAAabcdefghijklmnopqrstuvwxyz", "AIzaSyA1234567890abcdef",
                "eyJhbGciOiJIUzI1.eyJzdWIiOiIxMjM0.abcdefghijk", "api_key=hunter2hunter2"]
        st2, _ = statemod.build(g, {"note": " ".join(keys)}, root=tmp)
        ok("key shapes are redacted", not any(k in json.dumps(st2) for k in keys))
        try:
            statemod.build(g, {"failing_checks": ["x" * 50] * 10}, root=tmp, budget_tokens=50)
            ok("over-budget required facts fail closed", False)
        except ValueError:
            ok("over-budget required facts fail closed", True)
        prov, mid = worker_model().split("/", 1)
        exp = json.dumps({"info": {"agent": "sisyphus", "providerID": prov, "modelID": mid},
                          "messages": [{"info": {"agent": "hephaestus"}}]})
        ps = workers.parse_session(exp)
        ok("session parsing returns every agent, not the first", ps["agents"] == ["hephaestus", "sisyphus"]
           and ps["models"] == [worker_model()])
        rr = os.path.join(tmp, "run.json")
        open(rr, "w").write('{"sessionId": "ses_1", "success": true, "durationMs": 5, "messageCount": 2, "summary": "done"}\n')
        ok("a mode field is not read as an agent", workers.parse_session(json.dumps({"agent": "sisyphus", "mode": "build"}))["agents"] == ["sisyphus"])
        ok("findings come from the last output line", workers.parse_findings("text\n[]\n") == [] and
           workers.parse_findings("[]\nmore text") is None)
        ok("run result yields the session id and keeps success as a claim",
           workers.parse_run_result(rr) == {"session_id": "ses_1", "run_success_claim": True})
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
    ok("a dual backend reserves two calls", decide.remote_calls({"kind": "dual", "first": {"kind": "http"}, "second": {"kind": "http"}}) == 2)
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
