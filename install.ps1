# model-mesh standalone skill installer (Windows PowerShell).
#
# Plugin install (recommended): inside your agent harness run
#   /plugin marketplace add bughunt8/model-mesh
#   /plugin install model-mesh@model-mesh
#
# This script installs all four skills, backing up existing same-named skills.
$ErrorActionPreference = "Stop"
$src = Split-Path -Parent $MyInvocation.MyCommand.Path
$dst = if ($env:MM_SKILLS_DIR) { $env:MM_SKILLS_DIR } else { Join-Path $HOME ".mm\skills" }
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"

New-Item -ItemType Directory -Force -Path $dst | Out-Null
foreach ($skill in @("mm-method","mm-loop","mm-verify","mm-domain")) {
  $target = Join-Path $dst $skill
  if (Test-Path $target) {
    Move-Item $target "$target.bak-$stamp"
    Write-Host "backed up existing $skill -> $skill.bak-$stamp"
  }
  Copy-Item (Join-Path $src "skills\$skill") $dst -Recurse -Force
}

Write-Host "Installed: mm-method, mm-loop, mm-verify, mm-domain -> $dst"
Write-Host "Try it: run /mm-verify after any agent claims work is done."
