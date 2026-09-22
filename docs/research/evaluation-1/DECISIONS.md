# Evaluation 1 decision log

Status as of 23 September 2026 | Planning only

This log records owner instructions and explicit selections from the planning discussion. It does not treat the drafter's recommendation as approval. Ordering preserves the sequence of decisions; dates use Hong Kong time.

## Settled decisions

| ID | Decision | Status and effect |
|---|---|---|
| D01 | Address adoption risk, auditing, guardrails, and a method independent of oh-my-openagent. Consider Orca, Qwen Code, Pi, and worktree-based execution. | Settled direction. No alternative harness is selected or qualified yet. |
| D02 | Prepare a pilot plan without implementing it. Continue probing measurement definitions until there is shared understanding. | Settled boundary. No installs, adapters, benchmark runs, runtime changes, or deployments authorized. |
| D03 | Supply 12 scenario options and 10 researched benchmark options for multi-selection, including non-coding work. | Delivered menus retained in BENCHMARKS.md. |
| D04 | Priorities, high to low: fewer defects, less owner attention, faster accepted delivery, lower total cost. No compensating trade-offs. | Settled. No blended score or silent regression allowance. |
| D05 | First business purpose: offer model-mesh to clients using successful projects of the owner's own as evidence. | Settled audience and purpose. Does not authorize claims of causality without evidence. |
| D06 | Usefulness is already established; ignore useful-work discovery for now. | Settled correction. Do not require personally useful tasks or project selection as a prerequisite for benchmark selection. |
| D07 | Raise a PR instead of making direct changes to main. | Settled change boundary. Documentation is proposed, not merged. |
| D08 | Require independent adversarial review. | Settled. Review implementation-independent claims, methods, and controls; do not interpret a docs-only SHIP as runtime certification. |
| D09 | Select B01 SWE-bench Verified, B06 GAIA, and B10 TheAgentCompany. | Settled shortlist. Access, task-subset, evaluator, adapter, and security qualification remain mandatory. |
| D10 | Re-send the scenario menu after the first prompt expired; label it A01 through A12. | Supersedes T-prefixed display labels without changing scenario meanings. |
| D11 | Select A01 bug repair, A03 refactoring, A05 security audit and remediation, A08 data reconciliation and analysis, A09 requirements and architecture planning, A11 browser administration, A12 cross-application office work. | Settled scenario scope. A02, A04, A06, A07, A10 are not separately selected. |
| D12 | Create a new branch named `evaluation-1`; keep plan, analysis, research, all documentation, and a decision log there; independently review the package. | Settled repository organization. Package location: docs/research/evaluation-1/. |
| D13 | Update the original PR for this new organization rather than replacing it. | Settled. Retain PR #3 and its existing head branch; synchronize that branch to the reviewed `evaluation-1` commit. No second evaluation PR and no main update. |
| D14 | Establish both comparisons in separate stages: method effect first, then added routing effect. | Settled on 22 September 2026. Exact configurations remain open; D19 subsequently settles feedback categories. |
| D15 | Measure defect quality after bounded repair, rather than first handoff or both stages. | Settled. Do not add a separate first-handoff defect target; retain repair accounting and audit traces. |
| D16 | Permit one repair cycle after the initial submission, with the same cap on both sides of each comparison. | Settled. At most one cycle; all work within it remains subject to task-level resource limits. |
| D17 | No human rescue during scored attempts. | Settled. No coaching or fixes; humans may stop unsafe execution and evaluate frozen final results. |
| D18 | Count failure at the repair/resource limit; rescue separately. | Settled. Freeze the failure. Later rescue requires separate authorization, remains unscored and disclosed, and cannot revise the original result. |
| D19 | Permit both executable checks and agent review during the one repair cycle, excluding hidden final-evaluator information. | Settled. Exact visible checks, prompts, reviewer configuration, and delivery remain to be pinned. |
| D20 | Any defect, including cosmetic defects, fails final task acceptance, in addition to mandatory safety failures. | Settled. Use confirmed deviations from predeclared criteria; severity does not excuse a defect. This is not a guarantee of no undiscovered defects. |
| D21 | Structure time and resource caps by scenario or difficulty class. | Settled. Assign classes before scored outcomes, match caps across arms on the same task, and decide numeric task-level values within D26/D27 before execution. |
| D22 | Use independent AI judges; a human resolves disagreements or uncertain defect findings on frozen final outputs. | Settled. Human adjudication is not rescue, may not edit outputs, and cannot reopen repair. D24/D25 settle panel size and owner; judge configuration, calibration, and timing remain open. |
| D23 | Grade cosmetic correctness against an exact reference or template, with exceptions declared in advance. | Settled. Freeze the comparison contract before execution; do not expose hidden answers through task-visible formatting templates. Specific artifacts and variable fields remain to be agreed. |
| D24 | Use two independent AI judges per final deliverable. | Settled. Both must participate under the declared protocol; disagreement or uncertainty goes to the human dispute path. Exact models remain open. |
| D25 | The project owner will personally resolve disputes. | Settled. No delegated colleague or external reviewer is selected for this role. Active effort and waiting are recorded separately. |
| D26 | The 10-hour limit means total elapsed pilot runtime. | Settled after explicit clarification. It is not an active-adjudication allowance and does not reset per task, suite, or stage. D28 subsequently fixes clock boundaries. |
| D27 | Cap combined model, tool, and compute charges at USD 100 for the pilot. | Settled monetary ceiling and currency; no per-arm or per-suite reset. D29 subsequently fixes the all-new-charges boundary; allocations remain open. |
| D28 | Start the continuous 10-hour clock at first scored-task dispatch; include subsequent execution, queues, grading, and waits for owner decisions, with no pauses. | Settled. Preparation is before the scored clock, without hiding scored solving or evaluation there. |
| D29 | Count all new pilot-related model, tool, and compute charges toward USD 100, including setup, scored work, repairs, both judges, simulators, storage, and cleanup. | Settled. Being outside the scored clock does not exempt a new charge. Owner labor is separately measured. |
| D30 | Allow eight elapsed minutes for the owner's dispute ruling, capped by the global deadline if sooner. Without a timely ruling, freeze the task as unresolved and not accepted. | Settled. Measure from recorded dispute escalation; no clock pause, late score rewrite, or automatic confirmation of a suspected defect. Notification mechanics remain open. |
| D31 | Use minimum breadth, then depth when proposing sampling within the fixed limits. | Settled approach. D34 subsequently fixes the numeric floor; cases, repeats, and stage allocations need approval. If the floor is infeasible, return for a scope decision. |
| D32 | Apply the minimum coverage floor across the whole pilot, not separately to each comparison stage. | Settled. Stage subsets may differ, but both stages remain required; preserve matched comparisons within stages and limit each stage's claims to its tested scenarios. D34 fixes the floor; the stage matrix remains open. |
| D33 | Use all active owner pilot attention as the headline attention measure. | Settled. Include preparation/setup, briefing, supervision, safety intervention, evaluation, disputes, record keeping, and cleanup, with category breakdowns. Passive waiting is elapsed time, not active attention. D35 fixes the recording method; shared-effort allocation remains open and must not duplicate minutes. |
| D34 | Use two distinct cases per selected scenario as the feasibility floor before allocating remaining capacity to repeats. | Settled on 23 September 2026. At least fourteen distinct cases across the whole pilot, not per stage. Final case selection, repeats, additional cases, and stage allocation remain open. Infeasibility requires an owner scope decision, not silent reduction. |
| D35 | Record all active owner pilot attention with a timer plus activity log. | Settled on 23 September 2026. Owner-operated timer, activity tags, reconciliation, preserved corrections, and explicit missing/estimated intervals. Specific tooling and shared-effort attribution remain open; no recording system is implemented. |

## Superseded or constrained proposals

| Proposal | Disposition |
|---|---|
| Reopen the usefulness question or require actual useful-project examples immediately. | Rejected by D06. |
| Use a cost or attention gain with an acceptable quality regression. | Rejected by D04 and independent review; all objective regressions cannot be compensated by gains elsewhere. |
| Treat an upstream benchmark quickstart as authorization for host privileges. | Rejected by the security boundary and independent review. Qualify the complete stack or defer it. |
| Prefer other benchmark or scenario options based on the drafter's shortlist. | Owner selections D09 and D11 take precedence. Retain other options as research only. |
| Replace PR #3 with a new evaluation PR. | Superseded by D13 before a replacement PR was created. |
| Use an illustrative coding-only sample size for the entire evaluation. | Removed. Sample allocation must follow the selected scenario mix and evidence requirements. |
| Measure first-handoff and final defect quality as coequal outcomes. | Not selected. D15 chooses post-repair defect quality only. |
| Leave the number of repair cycles, human rescue, or failure overwrite policy open. | Superseded by D16 through D18. |
| Choose between test-only and agent-review-only repair feedback. | Superseded by D19; both categories are selected. |
| Accept minor or cosmetic defects when substantive requirements pass. | Rejected by D20. |
| Use one uniform cap for every task or assign caps only by benchmark suite. | Not selected. D21 chooses scenario or difficulty classes. |
| Require a human to judge every task, or use AI-only adjudication with no human dispute path. | Not selected. D22 uses AI judges with human dispute resolution. |
| Grade cosmetic correctness using only broad constraints that permit varied presentations, or an unspecified hybrid chosen afterwards. | Not selected. D23 requires an exact reference/template with advance exceptions. |
| Use three judges or delegate dispute resolution to a colleague or external reviewer. | Not selected. D24 and D25 choose two judges and the owner. |
| Interpret the owner's initial "10 hours" as active adjudication time or both time measures. | Superseded by D26's clarification: total elapsed pilot runtime. |
| Treat the overall cash amount or currency as undecided, or allocate USD 100 separately to each arm. | Superseded or prohibited by D27. |
| Start the clock when environment setup begins, or pause it during grading or owner waits. | Not selected or prohibited by D28. |
| Count only scored-run charges while excluding new setup or cleanup costs from the pilot ceiling. | Not selected. D29 includes all new pilot charges. |
| Wait 15, 30, or 60 minutes, or until the global deadline without a shorter dispute window. | Not selected. D30 chooses eight minutes, capped by the global deadline. |
| Prioritize breadth alone or silently reduce scope to maximize depth. | Not selected. D31 chooses minimum breadth, then depth, with an owner decision if the floor is infeasible. |
| Require the full seven-scenario floor independently in both comparison stages. | Not selected. D32 applies the floor across the whole pilot; no claim extends to an untested stage/scenario combination. |
| Use operational attention alone as the headline and omit setup or experimental adjudication. | Not selected. D33 includes all active owner pilot effort, while retaining separate categories. |
| Use one or three distinct cases per scenario as the minimum floor, or call repeated runs new cases. | Not selected. D34 chooses two distinct cases per scenario; more cases may be proposed without redefining the floor. |
| Use only a manual activity log or infer active minutes from interaction events alone. | Not selected. D35 chooses timer plus activity log; missing intervals must be flagged rather than silently inferred or treated as zero. |

## Open questions

These remain genuinely unresolved. Their presence does not prevent a documentation PR; they do prevent an execution-ready protocol or adoption claim.

| ID | Question to resolve | Decision needed before |
|---|---|---|
| O01 | Which exact model, harness, prompts, tools, reasoning settings, visible checks, and agent-review procedures define each selected controlled comparison? | Environment and protocol freeze; stages and feedback categories are settled. |
| O02 | Which versioned references/templates, declared variable fields/exceptions, comparison representation, and correctness criteria define defects in each scenario? | Task and evaluator freeze; exact-template grading and every-confirmed-defect failure are settled. |
| O03 | Which two AI-judge configurations, calibration/validation procedures, evidence access, and recorded escalation/notification mechanics implement final adjudication? | Evaluation approval; two judges, owner identity, eight-minute response window, and unanswered-dispute outcome are settled. |
| O04 | Which timer/log tool, fields, reconciliation cadence, missing-data procedure, and shared-effort allocation implement D35 without duplication? | Measurement instrumentation and comparative analysis; all-pilot scope and timer-plus-log method are settled. |
| O05 | What evidence standard distinguishes improvement, regression, and inconclusive results without unauthorized regression margins? | Sample-size choice and preregistration. |
| O06 | Which data classes, recipients, jurisdictions, retention rules, and tool permissions apply? | Any real-data or networked execution. |
| O07 | Which second harness, pinned release, and adapter contract should test portability? | Adapter implementation authorization. |
| O08 | Which exact benchmark releases, splits, task subsets, graders, and simulator configurations are available and appropriate? | Environment freeze. |
| O09 | Can TheAgentCompany meet the complete security boundary without unsafe privileges on the user/shared host? | Its installation or execution. |
| O10 | Which supplemental refactoring, security, and architecture cases are needed, and how will they be independently graded? | Coverage approval. |
| O11 | What class taxonomy, assignment procedure, numeric task-level limits, safety stop rules, case manifest, repeats, and scenario-by-stage matrix fit the settled envelope? | Execution authorization; the two-distinct-cases-per-scenario whole-pilot floor is settled, but final cases and allocations are not. |
| O12 | What time horizon and allocation rules define total cost, including setup and qualification? | Any total-cost comparison. |
| O13 | Which project case studies may later be used, and what may be published? | Case-study disclosure; deferred for now. |
| O14 | How are other pending, in-flight, unstarted, and missing-judge tasks classified at cutoff, and how do shutdown, evidence retention, and cleanup avoid extending scored execution? | Execution authorization; clock boundaries and unanswered-dispute classification under D30 are settled. |
| O15 | Which billing rates, allocation and reconciliation rules, and non-overlapping reservations cover in-flight calls, both judges, storage retention, and safe cleanup? | Execution authorization; all new pilot charges, including setup/cleanup, already count toward USD 100. |

## Change protocol

Append new owner decisions rather than erase their history. Mark superseded entries with the replacing decision. Update the plan and analysis when a decision changes scope, controls, evidence, or claims.

Propose all updates on `evaluation-1` and synchronize the original PR branch to the same reviewed commit. Require independent review of material changes and run repository gates before updating the PR. A merged documentation proposal does not authorize pilot execution.
