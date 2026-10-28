"""Worker and reviewer adapters.

An adapter runs one bounded batch and returns what happened. It never decides success: exit 0
means the process stopped, not that the goal was met.

  omo       one call of the oh-my-openagent run command in the run's worktree, from a pinned
            local install, with the agent named by config key. omo's own continuation hooks
            are disabled in the materialized config, so this call is one batch and the
            superloop owns continuation. The adapter records the agent and model the JSON
            output reports, if any, so the driver can check them against the assignment.
  command   any harness, from an argv template with {worktree}, {prompt_file}, {findings_out}
            and {diff_file} placeholders. Used for cross-family reviewers.
  fake      a Python callable. For offline tests.

Every process runs in its own process group with a hard timeout; on timeout the whole group
gets SIGTERM, then SIGKILL.
"""
import json, os, signal, subprocess, time


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
            code = p.wait(timeout=max(1.0, timeout))
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


def parse_json_output(path):
    """Find reported agent and model in JSON output: one JSON document, or JSON lines."""
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return {}
    docs = []
    try:
        docs = [json.loads(text)]
    except ValueError:
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("{"):
                try:
                    docs.append(json.loads(line))
                except ValueError:
                    pass
    found = {}

    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k in ("agent", "agentName") and isinstance(v, str):
                    found.setdefault("agent", v)
                elif k in ("model", "modelID", "modelId") and isinstance(v, str):
                    found.setdefault("model", v)
                else:
                    walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    for d in docs:
        walk(d)
    return found


class OmoWorker:
    kind = "omo"

    def __init__(self, cfg):
        self.cfg = cfg

    def argv(self, worktree, prompt):
        return [self.cfg["binary"], "run", "--agent", self.cfg.get("agent", "sisyphus"), "--json",
                "--directory", worktree, prompt]

    def run(self, worktree, prompt, iteration, timeout, out_dir):
        env = dict(os.environ)
        env.update(self.cfg.get("env", {}))
        env["OMO_SEND_ANONYMOUS_TELEMETRY"] = "0"
        res = run_bounded(self.argv(worktree, prompt), worktree, env, timeout, out_dir, f"worker-{iteration:03d}")
        res["reported"] = parse_json_output(res["stdout"])
        return res


class CommandAdapter:
    kind = "command"

    def __init__(self, cfg):
        self.cfg = cfg

    def run(self, worktree, prompt, iteration, timeout, out_dir, extra=None):
        os.makedirs(out_dir, exist_ok=True)
        pf = os.path.join(out_dir, f"{self.cfg.get('tag', 'cmd')}-{iteration:03d}.prompt.txt")
        open(pf, "w", encoding="utf-8").write(prompt)
        subs = {"worktree": worktree, "prompt_file": pf}
        subs.update(extra or {})
        argv = [a.format(**subs) for a in self.cfg["argv"]]
        env = dict(os.environ)
        env.update(self.cfg.get("env", {}))
        res = run_bounded(argv, worktree, env, timeout, out_dir, f"{self.cfg.get('tag', 'cmd')}-{iteration:03d}")
        res["reported"] = parse_json_output(res["stdout"])
        return res


class FakeWorker:
    kind = "fake"

    def __init__(self, fn):
        self.fn = fn

    def run(self, worktree, prompt, iteration, timeout, out_dir, extra=None):
        t0 = time.time()
        rep = self.fn(worktree, prompt, iteration, extra or {}) or {}
        return {"exit_code": rep.get("exit_code", 0), "timed_out": rep.get("timed_out", False),
                "duration": round(time.time() - t0, 3), "stdout": None, "stderr": None, "error": None,
                "reported": rep.get("reported", {})}


def build(cfg, fakes=None):
    if cfg["kind"] == "omo":
        return OmoWorker(cfg)
    if cfg["kind"] == "command":
        return CommandAdapter(cfg)
    if cfg["kind"] == "fake":
        return FakeWorker((fakes or {})[cfg["name"]])
    raise ValueError(f"unknown adapter kind {cfg['kind']}")
