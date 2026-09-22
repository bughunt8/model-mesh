# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 22 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker remains in the reviewed bounded-repair revision. Decisions D14 through D18 are represented consistently in the plan, analysis, index, and decision log, without reopening settled priorities or authorizing execution. This verdict applies only to the five substantive document versions fingerprinted below. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [README.md](README.md), [DECISIONS.md](DECISIONS.md))

## Scope and review method

I reviewed the uncommitted documentation changes on local branch `evaluation-1` at base HEAD `b8e4f8915d0121d7b2796c82de37a030cfd3feab`. The base commit does not identify the new working-tree content; the document hashes below do.

I examined the complete diff to all five substantive documents, including the final consistency update to `BENCHMARKS.md`, checked repair, feedback, rescue, metric, and comparator wording across the package, and verified that all five committed baseline documents match the hashes from my preceding expanded-package review.

I did not edit target documents or branches. This report was authored outside the repository for incorporation as `REVIEW.md`. It supersedes the previous review record while preserving its history below.

## Prior review history

The initial two-document review returned REVISE with three substantive findings. The corrected two-document package subsequently received SHIP for documentation only. I then independently reviewed the expanded five-document package, including its new analysis and decision log, and returned SHIP with no new substantive blocker. None of those decisions authorized execution or certified runtime performance.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording allowed prohibited tradeoffs and weakened mandatory controls. | High | Resolved. All mandatory controls and evidence are required; no accepted objective regression may be compensated by another improvement. Uncertainty remains inconclusive without a silently authorized positive regression margin. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Mandatory discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. These inputs remain settled, useful-work discovery is deferred, and current questions concern genuinely unresolved protocol definitions. ([Plan: Measurement interview](PLAN.md#measurement-interview), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review insufficiently covered the evaluator and surrounding stack. | High | Resolved. Whole-stack qualification remains mandatory, including installer, coordinator, evaluator, simulated users, services, and worker. Unsafe user/shared-host privileges are not authorized by upstream instructions; inability to meet policy means deferral. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The expanded-package review confirmed consistent selections, explicit coverage gaps, constrained causal claims, operational/evaluation/setup accounting, and the distinction between documentation, measured outcomes, and adoption evidence. Those protections remain present in the current package. ([BENCHMARKS.md](BENCHMARKS.md), [ANALYSIS.md](ANALYSIS.md), [DECISIONS.md](DECISIONS.md))

## Current review findings

**No new substantive blockers.**

### Comparison fidelity

D14 is correctly represented as two selected stages: `arm-baseline` versus `arm-method` first, then `arm-method` versus `arm-routing`. The controlled comparisons cannot be replaced by a later human-led or already multimodel operational comparator. Exact configurations and permitted feedback remain open without reopening the stage selection. ([Plan: Isolate the method and routing effects](PLAN.md#isolate-the-method-and-routing-effects), [Analysis: Distinguish the experiment's causes](ANALYSIS.md#distinguish-the-experiments-causes), [Decision D14](DECISIONS.md#settled-decisions))

### Defect outcome and repair cap

D15 and D16 are faithfully represented: defect quality is scored on the final frozen artifact after at most one repair cycle following initial submission, with the same cap within each comparison. An artifact may be submitted without repair. The prior first-submission acceptance metric has been replaced, and the text expressly prohibits a separately scored first-handoff defect target while retaining audit traces and resource accounting. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [Plan: Candidate measurement dictionary](PLAN.md#candidate-measurement-dictionary), [Decisions D15 and D16](DECISIONS.md#settled-decisions))

### Feedback isolation and human intervention

D17 is preserved without a coaching loophole: human diagnoses, hints, clarification, and edits cannot rescue a scored attempt. Humans may stop unsafe execution and evaluate frozen results. Final hidden answers, holdout tests, and evaluator findings cannot enter repair, and final failure cannot reopen an unused repair opportunity. The permitted non-holdout feedback remains a required pre-execution decision. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [Analysis: Define defects before optimizing anything](ANALYSIS.md#define-defects-before-optimizing-anything))

### Failure at the limit

The plan correctly distinguishes consuming the single repair from failing the task. The last permitted submission is frozen and evaluated; a failed final artifact or resource-limit termination is recorded as failure. Missing output remains in the assigned-task denominator without inventing defect findings. Completion, incompletion, safety stops, and severity-specific defects remain separately visible. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation))

### Separate rescue and accounting

D18 is represented as immutable scored outcomes followed, only if separately authorized, by an unscored rescue with its own run identity. Rescue cannot replace the original failure or contaminate other scored attempts. The four-ledger analysis separates operational delivery, independent evaluation, setup/qualification, and later rescue, with rescue expenditure disclosed in broader observed totals rather than hidden or credited as scored success. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [Analysis: Human attention and cost boundaries](ANALYSIS.md#human-attention-and-cost-boundaries), [Decision D18](DECISIONS.md#settled-decisions))

### Remaining scope and authorization boundaries

The selected benchmarks remain B01, B06, and B10; selected scenarios remain A01, A03, A05, A08, A09, A11, and A12. The package retains no compensated regressions, deferred useful-work discovery, security qualification, original PR #3, and no direct main update. It explicitly leaves resource caps and execution approval unresolved rather than treating one repair cycle as an unlimited budget or runtime authorization. ([README.md](README.md), [BENCHMARKS.md](BENCHMARKS.md), [DECISIONS.md](DECISIONS.md))

The final benchmark update also records the settled stages and repair rules, replaces the obsolete open comparator-choice question with exact configuration and feedback questions, and expressly distinguishes the modified local pilot protocol from an unchanged official benchmark evaluation. The official grading result therefore does not erase or conceal the local repair conditions. ([Benchmark rules](BENCHMARKS.md#rules-already-settled), [Measurement questions](BENCHMARKS.md#measurement-questions-that-remain-open))

## Nonblocking decisions before execution

These are protocol requirements, not documentation blockers and not invitations to renegotiate D14 through D18:

- Pin both controlled comparisons, including models, harnesses, prompts, tools, reasoning settings, and the intended intervention. Predeclare how stage-two configuration is chosen without tuning against hidden final results.
- Define initial submission, final submission, and repair boundaries operationally. Specify permitted non-holdout tests and agent-review feedback, while preserving the prohibition on hidden final-evaluator feedback and human rescue.
- Set task-level time, token, monetary, tool-call, concurrency, and retry limits across initial work and the single repair. One repair cycle is not itself a complete resource envelope.
- Freeze defect taxonomy, severity, adjudication, failure/refusal classification, denominators, observation windows, and the evidence standard for improvement or inconclusive outcomes.
- Predeclare cost scope, attention allocation, and amortization horizon. Distinguish bounded scored outcomes from evaluation overhead and broader expenditure including any separately authorized rescue.
- Pin benchmark subsets, graders, simulator settings, environments, and policy versions; qualify the execution boundary; define supplemental A03, A05, and A09 cases; obtain separate execution authorization.

The decision log and analysis already leave these matters open. They must be resolved before execution without adding a first-handoff quality target, additional repair cycles, human coaching, or outcome-overwriting rescue. ([Decision log: Open questions](DECISIONS.md#open-questions), [PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `16a3fe7a3b4151cb6cc0ea8d8ceff60e06f5d339a741bbd7048d6270b717810f` |
| `PLAN.md` | `d8e017a51596d1977ab2031dffa2955f61d9e5dfeba5e1c0ef5c9c97cfccc76a` |
| `BENCHMARKS.md` | `08ef2be6de2068db8bb1dc91e09cb0af23aa4a2e72ea867878dcb1d2b98d6505` |
| `ANALYSIS.md` | `e065df209b868d97b589e62417f6eab9bc28dc58c5678e87127ce3190da4cb2a` |
| `DECISIONS.md` | `e06f0e3bd52e6629a4ea4e8cb541d42b77fee7a2dc27291b049bf6176a04c13f` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to the substantive documents require renewed review.

## Limits

- This is a read-only adversarial document review, not a runtime certification, execution approval, benchmark result, or performance guarantee.
- I performed no installation, model runtime test, benchmark execution, penetration test, or implementation audit. None is required for this documentation-only revision.
- I did not run or certify repository gates. They remain the integrating agent's separate responsibility.
- Earlier source checking was selective. No new external research was needed or performed for these owner-decision changes; this review does not independently verify every benchmark citation, license, or dependency.
- I checked fidelity against the supplied owner decisions and review context, not an independently authenticated transcript of every historical decision.
- I did not change or verify the remote state of PR #3, either branch, or main.

**Final disposition: SHIP the fingerprinted documentation through the existing PR workflow, subject to separately run repository gates. No pilot execution is authorized.**
