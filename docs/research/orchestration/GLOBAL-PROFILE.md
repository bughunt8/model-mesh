# Global profile evidence

`global` is the unrestricted twin of `ultimate`. It has no region limit and no budget cap, and it follows the same discipline as the landscape engine: independent evidence first, vendor claims labelled, judgement labelled as judgement. The landscape scorer was not extended to a fourth profile in this package, so no score or verdict was produced. The table below is a manual evidence sheet, and extending the scorer is an open follow-up.

Files: [profiles/global.json](../../../profiles/global.json) holds placeholders. [profiles/global.example.json](../../../profiles/global.example.json) holds real IDs.

## Seats and evidence

Artificial Analysis Intelligence Index values come from [its model leaderboard](https://artificialanalysis.ai/leaderboards/models), fetched 2026-10-11 with no page date shown, at the effort setting named in each row. The index measures general intelligence, not coding. Output prices come from [OpenAI](https://developers.openai.com/api/docs/models/), [Anthropic](https://platform.claude.com/docs/en/models/sonnet-5-5/overview) and the [OpenCode Zen price list](https://opencode.ai/docs/zen/), fetched the same day. Prices above 272K or 200K prompt tokens are higher, so the validator uses the higher figure.

| Placeholder | Real ID | Seat | Intelligence Index (effort) | Output price per 1M | Note |
|---|---|---|---|---|---|
| `flagship-mid` | gpt-6.1-sol | Default author for implementer, architect fallback | 51 (xhigh; no max setting listed) | $10, $15 above 272K | Judgement: the best index-per-dollar of the top tier |
| `flagship-xl` | gpt-6-astra | Ultrawork and oracle primary | 53 (max) | $50, $75 above 272K | Judgement: five times the price for two more index points, so only the escalation slots use it |
| `flagship-lite` | gpt-6-luna | Quick and junior seats | 38 (earlier fetch, effort not recorded) | $0.50, $0.75 above 272K | |
| `premium-comm` | claude-sonnet-5-5 | Orchestrator | 56 (max) | $10 | Opus 5.5 scores 58 (max) at $20 and stays an optional escalation, not the default |
| `div-flagship` | grok-4.7 | Independent reviewer | 46 (xhigh) | $6, $12 above 200K | Chosen because its family differs from every author family |
| `coder-xl` | kimi-k3 | Author fallback in the base global profile; not in matrix chains | 44 (max) | $15 | Inherited from `ultimate` |
| `flagship-open` | qwen3.8-max | General author in the Alibaba pool | 45 (0902 build) | $6 | Inherited from `ultimate` |
| `open-reason-xl` | deepseek-v4-pro | Second reviewer rung | 36 (0813 build, max) | $3.48 on Zen, $3.96 in the repo reference | Inherited from `ultimate`; low index, kept for family diversity |
| `vision-xl` | MiniMax-M3 | Multimodal looker | 29 | $1.20 | Inherited from `ultimate` |

## Decisions that need the owner's eyes

- Gemini is not used. The repository retired Gemini in v1.1.1 and nothing here reverses that. Two council members placed Gemini rungs in global cells, and one named Gemini 4 Argon, which has no public model ID. All were dropped.
- Orchestrator choice trades price against fit. Claude Opus 5.5 scores two index points higher than Sonnet 5.5 at twice the price, so Sonnet is the default.
- The index leader, Claude Opus 5.5, is absent from author chains on purpose. Independence needs the reviewer pool and the orchestrator pool to avoid author families, and spreading the top models across three disjoint pools beats stacking them in one.
- ID checks: model IDs were confirmed from vendor documentation or the OpenCode Zen listing on 2026-10-11. GPT 6.1 Luna does not exist, so GPT 6 Luna is used.

## Media models

The owner also named Seedance 2.5, Wan 3, Kling Video v3 and GPT Image 2.5 Sunburst. They generate video and images and do not take coding seats. They are out of scope for this matrix. A future media-generation note can cover them.
