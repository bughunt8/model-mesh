#!/usr/bin/env python3
"""Validate the cross-harness orchestration matrix.

The matrix is a design proposal. This script proves structure and policy only:
vocabulary, independence of review, region and cap rules, and that the readable
table is rendered from the data. It does not prove any harness can execute a row.

Usage:
  python scripts/validate-orchestration.py            validate files in the repo
  python scripts/validate-orchestration.py --render   rewrite docs/research/orchestration/MATRIX.md
  python scripts/validate-orchestration.py --self-test  mutate a valid matrix and expect each rule to fire

Rules:
  O1  schema: version, design-only status, 12 situations A01-A12 in order, 4 profiles each.
  O2  every situation/profile has a primary and an alternate with distinct harness sets.
  O3  vocabulary: omo agents, categories, harnesses, coordinators, patterns, statuses.
  O4  every chain rung exists in that profile's model table, no duplicate rung in a chain,
      no retiring or unknown-family model in a chain.
  O5  reviewer independence: reviewer harness differs from every author harness AND the
      orchestrator harness; families are derived from IDs, not editable labels; they share nothing with every
      rung of every author seat and category route. The orchestrator family shares nothing
      with authors or reviewers. No exception is authorized in this package.
  O6  ultimate is Hong Kong-native: every rung is HK-eligible; the Codex harness appears
      only in an alternate marked conditional on a custom provider.
  O7  hybrid and b4b obey conservative price references and exact coding-tier slots.
  O8  hephaestus is only assigned to a chain whose first model is flagship-native (OpenAI family).
  O9  only 'none' and 'orca' coordinators may be used in a cell; the rest are reference only.
  O10 model table agrees with the profile example files, and profiles/global*.json exist.
  O11 no key or value claims verified, measured or qualified results.
  O12 A06 options require author provenance; A11 options require the official Playwright MCP.
  O13 the seven harness example files exist, parse, and are marked docs-checked, runtime-deferred.
  O14 MATRIX.md equals the table rendered from the data.
"""
import copy, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIX = os.path.join(ROOT, "examples", "orchestration", "matrix.example.json")
TABLE = os.path.join(ROOT, "docs", "research", "orchestration", "MATRIX.md")
HARNESS_DIR = os.path.join(ROOT, "examples", "orchestration", "harnesses")

SITUATIONS = [f"A{n:02d}" for n in range(1, 13)]
PROFILES = ["ultimate", "hybrid", "b4b", "global"]
AGENTS = {"hephaestus", "oracle", "prometheus", "metis", "momus", "atlas", "sisyphus-junior",
          "sisyphus", "librarian", "explore", "multimodal-looker"}
CATEGORIES = {"visual-engineering", "ultrabrain", "deep", "artistry", "quick",
              "unspecified-low", "unspecified-high", "writing"}
HARNESSES = ["opencode-omo", "dsh", "codex", "pi", "qwen-code", "aider", "goose"]
COORDINATORS = {"none", "orca", "emdash", "nimbalyst", "vibe-kanban", "superset", "conductor", "aq", "warp"}
CELL_COORDINATORS = {"none", "orca"}
PATTERNS = {"P1+P4", "P2+P4", "P3+P4", "P5+P4"}
STATUSES = {"proposed-adapter-qualification-deferred", "conditional-custom-provider-features-deferred"}
HK_FAMILIES = {"deepseek", "moonshot", "zai", "alibaba", "minimax", "xiaomi"}
HK_BLOCKED = {"openai", "anthropic", "google", "xai"}
# Mirrors .github/checks.py OVER_CAP / METERED_EXEMPT. checks.py asserts the same sets.
OVER_CAP = {"flagship-open", "div-flagship", "reasoner-xl", "coder-xl"}
METERED_EXEMPT = {"coder-xl"}
CLAIMS = re.compile(r"\b(verified|measured|qualified|passes|proven|certified)\b", re.I)
CLAIM_OK = re.compile(r"(not|un|dis)[ -]?(verified|measured|qualified)|not a measured|no measured|runtime-deferred", re.I)
EXPECTED_HARNESS_FILES = {
    "opencode-omo": "opencode-omo.example.json", "dsh": "dsh.example.json", "codex": "codex.example.json",
    "pi": "pi.example.json", "qwen-code": "qwen-code.example.json", "aider": "aider.example.json",
    "goose": "goose.example.json",
}
ENVELOPE_KEYS = {"harness", "status", "native_path", "native_format", "native_config", "invocation",
                 "sources", "limitations", "role_binding", "profiles"}


def seats(option):
    out = list(option.get("authors", [])) + list(option.get("reviewers", []))
    if option.get("orchestrator"):
        out.append(option["orchestrator"])
    return out


def families(matrix, profile, chain):
    table = matrix["models"][profile]
    return {model_family(table[m]["id"]) for m in chain if m in table}


# Model identity comes from the model name, never from editable labels in the matrix.
# Different hosts for one model do not create different families.
PREFIX_FAMILY = {"gpt-": "openai", "claude-": "anthropic", "gemini-": "google",
                 "grok-": "xai", "deepseek-": "deepseek", "kimi-": "moonshot",
                 "glm-": "zai", "qwen": "alibaba", "minimax-": "minimax",
                 "mimo-": "xiaomi", "muse-": "meta"}
NATIVE_ROUTES = {"openai": "openai", "anthropic": "anthropic", "google": "google", "xai": "xai",
                 "deepseek": "deepseek", "moonshotai": "moonshot", "zai-coding-plan": "zai", "minimax": "minimax"}
# Conservative list-price reference, USD / 1M output. Never a proof of billed cost.
# Sources and transport caveats: docs/research/orchestration/PRICE-REFERENCE.md.
# Values for native routes use conservative references where hosts differ.
OUTPUT_REFERENCE = {"gpt-5.6-terra": 18, "gpt-5.6-luna": 1.8, "gpt-6.1-sol": 15,
                    "gpt-6-astra": 75, "gpt-6-luna": .75, "claude-sonnet-5-5": 10,
                    "grok-4.7": 12, "deepseek-v4-pro": 3.96, "deepseek-v4-flash": .60,
                    "kimi-k3": 15, "kimi-k2.7-code": 4, "qwen3.8-max": 6,
                    "qwen3.7-plus": 1.6, "qwen3.5-plus": 1.2, "glm-5.3": 4.4,
                    "glm-5.3-flash": .5, "minimax-m3": 1.2}


def model_family(mid):
    if not isinstance(mid, str) or mid.count("/") != 1:
        return "unknown"
    name = mid.split("/", 1)[1].lower()
    return next((fam for prefix, fam in PREFIX_FAMILY.items() if name.startswith(prefix)), "unknown")


def cap_exempt(profile, role, index, category=False):
    # Exact slot policy from docs/EXAMPLE-MAPPING.md. No family-wide free pass.
    if category:
        return role == "deep" and index == 1 or profile == "hybrid" and role == "ultrabrain" and index == 2
    return profile == "hybrid" and role in ("atlas", "prometheus") and index == 0


def check_native_keys(d):
    native = parse_native(d)
    if not isinstance(native, dict):
        raise ValueError("native config must be an object")
    allowed = {
        "opencode-omo": {"$schema", "plugin", "permission"},
        "dsh": {"dsh_home", "cwd", "provider", "model", "reasoning_effort", "max_tokens"},
        "codex": {"model", "model_provider", "model_context_window", "model_providers"},
        "pi": {"models_json", "settings_json"},
        "qwen-code": {"modelProviders", "mcpServers"},
        "aider": {"model", "architect", "editor-model", "auto-commits", "auto-test", "test-cmd", "map-tokens", "read"},
        "goose": {"version", "title", "description", "instructions", "prompt", "extensions", "settings", "parameters", "sub_recipes", "response", "retry"},
    }[d["harness"]]
    if set(native) != allowed:
        raise ValueError("native keys differ from this documented fixture: " + str(set(native) ^ allowed))
    return native


def validate(matrix, root=ROOT, check_files=True):
    errs, notes = [], []

    def e(rule, msg):
        errs.append(f"{rule}: {msg}")

    # Reject malformed collections before deeper traversal, not by traceback.
    if not isinstance(matrix, dict) or not isinstance(matrix.get("situations"), list) or not isinstance(matrix.get("models"), dict):
        return ["O1: invalid matrix root or collections"], []
    for situation in matrix["situations"]:
        if not isinstance(situation, dict) or not isinstance(situation.get("profiles"), dict):
            return ["O1: invalid situation object"], []
        for profile, block in situation["profiles"].items():
            if not isinstance(block, dict) or not isinstance(block.get("options"), list):
                return ["O1: invalid options collection"], []
            for option in block["options"]:
                if not isinstance(option, dict) or not isinstance(option.get("authors"), list) or not option["authors"] or not isinstance(option.get("reviewers"), list):
                    return ["O1: invalid option seats"], []
                if not option["reviewers"]:
                    e("O5", "at least one reviewer is required")
                for st in seats(option):
                    if not isinstance(st, dict) or not {"role", "harness", "chain", "kind"} <= set(st):
                        return ["O1: malformed seat"], []
                    if not isinstance(st["chain"], list) or not st["chain"] or not all(isinstance(x, str) for x in st["chain"]):
                        return ["O4: every seat needs a non-empty string chain"], []
                if not isinstance(option.get("category_routes"), dict) or not all(isinstance(ch,list) and ch and all(isinstance(x,str) for x in ch) for ch in option["category_routes"].values()):
                    return ["O4: non-empty category routes required"], []
    # O1
    if matrix.get("version") != 1:
        e("O1", "version must be 1")
    if matrix.get("status") != "design-only-runtime-deferred":
        e("O1", "status must be design-only-runtime-deferred")
    if matrix.get("profiles") != PROFILES:
        e("O1", f"profiles must be {PROFILES}")
    sits = matrix.get("situations", [])
    if [s.get("id") for s in sits] != SITUATIONS:
        e("O1", "situations must be A01..A12 in order")
    if set(matrix.get("agents", [])) != AGENTS:
        e("O3", "agents list must equal the 11 omo agent names")
    if set(matrix.get("categories", [])) != CATEGORIES:
        e("O3", "categories list must equal the 8 omo category names")
    if matrix.get("harnesses") != HARNESSES:
        e("O3", f"harnesses must be {HARNESSES}")
    if set(matrix.get("coordinators", {})) != COORDINATORS:
        e("O3", "coordinator table must list exactly the eight assessed coordinators plus none")
    models = matrix.get("models", {})
    for p in PROFILES:
        if p not in models:
            e("O1", f"models table missing profile {p}")
    # O4 model table hygiene
    for p, table in models.items():
        for ph, info in table.items():
            if not {"id", "family", "hk_policy_eligible", "status"} <= set(info):
                e("O4", f"{p}:{ph} model entry incomplete")
            actual = model_family(info.get("id"))
            if actual != "unknown" and info.get("family") != actual:
                e("O4", f"{p}:{ph} family label disagrees with model identity")
            vendor = info.get("id", "").split("/", 1)[0]
            if vendor in NATIVE_ROUTES and NATIVE_ROUTES[vendor] != actual:
                e("O4", f"{p}:{ph} first-party route belongs to a different family")
    for s in sits:
        sid = s.get("id")
        for c in s.get("categories", []):
            if c not in CATEGORIES:
                e("O3", f"{sid}: unknown category {c}")
        for a in s.get("agent_sequence", []):
            if a not in AGENTS:
                e("O3", f"{sid}: unknown agent {a}")
        for p in PROFILES:
            block = s.get("profiles", {}).get(p)
            if not block:
                e("O1", f"{sid}: missing profile {p}")
                continue
            opts = block.get("options", [])
            names = [o.get("name") for o in opts]
            if len(opts) < 2 or names[:2] != ["primary", "alternate"] or len(set(names)) != len(names):
                e("O2", f"{sid}/{p}: need unique options starting primary, alternate")
                continue
            sets = [tuple(sorted({a["harness"] for a in o["authors"]})) for o in opts]
            if len(set(sets)) != len(sets):
                e("O2", f"{sid}/{p}: every option must have a distinct author harness set")
            for o in opts:
                where = f"{sid}/{p}/{o.get('name')}"
                if "absolute_exception" in o:
                    e("O5", f"{where}: no owner-approved independence exception exists in this package")
                sequence = [a["role"] for a in o["authors"]] + [r["role"] for r in o["reviewers"]]
                if o.get("agent_sequence") != sequence:
                    e("O3", f"{where}: option agent_sequence must match its actual seats")
                if o.get("orchestrator") and o["orchestrator"]["harness"] == "aider":
                    e("O3", f"{where}: Aider is not an orchestrator")
                if o["name"] != "primary" and o.get("orchestrator") and o["orchestrator"]["harness"] == "opencode-omo":
                    e("O9", f"{where}: the open-source-only alternate must replace omo orchestration")
                if any(st["harness"] == "pi" for st in seats(o)) and "pi-external-container" not in o.get("constraints", []):
                    e("O3", f"{where}: every Pi seat requires external container isolation")
                if o.get("pattern") not in PATTERNS:
                    e("O3", f"{where}: pattern {o.get('pattern')}")
                if o.get("coordinator") not in COORDINATORS:
                    e("O3", f"{where}: unknown coordinator {o.get('coordinator')}")
                elif o["coordinator"] not in CELL_COORDINATORS:
                    e("O9", f"{where}: coordinator {o['coordinator']} is reference-only")
                if o.get("coordinator") == "orca" and o.get("pattern") != "P5+P4":
                    e("O9", f"{where}: orca requires pattern P5+P4")
                if o.get("status") not in STATUSES:
                    e("O3", f"{where}: status {o.get('status')}")
                if o.get("external_adapters") != "proposed-not-implemented":
                    e("O11", f"{where}: external_adapters must stay proposed-not-implemented")
                for st in seats(o):
                    if st["role"] not in AGENTS:
                        e("O3", f"{where}: unknown role {st['role']}")
                    if st["harness"] not in HARNESSES:
                        e("O3", f"{where}: unknown harness {st['harness']}")
                chains = [st["chain"] for st in seats(o)] + list(o.get("category_routes", {}).values())
                for ch in chains:
                    if len(set(ch)) != len(ch):
                        e("O4", f"{where}: duplicate rung in {ch}")
                    for m in ch:
                        info = models[p].get(m)
                        if not info:
                            e("O4", f"{where}: {m} missing from {p} model table")
                        elif info["status"].startswith("retires") or model_family(info["id"]) in ("unknown", "google") \
                                or info["status"].startswith("unknown"):
                            e("O4", f"{where}: {m} is {info['status']}/{info['family']}")
                for c in s["categories"]:
                    if c not in o.get("category_routes", {}):
                        e("O3", f"{where}: category route missing for {c}")
                # O5 independence, over every rung
                authors = o["authors"]
                a_h = {a["harness"] for a in authors}
                a_f = set()
                for ch in [a["chain"] for a in authors] + list(o.get("category_routes", {}).values()):
                    a_f |= families(matrix, p, ch)
                orch = o.get("orchestrator")
                if orch and families(matrix, p, orch["chain"]) & a_f:
                    e("O5", f"{where}: orchestrator family overlaps authors")
                author_ids = {models[p][mid]["id"].lower() for a in authors for mid in a["chain"] if mid in models[p]}
                for r in o["reviewers"]:
                    if r.get("execution") != "original-external-role-contract" or r["harness"] == "opencode-omo":
                        e("O5", f"{where}: review must be an original external role contract, not native omo")
                    if r["harness"] in a_h:
                        e("O5", f"{where}: reviewer harness is also an author harness")
                    shared = families(matrix, p, r["chain"]) & a_f
                    if shared:
                        e("O5", f"{where}: reviewer family {sorted(shared)} overlaps authors")
                    if author_ids & {models[p][mid]["id"].lower() for mid in r["chain"] if mid in models[p]}:
                        e("O5", f"{where}: reviewer repeats an author model ID")
                    if orch:
                        if r["harness"] == orch["harness"]:
                            e("O5", f"{where}: reviewer harness equals orchestrator harness")
                        if families(matrix, p, orch["chain"]) & families(matrix, p, r["chain"]):
                            e("O5", f"{where}: orchestrator family overlaps reviewers")
                # O6 HK
                all_f = set()
                for ch in chains:
                    all_f |= families(matrix, p, ch)
                if p == "ultimate":
                    bad = all_f - HK_FAMILIES
                    if bad:
                        e("O6", f"{where}: non-HK families {sorted(bad)}")
                    for ch in chains:
                        for m in ch:
                            if m in models[p]:
                                inf = models[p][m]
                                vendor = inf["id"].split("/", 1)[0]
                                if not inf["hk_policy_eligible"] or vendor not in {"opencode", "deepseek", "moonshotai", "zai-coding-plan", "minimax"}:
                                    e("O6", f"{where}: {m} not an eligible native/gateway HK route; proxies prohibited")
                    if any(st["harness"] == "codex" for st in seats(o)):
                        if o["name"] == "primary" or o["status"] != "conditional-custom-provider-features-deferred":
                            e("O6", f"{where}: codex in ultimate must be a conditional alternate")
                # O7 cap uses model identity and conservative price references.
                if p in ("hybrid", "b4b"):
                    entries = [(st["role"], i, mid, False) for st in seats(o) for i,mid in enumerate(st["chain"])]
                    entries += [(c,i,mid,True) for c,ch in o["category_routes"].items() for i,mid in enumerate(ch)]
                    for role,i,mid,iscat in entries:
                        if mid not in models[p]:
                            continue
                        name = models[p][mid]["id"].split("/",1)[1].lower()
                        price = OUTPUT_REFERENCE.get(name)
                        allowed = name == "kimi-k3" and cap_exempt(p,role,i,iscat)
                        if price is None or price > 4.65 and not allowed:
                            e("O7", f"{where}: {mid} at {role}[{i}] has no cap-safe reference or exact slot exception")
                # O8 applies to the entire chain, including fallbacks.
                for st in seats(o):
                    if st["role"] == "hephaestus" and families(matrix,p,st["chain"]) != {"openai"}:
                        e("O8", f"{where}: hephaestus needs a wholly OpenAI-family chain; use atlas otherwise")
                # O12
                caps = set(o.get("required_capabilities", [])) | set(o.get("constraints", []))
                if sid == "A06" and "author-provenance-required" not in caps:
                    e("O12", f"{where}: A06 needs author-provenance-required")
                if sid == "A11" and "official-playwright-mcp" not in caps:
                    e("O12", f"{where}: A11 needs official-playwright-mcp")
    # O11 claims
    def walk(x, path=""):
        if isinstance(x, dict):
            for k, v in x.items():
                if CLAIMS.search(str(k)) and not CLAIM_OK.search(str(k)):
                    e("O11", f"claim-like key {path}/{k}")
                walk(v, f"{path}/{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                walk(v, f"{path}[{i}]")
        elif isinstance(x, str) and CLAIMS.search(x) and not CLAIM_OK.search(x):
            e("O11", f"claim-like text at {path}")
    walk(matrix)
    if check_files:
        errs += file_checks(matrix, root)
    return errs, notes


def read_jsonc(path):
    text = "\n".join(l for l in io.open(path, encoding="utf-8").read().splitlines() if not l.lstrip().startswith("//"))
    return json.loads(text)


def file_checks(matrix, root):
    errs = []
    for p in PROFILES:
        for suffix in ("", ".example"):
            if not os.path.exists(os.path.join(root, "profiles", f"{p}{suffix}.json")):
                errs.append(f"O10: missing profiles/{p}{suffix}.json")
    # O10 placeholder-to-ID agreement with the example profile files
    for p in PROFILES:
        gp, ep = (os.path.join(root, "profiles", f"{p}.json"), os.path.join(root, "profiles", f"{p}.example.json"))
        if not (os.path.exists(gp) and os.path.exists(ep)):
            continue
        pairs = {}

        def walk(x, y):
            if isinstance(x, dict):
                for k, v in x.items():
                    if k == "model" and isinstance(y, dict) and k in y:
                        pairs[v] = y[k]
                    elif isinstance(y, dict) and k in y:
                        walk(v, y[k])
            elif isinstance(x, list) and isinstance(y, list):
                for a, b in zip(x, y):
                    walk(a, b)
        walk(read_jsonc(gp), read_jsonc(ep))
        for ph, info in matrix["models"].get(p, {}).items():
            if ph in pairs and pairs[ph] != info["id"]:
                errs.append(f"O10: {p}:{ph} maps to {info['id']} in matrix but {pairs[ph]} in profile example")
    # O13 harness examples
    for h, fn in EXPECTED_HARNESS_FILES.items():
        path = os.path.join(root, "examples", "orchestration", "harnesses", fn)
        if not os.path.exists(path):
            errs.append(f"O13: missing examples/orchestration/harnesses/{fn}")
            continue
        try:
            d = json.load(io.open(path, encoding="utf-8"))
        except Exception as exc:
            errs.append(f"O13: {fn} invalid JSON: {exc}")
            continue
        if set(d) != ENVELOPE_KEYS:
            errs.append(f"O13: {fn} keys {sorted(set(d) ^ ENVELOPE_KEYS)} differ from the envelope")
            continue
        if d["harness"] != h or d["status"] != "docs-checked-runtime-deferred":
            errs.append(f"O13: {fn} harness/status marker wrong")
        if not d["sources"] or not all(str(u).startswith("https://") for u in d["sources"]):
            errs.append(f"O13: {fn} needs https sources")
        if not d["limitations"]:
            errs.append(f"O13: {fn} needs limitations")
        try:
            check_native_keys(d)
        except Exception as exc:
            errs.append(f"O13: {fn} native_config does not parse as {d['native_format']}: {exc}")
        if re.search(r"(sk-[A-Za-z0-9]{12,}|api[_-]?key\"?\s*[:=]\s*\"[A-Za-z0-9]{16,})", d["native_config"]):
            errs.append(f"O13: {fn} looks like it embeds a secret")
    # O14
    if os.path.exists(TABLE) and os.path.abspath(root) == ROOT:
        if io.open(TABLE, encoding="utf-8").read() != render(matrix):
            errs.append("O14: docs/research/orchestration/MATRIX.md differs from the rendered matrix (run --render)")
    elif os.path.abspath(root) == ROOT:
        errs.append("O14: docs/research/orchestration/MATRIX.md missing")
    return errs


def parse_native(d):
    fmt, text = d["native_format"], d["native_config"]
    if fmt == "json":
        return json.loads(text)
    if fmt == "toml":
        import tomllib
        return tomllib.loads(text)
    if fmt == "yaml":
        try:
            import yaml
        except ImportError as exc:
            raise ValueError("PyYAML required for YAML parsing") from exc
        return yaml.safe_load(text)
    raise ValueError(f"unknown format {fmt}")


def short(m):
    return m.split("/", 1)[-1]


def seat_text(matrix, p, st):
    return f"{st['harness']} {st['role']}: " + " > ".join(short(matrix["models"][p][m]["id"]) for m in st["chain"])


def render(matrix):
    out = ["# Situation to harness and model matrix", "",
           "This file is generated from [matrix.example.json](../../../examples/orchestration/matrix.example.json) by "
           "`python scripts/validate-orchestration.py --render`. Do not edit it by hand; CI fails if it drifts.", "",
           "Reading the tables. Each option is one complete assignment, so do not mix seats between options. "
           "An arrow marks an ordered fallback for one seat, not parallel work. Every harness in an `Authors` cell "
           "also supplies the helper roles listed after `same chain for`. The reviewer is always a different harness "
           "and a different model family from every author rung. All rows are proposals. No row has been run.", ""]
    for p in PROFILES:
        out += [f"## {p}", "", "| Situation / option | Pattern / coordinator | Orchestrator | Authors | Adversarial reviewer |",
                "|---|---|---|---|---|"]
        for s in matrix["situations"]:
            for o in s["profiles"][p]["options"]:
                au = o["authors"]
                main = seat_text(matrix, p, au[0])
                same = [a["role"] for a in au[1:] if a["chain"] == au[0]["chain"]]
                other = [seat_text(matrix, p, a) for a in au[1:] if a["chain"] != au[0]["chain"]]
                cell = main + ("; same chain for " + ", ".join(same) if same else "") + ("; " + "; ".join(other) if other else "")
                orch = seat_text(matrix, p, o["orchestrator"]) if o.get("orchestrator") else "peers, no AI orchestrator"
                rev = "; ".join(seat_text(matrix, p, r) for r in o["reviewers"])
                out.append(f"| {s['id']} {o['name']} | {o['pattern']} / {o['coordinator']} | {orch} | {cell} | {rev} |")
        out += ["", "Category routes and row rationale:", ""]
        for s in matrix["situations"]:
            o = s["profiles"][p]["options"][0]
            routes = "; ".join(f"{c}: " + " > ".join(short(matrix['models'][p][m]['id']) for m in ch)
                               for c, ch in o["category_routes"].items())
            out.append(f"- {s['id']} {s['title']}. Priority: {s['priority']}. Routes: {routes}. {s['profiles'][p]['rationale']}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def self_test(matrix):
    base_errs, _ = validate(matrix, check_files=False)
    if base_errs:
        print("base matrix invalid:", base_errs[:5]); return 1
    failures = 0

    def expect(label, mutate, rule):
        nonlocal failures
        m = copy.deepcopy(matrix)
        mutate(m)
        errs, _ = validate(m, check_files=False)
        if any(x.startswith(rule + ":") for x in errs):
            print(f"  ok   {label} -> {rule}")
        else:
            failures += 1
            print(f"  FAIL {label}: {rule} did not fire")

    def opt(m, sid="A01", p="ultimate", n=0):
        s = next(x for x in m["situations"] if x["id"] == sid)
        return s["profiles"][p]["options"][n]

    expect("reviewer on author harness", lambda m: opt(m)["reviewers"][0].__setitem__("harness", opt(m)["authors"][0]["harness"]), "O5")
    expect("reviewer shares author family", lambda m: opt(m)["reviewers"][0].__setitem__("chain", list(opt(m)["authors"][0]["chain"])), "O5")
    expect("reviewer family only in a late author rung", lambda m: opt(m)["authors"][0]["chain"].append(opt(m)["reviewers"][0]["chain"][0]), "O5")
    expect("category route carries reviewer family", lambda m: opt(m)["category_routes"].__setitem__("deep", list(opt(m)["reviewers"][0]["chain"])), "O5")
    expect("orchestrator family in reviewer", lambda m: opt(m)["reviewers"][0].__setitem__("chain", list(opt(m)["orchestrator"]["chain"])), "O5")
    expect("reviewer on orchestrator harness", lambda m: opt(m)["reviewers"][0].__setitem__("harness", "opencode-omo")
           if opt(m)["authors"][0]["harness"] != "opencode-omo" else opt(m, "A04")["reviewers"][0].__setitem__("harness", "opencode-omo"), "O5")
    expect("non-HK rung in ultimate", lambda m: opt(m)["authors"][0]["chain"].append("ProviderG/div-flagship") or m["models"]["ultimate"].__setitem__("ProviderG/div-flagship", {"id": "xai/grok-4.7", "family": "xai", "hk_policy_eligible": False, "status": "x"}), "O6")
    expect("codex primary in ultimate", lambda m: [a.__setitem__("harness", "codex") for a in opt(m)["authors"]], "O6")
    expect("over-cap rung in b4b", lambda m: opt(m, "A01", "b4b")["authors"][0]["chain"].append("ProviderB/flagship-open") or m["models"]["b4b"].__setitem__("ProviderB/flagship-open", {"id": "opencode/qwen3.8-max", "family": "alibaba", "hk_policy_eligible": True, "status": "x"}), "O7")
    expect("hephaestus on non-OpenAI chain", lambda m: opt(m, "A01", "ultimate")["authors"][0].__setitem__("role", "hephaestus"), "O8")
    expect("reference-only coordinator in a cell", lambda m: opt(m)["__setitem__"]("coordinator", "superset") if False else opt(m).update({"coordinator": "superset"}), "O9")
    expect("orca without P5", lambda m: opt(m).update({"coordinator": "orca"}), "O9")
    expect("unknown agent", lambda m: opt(m)["authors"][0].__setitem__("role", "gandalf"), "O3")
    expect("unknown harness", lambda m: opt(m)["authors"][0].__setitem__("harness", "mystery"), "O3")
    expect("missing alternate", lambda m: next(x for x in m["situations"] if x["id"] == "A02")["profiles"]["global"]["options"].pop(1), "O2")
    expect("alternate repeats harness", lambda m: [a.__setitem__("harness", opt(m)["authors"][0]["harness"]) for a in opt(m, "A01", "global", 1)["authors"]], "O2")
    expect("retiring model in chain", lambda m: opt(m)["authors"][0]["chain"].append("ProviderB/open-coder"), "O4")
    expect("duplicate rung", lambda m: opt(m)["authors"][0]["chain"].append(opt(m)["authors"][0]["chain"][0]), "O4")
    expect("claim of verified result", lambda m: m["situations"][0]["profiles"]["global"].__setitem__("rationale", "This route is verified in production."), "O11")
    expect("adapter marked implemented", lambda m: opt(m).__setitem__("external_adapters", "implemented"), "O11")
    expect("A06 loses provenance requirement", lambda m: next(x for x in m["situations"] if x["id"] == "A06")["profiles"]["ultimate"]["options"][0]["constraints"].remove("author-provenance-required") if "author-provenance-required" in next(x for x in m["situations"] if x["id"] == "A06")["profiles"]["ultimate"]["options"][0]["constraints"] else next(x for x in m["situations"] if x["id"] == "A06")["profiles"]["ultimate"]["options"][0]["required_capabilities"].clear(), "O12")
    expect("situation missing", lambda m: m["situations"].pop(5), "O1")
    expect("exception needs reason", lambda m: (opt(m).update({"absolute_exception": {"reason": ""}}), opt(m)["reviewers"][0].__setitem__("harness", opt(m)["authors"][0]["harness"])), "O5")
    expect("a reason cannot authorize an exception", lambda m: opt(m,"A04").update({"absolute_exception":{"reason":"x"}}), "O5")
    expect("empty reviewer list", lambda m: opt(m).__setitem__("reviewers",[]), "O5")
    expect("empty reviewer chain", lambda m: opt(m)["reviewers"][0].__setitem__("chain",[]), "O4")
    expect("spoofed family label", lambda m: m["models"]["ultimate"]["ProviderC/open-reason-xl"].__setitem__("family","alibaba"), "O4")
    expect("same family on another host", lambda m: m["models"]["ultimate"]["ProviderB/flagship-open"].update({"id":"opencode/deepseek-v4-flash","family":"deepseek"}), "O5")
    expect("HK proxy hidden by label", lambda m: m["models"]["ultimate"]["ProviderC/open-reason-xl"].update({"id":"apiyi/gpt-5.6-terra","family":"deepseek","hk_policy_eligible":True}), "O6")
    expect("over-cap model under cheap placeholder", lambda m: m["models"]["b4b"]["ProviderB/gen-pro"].update({"id":"opencode/qwen3.8-max","family":"alibaba"}), "O7")
    expect("coder exemption cannot leak to a helper", lambda m: opt(m,"A01","hybrid")["authors"][1]["chain"].append("ProviderE/coder-xl"), "O7")
    expect("Pi requires isolation", lambda m: opt(m,"A05")["constraints"].remove("pi-external-container"), "O3")
    expect("Aider cannot orchestrate", lambda m: opt(m)["orchestrator"].__setitem__("harness","aider"), "O3")
    expect("third option clone", lambda m: [a.__setitem__("harness",opt(m)["authors"][0]["harness"]) for a in opt(m,"A01","ultimate",2)["authors"]], "O2")
    expect("claim hidden in constraints", lambda m: opt(m)["constraints"].append("verified"), "O11")
    expect("empty author list", lambda m: opt(m).__setitem__("authors",[]), "O1")
    expect("retired family with benign label", lambda m: m["models"]["global"]["ProviderA/flagship-mid"].update({"id":"google/gemini-3.8-flash","family":"openai"}), "O4")
    print("self-test " + ("passed" if not failures else f"FAILED ({failures})"))
    return 1 if failures else 0


def main(argv):
    matrix = json.load(io.open(MATRIX, encoding="utf-8"))
    if "--render" in argv:
        io.open(TABLE, "w", encoding="utf-8").write(render(matrix))
        print("wrote", os.path.relpath(TABLE, ROOT))
        return 0
    if "--self-test" in argv:
        return self_test(matrix)
    errs, notes = validate(matrix)
    for n in notes:
        print("  note", n)
    for x in errs:
        print("  FAIL", x)
    if errs:
        print(f"{len(errs)} orchestration check(s) FAILED")
        return 1
    print("all orchestration checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
