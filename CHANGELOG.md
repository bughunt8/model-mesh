# Changelog

## 1.1.4

### Fixed
- Aligned the repo's schema rules with the authoritative **v4.19.4** `omo.schema.json` (`[opencode]` block). Corrected the `reasoning` enum to `off/minimal/low/medium/high/xhigh/max/auto` — the value `ultra` is **not** valid and was replaced with `max` in the profiles that used it.
- Removed an invalid `enabled` key from `momus` in the full deployable example (the v4.19.4 schema key is `disable`; `enabled` is rejected by `oh-my-openagent doctor`).

### Added
- `scripts/validate-full-config.py`: new rule **R14** validates every agent/category/model-ref object against the schema's allowed key set (`additionalProperties:false`), mirroring `oh-my-openagent doctor`. This catches invented keys (e.g. an agent `models` key, or `enabled` instead of `disable`) that earlier slipped through.
- `.github/checks.py`: the profile schema-shape check now enforces the same allowed-key sets and the corrected `reasoning` enum on the genericized profiles, and accepts any schema-valid category model form (`models`, `model`, or `fallback_models`).

### Changed
- `scripts/validate-full-config.py`: rule **R9** corrected — it now requires the schema key `disable` (bool) and flags `enabled` as invalid (previously reversed).

## 1.1.3

### Changed
- `scripts/validate-full-config.py`: tightened rule **R12** from loose substring matching to exact per-provider model-name matching, so a near-miss typo in a model name (a valid model family with an invalid version/variant suffix) no longer slips through.

### Added
- `scripts/validate-full-config.py`: new rule **R13** (cross-vendor route check) flags a first-party model served under the wrong native vendor prefix (a `ProviderX/model` where `model` belongs to a different first-party vendor). Relay/aggregator provider prefixes are exempt by design — a relay may legitimately mirror many vendors and their full coverage is not enumerable, so R13 makes no negative claim about relay routes to avoid false failures. It is the honest, non-guessing complement to R12's name-validity check.

## 1.1.2

### Added
- **MiMo across the profiles.** New `open-coder` placeholder (`opencode/mimo-v2.5-free`; the full deployable example uses `mimo-v2.5-pro` via the tokeness relay) — a token-efficient open-weight coder wired as a coding/open fallback rung in `deep` (all profiles), on `atlas`/`sisyphus-junior` open backups, and in `b4b`'s `unspecified-low`.

### Fixed
- Removed two pre-existing duplicate fallback rungs in the genericized profiles (`ultimate` `ultrabrain` had `flagship-xl` twice → 2nd is now `coder-xl`; `hybrid` `oracle` had `comm-xl` twice → trailing duplicate dropped), plus a duplicate `gen-pro` on `hybrid` `atlas`.
- Replaced the invalid `tokeness/big-pickle` rung in the full config with the MiMo relay model (`big-pickle` is OpenCode-Zen-exclusive, not carried by a relay).

### Changed
- `.github/checks.py`: profile schema-check now also fails on duplicate fallback rungs in the genericized `*.json` profiles (example files are exempt because distinct placeholders may legitimately collapse to the same real model under a mapping).
- `scripts/validate-full-config.py`: added rule R12 (model-ID validity against a known catalog; Zen-exclusive codenames rejected under relay/native prefixes).

## 1.1.1

### Changed - model refresh (Aug 2026)
(Concrete model IDs, prices, and benchmark citations live in `docs/EXAMPLE-MAPPING.md`; this public changelog uses role placeholders per the repo's placeholder-only convention.)
- **`open-reason-xl` -> GA build:** the open-weight reasoning lifeline moved to its new general-availability build. The provider's API ID is unchanged, so no config edit was needed; large agentic-benchmark gains. Provider moved to peak/off-peak billing mid-August; still under the cost cap.
- **`flagship-open` (new):** a new placeholder for the now-GA frontier-class open flagship replaces the retired preview last-resort rung. Its per-token output cost exceeds the `coder-xl` cap, so it is wired in `ultimate` only; `hybrid`/`b4b` use `gen-pro` in those slots.
- **`comm-xl` upgraded:** migrated to the communicator vendor's newest release across all three profiles. Assumption: pricing unchanged (same subscription tier; per-token price not yet published), so the per-token cap does not gate it.
- **Retired the utility vendor family:** removed both former `util-pro`/`util-flash` models entirely. Role-aware replacements: `gen-pro` (planning/writing/visual/artistry generalist) and `gen-flash` (fast loop). High-stakes safety rungs on `oracle`/`momus`/`prometheus` were promoted to the strongest model not already in-chain rather than a flat swap.
- **`div-flagship` (new, provider `ProviderG`):** an independent 5th-vendor diversification fallback added to `atlas` and `prometheus` in `ultimate` only (not `hephaestus`, which stays flagship-native-only). Rationale is independent-vendor resilience + token efficiency, not a raw benchmark lead. Cost > cap, hence ultimate only.
- Updated `docs/EXAMPLE-MAPPING.md` and `docs/PROVIDERS.md` to match.
- `.github/checks.py`: added the new vendor tokens to the release denylist so real IDs cannot leak into genericized files.

## 1.1.0

### Added - four engineering gates folded into the mm-method loop
(concepts adapted from matt-pocock/skills by Matt Pocock; see THIRD_PARTY_NOTICES.md)
- **Grill gate (Step 1)** - requirement-sharpening interview: mini-orient first, decisions-only (facts are looked up), one question at a time with a recommended answer, bounded; reconciled with Step 0. Owed `GRILL:` line.
- **Prototype gate (new Step 3.5, conditional)** - throwaway code for genuine design risks (race conditions, non-atomic/multi-step transactions, state-machine uncertainty, distributed effects, UI shape) in the change's own scope; a "do NOT prototype when" negative gate; capture transcript, delete code. Owed `PROTO:` line.
- **Test-first (Step 4)** - vertical slices at agreed seams, observed-red before green, anti-patterns (tautological, implementation-coupled, horizontal slicing). Owed `SEAMS:` line.
- **Two-axis review (Step 4 close)** - Spec + Standards judged independently on a materialized diff, two counts never merged, refactor only on a green baseline with a 2-round bound. Owed `REVIEW:` line.

### Added - verification fold-ins
(concepts adapted from the debug-pipeline2 protocol by ronald-ng, MIT)
- **Machine-checkable evidence** - a report claim needs the exact command + real output; new `references/evidence.md`.
- **Negative tests / discrimination** - a behavior-changing check must be shown able to fail (observed-red, or fails on revert); scoped to exclude refactors, regression checks, and Question-shaped work.
- **False-green defence (full-band coding work)** - re-run it yourself, do not trust a log you did not produce. Owed `VERIFY:` line with command + output.
- **Independent-reviewer isolation** - review axes run as fresh, artifacts-only subagents, never told each other's verdict.

### Added - references and coverage
- `references/gates.md` - worked walk-throughs of all four gates plus a full four-gate feature example.
- `references/evidence.md` - the binding evidence standard.
- `references/smells.md` - the Standards-axis smell baseline.
- `references/examples.md` - extended with a gate-firing example.
- `references/failure-modes.md` - expanded from 18 to 26 modes (19-26 cover the gates and fold-ins); audit guidance for hollow vs missing gate lines.
- New owed report line `VERIFY:` and audit coverage of evidence capture, discrimination, and reviewer isolation.

### Changed
- Proportionality bands formalized (trivial / Small / full); gates fire per their own triggers, Small-band and trivial work exempt from the heavier gates.
- README Credits expanded to name Matt Pocock and debug-pipeline2.

### Notes
- Hardened across three independent adversarial review rounds; all critical, major, and minor findings resolved.

## 1.0.0
- Initial release of model-mesh.
- Loop skills adapted from fable-method (MIT; see THIRD_PARTY_NOTICES.md): think (mm-method), act (mm-loop), prove (mm-verify), grow (mm-domain).
- Multi-model routing layer for oh-my-openagent with three profiles: ultimate, hybrid (default), b4b.
- All provider/model names genericized to placeholders (docs/PROVIDERS.md). Framework names (oh-my-openagent, opencode) intentionally kept and documented.
- Safe setup: setup-config.sh materializes any profile into a complete, schema-valid config with backup; profiles ship as fragments.
- CI enforces a vendor-name denylist, manifest/skill/profile validation, and link checks.
- Privacy note added: cross-provider fallback data-boundary caveat; 400 removed from transient retries.
- Schema pinned to a released framework tag for reproducibility.
