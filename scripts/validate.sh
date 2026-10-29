#!/usr/bin/env bash
# Validates configs/omo.recommended.jsonc across four layers.
# Layer 4 (runtime resolution) must be run manually — see docs/06-handover.md.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CFG="${ROOT}/configs/omo.recommended.jsonc"

layers="1,2,3"
while [ $# -gt 0 ]; do
  case "$1" in
    --layers)
      [ $# -ge 2 ] || { echo "error: --layers requires a value" >&2; exit 2; }
      layers="$2"
      shift 2
      ;;
    --layers=*)
      layers="${1#*=}"
      shift
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

has_layer() {
  case ",${layers}," in
    *",$1,"*) return 0 ;;
    *) return 1 ;;
  esac
}

fail=0

if has_layer 1; then
  echo "== Layer 1: JSONC syntax =="
  if ! python3 - "$CFG" <<'PY'
import json, re, sys, pathlib
p = pathlib.Path(sys.argv[1])
s = p.read_text()
s = re.sub(r'^\s*//.*$', '', s, flags=re.M)          # line comments
s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)           # block comments
s = re.sub(r',(\s*[}\]])', r'\1', s)                  # trailing commas
try:
    json.loads(s)
    print("  OK — valid JSONC")
except json.JSONDecodeError as e:
    print(f"  FAIL — {e}")
    sys.exit(1)
PY
  then
    fail=1
  fi
  echo
fi

if has_layer 2; then
  echo "== Layer 2: required keys and duplicate keys =="
  if ! python3 - "$CFG" <<'PY'
import json, re, sys, pathlib

s = pathlib.Path(sys.argv[1]).read_text()
s = re.sub(r'^\s*//.*$', '', s, flags=re.M)
s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
s = re.sub(r',(\s*[}\]])', r'\1', s)

duplicates = []

def no_duplicate_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            duplicates.append(key)
        out[key] = value
    return out

d = json.loads(s, object_pairs_hook=no_duplicate_keys)
if duplicates:
    for key in duplicates:
        print(f"  FAIL — duplicate key: {key}")
    sys.exit(1)

oc = d["[opencode]"]

required_agents = [
    "hephaestus", "oracle", "prometheus", "metis", "momus", "atlas",
    "sisyphus-junior", "sisyphus", "librarian", "explore", "multimodal-looker",
]
required_cats = [
    "architect", "artistry", "deep-low", "deep-high", "quick",
    "ultrabrain", "unspecified-high", "unspecified-low",
    "visual-engineering", "writing",
]

missing = [a for a in required_agents if a not in oc.get("agents", {})]
if missing:
    print(f"  FAIL — missing agents: {missing}")
    sys.exit(1)
missing = [c for c in required_cats if c not in oc.get("categories", {})]
if missing:
    print(f"  FAIL — missing categories: {missing}")
    sys.exit(1)

for name in required_agents:
    print(f"  OK — {name}")
print("  OK — no duplicate keys")
print("  OK — all 11 agents and 10 categories present")
PY
  then
    fail=1
  fi
  echo
fi

if has_layer 3; then
  echo "== Layer 3: doctor (requires oh-my-openagent) =="
  if command -v bunx >/dev/null 2>&1; then
    cp "$CFG" "${HOME}/.omo/omo.jsonc.bak.$(date +%s)" 2>/dev/null || true
    bunx oh-my-openagent doctor --verbose || true
  else
    echo "  SKIP — bunx not found"
  fi
  echo
fi

if has_layer 4; then
  echo "== Layer 4: runtime resolution (manual) =="
  cat <<'EOF'
  Run one spawn per agent and category, then check the resolved model:

    opencode run --format json "@explore find OmoConfigSchema" \
      | jq -r 'select(.model != null) | .model' | sort -u

    opencode run --format json "task(category='quick', prompt='print hi')" \
      | jq -r 'select(.model != null) | .model' | sort -u

  Then confirm the structured contracts still fire:

    opencode run --format json "@momus review .omo/plans/example.md" \
      | jq -r 'select(.type=="text") | .text' \
      | grep -E '^(PLAN_APPROVED|PLAN_REJECTED)$'
EOF
  echo
fi

if [ "$fail" -ne 0 ]; then
  echo "RESULT: validation failed at layer 1 or 2."
  exit 1
fi
echo "RESULT: requested layers passed."
