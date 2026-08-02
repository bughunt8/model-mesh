#!/usr/bin/env python3
"""CI checks for model-mesh. The vendor denylist is the release gate and runs first."""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = 0

def ok(m):  print(f"  ok   {m}")
def fail(m):
    global fails; fails += 1; print(f"  FAIL {m}")

# ---------------------------------------------------------------------------
# 1. VENDOR DENYLIST (release gate) — scan file contents AND paths.
#    Allowed framework names: oh-my-openagent, opencode.
# ---------------------------------------------------------------------------
# Real vendor/model names are forbidden. `fable` is allowed ONLY as attribution
# to the upstream MIT project (fable-method / Sahir619), per THIRD_PARTY_NOTICES.
DENY = re.compile(
    r"\b(apiyi|claude|gpt-5|kimi|glm-5|deepseek|gemini|qwen|minimax|haiku|sonnet|opus|codex)\b",
    re.I,
)
# A bare `fable` reference is allowed only on lines that also carry the attribution
# context (the upstream repo/author). Anywhere else it is a leak.
FABLE = re.compile(r"\bfable\b", re.I)
FABLE_OK = re.compile(r"fable-method|Sahir619|github\.com/Sahir619", re.I)
TEXT_EXT = (".md", ".json", ".jsonc", ".sh", ".ps1", ".py", ".yml", ".yaml", ".txt")

def tracked_files():
    for base, dirs, files in os.walk(ROOT):
        if os.sep + ".git" in base:
            continue
        for fn in files:
            yield os.path.join(base, fn)

# *.example.json files intentionally carry real provider/model IDs as a reference
# mapping (see README). They are exempt from the vendor-name denylist by design,
# but still validated for JSON/schema shape below.
def is_example(rel):
    return rel.endswith(".example.json")

print("[1] vendor denylist")
for path in tracked_files():
    rel = os.path.relpath(path, ROOT)
    if is_example(rel):
        continue
    if DENY.search(rel):
        fail(f"forbidden name in PATH: {rel}")
    if path.endswith(TEXT_EXT):
        try:
            with io.open(path, encoding="utf-8", errors="ignore") as f:
                for i, line in enumerate(f, 1):
                    if DENY.search(line):
                        fail(f"forbidden name in {rel}:{i}: {line.strip()[:80]}")
                    if FABLE.search(line) and not FABLE_OK.search(line):
                        fail(f"bare 'fable' (not attribution) in {rel}:{i}: {line.strip()[:80]}")
        except Exception as e:
            fail(f"could not read {rel}: {e}")
if fails == 0:
    ok("no forbidden vendor/model names in contents or paths")

# ---------------------------------------------------------------------------
# 2. Manifests parse and identify as model-mesh
# ---------------------------------------------------------------------------
print("[2] manifests")
for name in [".plugin/plugin.json", ".plugin/marketplace.json"]:
    p = os.path.join(ROOT, name)
    if not os.path.exists(p):
        fail(f"missing {name}"); continue
    try:
        data = json.load(io.open(p, encoding="utf-8"))
        ok(f"{name} parses")
        blob = json.dumps(data)
        if "model-mesh" not in blob:
            fail(f"{name} does not identify as model-mesh")
    except Exception as e:
        fail(f"{name}: {e}")

# ---------------------------------------------------------------------------
# 3. Skills present
# ---------------------------------------------------------------------------
print("[3] skills")
for skill in ["mm-method", "mm-loop", "mm-verify", "mm-domain"]:
    p = os.path.join(ROOT, "skills", skill, "SKILL.md")
    ok(f"{skill}") if os.path.exists(p) else fail(f"missing skills/{skill}/SKILL.md")

# ---------------------------------------------------------------------------
# 4. Profiles: valid JSON + schema shape (agents use model+fallback_models,
#    ultrawork singular model, categories use models[], no `variant`, no `models` on agents)
# ---------------------------------------------------------------------------
print("[4] profiles")
_profile_files = []
for prof in ["ultimate", "hybrid", "b4b"]:
    _profile_files.append(f"{prof}.json")
    ex = os.path.join(ROOT, "profiles", f"{prof}.example.json")
    if os.path.exists(ex):
        _profile_files.append(f"{prof}.example.json")
for prof_file in _profile_files:
    prof = prof_file[:-5]
    p = os.path.join(ROOT, "profiles", prof_file)
    if not os.path.exists(p):
        fail(f"missing profiles/{prof_file}"); continue
    try:
        _txt = io.open(p, encoding="utf-8").read()
        _txt = "\n".join(l for l in _txt.splitlines() if not l.lstrip().startswith("//"))
        d = json.loads(_txt)
    except Exception as e:
        fail(f"{prof_file} invalid JSON: {e}"); continue
    bad = []
    for an, a in d.get("agents", {}).items():
        if "models" in a: bad.append(f"agents.{an}.models (use model+fallback_models)")
        if "variant" in a: bad.append(f"agents.{an}.variant (use reasoning)")
        if "ultrawork" in a and "models" in a["ultrawork"]:
            bad.append(f"agents.{an}.ultrawork.models (use singular model)")
        for m in a.get("fallback_models", []):
            if "variant" in m: bad.append(f"agents.{an} fallback variant")
    for cn, c in d.get("categories", {}).items():
        if "models" not in c: bad.append(f"categories.{cn} missing models[]")
    if bad:
        for b in bad: fail(f"{prof}.json: {b}")
    else:
        ok(f"{prof}.json schema shape")

# ---------------------------------------------------------------------------
# 5. Local markdown links resolve
# ---------------------------------------------------------------------------
print("[5] local links")
link_re = re.compile(r"\]\((?!https?://|#)([^)]+)\)")
for base, dirs, files in os.walk(ROOT):
    if os.sep + ".git" in base:
        continue
    for fn in files:
        if not fn.endswith(".md"):
            continue
        p = os.path.join(base, fn)
        for m in link_re.finditer(io.open(p, encoding="utf-8", errors="ignore").read()):
            target = m.group(1).split("#")[0]
            if not target:
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                fail(f"broken link in {os.path.relpath(p, ROOT)}: {target}")
print("  (link check complete)")

# ---------------------------------------------------------------------------
print()
if fails:
    print(f"{fails} check(s) FAILED")
    sys.exit(1)
print("all checks passed")
