"""The superloop control plane.

Code owns the loop. A typed decision model answers questions at fixed forks; in shadow mode its
answers are only logged, and in advisory mode a qualified answer may only brake: pause for a
person, stop for no progress, or add a review. It can never end the loop as a success, skip a
check, change the profile or approve an action. omo workers do the work in bounded batches.
Acceptance checks and a reviewer from a family that never authored in the run decide whether
the work is done.

One run:
  admission   refuse a reused output directory; validate goal and controller; load the frozen
              matrix cell; record the orchestrator and author lineage, prior_lineage and every
              earlier run on the same branch or goal from the lineage registry; check the
              decision seat; verify qualification records; resolve reviewers from the owner's
              registry and check their pins.
  setup       materialize the omo config restricted to the cell's author and orchestrator
              families, with omo's own continuation, runtime fallback and team mode off;
              check the omo version; hash the protected paths and the baseline tree.
  iteration   interlocks (stop file, caps, budget) -> rewrite the omo config -> one worker
              batch -> config tamper check -> session agent and model check -> acceptance
              checks -> facts -> decision questions -> brake effects -> stop rules -> review
              when the checks are green, on a brake or on cadence -> recheck before success.
  terminal    verified_pending_owner, verified, cap_iterations, cap_wall_clock, cap_budget,
              no_progress, fix_cycles_exhausted, blocked_human, review_unavailable,
              worker_failure, policy_denied, cancelled.

Only verified and verified_pending_owner are success. Both need: every acceptance check passing
on a fresh copy of the hashed tree, a review of the diff to that same tree by a reviewer
independent of the whole lineage with no blocker and no major finding, an unchanged tree after
the review, a second run of the checks on a new copy, and wall-clock time left.

Trust boundary: these rules hold against a worker that cannot write outside its worktree, with
checks jailed by bubblewrap. A worker running as the driver's own OS user can edit the driver,
the registries and the run folder, and no check in this file can stop that; an unjailed check can
read the live worktree by path. The controller states the isolation and the jail, and final.json
repeats both with a protected flag. The driver never runs git in the worker's repository.
"""
import hashlib, importlib.util, json, os, re, shutil, subprocess, sys, time
from urllib.parse import urlparse

from . import assign, decide, ledger, qualify, state as statemod, workers

ROOT = assign.ROOT
SUCCESS = {"verified", "verified_pending_owner"}
BRAKE_EFFECTS = {"pause_human", "stop_no_progress", "add_review"}
STATUS_FILE = os.path.join(".superloop", "status.json")
OMO_CONFIG = os.path.join(".omo", "omo.jsonc")
HASH_EXCLUDE = [":(exclude).superloop/status.json", ":(exclude).omo/omo.jsonc"]
REQUIRED_HOOKS = ("goal", "todo-continuation-enforcer", "start-work", "atlas", "runtime-fallback")
REQUIRED_COMMANDS = ("goal", "start-work")
LOOPBACK = {"127.0.0.1", "localhost", "::1"}


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


agg = _load("_agg", "scripts/aggregate-findings.py")
vsl = _load("_vsl", "scripts/validate-superloop.py")


class PolicyError(Exception):
    pass


EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
GIT_SAFE = ["-c", "core.fsmonitor=false", "-c", "core.untrackedCache=false", "-c", "core.splitIndex=false",
            "-c", "core.autocrlf=false", "-c", "core.safecrlf=false", "-c", "core.symlinks=true"]


def clean_env(home, extra=None):
    """A process environment built from nothing: PATH, a private HOME and a plain locale. Nothing
    from the driver's environment leaks in, including MM_* and GIT_* variables."""
    e = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": home, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
         "TMPDIR": os.environ.get("TMPDIR", "/tmp")}
    e.update(extra or {})
    return e


def git_dir_of(worktree):
    """Resolve the worktree's git directory and common directory without running git in it.
    The worktree must be the root of a checkout: .git is a directory, a symlink or a gitfile."""
    dot = os.path.join(worktree, ".git")
    if os.path.isdir(dot):
        gd = os.path.realpath(dot)
    elif os.path.isfile(dot):
        line = open(dot, encoding="utf-8", errors="replace").readline().strip()
        if not line.startswith("gitdir:"):
            raise PolicyError("the worktree's .git file is not a gitdir pointer")
        gd = os.path.realpath(os.path.join(worktree, line[len("gitdir:"):].strip()))
    else:
        raise PolicyError("the worktree must be the root of a git checkout")
    cf = os.path.join(gd, "commondir")
    common = os.path.realpath(os.path.join(gd, open(cf, encoding="utf-8").read().strip())) if os.path.isfile(cf) else gd
    return gd, common


class Store:
    """The driver's own git object store, in the run folder, outside the worktree.

    Every hash, snapshot and diff goes through this store with the worktree as a plain work tree.
    Git never reads the worker's repository here: no repository config, hooks, filters, replace
    refs, alternates or info/attributes. System and global config are off, replace objects are
    off, hooks point at an empty folder, and attributes come from the empty tree, so the
    worktree's own .gitattributes cannot convert bytes either. Git skips every path named .git.
    What the store holds is exactly the bytes in the worktree's files."""

    def __init__(self, scratch, worktree):
        self.dir = os.path.join(scratch, "store.git")
        self.hooks = os.path.join(scratch, "no-hooks")
        self.home = os.path.join(scratch, "git-home")
        self.wt = worktree
        for d in (self.hooks, self.home):
            os.makedirs(d, exist_ok=True)
        self.env = clean_env(self.home, {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
                                         "GIT_ATTR_NOSYSTEM": "1", "GIT_NO_REPLACE_OBJECTS": "1",
                                         "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0"})
        r = subprocess.run(["git", "init", "-q", "--bare", "--template=", self.dir], capture_output=True, env=self.env)
        if r.returncode != 0:
            raise RuntimeError(f"git init of the driver store failed: {r.stderr.decode(errors='replace').strip()}")

    def cmd(self, *args):
        return ["git", "--git-dir=" + self.dir, "--work-tree=" + self.wt, "--no-replace-objects",
                "--attr-source=" + EMPTY_TREE, "-c", "core.hooksPath=" + self.hooks] + GIT_SAFE + list(args)

    def run(self, *args, env=None, stdin=None):
        e = dict(self.env)
        e.update(env or {})
        r = subprocess.run(self.cmd(*args), capture_output=True, env=e, input=stdin)
        if r.returncode != 0:
            raise RuntimeError(f"git {args[0]} failed: {r.stderr.decode(errors='replace').strip()}")
        return r.stdout

    def tree_hash(self, scratch):
        """Hash of the whole working tree through a fresh private index: tracked, untracked and
        ignored files alike. Left out: every .git, the worker's status file and the
        controller-written omo config (that one is checked on its own)."""
        idx = os.path.join(scratch, "superloop.index")
        if os.path.exists(idx):
            os.remove(idx)
        env = {"GIT_INDEX_FILE": idx}
        self.run("add", "-A", "-f", "--", ".", *HASH_EXCLUDE, env=env)
        return self.run("write-tree", env=env).decode().strip()

    def extract(self, tree, dest):
        """Write the exact blobs of a tree object into dest. No filters, no checkout. A nested
        repository (gitlink) or a symlink that leaves the tree is refused."""
        os.makedirs(dest)
        entries = []
        for e in self.run("ls-tree", "-r", "-z", "--full-tree", tree).split(b"\0"):
            if not e:
                continue
            meta, path = e.split(b"\t", 1)
            mode, typ, sha = meta.split(b" ")
            if typ != b"blob":
                raise PolicyError(f"{path.decode(errors='replace')} is a nested repository; its content cannot be reviewed")
            entries.append((mode.decode(), sha.decode(), path.decode("utf-8", errors="surrogateescape")))
        if not entries:
            return
        data = self.run("cat-file", "--batch", stdin=("\n".join(sha for _, sha, _ in entries) + "\n").encode())
        pos = 0
        root = os.path.realpath(dest)
        for mode, sha, path in entries:
            nl = data.index(b"\n", pos)
            size = int(data[pos:nl].split(b" ")[2])
            body = data[nl + 1:nl + 1 + size]
            pos = nl + 1 + size + 1
            full = os.path.join(dest, path)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            if mode == "120000":
                target = body.decode("utf-8", errors="surrogateescape")
                if os.path.isabs(target) or not os.path.realpath(os.path.join(os.path.dirname(full), target)).startswith(root + os.sep):
                    raise PolicyError(f"symlink {path} points outside the tree")
                os.symlink(target, full)
                continue
            with open(full, "wb") as f:
                f.write(body)
            if mode == "100755":
                os.chmod(full, 0o755)

    def write_diff(self, base_tree, tree, path):
        """The change since admission, tree object to tree object, as raw bytes."""
        with open(path, "wb") as f:
            f.write(self.run("diff", "--binary", "--no-ext-diff", "--no-textconv", "--no-color", base_tree, tree))


def jail_argv(argv, snap, hide):
    """bubblewrap around one acceptance check: the whole filesystem read-only, the live
    worktree, its git directory and the run folder replaced by empty folders, the snapshot
    bound back read-write, a fresh /tmp, its own process, network and IPC namespaces, and an
    environment built from nothing."""
    j = ["bwrap", "--die-with-parent", "--new-session", "--unshare-all", "--clearenv",
         "--setenv", "PATH", os.environ.get("PATH", "/usr/bin:/bin"), "--setenv", "HOME", "/tmp",
         "--setenv", "TMPDIR", "/tmp", "--setenv", "LANG", "C.UTF-8",
         "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp"]
    for h in hide:
        j += ["--tmpfs", h]
    return j + ["--bind", snap, snap, "--chdir", snap, "--"] + list(argv)


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


def config_models(x, out=None):
    out = [] if out is None else out
    if isinstance(x, dict):
        for k, v in x.items():
            if k == "model" and isinstance(v, str):
                out.append(v)
            else:
                config_models(v, out)
    elif isinstance(x, list):
        for v in x:
            config_models(v, out)
    return out


def restrict(block, allowed, run_agent):
    """Keep only models whose family is in the run's author and orchestrator families. An agent
    with none left is disabled. A category with none left gets the run agent's model."""
    rep = {"dropped": [], "disabled_agents": [], "filled_categories": []}

    def ok(m):
        return assign.family_of(m) in allowed
    agents = block.get("agents", {})
    for name in list(agents):
        a = agents[name]
        cands = []
        if isinstance(a.get("model"), str):
            cands.append({k: a[k] for k in ("model", "reasoning") if k in a})
        cands += [f for f in a.get("fallback_models", []) if isinstance(f, dict) and isinstance(f.get("model"), str)]
        keep = [c for c in cands if ok(c["model"])]
        rep["dropped"] += [f"{name}:{c['model']}" for c in cands if not ok(c["model"])]
        uw = a.get("ultrawork")
        if isinstance(uw, dict) and isinstance(uw.get("model"), str) and not ok(uw["model"]):
            rep["dropped"].append(f"{name}:ultrawork:{uw['model']}")
            a.pop("ultrawork")
        if not keep:
            agents.pop(name)
            rep["disabled_agents"].append(name)
            continue
        a["model"] = keep[0]["model"]
        if "reasoning" in keep[0]:
            a["reasoning"] = keep[0]["reasoning"]
        else:
            a.pop("reasoning", None)
        if keep[1:]:
            a["fallback_models"] = keep[1:]
        else:
            a.pop("fallback_models", None)
    if run_agent not in agents:
        raise PolicyError(f"the run agent {run_agent} has no model in the cell's families {sorted(allowed)}")
    default = {"model": agents[run_agent]["model"]}
    for cname, c in block.get("categories", {}).items():
        ms = [m for m in c.get("models", []) if isinstance(m, dict) and ok(m.get("model", ""))]
        rep["dropped"] += [f"category:{cname}:{m.get('model')}" for m in c.get("models", [])
                           if isinstance(m, dict) and not ok(m.get("model", ""))]
        if isinstance(c.get("model"), str) and not ok(c["model"]):
            rep["dropped"].append(f"category:{cname}:{c['model']}")
            c.pop("model")
        if not ms:
            ms = [dict(default)]
            rep["filled_categories"].append(cname)
        c["models"] = ms
    block["disabled_agents"] = sorted(set(block.get("disabled_agents", [])) | set(rep["disabled_agents"]))
    return rep


def materialize(controller, goal, worktree, scratch, allowed, run_agent):
    """Build the omo config for this run. Returns (text, report)."""
    m = controller.get("materialize", {})
    frag = os.path.join(ROOT, m.get("fragment", f"profiles/{goal['profile']}.example.json"))
    # example profiles carry // comment lines that materialize.py does not strip
    clean = os.path.join(scratch, "fragment.json")
    open(clean, "w", encoding="utf-8").write("\n".join(
        l for l in open(frag, encoding="utf-8").read().splitlines() if not l.lstrip().startswith("//")))
    out = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "materialize.py"), clean, goal["profile"]],
                         capture_output=True, text=True, check=True).stdout
    cfg = json.loads("\n".join(l for l in out.splitlines() if not l.lstrip().startswith("//")))
    block = cfg["[opencode]"]
    rep = restrict(block, allowed, run_agent)
    block["disabled_hooks"] = sorted(set(block.get("disabled_hooks", [])) | set(REQUIRED_HOOKS) | set(m.get("disabled_hooks", [])))
    block["disabled_commands"] = sorted(set(block.get("disabled_commands", [])) | set(REQUIRED_COMMANDS))
    block["goal"] = {"enabled": False}
    block["runtime_fallback"] = {"enabled": False}
    block["team_mode"] = dict(block.get("team_mode", {}), enabled=False)
    fams = {assign.family_of(x) for x in config_models(cfg)}
    if not fams <= set(allowed):
        raise PolicyError(f"materialized config still names families {sorted(fams - set(allowed))}")
    rep["families"] = sorted(fams)
    rep["disabled_hooks"] = block["disabled_hooks"]
    return json.dumps(cfg, indent=2) + "\n", rep


def compose_prompt(goal, iteration, checks, open_findings):
    lines = [f"Goal {goal['id']}: {goal['objective']}", "", "Acceptance criteria:"]
    lines += [f"- {c['name']}: {c['description']}" for c in goal["acceptance"]]
    if checks:
        failing = [c["name"] for c in checks if not c["passed"]]
        lines += ["", "Failing checks from the last batch: " + (", ".join(failing) if failing else "none")]
    if open_findings:
        lines += ["", "Open review findings to address:"]
        lines += [f"- {c['severity']} {c['path']}:{c.get('line_start') or ''} {c['claim']}" for c in open_findings[:20]]
    lines += ["", f"This is batch {iteration}. Work on the next unmet criterion, then stop.",
              "Do not declare the goal complete: the controller runs the checks and an independent review.",
              "Do not edit protected paths: " + (", ".join(goal.get("protected_paths", [])) or "none") + ".",
              "Do not edit .omo/omo.jsonc. Do not send, publish, pay, change permissions or delete anything "
              "outside this worktree.",
              "If you are blocked by something only a person can fix, or the goal needs one of those actions, write "
              ".superloop/status.json with {\"status\": \"blocked\", \"reason\": \"<short code>\"} and stop."]
    return "\n".join(lines)


def read_claims(worktree):
    p = os.path.join(worktree, STATUS_FILE)
    try:
        d = json.load(open(p, encoding="utf-8"))
        return {"status": d.get("status") if d.get("status") in ("blocked", "working", "done") else "unknown"}
    except (OSError, ValueError, AttributeError):
        return {"status": "none"}


def _sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


class Run:
    def __init__(self, goal, controller, worktree, out_dir, deps=None):
        deps = deps or {}
        self.goal, self.ctl, self.wt, self.out = goal, controller, os.path.abspath(worktree), os.path.abspath(out_dir)
        self.clock = deps.get("clock", time.time)
        self.fakes = deps.get("fakes", {})
        self.allow_fakes = bool(deps.get("allow_fakes"))
        self.matrix = deps.get("matrix") or assign.load_matrix()
        self.registry = ledger.Registry(deps.get("registry") or ledger.default_registry())
        self.tools_path = deps.get("tools") or os.environ.get("MM_SUPERLOOP_TOOLS") or \
            os.path.join(os.path.expanduser("~"), ".config", "model-mesh", "superloop-tools.json")
        self.prov = ledger.Provenance()
        self.spent = 0.0
        self.disagreements = 0
        self.decisions = 0
        self.admitted = False
        self.thresholds = {}
        self.log = None
        self.reused = os.path.exists(os.path.join(self.out, "events.jsonl")) or \
            os.path.exists(os.path.join(self.out, "final.json"))
        if self.reused:
            return
        os.makedirs(self.out, exist_ok=True)
        self.scratch = os.path.join(self.out, "scratch")
        os.makedirs(self.scratch, exist_ok=True)
        self.log = ledger.EventLog(os.path.join(self.out, "events.jsonl"), self.clock)

    # -- helpers -------------------------------------------------------------------
    def remaining(self):
        return self.ctl["caps"]["wall_clock_seconds"] - (self.clock() - self.t0)

    def reserve(self, kind, n=1):
        res = self.ctl.get("reservations_usd", {})
        if kind not in res:
            return False  # missing usage is not zero cost
        cost = float(res[kind]) * n
        cap = self.ctl["caps"].get("budget_usd")
        if cap is not None and self.spent + cost > cap + 1e-9:
            return False
        self.spent += cost
        return True

    def finish(self, status, detail, **extra):
        out = {"status": status, "success": status in SUCCESS, "detail": detail, "goal": self.goal.get("id"),
               "profile": self.goal.get("profile"), "situation": self.goal.get("situation"),
               "option": self.goal.get("option"), "mode": self.ctl.get("mode"), "reserved_usd": round(self.spent, 4),
               "decisions": self.decisions, "disagreements": self.disagreements, "provenance": self.prov.snapshot(),
               "isolation": self.ctl.get("worker", {}).get("isolation"), "check_jail": self.ctl.get("check_jail"),
               "protected": self.ctl.get("worker", {}).get("isolation") in ("container", "separate_user")
               and self.ctl.get("check_jail") == "bwrap"}
        out.update(extra)
        if self.log is None:
            return out
        self.log.write("terminal", **out)
        json.dump(out, open(os.path.join(self.out, "final.json"), "w"), indent=2)
        if self.admitted:
            self.registry.append({"repo_key": self.repo_key, "goal": self.goal["id"], "run": self.out,
                                  "status": status, "harnesses": sorted(self.prov.harnesses),
                                  "families": sorted(self.prov.families)})
        return out

    # -- admission ---------------------------------------------------------------
    def admit(self):
        errs = vsl.validate_goal(self.goal) + vsl.validate_controller(self.ctl, self.goal, allow_fake=self.allow_fakes)
        if errs:
            return errs
        try:
            self.a = assign.assignment(self.matrix, self.goal["situation"], self.goal["profile"], self.goal["option"])
        except KeyError as ex:
            return [f"assignment: {ex}"]
        if {s["harness"] for s in self.a["authors"]} != {"opencode-omo"}:
            return [f"{self.goal['situation']}/{self.goal['profile']}/{self.goal['option']} authors do not run on opencode-omo"]
        self.allowed = set().union(*[set(s["families"]) for s in self.a["authors"]])
        if self.a["orchestrator"]:
            self.allowed |= set(self.a["orchestrator"]["families"])
            self.prov.record(0, "orchestrator", self.a["orchestrator"]["harness"], self.a["orchestrator"]["families"])
        for s in self.a["authors"]:
            self.prov.record(0, "author:" + str(s["role"]), s["harness"], s["families"])
        for s in self.goal.get("prior_lineage", []):
            self.prov.record(-1, "prior:" + str(s.get("note", "")), s["harness"], s["families"])
        wt_real, out_real = os.path.realpath(self.wt), os.path.realpath(self.out)
        if out_real == wt_real or out_real.startswith(wt_real + os.sep) or wt_real.startswith(out_real + os.sep):
            return ["the output folder and the worktree must not contain each other; put --out outside the checkout"]
        try:
            self.git_dir, self.common = git_dir_of(self.wt)
        except (PolicyError, OSError) as ex:
            return [f"worktree: {ex}"]
        if not self.registry.exists():
            return [f"lineage registry {self.registry.path} is missing; create it once with --init-registry. "
                    "A missing registry is not an empty history"]
        # the owner names the repository; the registry binds that name to one git directory, so a
        # worker that moves .git between runs cannot start a fresh lineage under the same name
        self.repo_key = self.ctl["repository"]
        bound = self.registry.binding(self.repo_key)
        if bound is None:
            self.registry.bind(self.repo_key, self.common)
        elif bound != self.common:
            return [f"repository {self.repo_key!r} is bound to {bound}, but this worktree's git directory is "
                    f"{self.common}. A moved .git cannot reset the lineage; the owner must investigate"]
        if self.ctl["check_jail"] == "bwrap":
            exe = shutil.which("bwrap")
            ok = exe and subprocess.run([exe, "--unshare-all", "--ro-bind", "/", "/", "--", "true"],
                                        capture_output=True).returncode == 0
            if not ok:
                return ["check_jail bwrap: bubblewrap is missing or cannot create namespaces on this host"]
        for e in self.registry.prior(self.repo_key, self.goal["id"]):
            for h in e.get("harnesses", []) or ["unknown"]:
                self.prov.record(-2, "registry:" + str(e.get("run")), h, e.get("families", []))
        d = self.ctl["decision"]
        lin = d.get("lineage", {})
        if self.ctl["mode"] != "shadow":
            fam = lin.get("base_family")
            if fam not in vsl.KNOWN_FAMILIES:
                return ["advisory mode needs a decision model with a disclosed, known base family"]
            rev_f = set().union(*[set(r["families"]) for r in self.a["reviewers"]]) if self.a["reviewers"] else set()
            if fam in self.prov.families | rev_f | set(self.a["aggregator"]["families"]):
                return [f"decision family {fam} overlaps an author, orchestrator, reviewer or aggregator family"]
            cat = json.load(open(os.path.join(ROOT, d["questions"]), encoding="utf-8"))
            revs = {q["id"]: q["revision"] for q in cat["questions"]}
            for q in self.ctl.get("qualifications", []):
                t, err = qualify.verify_record(q["record"], q["model"], q["question_id"], revs.get(q["question_id"]),
                                               q["locale"])
                if err:
                    return [f"qualification for {q['question_id']}: {err}"]
                self.thresholds[(q["model"], q["question_id"], revs[q["question_id"]], q["locale"])] = t
        if self.goal["profile"] == "ultimate":
            for b in _http_backends(d["backend"]):
                if (urlparse(b.get("base_url", "")).hostname or "") not in LOOPBACK:
                    return ["ultimate profile: only local or offline decision backends are admitted until a "
                            "reachability and data-policy check exists"]
        # tools: the controller names them, the owner's registry defines and pins them
        need_tools = self.ctl["worker"]["kind"] == "omo" or any(r["kind"] == "command" for r in self.ctl.get("reviewers", [])) \
            or self.ctl.get("qualifications")
        try:
            self.tools = json.load(open(self.tools_path, encoding="utf-8")) if need_tools else {}
        except (OSError, ValueError) as ex:
            return [f"tools registry {self.tools_path}: {ex}"]
        if need_tools:
            errs = vsl.validate_tools(self.tools)
            if errs:
                return [f"tools registry: {x}" for x in errs]
        for q in self.ctl.get("qualifications", []):
            rp = os.path.realpath(q["record"])
            pins = {os.path.realpath(k): v for k, v in self.tools.get("qualifications", {}).items()}
            if pins.get(rp) != workers.sha256_file(rp):
                return [f"qualification record {q['record']} is not pinned in the owner's tools registry"]
        self.reviewers = []
        for r in self.ctl.get("reviewers", []):
            seatm = next((s for s in self.a["reviewers"] if s["harness"] == r["harness"]), None)
            if not seatm:
                continue
            if r["kind"] == "command":
                t = self.tools.get("reviewers", {}).get(r["ref"])
                if not t or t.get("harness") != r["harness"]:
                    return [f"reviewer {r['ref']!r} for {r['harness']} is not in the owner's tools registry"]
                _, err = workers.check_pins([t["argv"]], t["pins"])
                if err:
                    return [f"reviewer {r['ref']!r}: {err}"]
                self.reviewers.append((seatm, workers.CommandAdapter(dict(t, tag="review-" + r["ref"]))))
            else:
                self.reviewers.append((seatm, workers.build_fake(r, self.fakes, self.allow_fakes)))
        w = self.ctl["worker"]
        if w["kind"] == "omo":
            t = self.tools.get("workers", {}).get(w["ref"])
            if not t:
                return [f"worker {w['ref']!r} is not in the owner's tools registry"]
            _, err = workers.check_pins([t["argv"], t["export_argv"]], t["pins"])
            if err:
                return [f"worker {w['ref']!r}: {err}"]
            self.worker = workers.OmoWorker(w, t)
            self.pin_version = t["version"]
        else:
            self.worker = workers.build_fake(w, self.fakes, self.allow_fakes)
            self.pin_version = "4.19.4"
        return []

    def tree(self):
        return self.store.tree_hash(self.scratch)

    def setup(self):
        self.store = Store(self.scratch, self.wt)
        r = subprocess.run(["git", "--git-dir=" + self.git_dir, "--no-replace-objects", "-c", "core.hooksPath=" +
                            self.store.hooks, "rev-parse", "--verify", "-q", "HEAD"], capture_output=True, env=self.store.env)
        self.base = r.stdout.decode().strip() or None
        hide = [os.path.realpath(self.wt)]
        for d in (self.git_dir, self.common, os.path.realpath(self.out)):
            if not any(d == h or d.startswith(h + os.sep) for h in hide):
                hide.append(d)
        self.hide = hide
        self.cfg_text, self.mat = materialize(self.ctl, self.goal, self.wt, self.scratch, self.allowed,
                                              self.ctl["worker"].get("agent", "sisyphus"))
        self.cfg_sha = _sha(self.cfg_text)
        self.write_config()
        ver = self.worker.version(self.wt, self.out)
        pin = self.pin_version
        if not re.search(r"(?<![\d.])v?" + re.escape(pin) + r"(?![\d.])", ver):
            raise PolicyError(f"omo reports version {ver!r}, expected {pin}")
        for f in self.mat["families"]:
            self.prov.record(0, "config", "opencode-omo", [f])
        self.protected0 = protected_hashes(self.wt, self.goal.get("protected_paths", []))
        self.base_tree = self.tree()
        base_checks = self.run_checks(0, self.base_tree, tag="baseline")
        if base_checks is not None and all(c["passed"] for c in base_checks):
            raise PolicyError("every acceptance check already passes on the baseline tree; at least one must fail "
                              "before the work, or the checks cannot show it was done")
        cat = json.load(open(os.path.join(ROOT, self.ctl["decision"]["questions"]), encoding="utf-8"))
        self.catalog = {q["id"]: q for q in cat["questions"]}
        self.locale = self.ctl["decision"].get("locale", "en")
        self.rules = decide.RulesBackend(self.catalog)
        self.backend = decide.build_backend(self.ctl["decision"]["backend"], self.catalog)
        self.remote_calls = decide.remote_calls(self.ctl["decision"]["backend"])
        self.log.write("admitted", assignment={k: self.a[k] for k in ("situation", "profile", "option", "pattern")},
                       base=self.base, base_tree=self.base_tree, config_sha256=self.cfg_sha, materialized=self.mat,
                       omo_version=ver, provenance=self.prov.snapshot(), reviewers=[s["harness"] for s, _ in self.reviewers])

    def write_config(self):
        os.makedirs(os.path.join(self.wt, ".omo"), exist_ok=True)
        open(os.path.join(self.wt, OMO_CONFIG), "w", encoding="utf-8").write(self.cfg_text)

    def config_intact(self):
        try:
            return _sha(open(os.path.join(self.wt, OMO_CONFIG), encoding="utf-8").read()) == self.cfg_sha
        except OSError:
            return False

    # -- checks ------------------------------------------------------------------
    def run_checks(self, iteration, tree, tag="check"):
        """Run every acceptance check on a fresh copy of the tree object, each with a shrinking
        share of the wall clock. Returns None when the clock runs out before every check has run."""
        snap = os.path.join(self.scratch, f"snap-{tag}-{iteration:03d}")
        shutil.rmtree(snap, ignore_errors=True)
        self.store.extract(tree, snap)
        home = os.path.join(self.scratch, "check-home")
        os.makedirs(home, exist_ok=True)
        jail = self.ctl["check_jail"] == "bwrap"
        res = []
        try:
            for c in self.goal["acceptance"]:
                left = self.remaining()
                if left <= 0:
                    return None
                argv = jail_argv(c["argv"], snap, self.hide) if jail else c["argv"]
                r = workers.run_bounded(argv, snap, clean_env(home), min(c.get("timeout_seconds", 300), left),
                                        self.out, f"{tag}-{iteration:03d}-{c['name']}")
                res.append({"name": c["name"], "passed": r["exit_code"] == 0 and not r["timed_out"],
                            "exit_code": r["exit_code"], "timed_out": r["timed_out"]})
        finally:
            shutil.rmtree(snap, ignore_errors=True)
        if self.remaining() <= 0:
            return None
        return res

    def verify_reported(self, res, iteration):
        """Refuse a batch whose session agent or model cannot be read or is outside the cell."""
        w = self.ctl["worker"]
        expect = w.get("expect_agents")
        rep = res.get("reported") or {}
        agents, models = rep.get("agents") or [], rep.get("models") or []
        for mid in models:
            self.prov.record(iteration, "reported", "opencode-omo", [assign.family_of(mid)])
        if not expect:
            return None
        if not agents:
            return "the worker's agent could not be read from its session"
        if not models:
            return "the worker's model could not be read from its session"
        wrong = sorted(set(agents) - set(expect))
        if wrong:
            return f"worker session ran as {wrong}, expected only {expect}"
        outside = sorted({assign.family_of(m) for m in models} - self.allowed)
        if outside:
            return f"worker session used model families {outside} outside the cell's {sorted(self.allowed)}"
        return None

    # -- decisions ---------------------------------------------------------------
    def ask(self, ids, facts, claims, iteration, menus=None):
        try:
            st, _ = statemod.build(self.goal, facts, claims, root=self.wt,
                                   budget_tokens=self.ctl["decision"].get("budget_tokens", 30000))
        except ValueError as ex:
            self.log.write("decision_skipped", iteration=iteration, reason=str(ex))
            return {}, {}
        ctx = {"iteration": iteration, "time_left": max(0.0, self.remaining())}
        ra, rrec = decide.ask(self.rules, self.catalog, ids, menus or {}, st, ctx)
        if self.backend.name == "rules":
            ma, mrec = ra, rrec
        elif self.remaining() < 2:
            ma = {q: {"type": "abstain", "reason": "wall clock"} for q in ids}
            mrec = {"backend": self.backend.name, "error": "wall clock", "answers": ma}
        elif self.remote_calls and not self.reserve("decision_call", self.remote_calls):
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
        """Advisory mode only: the brake effects that answers above a verified threshold trigger."""
        if self.ctl["mode"] != "advisory":
            return []
        out = []
        for qid, ans in answers.items():
            q = self.catalog[qid]
            if q.get("authority") != "brake" or ans["type"] == "abstain":
                continue
            t = self.thresholds.get((rec.get("model"), qid, q["revision"], self.locale))
            if t is None:
                continue
            eff = q["effect"]
            hit = (ans["type"] == "noul" and ans["p"] >= t) or \
                  (ans["type"] == "choice" and ans["choice"] in eff.get("on_options", []) and ans["top"] >= t)
            if hit:
                out.append((qid, eff["effect"]))
        return out

    def smoke_qualified(self, rec):
        q = self.catalog.get("goal_met", {})
        return (rec.get("model"), "goal_met", q.get("revision"), self.locale) in self.thresholds

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
        rdir = os.path.join(self.scratch, f"review-{iteration:03d}")
        shutil.rmtree(rdir, ignore_errors=True)
        os.makedirs(rdir)
        diff = os.path.join(rdir, "change.patch")
        self.store.write_diff(self.base_tree, tree, diff)
        findings, ran = [], []
        for seatm, adapter in usable:
            left = self.remaining()
            if left <= 0:
                return {"stop": "cap_wall_clock", "detail": "wall clock ran out before the review"}
            if not self.reserve("review_call"):
                return {"stop": "cap_budget", "detail": "review reservation would exceed the budget"}
            prompt = ("Review the change in the diff file against the lenses " + ", ".join(seatm["lenses"]) +
                      ". You have no other context. Print the findings as one JSON list in the finding schema on the "
                      "last line of standard output. Print [] if there are none.")
            res = adapter.run(rdir, prompt, iteration, min(self.ctl["caps"]["per_call_seconds"], left), self.out,
                              {"diff_file": diff, "lenses": ",".join(seatm["lenses"])})
            ran.append(seatm["harness"])
            if res.get("pin_error"):
                return {"stop": "policy_denied", "ran": ran, "detail": res["error"]}
            if res["exit_code"] != 0 or res["timed_out"]:
                return {"stop": "review_unavailable", "ran": ran,
                        "detail": f"reviewer {seatm['harness']} exited {res['exit_code']} (timed out: {res['timed_out']})"}
            items = workers.parse_findings(res.get("stdout_text"))
            if items is None:
                return {"stop": "review_unavailable", "ran": ran,
                        "detail": f"reviewer {seatm['harness']} printed no findings list on its last output line"}
            errs = agg.check(items)
            if errs:
                sev = {x.get("severity") for x in items if isinstance(x, dict)}
                return {"stop": "review_unavailable", "ran": ran,
                        "detail": f"reviewer {seatm['harness']} findings invalid{' (a blocker was among them)' if 'blocker' in sev else ''}: {errs[:3]}"}
            findings += [dict(x, id=f"{seatm['harness']}:{x['id']}") for x in items]
        if self.remaining() <= 0:
            return {"stop": "cap_wall_clock", "detail": "wall clock ran out during the review"}
        if self.tree() != tree or not self.config_intact():
            return {"stop": "policy_denied", "ran": ran, "detail": "the worktree changed during the review"}
        clusters = agg.cluster(findings)
        blockers = [c for c in clusters if c["severity"] == "blocker"]
        majors = [c for c in clusters if c["severity"] == "major"]
        open_ = [{"severity": c["severity"], "category": c["category"], "path": c["path"],
                  "line_start": c.get("line_start"), "claim": c["claims"][0], "corroborated": c["corroborated"]}
                 for c in blockers + majors]
        return {"tree": tree, "ran": ran, "clusters": len(clusters), "blockers": len(blockers), "majors": len(majors),
                "corroborated_majors": sum(1 for c in majors if c["corroborated"]), "open": open_}

    # -- main loop ---------------------------------------------------------------
    def run(self):
        try:
            return self._run()
        except Exception as ex:  # any failure ends in final.json, never a bare traceback
            return self.finish("policy_denied", f"{type(ex).__name__}: {ex}")

    def _run(self):
        if self.reused:
            return self.finish("policy_denied", "the output directory already holds a run; use a new one")
        self.t0 = self.clock()
        errs = self.admit()
        if errs:
            return self.finish("policy_denied", errs)
        self.admitted = True
        try:
            self.setup()
        except Exception as ex:
            return self.finish("policy_denied", f"{type(ex).__name__}: {ex}")
        caps = self.ctl["caps"]
        prev_passing, prev_failing, idle = set(), None, 0
        cycles, checks, open_findings, last_review, review_rounds = {}, [], [], None, 0
        tree = self.base_tree
        self.ask(["situation"], {"iteration": 0}, None, 0)
        for it in range(1, caps["max_iterations"] + 2):
            if os.path.exists(os.path.join(self.out, "STOP")):
                return self.finish("cancelled", "stop file present", iterations=it - 1)
            if it > caps["max_iterations"]:
                return self.finish("cap_iterations", f"{caps['max_iterations']} iterations", iterations=it - 1)
            if self.remaining() <= 0:
                return self.finish("cap_wall_clock", f"{caps['wall_clock_seconds']} s", iterations=it - 1)
            if not self.reserve("worker_call"):
                return self.finish("cap_budget", f"reservation would exceed {caps.get('budget_usd')} USD", iterations=it - 1)
            self.write_config()
            prompt = compose_prompt(self.goal, it, checks, open_findings)
            res = self.worker.run(self.wt, prompt, it, min(caps["per_call_seconds"], self.remaining()), self.out)
            for s in self.a["authors"]:
                self.prov.record(it, "author:" + str(s["role"]), s["harness"], s["families"])
            self.log.write("worker", iteration=it, exit_code=res["exit_code"], timed_out=res["timed_out"],
                           duration=res["duration"], reported=res.get("reported"), error=res.get("error"))
            if res["exit_code"] is None and not res["timed_out"]:
                return self.finish("worker_failure", res.get("error"), iterations=it)
            if not self.config_intact():
                return self.finish("policy_denied", "the worker changed .omo/omo.jsonc", iterations=it)
            try:
                moved = git_dir_of(self.wt) != (self.git_dir, self.common)
            except (PolicyError, OSError):
                moved = True
            if moved:
                return self.finish("policy_denied", "the worker moved or replaced the worktree's .git", iterations=it)
            bad = self.verify_reported(res, it)
            if bad:
                return self.finish("policy_denied", bad, iterations=it)
            claims = read_claims(self.wt)
            tree_prev, tree = tree, self.tree()
            checks = self.run_checks(it, tree)
            if checks is None:
                return self.finish("cap_wall_clock", "wall clock ran out during the checks", iterations=it)
            passing = {c["name"] for c in checks if c["passed"]}
            failing = sorted(c["name"] for c in checks if not c["passed"])
            prot = protected_hashes(self.wt, self.goal.get("protected_paths", []))
            touched = sorted(k for k in set(prot) | set(self.protected0) if prot.get(k) != self.protected0.get(k))
            # a batch is idle when it left the tree as it found it and the failing checks unchanged
            idle = idle + 1 if tree == tree_prev and (prev_failing is None or failing == prev_failing) else 0
            prev_failing = failing
            regressed = sorted(prev_passing - passing)
            prev_passing = passing
            if failing:
                key = "checks:" + ",".join(failing)
                cycles[key] = cycles.get(key, 0) + 1
            facts = {"iteration": it, "max_iterations": caps["max_iterations"], "checks_run": len(checks),
                     "checks_failed": len(failing), "failing_checks": failing, "tree_changed": tree != tree_prev,
                     "unchanged_streak": idle, "regressed": bool(regressed), "regressed_checks": regressed,
                     "touches_protected": bool(touched), "worker_exit": res["exit_code"],
                     "worker_timed_out": res["timed_out"], "worker_reported_blocked": claims["status"] == "blocked",
                     "remaining_fraction": round(max(0.0, self.remaining()) / caps["wall_clock_seconds"], 3),
                     "review": {k: last_review.get(k) for k in ("blockers", "majors", "clusters")} if last_review else None}
            self.log.write("facts", **facts)
            answers, rec = self.ask(["progress", "blocked", "needs_human", "goal_met", "next_action"], facts, claims, it)
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
            if idle >= caps["no_progress_streak"]:
                return self.finish("no_progress", f"{idle} batches in a row left the tree and the failing checks unchanged",
                                   iterations=it)
            if any(e == "stop_no_progress" for _, e in effects):
                return self.finish("no_progress", f"decision brake: {effects}", iterations=it)
            worst = max(cycles.values()) if cycles else 0
            if worst >= caps["fix_verify_cycles"]:
                return self.finish("fix_cycles_exhausted", f"{worst} cycles on {max(cycles, key=cycles.get)}", iterations=it)
            green = bool(checks) and not failing
            if green and tree == self.base_tree:
                # the same tree failed these checks at admission, so a pass now came from outside it
                return self.finish("policy_denied", "the checks pass on the tree that failed them at admission; "
                                   "they depend on something outside the tree", iterations=it)
            cadence = self.ctl.get("review", {}).get("every_k_iterations")
            smoke = green and answers.get("goal_met", {}).get("type") == "noul" and \
                answers["goal_met"]["p"] < self.ctl.get("review", {}).get("smoke_below", 0.5)
            extra_review = any(e == "add_review" for _, e in effects) or \
                (smoke and self.ctl["mode"] == "advisory" and self.smoke_qualified(rec))
            if smoke:
                self.log.write("smoke_detector", iteration=it, p=answers["goal_met"]["p"], acted=extra_review)
            if not (green or extra_review or (cadence and it % cadence == 0)):
                continue
            rv = self.review(it, tree, all_seats=extra_review)
            if rv is None:
                return self.finish("review_unavailable", "no reviewer is independent of this run's lineage", iterations=it)
            if "stop" in rv:
                self.log.write("review", iteration=it, **rv)
                return self.finish(rv["stop"], rv["detail"], iterations=it)
            self.log.write("review", iteration=it, **rv)
            last_review, open_findings = rv, rv["open"]
            if rv["blockers"] or rv["majors"]:
                review_rounds += 1
                if review_rounds >= caps["fix_verify_cycles"]:
                    return self.finish("fix_cycles_exhausted", f"{review_rounds} reviews in a row found a blocker or major",
                                       iterations=it, open_findings=open_findings)
                continue
            review_rounds = 0
            if not green:
                continue
            again = self.run_checks(it, rv["tree"], tag="recheck")
            if again is None:
                return self.finish("cap_wall_clock", "wall clock ran out during the recheck", iterations=it)
            if not all(c["passed"] for c in again) or self.tree() != rv["tree"] or not self.config_intact():
                self.log.write("recheck_failed", iteration=it, checks=again)
                checks = again
                continue
            if self.remaining() <= 0:
                return self.finish("cap_wall_clock", "wall clock ran out before success", iterations=it)
            status = "verified_pending_owner" if self.goal.get("owner_approval_required", True) else "verified"
            return self.finish(status, "checks pass twice on the reviewed tree and an independent review found no "
                                       "blocker and no major", iterations=it, tree=rv["tree"], review=rv["ran"],
                               open_findings=[])
        return self.finish("cap_iterations", "loop bound", iterations=caps["max_iterations"])


def _http_backends(spec):
    if spec.get("kind") == "http":
        return [spec]
    if spec.get("kind") == "dual":
        return _http_backends(spec.get("first", {})) + _http_backends(spec.get("second", {}))
    return []
