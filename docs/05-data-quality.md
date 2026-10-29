# 05 — Data Quality and Caveats

## 5.1 Hermes Index is the anchor, but not the whole story

The Hermes Index is the only benchmark in this report that runs models **inside a
real agent harness with files, follow-ups, and state grading**. That makes it the
closest proxy to OMO's workload. Three limitations:

- It averages four suites, which can hide a profile-specific inversion. GLM-5.3's
  Hermes 39.23 masks a TB4 38.1 vs Skills 45.6 inversion that matters enormously
  for contract profiles.
- It is cost-inclusive, correct for chain design but not for single-seat
  evaluation. Opus 5.5's $4.99/task is a strength for Oracle and a weakness for
  Explore.
- It is one harness. A model that loops in OpenCode may not loop in Hermes.

## 5.2 The SkillsBench discrepancy

Two independent sources report different DeepSeek V4.1 Flash SkillsBench scores:

| Source | Score | Harness |
|---|---:|---|
| Hermes | 56.5 | Hermes agent loop |
| Vals AI | 69.80 | OpenHands |

The 13-point gap is harness-dependent. This report uses the **conservative Hermes
number** for the agentic composite and flags the Vals number where it affects a
chain decision. Re-run both harnesses before changing a head.

## 5.3 Reasoning-tier validity

| Model | Tiers supported | Config uses | Risk |
|---|---|---|---|
| Gemini 4 Argon | low / medium / high | `high` | Valid |
| Gemini 3.7 Flash | low / medium / high | `high` (after fix) | Valid |
| GPT-6 Astra | low / medium / high / xhigh / max | `medium`, `high` | Valid |
| Kimi K3 | low / high / max | `low`, `max` | Valid |
| GLM-5.3 | low / high / max | `max` | Valid |
| DeepSeek Flash | none / low / high / max | `off`, `max` | `off` maps to `none` |

The risk is not the tier names; it is **relay-level silent mapping**. A provider
that does not recognize `xhigh` may silently serve `high`, which means a chain
configured for the ceiling runs one tier below it. Verify with
`bunx oh-my-openagent doctor --verbose`.

## 5.4 Benchmark noise

DeepSWE v1.1 run-to-run variation is **1.4 to 3.2 points**, and the top four
models sit within **0.55 points of each other**. A 0.2-point lead is not a
finding. OMO-Benchmark therefore uses **grade bands**, not rank order, for any
comparison inside the noise floor.

## 5.5 Provider-verification gaps

| Provider / model | Issue |
|---|---|
| `packyapi/gpt-6.1-sol` | Historical function-calling pass rate 7–20%; model consistency 41.7% |
| `packyapi/claude-*` | Thinking-signature pass rate 31%; model-identity 39% |
| `packyapi/gemini-4-argon` | Not present in indexed PackyAPI Gemini listings |
| `tokeness/deepseek-v4.1-flash` | No canonical ID; Tokeness lists `deepseek-v4-flash` |
| `tokeness/MiniMax-M3` | Tokeness catalog does not include MiniMax |
| `zai-coding-plan/glm-5.3-flashx` | FlashX is not available on the Coding Plan |

## 5.6 What this report cannot tell you

- Whether Kimi K3's tool-call repeat bug reproduces on Tokeness routing
- Whether `tokeness/gemini-4-argon` serves the real Argon or a downgraded variant
  (its effective price of $0.60/$3.00 is well below Google's $2/$10)
- Whether the `no-hephaestus-non-gpt` hook fires on a **fallback** rung as opposed
  to a primary
- Whether PackyAPI's function-calling failures have been remediated since the
  snapshot

Each of these requires a live verification call, not a benchmark lookup.
