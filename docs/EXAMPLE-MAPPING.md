<!-- example-mapping: contains real provider/model IDs by design; exempt from the vendor denylist like profiles/*.example.json -->
# Example Mapping (placeholder → real ID)

This is the concrete reference mapping used by the `profiles/*.example.json` files. It shows one real-world way to fill in the placeholders. **Your mapping will differ** — use this only as a worked example, and keep your own mapping in a git-ignored `provider-map.local` (see [`PROVIDERS.md`](PROVIDERS.md)).

> These are illustrative IDs for a specific stack (including a proxy provider for geo-locked flagship models). They are not recommendations, and availability/pricing change frequently.

## Provider placeholders

| Placeholder | Real provider |
|---|---|
| `ProviderA` | `apiyi` (proxy for geo-locked flagship / premium models) |
| `ProviderB` | `opencode` (general gateway) |
| `ProviderC` | `deepseek` (open-weight reasoning) |
| `ProviderD` | `zai-coding-plan` (communicator-class subscription) |
| `ProviderE` | `moonshotai` (coding-specialist family) |
| `ProviderF` | `minimax` (multimodal / long-context) |
| `ProviderG` | `xai` (independent 5th-vendor diversification) |

## Model placeholders

| Placeholder | Real model ID | Role |
|---|---|---|
| `ProviderA/flagship-xl` | `apiyi/gpt-5.6-sol` | Top flagship reasoner |
| `ProviderA/flagship-mid` | `apiyi/gpt-5.6-terra` | Value flagship workhorse |
| `ProviderA/flagship-lite` | `apiyi/gpt-5.6-luna` | Cheap flagship tier |
| `ProviderA/flagship-prev` | `apiyi/gpt-5.5` | Previous-gen safety rung |
| `ProviderA/reasoner-xl` | `apiyi/claude-opus-5` | Cross-family deep reasoner |
| `ProviderE/coder-xl` | `moonshotai/kimi-k3` | Flagship coding model |
| `ProviderE/coder-mid` | `moonshotai/kimi-k2.7-code` | Coding workhorse |
| `ProviderE/coder-swarm` | `moonshotai/kimi-k2.6` | Long-context / swarm coding |
| `ProviderB/coder-swarm` | `opencode/kimi-k2.6` | Same model via the general gateway (alt route) |
| `ProviderD/comm-xl` | `zai-coding-plan/glm-5.3` | Communicator-class orchestrator |
| `ProviderD/comm-lite` | `zai-coding-plan/glm-5-turbo` | Cheap communicator |
| `ProviderC/open-reason-xl` | `deepseek/deepseek-v4-pro` | Open-weight reasoning lifeline (GA 0813 build; ID unchanged) |
| `ProviderC/open-reason-lite` | `deepseek/deepseek-v4-flash` | Open-weight fast reasoner |
| `ProviderB/gen-pro` | `opencode/qwen3.7-plus` | Concise planning/writing generalist (replaces retired gemini-3.1-pro) |
| `ProviderB/gen-flash` | `deepseek/deepseek-v4-flash` | Fast utility loop steps (replaces retired gemini-3-flash) |
| `ProviderB/util-misc` | `opencode/big-pickle` | Misc utility backup (Zen-exclusive experimental model) |
| `ProviderB/open-coder` | `opencode/mimo-v2.5-free` | Token-efficient open-weight coder (MiMo) — coding/open fallback rung |
| `ProviderB/retrieval-mid` | `opencode/qwen3.6-plus` | Retrieval / librarian |
| `ProviderB/creative-mid` | `opencode/qwen3.7-plus` | Creative generalist |
| `ProviderB/budget-low` | `opencode/qwen-2.7-plus` | Cheapest general |
| `ProviderB/flagship-open` | `opencode/qwen3.8-max` | GA frontier-class open flagship — ultimate only (cost > cap) |
| `ProviderF/vision-xl` | `minimax/MiniMax-M3` | Native multimodal + long context |
| `ProviderG/div-flagship` | `xai/grok-4.6` | Diversification fallback — ultimate only (cost > cap) |

## Notes

- `coder-swarm` appears under two providers because the same model is reachable via both a specialist provider and the general gateway; the profiles use whichever route fits the fallback slot.
- `flagship-prev` (`gpt-5.5`) is retained only as a compatibility/safety fallback rung.
- `flagship-open` (`qwen3.8-max`) is the **GA production** release (ID `qwen3.8-max`, replacing the former `qwen3.8-max-preview` last-resort rung). It is [frontier-class on agentic work](https://rits.shanghai.nyu.edu/ai/qwen3-8-max-draws-level-with-the-frontier-on-agentic-benchmarks/) but priced at [$2 in / $6 out per 1M](https://aireiter.com/blog/qwen3-8-max-api-pricing); the $6 output rate exceeds the kimi-k3 cost cap ($4.65), so it is used in `ultimate` only. `hybrid`/`b4b` now use `gen-pro` (`qwen3.7-plus`) in the slots the preview previously occupied.
- `comm-xl` migrated `glm-5.2 → glm-5.3` in all three profiles. GLM-5.3 is a [post-training upgrade on the same base](https://www.marktechpost.com/2026/08/14/z-ai-ships-glm-5-3-without-retraining-the-base-model-better-at-complex-coding-and-long-horizon-tasks/) with large agentic-coding gains ([Terminal-Bench 2.1 81.0 → 88.2, DeepSWE 46.2 → 66.9](https://aq.dev/guides/glm-5-3-for-coding-agents/)). **Assumption: GLM-5.3 pricing is unchanged from GLM-5.2** — it ships on the same subscription/Coding-Plan tier ([per-token price not yet published](https://atoms.dev/blog/glm-5-3-benchmarks-api-coding-open-weights)), so `ProviderD` remains a subscription and the per-token cost cap does not gate it.
- `open-reason-xl` (`deepseek/deepseek-v4-pro`) now resolves to the [GA **0813** build](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) — the [API ID is unchanged](https://openllmstack.com/models/deepseek-v4-pro-0813/), so no edit was needed. Note DeepSeek [moved the V4 family to peak/off-peak billing on 2026-08-16](https://ofox.ai/blog/deepseek-v4-pro-0813-price-weights-benchmarks-api-access-2026/) (peak $1.32/$3.96, off-peak $0.66/$1.98 per 1M) — still under the cap.
- **All Gemini models were retired** (both `gemini-3.1-pro` and `gemini-3-flash`). Role-aware replacements: the planning/writing/visual/artistry role (`gen-pro`) → `qwen3.7-plus`; the fast utility-loop role (`gen-flash`) → `deepseek-v4-flash`. In the high-stakes fallback slots on `oracle`/`momus`/`prometheus` where the retired model was a *capability safety rung*, it was promoted to the strongest model not already in that chain (`deepseek-v4-pro`, else `glm-5.3`, else `gpt-5.6-terra`) rather than a flat generalist swap.
- `grok-flagship` (`xai/grok-4.6`) is an **ultimate-only** diversification fallback on `atlas` and `prometheus` — **not** `hephaestus` (which stays GPT-native-only). Grok trails the stack's primaries on role-relevant benchmarks ([Terminal-Bench 2.1 83.3 vs kimi-k3 88.3 / deepseek-0813 87.9 / glm-5.3 88.2](https://www.tldevtech.com/grok-45-benchmarked-where-it-actually-wins)) but adds an independent 5th vendor (xAI) and is very token-efficient ([~16k output tok/task vs Opus 4.8's ~67k](https://hokai.io/hub/models/grok-4.5)). Priced [$2/$6 per 1M](https://benchlm.ai/xai/api-pricing) — the $6 output exceeds the kimi-k3 cap ($4.65), hence ultimate only.
- `open-coder` (`opencode/mimo-v2.5-free`) is Xiaomi's MiMo, a [1T-param open-weight MoE coder that matches frontier coding benchmarks at 40-60% fewer tokens](https://codersera.com/blog/xiaomi-mimo-v2-5-coding-model-2026/) (MIT). It is wired as a coding/open fallback rung in `deep` (all profiles), on `atlas`/`sisyphus-junior` open backups, and in `b4b`'s cost-preferenced `unspecified-low` — chosen for token efficiency, exactly what a resilience rung should optimize for. The full deployable example (`examples/omo.full.example.json`) uses `mimo-v2.5-pro` via the tokeness relay instead of the Zen `-free` tier.
- Provider `apiyi` is a proxy used here because some flagship models are geo-locked; substitute your own gateway.
