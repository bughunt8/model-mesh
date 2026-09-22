# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 22 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker was found in the D24 through D27 update. The five substantive documents consistently specify two independent AI judges, personal dispute resolution by the project owner, a pilot-wide limit of 10 hours of total elapsed runtime, and a combined pilot-wide USD 100 model/tool/compute ceiling. They do not turn those limits into an execution authorization or a claim that the selected scope fits. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [BENCHMARKS.md](BENCHMARKS.md), [DECISIONS.md](DECISIONS.md), [README.md](README.md))

## Scope and method

I reviewed the uncommitted documentation changes on local branch `evaluation-1`, based on HEAD `885e35b731b093cdb5f2754b8c7ad75e0f1aafeb`. That commit identifies the baseline, not the new working-tree content.

I inspected the complete diff to all five substantive documents and checked panel size, dispute ownership, elapsed time, spending, resource reservations, stop behavior, accounting, and authorization language across the package. I verified that every committed substantive baseline document matches its fingerprint in my preceding judges-and-templates review.

I made no target-file or branch changes. This report was authored outside the repository for incorporation as `REVIEW.md`. It replaces the prior attestation while preserving its history.

## Prior review history

The original two-document review returned REVISE with R1 through R3. The corrected two-document package received SHIP for documentation only. The expanded-package review and subsequent reviews covering D14 through D18, D19 through D21, and D22/D23 also returned SHIP within that documentation-only boundary. None authorized pilot execution or certified runtime effectiveness or safety.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording permitted compensated regressions and weakened mandatory controls. | High | Resolved. Mandatory controls and evidence remain required, no objective regression can be compensated by another improvement, and uncertainty remains inconclusive without an unauthorized regression margin. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. The client purpose and priorities remain fixed; useful-work discovery stays deferred. ([Plan: Measurement interview](PLAN.md#measurement-interview), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review did not adequately cover the full execution stack. | High | Resolved. Whole-stack qualification and deferral for unmet controls remain mandatory, without an upstream-instruction exception. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The expanded-package review confirmed consistent selections, explicit coverage gaps, cautious causal claims, separate accounting, and separation of reviewed documentation from measured outcomes. These protections remain present. ([BENCHMARKS.md](BENCHMARKS.md), [ANALYSIS.md](ANALYSIS.md))

D14 through D18 remain intact: method effect first, routing effect second, final post-repair defect scoring only, at most one repair inside the task envelope, no human rescue during scored work, frozen failures, and separately authorized unscored rescue that cannot rewrite outcomes. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [DECISIONS.md](DECISIONS.md))

D19 through D21 remain intact: visible checks and agent review may inform repair without hidden final-evaluator information; every confirmed defect, including cosmetic defects, fails acceptance; and task caps are predeclared by scenario or difficulty class and matched between competing arms. ([PLAN.md](PLAN.md), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))

D22 and D23 remain intact: AI judges assess frozen outputs with human dispute resolution, and cosmetic grading uses an exact versioned reference/template with advance exceptions rather than post-outcome preferences. Task-visible templates must not reveal hidden answers or completed solutions. The new decisions specify the panel and dispute owner without weakening those rules. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [DECISIONS.md](DECISIONS.md))

## Current findings

**No new substantive blockers.**

### Panel size and dispute authority

D24 requires two independent AI judges per final deliverable, and D25 names the project owner personally as the dispute resolver. The plan prohibits silently accepting one judge's result if the second judge is unavailable. Either judge's disagreement or uncertainty uses the dispute path, and agreement must still satisfy frozen checks and evidence. Exact models, independence controls, calibration, response windows, and unresolved-result handling remain protocol details. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [Decisions D24 and D25](DECISIONS.md#settled-decisions))

Owner adjudication remains post-freeze evaluation, not permission to edit output, coach repair, restart an attempt, or require owner review of every undisputed task. Active effort and waiting remain separately recorded. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [Analysis: Define defects before optimizing anything](ANALYSIS.md#define-defects-before-optimizing-anything))

### Elapsed runtime is not human labor

D26 correctly preserves the explicit clarification: 10 hours means total elapsed pilot runtime, not active adjudication hours, cumulative agent CPU hours, or separate allowances per task, suite, or stage. The documents do not infer a distinct owner-hours cap. Clock anchors and setup, queue, pause, grading, and owner-wait treatment remain explicitly unresolved; no automatic pause or exclusion is presumed. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [Decision D26 and O14](DECISIONS.md))

### Combined monetary ceiling

D27 specifies USD 100 for combined model, tool, and compute charges across the pilot, not per arm, benchmark, worker, judge, comparison, or retry. The proposed ledger includes repair review, both final judges, retries, simulators, and compute. Unclassified charges are not presumed exempt while setup, subscriptions, fees, and separately authorized rescue treatment await approval. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [Decision D27 and O15](DECISIONS.md))

The USD 100 charged-resource limit is explicitly separate from the economic value of owner labor and the broader total-cost objective. No owner hourly rate, amortization horizon, or conversion to platform credits is represented as agreed. ([Analysis: Human attention and cost boundaries](ANALYSIS.md#human-attention-and-cost-boundaries), [DECISIONS.md](DECISIONS.md))

### Reservations and global stops

The plan requires dispatch decisions to account for spent, committed, reserved, and in-flight charges, including final judging, rather than checking only invoices already received. Capacity is reserved for safe termination and evidence retention; activities whose charges cannot be bounded within the remaining allowance must not launch. These are proposed enforcement requirements, not claims that a budget controller exists. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [README.md](README.md))

Reaching a global ceiling cannot reset the budget, add a repair, or promote unfinished or disputed work to a pass. Rescue requires separate authorization and an explicit remaining or additional resource envelope, not automatic permission to exceed the original limits. Global-stop classification and finalization remain explicit pre-execution decisions. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [Decision log: Open questions](DECISIONS.md#open-questions))

### Feasibility and preserved scope

The documents make no claim that all selected scenarios, suites, both comparison stages, repeats, supplemental cases, and two-judge evaluation fit the ceilings or provide adequate statistical evidence. They require a proposed predeclared subset or deferral if needed rather than quietly dropping difficult tasks, removing a judge, weakening controls, or extending the pilot. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))

B01, B06, and B10 remain the selected benchmarks; A01, A03, A05, A08, A09, A11, and A12 remain the selected scenarios. No compensated tradeoffs, useful-work rediscovery, runtime approval, or direct main update is introduced. Original PR #3 remains the documented publication route. ([README.md](README.md), [DECISIONS.md](DECISIONS.md))

## Nonblocking decisions before execution

The documentation can ship while these execution-readiness decisions remain open:

- Fix the 10-hour start and end anchors and treatment of setup, queues, grading, owner waits, and any proposed pauses. Do not silently convert elapsed runtime into active-work time.
- Define global admission and shutdown rules, including in-flight work, final grading, evidence retention, and owner disputes. Predeclare how unfinished, undisputed, disputed, and not-yet-started tasks are reported without hiding assigned failures or claiming success without required evidence.
- Specify the USD 100 billing boundary and a non-overlapping reservation ledger, including estimation uncertainty, cancellation, reconciliation, setup, subscription allocation, fees, and any later authorized rescue.
- Select and qualify both judges, their independence and calibration arrangements, and the owner's response procedure. An unavailable second judge cannot become an automatic one-judge pass.
- Set numeric task/class caps and propose an adequately balanced allocation within both aggregate ceilings. Do not promise complete coverage or statistically supported improvements before feasibility and evidence requirements are assessed.
- Complete exact reference/template artifacts, benchmark subsets, comparator configurations, supplemental cases, economic cost allocation, whole-stack security qualification, and separate execution authorization.

These are implementation and protocol requirements, not permission to renegotiate panel size, dispute ownership, the elapsed-time meaning, the aggregate currency/ceiling, or the previously settled repair and acceptance rules. ([Decision log: Open questions](DECISIONS.md#open-questions), [PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `f1962cd1a2fb05df4a32218d1f5f5623244304bbdd3caf7844c16c3bed177479` |
| `PLAN.md` | `23b4fa238a9391d7e42b314eae51293426f30beafa1ec2e8c44a3dbc757f5d8b` |
| `BENCHMARKS.md` | `0f0d69731cedca0b8d7fa78a1b3a59930d59f7e08787390e70d494b4fbfcd76d` |
| `ANALYSIS.md` | `d67fa6dcbab63e51f8b5565b5043cff01212114d022813a699e20f2b4cebd2ff` |
| `DECISIONS.md` | `7eeddfb847da8ffc4b8188497e1fc81730287464ba82ec7424afb8ca28766e58` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to substantive documents require renewed review.

## Limits

- This is an independent read-only document review, not an execution approval, runtime certification, benchmark result, spending authorization, or guarantee of improved outcomes.
- I performed no installation, benchmark execution, model runtime test, penetration test, implementation audit, cost simulation, or feasibility trial. None is required for this documentation-only change.
- I did not run or certify repository gates. They remain the integrating agent's separate responsibility.
- No external research was performed for these owner-decision updates. Earlier source checks were selective rather than exhaustive verification of all benchmark descriptions, licenses, dependencies, or execution requirements.
- Fidelity was assessed against the supplied owner decisions and review context, not an independently authenticated transcript of every historical discussion.
- I did not change or independently verify the remote state of PR #3, either branch, or main.

**Final disposition: SHIP the fingerprinted documentation through the existing PR workflow, subject to separately run repository gates. No pilot execution or expenditure is authorized.**
