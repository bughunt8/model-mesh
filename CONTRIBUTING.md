# Contributing to model-mesh

Thanks for helping. Two ground rules keep this repo shippable:

1. **Provider-neutral core.** CI rejects real model and provider names outside the explicit examples, research, benchmark and rule-implementation exceptions in `.github/checks.py`. Use placeholders such as `ProviderA` and `flagship-xl` in generic method and profile files. Required harness identifiers are not model choices. Read the gate's self-tested exact-path and prefix lists before adding a name; a benchmark import is not permission to add model IDs elsewhere.
2. **Configs must validate.** Agents use `model` + `fallback_models` (never `models`); `ultrawork` uses a singular `model`; categories use `models[]`; use `reasoning` not `variant`. Run the checks below before opening a PR.

## Before you open a PR

```bash
python .github/checks.py         # denylist + manifest + skill + profile-shape + link checks
./setup-config.sh hybrid         # materialize succeeds for each profile
bunx oh-my-openagent doctor      # if you changed configs and have the framework installed
```

Run the loop's own reviewer on your change: `/mm-verify`.

## What lives where

Read [the repository map](docs/REPOSITORY-MAP.md) before a change that crosses the benchmark, routing, review panel or superloop. Benchmark candidates do not bypass runtime policy or live qualification.

- `skills/`: the loop (adapted from fable-method, MIT; see `THIRD_PARTY_NOTICES.md`). Keep changes here in sync with the loop's intent.
- `profiles/`: routing fragments. If you change a profile, update the README "Profile at a glance" table to match (CI checks profile validity; keep the prose honest).
- `docs/`: methodology and mapping guides, plus the benchmark docs `docs/01-methodology.md` through `docs/06-handover.md`.
- `configs/`: the recommended benchmark configuration and its change log.
- `data/`: the benchmark scorecard, profile weights, and provenance.
- `BENCHMARK.md`: the benchmark entry point.
- `examples/orchestration/`: situation matrices, review lenses and harness examples.
- `examples/superloop/` and `scripts/superloop/`: bounded run templates and the control plane.
- `tests/scenarios/` and `TESTING.md`: static skill contracts, checks and their limits.

`configs/`, `data/`, `BENCHMARK.md`, and `docs/01` through `docs/06` are the benchmark-specific denylist exceptions because real model IDs are the benchmark's product. The gate also has existing mapping, research, validator and source-registry exceptions; its self-test defines the complete set. Do not carry benchmark model IDs into generic method files or assume a nearby path is exempt.

## OMO-Benchmark

The benchmark has its own rules:

- **One rule: do not change a head slot on the basis of a single benchmark.** Head slots carry 50% of the chain score, and single-benchmark decisions are how a model with a documented instruction-following collapse ended up in four chains.
- **Update a model score:** edit `data/model-scores.csv`, change only the column whose anchor benchmark moved, note the snapshot date in the commit message, run `python3 scripts/score.py`, and update the affected doc in `docs/` in the same commit if a grade band changes.
- **Add a model:** it needs a Hermes Index entry or a harness-consistent Terminal-Bench 4.0 entry. A contract-bearing seat (Momus, Sisyphus-Junior, Metis, Explore, Multimodal-Looker) also needs no documented instruction-following failure, or accepts the CXR penalty. Multimodal-Looker needs a published vision or document benchmark; "multimodal" in a press release is not evidence.
- **Normalization:** the best observed model scores 100, the worst 0, and the 50th percentile 50. If a new model exceeds the current ceiling, rescale the whole column and bump the minor version.
- **Commit prefixes:** `score:`, `config:`, `docs:`, `fix:` (for example `score: update Hermes snapshot to 2026-11-01`, `config: promote a model to an Atlas head`, `docs: add a model to the scorecard`, `fix: correct a provider/model ID`).

## License

By contributing you agree your contributions are MIT licensed. New original work is © bughunt8; upstream portions remain © Sahir619.
