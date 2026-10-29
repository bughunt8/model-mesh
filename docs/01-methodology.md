# 01 — Methodology

## 1. Why a profile-weighted benchmark

A conventional leaderboard answers "which model is best?" OMO-Benchmark answers
"which model is best *for this seat*?" The roster spans incompatible workloads:

| Profile | Core focus | The wrong question |
|---|---|---|
| Hephaestus | Deep autonomous implementation, GPT-native, completion-guarantee prompt | "Which model has the highest reasoning score?" |
| Oracle | High-IQ consultation on architecture and debugging | "Which model codes fastest?" |
| Prometheus | Gated planning: interview → approval → scaffold → Metis → write file | "Which model is most creative?" |
| Metis | Adversarial gap analysis and ambiguity detection | "Which model is most agreeable?" |
| Momus | Binary verdict gate against repository state | "Which model has the longest context?" |
| Atlas | Todo orchestration: one item in progress, verify before complete | "Which model writes the best code?" |
| Sisyphus-Junior | One bounded delegated task, no scope drift | "Which model is most autonomous?" |
| Sisyphus | Long-loop primary orchestrator with delegation | "Which model is fastest?" |
| Librarian | Documentation retrieval with version-stamped citations | "Which model reasons deepest?" |
| Explore | Parallel grep/search at 3–5x fan-out | "Which model is smartest?" |
| Multimodal-Looker | Verbatim document extraction with locators | "Which model is most creative?" |

## 2. The eight dimensions

| Code | Dimension | Primary anchor | Secondary anchor |
|---|---|---|---|
| AE | Agentic Execution | Terminal-Bench 4.0 | DeepSWE v1.1 |
| TO | Tool Orchestration | MCP Atlas | MCP Mark Verified / Toolathlon |
| IP | Instruction / Procedure | SkillsBench | Hermes Bench |
| R | Reasoning | AA Intelligence Index | HLE / GPQA Diamond |
| CR | Context & Retrieval | AA-LCR / 1M-context utilization | Long-context coding |
| VD | Vision / Document | OmniDocBench | OCR / IDP Core |
| LC | Latency & Cost | $/task (Hermes) | tok/s, TTFT |
| REL | Reliability | Absence of documented loop/instruction failures | Provider verification rate |

## 3. Normalization

Each dimension is normalized so the best observed model scores 100 and the worst
scores 0, with the 50th percentile at 50. This makes columns comparable even
though the underlying benchmarks use different scales.

Rule: never compare raw scores across dimensions. A 90 on LC and a 90 on R mean
different things. Only the **Fit** column is cross-dimension comparable, because
it applies profile weights.

## 4. Chain score formula

A profile's chain is an ordered list, not a set. On a primary agent, slot 1 is
not a fallback — it is the model that actually runs. The chain score therefore
uses geometric decay:
```
ChainScore = sum(w_i * Fit(m_i))
w = [0.50, 0.25, 0.12, 0.08, 0.05]
Fit(m) = sum(d_j * score_j(m)) for j in profile dimensions
```

A chain with a strong head and four irrelevant fallbacks scores higher than a
chain with five mediocre models. That is the correct behaviour: the head is what
runs.

## 5. The Contract Risk (CXR) penalty

Capability alone understates risk for profiles whose output is machine-parsed. A
model that scores 90 on Reasoning but omits a required `STATUS:` token produces
a useless 90.

| Profile | Contract | CXR if a documented instruction-following failure exists |
|---|---|---|
| Momus | Standalone `PLAN_APPROVED` / `PLAN_REJECTED` | -15 |
| Sisyphus-Junior | `STATUS: DONE\|BLOCKED\|NEEDS_ESCALATION` | -15 |
| Metis | `Safe to proceed: yes/no` | -10 |
| Explore | `<analysis>` + `<results>` with absolute paths | -10 |
| Multimodal-Looker | Observation/Inference separation + locators | -10 |
| Oracle | Four-part verdict shape | -5 |

The penalty is not a model-quality judgment. It is a parse-failure probability
discount, and it is the largest single correction in the matrix.

## 6. Grade bands

| Grade | Chain score |
|---|---|
| A | >= 85 |
| A- | >= 80 |
| B+ | >= 75 |
| B | >= 70 |
| B- | >= 65 |
| C+ | >= 60 |
| C | >= 55 |
| D | >= 45 |
| F | < 45 |

Grade bands are authoritative. Rank order inside a band is not, because DeepSWE
v1.1 run-to-run variation is 1.4–3.2 points and the top four models sit within
0.55 points of each other.

## 7. Reproducing the scores

```
bash
python3 scripts/score.py --profile oracle --verbose
python3 scripts/score.py --category quick
python3 scripts/score.py --all --format markdown
```

