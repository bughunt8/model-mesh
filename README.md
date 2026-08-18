# model-mesh

**A disciplined agent loop + multi-model routing, for any model, any stack.**

Two ideas, fused:

1. **The loop** — a self-contained problem-solving method (think / act / prove / grow) that guides a model to work like a careful senior engineer: classify the ask, define done, gather evidence, decide, act surgically, verify by observation, report outcome-first. Adapted from [fable-method](https://github.com/Sahir619/fable-method) (MIT) — see [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
2. **The routing** — a config system for the [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) / opencode framework that assigns each agent role to a model *family* instead of using one model everywhere. Three profiles: **ultimate**, **hybrid** (default), **b4b**.

> **Design heuristic (not a proven benchmark):** the right model in the right role, following a disciplined loop, tends to beat one model free-styling. These are design opinions, not measured guarantees — see [Claims & limits](#claims--limits).

> **What's new in v1.1.2:** added a token-efficient open-weight coder (`open-coder`, mapped to MiMo) as a coding/open fallback rung across **all three** profiles — in the `deep` category everywhere, on `atlas`/`sisyphus-junior` open backups, and in `b4b`'s `unspecified-low`. Also fixed pre-existing duplicate fallback rungs and added a CI guard so duplicate rungs and invalid model IDs now fail the build. See [`CHANGELOG.md`](CHANGELOG.md).
>
> **What's new in v1.1.1 (Aug 2026 model refresh):** the open-weight reasoning lifeline (`open-reason-xl`) moved to its new GA build (API ID unchanged); the communicator (`comm-xl`) upgraded to its newest release across all profiles; a now-GA frontier open flagship (`flagship-open`) and an independent 5th-vendor diversification fallback (`div-flagship`, `ProviderG`) were added to **ultimate only** (both exceed the cost cap); the previous utility-vendor family was retired and replaced role-aware by `gen-pro` / `gen-flash`. Concrete IDs, prices, and citations are in [`docs/EXAMPLE-MAPPING.md`](docs/EXAMPLE-MAPPING.md); full detail in [`CHANGELOG.md`](CHANGELOG.md).

## What's genericized vs kept

This repo is **model-agnostic**. To be explicit about what that means:

- **Genericized (placeholders):** every provider and model name → `ProviderA…ProviderG` and role-named models like `flagship-xl`, `coder-mid`. You map these to your real models. See [`docs/PROVIDERS.md`](docs/PROVIDERS.md).
- **Kept (real framework names, on purpose):** `oh-my-openagent`, `opencode`, the `[opencode]` config key, and the schema URL. These are the actual framework identifiers the config **must** contain to load. They are not vendor model names; keeping them is what makes the config deployable.

CI enforces a denylist of real model/provider names (`.github/checks.py`); `oh-my-openagent` and `opencode` are the only allowed framework names.

---

## What's in here

```
profiles/
  ultimate.json        # max capability, uncapped        (FRAGMENT: agents+categories)
  hybrid.json          # DEFAULT                          (FRAGMENT)
  b4b.json             # cost-preferenced                 (FRAGMENT)
setup-config.sh        # materializes a profile into a full deployable ~/.omo/omo.jsonc
scripts/materialize.py # wraps a fragment in the [opencode] structure
skills/                # the loop as installable skills
  mm-method/  mm-loop/  mm-verify/  mm-domain/
docs/
  ROUTING.md           # routing methodology (4 axes, families, roles)
  PROVIDERS.md         # placeholder -> real model mapping guide + framework compat
AGENTS.md              # portable method + routing runbook for any agent
THIRD_PARTY_NOTICES.md # upstream attribution
```

Each profile also ships a `*.example.json` (e.g. `profiles/hybrid.example.json`) showing the same fragment populated with **real provider/model IDs** as a concrete reference mapping. The plain `*.json` files stay genericized; the `*.example.json` files are illustrative and are exempt from the vendor-name CI check by design.

The three `profiles/*.json` are **fragments** (agents + categories only). `setup-config.sh` wraps a chosen fragment in the required `[opencode]` structure to produce a complete, deployable config.

---

## Quickstart — Human

1. **Clone**
   ```bash
   git clone https://github.com/bughunt8/model-mesh
   cd model-mesh
   ```
2. **Materialize a profile** (default is hybrid):
   ```bash
   ./setup-config.sh hybrid      # or: ultimate | b4b
   ```
   This backs up any existing `~/.omo/omo.jsonc`, then writes the selected profile as a complete config. It does **not** invent model IDs.
3. **Map placeholders to your models.** Open the written `~/.omo/omo.jsonc` and [`docs/PROVIDERS.md`](docs/PROVIDERS.md); replace each `ProviderX/role-name` with a real provider/model you have confirmed exists. Put your mapping in `provider-map.local` (git-ignored) — never commit it.
4. **Validate.**
   ```bash
   bunx oh-my-openagent doctor    # must report no issues
   ```
5. **Install the loop skills** (optional):
   ```bash
   bash install.sh                # or install.ps1 on Windows (backs up existing skills)
   ```
6. **Use it:** `/mm-method <task>` runs the full loop; `/mm-loop <task>` orchestrates plan→execute→verify→audit; `/mm-verify` adversarially reviews finished work.

Rollback anytime: `cp ~/.omo/omo.jsonc.bak-<stamp> ~/.omo/omo.jsonc`.

## Quickstart — LLM / Agent

Follow [`AGENTS.md`](AGENTS.md) (Part A is the routing runbook, Part B is the loop). In short:

1. Read [`docs/ROUTING.md`](docs/ROUTING.md) and [`docs/PROVIDERS.md`](docs/PROVIDERS.md) fully first.
2. Use `hybrid` unless the user specified otherwise.
3. Produce a placeholder→real-model mapping table and get user approval **before** writing real IDs. Never invent model IDs from memory — confirm each resolves.
4. Run `./setup-config.sh <profile>`, then apply the mapping to `~/.omo/omo.jsonc`.
5. Enforce the schema: agents use `model` + `fallback_models` (not `models`); `ultrawork` uses singular `model`; categories use `models[]`; use `reasoning` not `variant`. Run `oh-my-openagent doctor` until clean.
6. Report outcome-first (AGENTS.md Step 6); list any placeholder you could not confidently map.

---

## The loop (think / act / prove / grow)

| Phase | Skill | What it does |
|---|---|---|
| **think** | `mm-method` | classify → define done → evidence → decide → act → verify → report |
| **act** | `mm-loop` | orchestrated plan/execute/verify/audit across subagents |
| **prove** | `mm-verify` | adversarial verification of finished work |
| **grow** | `mm-domain` | generates domain adapters (marketing, research, data, devops, …) |

Hard bounds: 3 failed verify cycles → stop and hand back; 2 fruitless lookups → stop searching; can't name a verification → ask one pointed question. Full detail in [`AGENTS.md`](AGENTS.md) and `skills/`.

## The routing (profiles)

See [`docs/ROUTING.md`](docs/ROUTING.md). Each agent role maps to a behavioral **family** (flagship-native, communicator-class, dual-prompt, multimodal, open-weight, utility); family fit is the routing rule, not raw benchmark rank.

### Profile at a glance (primary model per role, from the actual JSON)

| Role | ultimate | hybrid (default) | b4b |
|---|---|---|---|
| implementer (`hephaestus`) | `flagship-xl` | `flagship-mid` | `flagship-mid` |
| architect (`oracle`) | `flagship-xl` | **`flagship-xl`** | `flagship-mid` |
| reviewer (`momus`) | `flagship-xl` | `flagship-mid` | `flagship-mid` |
| coding agents (`atlas`, `prometheus`) | `coder-xl` | `coder-xl` | `coder-mid` |
| `deep` category | `coder-xl` | `coder-mid` | `coder-mid` |
| orchestration (`sisyphus`) | `comm-xl` | `comm-xl` | `comm-xl` |

Hybrid's distinguishing choice: it keeps the flagship only for the **architect** (`oracle`), the highest-leverage advisory role, while dropping the implementer/reviewer to the mid tier.

Ultimate-only (v1.1.1): the coding agents (`atlas`, `prometheus`) carry two extra over-cap fallback rungs — `flagship-open` (GA frontier open flagship) and `div-flagship` (independent 5th-vendor diversification, `ProviderG`) — for resilience when the primaries rate-limit. `hephaestus` deliberately keeps a flagship-native-only fallback chain. See [`docs/PROVIDERS.md`](docs/PROVIDERS.md) and [`docs/EXAMPLE-MAPPING.md`](docs/EXAMPLE-MAPPING.md).

Open-coder fallback (v1.1.2): `open-coder` (a token-efficient open-weight coder, mapped to MiMo) is wired as a coding/open fallback rung in the `deep` category of **all three** profiles, on the `atlas` and `sisyphus-junior` open backups, and — most heavily — in the cost-preferenced `b4b` profile's `unspecified-low`. It is chosen for token efficiency, which is what a resilience rung should optimize for, rather than as a primary. Duplicate fallback rungs are now rejected by CI in the genericized profiles.

---

## Validation

Two checks guard this repo; both run in CI on every push and PR, and both exit non-zero on any violation so you can run them locally before committing.

```bash
python .github/checks.py                     # repo-wide gate
python scripts/validate-full-config.py       # full deployable config example
python scripts/validate-full-config.py path/to/your-omo.jsonc   # validate your own config
```

- **`.github/checks.py`** — the release gate: a vendor-name denylist (genericized files must use placeholders; `*.example.json` and `docs/EXAMPLE-MAPPING.md` are exempt by design), plus manifest, skill-presence, profile-schema-shape, and local-link checks.
- **`scripts/validate-full-config.py`** — validates [`examples/omo.full.example.json`](examples/omo.full.example.json) (or any config path you pass) against the hardened deployment invariants: valid JSON, `reasoning` within enum, every agent has a non-empty `fallback_models`, no duplicate or degenerate fallback rungs (a fallback must differ from the primary), `hephaestus` stays flagship-native-only (its `ultrawork` may be cross-family by design), `runtime_fallback.retry_on_errors` excludes `400` (a rejected request is not a transient outage), no unused `providerConcurrency` entries, `momus` uses `enabled` (not `disable`), no retired-vendor names, a pinned `$schema` tag, every model ID resolves to a known catalog entry (`opencode/*` must be a published Zen model; Zen-exclusive codenames are rejected under a relay/native prefix), and no known cross-vendor mis-route (a first-party model under the wrong native vendor prefix; relay/aggregator prefixes are exempt because a relay may legitimately mirror many vendors).

Point the second command at your own materialized `~/.omo/omo.jsonc` to catch the same classes of mistakes before you deploy.

---

## Privacy & fallbacks (read before deploying)

Routing forwards work to a **fallback model on a different provider** when the primary fails. That means prompts, source code, and retrieved context can cross provider (and possibly data-residency) boundaries. Before deploying:

- Treat each fallback provider as a data recipient; only include providers you are contractually comfortable sending your context to.
- If you need a same-boundary setup, restrict fallbacks to providers under the same agreement.
- The default `runtime_fallback` retries only transient errors (`429/503/529`). It deliberately does **not** retry `400` (a rejected/malformed request is not an outage).
- Never put API keys or secrets in the config or in your mapping file. The config holds model IDs only; credentials are configured in the framework, not here.

## Claims & limits

The routing rationale in this repo is a set of **design heuristics**, not measured results. Because you map placeholders to arbitrary real models, no fixed cost or quality number can hold across all mappings. This repo ships **no benchmark data** and makes no quantitative quality/cost guarantee. Where the docs say a profile is "cost-preferenced," that means the routing *prefers* cheaper tiers for most roles — it is not an enforced spend cap. Measure blended cost-per-solved-task on your own mapping.

## Credits & license

- Loop skills adapted from **[fable-method](https://github.com/Sahir619/fable-method)** by Sahir619 (MIT).
- The four engineering gates (grill, prototype, test-first, code-review) adapt concepts from **[matt-pocock/skills](https://github.com/mattpocock/skills)** by Matt Pocock.
- The verification fold-ins (machine-checkable evidence, negative tests, false-green defence, reviewer isolation) adapt concepts from the **debug-pipeline2** protocol by ronald-ng (MIT).
- Routing layer targets **[oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)** by code-yeongyu.
- Full attribution in [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md).
- MIT licensed. Upstream copyright retained in [`LICENSE`](LICENSE); new contributions © bughunt8. See [`CONTRIBUTING.md`](CONTRIBUTING.md).
