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
| `reasoner-breadth` | Breadth reasoning leader | Optional high-ceiling reasoning fallback |
| `coder-xl` | Flagship coding model | Dual-prompt coding tier (capability-first) |
| `coder-mid` | Coding workhorse | Everyday code-gen/review (cost-sane) |
| `coder-swarm` | Long-context coding, swarm-capable | Large low-risk subagent swarms |
| `comm-xl` | Communicator-class orchestrator | Orchestration roles (sisyphus, metis) |
| `comm-lite` | Cheap communicator | Fast orchestration / utility |
| `open-reason-xl` | Open-weight reasoning, SOTA | Non-proxy escalation lifeline |
| `open-reason-lite` | Open-weight fast reasoner | Latency-sensitive subtasks |
| `util-pro` | Concise utility/reasoning | Planning, writing, visual-engineering |
| `util-flash` | Fast utility | Low-latency loop steps |
| `util-misc` | Misc utility | Backup rung |
| `retrieval-mid` | Retrieval/librarian | Fast retrieval role |
| `creative-mid` | Creative generalist | Artistry role |
| `budget-low` | Cheapest general | unspecified-low |
| `preview-xl` | Preview/experimental model | Last-resort backup only (see caveats) |
| `vision-xl` | Native multimodal + long context | multimodal-looker primary |

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
3. **Preview/experimental models stay last-resort.** `preview-xl` is a final fallback only.
