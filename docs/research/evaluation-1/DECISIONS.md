# Evaluation 1 decision log

Status as of 22 September 2026 | Planning only

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
| D21 | Structure time and resource caps by scenario or difficulty class. | Settled. Assign classes before scored outcomes, match caps across arms on the same task, and decide numeric values before execution. |
| D22 | Use independent AI judges; a human resolves disagreements or uncertain defect findings on frozen final outputs. | Settled. Human adjudication is not rescue, may not edit outputs, and cannot reopen repair. Judge configuration, calibration, adjudicator identity, and timing remain open. |
| D23 | Grade cosmetic correctness against an exact reference or template, with exceptions declared in advance. | Settled. Freeze the comparison contract before execution; do not expose hidden answers through task-visible formatting templates. Specific artifacts and variable fields remain to be agreed. |

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

## Open questions

These remain genuinely unresolved. Their presence does not prevent a documentation PR; they do prevent an execution-ready protocol or adoption claim.

| ID | Question to resolve | Decision needed before |
|---|---|---|
| O01 | Which exact model, harness, prompts, tools, reasoning settings, visible checks, and agent-review procedures define each selected controlled comparison? | Environment and protocol freeze; stages and feedback categories are settled. |
| O02 | Which versioned references/templates, declared variable fields/exceptions, comparison representation, and correctness criteria define defects in each scenario? | Task and evaluator freeze; exact-template grading and every-confirmed-defect failure are settled. |
| O03 | Which independent AI-judge configurations, calibration/validation procedures, human adjudicator, response window, and unresolved-result disposition implement D22? | Evaluation approval; AI judges with human dispute resolution are settled. |
| O04 | How are active owner attention and operational review separated from experimental adjudication? | Measurement instrumentation. |
| O05 | What evidence standard distinguishes improvement, regression, and inconclusive results without unauthorized regression margins? | Sample-size choice and preregistration. |
| O06 | Which data classes, recipients, jurisdictions, retention rules, and tool permissions apply? | Any real-data or networked execution. |
| O07 | Which second harness, pinned release, and adapter contract should test portability? | Adapter implementation authorization. |
| O08 | Which exact benchmark releases, splits, task subsets, graders, and simulator configurations are available and appropriate? | Environment freeze. |
| O09 | Can TheAgentCompany meet the complete security boundary without unsafe privileges on the user/shared host? | Its installation or execution. |
| O10 | Which supplemental refactoring, security, and architecture cases are needed, and how will they be independently graded? | Coverage approval. |
| O11 | What class taxonomy, assignment procedure, numeric resource limits, broader safety stop rules, and sampling plan apply within the settled scenario/difficulty-class and one-repair envelope? | Execution authorization. |
| O12 | What time horizon and allocation rules define total cost, including setup and qualification? | Any total-cost comparison. |
| O13 | Which project case studies may later be used, and what may be published? | Case-study disclosure; deferred for now. |

## Change protocol

Append new owner decisions rather than erase their history. Mark superseded entries with the replacing decision. Update the plan and analysis when a decision changes scope, controls, evidence, or claims.

Propose all updates on `evaluation-1` and synchronize the original PR branch to the same reviewed commit. Require independent review of material changes and run repository gates before updating the PR. A merged documentation proposal does not authorize pilot execution.
