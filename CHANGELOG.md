# Changelog

## 1.4.0

### Added
- **Superloop.** `docs/SUPERLOOP.md` defines an outer loop for long goals: code owns continuation and the caps, omo workers run one batch per call under a frozen matrix cell, a typed decision model answers logged questions, and success needs passing checks on a copy of the hashed tree, a review with no blocker and no major by a reviewer independent of the whole lineage, an unchanged tree during the review and a second check run. The guarantees need a worker that cannot write outside its worktree and checks that read nothing a worker wrote except their snapshot. On Linux the driver enforces both with a pinned bubblewrap, and `final.json` records what it enforced and what was only stated. The decision model may brake and never accelerate. Shadow mode is the default and there is no control mode. Design plus an offline-tested driver; no live run.
- **`scripts/mm-superloop.py` and `scripts/superloop/`.** The driver: admission against the matrix; an omo config restricted to the cell's author and orchestrator families, with continuation, runtime fallback and team mode off, rewritten before every batch and checked for tampering; session agent and model checks through a pinned session export; a driver-owned git store outside the worktree, so no config, hook, filter, replace ref or attribute from the worker's repository takes part; a whole-tree hash that includes ignored files, with checks run on a copy of the hashed tree, in a bubblewrap jail that mounts only the system folders, the owner's check mounts and the snapshot when `check_jail` is `bwrap`, a bubblewrap worker jail when `worker.isolation` is `bwrap`, and nested repositories, escaping symlinks and a moved `.git` refused; binary diffs kept as bytes; an output folder inside the worktree refused; checks that start passing on an unchanged tree refused; any unexpected error ending in `final.json`; workers and reviewers resolved from the owner's tools registry with pins re-hashed before every call; reviewer findings read from the reviewer's output stream; a refusal of checks that already pass before the work; a hash-chained event log; a cumulative lineage ledger and a lineage registry that must exist, keyed by the owner's repository name and bound to one git directory; a fact-only state builder with redaction; decision backends (rules, replay, HTTP, dual); learn-then-test qualification records verified at admission; and the stop rules. `--self-test` runs 81 scenarios and 21 unit checks offline.
- **`scripts/validate-superloop.py`.** Rules L1 to L12 for goals, controllers, the tools registry and the question catalog, with 66 mutation cases.
- **`examples/superloop/`.** The question catalog, a goal template, a shadow pilot controller, an offline rules controller and a tools registry template.
- **`skills/mm-superloop/`** with scenarios in `tests/scenarios/mm-superloop.json`.
- **`docs/research/orchestration/SUPERLOOP-COUNCIL.md` and `superloop-council/`.** A five-family council on whether a decision model fits the six agentic patterns and the omo superloop, the raw reports, and four rounds of independent review of the driver with what changed because of them.

### Changed
- `docs/research/orchestration/SYSTEM-ONE.md` corrects two errors (the retention terms, and an integration guide wrongly called the vendor's) and adds model limits, confidence definitions, other decision models, constrained decoding and the council outcome. Still no decision seat in the matrix.
- `mm-loop` points long goals to the superloop and gains a BLOCKED outcome. `mm-verify` gains machine-readable findings, printed as a JSON list on the last output line.
- The OpenCode with omo harness example now invokes the omo run wrapper from a pinned local install.

## 1.3.0

### Added
- **Review panel.** `docs/REVIEW-PANEL.md` defines how reviews run: zero-context reviewers with read-only tools, twelve review lenses, a fan-out budget by tier, an aggregator, and spec and drift gates. The design was informed by a study of the Elephant-Goldfish Model, recorded in `docs/research/orchestration/EGM-ANALYSIS.md`. No source text was copied.
- **Matrix fields.** Every situation has `review_tier`, `lenses` and `gates`. Every reviewer seat has `lenses`. Every option has an `aggregator` seat and the `zero-context-review` constraint. A05 and A06 get a second reviewer seat from a disjoint model family, with the primary lens run by both.
- **Validator rules O15 to O18** with 34 new mutation cases, including file-based cases that finally cover O10, O13 and O14 in `--self-test`.
- **`examples/orchestration/lenses.json`, `finding.schema.json` and `standards/`** (spec readiness and drift).
- **`scripts/aggregate-findings.py`.** Validates findings, clusters them deterministically against the first finding's range, namespaces ids by file, normalizes paths and families, marks cross-family corroboration and lists possible duplicates for the model merge.
- **`scripts/score-review.py`, `examples/orchestration/seeded/` and `docs/research/orchestration/SEEDED-DEFECTS.md`.** The scorer and protocol for testing whether more lenses or more families catch more. The fixture is invented and no result is claimed.
- **`scripts/check-drift.py`.** Compares counts, IDs, links, versions, tier and gate tables and the test counts in the docs with the data and scripts (rules D1 to D9).
- **`docs/research/orchestration/SYSTEM-ONE.md`.** Assessment note on System One decision models: why none is in the matrix, where one could fit, and the shadow-mode pilot criteria.
- **`scripts/validate-scenarios.py`, `tests/scenarios/` and `TESTING.md`.** Skill front matter and size cap checks and static scenario patterns.

### Changed
- Rule O14 now reads `MATRIX.md` under the root it is given, so the self-test can cover it.
- Spread options outside ultimate use a third family as the aggregator's first rung where the model table has one.
- `MATRIX.md` gains lens and aggregator columns and a review panel table.
- The independence rule gains a fifth point: the aggregator sits outside the author and orchestrator harness and families.
- `mm-domain` and `mm-verify` gain a `description` in their front matter. Both had none.
- `README.md` said three profiles in two places. It now says four.

## 1.2.0

### Added
- **Multi-agent orchestration direction.** `docs/ORCHESTRATION.md` extends routing from one agent and its sub-agents to several agents across seven harnesses, using omo role and category names. Twelve situations (A01 to A12) map to a harness, a model chain with fallbacks, and an independent reviewer, for four profiles. Design proposal only: nothing was installed or run.
- **`global` profile.** The unrestricted twin of `ultimate` (no region limit, no budget cap). `profiles/global.json` and `profiles/global.example.json`; `setup-config.sh global` works. The retired Google family stays retired.
- **`scripts/validate-orchestration.py`.** Checks vocabulary, review independence over every fallback rung, the Hong Kong rule for `ultimate`, cap placement for `hybrid` and `b4b`, hephaestus family, and that the generated table matches the data. A mutation self-test proves 40 failure cases are caught, including every hole the independent review found. Both modes run in CI.
- **Seven harness configuration examples** under `examples/orchestration/harnesses/`, each with sources and limitations. Docs-checked only; install, load and dry-run are deferred.
- **Research record** under `docs/research/orchestration/`: council reports, synthesis, harness and coordinator evidence, worked examples, and the independent review.

### Changed
- `.github/checks.py`: a narrow harness-name allowlist (Codex CLI, Qwen Code) so orchestration docs can name harnesses without admitting model IDs, with must-pass and must-fail self-tests; the validator script joins the exact exemption list; `global` joins the profile schema loop; a mirror check keeps the cap policy in `validate-orchestration.py` equal to `checks.py`.
- `scripts/validate-full-config.py`: the model-ID catalog accepts the verified `global` IDs, and R12b covers `global.example.json`.

### Known issues found by the audit, not fixed here
- In the shipped `ultimate` and `hybrid` profiles, `momus` uses the same model as `hephaestus`, inside one harness. The orchestration matrix fixes this with an external reviewer; the base profiles are unchanged.
- The `opencode/mimo-v2.5-free` route used in the example profiles stops working on 2026-10-21.
- omo is under the Sustainable Use License 1.0. The owner accepted it as an explicit exception. Client or commercial use needs a separate licence check.

## 1.1.5

### Fixed
- **Cap semantics corrected (docs).** Earlier notes described the metered-profile budget ceiling as "the `coder-xl` cost cap", implying it equalled that model's price. It does **not** — `coder-xl`'s published output price ($15/1M) is far above the ceiling. The ceiling is now documented as an explicit, editable **policy budget cap** independent of any vendor's list price, governing generalist/utility/orchestration rungs; the flagship coding tier (`coder-xl`), the architect (`oracle`), and each agent's `ultrawork` escape hatch are **named exemptions** that may exceed it. `docs/EXAMPLE-MAPPING.md` now carries an exemption table listing exactly which over-cap slots exist in the metered profiles, and every "under/over cap" claim was re-audited against the $4.65 number. (Previously the docs both under- and over-claimed: they called the cap a hard ceiling while shipping an over-cap flagship coder in the metered profiles.)
- **`comm-xl` pricing note honesty.** The prior "assumption: pricing unchanged / per-token price not yet published" note is replaced with the now-published rate card. The communicator's newest release carries the **same unit price** as its predecessor (only publication is new, not a price change), and a verbosity caveat was added: measurably more output tokens per task can raise real cost-per-solved-task even at an unchanged unit price.
- **No-op fallback rungs removed (mapping level).** Several `*.example.json` chains listed two distinct placeholders that resolved to the **same** real model in one chain (a retry that buys nothing). Root-caused in the example mapping, where two placeholder pairs had collapsed onto one model: `gen-flash` is remapped to a distinct fast gateway model (previously shared `open-reason-lite`'s target) and `creative-mid` to a distinct creative model (previously shared `gen-pro`'s target, and its first fix would have shared `retrieval-mid`'s — corrected). The genericized templates were left intact (the collapse was a property of the example mapping, not the templates), and the `.example.json` files were regenerated from the templates + corrected mapping. The remaining intentional alias (`comm-lite`/`vision-lite` → one cheap GLM model) never lands twice in a single chain.
- **Stale full-example rungs.** The full deployable example still referenced a retired cheap communicator on three chains; replaced with the current cheap communicator/vision model and added to `modelConcurrency`.

### Added
- **New cheap multimodal fallback role (`vision-lite`).** Added to `multimodal-looker` directly behind the vision primary in the metered profiles — a native-vision cheap model, so the first fallback keeps vision capability instead of degrading to a text-only rung. Documented in `docs/PROVIDERS.md` and the local provider map. Its vision note now cites an **independent, ground-truth** vision benchmark (Roboflow Vision Evals: 66.3% overall, #23 of 34) rather than the vendor's self-reported MVBench/MMVU figures, which the note flags as unverified; the placement is documented as cost-first, not a capability claim.

### Changed
- `.github/checks.py`: the duplicate-rung check now also runs on `*.example.json` (and now walks each agent's `ultrawork` slot too). With real IDs, a byte-identical model repeated in one chain is unambiguously a no-op bug; distinct placeholders that resolve to one model in *different* chains remain allowed.
- `.github/checks.py`: **new budget-cap placement rule** — an over-cap placeholder (`flagship-open`, `div-flagship`, `reasoner-xl`) that is not on the explicit metered-profile exemption list fails the build if it appears in `hybrid.json`/`b4b.json`. The flagship coding tier (`coder-xl`) is the documented exemption. This closes the gap where the metered profiles' cost policy was documented but unenforced.
- `scripts/validate-full-config.py`: **R12** (model-ID catalog validity) now also runs on `profiles/*.example.json`, not just the full deployable example.

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
- **`flagship-open` (new):** a new placeholder for the now-GA frontier-class open flagship replaces the retired preview last-resort rung. Its per-token output cost exceeds the policy budget cap (see v1.1.5 and `docs/EXAMPLE-MAPPING.md`), so it is wired in `ultimate` only; `hybrid`/`b4b` use `gen-pro` in those slots.
- **`comm-xl` upgraded:** migrated to the communicator vendor's newest release across all three profiles. (Per-token pricing was later published — same unit price as the prior release, under the policy budget cap; see v1.1.5.)
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
