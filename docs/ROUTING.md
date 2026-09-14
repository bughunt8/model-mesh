# Routing Methodology

> **Harness-agnostic.** This methodology is not tied to any single coding-agent harness. The routing model (roles → families → profiles) applies to any harness that can bind an agent role to a model with fallbacks. The repo ships concrete configuration **examples** for two harnesses (an OpenCode-based setup via oh-my-openagent, and the DeepSeek Harness), but the rules below are the portable part.

The method's **design heuristic** (an opinion, not a benchmarked result): a well-routed set of models, each in the role it fits, can rival one flagship doing everything, at lower cost. As frontier models converge, matching each role to a model on four axes tends to matter more than raw rank. This repo ships no eval data; treat the rationale as a starting hypothesis and measure on your own mapping.

## The four axes

Every placement trades off four things, not one:

1. **Capability.** Benchmark and real-task performance.
2. **Cost.** Blended price *and* verbosity (a wordy model at the same sticker price costs more per solved task).
3. **Latency / throughput.** Tokens/sec matters inside tight agent loops.
4. **License + behavior.** Open-weight vs proprietary, and behavioral family (autonomous vs deferential, verbose vs terse). Behavior decides **prompt-family fit**: an agent's prompt is written for a family, and the wrong family degrades output regardless of raw score.

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
| **hybrid** (default) | Budget cap on generalist/utility/orchestration rungs; flagship **coding** tier + `oracle` + each agent's `ultrawork` escape hatch are exempt | Best value + best-in-class coding/architecture |
| **b4b** | Same budget cap, applied more aggressively (fewer exempt slots) | Strict performance-per-dollar |

### Regional profiles: the Hong Kong-native `ultimate`

`ultimate` is now **Hong Kong-native**: its whole model set is restricted to providers whose developer API is natively reachable from Hong Kong, and it uses **no geo-unlock proxy**. Several US frontier vendors self-restrict developer-API access from that region, so no US-hosted proprietary flagship is available to it. Under that constraint, the flagship-native roles (`hephaestus`, `oracle`, `momus`) cannot be filled by a proprietary US flagship family; they map instead to the **strongest region-reachable open-weight reasoner** (`open-reason-xl`) as their primary tier. This is an **availability-forced family remap, documented, not a silent drop**. The regional profile explicitly waives the flagship-native-family invariant for those seats and substitutes the open-weight reasoning family, because that is the strongest option reachable in the region. The seat is no longer flagship-native under the taxonomy above; the waiver is the point. `hybrid` and `b4b` are **unchanged and remain global**. The concrete region rationale, the excluded vendors, and the placeholder→model table live in [`EXAMPLE-MAPPING.md`](EXAMPLE-MAPPING.md) (which is denylist-exempt and may name real models).

Hybrid is the default because it spends over-cap budget only where it has the highest leverage, the read-only architect (`oracle`) and the flagship **coding** tier (`coder-xl`) on the agents/categories that do the hardest implementation (`prometheus`, `atlas`, `deep`, `ultrabrain`), while holding generalist, utility, and orchestration roles at or under the [policy budget cap](PROVIDERS.md#rules-that-survive-any-mapping) ($4.65/1M output in the example mapping). The cap is a *preference for the cheap tiers*, not a hard ceiling on every slot; `docs/EXAMPLE-MAPPING.md` lists which mapped models sit above it and why. Whether the trade is worth it depends on the models you map in, so measure it.

## Standing rules

1. **Family fit beats raw rank.** Never place a model outside its behavioral family's roles.
2. **Keep a non-primary-provider lifeline.** Each *critical agent*, defined here as `hephaestus`, `oracle`, `momus`, and `sisyphus`, has at least one fallback on a different provider, so one outage never fully stalls it. (Utility agents may stay single-provider.)
3. **Reserve the top tier for the ceiling roles.** `ultra`/max-effort settings belong to the hardest reasoning only; they are the biggest token multiplier.
4. **Preview/experimental models are last-resort fallbacks only.**
5. **Fallback order = priority.** In each `fallback_models` list, earlier = tried first.
6. **A frontier launch triggers a role-fit review, not a wholesale swap.** Measure blended cost-per-solved-task, not benchmark rank.

## Fallback ordering under a proxy

If your flagship provider is a single proxy (a common geo-lock pattern), all flagship rungs share one point of failure. Put an **open-weight, different-provider model** early enough in the chain that a proxy outage reaches a working model quickly. In this repo, `open-reason-xl` (ProviderC) is that lifeline on the flagship-native agents.
