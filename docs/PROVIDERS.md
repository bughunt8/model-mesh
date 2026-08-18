# Provider & Model Placeholders

This repo is model-agnostic and vendor-neutral. Every config uses **generic placeholders** instead of real provider or model names, so the method survives model churn and reads cleanly for any stack.

You map placeholders to whatever you actually run. The **roles** are what matter; the specific models are yours to choose.

## Provider placeholders

| Placeholder | Role in the stack | What you map it to |
|---|---|---|
| `ProviderA` | Flagship gateway (often a proxy for geo-locked or premium models) | Your primary paid/frontier provider |
| `ProviderB` | General-purpose gateway (utility, vision, misc models) | Your broad model gateway |
| `ProviderC` | Open-weight reasoning provider | Your open-weight reasoning host |
| `ProviderD` | Communicator-class / subscription provider | Your orchestration-model subscription |
| `ProviderE` | Coding-specialist family provider | Your coding-model provider |
| `ProviderF` | Multimodal / long-context provider | Your vision/long-context provider |

## Model placeholders (named by ROLE, not vendor)

| Placeholder | Role / tier | Typical use |
|---|---|---|
| `flagship-xl` | Top flagship reasoner | Hardest reasoning, architecture (uncapped profile) |
| `flagship-mid` | Value flagship | Everyday flagship work; the cost-capped workhorse |
| `flagship-lite` | Cheap flagship | Fast, low-cost flagship tier |
| `flagship-prev` | Previous-gen flagship | Compatibility / safety fallback rung |
| `reasoner-xl` | Cross-family deep reasoner | Architecture advisory (dual-prompt / oracle fallback) |
| `coder-xl` | Flagship coding model | Dual-prompt coding tier (capability-first) |
| `coder-mid` | Coding workhorse | Everyday code-gen/review (cost-sane) |
| `coder-swarm` | Long-context coding, swarm-capable | Large low-risk subagent swarms |
| `comm-xl` | Communicator-class orchestrator | Orchestration roles (sisyphus, metis) |
| `comm-lite` | Cheap communicator | Fast orchestration / utility |
| `open-reason-xl` | Open-weight reasoning, SOTA | Non-proxy escalation lifeline |
| `open-reason-lite` | Open-weight fast reasoner | Latency-sensitive subtasks |
| `gen-pro` | Concise generalist | Planning, writing, visual-engineering |
| `gen-flash` | Fast utility | Low-latency loop steps |
| `util-misc` | Misc utility | Backup rung |
| `open-coder` | Token-efficient open-weight coder | Coding/open fallback rung (`deep`, coder agents) |
| `retrieval-mid` | Retrieval/librarian | Fast retrieval role |
| `creative-mid` | Creative generalist | Artistry role |
| `budget-low` | Cheapest general | unspecified-low |
| `flagship-open` | GA frontier-class open flagship | Ultimate-only rung (cost > cap) |
| `vision-xl` | Native multimodal + long context | multimodal-looker primary |
| `div-flagship` | Independent 5th-vendor diversification | Ultimate-only fallback (atlas/prometheus) |

## How to map (example)

Create a private mapping file (never committed) that translates placeholders to your real IDs, e.g.:

```
ProviderA/flagship-xl   -> <your-provider>/<your-flagship-model>
ProviderC/open-reason-xl -> <your-open-weight-provider>/<your-open-weight-model>
```

Then either (a) hand-edit the config's model strings, or (b) run a find/replace with your mapping before deploying. Keep the mapping out of version control.

## Rules that survive any mapping

1. **Family fit beats raw rank.** Map each role to a model whose behavioral family matches (see `docs/ROUTING.md`).
2. **Keep a non-flagship lifeline.** At least one fallback per critical agent should be a different provider than the primary, so a single provider outage does not stall the agent.
3. **Cost-capped profiles honor the cap.** Models whose per-token cost exceeds the cap (`flagship-open`, `div-flagship`) appear in `ultimate` only; `hybrid`/`b4b` stay under the coder-xl cap. See `docs/EXAMPLE-MAPPING.md` for the concrete IDs and prices.


## Worked example

For a complete filled-in reference (every placeholder → a real ID, matching `profiles/*.example.json`), see [`EXAMPLE-MAPPING.md`](EXAMPLE-MAPPING.md). Your own mapping will differ.

## Mapping file (keep it private)

Put your placeholder→real-model mapping in a file named exactly **`provider-map.local`** at the repo root. It is git-ignored by default. Do **not** name it `provider-map.json` or anything without `.local`, or it may be committed. A safe starter is provided as `provider-map.local.example`.

Rules for the mapping file:
- Model IDs only. **Never** put API keys, tokens, or secrets in it — credentials belong in the framework's own auth, not here.
- Even model IDs can reveal your vendors and account topology, so treat the file as sensitive.

## Framework compatibility

- Target framework: **oh-my-openagent** (opencode). These names are kept intentionally (see README "What's genericized vs kept").
- The generated config pins the schema to a released tag (`v4.19.4`) for reproducibility rather than a mutable `dev` branch. If you run a different framework version, update the `$schema` line and re-run `oh-my-openagent doctor`.
- Schema shape enforced: agents use `model` + `fallback_models`; `ultrawork` uses a singular `model`; categories use a `models` array; use `reasoning` (not the deprecated `variant`).
