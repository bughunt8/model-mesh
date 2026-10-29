# Review panel

The independence rule in [ORCHESTRATION.md](ORCHESTRATION.md) decides who may review. This page decides how a review is run: what a reviewer sees, which questions it asks, how findings are merged, and when a review happens before and after the work.

Status: a design proposal dated 2026-10-26. The validator checks the data and the scripts have self-tests. No panel has been run, so no claim here about catch rates is measured. The ideas on zero-context reviewers, lens personas and design gates come from a study of the Elephant-Goldfish Model, summarised in [EGM-ANALYSIS.md](research/orchestration/EGM-ANALYSIS.md).

## Two axes, kept apart

| Axis | What it buys | How model-mesh sets it |
|---|---|---|
| Independence | Different training and different harness, so the reviewer does not repeat the author's blind spot | Harness and model family rules O5, O16 and the spread tier |
| Lens | Different questions, so the review covers more kinds of defect | The lens library and the lens list per situation |

Many lenses on one model family add breadth and no independence. A lens never replaces the independence rule, and the validator checks both separately.

## Zero-context contract

Every reviewer call starts fresh. Each option carries the constraints `zero-context-review` and `readonly-review-artifact` (rule O15). In practice:

1. The reviewer receives three things: the artifact under review, the standard or lens it applies, and any explicit context the orchestrator chooses to pass as text.
2. It does not receive the author's conversation, the orchestrator's plan, earlier reviewer findings or the author's own summary of what changed.

The validator checks the part it can see (rule O15). Each reviewer seat may carry only the keys `role`, `seat`, `harness`, `chain`, `kind`, `execution` and `lenses`, so a seat cannot declare write tools or an author transcript in the data. Whether a runner honors the contract at run time is not checked and not tested.
3. It gets read-only tools. It cannot edit the artifact, push, or call the author's harness.
4. Its project instruction files are the ones for review, not the author's.
5. It returns findings in the shape of [finding.schema.json](../examples/orchestration/finding.schema.json). Free text does not enter the merge.

This is context isolation, not a security boundary. A reviewer with shell access can still read the working tree. Run it in a separate checkout when that matters.

## Lenses

A lens is a set of questions. The library is [lenses.json](../examples/orchestration/lenses.json). Each situation names its lenses and the first one is primary.

| Lens id | Looks for |
|---|---|
| `contract-fit` | Requirements with no matching change, and changes nobody asked for |
| `regression-risk` | Existing behavior the change could break, and tests that would not notice |
| `security-abuse` | Untrusted input reaching sensitive places, and widened permissions |
| `simplicity` | Parts that could be removed or replaced, and single-user abstractions |
| `operability` | Missing logs, missing rollback, steps that need a person |
| `migration-compat` | Old data, old clients and mixed-version behavior |
| `cost-quota` | Money, tokens and rate limits at expected and peak load |
| `comprehension` | Undefined terms and steps that depend on the author's knowledge |
| `evidence-provenance` | Claims with no source, and contrary evidence left out |
| `numerics-reconciliation` | Totals, units, periods and rounding that do not agree |
| `authorization-state` | Unrecorded approval, wrong target, and end state that differs from the request |
| `consistency` | Names, numbers and references that differ between artifacts |

## Tiers and fan-out budget

Every lens is one fresh reviewer call by default. The primary lens is named in the situation's `primary_lens` field and must be the first lens. Putting several lenses in one call saves money and gives up the diversity the lens was for. The tier caps the cost, and rule O17 enforces the split for the spread tier: the primary lens runs on both seats and every other lens runs on exactly one seat. For the other tiers O17 caps lens count and seat count only.

| Tier | Situations | Lenses at most | Reviewer seats | Reviewer calls per round |
|---|---|---|---|---|
| `standard` | A01 to A04, A07, A08, A10 to A12 | 4 | 1 | up to 4 |
| `wide` | A09 | 6 | 1 | up to 6 |
| `spread` | A05, A06 | 6 | 2, disjoint families | up to 7, because both seats run the primary lens |

Add one aggregator call per round. The old design spent one reviewer call. A `standard` round spends up to five calls in total. Check that against the profile cap before adopting a row: the cap limits price per token and does not limit the number of calls.

The spread tier is for security work and independent change review, where one family missing a defect costs the most. Its second seat cross-checks the primary lens, and the remaining lenses split between the two seats. A ranking of which tier is worth its cost is a hypothesis until [score-review.py](../scripts/score-review.py) has run on a real corpus.

## Aggregator

Each option has an aggregator seat (rule O16). It sits outside the author and orchestrator harness and families, so the merge step cannot inherit the author's bias.

In the spread tier the merge model would otherwise be one of the two reviewing families. Outside ultimate, the aggregator's first rung is therefore a third family whenever the model table has one under the cap, and a later rung may fall back to a reviewer family. Where no third family exists the aggregator copies reviewer seat 1. That is the case for A05 on hybrid and b4b, and for every option on ultimate. Rule O16 enforces the third-family preference. When the aggregator shares a family with a reviewer, treat the merge as less neutral and keep the single-family blocker rule below.

Merge in this order:

1. Validate every finding against the schema. Reject free text.
2. Cluster with [aggregate-findings.py](../scripts/aggregate-findings.py): same path, same category, and a range within 3 lines of the range of the cluster's first finding, so a chain of nearby findings cannot grow into one cluster. Paths and family names are normalized and ids are prefixed with the input file name. Keep the highest severity. Record the lenses, harnesses and families that reported it.
3. Mark a cluster `corroborated` when two or more families reported it. A single-family cluster is kept and labeled, not dropped.
4. Possible duplicates the rules cannot settle go to a model merge. The script lists them in `related_clusters` and sets `needs_model_merge`: the same place under a different category, a finding with no line range next to ranged findings of the same category, and several rangeless findings on one path and category.
5. Sort by severity, then corroborated first. Blockers stop the round.
6. The model merge must keep each cluster's families, severity and corroboration flag. A blocker reported by one family stays a blocker. The script does not check what the model merge does with its output.

The deterministic step runs first so the model merge cannot silently rewrite what two reviewers said.

## Gates

Two optional reviews wrap the author work in A02 and A03, set in each situation's `gates` field (rule O18). Both use the option's reviewers, so they are cross-family and cross-harness like any other review.

| Gate | When | Standard | Output |
|---|---|---|---|
| `spec-readiness` | After the contract or spec is written and before authors start | [spec-readiness.md](../examples/orchestration/standards/spec-readiness.md) | Findings. Blockers stop the run |
| `drift` | After authors finish and before acceptance | [drift.md](../examples/orchestration/standards/drift.md) | A list of differences between the spec and the delivered change, or "No drift detected" |

A09 produces the spec that the A02 and A03 gate reads. It has no gate of its own because its panel is the review.

## Repository drift

[check-drift.py](../scripts/check-drift.py) applies the same idea to model-mesh itself. It compares the counts, IDs and paths that the method docs state against the data and scripts, and prints only the differences. It runs in CI.

## Measuring

[score-review.py](../scripts/score-review.py) scores runs against seeded defects. For each run it reports recall, cluster precision, what each lens and each family caught alone, and what only one of them caught. The committed fixture is invented. The protocol for a real corpus is in [SEEDED-DEFECTS.md](research/orchestration/SEEDED-DEFECTS.md).

## Known limits

- On ultimate, the second spread reviewer seat in A05 and A06 is a single rung with no fallback. The model table has no legal fallback for it: every other eligible family overlaps an author, the orchestrator or reviewer seat 1, or is retiring, and the one family it uses has a single model row. If that rung fails, the round runs with one reviewer family and should be reported as degraded.
- On hybrid, b4b and global, the second seat has one fallback from another family. The seat that answers can change between runs, and a run should record which family answered.
- Spread seats run on qwen-code in the example data. Most second-seat models there come from other vendors than the harness maker, so that pairing needs an adapter that has not been built or run.
- `corroborated` means two families reported a finding in the same place. It does not mean the finding is correct, because families can share an error.
- Nothing here has run on a real artifact.

## Not adopted

- A decision model that returns typed probabilities in place of text, as a router or finding triage seat. It was not assessed when the matrix was built. [SYSTEM-ONE.md](research/orchestration/SYSTEM-ONE.md) records why it is not in the matrix and what a pilot would have to show.
- Unbounded reviewer swarms and nested spawning. The tier table is the limit.
- Reviewers that inherit the author's model. The independence rule forbids it.
- A human approval step inside every stage. The profiles run without one, and gates only stop on blockers.
- A separate AI policy file. This is a one-owner repository and `CONTRIBUTING.md` already states the review rule.
