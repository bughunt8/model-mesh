
---

## `docs/02-model-scorecard.md`

```markdown
# 02 — Model Scorecard

Scores 0–100 per dimension. Bold = best in roster for that dimension.
Snapshot: 2026-10-18. Machine-readable copy: `data/model-scores.csv`.

| Model | AE | TO | IP | R | CR | VD | LC | REL | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Claude Opus 5.5** | 95 | 88 | **90** | **100** | 85 | 78 | 30 | 85 | Hermes #1; Skills 69.6; $4.99/task |
| **GPT-6.1 Sol** | 88 | 82 | 80 | 88 | 80 | 62 | 80 | **92** | Hermes #2; $1.19/task; best value |
| **GPT-6 Astra** | 75 | 80 | 78 | 92 | 85 | 65 | 25 | 70 | Highest reasoning ceiling; $11.61/task; asks clarifying questions |
| **Claude Sonnet 5.5** | 65 | 78 | 85 | 82 | **90** | 72 | 55 | 75 | Skills 66.9; IF regressed -7.1 vs Sonnet 5 |
| **GPT-6 Sol** | 55 | 75 | 80 | 70 | 75 | 55 | 70 | 82 | DeepSWE 68.8; Skills 60.5 |
| **GLM-5.3** | 72 | 70 | **45** | 75 | 75 | 60 | 65 | **30** | TB4 37.9 vs Skills 45.6 — 7.5-pt inversion; plan-adherence failure |
| **Kimi K3** | 45 | **95** | 70 | 80 | 80 | 50 | 45 | 60 | MCP Atlas 84.2; TB4 12.6; tool-call repeat bug |
| **Kimi K2.7 Code** | 50 | 88 | 75 | 65 | 65 | 40 | 60 | 80 | MCP Atlas 76.0; MCP Mark 81.1; 30% less overthinking |
| **DeepSeek V4.1 Flash-1017** | 80 | 68 | 78 | 70 | 75 | 55 | **100** | 65 | TB4 42.3, DeepSWE 77.0, $0.26/task; parser drift risk |
| **MiniMax M3** | 65 | 75 | 65 | 60 | 75 | **88** | 70 | 75 | OmniDocBench 91.6; 24h/1,959 calls |
| **Qwen3.8-Max** | 50 | 60 | 70 | 65 | 70 | 75 | 30 | 55 | Skills 70.2; TB4 17.5; $6.69/task |
| **Claude Haiku 5.5** | 55 | 60 | 75 | 55 | 70 | 60 | 95 | 75 | TB4 39.2; $0.488/task |
| **GLM-5.3 Flash** | 60 | 80 | 50 | 55 | 60 | 50 | 90 | 45 | Toolathlon 78.4; $0.497/task |
| **GPT-6 Luna** | 25 | 50 | 65 | 45 | 60 | 40 | **100** | 70 | TB4 6.3; $0.141/task |
| **Gemini 4 Argon** | 82 | 75 | 70 | 88 | **95** | 80 | 45 | 75 | TB4 57.4; DeepSWE 77.9; 1M context |
| **MiMo-V2.6-Pro** | 55 | 70 | 50 | 65 | 90 | 60 | 80 | 35 | 1M context; tool-call repetition (MOPD-mitigated) |

## Dimension leaders

| Dimension | Leader | Why |
|---|---|---|
| AE | Claude Opus 5.5 (95) | TB4 59.6 at xhigh; strongest terminal ceiling |
| TO | Kimi K3 (95) | MCP Atlas 84.2, the highest measured tool-orchestration score |
| IP | Claude Opus 5.5 (90) | SkillsBench 69.6; best procedure execution |
| R | Claude Opus 5.5 (100) | AA Intelligence Index 58 at max; #1 of 212 models |
| CR | Gemini 4 Argon (95) | 1M unified context with AA-LCR 80% |
| VD | MiniMax M3 (88) | OmniDocBench 91.6; native video (VideoMME 85.4) |
| LC | DeepSeek Flash / GPT-6 Luna (100) | $0.26 and $0.141 per task respectively |
| REL | GPT-6.1 Sol (92) | Instruction following 74.2; no documented loop defect |

## Reading the table

- **A model can be excellent and still lose a seat.** Kimi K3 leads TO but scores
  AE 45; it belongs in Atlas and Explore, never in a terminal-heavy head slot.
- **The GLM inversion is the single most important row.** IP 45 with AE 72 means
  it can act but cannot follow instructions. Every contract-bearing seat must
  subtract 15.
- **Two models tie at LC 100.** GPT-6 Luna is cheaper per token; DeepSeek Flash
  is far stronger at AE. LC alone never decides a seat.
