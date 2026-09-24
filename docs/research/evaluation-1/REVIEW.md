# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 25 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker or required correction was found in the D41 update. Continuing the planned sample after an ordinary acceptance failure is consistently distinguished from accepting that task, changing its score, approving adoption, or authorizing execution. Mandatory safety and resource stops retain precedence. ([PLAN.md](PLAN.md#bounded-repair-and-final-evaluation), [ANALYSIS.md](ANALYSIS.md#define-defects-before-optimizing-anything), [DECISIONS.md](DECISIONS.md#settled-decisions))

## Scope and method

I reviewed the complete uncommitted diff and the five substantive documents on local branch `evaluation-1`, based on HEAD `96c7247b482eeb95cc97ad24f257afe72bd12e25`. The commit identifies the baseline, not the reviewed working-tree content.

I checked the D41 wording against the supplied owner decision, read the prior review, examined related stop, acceptance, repair, safety, denominator, resource, and authorization rules, and verified that all five committed baseline documents match the preceding D40 review's fingerprints. I made no target-file, branch, or git-state changes.

This report is authored outside the repository for incorporation as `REVIEW.md`. It covers documentation, not an implemented controller or an authorized pilot.

## Prior review history

The original two-document review returned REVISE for R1 through R3. After correction, the two-document package received SHIP for documentation only. Reviews of the expanded package and subsequent owner decisions through D40 also returned SHIP within that boundary. Earlier nonblocking wording notes were corrected and independently rechecked. This history does not constitute evidence of runtime performance or safety.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording allowed compensated regressions and weakened mandatory controls. | High | Resolved. All mandatory controls and evidence remain required; no objective regression may be compensated by another improvement, and uncertainty cannot silently pass. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. Client purpose and priorities remain fixed, and useful-work discovery remains deferred. ([Plan: Agreed priorities](PLAN.md#agreed-priorities), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review omitted parts of the execution stack. | High | Resolved. Installers, coordinators, evaluators, simulated users, tools, and workers share the mandatory security boundary; unmet controls require deferral rather than waiver. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The expanded-package review retained B01 SWE-bench Verified, B06 GAIA, and B10 TheAgentCompany, the seven selected scenarios, all original menu options, and explicit supplemental coverage gaps without claiming that benchmark selection certifies coverage. ([BENCHMARKS.md](BENCHMARKS.md))

Previously reviewed decisions remain in force:

- D14 through D18 establish method-first and routing-second comparisons, post-bounded-repair scoring, at most one repair within the matched envelope, no scored human rescue, frozen failures, and separately authorized unscored rescue that cannot rewrite outcomes. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D19 through D25 retain checks plus agent-review feedback without hidden evaluator information, failure for any confirmed defect including cosmetic defects, class-based matched caps, exact templates with advance exceptions, two independent final AI judges, and personal owner dispute resolution after artifact freeze. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D26 through D29 retain the continuous 10-hour clock from first scored dispatch and a global USD 100 ceiling for all new pilot model/tool/compute charges, including setup and cleanup, with no hidden pre-clock solving or spending permission. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [DECISIONS.md](DECISIONS.md))
- D30 through D33 retain the eight-minute dispute window capped by the global deadline, unresolved/not-accepted timeout outcomes, minimum breadth before depth, whole-pilot coverage with matched stage-local claims, and all active owner attention without duplicated minutes. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))
- D34 through D37 retain two distinct underlying tasks per scenario, fourteen across the pilot, timer-plus-log attention recording, no requirement for different contexts, and missing rather than estimated or zero forgotten intervals. No missing-data analysis exception is currently agreed. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [DECISIONS.md](DECISIONS.md))
- D38 and D39 retain two routine cases per scenario, routine eligibility fixed before selection and outcomes, intact scenario pairs within one stage, both competing arms on every case, and mandatory adversarial security qualification. ([PLAN.md](PLAN.md), [BENCHMARKS.md](BENCHMARKS.md))
- D40 fixes method scenarios A01/A03/A05/A09 and routing scenarios A08/A11/A12. Eight method cases and six routing cases give fourteen matched comparisons and twenty-eight initial arm attempts before repeats, not twenty-eight independent tasks or proof of feasibility or statistical power. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))

## Current findings

### D41 matches the owner choice

The plan explicitly continues predeclared comparisons after ordinary acceptance failure in either arm, including a confirmed cosmetic defect, and completes the planned matched counterpart only when safe and within limits. The same rule applies to all arms and both stages, so a baseline failure and a treatment failure do not receive different continuation policies. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation))

The README, benchmark rules, analysis, and decision log reflect the same choice. D41 and the superseded-proposals table reject stopping the entire pilot solely because of its first ordinary acceptance failure. O11 asks for operational safety-stop procedures rather than reopening this settled continuation choice. ([README.md](README.md#settled-scope), [BENCHMARKS.md](BENCHMARKS.md#rules-already-settled), [ANALYSIS.md](ANALYSIS.md#define-defects-before-optimizing-anything), [DECISIONS.md](DECISIONS.md))

### Continuation does not change acceptance or adoption

Failures remain frozen and reported in assigned-outcome evidence. A later success cannot repair an earlier score, and official benchmark grades remain separate from stricter local acceptance. Continuing evidence collection neither demonstrates improvement nor permits a compensated regression. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [ANALYSIS.md](ANALYSIS.md#define-defects-before-optimizing-anything), [BENCHMARKS.md](BENCHMARKS.md#rules-already-settled))

The any-confirmed-defect rule still applies to the final frozen artifact. Unresolved findings remain distinct from confirmed defects, and an unanswered dispute remains unresolved and not accepted rather than becoming a pass or a newly confirmed defect. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance))

### No added attempts, substitutions, tuning, or evaluator leakage

D41 prohibits extra repair or reruns, replacement cases, configuration changes, and hidden final-evaluator feedback to subsequent scored workers. The existing one-repair rule, independent final evaluation, clean environments, and exclusion of previous solutions and traces from later contexts remain in force. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty), [ANALYSIS.md](ANALYSIS.md#define-defects-before-optimizing-anything))

Once the predeclared sample is exhausted, continuation provides no authority for additional trials. Planned matched counterpart attempts are part of the original comparison, not replacement or rescue attempts; any repeats still require prior approval and resource allocation. ([PLAN.md](PLAN.md#bounded-repair-and-final-evaluation), [DECISIONS.md](DECISIONS.md#settled-decisions))

### Safety uncertainty and resource limits still stop work

The plan expressly forbids relabeling an actual or unresolved mandatory-control problem as an ordinary task failure to keep running. It also avoids the opposite mistake of treating every task-quality defect as proof that a runtime control failed. Events must be classified against frozen criteria with evidence retained. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [ANALYSIS.md](ANALYSIS.md#define-defects-before-optimizing-anything))

Mandatory safety stops, task limits, and global time/cash ceilings override continuation. The existing requirements for reservations, bounded charges, safe termination, and no scored work or grading after the global deadline are unchanged; coverage truncated by a safety or resource stop must be reported. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [ANALYSIS.md](ANALYSIS.md#define-defects-before-optimizing-anything))

### Dates and authority remain accurate

All five document headers now identify 25 September 2026, and the plan is v0.15. The benchmark research retains its separate 22 September 2026 review date, so the new decision date does not claim fresh verification of external sources. ([README.md](README.md), [PLAN.md](PLAN.md), [BENCHMARKS.md](BENCHMARKS.md#ten-researched-benchmark-options), [ANALYSIS.md](ANALYSIS.md), [DECISIONS.md](DECISIONS.md))

No new implementation, dispatch, spending, human-rescue, benchmark qualification, or adoption authority is introduced. The existing PR #3 workflow, no-direct-main boundary, and requirement for separate execution approval remain explicit. ([README.md](README.md#status-and-boundaries), [DECISIONS.md](DECISIONS.md#change-protocol))

## Nonblocking details before execution

The following are execution prerequisites, not reasons to block this documentation update:

- Freeze the event-classification criteria, safety escalation and stop procedures, and evidence required to distinguish task failure from an actual or unresolved control problem.
- Approve actual routine cases, task identities, case-level manifests, order/counterbalancing, repeats, and class-level limits under the settled D40 mapping and D41 continuation rule.
- Pin comparator configurations, visible repair feedback, templates, two judge configurations, calibration, evidence access, and dispute notification mechanics.
- Specify enforceable time/cash reservations and cutoff classifications for pending, in-flight, unstarted, and missing-judge work without extending scored time or changing frozen outcomes.
- Define attention attribution, statistical evidence standards, and economic-cost accounting without inventing missing durations or silently allowing a regression margin.
- Qualify the complete execution stack and obtain separate execution authorization; return for a scope decision if the floor cannot fit safely.

These details remain open in the plan and decision log; they do not reopen ordinary-failure continuation or the settled limits. ([Decision log: Open questions](DECISIONS.md#open-questions), [Plan: Measurement interview](PLAN.md#measurement-interview))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `e4e56742cfc4cc303072255aef489397a2c29ba07c2aa0945b6766bf74af988e` |
| `PLAN.md` | `3bed4990dff23e8846f3610f489fc3ec0d8906679324cc31cd7cc1ea7648d142` |
| `BENCHMARKS.md` | `ca6a3e1e7f9de93051e441ae3d9a4a65528556d2ad976ab8b9a4d02841bc497e` |
| `ANALYSIS.md` | `df1247ddf15999700fbb89e6a3688264061f4bd12451a23b0aa27a24a4ed372e` |
| `DECISIONS.md` | `7ae29026968042acfc1b134f9218b2349fe4a4b66ee31796d5fc871fc0ef914f` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to substantive documents require renewed review.

## Limits

- This is an independent read-only documentation review, not an implementation audit, runtime certification, execution or expenditure approval, benchmark result, or guarantee of improvement.
- No installation, benchmark execution, model runtime test, penetration test, timing trial, cost simulation, or feasibility trial was performed. None is required for this docs-only change.
- Repository gates were not run or certified. They remain the integrating agent's responsibility before updating the original PR.
- No external research was performed for D41. Earlier source checks were selective, not exhaustive verification of every benchmark, dependency, license, or execution requirement.
- Fidelity was assessed against supplied owner decisions and the review history, not an independently authenticated transcript of every historical discussion.
- Remote PR and branch states were not independently verified or changed.

**Final disposition: SHIP the fingerprinted documentation through the existing PR workflow, subject to separately run repository gates. No pilot execution or expenditure is authorized.**
