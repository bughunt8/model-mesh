"""Worker and reviewer adapters.

An adapter runs one bounded batch and returns what happened. It never decides success: exit 0
means the process stopped, not that the goal was met.

Tools come from the owner's tools registry, never from the controller. The registry holds the
argv of each worker and reviewer and a SHA-256 for every file in it. Every pin is hashed again
immediately before each call, and the resolved real path of the executable is what runs.

  omo       one call of the oh-my-openagent run command in the run's worktree. omo's own
            continuation hooks are disabled in the materialized config, so this call is one
            batch and the superloop owns continuation. In 4.19.4 the --json result carries only
            sessionId, success, durationMs, messageCount and summary, so the adapter reads the
            agents and models of the session from the registry's pinned export command
            (for example `opencode export <id>`). Not run live.
  command   a reviewer. It runs in a fresh review folder, never in the worktree, and its
            findings are the JSON list on the last non-empty line of its standard output, read
            through a pipe, so no file the worker could reach is trusted. Placeholders:
            {review_dir}, {prompt_file}, {diff_file} and {lenses}.
  fake      a Python callable. Offline tests only; the driver refuses it otherwise.

Every process runs in its own process group with a hard timeout; on timeout the whole group
gets SIGTERM, then SIGKILL.
"""
import hashlib, json, os, shutil, signal, subprocess, time


def _kill(p):
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(p.pid, sig)
        except ProcessLookupError:
            return
        try:
            p.wait(timeout=10)
            return
        except subprocess.TimeoutExpired:
            continue


def run_bounded(argv, cwd, env, timeout, out_dir, tag, capture=False):
    """Run argv with a hard timeout. With capture, stdout is read through a pipe and returned
    as text instead of going to a file."""
    os.makedirs(out_dir, exist_ok=True)
    so, se = os.path.join(out_dir, tag + ".stdout"), os.path.join(out_dir, tag + ".stderr")
    t0 = time.time()
    timed_out, text = False, None
    with open(se, "wb") as fe, (open(os.devnull, "wb") if capture else open(so, "wb")) as fo:
        try:
            p = subprocess.Popen(argv, cwd=cwd, env=env, stdout=subprocess.PIPE if capture else fo, stderr=fe,
                                 start_new_session=True)
        except OSError as ex:
            fe.write(str(ex).encode())
            return {"exit_code": None, "timed_out": False, "duration": 0.0, "stdout": None, "stderr": se,
                    "stdout_text": None, "error": f"could not start: {ex}"}
        try:
            if capture:
                out, _ = p.communicate(timeout=max(0.5, timeout))
                text = out.decode("utf-8", errors="replace")
            else:
                p.wait(timeout=max(0.5, timeout))
        except subprocess.TimeoutExpired:
            timed_out = True
            _kill(p)
            if capture:
                try:
                    p.communicate(timeout=5)
                except (subprocess.TimeoutExpired, ValueError):
                    pass
        code = p.returncode
    return {"exit_code": code, "timed_out": timed_out, "duration": round(time.time() - t0, 3),
            "stdout": None if capture else so, "stderr": se, "stdout_text": text, "error": None}


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
    except (OSError, TypeError):
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
            for k in ("agent", "agentName"):
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


def parse_findings(text):
    """The findings list: the last non-empty stdout line that parses as a JSON list."""
    for line in reversed((text or "").splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            v = json.loads(line)
        except ValueError:
            return None
        return v if isinstance(v, list) else None
    return None


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def path_like(a):
    return "/" in a and "{" not in a


def resolve_exec(a):
    exe = shutil.which(a) if "/" not in a else (a if os.path.isfile(a) else None)
    return os.path.realpath(exe) if exe else None


def check_pins(argvs, pins):
    """Return (resolved argvs, error). Every path in the argvs and every executable must be pinned,
    and every pin must match now."""
    real = {os.path.realpath(p): v for p, v in (pins or {}).items()}
    out = []
    for argv in argvs:
        exe = resolve_exec(argv[0])
        if not exe:
            return None, f"{argv[0]} not found"
        need = [exe] + [os.path.realpath(a) for a in argv[1:] if path_like(a)]
        for n in need:
            if n not in real:
                return None, f"{n} has no pinned hash"
        out.append([exe] + list(argv[1:]))
    for p, want in real.items():
        if not os.path.isfile(p) or sha256_file(p) != want:
            return None, f"{p} does not match its pinned hash"
    return out, None


class OmoWorker:
    kind = "omo"

    def __init__(self, cfg, tool, jail=None):
        self.cfg, self.tool, self.jail = cfg, tool, jail

    def _wrap(self, argv, worktree):
        if not self.jail:
            return argv
        from .control import worker_jail_argv  # late import: control imports this module
        return worker_jail_argv(self.jail["bwrap"](), argv, worktree, self.jail["writable"])

    def _argvs(self):
        argvs, err = check_pins([self.tool["argv"], self.tool["export_argv"]], self.tool["pins"])
        if err:
            raise PermissionError(f"omo tool: {err}")
        return argvs

    def version(self, worktree, out_dir):
        base, _ = self._argvs()
        r = run_bounded(self._wrap(base + ["--version"], worktree), worktree, dict(os.environ), 60, out_dir,
                        "omo-version", capture=True)
        return (r["stdout_text"] or "").strip()

    def run(self, worktree, prompt, iteration, timeout, out_dir):
        env = dict(os.environ)
        env.update(self.cfg.get("env", {}))
        env["OMO_SEND_ANONYMOUS_TELEMETRY"] = "0"
        t0 = time.time()
        try:
            base, _ = self._argvs()
        except PermissionError as ex:
            return {"exit_code": None, "timed_out": False, "duration": 0.0, "error": str(ex), "reported": {}}
        argv = base + ["run", "--agent", self.cfg.get("agent", "sisyphus"), "--json", "--directory", worktree, prompt]
        try:
            argv = self._wrap(argv, worktree)
        except PermissionError as ex:
            return {"exit_code": None, "timed_out": False, "duration": 0.0, "error": str(ex), "reported": {}}
        res = run_bounded(argv, worktree, env, timeout, out_dir, f"worker-{iteration:03d}")
        rep = parse_run_result(res["stdout"])
        if rep.get("session_id"):
            try:
                _, export = self._argvs()  # pins again: the batch may have replaced the export program
            except PermissionError as ex:
                rep["export_error"] = str(ex)
            else:
                left = max(5.0, timeout - (time.time() - t0))
                ex = run_bounded([a.format(session_id=rep["session_id"]) for a in export], worktree, env,
                                 min(60.0, left), out_dir, f"export-{iteration:03d}", capture=True)
                if ex["exit_code"] == 0 and not ex["timed_out"]:
                    rep.update(parse_session(ex["stdout_text"]))
        res["reported"] = rep
        return res


class CommandAdapter:
    kind = "command"

    def __init__(self, tool):
        self.tool = tool

    def run(self, cwd, prompt, iteration, timeout, out_dir, extra=None):
        argvs, err = check_pins([self.tool["argv"]], self.tool["pins"])
        if err:
            return {"exit_code": None, "timed_out": False, "stdout_text": None, "error": f"reviewer tool: {err}",
                    "pin_error": True}
        pf = os.path.join(cwd, "prompt.txt")
        open(pf, "w", encoding="utf-8").write(prompt)
        subs = {"review_dir": cwd, "prompt_file": pf}
        subs.update(extra or {})
        argv = [a.format(**subs) for a in argvs[0]]
        env = dict(os.environ)
        env.update(self.tool.get("env", {}))
        return run_bounded(argv, cwd, env, timeout, out_dir, f"{self.tool.get('tag', 'review')}-{iteration:03d}", capture=True)


class FakeWorker:
    kind = "fake"
    fake_version = "4.19.4"

    def __init__(self, fn):
        self.fn = fn

    def version(self, worktree, out_dir):
        return self.fake_version

    def run(self, worktree, prompt, iteration, timeout, out_dir, extra=None):
        t0 = time.time()
        rep = self.fn(worktree, prompt, iteration, extra or {}) or {}
        return {"exit_code": rep.get("exit_code", 0), "timed_out": rep.get("timed_out", False),
                "duration": round(time.time() - t0, 3), "stdout": None, "stderr": None, "error": None,
                "stdout_text": rep.get("stdout"), "reported": rep.get("reported", {})}


def build_fake(cfg, fakes, allow_fakes):
    if not allow_fakes:
        raise PermissionError("fake adapters are for the offline self-test only")
    fw = FakeWorker((fakes or {})[cfg["name"]])
    fw.fake_version = (fakes or {}).get(cfg["name"] + "@version", "4.19.4")
    return fw
