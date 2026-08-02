# open-model-method

**A disciplined agent loop + multi-model routing, for any model, any stack.**

Two ideas, fused:

1. **The loop** — a self-contained problem-solving method (think / act / prove / grow) that makes a mid-tier model behave like a careful senior engineer: classify the ask, define done, gather evidence, decide, act surgically, verify by observation, report outcome-first. Adapted from [fable-method](https://github.com/Sahir619/fable-method) (MIT).
2. **The routing** — a config system for the [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) / opencode framework that puts each agent role on the *right model family* instead of one model everywhere. Three profiles: **ultimate**, **hybrid** (default), **b4b**.

> **Core thesis:** the right model in the right role, following a disciplined loop, beats the best single model free-styling. Capability has commoditized; routing and method are the edge.

Everything here is **model-agnostic and vendor-neutral** — all provider/model names are placeholders (`ProviderA`, `flagship-xl`, …). You map them to whatever you run. See [`docs/PROVIDERS.md`](docs/PROVIDERS.md).

---

## What's in here

```
omo.jsonc              # default deployable config (hybrid profile), oh-my-openagent schema
profiles/
  ultimate.json        # max capability, uncapped
  hybrid.json          # DEFAULT: cost-capped except the architect
  b4b.json             # strict cost-capped
skills/                # the loop as installable skills (think/act/prove/grow)
  fable-method/  fable-loop/  fable-judge/  fable-domain/
docs/
  ROUTING.md           # the routing methodology (4 axes, families, roles)
  PROVIDERS.md         # placeholder -> real model mapping guide
AGENTS.md              # portable method for any agent/harness
```

---

## Quickstart — Human

1. **Clone**
   ```bash
   git clone https://github.com/bughunt8/open-model-method
   cd open-model-method
   ```
2. **Pick a profile.** Default is **hybrid** (`omo.jsonc` already holds it). For max capability use `profiles/ultimate.json`; for strict cost control use `profiles/b4b.json`.
3. **Map placeholders to your models.** Open [`docs/PROVIDERS.md`](docs/PROVIDERS.md), decide which real provider/model each `ProviderX/role` maps to, and find-replace them in your chosen config. Keep the mapping file out of git.
4. **Deploy the config.**
   ```bash
   cp omo.jsonc ~/.omo/omo.jsonc     # oh-my-openagent reads ~/.omo/omo.jsonc
   bunx oh-my-openagent doctor        # must report no issues
   ```
5. **Install the loop skills** (optional but recommended):
   ```bash
   bash install.sh                    # or: install.ps1 on Windows
   ```
6. **Use it.** In your agent: `/fable-method <task>` runs the full loop; `/fable-loop <task>` orchestrates plan→execute→verify→audit; `/fable-judge` adversarially verifies finished work.

## Quickstart — LLM / Agent

If you are an LLM setting this up autonomously, follow [`AGENTS.md`](AGENTS.md) for the loop, and this checklist for the config:

1. Read [`docs/ROUTING.md`](docs/ROUTING.md) and [`docs/PROVIDERS.md`](docs/PROVIDERS.md) fully before editing anything.
2. Choose the profile the user asked for; if unspecified, **use `hybrid`** (it is the default).
3. Produce a placeholder→real-model mapping table and show it to the user for approval **before** writing real IDs. Do not invent model IDs from memory — confirm each resolves against the target provider.
4. Apply the mapping to a copy of the chosen profile, wrapped in the deployable `[opencode]` structure (see `omo.jsonc`).
5. Validate: agents use `model` + `fallback_models` (not `models`); `ultrawork` uses singular `model`; categories use `models[]`. Run `oh-my-openagent doctor` and fix every reported key.
6. Report outcome-first per `AGENTS.md` Step 6, listing any placeholder you could not confidently map.

---

## The loop (think / act / prove / grow)

| Phase | Skill | What it does |
|---|---|---|
| **think** | `fable-method` | The problem-solving loop: classify → define done → evidence → decide → act → verify → report |
| **act** | `fable-loop` | Orchestrated plan/execute/verify/audit across subagents |
| **prove** | `fable-judge` | Adversarial verification of finished work + trap suite |
| **grow** | `fable-domain` | Generates domain adapters (marketing, research, data, devops, …) |

Hard bounds baked in: 3 failed verify cycles → stop and hand back; 2 fruitless lookups → stop searching; can't name a verification → ask one pointed question. Full detail in [`AGENTS.md`](AGENTS.md) and `skills/`.

## The routing (profiles)

See [`docs/ROUTING.md`](docs/ROUTING.md) for the full methodology. Summary:

- **Four axes:** capability, cost (incl. verbosity), latency, license+behavior.
- **Family fit beats rank:** each agent role maps to a behavioral family (flagship-native, communicator-class, dual-prompt, multimodal, open-weight, utility).
- **hybrid is default:** cost-capped everywhere except the architect (`oracle`), which gets the flagship for its high leverage.
- **Resilience:** every critical agent keeps a different-provider fallback so one outage never stalls it.

### Profile at a glance

| Role | ultimate | hybrid (default) | b4b |
|---|---|---|---|
| implementer | `flagship-xl` | `flagship-mid` | `flagship-mid` |
| architect (`oracle`) | `flagship-xl` | **`flagship-xl`** | `flagship-mid` |
| reviewer (`momus`) | `flagship-xl` | `flagship-mid` | `flagship-mid` |
| coding tier | `coder-xl` | `coder-mid` (+`coder-xl` fallback) | `coder-mid` |
| orchestration | `comm-xl` | `comm-xl` | `comm-xl` |

---

## Why this exists

Distilled from real multi-model config work: as frontier models converged, "use the best model" stopped being the right question. A model can rank top-4 in the world and still be the wrong default for most agent roles once cost, verbosity, license, and behavior are priced in. This repo encodes that discipline so another human — or another LLM — can reproduce it.

## Credits & license

- The loop skills are adapted from **[fable-method](https://github.com/Sahir619/fable-method)** by Sahir619 (MIT).
- The routing layer targets **[oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)** by code-yeongyu.
- MIT licensed. See [`LICENSE`](LICENSE).

Contributions welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). This repo ships its own review discipline; run `/fable-judge` on your changes before opening a PR.
