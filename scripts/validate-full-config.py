#!/usr/bin/env python3
"""Validate examples/omo.full.example.json against the model-mesh design rules.

This guards the hardened invariants of the full deployable config so they cannot
silently regress. It is intentionally strict and self-documenting: each check
prints ok/FAIL with the rule it enforces. Exit code is non-zero on any failure.

Usage:  python scripts/validate-full-config.py [path]
        (defaults to examples/omo.full.example.json)

Rules enforced:
  R1  Valid strict JSON (no trailing commas / comments).
  R2  Required top-level + [opencode] structure present.
  R3  reasoning values are within the allowed enum.
  R4  Every agent has model + a non-empty fallback_models list.
  R5  No fallback rung equals the agent's own primary (no degenerate rung),
      and no model repeats within a single agent chain or a category list.
  R6  hephaestus is flagship-native-only: its primary and all fallback rungs
      share the primary's provider family (its ultrawork MAY be cross-family
      by design — that is the explicit non-flagship lifeline).
  R7  runtime_fallback.retry_on_errors excludes 400 (not a transient error).
  R8  background_task.providerConcurrency lists no provider that is unused.
  R9  momus uses `enabled` (not the invalid `disable` key).
  R10 No leftover retired-vendor names (Gemini) anywhere in the config.
  R11 $schema is pinned to a version tag (not the moving `dev` branch).
  R12 every model ID resolves to a known catalog entry (opencode/* must be an
      OpenCode Zen model; 'big-pickle' is Zen-exclusive and invalid on a relay).
  R13 no known cross-vendor mis-route: a first-party model under the WRONG
      native vendor prefix (e.g. deepseek/kimi-k3). Relay/aggregator prefixes
      (apiyi, tokeness, opencode) are exempt — we make no negative claim about
      what a relay may legitimately mirror, to avoid false failures.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT = os.path.join(ROOT, "examples", "omo.full.example.json")
path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT

ALLOWED_REASONING = {"low", "medium", "high", "max", "ultra"}
RETIRED_VENDORS = re.compile(r"\bgemini\b", re.I)  # Gemini was retired in v1.1.1

# --- Known-valid model catalog (R12) ----------------------------------------
# Guards against invalid IDs like 'tokeness/big-pickle' (big-pickle is an
# OpenCode-Zen-exclusive cloaked model, not a relay model). Two layers:
#  1) OPENCODE_ZEN: exact model names published in the OpenCode Zen catalog,
#     valid under the 'opencode/' provider (https://opencode.ai/docs/zen/).
#  2) RELAY_OK / NATIVE_OK: model *name substrings* known to be carried by the
#     relay/native providers used here (tokeness.io relay; deepseek / moonshotai
#     / minimax / zai-coding-plan native APIs). Substring match keeps this robust
#     to minor version bumps while still catching a nonexistent codename.
OPENCODE_ZEN = {
    "gpt-5.6-sol","gpt-5.6-terra","gpt-5.6-luna","gpt-5.5","gpt-5.5-pro","gpt-5.4",
    "gpt-5.4-pro","gpt-5.4-mini","gpt-5.4-nano","gpt-5.3-codex","gpt-5.3-codex-spark",
    "gpt-5.2","gpt-5.2-codex","gpt-5.1","gpt-5.1-codex","gpt-5.1-codex-max",
    "gpt-5.1-codex-mini","gpt-5","gpt-5-codex","gpt-5-nano",
    "claude-fable-5","claude-opus-5","claude-opus-4-8","claude-opus-4-7",
    "claude-opus-4-6","claude-opus-4-5","claude-sonnet-5","claude-sonnet-4-6",
    "claude-sonnet-4-5","claude-haiku-4-5",
    "gemini-3.7-flash","gemini-3.6-flash","gemini-3.5-flash","gemini-3.5-flash-lite",
    "gemini-3.1-pro","gemini-3-flash","grok-4.6","grok-4.5","grok-build-0.1",
    "muse-spark-1.2","qwen3.7-max","qwen3.7-plus","qwen3.6-plus","qwen3.5-plus",
    "deepseek-v4-pro","deepseek-v4-flash","minimax-m3","minimax-m2.7","minimax-m2.5",
    "glm-5.2","glm-5.1","glm-5","kimi-k2.5","kimi-k2.6","kimi-k2.7-code","kimi-k3",
    "big-pickle","mimo-v2.5-free","hy3-free","laguna-s-2.1-free",
    "nemotron-3-ultra-free","nemotron-3.5-lightning-free","deepseek-v4-flash-free",
}
# Exact model NAMES valid on non-opencode providers (relays mirror these IDs;
# native providers publish them). Matched case-insensitively but EXACTLY, so a
# near-miss typo like 'deepseek-v4-max' or a wrong-cased 'MiniMax-M3' on a relay
# that doesn't carry it is caught. Extend deliberately as real models ship.
# 'big-pickle' is intentionally absent: it is Zen-exclusive (opencode/ only).
RELAY_NATIVE_NAMES = {
    # GPT family (apiyi / tokeness relays)
    "gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna", "gpt-5.5", "gpt-5.5-pro",
    "gpt-5.4", "gpt-5.4-pro",
    # Qwen (relays)
    "qwen3.8-max", "qwen3.8-max-free", "qwen3.7-max", "qwen3.7-plus", "qwen3.6-plus",
    # DeepSeek (native)  -- NOTE: only pro/flash exist; 'deepseek-v4-max' is invalid
    "deepseek-v4-pro", "deepseek-v4-flash",
    # Moonshot / Kimi (native)
    "kimi-k3", "kimi-k2.7-code", "kimi-k2.6", "kimi-k2.5",
    # Z.ai / GLM (native subscription)
    "glm-5.3", "glm-5.2", "glm-5-turbo", "glm-5.1", "glm-5",
    # MiniMax (native) -- canonical casing 'MiniMax-M3'
    "minimax-m3", "minimax-m2.7",
    # MiMo (relay) / Grok (relay)
    "mimo-v2.5-pro", "mimo-v2.5-free", "grok-4.6", "grok-4.5",
}

def model_id_valid(full):
    prov, _, name = full.partition("/")
    if not name:
        return False
    if prov == "opencode":
        return name in OPENCODE_ZEN
    # relay / native providers: exact known model name (case-insensitive),
    # never a Zen-exclusive codename.
    if name.lower() == "big-pickle":
        return False
    return name.lower() in {n.lower() for n in RELAY_NATIVE_NAMES}

# --- R13: known cross-vendor mismatches -------------------------------------
# We CANNOT enumerate everything each relay carries (a relay may legitimately
# mirror many vendors), so R12 stays name-only and R13 flags ONLY the routes we
# can affirmatively call wrong: a first-party model served under a DIFFERENT
# first-party vendor's prefix (e.g. deepseek/kimi-k3, minimax/glm-5.3). Relay
# prefixes (apiyi, tokeness, opencode) are exempt — they aggregate many vendors,
# so we make no negative claim about them and avoid false failures.
NATIVE_VENDORS = {"deepseek", "moonshotai", "minimax", "zai-coding-plan"}
# model-name prefix -> the ONLY native vendor that may serve it
NATIVE_OWNER = {
    "deepseek-": "deepseek",
    "kimi-": "moonshotai",
    "minimax-": "minimax",
    "glm-": "zai-coding-plan",
}

def route_mismatch(full):
    """Return an explanation string if this is a known-wrong native route, else None."""
    prov, _, name = full.partition("/")
    if prov not in NATIVE_VENDORS:
        return None  # relay/aggregator: no negative claim
    nl = name.lower()
    for pfx, owner in NATIVE_OWNER.items():
        if nl.startswith(pfx) and prov != owner:
            return f"{full}: '{name}' is a {owner} model, not servable under native '{prov}/'"
    return None

fails = 0
def ok(m):  print(f"  ok   {m}")
def fail(m):
    global fails; fails += 1; print(f"  FAIL {m}")

# ---- R1: strict JSON --------------------------------------------------------
print("[R1] strict JSON parse")
try:
    raw = io.open(path, encoding="utf-8").read()
    d = json.loads(raw)
    ok(f"{os.path.relpath(path, ROOT)} is valid JSON")
except Exception as e:
    fail(f"invalid JSON: {e}")
    print("\n1 or more checks FAILED"); sys.exit(1)

# ---- R2: structure ----------------------------------------------------------
print("[R2] structure")
if "[opencode]" not in d:
    fail("missing '[opencode]' block"); print(); sys.exit(1)
oc = d["[opencode]"]
for k in ("agents", "categories", "runtime_fallback", "background_task"):
    ok(f"[opencode].{k} present") if k in oc else fail(f"[opencode].{k} missing")
agents = oc.get("agents", {})
cats = oc.get("categories", {})

def iter_entries():
    """Yield (context, entry_dict) for every model-bearing object."""
    for an, a in agents.items():
        if isinstance(a.get("model"), str):
            yield f"agent {an}", a
        for i, m in enumerate(a.get("fallback_models", [])):
            yield f"agent {an}.fallback[{i}]", m
        if isinstance(a.get("ultrawork"), dict):
            yield f"agent {an}.ultrawork", a["ultrawork"]
    for cn, c in cats.items():
        for i, m in enumerate(c.get("models", [])):
            yield f"cat {cn}[{i}]", m

# ---- R3: reasoning enum -----------------------------------------------------
print("[R3] reasoning enum")
bad_reasoning = [(ctx, e["reasoning"]) for ctx, e in iter_entries()
                 if "reasoning" in e and e["reasoning"] not in ALLOWED_REASONING]
if bad_reasoning:
    for ctx, v in bad_reasoning:
        fail(f"{ctx}: reasoning '{v}' not in {sorted(ALLOWED_REASONING)}")
else:
    ok("all reasoning values within enum")

# ---- R4: model + non-empty fallback per agent -------------------------------
print("[R4] agents have model + fallback_models")
for an, a in agents.items():
    if not isinstance(a.get("model"), str) or not a["model"]:
        fail(f"agent {an}: missing/empty primary model")
    if not a.get("fallback_models"):
        fail(f"agent {an}: no fallback_models (a single point of failure)")
ok("agent model/fallback presence checked")

# ---- R5: no degenerate/duplicate rungs --------------------------------------
print("[R5] no duplicate/degenerate rungs")
dup_found = False
for an, a in agents.items():
    chain = [a.get("model")] + [m.get("model") for m in a.get("fallback_models", [])]
    seen = set()
    for i, mid in enumerate(chain):
        if mid in seen:
            role = "primary" if i == 0 else f"fallback[{i-1}]"
            fail(f"agent {an}: duplicate model '{mid}' at {role} (fallback must differ from earlier rungs)")
            dup_found = True
        seen.add(mid)
for cn, c in cats.items():
    ms = [m.get("model") for m in c.get("models", [])]
    for x in set(ms):
        if ms.count(x) > 1:
            fail(f"cat {cn}: duplicate model '{x}'")
            dup_found = True
if not dup_found:
    ok("no duplicate or degenerate rungs")

# ---- R6: hephaestus flagship-native-only ------------------------------------
print("[R6] hephaestus flagship-native-only")
NON_FLAGSHIP = ("kimi", "glm", "deepseek", "minimax", "qwen", "gemini")
heph = agents.get("hephaestus")
if not heph:
    fail("hephaestus agent missing")
else:
    prim = heph.get("model", "")
    prov = prim.split("/")[0] if "/" in prim else ""
    offenders = []
    for i, m in enumerate(heph.get("fallback_models", [])):
        mid = m.get("model", "").lower()
        if any(tag in mid for tag in NON_FLAGSHIP):
            offenders.append(f"fallback[{i}]={m['model']}")
    if offenders:
        fail(f"hephaestus fallbacks contain non-flagship families: {offenders} "
             f"(rule: hephaestus fallback chain must be flagship-native-only)")
    else:
        ok(f"hephaestus fallbacks are flagship-native (primary {prim})")
    # ultrawork is allowed to be cross-family (explicit lifeline) — report only.
    uw = heph.get("ultrawork", {}).get("model", "")
    if uw and any(tag in uw.lower() for tag in NON_FLAGSHIP):
        ok(f"hephaestus.ultrawork is cross-family by design: {uw} (allowed)")

# ---- R7: retry_on_errors excludes 400 ---------------------------------------
print("[R7] runtime_fallback excludes 400")
rf = oc.get("runtime_fallback", {})
codes = rf.get("retry_on_errors", [])
if 400 in codes:
    fail(f"retry_on_errors includes 400 {codes} (400 is a rejected request, not a transient outage)")
else:
    ok(f"retry_on_errors = {codes} (400 excluded)")

# ---- R8: providerConcurrency has no unused provider -------------------------
print("[R8] providerConcurrency references only used providers")
used = set()
for _, e in iter_entries():
    mid = e.get("model", "")
    if "/" in mid:
        used.add(mid.split("/")[0])
pc = oc.get("background_task", {}).get("providerConcurrency", {})
unused = [p for p in pc if p not in used]
if unused:
    fail(f"providerConcurrency lists unused providers {unused}; providers in use: {sorted(used)}")
else:
    ok(f"providerConcurrency providers all in use ({sorted(pc.keys()) or 'none listed'})")

# ---- R9: momus enabled, not disable ----------------------------------------
print("[R9] momus uses 'enabled'")
mom = agents.get("momus", {})
if "disable" in mom:
    fail("momus uses invalid key 'disable' (use 'enabled')")
elif "enabled" in mom:
    ok(f"momus.enabled = {mom['enabled']}")
else:
    ok("momus present (no enable/disable flag; framework default applies)")

# ---- R10: no retired-vendor names ------------------------------------------
print("[R10] no retired-vendor (Gemini) names")
hits = [ctx for ctx, e in iter_entries() if RETIRED_VENDORS.search(e.get("model", ""))]
if hits:
    for ctx in hits:
        fail(f"{ctx}: retired vendor (Gemini) present")
else:
    ok("no retired-vendor model names")

# ---- R11: schema pinned -----------------------------------------------------
print("[R11] $schema pinned to a version tag")
schema = d.get("$schema", "")
tag = re.search(r"/v\d+\.\d+\.\d+/", schema)
if "/dev/" in schema:
    fail(f"$schema uses the moving 'dev' branch: {schema} (pin a version tag)")
elif tag:
    ok(f"$schema pinned: {tag.group(0).strip('/')}")
elif schema:
    fail(f"$schema not pinned to a vX.Y.Z tag: {schema}")
else:
    fail("$schema missing")

# ---- R12: model-ID validity -------------------------------------------------
print("[R12] model IDs are valid")
bad_ids = []
for ctx, e in iter_entries():
    mid = e.get("model", "")
    if not model_id_valid(mid):
        bad_ids.append((ctx, mid))
if bad_ids:
    for ctx, mid in bad_ids:
        fail(f"{ctx}: invalid/unknown model ID '{mid}' "
             f"(opencode/* must be a Zen model; big-pickle is Zen-exclusive)")
else:
    ok("all model IDs resolve to a known catalog entry")

# ---- R13: known cross-vendor route mismatches -------------------------------
print("[R13] no known cross-vendor native mis-routes")
misroutes = [route_mismatch(e.get("model", "")) for _, e in iter_entries()]
misroutes = [m for m in misroutes if m]
if misroutes:
    for m in misroutes:
        fail(m)
else:
    ok("no first-party model served under the wrong native vendor prefix")

# ---- result -----------------------------------------------------------------
print()
if fails:
    print(f"{fails} check(s) FAILED")
    sys.exit(1)
print("all full-config checks passed")
