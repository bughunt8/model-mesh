# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 22 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker was found in the D30/D31 update. The documents implement an eight-minute elapsed dispute window bounded by the earlier global deadline, freeze unanswered disputes as unresolved and not accepted, and adopt minimum breadth followed by depth without inventing a numeric coverage floor or silently reducing scope. This verdict applies to the five substantive document versions fingerprinted below. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [BENCHMARKS.md](BENCHMARKS.md), [DECISIONS.md](DECISIONS.md), [README.md](README.md))

## Scope and method

I reviewed the uncommitted changes on local branch `evaluation-1`, based on HEAD `6b4b9baf484ff46b037c282ccecc401f4ad71107`. That commit identifies the baseline, not the new working-tree content.

I inspected the complete diff to all five substantive documents, checked related dispute, escalation, timeout, unresolved-outcome, denominator, sampling, allocation, scope, and authorization wording, and read the previous review record for continuity. I verified that each committed substantive baseline document matches its fingerprint in my preceding clock-and-cost review.

After the first D30/D31 review, I inspected two targeted consistency cleanups in the plan and analysis. Reversing those two replacements in memory reproduced the previously reviewed file hashes, confirming that no other content in those files changed. The refreshed fingerprints below identify the final reviewed versions.

I made no target-file, branch, or git-state changes. This report was authored outside the repository for incorporation as `REVIEW.md` and preserves the earlier review history.

## Prior review history

The original two-document review returned REVISE with R1 through R3. The corrected two-document package then received SHIP for documentation only. The expanded-package review and subsequent reviews of owner decisions through D29 also returned SHIP within that boundary. None authorized execution, certified runtime safety, established measured effectiveness, or guaranteed feasibility.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording permitted compensated regressions and weakened mandatory controls. | High | Resolved. Mandatory controls and evidence remain required, objective regressions cannot be compensated by other improvements, and uncertainty remains inconclusive without an unauthorized regression margin. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. The client purpose and priorities remain fixed; useful-work discovery remains deferred. ([Plan: Measurement interview](PLAN.md#measurement-interview), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review did not adequately cover the complete execution stack. | High | Resolved. Whole-stack qualification and deferral for unmet controls remain mandatory. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The expanded-package review confirmed consistent selections, explicit coverage gaps, cautious causal claims, separate accounting, and the distinction between documentation and measured outcomes. These protections remain present. ([BENCHMARKS.md](BENCHMARKS.md), [ANALYSIS.md](ANALYSIS.md))

Previously reviewed decisions remain intact:

- D14 through D18: method-first and routing-second comparisons, final post-repair defect scoring, at most one repair inside the task envelope, no scored human rescue, frozen failures, and separately authorized unscored rescue without rewriting outcomes. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [DECISIONS.md](DECISIONS.md))
- D19 through D21: checks plus agent-review feedback without hidden final-evaluator information, failure for every confirmed defect including cosmetic defects, and predeclared matched scenario/difficulty-class caps. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))
- D22 through D25: exact references/templates with advance exceptions, protected hidden answers, two independent AI judges, and personal owner dispute resolution after artifact freeze without edits or renewed repair. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [DECISIONS.md](DECISIONS.md))
- D26 through D29: a continuous 10-hour clock from first scored-task dispatch including grading and owner waits, no concealed scored solving during setup, and an aggregate USD 100 cap covering all new pilot model/tool/compute charges including setup and cleanup. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [DECISIONS.md](DECISIONS.md))

## Current findings

**No new substantive blockers.**

### Timeout fidelity and escalation

D30 sets eight continuous elapsed minutes from recorded dispute escalation, truncated by the global scored deadline if earlier. Owner waiting does not pause the pilot clock, and notification delay cannot silently reset the timer. The existing rule that disagreement, conflicting checks, or uncertain findings trigger owner dispute resolution remains in place; exact escalation and notification mechanics remain open. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [Decision D30](DECISIONS.md#settled-decisions))

The timeout requires a recorded ruling, not merely permission to keep waiting. If no ruling arrives by the cutoff, the task is frozen as unresolved and not accepted. Both judge findings and evidence are preserved, and a late ruling cannot change the scored outcome or reopen the attempt. Other eligible work may continue only within the existing resource limits. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance))

### Unresolved is not a confirmed defect

The package distinguishes a timeout from an adjudicated defect and from a pass. Unresolved tasks remain in assigned-outcome reporting and cannot be removed to inflate accepted-delivery rates. Dispute frequency and response delays are reported instead of attributing every unresolved case to defective model output. The local unresolved outcome also remains separate from the official benchmark grade. ([Analysis: Define defects before optimizing anything](ANALYSIS.md#define-defects-before-optimizing-anything), [BENCHMARKS.md](BENCHMARKS.md), [README.md](README.md))

### Minimum breadth before depth

D31 is an agreed sampling approach, not an agreed sample size. A minimum coverage floor must first be proposed across all seven selected scenarios, using qualified selected benchmarks and needed supplemental cases. Remaining capacity may then support repeated paired trials. Numeric floor, distinct cases, repeats, selection procedure, and allocation across both comparison stages must be approved and frozen before results. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification), [Decision D31](DECISIONS.md#settled-decisions))

Repeated runs do not become new distinct tasks or supply a missing scenario. A loosely mapped benchmark task cannot automatically satisfy every associated scenario. The package does not claim that sparse breadth proves a comparative improvement or a powered design. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [BENCHMARKS.md](BENCHMARKS.md))

### Infeasibility and authority boundaries

If the proposed floor cannot fit safely within the aggregate limits, the plan requires an owner scope decision before execution. It does not authorize silent selection removal, benchmark substitution, a security waiver, reduced judging, or an extended budget. B01, B06, and B10 and scenarios A01, A03, A05, A08, A09, A11, and A12 remain the selected scope pending any explicit new decision. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [BENCHMARKS.md](BENCHMARKS.md), [README.md](README.md))

The update does not introduce runtime or spending permission, a compensated tradeoff, useful-work rediscovery, or direct changes to main. Original PR #3 remains the documented publication route. ([README.md](README.md), [DECISIONS.md](DECISIONS.md))

## Resolved consistency notes

Both nonblocking consistency notes from the first D30/D31 review are now resolved:

- `PLAN.md`, next measurement round, line 297, now asks about recorded escalation and notification mechanics within the settled eight-minute window, and how missing-judge cases or timely but inconclusive responses are recorded without becoming passes. It no longer reopens the selected duration. ([Plan: Next measurement round](PLAN.md#next-measurement-round))
- `ANALYSIS.md`, resource-cap classification, line 83, now limits the open classification work to other pending, in-flight, unstarted, and missing-judge tasks plus shutdown mechanics. It explicitly states that the unanswered-dispute outcome is settled, consistent with O14. ([Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification), [Decision log: Open questions](DECISIONS.md#open-questions))

## Nonblocking details before execution

- Define the escalation event, notification channel, timestamps, delivery-failure handling, and evidence required for a valid ruling. Acknowledgment or a request for more time must not silently restart or extend the fixed deadline.
- Specify handling of timely but still inconclusive responses and multiple findings on a task without weakening the no-default-pass rule or freezing an invented confirmed defect.
- Define missing-judge and other global-cutoff outcomes, preserving assigned denominators and the prohibition on late scored grading.
- Propose the numeric coverage floor, qualified case inventory, distinct-task/repeat counts, and both-stage allocations within the two-judge, one-repair, 10-hour, USD 100 envelope. If infeasible, return for the required scope decision.
- Complete resource reservations, exact templates, comparator and judge configurations, calibration, accounting, statistical evidence rules, whole-stack security qualification, and separate execution authorization.

These details implement settled choices; they do not authorize changing the timeout, unanswered-dispute outcome, breadth-first minimum, no-compensation rule, or selected scope. ([Decision log: Open questions](DECISIONS.md#open-questions), [PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `f60569abcacda087e8e2eeb3c975264f7aaa60d6cfff35664640e6a0cb5c6fda` |
| `PLAN.md` | `b46d7b0e53b229692021f05fc09730911c054b619e80648f453869a02d942255` |
| `BENCHMARKS.md` | `9cb51de2e2caac9ffc302472f16e8d9184067ffff21a44d633cbbb42bb109e46` |
| `ANALYSIS.md` | `b3daea69aa4d4201bf5108927d28fcabecd339f2106b563b7b91c7498fc679ab` |
| `DECISIONS.md` | `4592ed4db411f465c166075fbb4f103d23f9d30ac33f963c76b9d88a364e9983` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to substantive documents require renewed review.

## Limits

- This is an independent read-only document review, not execution or expenditure approval, runtime certification, a benchmark result, or a guarantee of improved outcomes.
- I performed no installation, benchmark execution, model runtime test, penetration test, implementation audit, cost simulation, or feasibility trial. None is required for this documentation-only update.
- I did not run or certify repository gates. They remain the integrating agent's separate responsibility.
- No external research was performed for these owner-decision changes. Earlier source checks were selective, not exhaustive verification of all benchmark descriptions, licenses, dependencies, or execution requirements.
- Fidelity was assessed against supplied owner decisions and review context, not an independently authenticated transcript of every historical discussion.
- I did not change or independently verify the remote state of PR #3, either branch, or main.

**Final disposition: SHIP the fingerprinted documentation through the existing PR workflow, subject to separately run repository gates. No pilot execution or expenditure is authorized.**
