# 06 — Handover Notes for the Next LLM

This document is written for a model that inherits the repository and must
update it. Read it before changing a single score.

## 6.1 What to update first

1. **Hermes Index snapshot.** The anchor for six of eight dimensions. Refresh and
   record the snapshot date in the header of `docs/02-model-scorecard.md` and in
   `data/sources.yaml`.
2. **Terminal-Bench 4.0.** DeepSeek's official table is the cleanest cross-model
   source. If DeepSeek stops publishing it, use Anthropic's and Google's launch
   tables, which are harness-consistent within themselves.
3. **Model roster changes.** If a new model enters (Kimi K3.1, GLM-5.4, Opus 6),
   score it on all eight dimensions before adding it to any chain. Do not add a
   model to a head slot on the basis of one benchmark.

## 6.2 What not to change

- **Do not lower the Opus 5.5 reasoning score below 100.** It is the ceiling in
  the roster (AA 58). A future model scoring 60 should become the new 100, and
  all other scores should be rescaled.
- **Do not treat the CXR penalty as a model-quality judgment.** It is a
  parse-failure probability. A model can be excellent and still lose 15 points
  because it omits a token.
- **Do not compare raw scores across dimensions.** Only the Fit column is
  cross-dimension comparable.
- **Do not add a model to a contract-bearing seat** (Momus, Sisyphus-Junior,
  Metis, Explore, Multimodal-Looker) without either evidence of instruction
  adherence or the CXR penalty applied.

## 6.3 Open questions

| # | Question | How to resolve |
|---|---|---|
| 1 | Does Kimi K3's tool-call repeat bug reproduce on Tokeness routing? | Live timed test with a 20-turn task; count duplicate calls |
| 2 | Does `tokeness/gemini-4-argon` serve real Argon? | Timed verification call; check TTFT and TPS against published figures |
| 3 | Does `no-hephaestus-non-gpt` fire on a fallback rung? | One live Hephaestus invocation with the primary unavailable |
| 4 | Is PackyAPI's function calling fixed? | 10 sequential tool calls; count successes |
| 5 | Does DeepSeek V4.1 Flash's shorter output break the `STATUS:` contract? | Run Sisyphus-Junior once; grep for the token |

## 6.4 The one-line summary

> The config's head models are mostly correct; its fallback slots are where the
> errors live. Three chains contain dead or unverified entries, one chain has a
> duplicate key that discards its contract, and GLM-5.3 appears in four chains
> despite a documented instruction-following failure. Fix the fallbacks before
> adding capability.

## 6.5 Decision rules for a new model
```
IF no Hermes Index AND no TB4 entry
THEN it does not get a head slot.

IF documented instruction-following failure
THEN it does not get a contract-bearing seat without CXR -15.

IF no published vision or document benchmark
THEN it does not get a Multimodal-Looker rung.

IF effective price < 50% of official
THEN run a timed verification call before trusting it.
```


## 6.6 File map

| File | Update when |
|---|---|
| `data/model-scores.csv` | Any benchmark number changes |
| `data/sources.yaml` | A new source is added or a snapshot is refreshed |
| `data/profile-fits.csv` | Weights or chain membership change |
| `docs/02-model-scorecard.md` | Regenerate from the CSV |
| `docs/03-agent-profiles.md` | An agent chain changes |
| `docs/04-category-lanes.md` | A category chain changes |
| `configs/omo.recommended.jsonc` | After any accepted chain change |
| `configs/CHANGES.md` | Every config edit, with rationale |
