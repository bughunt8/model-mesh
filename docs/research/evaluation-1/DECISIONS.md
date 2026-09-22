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

## Superseded or constrained proposals

| Proposal | Disposition |
|---|---|
| Reopen the usefulness question or require actual useful-project examples immediately. | Rejected by D06. |
| Use a cost or attention gain with an acceptable quality regression. | Rejected by D04 and independent review; all objective regressions cannot be compensated by gains elsewhere. |
| Treat an upstream benchmark quickstart as authorization for host privileges. | Rejected by the security boundary and independent review. Qualify the complete stack or defer it. |
| Prefer other benchmark or scenario options based on the drafter's shortlist. | Owner selections D09 and D11 take precedence. Retain other options as research only. |
| Replace PR #3 with a new evaluation PR. | Superseded by D13 before a replacement PR was created. |
| Use an illustrative coding-only sample size for the entire evaluation. | Removed. Sample allocation must follow the selected scenario mix and evidence requirements. |

## Open questions

These remain genuinely unresolved. Their presence does not prevent a documentation PR; they do prevent an execution-ready protocol or adoption claim.

| ID | Question to resolve | Decision needed before |
|---|---|---|
| O01 | What comparator supports the intended claim: a matched single-model setup, current complete workflow, or absolute qualification criteria? | Final experiment design and any improvement claim. |
| O02 | What constitutes a defect for each selected scenario, how is severity assigned, and what is an automatic failure? | Task and evaluator freeze. |
| O03 | Who independently adjudicates findings, false positives, and disagreements between tests or judges? | Evaluation approval. |
| O04 | How are active owner attention and operational review separated from experimental adjudication? | Measurement instrumentation. |
| O05 | What evidence standard distinguishes improvement, regression, and inconclusive results without unauthorized regression margins? | Sample-size choice and preregistration. |
| O06 | Which data classes, recipients, jurisdictions, retention rules, and tool permissions apply? | Any real-data or networked execution. |
| O07 | Which second harness, pinned release, and adapter contract should test portability? | Adapter implementation authorization. |
| O08 | Which exact benchmark releases, splits, task subsets, graders, and simulator configurations are available and appropriate? | Environment freeze. |
| O09 | Can TheAgentCompany meet the complete security boundary without unsafe privileges on the user/shared host? | Its installation or execution. |
| O10 | Which supplemental refactoring, security, and architecture cases are needed, and how will they be independently graded? | Coverage approval. |
| O11 | What budget, concurrency, retries, time limits, stopping rules, and sampling plan apply? | Execution authorization. |
| O12 | What time horizon and allocation rules define total cost, including setup and qualification? | Any total-cost comparison. |
| O13 | Which project case studies may later be used, and what may be published? | Case-study disclosure; deferred for now. |

## Change protocol

Append new owner decisions rather than erase their history. Mark superseded entries with the replacing decision. Update the plan and analysis when a decision changes scope, controls, evidence, or claims.

Propose all updates on `evaluation-1` and synchronize the original PR branch to the same reviewed commit. Require independent review of material changes and run repository gates before updating the PR. A merged documentation proposal does not authorize pilot execution.
