# Evaluation 1 analysis

Design analysis, not experimental results | 23 September 2026

## What the evaluation can establish

The client-facing goal requires separating three claims: a workflow can complete specified tasks, it improves on a declared comparator, and its controls behave as required under tested failure conditions. Passing one does not establish the others.

The existing model-mesh repository presents its routing rationale as heuristics and disclaims general quantitative quality and cost guarantees. Evaluation should produce evidence for narrower claims rather than remove those caveats pre-emptively. [Model-mesh repository](https://github.com/bughunt8/model-mesh)

A future client statement must identify the evaluated scope, model and harness versions, task population, controls, comparator, sample size, failures, and uncertainty. Successful historical projects can demonstrate experience, but cannot by themselves identify which part of the method caused improvement.

## Distinguish the experiment's causes

The owner selected two separate stages: isolate the disciplined loop first, then the additional effect of role-specific routing. Portability and optional parallel orchestration remain later proposed comparisons. Changing all four at once gives a system comparison, not an estimate of the method's individual contribution.

Use the matched single-model reference for the staged comparisons in [PLAN.md](PLAN.md), with exact configurations still to be agreed. If a human-led or already multi-model operational reference is later added, report it separately and limit its attribution to whole-system differences. Do not substitute it for either selected controlled stage.

Use `arm-baseline`, `arm-method`, and `arm-routing` in a future protocol to avoid confusion with A-prefixed scenario IDs. These are labels only; no experiment runner is being introduced.

Portability requires a second harness to meet the same mandatory contract, not merely accept the same prose. Orca documents coordinating multiple CLI agents and worktrees, while Pi exposes distinct runtime, model-API, and coding-agent components; these occupy different layers and should not be treated as interchangeable benchmark contestants. [Orca](https://github.com/stablyai/orca), [Pi](https://github.com/badlogic/pi-mono)

Git worktrees share repository data and normally configuration, while providing separate checkout state. They do not document the process, network, or credential boundary required by this plan. [Git worktree documentation](https://git-scm.com/docs/git-worktree)

## Coverage across selected scenarios

SWE-bench Verified supplies repository issue-resolution tasks with issue-specific and regression tests. That supports A01, but does not establish that it is a dedicated refactoring or security-audit benchmark. [SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)

GAIA supplies general-assistant questions involving reasoning, browsing, multimodal handling, and tools, and withholds some answers for its leaderboard. Treat it as a candidate source for suitable A08 or A12 tasks only after inspecting accessible subsets, not as proof of complete data-analysis or office-work coverage. [GAIA](https://ai.meta.com/research/publications/gaia-a-benchmark-for-general-ai-assistants/)

TheAgentCompany includes simulated professional work and result/subcheckpoint evaluation. Its task inventory is a candidate for A08, A11, and A12, but each selected subset still requires inspection. [TheAgentCompany](https://github.com/TheAgentCompany/TheAgentCompany)

Propose supplemental cases for A03, A05, and A09. Do not quietly replace an unrepresented scenario with a loosely related benchmark score. In particular:

- **Refactoring.** Specify the preserved contract and independent differential tests. A cleaner-looking patch with a changed edge case fails.
- **Security audit and remediation.** Use controlled vulnerabilities, independent exploit checks, severity adjudication, and false-positive accounting. Safe execution boundaries are prerequisites for these cases.
- **Architecture planning.** Freeze a brief and exact output template, then have independent AI judges assess traceability, feasibility, and contradictions, with human dispute resolution. Document the supporting evidence and disagreement; a bare model score is not sufficient.

Supplemental case construction is a proposal awaiting the final protocol. It is not already performed, approved for execution, or an official score from a selected public benchmark.

## Define defects before optimizing anything

The primary objective is fewer defects, not a higher completion score alone. Report both task-level outcomes and severity-specific defect outcomes across the full assigned population.

The scored defect outcome is the final frozen deliverable after at most one repair cycle, not first-handoff quality. Distinguish final defects, false acceptance, escaped defects within a declared observation window, incomplete tasks, and correct safe refusals. Retain repair traces for audit without creating a separate first-handoff defect target. Do not reward a system that avoids defects by refusing every feasible task; completion, required behavior, and safety must be interpreted together.

No human rescue is permitted during scored work. Repair feedback uses both executable checks and agent review, with the same declared access rules within a comparison and no hidden final-evaluator information. Exact checks, review prompts, and configurations remain to be pinned. Do not mistake a reviewer's unsupported finding for a confirmed defect.

Hold the repair-reviewer configuration constant within the method-effect comparison so that adding a different reviewer is not an undeclared intervention. In the routing stage, explicitly identify any reviewer-role routing change as part of the treatment. Final-grading procedures must remain independent and matched; comparable permissions do not require feedback content to be identical on different outputs.

After initial submission, one repair opportunity is a maximum, not an instruction to use the final evaluator repeatedly. Final submission freezes the scoreable artifact; hidden final-evaluator findings cannot reopen the attempt. At a repair or resource limit, retain the failure even if a later separately authorized rescue succeeds.

Within each scenario, freeze what counts as an opportunity for failure and how duplicate findings are deduplicated. Do not compare defect counts across tasks of very different scope without their task-level denominators.

Do not average a defect away with successes. The owner selected failure for any confirmed defect, including cosmetic defects. Severity classification remains useful for explanation, but no severity category is exempt from task failure. Two independent AI judges assess final outputs and the owner personally resolves disputes; exact judge configurations, response procedures, and detailed reference/template artifacts remain open.

This strict rule uses an exact reference or template frozen before execution, not general constraints permitting varied presentations. Predeclare variable fields, exceptions, comparison representation, and any normalization; do not add them after observing failures. A reference violation can fail a task, while an evaluator's new style preference cannot.

The presentation contract must be visible equally to competing arms without exposing hidden expected answers or completed solutions. Keep template conformance distinct from correctness so that literal imitation of a reference cannot stand in for solving the task.

Report unconfirmed or disputed findings explicitly until the human adjudicator resolves them on the frozen output. Adjudication supplies no hints to workers, alters no deliverable, and does not reopen repair. Record its human minutes, waiting time, and cost under the declared accounting rules. Never promote uncertainty to a pass or describe a scoped zero-confirmed-defect observation as proof that no defects exist.

The owner response window is eight elapsed minutes from recorded dispute escalation, truncated by the global deadline. An unanswered dispute freezes as unresolved and not accepted. Keep that reason distinct from a confirmed defect while retaining the task in assigned-outcome reporting; do not exclude unresolved tasks to inflate accepted-delivery rates. Later adjudication cannot replace the frozen scored result. Dispute frequency and response delays may affect delivery and attention measurements, so report them rather than attributing every unresolved case to model defects.

Agreement between AI judges can still be wrong. Before execution, define calibration cases, independence controls, and any validation sampling. Those details remain proposals; this selection does not silently authorize human review of every task or an unapproved recurring validation workload.

The official benchmark result and stricter local task acceptance are distinct outcomes. A benchmark pass may be a local failure due to a confirmed cosmetic defect or policy breach. Both results should remain visible.

## Resource-cap classification

Caps are predeclared by scenario or difficulty class, with identical values for competing arms on the same task. Define the class taxonomy and assignment procedure before scored execution. Do not reclassify failed or expensive tasks to obtain a larger allowance.

The one-cycle limit applies within the total task envelope, not as a fresh allowance added after initial work. Numeric task-level time, token, monetary, tool-call, concurrency, and retry caps remain undecided but must fit within the aggregate 10-hour and USD 100 ceilings. Class-specific results must stay visible so that different class mixes cannot conceal an objective regression.

The monetary and elapsed-time caps are feasibility constraints, not evidence that the full selected scope can be completed or that the sample will support a comparative claim. Count both judge calls and likely dispute workload in design estimates. If adequate coverage or evidence cannot fit, propose a bounded subset or deferral rather than quietly weakening controls, dropping one judge, or extending the pilot.

Minimum breadth, then depth now has a feasibility floor of two distinct cases per selected scenario, fourteen distinct cases across the pilot before repeats. This is a minimum, not a final powered sample size or a promise that the limits accommodate it. Case selection, counts beyond the floor, repeats, and both-stage allocations remain open. Assign each floor case one primary scenario; reuse across arms or stages and repeated runs cannot inflate distinct-case coverage. An infeasible floor requires an owner scope decision before execution. Sparse coverage may support feasibility observations while leaving comparative improvement inconclusive; breadth alone does not establish statistical adequacy.

Distinctness depends on the underlying task, not a new case ID. A materially different defect, dataset problem, brief, target-system task, or office workflow may qualify in the same repository or application. Paraphrases, cosmetic variants, revision changes, and seeds alone do not. Freeze task identities and distinctness reasons before results. Distinct tasks can still be correlated, so this counting rule is not evidence that all fourteen observations are statistically independent.

The floor applies across the whole pilot and now consists of two routine cases per scenario. Declare routine eligibility before selecting cases and observing results. A routine-only sample does not establish challenging-case reliability or representativeness of the full client workload. Failed or unexpectedly difficult cases retain their assigned outcomes; the routine label cannot be revised after results to remove failures.

Keep each scenario's two-case floor together in one stage, dividing the seven scenarios between the required method and routing stages. The specific partition remains open, and both stages must receive scenarios. Each case still receives matched competing-arm attempts within its assigned stage; the two different cases are not substitutes for a matched comparison. Preserve a scenario-by-stage matrix. Evidence for a scenario in one stage cannot stand in for the other stage's missing comparison, and a difference between stage aggregates cannot be attributed to method versus routing when their scenario populations differ.

The routine-work choice does not waive mandatory security qualification, boundary attacks, evidence-tampering checks, or any-confirmed-defect acceptance. Those controls remain separate gates, not optional challenging productivity cases to omit under the new sampling scope.

Ten hours is a continuous window starting with the first scored-task dispatch. Queues, grading, and waits for the owner's decisions consume it; they do not pause it. Setup precedes the clock, but solving scored tasks in advance cannot be relabeled as preparation. This is not an active-human-time allowance.

USD 100 includes all new pilot model/tool/compute charges, including setup and cleanup even when outside the scored clock. Per-task and per-stage allocations draw from that aggregate balance. Pre-existing sunk expenditure and owner labor remain visible in economic cost accounting without being falsely counted as new pilot charges.

Pending disputes at the deadline cannot be treated as accepted results, nor can further scored grading extend the clock. Classification of other pending, in-flight, unstarted, and missing-judge tasks, plus shutdown mechanics, remains open; the unanswered-dispute outcome is settled. Reserve resources and money for safe stopping and cleanup before admitting more work; a late invoice or post-run storage charge still belongs to the cash ledger if incurred by this pilot.

## Human attention and cost boundaries

All active owner pilot effort is the headline attention measure, including preparation/setup, briefing, supervision, safety intervention, independent evaluation, dispute resolution, record keeping, and cleanup. Being experiment-only or outside the scored clock does not exempt active effort. Passive waiting is elapsed time, while active monitoring during a wait consumes attention. Report the raw total and category breakdowns; the operational-only subset is diagnostic, not a replacement headline.

Use an owner-operated timer plus a tagged activity log and reconcile the two. Keep original entries and explained corrections. A missed start or stop leaves the interval missing, not estimated, reconstructed, or zero. Existing valid timer evidence may support a label or transcription correction, not an invented duration. Overlapping entries must not duplicate active minutes. Time spent recording and reconciling is itself included, and equivalent recording procedures apply across arms.

When intervals are missing, the observed sum is incomplete, not the true all-pilot attention total. Report gaps and affected comparisons, retaining all assigned task outcomes rather than excluding inconvenient tasks. The affected attention comparison is inconclusive unless an owner-approved missing-data threshold and analysis procedure were frozen before runs; none is agreed yet. Such a procedure cannot impute missing durations, hide missingness, select exclusions after outcomes, or turn unassessable regression risk into a pass. Do not assume missing records are random or affect both arms equally.

Keep four ledgers distinct:

| Ledger | Proposed contents | How it affects interpretation |
|---|---|---|
| Operational delivery | Frozen briefing, supervision, ordinary final review, agent reviewer calls, the single permitted agent repair, safety interventions, tool and inference usage. | Counts in workflow attention, time, and cost. Normal model-mesh review is not experiment-only overhead; human coaching is prohibited during scored attempts. |
| Independent evaluation | Hidden tests, benchmark grading, independent defect adjudication, simulator calls used only for evaluation, and experimental record keeping. | All active owner effort counts in headline attention, with a separate category breakdown; apply equivalent evaluation requirements to comparison arms. |
| Setup and qualification | Adapter work, installation audit, sandbox qualification, environment provisioning, and operator training before scored-task dispatch. | Active owner effort counts in headline attention, and new model/tool/compute charges count toward USD 100 despite being before the runtime clock. Any economic amortization needs a declared horizon and does not erase observed active minutes. |
| Separately authorized rescue | Post-score recovery under a separate run identity, with any human effort, tools, and inference explicitly attributed. | Cannot change the scored failure, success denominator, or accepted-delivery result. Report separately and include in disclosed all-in observed expenditure. |

If one action serves both delivery and evaluation, predeclare the allocation rule and report it once. Shared setup, evaluation, or simultaneous task monitoring must not produce duplicated owner minutes across tasks, arms, or stages. Publish the raw pilot total alongside attributed comparisons; a raw total across different populations alone cannot establish an attention improvement. Include active owner effort for any separately authorized rescue that remains part of this pilot, with its separate identity and immutable original outcome. Disclose separate follow-on effort separately. Do not move inconvenient effort or costs between ledgers after seeing results.

The lower-total-cost objective must have a declared scope and horizon. A low steady-state token bill does not establish lower total adoption cost when setup, review, cleanup, or later rescue effort is omitted. Show the bounded scored comparison and broader observed expenditure separately. The all-new-charges USD 100 cap is not a valuation of owner time; no hourly rate or amortization horizon has been agreed.

## Enforce the no-trade-off instruction

No weighted utility score is proposed. All mandatory controls must pass, and no accepted regression in any of the four objectives is compensated by another improvement. Assess improvements in order: defects, attention, accepted-delivery time, total cost.

Exact equality of stochastic outcomes cannot be proven from a finite sample. The protocol must agree measurement resolution and an evidence standard without silently allowing positive regression margins. If the evidence cannot support a required condition, the conclusion is inconclusive.

Separate permission to conduct a safe, bounded experiment from permission to claim an improvement or adopt a production workflow. A benchmark qualification failure means deferral; a result too uncertain to support an adoption claim does not magically become a pass.

## Security feasibility is part of benchmark selection

TheAgentCompany's documented setup and evaluation include privileged operations, host-network task containers, and permissive container-control socket configuration. Its selection therefore requires an independently reviewed execution design rather than literal use of the upstream quickstart. [TheAgentCompany](https://github.com/TheAgentCompany/TheAgentCompany)

Apply policy to installers, coordinators, evaluators, simulated colleagues, tool servers, and task workers. No privileged benchmark component may be placed on the user's or a shared host merely because it sits outside the nominal agent process. Necessary privilege inside a separately approved disposable boundary must be qualified before execution.

Separate trusted evaluation evidence from worker-writable files. A correct final answer cannot compensate for an unapproved recipient, compromised evaluator, or green test result from the wrong revision.

## Proposed claim ladder

| Evidence available | Claim that may become supportable | Claim still unsupported |
|---|---|---|
| Reviewed specification only | A documented, independently critiqued evaluation plan exists. | The system is secure, effective, or production-ready. |
| Qualified adapter and negative-control tests | Named controls passed specified tests on a pinned setup. | Every bypass is impossible or every harness is supported. |
| Reproducible benchmark run | The named setup achieved the reported results under the declared conditions. | Equivalent performance on all client work. |
| Matched comparison with sufficient evidence | The selected objective improved against the declared comparator, subject to no-regression gates. | Unmeasured components caused the improvement. |
| Audited project cases | The documented scope succeeded with the stated contribution, effort, constraints, and failures. | Universal client outcomes or guaranteed savings. |

These are proposed limits on future claims, not claims that the later evidence already exists. Publication of case-study material remains a separate approval and confidentiality decision.
