# Repository map

model-mesh keeps the engineering method, benchmark research and runtime routing in separate files because they answer different questions. This page maps those files and states which one controls a decision when their recommendations differ.

## What lives where

| Area | Entry points | Authority and limits |
|---|---|---|
| Engineering method | [AGENTS.md](../AGENTS.md), [skills/](../skills/) | The task loop, evidence requirements and domain adapters, including motion. |
| Routing profiles | [ROUTING.md](ROUTING.md), [PROVIDERS.md](PROVIDERS.md), [profiles/](../profiles/) | Four routing profiles, `ultimate`, `hybrid`, `b4b` and `global`. Generic fragments use placeholders; examples carry explicit mappings. |
| Benchmark research | [BENCHMARK.md](../BENCHMARK.md), [methodology](01-methodology.md), [handover](06-handover.md), [configs/](../configs/), [data/](../data/) | Eleven agent seats and ten category lanes, candidate scores, weights and provenance. These seats are not the four routing profiles. |
| Multi-agent orchestration | [ORCHESTRATION.md](ORCHESTRATION.md), [matrix synthesis](research/orchestration/SYNTHESIS.md), [matrix data](../examples/orchestration/matrix.example.json) | Situations, allowed model families, harness choices, fallbacks, region rules and reviewer independence. |
| Independent review | [REVIEW-PANEL.md](REVIEW-PANEL.md), [lenses](../examples/orchestration/lenses.json), [finding schema](../examples/orchestration/finding.schema.json) | Fresh-context review packets, lenses, structured findings and aggregation. omo's own internal reviewers do not count as the independent review. |
| Bounded superloop | [SUPERLOOP.md](SUPERLOOP.md), [council synthesis](research/orchestration/SUPERLOOP-COUNCIL.md), [templates](../examples/superloop/), [driver](../scripts/mm-superloop.py) | Code drives one frozen matrix cell. Decision-model answers are shadow-only by default; evidence, not model confidence, determines success. |
| Validation | [TESTING.md](../TESTING.md), [checks workflow](../.github/workflows/checks.yml), [benchmark workflow](../.github/workflows/benchmark.yml) | Static policy checks, regression tests and score recomputation. They do not establish live harness compatibility or task effectiveness. |

## Which rules win

- **Owner policy and routing eligibility.** Benchmark rank cannot override region access, a retired family, licence requirements, provider boundaries, budget placement or independent-review rules. A benchmark roster can include a model that runtime policy excludes.
- **Runtime configuration.** `setup-config.sh` materializes `profiles/`. The superloop restricts the selected profile to the frozen matrix cell and writes its own worktree config. It does not load `configs/omo.recommended.jsonc` or use benchmark scores to pick a model.
- **Adopting a benchmark candidate.** Check its sources and limitations first, then update the explicit mapping and matrix in a reviewed change if policy permits it. Validate every fallback rung. Complete live qualification separately; score recomputation is not runtime evidence.
- **Council synthesis.** The matrix synthesis records the original orchestration decisions. The superloop synthesis adds the bounded control plane, qualification rules and dissent. Neither report changes the benchmark snapshot or proves model effectiveness.
- **Pinned runtime.** The superloop targets omo 4.19.4. The benchmark snapshot is not permission to upgrade that runtime or assume its role and category names work unchanged.

## Installing and running

Both [install.sh](../install.sh) and [install.ps1](../install.ps1) install all five `mm-*` skills and back up an existing same-named skill before replacing it. The installer tests compare every copied file and every backup with its source.

The standalone install copies skill instructions, not the Python driver or repository templates. Keep a repository checkout and run superloop commands from its root; the owner supplies the tools registry, pins, acceptance checks and budget. Read the sandbox and unverified-runtime limits in [SUPERLOOP.md](SUPERLOOP.md) before a live run.

## Validating an integration

Run the full commands in [TESTING.md](../TESTING.md), including the benchmark checks and installer tests. CI covers pull requests and pushes to both `main` and `staging`; no live model call is part of these checks.

Keep benchmark configs and provenance under the existing root-level `configs/` and `data/` paths. Keep orchestration examples under `examples/orchestration/`, run templates under `examples/superloop/`, and council reports under `docs/research/orchestration/`. Integrating one track must not silently replace the others or turn their proposals into measured results.
