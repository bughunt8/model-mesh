#!/usr/bin/env bash
# model-mesh standalone skill installer (macOS / Linux / Git Bash).
#
# Plugin install (recommended): inside your agent harness run
#   /plugin marketplace add bughunt8/model-mesh
#   /plugin install model-mesh@model-mesh
#
# This script is for users who prefer standalone skills. It installs all four
# skills, backing up any existing same-named skills first.
set -euo pipefail

src="$(cd "$(dirname "$0")" && pwd)"
dst="${MM_SKILLS_DIR:-$HOME/.mm/skills}"
stamp="$(date +%Y%m%d-%H%M%S)"

mkdir -p "$dst"
for skill in mm-method mm-loop mm-verify mm-domain; do
  if [ -e "$dst/$skill" ]; then
    mv "$dst/$skill" "$dst/$skill.bak-$stamp"
    echo "backed up existing $skill -> $skill.bak-$stamp"
  fi
  cp -r "$src/skills/$skill" "$dst/"
done

echo "Installed: mm-method, mm-loop, mm-verify, mm-domain -> $dst"
echo "Try it: run /mm-verify after any agent claims work is done."
