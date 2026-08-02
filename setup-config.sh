#!/usr/bin/env bash
# model-mesh config setup — materializes a chosen profile into a complete,
# schema-valid deployable config and installs it safely (backup, never blind overwrite).
#
# Usage:  ./setup-config.sh [hybrid|ultimate|b4b]     (default: hybrid)
#
# What it does:
#   1. Checks prerequisites (python3, and warns if oh-my-openagent is not installed)
#   2. Wraps the chosen profile fragment in the full [opencode] deployable structure
#   3. Backs up any existing ~/.omo/omo.jsonc before writing
#   4. Reminds you to map placeholders and run doctor
#
# NOTE: profiles/*.json are FRAGMENTS (agents + categories only). This script
# adds the required wrapper. It does NOT invent your real model IDs — you must
# map placeholders first (see docs/PROVIDERS.md).
set -euo pipefail

profile="${1:-hybrid}"
case "$profile" in hybrid|ultimate|b4b) ;; *) echo "Unknown profile: $profile (use hybrid|ultimate|b4b)"; exit 1;; esac

src="$(cd "$(dirname "$0")" && pwd)"
frag="$src/profiles/$profile.json"
[ -f "$frag" ] || { echo "Missing $frag"; exit 1; }
command -v python3 >/dev/null || { echo "python3 required"; exit 1; }

omo_dir="$HOME/.omo"
omo_file="$omo_dir/omo.jsonc"
mkdir -p "$omo_dir"
if [ -f "$omo_file" ]; then
  cp "$omo_file" "$omo_file.bak-$(date +%Y%m%d-%H%M%S)"
  echo "Backed up existing config -> $omo_file.bak-*"
fi

python3 "$src/scripts/materialize.py" "$frag" "$profile" > "$omo_file"
echo "Wrote $profile profile -> $omo_file"

if ! command -v bunx >/dev/null && ! command -v oh-my-openagent >/dev/null; then
  echo "WARNING: oh-my-openagent not found. Install it first (see its docs), then re-run doctor."
fi

cat <<EOF

NEXT STEPS (required):
  1. Map placeholders to your real provider/model IDs in $omo_file
     (see docs/PROVIDERS.md). The file will not work with placeholder names.
  2. Validate:  bunx oh-my-openagent doctor
  3. Roll back if needed:  cp $omo_file.bak-<stamp> $omo_file
EOF
