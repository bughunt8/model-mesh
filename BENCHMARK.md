# OMO-Benchmark

A profile-weighted evaluation framework for `omo.jsonc` configurations — the agent
and category model chains used by oh-my-openagent / OpenCode.

**Version:** 1.0
**Snapshot date:** 2026-10-18
**Status:** Living document. See `docs/06-handover.md` before editing.

This snapshot evaluates benchmark candidate configurations, not the current runtime-routing profiles. Its findings do not authorize a profile change or bypass region, retirement, licence or reviewer-independence policy; read [the repository map](docs/REPOSITORY-MAP.md) before adopting a candidate.

## Why this exists

`omo.jsonc` assigns model fallback chains to 11 agent profiles and 10 category
lanes. These profiles do not share a job description. Hephaestus needs terminal
execution depth; Oracle needs a reasoning ceiling; Explore needs latency;
Multimodal-Looker needs OCR fidelity. A single leaderboard cannot rank them,
because a model that wins one profile can lose another by 40 points on the same
chain.

OMO-Benchmark maps each profile's *core focus* onto eight benchmark dimensions,
scores every model in the roster, applies an ordered-chain decay, and subtracts a
contract-risk penalty for profiles whose output is machine-parsed.

## Quick start

```bash
./scripts/validate.sh   # validates configs/omo.recommended.jsonc
```

Read in this order:

- `docs/01-methodology.md` — how scores are produced
- `docs/02-model-scorecard.md` — the eight-dimension model table
- `docs/03-agent-profiles.md` — per-agent matrix and verdicts
- `docs/04-category-lanes.md` — per-category matrix and verdicts
- `docs/05-data-quality.md` — caveats, discrepancies, noise floors
- `docs/06-handover.md` — rules for the next updater

## Headline findings

Three profiles are structurally misconfigured: Hephaestus (GPT-native
constraint), Sisyphus (duplicate prompt_append discards the operating
contract), Explore (a 340 tok/s model is missing from a latency-bound chain).

Claude Opus 5.5 is the strongest single model in the roster — Hermes 63.31,
SkillsBench 69.6 — and is under-used: it heads only one of eleven profiles.

GPT-6.1 Sol is the best value: Hermes 57.09 at $1.19/task, 4.2x cheaper than
Opus per task.

DeepSeek V4.1 Flash-1017 is the Pareto winner for high-volume execution:
TB4 42.3, DeepSWE 77.0, $0.26/task.

The largest risk is instruction-following collapse, not capability. GLM-5.3
scores SkillsBench 45.6 against TB4 37.9 — a 7.5-point inversion — and
appears in four chains where it should appear in none.

Two chains contain dead or unverified entries: tokeness/deepseek-v4.1-flash
(no canonical ID) and packyapi/gemini-4-argon (availability unconfirmed).

## Data files

- `data/model-scores.csv` — the eight-dimension scorecard, machine-readable
- `data/profile-fits.csv` — per-profile slot weights and weighted scores
- `data/sources.yaml` — every benchmark source with URL and snapshot date

## License

MIT. See `LICENSE`.
