# Model Assessment — GPT-6 Astra & Gemini 3.8 Flash (September 2026)

Reusable reference for model-mesh routing decisions. Captures the full authoritative
benchmark survey for two frontier releases, with **vendor-reported vs independent**
provenance flagged throughout, so later refreshes can re-assess against a fixed record.

- **Compiled:** 2026-09-04
- **Scope:** GPT-6 Astra (OpenAI), Gemini 3.8 Flash (Google). Context notes on same-week releases (Muse Spark 1.3, Claude Fable 5.1 / Mythos 5.1).
- **Reading rule:** vendor launch tables are self-computed marketing documents (each lab runs its own harness and picks competitor numbers). Treat only clearly independent lines as cross-comparable. A DeepSWE/HLE gap under ~2 points is within run-to-run noise.
- **Authoritative independent sources** (co-equal, cross-comparable): the **Artificial Analysis** leaderboard/model pages ([artificialanalysis.ai/leaderboards/models](https://artificialanalysis.ai/leaderboards/models)), the **Datacurve DeepSWE** leaderboard, and the **Vellum LLM leaderboard** ([vellum.ai/llm-leaderboard](https://www.vellum.ai/llm-leaderboard)) are treated as the primary authorities here. Secondary independents: **Vals.ai**, **CMU ExploitBench**, **Irregular FrontierCyber**. Everything else in §3–§4 is vendor-reported unless marked **[I]**.
- **Price-baseline note:** all GPT-5.6 Sol comparisons use its **current** published price ($4 in / $20 out standard), set when [OpenAI cut Sol pricing on 2026-08-21](https://openai.com/api/pricing/). Vellum still shows the pre-cut $30 output; that figure is stale, not a genuine disagreement — so the "2.5× Astra vs Sol" multiplier below is exact ($50 ÷ $20 = 2.5×; AA blended $7.70 ÷ $3.08 = 2.5×), and AA states it verbatim.[cite:31]

### Authoritative independent snapshot (Artificial Analysis, Intelligence Index v4.1.1, 2026-09-04)

| Model (effort) | AA Intelligence Index | Output $/1M | Blended $/1M | Output speed (tok/s) |
|---|---:|---:|---:|---:|
| Claude Fable 5.1 | **66** | $50.00 | $7.17 | 66.4 |
| Claude Opus 5 | ~63 | — | — | — |
| Muse Spark 1.3 (`max`, partner-preview, no API provider) | **62** | — | — | — |
| **GPT-6 Astra (`max`)** | **61** | $50.00 | $7.70 | N/A |
| GPT-5.6 Sol | **61** | $20.00 | $3.08 | 76.5 |
| Grok 4.6 (`high`) — already mapped `div-flagship` | **61** | $6.00 | — | — |
| Muse Spark 1.3 (`xhigh`, GA) | **61** | — | — | — |
| GLM-5.3 (`max`) — already mapped `comm-xl` | **60** | $4.40 | — | — |
| Kimi K3 — already mapped `coder-xl` | **60** | $15.00 | — | — |
| **Gemini 3.8 Flash (`high`)** | **59** | $3.75 | **$0.58** | **326.9** |

AA is the single most decision-relevant table here, and it reframes both models:
- **GPT-6 Astra (61) ties the model it replaces, GPT-5.6 Sol (61), at exactly 2.5× Sol's current output price**, and is beaten by Fable 5.1 (66) — which lists at the *same* $10/$50 as Astra ([Vellum](https://www.vellum.ai/llm-leaderboard)). Astra also merely ties Grok 4.6 and Muse Spark 1.3 (`xhigh`), both already at 61.[cite:15][cite:18][cite:31]
- **Gemini 3.8 Flash (59) is near-frontier intelligence at ~1/13 the blended cost and ~4× the output speed** of the flagships — but note it does **not** beat the repo's *existing under-cap* placeholders on intelligence: GLM-5.3 (`comm-xl`) scores **60** at $4.40 and Kimi K3 (`coder-xl`) **60**. Gemini's real edge is speed/blended-cost/vision, not the intelligence index.[cite:25][cite:28][cite:32][cite:33]

### Cross-check — Vellum LLM leaderboard (mixed vendor/independent feed, 2026-09-04)

**Provenance caveat:** Vellum's board is a **mixed feed** — its own note says data "comes from model providers as well as independently run evaluations." Its GPT-6 Astra rows are attributed in Vellum's launch article to **OpenAI's announcement table**, so most Astra numbers here are the *same vendor figures* as §3, not an independent re-run. Vellum **does not yet track Gemini 3.8 Flash**. Treat this as corroboration of *positioning*, not as an independent measurement.[cite:30][cite:34]

| Category (Vellum board) | GPT-6 Astra | Rank on that board | Provenance | Leader / context |
|---|---:|---:|---|---|
| GPQA Diamond (reasoning) | 96% | #2 | [V] (OpenAI table) | Sonnet 5 96.2 |
| BrowseComp (browsing) | 91.5% | **#2** | [V] | Sol 92.2 leads — Astra trails the model it replaces |
| AutoBench / AutomationBench | 41.4% | #2 | [V] | GLM-5.3-Flash leads at 48.8 |
| Humanity's Last Exam | 57.2% | #7 | [V] | Fable 5.1 / Mythos 5.1 tie at 65; **Sol #14 at 47.2** |
| SWE-bench Verified (coding) | *not listed* | — | — | Sol 96.2 leads; Astra absent |
| OSWorld / computer use | *Astra not on Vellum's board* | — | — | Vellum's computer-use board: Fable 5 85 (#1), Opus 4.8 83.4, Sonnet 5 81.2 |

**Corrected reading:** Astra is **not** the OSWorld leader on Vellum — it does not appear on that board at all; the only computer-use numbers for Astra are **vendor-reported** (OpenAI's OSWorld 2.0 72.6 vs Sol 65.7; ScreenSpot-Pro 92.7), with the one independent corroboration being the **HUD OSWorld-Verified mirror reproducing OpenAI's 72.6**.[cite:34][cite:35] On HLE Astra gains ~10 pts over Sol (57.2 vs 47.2) but still trails the Claude 5.x line; AA's *parity* verdict is a 9-eval composite and is not reproduced benchmark-by-benchmark. On the one head-to-head where both appear (BrowseComp) Astra is **#2 behind Sol**, not a "clear win."

---

## 1. Executive summary

| | GPT-6 Astra | Gemini 3.8 Flash |
|---|---|---|
| Vendor / release | OpenAI, staged GA **2026-09-03** | Google, GA **2026-09-02** |
| API model ID | `gpt-6-astra` | `gemini-3.8-flash` |
| Positioning | New flagship above the GPT-5.6 Sol/Terra/Luna family; headline is **computer/browser control** | "Most intelligent workhorse" Flash; long-horizon SWE + agents at Flash price |
| Output price /1M | **$50** standard (**$75** long-context >272K) | **$3.75** intro (→**$7.50** on 2027-01-01) |
| Independent AA Intelligence Index (v4.1.1) | **~61** — level with GPT-5.6 Sol (61); behind Fable 5.1 (~66) and Muse Spark 1.3 (~62) | **59** (high effort); on the Intelligence-vs-Cost Pareto frontier |
| One-line verdict | **Vendor-reported** gains in computer-use / agentic autonomy / cyber; on the **independent AA Index it is at parity with the prior gen (61=61) at 2.5× the price**, and beaten by Fable 5.1 (66) at the same list price. Uncapped-tier only, if at all. | **Exceptional speed/cost/vision value** (AA 59, 326.9 tok/s, $0.58 blended, native vision). But it does **not** beat the repo's under-cap incumbents (GLM-5.3 = 60) on intelligence, its coding lead is vendor-self-computed, it is **proprietary** (no open-weight rung), and its cap-eligibility **flips on 2027-01-01**. Adopting reverses the repo's "all Gemini retired" decision AND requires a code change to the R10 guard. |

**Routing takeaway (detail in §6):** **no config changes this cycle — both models are held, not adopted.** GPT-6 Astra is prior-gen-parity at 2.5× the price (uncapped-tier only, if ever, for a future computer-use role). Gemini 3.8 Flash's only clear win over the repo's under-cap incumbents is output speed; its intelligence (59) trails GLM-5.3 (60), it is proprietary, its cap-eligibility flips on 2027-01-01, and re-introducing it requires reversing the v1.1.1 Gemini retirement plus a CI-guard (R10) code change. Revisit only if a latency- or vision-bottlenecked role emerges.

---

## 2. Confirmed specifications & pricing

### GPT-6 Astra
- **Pricing (OpenAI Standard, per 1M):** input **$10**, cached input **$1**, cache write **$12.50**, output **$50**. Long context (>272K tokens): input **$20**, cached **$2**, cache write **$25**, output **$75** — OpenAI publishes these as **multipliers** (2× input/cache, **1.5× output**), so $75 is 1.5× $50, not a 2× figure.[cite:1][cite:2]
- **Fast mode:** up to ~2× Standard speed at ~2× the price.[cite:3]
- **Context:** 1.1M input / 128K output.[cite:4]
- **Reasoning:** `reasoning.effort` up to **max** (API default **low**).[cite:4]
- **Availability:** OpenAI API, Azure, AWS Bedrock; Trusted Access first, then Plus/Pro/Business/Enterprise.[cite:3]

### Gemini 3.8 Flash
- **Pricing (per 1M):** input **$0.75**, output **$3.75** (introductory, through **2026-12-31**); reverts to **$1.50 / $7.50** on **2027-01-01**. Cache read **$0.075**, cache write **$0.0417**. Batch/flex ~half.[cite:5][cite:6][cite:7]
- **Context:** 1M input / 65.5K output.[cite:7]
- **Thinking levels:** default **medium**; low / high effort selectable.[cite:6]
- **Modalities:** text, image, video, audio, PDF in; text out. Native multimodal.[cite:7]
- **Availability:** Google AI Studio, Vertex AI.[cite:7]
- **Cost caveat:** despite flat per-token pricing, Artificial Analysis measured **~40% higher real cost per task** than 3.7 Flash (~30% more output tokens + more agent turns).[cite:8]
- **Cache write $0.0417** is a **storage rate** (per 1M tokens per hour), not a per-call fee — not comparable to Astra's one-time $12.50 cache-write.[cite:7]
- **Sibling (out of scope):** a restricted **Gemini 3.8 Flash Cyber** variant shipped in the same announcement; not assessed here.[cite:5]

---

## 3. GPT-6 Astra — full benchmark survey

Legend: **[V]** vendor-reported (OpenAI self-computed launch table); **[I]** independent.

### Coding & software engineering
| Benchmark | Score | Prov. | Comparators (as tabled) |
|---|---:|---|---|
| DeepSWE v1.1 (113-task agentic) | **74.1%** | [V] (Datacurve benchmark; OpenAI-run) | Gemini 3.8 Flash 73.8, Opus 5 73.7, Muse Spark 1.3 75.4, Sol 72.7, Fable 5 69.9[cite:9][cite:10] |
| Terminal-Bench 4.0 | **57.7%** | [V] | Fable 5.1 55.8, Opus 5 52.3, Sol 37.3, Gemini 3.8 Flash 19.1[cite:11] |
| Terminal-Bench Science 0.1 | **64.6%** | [V] | public top ~30%[cite:12] |
| FrontierCode v1.1 (Main) | **53.3%** | [V] | Fable 5 53.5, Opus 5 53.4[cite:12] |
| FrontierCode v1.1 (Extended) | **64.5%** | [V] | —[cite:12] |
| Database Migration Tasks | **63.9%** | [V] (OpenAI internal) | —[cite:12] |
| BenchCAD (CAD programming) | **95.9%** | [V] | Sol 83.3, Fable 5.1 84.3, Opus 5 82.1[cite:12][cite:13] |
| AA Coding Agent Index | **67** | [I] Artificial Analysis | **Fable 5.1 leads at 70**; Opus 5 / Fable 5 / Muse Spark 1.3 ≈ 67; Sol ~65 — i.e. Astra is mid-pack, not leading[cite:31] |

### Agentic, computer-use & tool use
| Benchmark | Score | Prov. | Comparators |
|---|---:|---|---|
| OSWorld 2.0 (offline) | **72.6%** (~40 min/task, ~47% less time than Sol) | [V] | Sol 65.7, Opus 5 70.2[cite:11][cite:14] |
| ScreenSpot-Pro | **92.7%** | [V] | Sol 76.9, Fable 5 87.3[cite:11] |
| Agents' Last Exam | **59.3%** (~65% fewer output tokens than Opus 5) | [V] | Opus 5 55.5, Sol 53.6[cite:14] |
| SRE-Bench | **99.2%** best-of-4 / **88.0%** pass@1 | [V] | Sol 55.9 (pass@1)[cite:12][cite:14] |
| BrowseComp | **91.5%** | [V] | —[cite:12] |
| AutomationBench | **41.4%** | [V] | —[cite:12] |
| Mind2Web (Codex harness) | ~1.9× faster task completion vs Sol | [V] | —[cite:14] |

### Math, science, reasoning & knowledge
| Benchmark | Score | Prov. | Comparators |
|---|---:|---|---|
| FrontierMath Tier 4 v2 | **97.6%** ("saturated") | [V] | Fable 5.1 87.8, Opus 5 73.2[cite:14] |
| ARC-AGI-3 (provider adapter harness) | **99.9%** ("saturated") | [V] | —[cite:12][cite:14] |
| GPQA Diamond | **96.0%** | [V] | Gemini 3.8 Flash 95.3, Sol 94.6[cite:13][cite:14] |
| Humanity's Last Exam (with tools) | **57.2%** | [V] | Fable 5.1 65.0, Opus 5 63.6 — **Astra loses here**[cite:14] |
| GeneBench-Pro | **39%** | [V] | —[cite:12] |
| MedChemBench (internal) | **49.7%** | [V] | —[cite:12] |

### Cybersecurity
| Benchmark | Score | Prov. | Comparators |
|---|---:|---|---|
| ExploitBench | **100%** ("saturated") | [V] (CMU-built benchmark, **OpenAI-run**) | Sol 78.5, Opus 5 70.0[cite:12][cite:34] |
| ExploitBench (contamination-controlled, Jun–Aug 2026) | **39.0%** | [V] | Sol 5.5[cite:14] |
| ExploitGym | **42.4%** | [V] | Sol 30.3[cite:14] |
| FrontierCyber challenges | **86 / 226** solved | **[I-partner]** Irregular (Irregular states it "worked with OpenAI" — third-party-run but vendor-partnered pre-release, not arm's-length) | Sol 34/226[cite:36] |

### Overall independent intelligence
| Metric | Score | Prov. | Note |
|---|---:|---|---|
| **AA Intelligence Index v4.1.1** | **~61** | [I] Artificial Analysis | **Level with GPT-5.6 Sol (61)**; behind Fable 5.1 (~66), Muse Spark 1.3 (~62). "Capability at parity with the previous generation at 2.5× the price."[cite:15][cite:16][cite:17] |

AA Index v4.1.1 composes 9 evals: GDPval-AA v2, τ³-Banking, Terminal-Bench v2.1, SciCode, HLE, GPQA Diamond, CritPt, AA-Omniscience, AA-LCR.[cite:18]

---

## 4. Gemini 3.8 Flash — full benchmark survey

### Coding & software engineering
| Benchmark | Score | Prov. | Note |
|---|---:|---|---|
| DeepSWE v1.1 | **73.7–73.8%** | **[V]** Google self-computed (mini-swe-agent, high thinking; posted to the public Datacurve view — *not* an independent run; other models' rows are their own self-reported numbers) | **3rd** on that view behind Muse Spark 1.3 (75.4) and GPT-6 Astra (74.1); vs 3.7 Flash 65.3 (+8.4pp)[cite:8][cite:19][cite:37] |
| Terminal-Bench 2.1 | **89.4%** (best published of all tracked models) | [V] | vs 3.7 Flash 85.8; edges Opus 5 89.1[cite:11][cite:21] |
| Terminal-Bench 4.0 | **19.1%** | [V] | recalibrated; not comparable to older TB[cite:21] |
| SWE-bench Verified | **96.40%** — highest-scoring **proprietary Flash-tier** model on the Vals board (Gemini 3.8 Flash is **closed-weights**, not open) | [I] Vals.ai | rank/denominator contested (Vals shows ~86–88 models, Opus 5 leading ~97.0; one tracker reports 80.0 for this model) — verify before relying[cite:22] |
| FrontierCode v1.1 (Main) | ~ (tabled vs Astra) | [V] | Astra 53.3[cite:11] |

### Agentic, computer-use & domain agents
| Benchmark | Score | Prov. | Note |
|---|---:|---|---|
| OSWorld 2.0 | **59%** | [V] Google self-computed (max-of-3, partial score, pre-08.08 patch) | Astra 72.6 (OpenAI's own harness) — **different harnesses/patch levels, not cross-comparable**[cite:20][cite:19] |
| Vals Finance Agent v2 | **61.4%** — **#1 of 56** | [I] Vals.ai (Google also cites) | standout domain result[cite:22][cite:23] |
| Harvey Legal Agent Benchmark | **10.0%** all-pass | [V] | weak spot[cite:23] |
| Vals Index (overall) | **66.25%** — **#12** | [I] Vals.ai | +10.6 vs DeepSeek V4[cite:22] |

### Reasoning, science & knowledge
| Benchmark | Score | Prov. | Note |
|---|---:|---|---|
| Humanity's Last Exam (Verified) | **54.9%** | [V] | verified edition runs lower than original[cite:19][cite:23] |
| GPQA | **95.3%** (Diamond, per cross-tables) | [V] | leads several frontier models[cite:13][cite:24] |
| BioMysteryBench (hard / human-solved) | **56.5% / 88.8%** | [V] | —[cite:23] |
| LAB-Bench 2 | **86.2%** | [V] | —[cite:23] |
| GDPval-AA v2 (Elo) | **1545** | [V] | —[cite:23] |

### Multimodal / vision / long context
| Benchmark | Score | Prov. | Note |
|---|---:|---|---|
| LVBench (agentic / static) | **87.8% / 87.1%** | [V] | video understanding[cite:23] |
| CharXiv Reasoning (no tools) | **86.2%** | [V] | chart reasoning[cite:23] |
| GDP.PDF | **35%** | [V] | document comprehension[cite:23] |
| Context window | 1M in / 65.5K out | [V] | native multimodal[cite:7] |

### Overall independent intelligence
| Metric | Score | Prov. | Note |
|---|---:|---|---|
| **AA Intelligence Index v4.1.1 (high)** | **59** | [I] Artificial Analysis | +3 vs 3.7 Flash; median for tier is 36; **on the Intelligence-vs-Cost Pareto frontier**; ~305 tok/s (fastest AA has measured)[cite:15][cite:25] |

Scales with `thinking_level` — AA measured low/medium/high separately; buy the setting that matches the task.[cite:25]

---

## 4a. Selection-criteria checklist (from the iternal.ai LLM selection guide)

Used here as a **decision-dimension checklist only** — its benchmark *numbers* are not treated as authoritative (AA and DeepSWE are). This is the lens the routing decision in §6 is scored against.[cite:29]

- **Hard filters (eliminate first):** data privacy / sovereignty / air-gap, deployment mode (API vs self-host vs hybrid), context window, licensing, language support, multimodal support, regulatory (SOC2/GDPR/HIPAA/FedRAMP), geographic availability.
- **Weighted soft criteria:** benchmark performance, cost efficiency (cost per *successful* request, not just per token), latency/throughput, context window, provider reliability (uptime SLA, rate limits, stability), ecosystem/tooling, safety/alignment (hallucination, refusal, factuality), customization (fine-tuning, system-prompt flexibility).
- **Tiering & routing:** classify task by intelligence level → route simple→budget, medium→mid-tier, hard→frontier, with confidence checks before escalation; prefer a hybrid architecture (self-host open weights for sensitive data, budget APIs for routine high-volume, frontier APIs for the hardest tasks). **Re-evaluate quarterly and after major releases.**
- **Benchmark names the guide says to consider** (names only, numbers ignored): MMLU / MMLU-Pro, GPQA Diamond, HumanEval(+), SWE-bench Verified, SWE-bench Pro, LiveCodeBench, FrontierCode, CursorBench, Aider Polyglot, Terminal-Bench 2.1, SWE Marathon, GSM8K, MATH / MATH-500, AIME 2025, USAMO'25, ArxivMath, ARC-AGI 2, BBH, IFEval, TruthfulQA, HELM, BFCL v4, RULER, Needle-in-a-Haystack, LongGenBench, MLNeedle, MMMU Pro, Arena Elo, Arena Vision, OSWorld, WebArena, GDPval-AA, Humanity's Last Exam, HalluLens, SimpleQA, MedQA, PubMedQA.
- **Capability categories:** knowledge, scientific reasoning, real-world coding, code self-repair, software engineering, mathematical reasoning, abstract/fluid reasoning, tool use / function calling, agentic tasks, long-context, multimodal (vision/audio/video), computer use, instruction following, safety/factuality/hallucination, multilingual, RAG, document processing, long-horizon coding, competitive programming, high-volume processing.

**How our two models score against the hard filters:** both pass API-availability, context (1M+), multimodal (Gemini native; Astra strong computer-use). Neither is self-hostable/air-gappable (both closed), which matters for the repo's `open-reason-*`/`open-coder` sovereignty rungs — so neither can replace an *open-weight* role, only a proprietary one.

## 5. Same-week context (not evaluated for adoption here)
- **Muse Spark 1.3** (Meta, 2026-09-02): DeepSWE v1.1 **75.4%** (max reasoning) — tops the DeepSWE field. **Closed-weight (proprietary)** agentic coder. AA Index **62 (`max`, partner-preview, no purchasable API provider)** / **61 (`xhigh`, GA)** — so the *buyable* config merely ties Astra, not beats it.[cite:10][cite:26]
- **Claude Fable 5.1 / Mythos 5.1** (Anthropic, 2026-09-01): Fable 5.1 leads AA Index (~66) and wins HLE-with-tools (65.0); same price as Fable 5 with cheaper cache reads.[cite:27]

These matter for future refreshes: the current independent intelligence leader is **Fable 5.1**, and the DeepSWE leader is **Muse Spark 1.3** — not either model this report was commissioned on.

---

## 6. Routing implications for model-mesh

### GPT-6 Astra — evaluated, held
- **Against adoption:** the honest cost argument is **family-fit + cost-per-capability**, not the cap (the flagship-coding slot `coder-xl` is a *named exemption* the cap never governs — see `docs/PROVIDERS.md`). On the independent AA Index Astra is **61 = GPT-5.6 Sol 61** — the family already mapped as `flagship-xl`/`flagship-mid` — at **2.5× Sol's current output price**, and **Fable 5.1 scores 66 at the identical $10/$50**. Paying 2.5× for prior-gen-parity, when a same-priced alternative scores higher, fails family-fit-over-rank and cost-per-capability.
- **Its real (vendor-reported) edge is computer-use / browser control / cyber** — capabilities *no current agent role exercises*, and for which there is only one thin independent corroboration (HUD's OSWorld-Verified mirror reproducing OpenAI's own 72.6). If a future computer-use agent role is ever added, Astra is the reference candidate; until then, **no change** — document as "evaluated, held."
- **hephaestus note:** Astra is GPT-family, so it *would* be schema-legal as a `hephaestus` flagship-native rung (passes R6), but it adds cost without an independent capability gain over the Sol tier already there.

### Gemini 3.8 Flash — the real decision (narrower than it first appears)

**Case for — what it *actually* wins on (independent only):** AA Index **59** on the Intelligence-vs-Cost **Pareto frontier**, **326.9 tok/s** (among the fastest AA has measured), **$0.58 blended**, native vision, 1M context. Those — not intelligence or coding rank — are the differentiators.

**Incumbent head-to-head (this is decisive):** the roles it was proposed for (`gen-pro`/`gen-flash`/`vision-lite`) sit *behind* placeholders that already beat or match it under cap:

| Model (role) | AA Index | Output $/1M | tok/s | Native vision | Open weights |
|---|---:|---:|---:|:--:|:--:|
| **Gemini 3.8 Flash** (candidate) | 59 | $3.75 intro / **$7.50 Jan-2027** | **326.9** | ✓ | ✗ |
| GLM-5.3 (`comm-xl`, in repo) | **60** | $4.40 | — | ✗ | ✓ (MIT) |
| GLM-5.3-Flash (`comm-lite`/`vision-lite`, in repo) | — | **$0.50** | — | ✓ | ✓ (MIT) |
| qwen3.7-plus (`gen-pro`, in repo) | 39 | $1.60 | — | ✗ | ✓ |

Gemini does **not** beat GLM-5.3 on intelligence (59 vs 60) and is dearer than the repo's existing native-vision `vision-lite` ($3.75 vs $0.50). Its genuine advantage over the incumbents is **raw output speed** and a stronger vision tier than GLM-5.3-Flash — a real but narrow niche.[cite:25][cite:32][cite:33]

**Blockers / caution (all must be handled before any adoption):**
1. **Cap-eligibility flips on 2027-01-01.** $3.75 out is under the $4.65 cap *today*; **$7.50 out is 62% over it**. A Gemini rung in `hybrid`/`b4b` would therefore be **time-boxed**: re-audit before 2026-12-31 and either remove it, move it to `ultimate` (the existing pattern for `flagship-open`/`div-flagship`), or grant a named exemption. **Do not adopt on the intro price.**
2. **Hard CI blocker — R10.** `scripts/validate-full-config.py` implements `RETIRED_VENDORS = re.compile(r"\bgemini\b", re.I)` and **fails the build on any `gemini` string**. Re-introduction is not just a doc reversal — it requires an explicit code change to the R10 guard (plus the `checks.py` denylist, which also lists `gemini`) and a CHANGELOG entry recording the reversal of the v1.1.1 retirement.
3. **Proprietary.** Closed-weights, Google-API-only — so it can only occupy a *proprietary* rung, never the open-weight sovereignty rungs (`open-reason-*`, `open-coder`).
4. **~40% higher real cost per task** than 3.7 Flash (verbosity) — same caveat class as GLM-5.3.
5. **Provider mapping unresolved.** Gemini is Google-served; the `opencode` gateway's coverage of `gemini-3.8-flash` is **not confirmed**. A re-introduction must either verify gateway coverage or add a Google provider row — do not assume a `ProviderB/opencode` route.

**Recommended posture:** **hold, do not adopt now.** The intelligence case is neutral-to-negative vs under-cap incumbents (GLM-5.3 = 60); the only clear win is output speed, which no current role is bottlenecked on. If a latency-sensitive or heavy-vision role emerges, revisit as a **time-boxed, `ultimate`-or-exempt-after-2026-12-31 proprietary rung**, gated on: (a) R10/denylist code change + CHANGELOG reversal, (b) verified provider mapping, (c) the post-intro $7.50 cap check. Not a silent swap, not on the intro price, not into an open-weight slot.

### Net
- **No config changes recommended this cycle.** Both models are *held*, not adopted:
  - **GPT-6 Astra** — held for a hypothetical future computer-use role; parity-at-2.5× today.
  - **Gemini 3.8 Flash** — held pending a latency/vision-bottlenecked role; blocked by cap-flip + R10 + proprietary-only + unverified provider mapping. Revisit before 2026-12-31 only if a fitting role appears.
- The current under-cap incumbents (GLM-5.3, GLM-5.3-Flash, Kimi K3, Qwen tiers) already cover these slots at equal-or-better intelligence and lower or comparable cost.

---

## References
[cite:1]: https://developers.openai.com/api/docs/pricing
[cite:2]: https://www.aipricing.guru/openai-pricing/
[cite:3]: https://openai.com/index/gpt-6-astra/
[cite:4]: https://llm-stats.com/models/gpt-6-astra
[cite:5]: https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/
[cite:6]: https://ai.google.dev/gemini-api/docs/models
[cite:7]: https://openrouter.ai/google/gemini-3.8-flash
[cite:8]: https://emergent.sh/learn/gemini-3-8-flash-benchmarks
[cite:9]: https://officechai.com/ai/these-are-the-official-openai-gpt-6-astra-benchmarks/
[cite:10]: https://ai-tldr.dev/models/gpt-6-astra/
[cite:11]: https://www.datacamp.com/blog/gpt-6-astra
[cite:12]: https://aireleasetracker.com/model/openai/gpt-6-astra
[cite:13]: https://aiwiki.ai/wiki/Astra_(OpenAI)
[cite:14]: https://www.vellum.ai/blog/gpt-6-astra-benchmarks-explained
[cite:15]: https://artificialanalysis.ai/
[cite:16]: https://fourweekmba.com/gpt-6-astra-benchmarks/
[cite:17]: https://www.requesty.ai/blog/gpt-6-astra-independent-benchmarks
[cite:18]: https://artificialanalysis.ai/models/gpt-6-astra
[cite:19]: https://deepmind.google/models/gemini/flash/
[cite:20]: https://aireleasetracker.com/model/google/gemini-3.8-flash
[cite:21]: https://kingy.ai/blog/gemini-3-8-flash-review/
[cite:22]: https://www.vals.ai/models/gemini-3-8-flash
[cite:23]: https://benchmarklist.com/models/gemini-3-8-flash
[cite:24]: https://mungomash.com/ai-benchmark-scores/
[cite:25]: https://artificialanalysis.ai/models/gemini-3-8-flash
[cite:26]: https://www.marktechpost.com/2026/09/02/meta-ai-released-muse-spark-1-3/
[cite:27]: https://www.anthropic.com/news/claude-fable-5-1-mythos-5-1
[cite:28]: https://artificialanalysis.ai/leaderboards/models
[cite:29]: https://iternal.ai/llm-selection-guide
[cite:30]: https://www.vellum.ai/llm-leaderboard
[cite:31]: https://artificialanalysis.ai/articles/benchmarking-gpt-6-astra
[cite:32]: https://artificialanalysis.ai/models/glm-5-3
[cite:33]: https://artificialanalysis.ai/models/qwen3-7-plus
[cite:34]: https://www.vellum.ai/blog/gpt-6-astra-benchmarks-explained
[cite:35]: https://sophon.at/leaderboards/osworld-verified-leaderboard
[cite:36]: https://www.irregular.com/research/assessing-gpt-6-astra
[cite:37]: https://deepmind.google/models/evals-methodology/gemini-3-8-flash/
