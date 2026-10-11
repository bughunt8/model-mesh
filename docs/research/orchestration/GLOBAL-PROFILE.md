# Global profile evidence

`global` is the unrestricted twin of `ultimate`. It has no region limit and no budget cap, and it follows the same discipline as the landscape engine: independent evidence first, vendor claims labelled, judgement labelled as judgement. The landscape scorer was not extended to a fourth profile in this package, so no score or verdict was produced. The table below is a manual evidence sheet, and extending the scorer is an open follow-up.

Files: [profiles/global.json](../../../profiles/global.json) holds placeholders. [profiles/global.example.json](../../../profiles/global.example.json) holds real IDs.

## Seats and evidence

Artificial Analysis Intelligence Index and per-task cost come from [its model leaderboard](https://artificialanalysis.ai/leaderboards/models), fetched 2026-10-11 with no page date shown. The index is general intelligence, not coding. Output prices are vendor list prices checked against the vendor documentation on the same day.

| Placeholder | Real ID | Seat | Intelligence Index | Output price per 1M | Note |
|---|---|---|---|---|---|
| `flagship-mid` | gpt-6.1-sol | Default author for implementer, architect fallback | 52 | $10 | Judgement: the best index-per-dollar of the top tier |
| `flagship-xl` | gpt-6-astra | Ultrawork and oracle primary | 53 | $50 | Judgement: five times the price for one more index point, so only the escalation slots use it |
| `flagship-lite` | gpt-6-luna | Quick and junior seats | 38 | $0.50 | |
| `premium-comm` | claude-sonnet-5-5 | Orchestrator | 56 | $10 | Opus 5.5 scores 58 at $20 and stays an optional escalation, not the default |
| `div-flagship` | grok-4.7 | Independent reviewer | 46 | $6 under 200k prompt | Chosen because its family differs from every author family |
| `coder-xl` | kimi-k3 | Third rung for author chains | 44 | repo price | Inherited from `ultimate` |
| `flagship-open` | qwen3.8-max | General author in the Alibaba pool | 45 | repo price | Inherited from `ultimate` |
| `open-reason-xl` | deepseek-v4-pro | Second reviewer rung | 36 | repo price | Inherited from `ultimate`; low index, kept for family diversity |
| `vision-xl` | MiniMax-M3 | Multimodal looker | 29 | repo price | Inherited from `ultimate` |

## Decisions that need the owner's eyes

- Gemini is not used. The repository retired Gemini in v1.1.1 and nothing here reverses that. Two council members placed Gemini rungs in global cells, and one named Gemini 4 Argon, which has no public model ID. All were dropped.
- Orchestrator choice trades price against fit. Claude Opus 5.5 scores two index points higher than Sonnet 5.5 at twice the price, so Sonnet is the default.
- The index leader, Claude Opus 5.5, is absent from author chains on purpose. Independence needs the reviewer pool and the orchestrator pool to avoid author families, and spreading the top models across three disjoint pools beats stacking them in one.
- ID checks: model IDs were confirmed from vendor documentation or the OpenCode Zen listing on 2026-10-11. GPT 6.1 Luna does not exist, so GPT 6 Luna is used.

## Media models

The owner also named Seedance 2.5, Wan 3, Kling Video v3 and GPT Image 2.5 Sunburst. They generate video and images and do not take coding seats. They are out of scope for this matrix. A future media-generation note can cover them.
