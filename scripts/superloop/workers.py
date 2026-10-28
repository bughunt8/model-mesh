"""Worker and reviewer adapters.

An adapter runs one bounded batch and returns what happened. It never decides success: exit 0
means the process stopped, not that the goal was met.

  omo       one call of the oh-my-openagent run command in the run's worktree, from a pinned
            local install, with the agent named by config key. omo's own continuation hooks
            are disabled in the materialized config, so this call is one batch and the
            superloop owns continuation. In 4.19.4 the --json result carries only sessionId,
            success, durationMs, messageCount and summary, so the adapter reads the agent and
            model of the session from an export command (default `opencode export <id>`).
            The driver refuses the batch when it cannot read them. Not run live.
  command   a reviewer harness, from an argv template held in the owner's reviewer registry,
            outside the worktree and outside the controller. Placeholders: {review_dir},
            {prompt_file}, {findings_out}, {diff_file} and {lenses}. It runs in a fresh review
            directory, never in the worktree.
  fake      a Python callable. Offline tests only; the driver refuses it otherwise.

Every process runs in its own process group with a hard timeout; on timeout the whole group
gets SIGTERM, then SIGKILL.
"""
import hashlib, json, os, shutil, signal, subprocess, time


def run_bounded(argv, cwd, env, timeout, out_dir, tag):
    os.makedirs(out_dir, exist_ok=True)
    so, se = os.path.join(out_dir, tag + ".stdout"), os.path.join(out_dir, tag + ".stderr")
    t0 = time.time()
    timed_out = False
    with open(so, "wb") as fo, open(se, "wb") as fe:
        try:
            p = subprocess.Popen(argv, cwd=cwd, env=env, stdout=fo, stderr=fe, start_new_session=True)
        except OSError as ex:
            fe.write(str(ex).encode())
            return {"exit_code": None, "timed_out": False, "duration": 0.0, "stdout": so, "stderr": se,
                    "error": f"could not start: {ex}"}
        try:
            code = p.wait(timeout=max(0.5, timeout))
        except subprocess.TimeoutExpired:
            timed_out = True
            for sig in (signal.SIGTERM, signal.SIGKILL):
                try:
                    os.killpg(p.pid, sig)
                except ProcessLookupError:
                    break
                try:
                    p.wait(timeout=10)
                    break
                except subprocess.TimeoutExpired:
                    continue
            code = p.returncode
    return {"exit_code": code, "timed_out": timed_out, "duration": round(time.time() - t0, 3),
            "stdout": so, "stderr": se, "error": None}


def _json_docs(text):
    try:
        return [json.loads(text)]
    except ValueError:
        docs = []
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("{"):
                try:
                    docs.append(json.loads(line))
                except ValueError:
                    pass
        return docs


def parse_run_result(path):
    """The RunResult of `oh-my-openagent run --json`: the last JSON object with a sessionId."""
    try:
        docs = _json_docs(open(path, encoding="utf-8", errors="replace").read())
    except OSError:
        return {}
    for d in reversed(docs):
        if isinstance(d, dict) and isinstance(d.get("sessionId"), str):
            return {"session_id": d["sessionId"], "run_success_claim": d.get("success")}
    return {}


def parse_session(text):
    """Every agent name and provider/model pair in a session export. All of them are returned,
    so one unexpected agent or model anywhere in the session is visible to the driver."""
    agents, models = set(), set()

    def walk(x):
        if isinstance(x, dict):
            for k in ("agent", "agentName", "mode"):
                if isinstance(x.get(k), str) and x[k]:
                    agents.add(x[k])
            prov, mid = x.get("providerID"), x.get("modelID")
            if isinstance(prov, str) and isinstance(mid, str):
                models.add(f"{prov}/{mid}")
            elif isinstance(x.get("model"), str) and "/" in x["model"]:
                models.add(x["model"])
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    for d in _json_docs(text):
        walk(d)
    return {"agents": sorted(agents), "models": sorted(models)}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class OmoWorker:
    kind = "omo"

    def __init__(self, cfg):
        self.cfg = cfg

    def argv(self, worktree, prompt):
        return [self.cfg["binary"], "run", "--agent", self.cfg.get("agent", "sisyphus"), "--json",
                "--directory", worktree, prompt]

    def version(self, worktree, out_dir):
        r = run_bounded([self.cfg["binary"], "--version"], worktree, dict(os.environ), 60, out_dir, "omo-version")
        try:
            return open(r["stdout"], encoding="utf-8", errors="replace").read().strip()
        except OSError:
            return ""

    def run(self, worktree, prompt, iteration, timeout, out_dir):
        env = dict(os.environ)
        env.update(self.cfg.get("env", {}))
        env["OMO_SEND_ANONYMOUS_TELEMETRY"] = "0"
        t0 = time.time()
        res = run_bounded(self.argv(worktree, prompt), worktree, env, timeout, out_dir, f"worker-{iteration:03d}")
        rep = parse_run_result(res["stdout"])
        if rep.get("session_id"):
            left = max(5.0, timeout - (time.time() - t0))
            argv = [a.format(session_id=rep["session_id"]) for a in
                    self.cfg.get("export_argv", ["opencode", "export", "{session_id}"])]
            ex = run_bounded(argv, worktree, env, min(60.0, left), out_dir, f"export-{iteration:03d}")
            if ex["exit_code"] == 0 and not ex["timed_out"]:
                rep.update(parse_session(open(ex["stdout"], encoding="utf-8", errors="replace").read()))
        res["reported"] = rep
        return res


class CommandAdapter:
    kind = "command"

    def __init__(self, cfg):
        self.cfg = cfg

    def run(self, cwd, prompt, iteration, timeout, out_dir, extra=None):
        os.makedirs(out_dir, exist_ok=True)
        tag = f"{self.cfg.get('tag', 'review')}-{iteration:03d}"
        pf = os.path.join(cwd, "prompt.txt")
        open(pf, "w", encoding="utf-8").write(prompt)
        subs = {"review_dir": cwd, "prompt_file": pf}
        subs.update(extra or {})
        argv = [a.format(**subs) for a in self.cfg["argv"]]
        env = dict(os.environ)
        env.update(self.cfg.get("env", {}))
        res = run_bounded(argv, cwd, env, timeout, out_dir, tag)
        res["reported"] = {}
        return res


class FakeWorker:
    kind = "fake"

    def __init__(self, fn):
        self.fn = fn

    fake_version = "4.19.4"

    def version(self, worktree, out_dir):
        return self.fake_version

    def run(self, worktree, prompt, iteration, timeout, out_dir, extra=None):
        t0 = time.time()
        rep = self.fn(worktree, prompt, iteration, extra or {}) or {}
        return {"exit_code": rep.get("exit_code", 0), "timed_out": rep.get("timed_out", False),
                "duration": round(time.time() - t0, 3), "stdout": None, "stderr": None, "error": None,
                "reported": rep.get("reported", {})}


def resolve_reviewer(entry, registry):
    """Look a controller reviewer reference up in the owner's registry and check its pins.
    Returns (cfg, error)."""
    ref = entry.get("ref")
    r = (registry or {}).get("reviewers", {}).get(ref)
    if not r:
        return None, f"reviewer {ref!r} is not in the owner's reviewer registry"
    if r.get("harness") != entry.get("harness"):
        return None, f"reviewer {ref!r} is registered for harness {r.get('harness')}, not {entry.get('harness')}"
    argv = r.get("argv")
    if not isinstance(argv, list) or not argv or not all(isinstance(a, str) for a in argv):
        return None, f"reviewer {ref!r}: argv must be a non-empty list of strings"
    exe = shutil.which(argv[0]) or (argv[0] if os.path.isfile(argv[0]) else None)
    if not exe:
        return None, f"reviewer {ref!r}: {argv[0]} not found"
    pins = r.get("pins", {})
    if os.path.realpath(exe) not in {os.path.realpath(p) for p in pins}:
        return None, f"reviewer {ref!r}: the executable {exe} has no pinned hash"
    for p, want in pins.items():
        if not os.path.isfile(p) or sha256_file(p) != want:
            return None, f"reviewer {ref!r}: {p} does not match its pinned hash"
    return dict(r, tag="review-" + str(ref)), None


def build(cfg, fakes=None, allow_fakes=False):
    if cfg["kind"] == "omo":
        return OmoWorker(cfg)
    if cfg["kind"] == "command":
        return CommandAdapter(cfg)
    if cfg["kind"] == "fake":
        if not allow_fakes:
            raise PermissionError("fake adapters are for the offline self-test only")
        fw = FakeWorker((fakes or {})[cfg["name"]])
        fw.fake_version = (fakes or {}).get(cfg["name"] + "@version", "4.19.4")
        return fw
    raise ValueError(f"unknown adapter kind {cfg['kind']}")
