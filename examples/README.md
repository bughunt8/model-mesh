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

Model-ID validity (Aug 2026): this example routes through the `tokeness` relay
(an OpenAI-compatible hub) plus several native provider APIs. The former
`tokeness/big-pickle` rung was removed — `big-pickle` is an OpenCode-Zen-exclusive
cloaked model and is not carried by a relay — and replaced with the MiMo open
coder on the relay, which also adds a token-efficient open-coder fallback rung.
The validator's rule R12 enforces this: any `opencode/*` model must be a published
Zen model, and Zen-exclusive codenames are rejected under any other provider prefix.

## DSH plugin settings example

`dsh-settings.example.yaml` is a reference for the **DSH** (DeepSeek-Harness) OmO
plugin extension — the `~/.dsh-env/data/settings.yaml` shape: UI/session prefs, the
`agent-default-model`, the `llm-pi-ai.providers` catalog (relay + native provider
blocks), and the `opencode-omo-roles.roles` map (per-role model + `fallbackModels` +
`ultrawork`). It mirrors the same routing methodology as `omo.full.example.json`:

- `hephaestus` is kept flagship-native (GPT primary + GPT fallbacks; the sole
  cross-family rung is `ultrawork`).
- Provider routes are consistent with each provider's own `models` catalog (each
  role routes a model only through a provider whose catalog lists it; the relay
  proxy carries the broad catalog, the native provider blocks carry their own).
- No duplicate/no-op rungs within any role chain.
- `sessions:` is emptied (a real install fills it with live session→role bindings).

Notes specific to this example (intentional, documented deviations):
- The relay catalog lists several models that **no role routes to** (including
  entries from vendors the routing never selects) — they reflect what the relay
  offers, not routing choices. The routing map never selects a disallowed-vendor
  model.
- `agent-default-model` is set to a fast, cheap default by owner preference. The
  Sept-2026 landscape assessment recommends HOLD on that model for cost-capped
  *routing roles*; as a cheap default chat model outside the role map it is a
  deliberate choice, not a routing rung. See the report under `docs/research/`.
- `hephaestus` primary here is the flagship reasoning tier (max reasoning) — a
  deliberate flagship-first choice for the lead implementation agent, cost ignored
  by design. Its fallbacks and the rest of the chain remain flagship-native.
- `omoJson.enabled: true` writes `~/.omo/omo.jsonc`. If you ALSO hand-maintain an
  `omo.jsonc`, treat one as the source of truth to avoid last-writer-wins drift.
- The DSH-runtime open-reasoning provider referenced by some roles is resolved by
  the DSH runtime and is intentionally not duplicated in the `providers` block.

(Real provider/model IDs are exempt from the vendor-name CI check for
`*.example.yaml` just as for `*.example.json`; this README is not, so it refers to
tiers/roles rather than literal model IDs.)

## Validation

Run `python scripts/validate-full-config.py` to check the JSON example against all of the
rules above (JSON validity, reasoning enum, per-agent fallback presence, no
duplicate/degenerate rungs, `hephaestus` flagship-native-only, `400` excluded from
retries, no unused provider-concurrency entries, `momus.enabled`, no retired-vendor
names, pinned schema). It exits non-zero on any violation and runs automatically in
CI. Pass a path argument to validate a different config file.
