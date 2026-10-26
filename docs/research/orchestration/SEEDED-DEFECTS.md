# Seeded-defect protocol

Purpose: find out whether more lenses or more model families catch more defects, and at what cost. Until this runs, the tier table in [REVIEW-PANEL.md](../../REVIEW-PANEL.md) is a hypothesis.

Status: protocol and scoring script only. The committed [fixture](../../../examples/orchestration/seeded/cases.example.json) is invented. No corpus exists and no result is claimed.

## Corpus rules

1. Artifacts are realistic: real repositories, real specs, real reports. Toy files overstate recall.
2. A person who will not review plants the defects. Reviewers and authors never see the defect list.
3. Each defect records path, line range, category and severity, in the same vocabulary as [finding.schema.json](../../../examples/orchestration/finding.schema.json).
4. Plant defects of every category the lenses target, including several that no single lens should catch alone.
5. Keep a share of clean artifacts. Precision cannot be read without them.
6. Hold out part of the corpus. Tune panels on one part, report on the other.

## Runs

Run each artifact through these panels:

| Panel | Families | Lenses |
|---|---|---|
| single | 1 | 1 (primary) |
| lenses only | 1 | situation list |
| families only | 2 | 1 (primary) |
| spread | 2 | situation list, as in the spread tier |

Record harness versions, model IDs, dates, calls and tokens per run so panels can be compared at equal cost. Repeat each run at least three times, because model output varies. Add one arm where the author's own family reviews, to measure what the independence rule buys.

## Reading the results

[score-review.py](../../../scripts/score-review.py) reports recall, cluster precision, per-lens and per-family catches, and what only one lens or family caught. Compare panels at equal cost, not equal count. If lenses only matches spread on recall, the second family is not paying for itself on that situation, and the independence rule stays for a different reason: it guards against the author's own blind spot, which the author-family arm measures.

## Limits

Planted defects are easier than natural ones. A panel that scores well here is not shown to work on unplanted defects. Three repeats give a rough spread, not a confidence interval.
