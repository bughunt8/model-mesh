# Full deployable config example

`omo.full.example.json` is a complete, ready-to-deploy `omo.jsonc` for the
oh-my-openagent / opencode framework — the `[opencode]` wrapper, `team_mode`,
`background_task`, `runtime_fallback`, plus the secondary-harness block and `_migrations`. Unlike
the genericized `profiles/*.json` fragments, this file carries **real provider/model
IDs** as a concrete reference (exempt from the vendor-name CI check by design, like
`profiles/*.example.json`). Substitute your own IDs before deploying.

Validated and hardened (Aug 2026): valid JSON (no trailing commas), the retired
utility-vendor family replaced role-aware, `hephaestus` kept flagship-native-only,
`runtime_fallback.retry_on_errors` excludes `400` (not a transient error),
no duplicate/degenerate fallback rungs, unused `providerConcurrency` entries removed,
`momus` uses `enabled` (not `disable`), single canonical `codegraph` per section,
schema pinned to `v4.19.4`.

## Validation

Run `python scripts/validate-full-config.py` to check this file against all of the
rules above (JSON validity, reasoning enum, per-agent fallback presence, no
duplicate/degenerate rungs, `hephaestus` flagship-native-only, `400` excluded from
retries, no unused provider-concurrency entries, `momus.enabled`, no retired-vendor
names, pinned schema). It exits non-zero on any violation and runs automatically in
CI. Pass a path argument to validate a different config file.
