# 03 — Agent Profiles

Eleven agent profiles, each scored on its own dimension weights. `Fit` is the
weighted score before the CXR penalty; `Weighted` is `Fit * slot_weight`.

---

## 3.1 Hephaestus

**Core focus:** deep execution, GPT family, long-running, tool-heavy, LSP/AST/CodeGraph.
**Constraint:** GPT-native. Non-GPT models are blocked by the `no-hephaestus-non-gpt`
hook unless `allow_non_gpt_model: true` is set, which produces a warning toast
but no redirect.
**Weights:** AE 40%, TO 20%, IP 15%, REL 15%, LC 10%.

| Slot | Model | AE | TO | IP | REL | LC | Fit | Weighted |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| ultrawork | `gpt-6.1-sol` high | 88 | 82 | 80 | 92 | 80 | 84.4 | 42.2 |
| 1 | `gpt-6-sol` high | 55 | 75 | 80 | 82 | 70 | 69.6 | 17.4 |
| 2 | `gpt-6-astra` medium | 75 | 80 | 78 | 70 | 25 | 70.4 | 17.6 |
| 3 | `packyapi/gpt-6.1-sol` high | 88 | 82 | 80 | 70 | 80 | 82.0 | 6.6 |
| 4 | `gemini-4-argon` high | 82 | 75 | 70 | 75 | 45 | 73.4 | 3.7 |

**Chain score: 87.5 → Grade A-**

**Verdict.** The head is correct. The weakness is slot 2: `gpt-6-astra` at medium
costs $11.61/task and scores TB4 41.3, below Sol's 50.8, while scoring higher on
reasoning. For a terminal-heavy agent that is the wrong trade.

**Action.** Promote `gpt-6-sol` to slot 1 to match the documented chain. Move
`gpt-6-astra` to slot 2 at `low` effort. Keep Argon last with the flag set.

---

## 3.2 Oracle

**Core focus:** reasoning ceiling, GPT-native, read-only consultation, three-layer
response with strict redundancy control.
**Weights:** R 40%, AE 20%, IP 15%, REL 15%, LC 10%.

| Slot | Model | R | AE | IP | REL | LC | Fit | Weighted |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `gpt-6.1-sol` high | 88 | 88 | 80 | 92 | 80 | 86.4 | 43.2 |
| 2 | `gemini-4-argon` high | 88 | 82 | 70 | 75 | 45 | 76.7 | 19.2 |
| 3 | `packyapi/gpt-6.1-sol` high | 88 | 88 | 80 | 70 | 80 | 83.4 | 10.0 |
| 4 | `gpt-6-astra` high | 92 | 75 | 78 | 70 | 25 | 76.6 | 6.1 |
| 5 | `deepseek-v4-pro` max | 75 | 65 | 65 | 65 | 60 | 68.8 | 3.4 |

**Chain score: 81.9 → Grade A-**

**Verdict.** Best-constructed chain in the config. It follows the documented
order: GPT head, then Gemini, then Claude-adjacent, then DeepSeek floor. The only
structural issue is the packyapi duplicate at slot 3, which is the same model at
the same effort as slot 1 — provider failover, not a second opinion. PackyAPI's
Sol endpoint has historically shown 7–20% function-calling pass rates.

**Action.** Replace slot 3 with `tokeness/claude-opus-5-5` at `high` for lineage
diversity. Opus 5.5's R score (100) exceeds Sol's (88).

---

## 3.3 Prometheus

**Core focus:** procedural adherence, long-context synthesis, writing quality,
multi-turn state. Terminal execution is irrelevant.
**Weights:** IP 30%, R 25%, CR 20%, REL 15%, LC 10%.

| Slot | Model | IP | R | CR | REL | LC | Fit | Weighted |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `gpt-6.1-sol` high | 80 | 88 | 80 | 92 | 80 | 84.4 | 42.2 |
| 2 | `claude-sonnet-5-5` high | 85 | 82 | 90 | 75 | 55 | 81.6 | 20.4 |
| 3 | `packyapi/claude-sonnet-5-5` high | 85 | 82 | 90 | 70 | 55 | 80.6 | 9.7 |
| 4 | `packyapi/gemini-4-argon` high | 70 | 88 | 95 | 75 | 45 | 76.8 | 6.1 |
| 5 | `deepseek-v4-pro` max | 65 | 75 | 70 | 65 | 60 | 68.8 | 3.4 |

**Chain score: 81.8 → Grade A-**

**Verdict.** The head is a deliberate trade. Sol has the highest measured
instruction following in the roster (74.2), which is what a seven-step gated
workflow depends on. Sonnet 5.5 has the highest context utilization and
SkillsBench 66.9, but carries a -7.1 instruction-following regression versus
Sonnet 5 and a documented "skipped workflows" behaviour that persists at xhigh.

Slot 4 is dead: `packyapi/gemini-4-argon` is unverified. PackyAPI's indexed
Gemini listings show 3.5, 3.6, and 3-flash-preview, not 4-Argon.

**Action.** Keep Sol head. Replace the packyapi duplicate with
`tokeness/claude-opus-5-5` for diversity. Fix the Argon provider to
`tokeness/gemini-4-argon`.

---

## 3.4 Metis

**Core focus:** reasoning depth, instruction-following to a rigid checklist,
reliability under long multi-turn prompts.
**Weights:** R 30%, IP 30%, REL 20%, CR 10%, LC 10%.

| Slot | Model | R | IP | REL | CR | LC | Fit | Weighted |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `claude-opus-5-5` high | 100 | 90 | 85 | 85 | 30 | 86.0 | 43.0 |
| 2 | `gpt-6.1-sol` high | 88 | 80 | 92 | 80 | 80 | 84.4 | 21.1 |
| 3 | `packyapi/claude-sonnet-5-5` high | 82 | 85 | 70 | 90 | 55 | 79.4 | 9.5 |
| 4 | `kimi-k3` low | 80 | 70 | 60 | 80 | 45 | 70.5 | 5.6 |
| 5 | `deepseek-v4-pro` max | 75 | 65 | 65 | 70 | 60 | 68.8 | 3.4 |

**Chain score: 82.6 → Grade A-**

**Verdict.** Correctly leads with Opus 5.5 at high, matching the documented Metis
default and capturing the highest reasoning score in the roster. High is correct:
Metis runs once or twice per plan, so per-task cost is trivial relative to
catching a blocker.

The packyapi duplicate at slot 3 is the weak link: PackyAPI's Claude path has
shown 31% thinking-signature pass rate and 39% model-identity consistency.

**Action.** Replace slot 3 with `tokeness/claude-sonnet-5-5` at `high` for clean
provenance within the Claude family, or `tokeness/gemini-4-argon` at `high` for
genuine family diversity. Kimi K3 at `low` is the documented second opinion and
should stay.

---

## 3.5 Momus

**Core focus:** tool reliability, instruction adherence to a rigid output
contract, reasoning depth for structural review.
**Weights:** TO 30%, IP 30%, R 15%, REL 15%, LC 10%. **CXR penalty: -15.**
**Contract:** standalone `PLAN_APPROVED` or `PLAN_REJECTED` on its own line, no
prose before it.

| Slot | Model | TO | IP | R | REL | LC | Fit | Weighted | CXR |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `gpt-6.1-sol` high | 82 | 80 | 88 | 92 | 80 | 84.4 | 42.2 | 0 |
| 2 | `gemini-4-argon` high | 75 | 70 | 88 | 75 | 45 | 76.5 | 19.1 | 0 |
| 3 | `packyapi/gpt-6.1-sol` high | 82 | 80 | 88 | 70 | 80 | 82.4 | 9.9 | -1.5 |
| 4 | `deepseek-v4-pro` max | 65 | 65 | 75 | 65 | 60 | 67.0 | 3.4 | -1.0 |

**Chain score: 72.1 → Grade B**

**Verdict.** Head is correct: Sol is the documented Momus head and has the
highest instruction-following score in the roster. Grade is dragged down by the
absence of a Claude rung (Opus 5.5 has the highest Toolathlon score, 80.6%) and
by the packyapi duplicate consuming a slot without adding diversity.

Correctly sets `temperature: 0.1` and a read-only tool surface.

**Action.** Replace slot 3 with `tokeness/claude-opus-5-5` at `high`. Keep
DeepSeek V4 Pro as the floor; GPQA Diamond 90.1% makes it a credible reasoning
backstop.

---

## 3.6 Atlas

**Core focus:** tool orchestration, instruction-following to a todo ledger,
long-context state management, reliability across many turns.
**Weights:** TO 35%, IP 25%, AE 15%, REL 15%, LC 10%.

| Slot | Model | TO | IP | AE | REL | LC | Fit | Weighted |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `kimi-k3` | 95 | 70 | 45 | 60 | 45 | 70.5 | 35.3 |
| 2 | `claude-sonnet-5-5` high | 78 | 85 | 65 | 75 | 55 | 75.4 | 18.9 |
| 3 | `deepseek-flash` | 68 | 78 | 80 | 65 | 100 | 75.6 | 9.1 |
| 4 | `packyapi/gpt-6.1-sol` medium | 82 | 80 | 88 | 70 | 80 | 81.0 | 6.5 |
| 5 | `glm-5.3-flash` 0.1 | 80 | 50 | 60 | 45 | 90 | 62.8 | 3.1 |

**Chain score: 72.9 → Grade B**

**Verdict.** Kimi K3's MCP Atlas 84.2 is the highest in the roster, which makes
it a defensible head on tool orchestration alone. But K3's TB4 12.6 is the lowest
of any non-trivial model, and its documented tool-call repeat bug (re-issuing
the same `Read` six times in 14 turns) is the exact failure a todo orchestrator
cannot tolerate. `glm-5.3-flash` has SkillsBench 42.6 — the lowest in the roster.

`temperature: 0.1` is set per-entry on slots 2, 4, and 5 but not at the agent
level; slots 1 and 3 inherit provider defaults.

**Action.** Promote `claude-sonnet-5-5` to slot 1 (SkillsBench 66.9, 1M context,
native Claude path for Atlas's dual-prompt design). Move Kimi K3 to slot 2.
Replace `glm-5.3-flash` with `tokeness/claude-haiku-5-5` at `low`.

---

## 3.7 Sisyphus-Junior

**Core focus:** agentic execution, instruction-following to a scope contract,
cost efficiency, absence of loop behaviour.
**Weights:** AE 40%, IP 20%, LC 20%, REL 15%, TO 5%. **CXR penalty: -15.**
**Contract:** `STATUS: DONE|BLOCKED|NEEDS_ESCALATION` plus `CHANGED`, `VERIFIED`,
`ASSUMPTIONS`, `ESCALATION` fields, at most 12 lines.

| Slot | Model | AE | IP | LC | REL | TO | Fit | Weighted | CXR |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `deepseek-flash` | 80 | 78 | 100 | 65 | 68 | 81.0 | 32.4 | 0 |
| 2 | `tokeness/deepseek-v4.1-flash` | 80 | 78 | 100 | 65 | 68 | 81.0 | 16.2 | 0 |
| 3 | `packyapi/gpt-6.1-sol` medium | 88 | 80 | 80 | 70 | 82 | 83.6 | 10.0 | -1.8 |
| 4 | `minimax/M3` | 65 | 65 | 70 | 75 | 75 | 67.0 | 5.4 | 0 |
| 5 | `glm-5.3-flash` | 60 | 50 | 90 | 45 | 80 | 58.0 | 2.9 | -0.8 |
| 6 | `packyapi/claude-haiku-5-5` | 55 | 75 | 95 | 75 | 60 | 66.0 | 3.3 | 0 |

**Chain score: 65.4 → Grade B-**

**Verdict.** Best value per task in the config. DeepSeek Flash at $0.26/task
with TB4 42.3 and DeepSWE 77.0 is the Pareto winner for bounded execution.

Two entries are broken. `tokeness/deepseek-v4.1-flash` has no canonical ID — the
official name is `deepseek-flash`, and Tokeness has historically listed
`deepseek-v4-flash`. `glm-5.3-flash` at slot 5 carries the -15 CXR penalty for
documented instruction collapse, the exact failure the `STATUS:` token exists
to catch.

**Action.** Fix the slot 2 ID. Replace `glm-5.3-flash` with
`tokeness/gpt-6-luna-fast` at `low`. Keep Haiku 5.5 as the Claude-family floor.

---

## 3.8 Sisyphus

**Core focus:** tool orchestration across many turns, agentic execution,
reliability (absence of loop), instruction-following to the operating contract.
**Weights:** TO 30%, AE 25%, REL 20%, IP 15%, LC 10%.

| Slot | Model | TO | AE | REL | IP | LC | Fit | Weighted |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| primary | `deepseek-flash` | 68 | 80 | 65 | 78 | 100 | 75.4 | 37.7 |
| ultrawork | `minimax/M3` max | 75 | 65 | 75 | 65 | 70 | 70.5 | 17.6 |
| 1 | `tokeness/MiniMax-M3` | 75 | 65 | 75 | 65 | 70 | 70.5 | 8.5 |
| 2 | `kimi-k2.7-code` | 88 | 50 | 80 | 75 | 60 | 73.6 | 5.9 |
| 3 | `packyapi/kimi-k2.7-code` | 88 | 50 | 80 | 75 | 60 | 73.6 | 3.7 |
| 4 | `deepseek-v4-pro` max | 65 | 65 | 65 | 65 | 60 | 64.5 | 3.2 |

**Chain score: 76.6 → Grade B+**

**Verdict.** A deliberate experimental chain. DeepSeek Flash's LC 100 combined
with AE 80 makes it rational for a user who has empirically validated it on long
loops. MiniMax M3 is the strongest long-loop evidence in the roster: 1,959 tool
calls over 24 hours with zero intervention.

Two structural defects. The config has **two `prompt_append` keys**; the second
(short) one wins in JSON, discarding the entire operating contract. And
`tokeness/MiniMax-M3` is a provider mismatch — Tokeness's catalog does not
include MiniMax.

**Action.** Delete the duplicate `prompt_append` (correctness bug, not tuning).
Replace `tokeness/MiniMax-M3` with `minimax/MiniMax-M3`. Consider adding
`tokeness/kimi-k3` at `low` as a supported-list third opinion.

---

## 3.9 Librarian

**Core focus:** long-context retrieval, instruction-following to a citation
contract, cost, speed.
**Weights:** CR 35%, IP 25%, LC 25%, R 10%, REL 5%.
**Documented default:** Gemini 3 Flash at temperature 0.1.

| Slot | Model | CR | IP | LC | R | REL | Fit | Weighted |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `deepseek-flash` | 75 | 78 | 100 | 70 | 65 | 79.8 | 39.9 |
| 2 | `gemini-3-flash` | 85 | 70 | 85 | 70 | 75 | 80.0 | 20.0 |
| 3 | `packyapi/deepseek-flash` | 75 | 78 | 100 | 70 | 65 | 79.8 | 9.6 |
| 4 | `opencode/minimax-m2.5-free` | 60 | 60 | 100 | 50 | 50 | 68.5 | 3.4 |

**Chain score: 72.9 → Grade B**

**Verdict.** The head is correct but not the documented default. DeepSeek Flash
is cheaper and now has native image input (Chartography 83.0 w/tools, BabyVision
92.5), which makes it a legitimate alternative — but its CR score of 75 is below
Gemini 3 Flash's 85 on retrieval. `temperature: 0.1` is correctly set at the
agent level.

**Action.** Swap slots 1 and 2: `gemini-3-flash` first for retrieval quality,
`deepseek-flash` second for cost. The free MiniMax M2.5 rung is capped at 20 RPM
and roughly 100 requests/day; keep it last and treat it as best-effort.

---

## 3.10 Explore

**Core focus:** latency and cost above all, tool-call parallelism,
instruction-following to a structured output contract.
**Weights:** CR 20%, IP 20%, LC 30%, TO 20%, AE 10%. **CXR penalty: -10.**
**Contract:** `<analysis>` and `<results>` blocks, absolute paths with `file:line`,
at least 3 tools in the first action.

| Slot | Model | CR | IP | LC | TO | AE | Fit | Weighted | CXR |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `kimi-k2.7-code-highspeed` off | 65 | 75 | 85 | 88 | 50 | 72.3 | 36.2 | 0 |
| 2 | `deepseek-flash` max | 75 | 78 | 100 | 68 | 80 | 78.4 | 19.6 | 0 |
| 3 | `tokeness/deepseek-flash` max | 75 | 78 | 100 | 68 | 80 | 78.4 | 9.4 | 0 |
| 4 | `packyapi/gemini-3.7-flash` high | 85 | 70 | 95 | 75 | 82 | 80.7 | 6.5 | 0 |
| 5 | `zai-coding-plan/glm-5.3-flashx` | 60 | 50 | 90 | 80 | 60 | 62.0 | 3.1 | -0.5 |

**Chain score: 74.3 → Grade B**

**Verdict.** Head is correct: Kimi K2.7 Code HighSpeed is the fastest
tool-reliability specialist in the roster (~180 tok/s, MCP Atlas 76.0, MCP Mark
81.1), and `reasoning: "off"` matches the documented head.

Two entries are wrong. `packyapi/gemini-3.7-flash` is unverified on PackyAPI's
catalog, and `max` is not a valid reasoning level for Gemini 3.7 Flash (it
supports low/medium/high only). `zai-coding-plan/glm-5.3-flashx` is not available
on the Coding Plan — only `glm-5.3-flash` is.

**Action.** Replace slot 4 with `tokeness/gemini-3.7-flash` at `high` (340 tok/s,
~8 parallel tool calls per turn). Replace slot 5 with
`zai-coding-plan/glm-5.3-flash` at `off`.

---

## 3.11 Multimodal-Looker

**Core focus:** vision/document fidelity above all, instruction-following to an
observation/inference contract.
**Weights:** VD 50%, IP 20%, R 10%, LC 10%, REL 10%. **CXR penalty: -10.**
**Contract:** Observation separated from Inference; every observation carries a
page/slide/region locator; `NOT_PRESENT` / `ILLEGIBLE` / `CROPPED` /
`LOW_CONFIDENCE` classification.

| Slot | Model | VD | IP | R | LC | REL | Fit | Weighted | CXR |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `gemini-3-flash` | 88 | 70 | 70 | 85 | 75 | 81.0 | 40.5 | 0 |
| 2 | `minimax/M3` | 88 | 65 | 60 | 70 | 75 | 78.3 | 19.6 | 0 |
| 3 | `glm-5.3-flash` | 50 | 50 | 55 | 90 | 45 | 55.5 | 6.7 | -1.0 |
| 4 | `opencode/kimi-k2.5-free` | 55 | 65 | 50 | 100 | 60 | 62.3 | 3.1 | 0 |

**Chain score: 68.9 → Grade B-**

**Verdict.** Top two slots are excellent. Gemini 3 Flash has OmniDocBench 90.1,
IDP Core 80.5, OCR 91.1 — the strongest published document-parsing numbers in
the roster. MiniMax M3 has OmniDocBench 91.6, MMMU-Pro 78.1, and native video
(VideoMME 85.4).

The chain is too short for a hard vision gate. Vision is a binary capability: a
model without it cannot run the agent at all. `glm-5.3-flash` at slot 3 has no
published OCR or table evidence.

**Action.** Insert `deepseek/deepseek-flash` at slot 3 (native image input,
improved chart reading, $0.26/task). Move GLM to slot 4 or drop it.

