<div align="center">

# model-mesh

### The right model in the right seat, following a loop that works like a careful senior engineer.

**An open-source, harness-agnostic agent loop + family-based multi-model routing. Model-agnostic. Deployable. Self-governing.**

_Works on any coding-agent harness. The shipped examples target two: [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) (OpenCode) and the DeepSeek Harness (DSH)._

[Quickstart](#quickstart-60-seconds) · [How it works](#how-it-works) · [Profiles](#the-routing-one-role-one-family) · [Self-governing](#self-governing-the-landscape-engine) · [Validation](#validation-two-gates) · [Claims & limits](#claims--limits)

`v1.1.5` · MIT · CI-gated on `main` and every PR

</div>

---

## Why this exists

Most multi-model setups do one of two things: pin everything to a single "best" model, or route by a benchmark leaderboard that's stale the week it ships. Both ignore the thing that actually moves quality. Put each agent role on a model whose *behavioral family* fits the job, and make the model work a disciplined loop instead of free-styling.

model-mesh is that idea, made concrete and deployable:

- **A loop** that makes a capable model work like a methodical senior engineer. Classify the ask, define "done," gather evidence, decide, act surgically, verify by observation, report outcome-first.
- **A routing layer** that assigns each agent role (implementer, architect, reviewer, coders, orchestrator, explorers) to a model *family*, not a raw benchmark rank, across three ready profiles.
- **A self-governing update engine**: a committed weekly **runbook** an agent cron executes on your side, scoring new releases against the repo's own rules, having an **independent model review the recommendation**, and opening a PR only when a change is actually warranted. (The scripts and gates ship here; the schedule and the reviewer credential are yours to wire up.)

> **Honesty up front:** the routing rationale is a set of design heuristics, not measured benchmarks. Because you map placeholders to your own models, no fixed cost or quality number holds across all mappings. See [Claims & limits](#claims--limits). This is a design opinion you can deploy and measure, not a guarantee.

---

## How it works

```
        ┌────────────────────────── THE LOOP ──────────────────────────┐
        │  think  →  act  →  prove  →  grow                             │
        │  classify · define done · evidence · decide · act · verify    │
        └───────────────────────────────┬───────────────────────────────┘
                                         │  runs on
                                         ▼
        ┌───────────────────────── THE ROUTING ────────────────────────┐
        │  each role → a model FAMILY (not a leaderboard rank)          │
        │  hephaestus  oracle  momus  atlas  prometheus  sisyphus  …    │
        │  profiles:   ultimate   ·   hybrid (default)   ·   b4b        │
        └───────────────────────────────┬───────────────────────────────┘
                                         │  kept current by
                                         ▼
        ┌────────────────────── THE LANDSCAPE ENGINE ──────────────────┐
        │  weekly scan → provenance-checked scoring → independent       │
        │  AI review gate → PR only when a change is justified          │
        └───────────────────────────────────────────────────────────────┘
```

Three layers, one principle at each: **method over improvisation, family-fit over rank, evidence over assertion.**

---

## Quickstart

**Human:**

```bash
git clone https://github.com/bughunt8/model-mesh && cd model-mesh
./setup-config.sh hybrid          # ultimate | hybrid (default) | b4b
# → backs up any existing ~/.omo/omo.jsonc, writes the chosen profile
```

Then map the placeholders to *your* models (open `~/.omo/omo.jsonc` + [`docs/PROVIDERS.md`](docs/PROVIDERS.md); put real IDs in the git-ignored `provider-map.local`), and verify:

```bash
bunx oh-my-openagent doctor       # must report no issues
bash install.sh                   # optional: install the loop skills
```

Use it: `/mm-method <task>` runs the full loop · `/mm-loop <task>` orchestrates plan→execute→verify→audit · `/mm-verify` adversarially reviews finished work. Rollback anytime from the timestamped `.bak`.

**LLM / agent:** follow [`AGENTS.md`](AGENTS.md). Read [`docs/ROUTING.md`](docs/ROUTING.md) + [`docs/PROVIDERS.md`](docs/PROVIDERS.md) first, default to `hybrid`, produce a placeholder→real-model mapping table and get approval **before** writing real IDs (never invent a model ID), then `./setup-config.sh` and validate to green.

---

## The loop (think / act / prove / grow)

| Phase | Skill | What it does |
|---|---|---|
| **think** | `mm-method` | classify → define done → gather evidence → decide → act → verify → report |
| **act** | `mm-loop` | orchestrated plan / execute / verify / audit across subagents |
| **prove** | `mm-verify` | adversarial verification of finished work, tries to *break* the result |
| **grow** | `mm-domain` | generates domain adapters (marketing, research, data, devops, …) |

**Hard bounds keep it honest:** 3 failed verify cycles → stop and hand back · can't name a verification → ask one pointed question · trivial asks skip the ceremony. Adapted from [fable-method](https://github.com/Sahir619/fable-method) (MIT), with engineering gates from [mattpocock/skills](https://github.com/mattpocock/skills) and verification fold-ins from the `debug-pipeline2` protocol. Full detail in [`AGENTS.md`](AGENTS.md) and `skills/`.

---

## The routing (one role, one family)

Every agent role maps to a behavioral **family**: flagship-native, communicator-class, dual-prompt, multimodal, open-weight, utility. A model that *behaves* like the role's prompt expects beats a higher-ranked model that doesn't. Full methodology in [`docs/ROUTING.md`](docs/ROUTING.md).

**Primary model per role, straight from the JSON:**

| Role | ultimate | hybrid (default) | b4b |
|---|---|---|---|
| implementer (`hephaestus`) | `open-reason-xl` | `flagship-mid` | `flagship-mid` |
| architect (`oracle`) | `open-reason-xl` | **`flagship-xl`** | `flagship-mid` |
| reviewer (`momus`) | `open-reason-xl` | `flagship-mid` | `flagship-mid` |
| coding agents (`atlas`, `prometheus`) | `coder-xl` | `coder-xl` | `coder-mid` |
| orchestration (`sisyphus`) | `comm-xl` | `comm-xl` | `comm-xl` |

The `ultimate` column shows `open-reason-xl` for the three flagship-native seats because that profile is Hong Kong-native. HK cannot reach the US proprietary flagships those seats use elsewhere, so the profile explicitly remaps them to the strongest region-reachable open-weight reasoner. See the regional note below.

**Why hybrid is the default:** it spends the flagship budget only where it has the highest leverage, the read-only **architect** and the **flagship coding tier**, while holding the implementer and reviewer at the mid tier. `hephaestus` keeps a **flagship-native primary tier**, one documented open-weight **lifeline** rung (a different-provider model, so a flagship-proxy outage still reaches something that works), and, where set, a single cross-family `ultrawork` escape hatch. (`flagship-native-only` is the stricter rule the validator enforces on the deployable *example* config.)

**Pick your profile:** `ultimate` = max capability, cost secondary · `hybrid` = best value + best-in-class coding/architecture · `b4b` = strict performance-per-dollar.

> **`ultimate` is Hong Kong-native.** Its example mapping deliberately omits every model whose **developer API is not natively available in Hong Kong**, the US frontier vendors' proprietary flagships (US vendors self-restrict HK developer-API access; one such vendor shipped a consumer app in HK but its native developer API and studio still refuse HK, and an enterprise `asia-east2` region is that vendor's only compliant dev route). `ultimate` uses no geo-unlock proxy and routes only to the strongest HK-reachable models (open-weight reasoning, coding-specialist, communicator-class, generalist, and multimodal families). `hybrid` and `b4b` remain **global** and unchanged. The concrete excluded vendors, the placeholder→real-model table, and the availability citations are in [`docs/EXAMPLE-MAPPING.md`](docs/EXAMPLE-MAPPING.md) (denylist-exempt).

### The policy budget cap (metered profiles)

`hybrid` and `b4b` hold their generalist / utility / orchestration rungs at or under an **explicit, editable policy budget cap**, a repo-chosen output-price ceiling, deliberately **decoupled from any single vendor's price**. In `hybrid`, three slots are named exemptions that may exceed it: the flagship **coding** tier, the **architect**, and each agent's **ultrawork** escape hatch. `b4b` applies the same cap more aggressively. The architect drops under cap and the flagship coder survives only as a `deep`-category fallback. The cap is a preference for the cheap tiers, not a hard per-slot ceiling. The *placement* rule is **enforced in CI**. An over-cap placeholder that isn't on the exemption list fails the build if it lands in a metered profile ([`.github/checks.py`](.github/checks.py)); the prices themselves are audited by hand against [`docs/EXAMPLE-MAPPING.md`](docs/EXAMPLE-MAPPING.md), which carries the exact exemption table.

---

## Self-governing: the landscape engine

New models drop constantly. Instead of a human eyeballing leaderboards, model-mesh keeps *itself* current, safely, with the same evidence discipline as the loop. Lives in [`scripts/landscape/`](scripts/landscape/).

- **Provenance-enforced scoring.** A deterministic scorer reads a weekly "scan dataset" (models × benchmarks × scores × **provenance**) and ranks **only on cells whose provenance is marked independent**, the three sources listed as authoritative-independent in `sources.json` (Artificial Analysis, DeepSWE, Vals). It refuses to score vendor-reported cells; because a board like the DeepSWE leaderboard hosts both, rows are judged per-row, not by board. Mixed feeds (e.g. Vellum) are usable only per-row and only for positioning.
- **Fail-closed hard gates.** Cap checks use the **durable** (post-promo) price; a retired vendor needs a *verified* reversal; a proprietary model can't fill an open-weight role; `hephaestus` stays flagship-native; and a region-locked profile (the Hong Kong-native `ultimate`) rejects any model whose owner is not on that region's allowlist, resolved from a trusted identity table rather than the scan's self-reported vendor. Missing, mislabeled, or ambiguous data fails **closed**, never open.
- **An independent AI reviews the recommendation.** Before anything ships, a separate model (via `review_gate.py`) audits the framework's own output; the verdict must arrive as a **structured JSON field**. Prose verdicts, verdict tokens injected via the scan data, and malformed output all **fail closed to *revise***.
- **Autonomous, but gated by a PR.** A committed weekly **runbook** ([`scripts/landscape/CRON_TASK.md`](scripts/landscape/CRON_TASK.md)) an agent cron executes on your side builds the dataset, runs the framework, passes it through the review gate, and opens a **Pull Request** only when a change is warranted, never a silent push. The scripts and gates ship here; the schedule and the reviewer credential are yours to wire up. A self-test (41 assertions) and a golden-file check run in CI.

> **First run in the wild (Sept 2026):** faced with two brand-new flagships, the engine's recommendation was **hold both**. One was prior-generation parity at ~2.5× the price. The other's clear wins were speed and a stronger vision tier, but no current role is bottlenecked on either. It was also proprietary, and adopting it would have reversed a deliberate earlier decision. Review caught one correction along the way: a leaderboard row that, on check, did not exist for that model. The full write-up lives under [`docs/research/`](docs/research/).

---

## What's in here

```
profiles/
  ultimate.json · hybrid.json · b4b.json     genericized FRAGMENTS (agents + categories)
  *.example.json                             same fragment with REAL provider/model IDs
setup-config.sh · scripts/materialize.py     wrap a fragment into a deployable ~/.omo/omo.jsonc
examples/
  omo.full.example.json                      complete deployable [opencode] config (real IDs)
  dsh-settings.example.yaml                   the harness plugin settings reference
  README.md                                  how the examples fit together
skills/  mm-method · mm-loop · mm-verify · mm-domain     the loop, installable
scripts/landscape/                           the self-governing landscape engine + review gate
install.sh · install.ps1                      copy the loop skills into place
provider-map.local.example                   template for your git-ignored real-ID mapping
docs/  ROUTING.md · PROVIDERS.md · EXAMPLE-MAPPING.md · research/
AGENTS.md · CHANGELOG.md · CONTRIBUTING.md · DOC.md · THIRD_PARTY_NOTICES.md
```

The three `profiles/*.json` are **fragments** (agents + categories only); `setup-config.sh` wraps a chosen one in the required `[opencode]` structure. Each ships a `*.example.json` with real IDs as a concrete mapping reference (exempt from the vendor-name CI check by design). Newest at a glance is always in [`CHANGELOG.md`](CHANGELOG.md). `v1.1.5` reframed the cost cap as an enforced policy knob, added a native-vision fallback, and removed no-op fallback rungs at the mapping level.

---

## Model-agnostic: what that means, exactly

- **Genericized (placeholders):** every provider and model name → `ProviderA…ProviderG` and role-named models like `flagship-xl`, `coder-mid`. You map these to your real models ([`docs/PROVIDERS.md`](docs/PROVIDERS.md)).
- **Kept on purpose (framework identifiers):** where an example targets a specific harness, the identifiers that harness *requires to load* are kept verbatim. For the OpenCode example that is `oh-my-openagent`, `opencode`, the `[opencode]` key and the schema URL; the DeepSeek Harness example keeps its own `settings.yaml` keys. These are harness identifiers, not vendor model names.

The messaging is **open-source and harness-agnostic**. The loop and routing method don't depend on any one harness. Only the concrete *examples* are harness-specific (OpenCode and DSH). CI enforces a real-model-name denylist (`.github/checks.py`); the harness identifiers above are the allowed framework names, and a small documented allowlist covers reference-mapping files and each target harness's own name.

---

## Validation (two gates)

Both run in CI on `main` and every PR, and both exit non-zero on any violation. Run them locally before committing:

```bash
python .github/checks.py                                      # repo-wide release gate
python scripts/validate-full-config.py                        # the deployable example
python scripts/landscape/landscape_scan.py --self-test        # the landscape engine
```

- **`.github/checks.py`**: vendor-name denylist, manifest / skill-presence / profile-schema-shape / local-link checks, duplicate-rung detection (incl. `*.example.*` and `ultrawork`), and the budget-cap placement rule.
- **`scripts/validate-full-config.py`**: 14 hardened deployment invariants (R1–R14); highlights: valid JSON, required `[opencode]` structure present, `reasoning` within the v4.19.4 enum (`off/minimal/low/medium/high/xhigh/max/auto`), per-agent fallback presence, no duplicate/degenerate rungs, `hephaestus` flagship-native-only, `400` excluded from retries, no unused `providerConcurrency`, `momus.disable` not `enabled`, no retired-vendor names, pinned `$schema`, every model ID resolves to a known catalog entry, no cross-vendor mis-routes, and only schema-allowed keys. Several are the same classes `oh-my-openagent doctor` catches. It runs on the comment-free `examples/omo.full.example.json`; to point it at a materialized `omo.jsonc`, strip the `//` header comments first (it parses strict JSON).

---

## Privacy & fallbacks (read before deploying)

Routing forwards work to a **fallback model on a different provider** when the primary fails, so prompts, source, and retrieved context can cross provider (and data-residency) boundaries.

- Treat each fallback provider as a data recipient; only include providers you're contractually comfortable sending context to. For a same-boundary setup, restrict fallbacks to providers under one agreement.
- The default `runtime_fallback` retries only transient errors (`429/503/529`), never `400` (a rejected request isn't an outage).
- **Never** put API keys or secrets in the config or your mapping file. The config holds model IDs only; credentials live in the framework.

---

## Claims & limits

The routing rationale is a set of **design heuristics**, not measured results. You map placeholders to arbitrary real models, so no fixed cost or quality number holds across all mappings. This repo ships **no benchmark data** and makes no quantitative quality/cost guarantee. "Cost-preferenced" means the routing *prefers* cheaper tiers for most roles; it is not an enforced spend cap. **Measure blended cost-per-solved-task on your own mapping.** The landscape engine's job is to keep the *recommendations* honest and current; it is not a promise about your results.

---

## Credits & license

- Loop skills adapted from **[fable-method](https://github.com/Sahir619/fable-method)** by Sahir619 (MIT).
- Engineering gates (grill · prototype · test-first · code-review) adapt concepts from **[mattpocock/skills](https://github.com/mattpocock/skills)** by Matt Pocock.
- Verification fold-ins (machine-checkable evidence, negative tests, false-green defence, reviewer isolation) adapt the **debug-pipeline2** protocol by ronald-ng (MIT).
- Routing layer targets **[oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)** by code-yeongyu.
- Full attribution in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md). MIT licensed; upstream copyright retained in [`LICENSE`](LICENSE), new contributions © bughunt8. See [`CONTRIBUTING.md`](CONTRIBUTING.md).
