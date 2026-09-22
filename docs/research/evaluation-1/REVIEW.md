# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 22 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker was found in the D22 and D23 update. The documents implement AI judges with human dispute resolution and exact-reference/template cosmetic grading, without authorizing human rescue, weakening the every-confirmed-defect failure rule, or treating review as execution approval. This verdict applies only to the five substantive document versions fingerprinted below. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [BENCHMARKS.md](BENCHMARKS.md), [DECISIONS.md](DECISIONS.md), [README.md](README.md))

## Scope and method

I reviewed the uncommitted documentation changes on local branch `evaluation-1`, based on HEAD `d729f42e265da2a29261f2dd233a04a35630598d`. That commit identifies the baseline, not the new working-tree content.

I inspected the complete diff to all five substantive documents and checked related judge, human-review, template, normalization, confirmation, evidence, accounting, and authorization wording across the package. I verified that all five committed baseline documents match their fingerprints in my preceding acceptance-and-caps review.

I made no target-file or branch changes. This reviewer-authored report was created outside the repository for incorporation as `REVIEW.md`. It replaces the previous attestation while preserving the review history below.

## Prior review history

The original two-document review returned REVISE with R1 through R3. The corrected documents subsequently received SHIP for documentation only. An independent review of the expanded package, including analysis and decision log, also returned SHIP. Later independent reviews of D14 through D18 and D19 through D21 each returned SHIP within that same documentation-only boundary.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording permitted compensated regressions and weakened mandatory controls. | High | Resolved. All mandatory controls and evidence remain required; no objective regression can be compensated by another improvement. Uncertainty is inconclusive without an unauthorized regression allowance. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. The client purpose and priorities remain fixed, useful-work discovery is deferred, and questions concern unresolved protocol details. ([Plan: Measurement interview](PLAN.md#measurement-interview), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review did not adequately cover the full execution stack. | High | Resolved. Whole-stack qualification remains mandatory, with deferral rather than an exception for unsafe upstream instructions. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The expanded-package review confirmed consistent selections, explicit benchmark coverage gaps, cautious causal claims, separate accounting boundaries, and separation of reviewed specifications from measured results. Those protections remain present. ([BENCHMARKS.md](BENCHMARKS.md), [ANALYSIS.md](ANALYSIS.md))

D14 through D18 remain intact: method effect first and routing effect second, final post-repair defect scoring only, at most one repair within the task envelope, no human rescue during scored work, frozen failures, and separately authorized unscored rescue that cannot rewrite results. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [Decision log](DECISIONS.md))

D19 through D21 remain intact: both visible executable checks and agent review may inform repair without hidden final-evaluator information; every confirmed defect, including cosmetic defects, fails acceptance; and resource caps are predeclared by scenario or difficulty class with matched caps across competing arms on the same task. Numeric values and execution approval remain open. ([PLAN.md](PLAN.md), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification), [DECISIONS.md](DECISIONS.md))

## Current findings

**No new substantive blockers.**

### AI judges and human dispute resolution

D22 is faithfully represented. Independent AI judges assess frozen outputs against the frozen rubric and evidence. A human resolves judge disagreement, conflicting checks, or uncertain findings only after the artifact is frozen, without edits, repair feedback, or another attempt. The text does not require a human to rejudge every undisputed task. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [Decision D22](DECISIONS.md#settled-decisions))

The A09 coverage route and architecture-planning analysis now use this same AI-judge plus human-dispute procedure rather than a separate requirement for broad human adjudication. A model score alone is not treated as evidence of correctness. ([Benchmark coverage table](BENCHMARKS.md#selected-scenarios-and-coverage-gaps), [Analysis: Coverage across selected scenarios](ANALYSIS.md#coverage-across-selected-scenarios))

### Exactness and declared exceptions

D23 remains an exact-reference or exact-template requirement, not broad stylistic constraints permitting varied presentations or an unspecified hybrid. Versioned artifacts, variable slots, exceptions, comparison representation, and normalization must be declared before execution; fuzzy visual similarity and post-outcome preferences cannot substitute for the selected contract. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [Decision D23](DECISIONS.md#settled-decisions))

The distinction from universal byte-for-byte comparison is not a substantive softening: exactness is defined against the predeclared representation and exceptions. The actual reference artifacts and normalization details are not yet approved, so this review does not certify a future exception set or an implementation that normalizes away required differences. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [Decision log: Open questions](DECISIONS.md#open-questions))

### Reference leakage and final-evaluation isolation

Task-visible presentation templates must be available equally to competing arms while remaining separate from hidden expected answers, completed solutions, and final-evaluator findings. The plan explicitly treats inability to separate these as an execution-readiness failure. Template conformance remains distinct from substantive correctness. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [Analysis: Define defects before optimizing anything](ANALYSIS.md#define-defects-before-optimizing-anything))

### Confirmed findings and uncertainty

The documents do not equate a suspected defect with a confirmed defect by assertion, do not promote unresolved findings to a pass, and do not claim that AI-judge agreement proves correctness. Panel composition, calibration, independence controls, consensus handling, response windows, and unresolved-result disposition remain open protocol requirements. Human dispute resolution changes the evaluation disposition of the frozen artifact, not the artifact itself or its repair allowance. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [Analysis: Define defects before optimizing anything](ANALYSIS.md#define-defects-before-optimizing-anything))

### Attention and authorization

The analysis explicitly requires human adjudication minutes, waiting time, and cost to be recorded under declared accounting rules. It does not silently authorize every-task human review or a recurring validation workload. The package retains no compensated tradeoffs, no useful-work rediscovery, no execution authorization, and no claim of statistical proof or universal correctness. ([ANALYSIS.md](ANALYSIS.md), [README.md](README.md), [PLAN.md](PLAN.md))

B01, B06, and B10 remain the selected benchmarks; A01, A03, A05, A08, A09, A11, and A12 remain the selected scenarios. Original PR #3 and the no-direct-main-change workflow remain the documented publication route. ([README.md](README.md), [DECISIONS.md](DECISIONS.md))

## Nonblocking decisions before execution

These details must be completed without reopening D22 or D23:

- Pin judge models, prompts, panel composition, evidence access, independence controls, calibration, and consensus rules. Define objective dispute triggers, including judge/check conflicts and uncertainty.
- Name the human adjudicator, response window, evidence required for confirmation or dismissal, and unresolved-result disposition. Preserve frozen artifacts and the prohibition on repair feedback or extra attempts.
- Freeze reference/template versions, variable fields, exceptions, comparison representation, and normalization. Validate both true conformance and meaningful deviations without relaxing exactness after outcomes.
- Inspect task-visible templates for embedded answers, completed examples, metadata, or other hidden solution content before use. Do not execute a task whose presentation contract cannot be separated from protected correctness evidence.
- Define allocation of judge usage, human adjudication attention, waiting time, and cost. Any validation sampling workload remains a proposed protocol detail requiring approval, not an automatic every-task human-review mandate.
- Complete numeric resource caps, class assignment, sample design, evidence standards, benchmark subsets, independent grading, supplemental cases, and whole-stack security qualification; obtain separate execution authorization.

These are necessary protocol details, not blockers to a documentation PR or permission to weaken settled acceptance and repair rules. ([Decision log: Open questions](DECISIONS.md#open-questions), [PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `5a4ea13cfa62c55943624a6220e02704720fae55ba25b302c82f764635fd31e0` |
| `PLAN.md` | `6e1cfe32fbf0fc44ca3af3ff1b9e3d36b9cd08b3f8d409699bec361ac5d7c220` |
| `BENCHMARKS.md` | `32f73638a139ee0f52288657b8da243cf20d337da3d07c1d118c7914755a6143` |
| `ANALYSIS.md` | `f1a88c96da9bd0836c77b62076aabb2e685d09384a51c2ee120e2a630ab1957a` |
| `DECISIONS.md` | `ab8abfcc4570c689aad5bbd7762929c467d610f515c552e4413db748070ac1c7` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to the substantive documents require renewed review.

## Limits

- This is a read-only independent document review, not execution approval, runtime certification, a benchmark result, or a guarantee of improved outcomes.
- I performed no installation, benchmark execution, model runtime test, penetration test, or implementation audit. None is required for this documentation-only revision.
- I did not run or certify repository gates. They remain the integrating agent's separate responsibility.
- No external research was performed for these owner-decision updates. Earlier source checks were selective, not exhaustive verification of every benchmark, license, dependency, or execution requirement.
- Fidelity was assessed against the supplied owner decisions and review context, not an independently authenticated transcript of every historical discussion.
- I did not change or independently verify the remote state of PR #3, either branch, or main.

**Final disposition: SHIP the fingerprinted documentation through the existing PR workflow, subject to separately run repository gates. No pilot execution is authorized.**
