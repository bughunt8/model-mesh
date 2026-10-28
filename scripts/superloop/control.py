"""The superloop control plane.

Code owns the loop. A typed decision model answers questions at fixed forks; in shadow mode its
answers are only logged, and in advisory mode a qualified answer may only brake: pause for a
person, stop for no progress, or add a review. It can never end the loop as a success, skip a
check, change the profile or approve an action. omo workers do the work in bounded batches.
Cross-family reviewers and acceptance checks decide whether the work is done.

One run:
  admission   validate goal and controller, load the frozen matrix assignment, record the
              orchestrator and author lineage, check the decision seat, hash protected paths,
              materialize the omo config with omo's own continuation disabled.
  iteration   interlocks (stop file, caps, budget) -> one worker batch -> acceptance checks ->
              facts -> decision questions -> brake effects -> review when the checks are green
              or on cadence -> stop rules -> log.
  terminal    verified_pending_owner, verified, cap_iterations, cap_wall_clock, cap_budget,
              no_progress, fix_cycles_exhausted, blocked_human, escalation_requested,
              review_unavailable, worker_failure, policy_denied, cancelled.

Only verified and verified_pending_owner are success, and both need every acceptance check to
pass on the final tree and a cross-family review of that same tree with no blocker and no
corroborated major finding.
"""
import hashlib, importlib.util, json, os, subprocess, sys, time

from . import assign, decide, ledger, state as statemod, workers

ROOT = assign.ROOT
SUCCESS = {"verified", "verified_pending_owner"}
BRAKE_EFFECTS = {"pause_human", "stop_no_progress", "add_review"}


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


agg = _load("_agg", "scripts/aggregate-findings.py")
vsl = _load("_vsl", "scripts/validate-superloop.py")


def git(worktree, *args, env=None, check=True):
    e = dict(os.environ)
    e.update(env or {})
    r = subprocess.run(["git", "-C", worktree] + list(args), capture_output=True, text=True, env=e)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout.strip()


def tree_hash(worktree, scratch):
    """Hash of the full working tree, untracked files included, via a private index."""
    env = {"GIT_INDEX_FILE": os.path.join(scratch, "superloop.index")}
    git(worktree, "add", "-A", "--", ".", ":(exclude).superloop", ":(exclude).omo", env=env)
    return git(worktree, "write-tree", env=env)


def write_diff(worktree, scratch, base, path):
    env = {"GIT_INDEX_FILE": os.path.join(scratch, "superloop.index")}
    git(worktree, "add", "-A", "--", ".", ":(exclude).superloop", ":(exclude).omo", env=env)
    open(path, "w", encoding="utf-8").write(git(worktree, "diff", "--cached", base, env=env, check=False))


def protected_hashes(worktree, paths):
    out = {}
    for p in paths:
        full = os.path.join(worktree, p)
        files = []
        if os.path.isdir(full):
            for d, _, fs in os.walk(full):
                files += [os.path.join(d, f) for f in fs]
        elif os.path.isfile(full):
            files = [full]
        for f in sorted(files):
            out[os.path.relpath(f, worktree)] = hashlib.sha256(open(f, "rb").read()).hexdigest()
        if not files:
            out[p] = "absent"
    return out


def materialize(controller, goal, worktree):
    """Write <worktree>/.omo/omo.jsonc from the profile fragment, with omo's continuation off."""
    m = controller.get("materialize", {})
    frag = os.path.join(ROOT, m.get("fragment", f"profiles/{goal['profile']}.example.json"))
    # example profiles carry // comment lines that materialize.py does not strip
    clean = os.path.join(worktree, ".superloop", "fragment.json")
    os.makedirs(os.path.dirname(clean), exist_ok=True)
    open(clean, "w", encoding="utf-8").write("\n".join(
        l for l in open(frag, encoding="utf-8").read().splitlines() if not l.lstrip().startswith("//")))
    out = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "materialize.py"), clean, goal["profile"]],
                         capture_output=True, text=True, check=True).stdout
    cfg = json.loads("\n".join(l for l in out.splitlines() if not l.lstrip().startswith("//")))
    block = cfg["[opencode]"]
    block["disabled_hooks"] = sorted(set(block.get("disabled_hooks", [])) | set(m.get("disabled_hooks", [])))
    block["goal"] = {"enabled": False}
    os.makedirs(os.path.join(worktree, ".omo"), exist_ok=True)
    text = json.dumps(cfg, indent=2) + "\n"
    open(os.path.join(worktree, ".omo", "omo.jsonc"), "w").write(text)
    return hashlib.sha256(text.encode()).hexdigest()[:16], block["disabled_hooks"]


def run_checks(goal, worktree, out_dir, iteration, remaining):
    res = []
    for c in goal["acceptance"]:
        r = workers.run_bounded(c["argv"], worktree, dict(os.environ), min(c.get("timeout_seconds", 300), remaining),
                                out_dir, f"check-{iteration:03d}-{c['name']}")
        res.append({"name": c["name"], "passed": r["exit_code"] == 0 and not r["timed_out"],
                    "exit_code": r["exit_code"], "timed_out": r["timed_out"]})
    return res


def compose_prompt(goal, iteration, checks, open_findings):
    lines = [f"Goal {goal['id']}: {goal['objective']}", "", "Acceptance criteria:"]
    lines += [f"- {c['name']}: {c['description']}" for c in goal["acceptance"]]
    if checks:
        failing = [c["name"] for c in checks if not c["passed"]]
        lines += ["", "Failing checks from the last batch: " + (", ".join(failing) if failing else "none")]
    if open_findings:
        lines += ["", "Open review findings to address:"]
        lines += [f"- {c['severity']} {c['path']}:{c['line_start'] or ''} {c['claims'][0]}" for c in open_findings[:20]]
    lines += ["", f"This is batch {iteration}. Work on the next unmet criterion, then stop.",
              "Do not declare the goal complete: the controller runs the checks and an independent review.",
              "Do not edit protected paths: " + (", ".join(goal.get("protected_paths", [])) or "none") + ".",
              "If you are blocked by something only a person can fix, write .superloop/status.json with "
              "{\"status\": \"blocked\", \"reason\": \"<short code>\"} and stop."]
    return "\n".join(lines)


def read_claims(worktree):
    p = os.path.join(worktree, ".superloop", "status.json")
    try:
        d = json.load(open(p, encoding="utf-8"))
        return {"status": d.get("status") if d.get("status") in ("blocked", "working", "done") else "unknown"}
    except (OSError, ValueError, AttributeError):
        return {"status": "none"}


def qualified_threshold(controller, model, qid, revision, locale):
    for q in controller.get("qualifications", []):
        if (q.get("model"), q.get("question_id"), q.get("revision"), q.get("locale")) == (model, qid, revision, locale) \
                and q.get("threshold") is not None:
            return q["threshold"]
    return None


def gate_score(ans):
    if ans["type"] == "noul":
        return ans["p"]
    if ans["type"] == "choice":
        return ans["top"]
    return None


class Run:
    def __init__(self, goal, controller, worktree, out_dir, deps=None):
        deps = deps or {}
        self.goal, self.ctl, self.wt, self.out = goal, controller, os.path.abspath(worktree), os.path.abspath(out_dir)
        self.clock = deps.get("clock", time.time)
        self.fakes = deps.get("fakes", {})
        self.matrix = deps.get("matrix") or assign.load_matrix()
        os.makedirs(self.out, exist_ok=True)
        self.scratch = os.path.join(self.out, "scratch")
        os.makedirs(self.scratch, exist_ok=True)
        self.log = ledger.EventLog(os.path.join(self.out, "events.jsonl"), self.clock)
        self.prov = ledger.Provenance()
        self.spent = 0.0
        self.disagreements = 0
        self.decisions = 0

    def reserve(self, kind):
        cost = float(self.ctl.get("reservations_usd", {}).get(kind, 0.0))
        cap = self.ctl["caps"].get("budget_usd")
        if cap is not None and self.spent + cost > cap + 1e-9:
            return False
        self.spent += cost
        return True

    def finish(self, status, detail, **extra):
        out = {"status": status, "success": status in SUCCESS, "detail": detail, "goal": self.goal["id"],
               "profile": self.goal["profile"], "situation": self.goal["situation"], "option": self.goal["option"],
               "mode": self.ctl["mode"], "reserved_usd": round(self.spent, 4), "decisions": self.decisions,
               "disagreements": self.disagreements, "provenance": self.prov.snapshot()}
        out.update(extra)
        self.log.write("terminal", **out)
        json.dump(out, open(os.path.join(self.out, "final.json"), "w"), indent=2)
        return out

    # -- admission ---------------------------------------------------------------
    def admit(self):
        errs = vsl.validate_goal(self.goal) + vsl.validate_controller(self.ctl, self.goal)
        if errs:
            return errs
        try:
            self.a = assign.assignment(self.matrix, self.goal["situation"], self.goal["profile"], self.goal["option"])
        except KeyError as ex:
            return [f"assignment: {ex}"]
        if self.ctl["worker"]["kind"] == "omo" and {s["harness"] for s in self.a["authors"]} != {"opencode-omo"}:
            return [f"{self.goal['situation']}/{self.goal['profile']}/{self.goal['option']} authors do not run on opencode-omo"]
        if self.a["orchestrator"]:
            self.prov.record(0, "orchestrator", self.a["orchestrator"]["harness"], self.a["orchestrator"]["families"])
        for s in self.a["authors"]:
            self.prov.record(0, "author:" + str(s["role"]), s["harness"], s["families"])
        for s in self.goal.get("prior_lineage", []):
            self.prov.record(-1, "prior:" + str(s.get("note", "")), s["harness"], s["families"])
        d = self.ctl["decision"]
        lin = d.get("lineage", {})
        if self.ctl["mode"] != "shadow":
            fam = lin.get("base_family")
            if not fam or fam in ("undisclosed", "unknown"):
                return ["advisory mode needs a decision model with a disclosed base family"]
            rev_f = set().union(*[set(r["families"]) for r in self.a["reviewers"]]) if self.a["reviewers"] else set()
            if fam in self.prov.families | rev_f | set(self.a["aggregator"]["families"]):
                return [f"decision family {fam} overlaps an author, orchestrator, reviewer or aggregator family"]
        if self.goal["profile"] == "ultimate" and d["backend"]["kind"] in ("http", "dual") \
                and not d.get("egress", {}).get("hk_reachable_verified"):
            return ["ultimate profile: the decision endpoint is not verified as Hong Kong reachable and policy eligible"]
        return []

    def setup(self):
        self.base = git(self.wt, "rev-parse", "HEAD")
        self.protected0 = protected_hashes(self.wt, self.goal.get("protected_paths", []))
        if self.ctl["worker"]["kind"] == "omo" or self.ctl.get("materialize", {}).get("always"):
            self.cfg_hash, hooks = materialize(self.ctl, self.goal, self.wt)
        else:
            self.cfg_hash, hooks = None, []
        cat = json.load(open(os.path.join(ROOT, self.ctl["decision"]["questions"]), encoding="utf-8"))
        self.catalog = {q["id"]: q for q in cat["questions"]}
        self.locale = self.ctl["decision"].get("locale", "en")
        self.rules = decide.RulesBackend(self.catalog)
        self.backend = decide.build_backend(self.ctl["decision"]["backend"], self.catalog)
        self.worker = workers.build(self.ctl["worker"], self.fakes)
        self.reviewers = []
        for r in self.ctl.get("reviewers", []):
            seatm = next((s for s in self.a["reviewers"] if s["harness"] == r["harness"]), None)
            if seatm:
                self.reviewers.append((seatm, workers.build(r, self.fakes)))
        self.log.write("admitted", assignment={k: self.a[k] for k in ("situation", "profile", "option", "pattern")},
                       base=self.base, config_hash=self.cfg_hash, disabled_hooks=hooks,
                       provenance=self.prov.snapshot(), reviewers=[s["harness"] for s, _ in self.reviewers])

    # -- decisions ---------------------------------------------------------------
    def ask(self, ids, st, iteration, menus=None):
        ctx = {"iteration": iteration}
        ra, rrec = decide.ask(self.rules, self.catalog, ids, menus or {}, st, ctx)
        if self.backend.name == "rules":
            ma, mrec = ra, rrec
        else:
            if not self.reserve("decision_call"):
                ma = {q: {"type": "abstain", "reason": "budget"} for q in ids}
                mrec = {"backend": self.backend.name, "error": "budget", "answers": ma}
            else:
                ma, mrec = decide.ask(self.backend, self.catalog, ids, menus or {}, st, ctx)
        for q in ids:
            self.decisions += 1
            a, b = ra[q], ma[q]
            dis = a["type"] != b["type"] or (a["type"] == "choice" and a["choice"] != b["choice"]) or \
                (a["type"] == "noul" and (a["p"] >= 0.5) != (b["p"] >= 0.5))
            self.disagreements += 1 if (dis and b["type"] != "abstain") else 0
        self.log.write("decision", iteration=iteration, questions=ids, rules=rrec["answers"], model=mrec,
                       mode=self.ctl["mode"])
        return ma, mrec

    def brakes(self, answers, rec):
        """Advisory mode only: return the brake effects that qualified answers trigger."""
        if self.ctl["mode"] != "advisory":
            return []
        out = []
        for qid, ans in answers.items():
            q = self.catalog[qid]
            if q.get("authority") != "brake" or ans["type"] == "abstain":
                continue
            t = qualified_threshold(self.ctl, rec.get("model"), qid, q["revision"], self.locale)
            if t is None:
                continue
            eff = q["effect"]
            hit = (ans["type"] == "noul" and ans["p"] >= t) or \
                  (ans["type"] == "choice" and ans["choice"] in eff.get("on_options", []) and ans["top"] >= t)
            if hit:
                out.append((qid, eff["effect"]))
        return out

    # -- review ------------------------------------------------------------------
    def review(self, iteration, tree, all_seats=False):
        usable = []
        for seatm, adapter in self.reviewers:
            c = self.prov.conflicts(seatm["harness"], seatm["families"])
            if c:
                self.log.write("review_refused", iteration=iteration, harness=seatm["harness"], reasons=c)
                continue
            usable.append((seatm, adapter))
        if not usable:
            return None
        if not all_seats:
            usable = usable[:1]
        findings = []
        diff = os.path.join(self.out, f"diff-{iteration:03d}.patch")
        write_diff(self.wt, self.scratch, self.base, diff)
        ran = []
        for seatm, adapter in usable:
            if not self.reserve("review_call"):
                return {"error": "budget"}
            fo = os.path.join(self.out, f"findings-{iteration:03d}-{seatm['harness']}.json")
            prompt = ("Review the change in the diff file against the lenses " + ", ".join(seatm["lenses"]) +
                      ". You have no other context. Write findings as a JSON list in the finding schema to the "
                      "findings file. Write [] if there are none.")
            res = adapter.run(self.wt, prompt, iteration, self.ctl["caps"]["per_call_seconds"], self.out,
                              {"findings_out": fo, "diff_file": diff, "lenses": ",".join(seatm["lenses"])})
            ran.append(seatm["harness"])
            try:
                items = json.load(open(fo, encoding="utf-8"))
            except (OSError, ValueError):
                return {"error": f"reviewer {seatm['harness']} wrote no valid findings file", "ran": ran}
            errs = agg.check(items)
            if errs:
                return {"error": f"reviewer {seatm['harness']} findings invalid: {errs[:3]}", "ran": ran}
            findings += [dict(x, id=f"{seatm['harness']}:{x['id']}") for x in items]
        clusters = agg.cluster(findings)
        blockers = [c for c in clusters if c["severity"] == "blocker"]
        corr_majors = [c for c in clusters if c["severity"] == "major" and c["corroborated"]]
        majors = [c for c in clusters if c["severity"] == "major"]
        return {"tree": tree, "ran": ran, "clusters": len(clusters), "blockers": len(blockers),
                "corroborated_majors": len(corr_majors), "open": blockers + majors}

    # -- main loop ---------------------------------------------------------------
    def run(self):
        t0 = self.clock()
        errs = self.admit()
        if errs:
            return self.finish("policy_denied", errs)
        self.setup()
        caps = self.ctl["caps"]
        prev_passing, prev_fp, streak = set(), None, 0
        cycles, checks, open_findings, last_review = {}, [], [], None
        reviews_invalid = 0
        tree = tree_hash(self.wt, self.scratch)
        for it in range(1, 10 ** 6):
            if os.path.exists(os.path.join(self.out, "STOP")):
                return self.finish("cancelled", "stop file present", iterations=it - 1)
            if it > caps["max_iterations"]:
                return self.finish("cap_iterations", f"{caps['max_iterations']} iterations", iterations=it - 1)
            remaining = caps["wall_clock_seconds"] - (self.clock() - t0)
            if remaining <= 0:
                return self.finish("cap_wall_clock", f"{caps['wall_clock_seconds']} s", iterations=it - 1)
            if not self.reserve("worker_call"):
                return self.finish("cap_budget", f"reservation would exceed {caps.get('budget_usd')} USD", iterations=it - 1)
            if it == 1:
                st0, _ = statemod.build(self.goal, {"iteration": 0}, root=self.wt,
                                        budget_tokens=self.ctl["decision"].get("budget_tokens", 30000))
                self.ask(["situation"], st0, 0)
            prompt = compose_prompt(self.goal, it, checks, open_findings)
            res = self.worker.run(self.wt, prompt, it, min(caps["per_call_seconds"], remaining), self.out)
            for s in self.a["authors"]:
                self.prov.record(it, "author:" + str(s["role"]), s["harness"], s["families"])
            rep = res.get("reported", {})
            expect = self.ctl["worker"].get("expect_agents")
            self.log.write("worker", iteration=it, exit_code=res["exit_code"], timed_out=res["timed_out"],
                           duration=res["duration"], reported=rep, error=res.get("error"))
            if res["exit_code"] is None and not res["timed_out"]:
                return self.finish("worker_failure", res.get("error"), iterations=it)
            if expect and rep.get("agent") and rep["agent"] not in expect:
                return self.finish("policy_denied", f"worker ran as {rep['agent']}, expected one of {expect}", iterations=it)
            claims = read_claims(self.wt)
            remaining = caps["wall_clock_seconds"] - (self.clock() - t0)
            checks = run_checks(self.goal, self.wt, self.out, it, max(1.0, remaining))
            passing = {c["name"] for c in checks if c["passed"]}
            failing = sorted(c["name"] for c in checks if not c["passed"])
            tree_prev, tree = tree, tree_hash(self.wt, self.scratch)
            prot = protected_hashes(self.wt, self.goal.get("protected_paths", []))
            touched = sorted(k for k in set(prot) | set(self.protected0) if prot.get(k) != self.protected0.get(k))
            fp = (tree, tuple(failing))
            streak = streak + 1 if fp == prev_fp else 0
            prev_fp = fp
            regressed = sorted(prev_passing - passing)
            prev_passing = passing
            if failing:
                key = "checks:" + ",".join(failing)
                cycles[key] = cycles.get(key, 0) + 1
            facts = {"iteration": it, "max_iterations": caps["max_iterations"], "checks_run": len(checks),
                     "checks_failed": len(failing), "failing_checks": failing, "tree_changed": tree != tree_prev,
                     "unchanged_streak": streak, "regressed": bool(regressed), "regressed_checks": regressed,
                     "touches_protected": bool(touched), "worker_exit": res["exit_code"],
                     "worker_timed_out": res["timed_out"], "worker_reported_blocked": claims["status"] == "blocked",
                     "remaining_fraction": round(max(0.0, remaining) / caps["wall_clock_seconds"], 3),
                     "review": {k: last_review.get(k) for k in ("blockers", "corroborated_majors", "clusters")}
                     if last_review and "error" not in last_review else None}
            self.log.write("facts", **facts)
            try:
                st, srep = statemod.build(self.goal, facts, claims, root=self.wt,
                                          budget_tokens=self.ctl["decision"].get("budget_tokens", 30000))
                answers, rec = self.ask(["progress", "blocked", "needs_human", "goal_met", "next_action"], st, it)
            except ValueError as ex:
                self.log.write("decision_skipped", iteration=it, reason=str(ex))
                answers, rec = {}, {}
            effects = self.brakes(answers, rec)
            if effects:
                self.log.write("brake", iteration=it, effects=effects)
            # interlocks that need no model
            if touched:
                return self.finish("blocked_human", f"protected paths changed: {touched}", iterations=it)
            if claims["status"] == "blocked":
                return self.finish("blocked_human", "worker reported blocked", iterations=it)
            if any(e == "pause_human" for _, e in effects):
                return self.finish("blocked_human", f"decision brake: {effects}", iterations=it)
            if streak >= caps["no_progress_streak"]:
                return self.finish("no_progress", f"same tree and failing checks for {streak + 1} batches", iterations=it)
            if any(e == "stop_no_progress" for _, e in effects):
                return self.finish("no_progress", f"decision brake: {effects}", iterations=it)
            worst = max(cycles.values()) if cycles else 0
            if worst >= caps["fix_verify_cycles"]:
                return self.finish("fix_cycles_exhausted", f"{worst} cycles on {max(cycles, key=cycles.get)}", iterations=it)
            green = bool(checks) and not failing
            cadence = self.ctl.get("review", {}).get("every_k_iterations")
            smoke = green and answers.get("goal_met", {}).get("type") == "noul" and \
                answers["goal_met"]["p"] < self.ctl.get("review", {}).get("smoke_below", 0.5)
            extra_review = any(e == "add_review" for _, e in effects) or (smoke and self.ctl["mode"] == "advisory")
            if smoke:
                self.log.write("smoke_detector", iteration=it, p=answers["goal_met"]["p"], acted=extra_review)
            if green or extra_review or (cadence and it % cadence == 0):
                rv = self.review(it, tree, all_seats=extra_review)
                if rv is None:
                    return self.finish("review_unavailable", "no reviewer is independent of this run's lineage", iterations=it)
                if rv.get("error") == "budget":
                    return self.finish("cap_budget", "review reservation would exceed the budget", iterations=it)
                self.log.write("review", iteration=it, **{k: v for k, v in rv.items() if k != "open"})
                if "error" in rv:
                    reviews_invalid += 1
                    cycles["review_invalid"] = reviews_invalid
                    if reviews_invalid >= 2:
                        return self.finish("review_unavailable", rv["error"], iterations=it)
                    continue
                last_review = rv
                open_findings = rv["open"]
                if green and rv["tree"] == tree and rv["blockers"] == 0 and rv["corroborated_majors"] == 0:
                    status = "verified_pending_owner" if self.goal.get("owner_approval_required", True) else "verified"
                    return self.finish(status, "checks pass and an independent review found no blocker",
                                       iterations=it, tree=tree, review=rv["ran"])
                for c in rv["open"]:
                    k = f"finding:{c['path']}:{c['category']}"
                    cycles[k] = cycles.get(k, 0) + 1
        return self.finish("cap_iterations", "loop bound", iterations=0)
