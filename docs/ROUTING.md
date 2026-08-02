# Routing Methodology

The method's **design heuristic** (an opinion, not a benchmarked result): a well-routed set of models, each in the role it fits, can rival one flagship doing everything, at lower cost. As frontier models converge, matching each role to a model on four axes tends to matter more than raw rank. This repo ships no eval data; treat the rationale as a starting hypothesis and measure on your own mapping.

## The four axes

Every placement trades off four things, not one:

1. **Capability** — benchmark and real-task performance.
2. **Cost** — blended price *and* verbosity (a wordy model at the same sticker price costs more per solved task).
3. **Latency / throughput** — tokens/sec matters inside tight agent loops.
4. **License + behavior** — open-weight vs proprietary, and behavioral family (autonomous vs deferential, verbose vs terse). Behavior decides **prompt-family fit**: an agent's prompt is written for a family, and the wrong family degrades output regardless of raw score.

Leaderboard rank collapses all four into one number and hides the decision that matters.

## Behavioral families

Each agent role is written for one family. Map your real models to the family, not the benchmark.

| Family | Character | Roles it drives |
|---|---|---|
| **Flagship-native** | Principle-driven, autonomous, steerable | implementer, architect, reviewer |
| **Communicator-class** | a flagship model-like orchestration, delegation | orchestrators |
| **Dual-prompt** | a flagship model-preferred, coding-optimized | coding tier |
| **Multimodal / long-context** | Native vision, huge context | the "looker" |
| **Open-weight reasoning** | Independent provider, non-proxy | escalation lifelines |
| **Utility** | Fast, terse, cheap | loop steps, retrieval |

## Agent roles (generic)

| Role | Job | Family | Notes |
|---|---|---|---|
| `hephaestus` | Primary implementer | flagship-native | Owns the codebase; delegates + reviews |
| `oracle` | Read-only architect | flagship-native | Deep reasoning; must not seize initiative |
| `momus` | Adversarial reviewer | flagship-native | Terse, low-initiative, strict |
| `sisyphus` | Top orchestrator | communicator-class | Delegates to implementer; parallelizes |
| `sisyphus-junior` | Sub-executor | utility (inherits) | Light; inherits category routing |
| `atlas` | Coding worker | dual-prompt | Autonomy + coding is an asset |
| `prometheus` | Planner | dual-prompt | Plan/execute/verify |
| `metis` | Gap analyzer | communicator-class | Non-zero temperature |
| `librarian` | Retrieval | utility | Fast, cheap |
| `explore` | Search/grep | utility | Cheapest viable |
| `multimodal-looker` | Vision + long context | multimodal | Native vision required |

## The three profiles

| Profile | Cost policy | When |
|---|---|---|
| **ultimate** | Uncapped, flagship-first | Max capability, cost secondary |
| **hybrid** (default) | Cost-capped except `oracle` | Best value + best-in-class architect |
| **b4b** | Cost-capped everywhere | Strict performance-per-dollar |

Hybrid is the default because it spends flagship budget only where it has the highest leverage (the architect), while dropping other roles to the mid tier. Whether that trade is worth it for you depends on the models you map in — measure it.

## Standing rules

1. **Family fit beats raw rank.** Never place a model outside its behavioral family's roles.
2. **Keep a non-primary-provider lifeline.** Each *critical agent* — defined here as `hephaestus`, `oracle`, `momus`, and `sisyphus` — has at least one fallback on a different provider, so one outage never fully stalls it. (Utility agents may stay single-provider.)
3. **Reserve the top tier for the ceiling roles.** `ultra`/max-effort settings belong to the hardest reasoning only — they are the biggest token multiplier.
4. **Preview/experimental models are last-resort fallbacks only.**
5. **Fallback order = priority.** In each `fallback_models` list, earlier = tried first.
6. **A frontier launch triggers a role-fit review, not a wholesale swap.** Measure blended cost-per-solved-task, not benchmark rank.

## Fallback ordering under a proxy

If your flagship provider is a single proxy (a common geo-lock pattern), all flagship rungs share one point of failure. Put an **open-weight, different-provider model** early enough in the chain that a proxy outage reaches a working model quickly. In this repo, `open-reason-xl` (ProviderC) is that lifeline on the flagship-native agents.
