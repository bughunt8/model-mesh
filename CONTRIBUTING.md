# Contributing to model-mesh

Thanks for helping. Two ground rules keep this repo shippable:

1. **No real model/provider names.** CI (`.github/checks.py`) fails the build if any real vendor/model name appears in file contents or paths. The messaging is **harness-agnostic**. The method targets any coding-agent harness, and the repo ships examples for two (**OpenCode** via oh-my-openagent, and the **DeepSeek Harness**). The names `oh-my-openagent` and `opencode` are allowed because they are the OpenCode example's required framework identifiers (not model names); the DeepSeek Harness example keeps its own required identifiers too. Use placeholders (`ProviderA`, `flagship-xl`, …) for everything else. (Real model IDs are permitted only in `docs/EXAMPLE-MAPPING.md`, `docs/research/`, and the benchmark surfaces listed below, which are denylist-exempt.)
2. **Configs must validate.** Agents use `model` + `fallback_models` (never `models`); `ultrawork` uses a singular `model`; categories use `models[]`; use `reasoning` not `variant`. Run the checks below before opening a PR.

## Before you open a PR

```bash
python .github/checks.py         # denylist + manifest + skill + profile-shape + link checks
./setup-config.sh hybrid         # materialize succeeds for each profile
bunx oh-my-openagent doctor      # if you changed configs and have the framework installed
```

Run the loop's own reviewer on your change: `/mm-verify`.

## What lives where

- `skills/`: the loop (adapted from fable-method, MIT; see `THIRD_PARTY_NOTICES.md`). Keep changes here in sync with the loop's intent.
- `profiles/`: routing fragments. If you change a profile, update the README "Profile at a glance" table to match (CI checks profile validity; keep the prose honest).
- `docs/`: methodology and mapping guides, plus the benchmark docs `docs/01-methodology.md` through `docs/06-handover.md`.
- `configs/`: the recommended benchmark configuration and its change log.
- `data/`: the benchmark scorecard, profile weights, and provenance.
- `BENCHMARK.md`: the benchmark entry point.

`configs/`, `data/`, `BENCHMARK.md`, and `docs/01`–`06` are the deliberately denylist-exempt benchmark surfaces: real model IDs are the benchmark's product, so the release gate's exact-path and exact-prefix exemptions cover those files and nothing else. Do not carry benchmark model IDs into any other file.

## OMO-Benchmark

The benchmark has its own rules:

- **One rule: do not change a head slot on the basis of a single benchmark.** Head slots carry 50% of the chain score, and single-benchmark decisions are how a model with a documented instruction-following collapse ended up in four chains.
- **Update a model score:** edit `data/model-scores.csv`, change only the column whose anchor benchmark moved, note the snapshot date in the commit message, run `python3 scripts/score.py`, and update the affected doc in `docs/` in the same commit if a grade band changes.
- **Add a model:** it needs a Hermes Index entry or a harness-consistent Terminal-Bench 4.0 entry. A contract-bearing seat (Momus, Sisyphus-Junior, Metis, Explore, Multimodal-Looker) also needs no documented instruction-following failure, or accepts the CXR penalty. Multimodal-Looker needs a published vision or document benchmark; "multimodal" in a press release is not evidence.
- **Normalization:** the best observed model scores 100, the worst 0, and the 50th percentile 50. If a new model exceeds the current ceiling, rescale the whole column and bump the minor version.
- **Commit prefixes:** `score:`, `config:`, `docs:`, `fix:` (for example `score: update Hermes snapshot to 2026-11-01`, `config: promote a model to an Atlas head`, `docs: add a model to the scorecard`, `fix: correct a provider/model ID`).

## License

By contributing you agree your contributions are MIT licensed. New original work is © bughunt8; upstream portions remain © Sahir619.
