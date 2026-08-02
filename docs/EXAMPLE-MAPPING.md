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
| `ProviderD/comm-xl` | `zai-coding-plan/glm-5.2` | Communicator-class orchestrator |
| `ProviderD/comm-lite` | `zai-coding-plan/glm-5-turbo` | Cheap communicator |
| `ProviderC/open-reason-xl` | `deepseek/deepseek-v4-pro` | Open-weight reasoning lifeline |
| `ProviderC/open-reason-lite` | `deepseek/deepseek-v4-flash` | Open-weight fast reasoner |
| `ProviderB/util-pro` | `opencode/gemini-3.1-pro` | Concise planning/writing |
| `ProviderB/util-flash` | `opencode/gemini-3-flash` | Fast utility loop steps |
| `ProviderB/util-misc` | `opencode/big-pickle` | Misc utility backup |
| `ProviderB/retrieval-mid` | `opencode/qwen3.6-plus` | Retrieval / librarian |
| `ProviderB/creative-mid` | `opencode/qwen3.7-plus` | Creative generalist |
| `ProviderB/budget-low` | `opencode/qwen-2.7-plus` | Cheapest general |
| `ProviderB/preview-xl` | `opencode/qwen3.8-max-preview` | Preview model — last-resort backup only |
| `ProviderF/vision-xl` | `minimax/MiniMax-M3` | Native multimodal + long context |

## Notes

- `coder-swarm` appears under two providers because the same model is reachable via both a specialist provider and the general gateway; the profiles use whichever route fits the fallback slot.
- `flagship-prev` (`gpt-5.5`) is retained only as a compatibility/safety fallback rung.
- `preview-xl` is wired strictly as a final fallback (the preview model is unstable and may carry usage-terms limits).
- Provider `apiyi` is a proxy used here because some flagship models are geo-locked; substitute your own gateway.
