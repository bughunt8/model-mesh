# Price reference for the cap check

`scripts/validate-orchestration.py` compares each hybrid and b4b rung with the $4.65 per 1M output cap using the values below. They are conservative list-price references taken on 2026-10-11, not proof of what any account is billed. Where a price rises above a prompt-size threshold, the higher figure is used. The validator rejects a rung with no reference, so a new model needs a verified row here and in the validator before it can enter a capped cell.

| Model | Reference output price per 1M | Source and note |
|---|---|---|
| gpt-5.6-terra | $18 | [OpenCode Zen](https://opencode.ai/docs/zen/): $12 up to 272K, $18 above |
| gpt-5.6-luna | $1.80 | Zen: $1.20 up to 272K, $1.80 above |
| gpt-6.1-sol | $15 | [OpenAI models](https://developers.openai.com/api/docs/models/): $10; Zen shows $15 above 272K |
| gpt-6-astra | $75 | OpenAI: $50; Zen shows $75 above 272K |
| gpt-6-luna | $0.75 | OpenAI: $0.50; Zen shows $0.75 above 272K |
| claude-sonnet-5-5 | $10 | [Anthropic](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) |
| grok-4.7 | $12 | Zen: $6 up to 200K, $12 above |
| deepseek-v4-pro | $3.96 | Repo reference at peak billing; Zen lists $3.48 |
| deepseek-v4-flash | $0.60 | Release page for V4.1 Flash; Zen lists $0.28 for the old ID |
| kimi-k3 | $15 | Zen and repo. Over the cap, so only the exact coding-tier slots may hold it |
| kimi-k2.7-code | $4 | Zen and repo |
| qwen3.8-max | $6 | Zen. Over the cap, so ultimate and global only |
| qwen3.7-plus | $1.60 | Zen |
| qwen3.5-plus | $1.20 | Zen |
| glm-5.3 | $4.40 | [Z.ai pricing](https://docs.z.ai/guides/overview/pricing) |
| glm-5.3-flash | $0.50 | Z.ai pricing |
| minimax-m3 | $1.20 | Zen |

The base hybrid profile still maps its implementer seat to a $12 to $18 model. The orchestration matrix does not repeat that: its hybrid cells use only rungs under the cap, plus kimi-k3 in the exact slots the cap policy already exempts. Whether the base profile should change is a separate decision.
