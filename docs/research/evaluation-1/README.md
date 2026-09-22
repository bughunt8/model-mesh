# Evaluation 1

Documentation proposal | No execution authorized | 22 September 2026

This package plans an evidence-based qualification of model-mesh for a client offering. Usefulness is already established by the owner's experience. The open question is what claims about defects, required human attention, accepted-delivery time, cost, controls, and portability can be defended.

## Documents

| Document | Purpose |
|---|---|
| [PLAN.md](PLAN.md) | Portable method, alternative implementations, guardrails, audit requirements, pilot stages, and proposed measurements. |
| [BENCHMARKS.md](BENCHMARKS.md) | Source-cited research on 10 benchmarks, the 12-scenario menu, selected scope, and coverage limitations. |
| [ANALYSIS.md](ANALYSIS.md) | Experimental interpretation, measurement boundaries, controls, and gaps that must be resolved before execution. |
| [DECISIONS.md](DECISIONS.md) | Ordered owner decisions, superseded proposals, open questions, and change rules. |
| [REVIEW.md](REVIEW.md) | Independent adversarial findings, disposition, reviewed scope, and review limitations. |

## Settled scope

The priority order is fewer defects, less owner attention, faster accepted delivery, then lower total cost. No regression may be compensated for by an improvement elsewhere. Safety controls remain mandatory gates.

Selected scenarios are A01 bug repair, A03 refactoring, A05 security audit and remediation, A08 data reconciliation and analysis, A09 requirements and architecture planning, A11 browser administration, and A12 cross-application office work. Selected benchmarks are B01 SWE-bench Verified, B06 GAIA, and B10 TheAgentCompany. The latter remains conditional on whole-stack security feasibility.

Run two comparisons in separate stages: isolate the method first, then the added effect of routing. Measure defect quality on the final artifact after at most one repair cycle following initial submission, with the same cap on both sides and no human rescue. Freeze unsuccessful attempts as failures; separately authorized later rescue remains unscored and cannot replace the failure.

Permitted repair feedback combines executable checks and agent review, without hidden final-evaluator information. Any confirmed defect against the frozen criteria, including cosmetic defects, fails task acceptance. Set resource caps by predeclared scenario or difficulty class, with identical caps for competing arms on the same task; numeric values remain open.

Two independent AI judges assess final outputs, with the project owner personally resolving disagreements or uncertain findings after artifacts are frozen. Cosmetic grading uses an exact reference or template, with any variable fields or exceptions declared before execution. Neither adjudication nor a template permits post-score edits, human rescue, or disclosure of hidden benchmark answers.

The pilot-wide ceilings are 10 hours of total elapsed runtime and USD 100 combined for model, tool, and compute charges. Neither limit resets per task, benchmark, comparison stage, or retry. Ten hours is not an active human-adjudication allowance. Clock anchors, waiting/setup treatment, and detailed cost boundaries must be fixed before execution; no claim is made that the full selected scope fits.

The working branch is `evaluation-1`. The existing [draft PR #3](https://github.com/bughunt8/model-mesh/pull/3) is retained at the owner's request; its branch, `docs/portable-method-pilot`, will be synchronized to the same reviewed commit. Do not merge either branch or treat a documentation merge as pilot authorization.

## Status and boundaries

No adapters, benchmark runner, metrics collector, sandbox, runtime guardrail, production configuration, or infrastructure are implemented by this package. No benchmark results exist from this evaluation. Existing repository checks validate repository consistency, not the method's effectiveness or runtime safety.

Exact comparator configurations, defect criteria, versioned references/templates, judge configurations, dispute procedure, attention accounting, evidence standard, sample allocation, class-level cap values, clock/cost boundaries, and execution environment remain open. The comparison stages, repair rules, acceptance rule, two-judge panel, owner adjudication, exact-template requirement, and pilot-wide ceilings are settled.

All further documentation belongs in this package and is proposed through the same PR. Require fresh independent review for material changes, especially claims, scope, decision rules, or security boundaries.
