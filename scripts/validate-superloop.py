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
      least one acceptance check given as an argv list with a timeout, and protected paths. A
      check may not be an obvious no-op (true, :, echo, exit 0). This is a first filter only:
      the driver also refuses a goal whose checks all pass on the baseline tree, and checks
      always run on a copy of the hashed tree, so they cannot read the status file, the omo
      config or anything under .git.
  L3  caps: max_iterations 1 to 50, wall_clock_seconds 60 to 86400, no_progress_streak and
      fix_verify_cycles at least 1, per_call_seconds positive, and a positive budget_usd.
  L4  mode is shadow or advisory. There is no control mode.
  L5  decision backend: rules, replay, http or dual. An http backend uses https (plain http only
      on a loopback host), a path, a model ID with a version number and no moving alias
      (latest, preview, stable, default, current, beta, nightly, auto), and the name of an
      environment variable for the key, never a key. dual needs a consequential question list.
  L6  advisory mode needs a decision base family from the known family list and at least one
      qualification entry for a brake or smoke question. Each entry points at a record file
      written by scripts/superloop/qualify.py; the record must verify: the labelled dataset
      still matches its hash, has at least 100 labels from people or ground truth, and
      re-running learn-then-test gives the recorded threshold. The entry's model must be the
      backend's pinned model.
  L7  the ultimate profile admits only local (loopback) or offline decision backends, until a
      reachability and data-policy check exists. A controller flag cannot override this.
  L8  worker: kind omo with a ref into the owner's tools registry and no binary, version or
      export command of its own, an agent, expect_agents, a stated isolation (separate_user,
      container or none), and disabled_hooks naming goal, todo-continuation-enforcer,
      start-work, atlas and runtime-fallback. The driver adds the hooks anyway.
  L9  reviewers: kind command with a ref into the owner's tools registry and no argv or env of
      their own, never on opencode-omo, and each names a harness.
  L10 reservations: worker_call and review_call above zero, decision_call above zero when a
      remote backend is used, every reservation non-negative. Missing usage is not zero cost.
  L11 tools registry (examples/superloop/tools.example.json, or the owner's file, checked again
      at admission): a reviewer names a harness, an argv list that passes {diff_file}, and pins;
      a worker names an argv list (no runtime package download), an export_argv with
      {session_id}, version 4.19.4 and pins; every absolute path in an argv and the executable
      itself must be pinned with a SHA-256; qualification record pins map a path to a SHA-256.
      The driver hashes every pin again immediately before each call.

Fake workers and reviewers pass only when the caller allows them, which only the offline
self-test does.

Usage:
  python scripts/validate-superloop.py                      check the committed examples
  python scripts/validate-superloop.py GOAL CONTROLLER      check one pair
  python scripts/validate-superloop.py --self-test
"""
import copy, importlib.util, io, json, os, re, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _mod(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_vo = _mod("_vo_sl", "scripts/validate-orchestration.py")
_q = _mod("_q_sl", "scripts/superloop/qualify.py")
KNOWN_FAMILIES = set(_vo.PREFIX_FAMILY.values()) | {"google"}
TOOLS_EXAMPLE = os.path.join(ROOT, "examples", "superloop", "tools.example.json")
ISOLATION = {"separate_user", "container", "none"}
DOWNLOADERS = {"bunx", "npx", "pnpx", "yarn", "npm", "pnpm", "uvx", "pipx"}
QUESTIONS = os.path.join(ROOT, "examples", "superloop", "questions.json")
EXAMPLES = [("examples/superloop/goal.example.json", "examples/superloop/controller.example.json"),
            ("examples/superloop/goal.example.json", "examples/superloop/controller.rules.example.json")]
REQUIRED_Q = {"situation", "progress", "blocked", "needs_human", "goal_met", "next_action"}
RULE_NAMES = {"situation", "progress", "blocked", "needs_human", "goal_met", "next_action"}
BRAKE_EFFECTS = {"pause_human", "stop_no_progress", "add_review"}
PROFILES = {"ultimate", "hybrid", "b4b", "global"}
SITUATIONS = {f"A{i:02d}" for i in range(1, 13)}
REQUIRED_HOOKS = {"goal", "todo-continuation-enforcer", "start-work", "atlas", "runtime-fallback"}
ALIAS = re.compile(r"(latest|preview|stable|default|current|beta|nightly|auto)", re.I)
VERSIONED = re.compile(r"\d+\.\d+")
LOOPBACK = {"127.0.0.1", "localhost", "::1"}
NOOP = {"true", ":", "echo", "printf"}
HIDDEN = (".superloop/status.json", ".omo/")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
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
            argv = c.get("argv") if isinstance(c.get("argv"), list) else []
            if argv and _noop(argv):
                e.append(f"L2 check {c.get('name')}: a no-op command is not an acceptance check")
            if any(h in str(a) for a in argv for h in HIDDEN):
                e.append(f"L2 check {c.get('name')}: may not read the status file or the omo config")
    if not isinstance(g.get("protected_paths"), list):
        e.append("L2 goal.protected_paths must be a list (it may be empty)")
    for pl in g.get("prior_lineage", []):
        if not isinstance(pl, dict) or not pl.get("harness") or not isinstance(pl.get("families"), list):
            e.append("L2 prior_lineage entries need a harness and a families list")
    return e


def _noop(argv):
    base = os.path.basename(argv[0])
    if base in NOOP:
        return True
    if base in ("sh", "bash", "zsh", "dash") and len(argv) >= 3 and argv[1] == "-c" and \
            argv[2].strip() in ("true", ":", "exit 0", "exit", ""):
        return True
    return base in ("python", "python3") and len(argv) >= 3 and argv[1] == "-c" and \
        argv[2].strip() in ("pass", "", "import sys; sys.exit(0)", "raise SystemExit(0)")


def validate_controller(c, g=None, catalog=None, allow_fake=False):
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
        if fam not in KNOWN_FAMILIES:
            e.append("L6 advisory mode needs decision.lineage.base_family from the known family list")
        quals = c.get("qualifications", [])
        if not quals:
            e.append("L6 advisory mode needs at least one qualification entry")
        pinned = _models(b)
        for qr in quals:
            q = qmap.get(qr.get("question_id"), {})
            if q.get("authority") not in ("brake", "smoke"):
                e.append(f"L6 qualification for {qr.get('question_id')}: not a brake or smoke question")
            if qr.get("model") not in pinned:
                e.append(f"L6 qualification model {qr.get('model')} is not the backend's pinned model")
            if not isinstance(qr.get("locale"), str):
                e.append("L6 qualification needs a locale")
            rec = qr.get("record")
            if not isinstance(rec, str) or not os.path.isfile(rec):
                e.append(f"L6 qualification for {qr.get('question_id')}: record file missing")
                continue
            _, err = _q.verify_record(rec, qr.get("model"), qr.get("question_id"), q.get("revision"), qr.get("locale"))
            if err:
                e.append(f"L6 qualification for {qr.get('question_id')}: {err}")
    if g and g.get("profile") == "ultimate":
        for hb in _http(b):
            if _host(hb.get("base_url", "")) not in LOOPBACK:
                e.append("L7 ultimate profile admits only local or offline decision backends")
    w = c.get("worker", {})
    if w.get("kind") == "omo":
        if not isinstance(w.get("ref"), str) or not w["ref"]:
            e.append("L8 omo worker needs a ref into the owner's tools registry")
        for k in ("binary", "pinned_version", "export_argv", "argv"):
            if k in w:
                e.append(f"L8 worker.{k} belongs in the owner's tools registry, not the controller")
        if not w.get("agent"):
            e.append("L8 omo worker needs an agent")
        if not isinstance(w.get("expect_agents"), list) or not w["expect_agents"]:
            e.append("L8 omo worker needs expect_agents")
        hooks = set(c.get("materialize", {}).get("disabled_hooks", []))
        if not REQUIRED_HOOKS <= hooks:
            e.append(f"L8 materialize.disabled_hooks must include {sorted(REQUIRED_HOOKS)}")
    elif not (allow_fake and w.get("kind") == "fake"):
        e.append("L8 worker kind must be omo")
    if w.get("isolation") not in ISOLATION:
        e.append(f"L8 worker.isolation must be one of {sorted(ISOLATION)}")
    for r in c.get("reviewers", []):
        if r.get("harness") in (None, "", "opencode-omo"):
            e.append("L9 reviewer needs a harness other than opencode-omo")
        if r.get("kind") == "command":
            if not isinstance(r.get("ref"), str) or not r["ref"]:
                e.append(f"L9 reviewer {r.get('harness')}: needs a ref into the owner's tools registry")
            if "argv" in r or "env" in r:
                e.append(f"L9 reviewer {r.get('harness')}: argv and env belong in the owner's tools registry, not the controller")
        elif not (allow_fake and r.get("kind") == "fake"):
            e.append(f"L9 reviewer {r.get('harness')}: kind must be command")
    res = c.get("reservations_usd", {})
    for k in ("worker_call", "review_call") + (("decision_call",) if _http(b) else ()):
        if not _num(res.get(k)) or res[k] <= 0:
            e.append(f"L10 reservations_usd.{k} must be above zero")
    for k, v in res.items():
        if not _num(v) or v < 0:
            e.append(f"L10 reservations_usd.{k} must be non-negative")
    return e


def _pins_cover(name, argv, pins, e, rule="L11"):
    names = {os.path.basename(p) for p in pins}
    paths = set(pins)
    if "/" in argv[0]:
        if argv[0] not in paths:
            e.append(f"{rule} {name}: the executable {argv[0]} must be pinned")
    elif argv[0] not in names:
        e.append(f"{rule} {name}: pins must cover the executable {argv[0]}")
    for a in argv[1:]:
        if "/" in a and "{" not in a:
            if not os.path.isabs(a):
                e.append(f"{rule} {name}: path {a} must be absolute")
            elif a not in paths:
                e.append(f"{rule} {name}: path {a} must be pinned")


def _pins_ok(name, pins, e):
    if not isinstance(pins, dict) or not pins or not all(isinstance(v, str) and HEX64.match(v) for v in pins.values()):
        e.append(f"L11 {name}: pins must map each pinned file to a SHA-256")
        return False
    return True


def validate_tools(reg):
    e = []
    if not isinstance(reg, dict):
        return ["L11 tools registry must be an object"]
    for name, r in (reg.get("reviewers") or {}).items():
        if not r.get("harness") or r.get("harness") == "opencode-omo":
            e.append(f"L11 {name}: needs a harness other than opencode-omo")
        argv = r.get("argv")
        if not isinstance(argv, list) or not argv or not all(isinstance(a, str) for a in argv):
            e.append(f"L11 {name}: argv must be a non-empty list of strings")
            continue
        if _pins_ok(name, r.get("pins"), e):
            _pins_cover(name, argv, r["pins"], e)
        if not any("{diff_file}" in a for a in argv):
            e.append(f"L11 {name}: argv must pass {{diff_file}}")
    for name, w in (reg.get("workers") or {}).items():
        argv, exp = w.get("argv"), w.get("export_argv")
        ok = True
        for k, v in (("argv", argv), ("export_argv", exp)):
            if not isinstance(v, list) or not v or not all(isinstance(a, str) for a in v):
                e.append(f"L11 {name}: {k} must be a non-empty list of strings")
                ok = False
        if not ok:
            continue
        if os.path.basename(argv[0]) in DOWNLOADERS:
            e.append(f"L11 {name}: a runtime package download is not a pinned install")
        if not any("{session_id}" in a for a in exp):
            e.append(f"L11 {name}: export_argv needs a {{session_id}} placeholder")
        if w.get("version") != "4.19.4":
            e.append(f"L11 {name}: omo must be pinned to 4.19.4")
        if _pins_ok(name, w.get("pins"), e):
            _pins_cover(name, argv, w["pins"], e)
            _pins_cover(name + " export", exp, w["pins"], e)
    q = reg.get("qualifications", {})
    if not isinstance(q, dict) or not all(isinstance(v, str) and HEX64.match(v) for v in q.values()):
        e.append("L11 qualifications must map record paths to SHA-256 values")
    return e


def _host(url):
    m = re.match(r"^[a-z]+://(\[[^\]]+\]|[^/:]+)", str(url))
    return m.group(1).strip("[]") if m else ""


def _http(b):
    if b.get("kind") == "http":
        return [b]
    if b.get("kind") == "dual":
        return _http(b.get("first", {})) + _http(b.get("second", {}))
    return []


def _backend(b):
    e = []
    k = b.get("kind")
    if k == "http":
        url = str(b.get("base_url", ""))
        if not (url.startswith("https://") or (url.startswith("http://") and _host(url) in LOOPBACK)):
            e.append("L5 http backend needs an https base_url (plain http only on a loopback host)")
        if not str(b.get("path", "")).startswith("/"):
            e.append("L5 http backend needs a path")
        if not b.get("model") or ALIAS.search(str(b.get("model"))) or not VERSIONED.search(str(b.get("model"))):
            e.append("L5 http backend needs a pinned, versioned model ID, not an alias")
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


def check_tools(path=TOOLS_EXAMPLE):
    return validate_tools(json.load(io.open(path, encoding="utf-8")))


def _labelled(n, source="human"):
    return [{"score": 0.99, "correct": True, "label_source": source}] * n


def _record(tmp, model, n=150, source="human", question="blocked"):
    ds = os.path.join(tmp, f"labels-{model}-{n}-{source}-{question}.json")
    json.dump(_labelled(n, source), open(ds, "w"))
    if source in _q.LABEL_SOURCES:
        rec = _q.make_record(ds, 0.05, 0.05, [0.99, 0.95], model, question, 1, "en")
    else:
        rec = _q.qualify(_labelled(n), 0.05, 0.05, [0.99, 0.95])
        rec.update(grid=[0.99, 0.95], dataset=ds, dataset_sha256=_q._sha(ds), model=model, question_id=question,
                   revision=1, locale="en")
    path = ds.replace("labels-", "record-")
    json.dump(rec, open(path, "w"))
    return path, ds


def self_test():
    fails = 0
    tmp = tempfile.mkdtemp()
    g0 = json.load(io.open(os.path.join(ROOT, EXAMPLES[0][0]), encoding="utf-8"))
    c0 = json.load(io.open(os.path.join(ROOT, EXAMPLES[0][1]), encoding="utf-8"))
    cat0 = json.load(io.open(QUESTIONS, encoding="utf-8"))
    reg0 = json.load(io.open(TOOLS_EXAMPLE, encoding="utf-8"))
    model = c0["decision"]["backend"]["model"]
    good_rec, good_ds = _record(tmp, model)

    def expect(label, mutate, rule):
        nonlocal fails
        g, c, cat, reg = copy.deepcopy(g0), copy.deepcopy(c0), copy.deepcopy(cat0), copy.deepcopy(reg0)
        mutate({"goal": g, "controller": c, "catalog": cat, "registry": reg})
        errs = validate_goal(g) + validate_controller(c, g, cat) + validate_tools(reg)
        hit = any(x.startswith(rule + " ") for x in errs)
        print(("  ok   " if hit else "  FAIL ") + f"{label} -> {rule}")
        fails += 0 if hit else 1

    def q(cat, i):
        return next(x for x in cat["questions"] if x["id"] == i)

    def advisory(m, record=None, **over):
        c = m["controller"]
        c["mode"] = "advisory"
        c["decision"]["lineage"]["base_family"] = "meta"
        ent = {"question_id": "blocked", "model": model, "locale": "en", "record": record or good_rec}
        ent.update(over)
        c["qualifications"] = [ent]

    def edit_record(field, value):
        path = os.path.join(tmp, f"edited-{field}.json")
        rec = json.load(open(good_rec))
        rec[field] = value
        json.dump(rec, open(path, "w"))
        return path

    def tampered_dataset():
        rec_path, ds = _record(tmp, model, n=151)
        json.dump(_labelled(150) + [{"score": 0.99, "correct": False, "label_source": "human"}], open(ds, "w"))
        return rec_path

    base = validate_goal(g0) + validate_controller(c0, g0, cat0)
    print(("  ok   " if not base else "  FAIL ") + "committed examples are valid " + str(base[:3]))
    fails += 1 if base else 0
    regb = validate_tools(reg0)
    print(("  ok   " if not regb else "  FAIL ") + "tools registry example is valid " + str(regb[:3]))
    fails += 1 if regb else 0
    adv = copy.deepcopy(c0)
    advisory({"controller": adv})
    ab = validate_controller(adv, g0, cat0)
    print(("  ok   " if not ab else "  FAIL ") + "a verified qualification record is accepted " + str(ab[:3]))
    fails += 1 if ab else 0
    expect("missing required question", lambda m: m["catalog"]["questions"].pop(), "L1")
    expect("threshold in the catalog", lambda m: q(m["catalog"], "blocked").__setitem__("threshold", 0.8), "L1")
    expect("authority over success", lambda m: q(m["catalog"], "goal_met").__setitem__("authority", "done"), "L1")
    expect("brake that succeeds", lambda m: q(m["catalog"], "blocked")["effect"].__setitem__("effect", "succeed"), "L1")
    expect("brake on a missing option", lambda m: q(m["catalog"], "progress")["effect"].__setitem__("on_options", ["nope"]), "L1")
    expect("one-option choice", lambda m: q(m["catalog"], "next_action").__setitem__("criteria", {"repair": "x"}), "L1")
    expect("shell string check", lambda m: m["goal"]["acceptance"][0].__setitem__("argv", "make test"), "L2")
    expect("bad situation", lambda m: m["goal"].__setitem__("situation", "A13"), "L2")
    expect("no acceptance", lambda m: m["goal"].__setitem__("acceptance", []), "L2")
    expect("no-op check", lambda m: m["goal"]["acceptance"][0].__setitem__("argv", ["true"]), "L2")
    expect("shell no-op check", lambda m: m["goal"]["acceptance"][0].__setitem__("argv", ["sh", "-c", "exit 0"]), "L2")
    expect("check reads the status file", lambda m: m["goal"]["acceptance"][0].__setitem__(
        "argv", ["grep", "done", ".superloop/status.json"]), "L2")
    expect("endless iterations", lambda m: m["controller"]["caps"].__setitem__("max_iterations", 10 ** 6), "L3")
    expect("no budget", lambda m: m["controller"]["caps"].pop("budget_usd"), "L3")
    expect("control mode", lambda m: m["controller"].__setitem__("mode", "control"), "L4")
    expect("alias model", lambda m: m["controller"]["decision"]["backend"].__setitem__("model", "jev-latest"), "L5")
    expect("stable alias model", lambda m: m["controller"]["decision"]["backend"].__setitem__("model", "stable-model"), "L5")
    expect("unversioned model", lambda m: m["controller"]["decision"]["backend"].__setitem__("model", "jev"), "L5")
    expect("literal key", lambda m: m["controller"]["decision"]["backend"].__setitem__("api_key_env", "sk-abc123"), "L5")
    expect("plain http to a remote host", lambda m: m["controller"]["decision"]["backend"].__setitem__("base_url", "http://x"), "L5")
    expect("advisory without lineage", lambda m: (advisory(m), m["controller"]["decision"]["lineage"].__setitem__("base_family", "undisclosed")), "L6")
    expect("advisory with a made-up family", lambda m: (advisory(m), m["controller"]["decision"]["lineage"].__setitem__("base_family", "made-up-family")), "L6")
    expect("advisory without qualification", lambda m: (advisory(m), m["controller"].__setitem__("qualifications", [])), "L6")
    expect("qualification without a record file", lambda m: advisory(m, record=os.path.join(tmp, "missing.json")), "L6")
    expect("qualification on too few labels", lambda m: advisory(m, record=_record(tmp, model, n=40)[0]), "L6")
    expect("qualification labelled by the model", lambda m: advisory(m, record=_record(tmp, model, source="model")[0]), "L6")
    expect("qualification with an edited threshold", lambda m: advisory(m, record=edit_record("threshold", 0.01)), "L6")
    expect("qualification on a changed dataset", lambda m: advisory(m, record=tampered_dataset()), "L6")
    expect("qualification for another model", lambda m: advisory(m, model="other-1.0"), "L6")
    expect("qualification for a shadow question", lambda m: advisory(m, question_id="next_action"), "L6")
    expect("ultimate with a remote endpoint", lambda m: m["goal"].__setitem__("profile", "ultimate"), "L7")
    expect("ultimate with a reachability flag set", lambda m: (m["goal"].__setitem__("profile", "ultimate"),
           m["controller"]["decision"]["egress"].__setitem__("hk_reachable_verified", True)), "L7")
    expect("worker binary in the controller", lambda m: m["controller"]["worker"].__setitem__("binary", "./x"), "L8")
    expect("export command in the controller", lambda m: m["controller"]["worker"].__setitem__("export_argv", ["x", "{session_id}"]), "L8")
    expect("no stated isolation", lambda m: m["controller"]["worker"].pop("isolation"), "L8")
    expect("omo continuation left on", lambda m: m["controller"]["materialize"]["disabled_hooks"].remove("todo-continuation-enforcer"), "L8")
    expect("atlas left on", lambda m: m["controller"]["materialize"]["disabled_hooks"].remove("atlas"), "L8")
    expect("runtime fallback left on", lambda m: m["controller"]["materialize"]["disabled_hooks"].remove("runtime-fallback"), "L8")
    expect("worker without a tools ref", lambda m: m["controller"]["worker"].pop("ref"), "L8")
    expect("no expected agents", lambda m: m["controller"]["worker"].pop("expect_agents"), "L8")
    expect("command worker", lambda m: m["controller"].__setitem__("worker", {"kind": "command", "argv": ["x"]}), "L8")
    expect("fake worker outside the self-test", lambda m: m["controller"].__setitem__("worker", {"kind": "fake", "name": "w"}), "L8")
    expect("reviewer on omo", lambda m: m["controller"]["reviewers"][0].__setitem__("harness", "opencode-omo"), "L9")
    expect("reviewer argv in the controller", lambda m: m["controller"]["reviewers"][0].__setitem__("argv", ["sh", "-c", "echo []"]), "L9")
    expect("reviewer without a registry ref", lambda m: m["controller"]["reviewers"][0].pop("ref"), "L9")
    expect("fake reviewer outside the self-test", lambda m: m["controller"]["reviewers"][0].__setitem__("kind", "fake"), "L9")
    expect("zero worker reservation", lambda m: m["controller"]["reservations_usd"].__setitem__("worker_call", 0), "L10")
    expect("missing review reservation", lambda m: m["controller"]["reservations_usd"].pop("review_call"), "L10")
    expect("zero decision reservation with a remote backend", lambda m: m["controller"]["reservations_usd"].__setitem__("decision_call", 0), "L10")
    first = next(iter(reg0["reviewers"]))
    wk = next(iter(reg0["workers"]))
    expect("reviewer entry without pins", lambda m: m["registry"]["reviewers"][first].pop("pins"), "L11")
    expect("reviewer pins miss the executable", lambda m: m["registry"]["reviewers"][first].__setitem__(
        "pins", {"/opt/other": "0" * 64}), "L11")
    expect("interpreter pinned, script not", lambda m: m["registry"]["reviewers"][first].update(
        argv=["python3", "/opt/review.py", "{diff_file}"], pins={"/usr/bin/python3": "0" * 64}), "L11")
    expect("relative script path", lambda m: m["registry"]["reviewers"][first].update(
        argv=["python3", "tools/review.py", "{diff_file}"], pins={"/usr/bin/python3": "0" * 64}), "L11")
    expect("reviewer argv without the diff", lambda m: m["registry"]["reviewers"][first].__setitem__("argv", ["goose", "run"]), "L11")
    expect("worker as a runtime package download", lambda m: m["registry"]["workers"][wk].__setitem__(
        "argv", ["bunx", "oh-my-openagent"]), "L11")
    expect("worker on another omo version", lambda m: m["registry"]["workers"][wk].__setitem__("version", "5.1.48"), "L11")
    expect("export without a session placeholder", lambda m: m["registry"]["workers"][wk].__setitem__(
        "export_argv", ["opencode", "export"]), "L11")
    expect("export program not pinned", lambda m: m["registry"]["workers"][wk].__setitem__(
        "export_argv", ["/opt/export", "{session_id}"]), "L11")
    expect("qualification pin that is not a hash", lambda m: m["registry"].__setitem__("qualifications", {"/x": "abc"}), "L11")
    print("self-test " + ("passed" if not fails else f"FAILED ({fails})"))
    return 1 if fails else 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    pairs = [tuple(argv[:2])] if len(argv) >= 2 else EXAMPLES
    errs = []
    for gp, cp in pairs:
        errs += [f"{cp}: {x}" for x in check_pair(gp, cp)]
    if len(argv) < 2:
        errs += [f"examples/superloop/tools.example.json: {x}" for x in check_tools()]
    for x in errs:
        print("  FAIL", x)
    print("superloop checks " + ("passed" if not errs else f"FAILED ({len(errs)})"))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
