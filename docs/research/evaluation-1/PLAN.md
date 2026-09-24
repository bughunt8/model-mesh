# Model-mesh portable method and pilot plan

Discussion draft v0.15 | 25 September 2026 | Planning only

## Agreed priorities

Your confirmed priority order is fewer defects, less of your attention, faster accepted delivery, then lower total cost. Do not use a weighted score that allows lower-priority gains to compensate for higher-priority regressions. No compensating trade-offs are authorized.

Scenario and benchmark selections were made separately, including non-coding work. [The benchmark research and selection record](BENCHMARKS.md) supplies the original 12 scenarios and 10 benchmark options. [Analysis](ANALYSIS.md) records experiment-design implications, and [the decision log](DECISIONS.md) separates settled instructions from open questions.

The selected benchmark shortlist is B01 SWE-bench Verified, B06 GAIA, and B10 TheAgentCompany. All remain subject to access, evaluator, adapter, and security qualification. Selected scenarios are A01 regression bug repair, A03 behavior-preserving refactor, A05 security audit and remediation, A08 data reconciliation and analysis, A09 requirements and architecture planning, A11 browser administration, and A12 cross-application office work. Selection does not authorize execution.

The adoption purpose is now confirmed: offer model-mesh to clients, supported by measured success on your own projects. Prospective clients are the audience. Usefulness is established by your experience and is not the question this pilot needs to reopen.

For now, focus on evaluation scenarios and existing benchmarks that can substantiate defects, reliability, guardrails, and portability. Defer discovery or selection of personally useful work. Later client claims may combine measured project case studies and benchmark evidence, with their respective limits stated.

Two comparison stages are agreed: isolate the method first, then routing's added effect. Defect quality is measured after bounded repair, with at most one repair cycle after the initial submission, the same cap for both sides, and no human rescue. Any attempt still failing at its repair or resource limit is frozen and counted as a failure; separately authorized later rescue is unscored and cannot revise that result.

Both executable checks and agent review are permitted repair feedback. Any confirmed defect, including cosmetic defects, fails final task acceptance. Define the criteria before scoring; this is not a guarantee of no undiscovered defects. Resource caps are set by scenario or difficulty class and matched between arms on each task.

Two independent AI judges assess frozen final deliverables, with the project owner personally resolving disagreements or uncertain findings. Cosmetic grading uses an exact reference or template; any exceptions must be declared in advance. This is final evaluation, not human rescue.

The continuous 10-hour elapsed clock starts at the first scored-task dispatch. It includes subsequent execution, queues, grading, and waits for owner decisions, without pauses; preparatory setup occurs before the scored clock. USD 100 covers all new pilot-related model, tool, and compute charges, including setup, scored work, repairs, both judges, simulators, storage, and cleanup. These are aggregate limits, not per-task, per-benchmark, or per-stage allowances. Owner labor is measured separately.

Exact comparator configurations, defect criteria, versioned templates/references, judge configurations, dispute procedure, class-level limits, cutoff/cleanup mechanics, budget reservations, and adoption evidence requirements remain unresolved. Continued planning does not authorize implementation.

## Decision sought

Determine what defensible claims can be made about an already-useful engineering method's quality, reliability, guardrails, and portability for a client offer. Do not reopen whether the work is useful. Neither qualification nor portability should depend on accepting an entire repository or trusting a model's self-review.

For each proposed client case study, require a named scope, initial state, comparator, task outcomes, independently checked defects, your active attention, accepted-delivery time, full cost, and limitations. Include unsuccessful eligible tasks in the evidence even if the public case study focuses on a successful project. Retrospective project success without a suitable comparator cannot establish that model-mesh caused the improvement.

This document proposes architecture, controls, experiments, and measurement definitions. No implementation, installation, pilot execution, repository modification, AWS deployment, or new scheduled task is authorized by this plan. The continuous 10-hour clock and all-new-charges USD 100 ceiling are settled; sample sizes, statistical evidence rules, allocations and enforcement within those ceilings, repositories, and provider permissions remain open.

## Answer to the DeepSeek assessment

The quoted review makes a reasonable demand for evidence. The response should be a narrower adoption claim and an auditable qualification process, not an assertion that more documentation makes the system safe.

| Review concern | Proposed response | Evidence required before adoption |
|---|---|---|
| Adoption depends on oh-my-openagent | Publish a portable method, a versioned adapter contract, and separately qualified implementations. Keep existing configuration examples as one implementation. | A second harness completes the same workflow and passes the same mandatory control tests. |
| The setup script cannot be audited | Offer a manual, inspect-before-install path with a complete file and network change manifest. Pin the reviewed source and dependencies. | Independent review of the exact revision, observed clean-environment installation, idempotency check, and rollback rehearsal. |
| Sensitive code may reach uncontrolled fallbacks | Require explicit provider-endpoint and data-class eligibility before every request, including retries, reviewers, tools, and fallbacks. | Denied-routing tests show no data leaves the boundary, rather than merely recording a warning afterwards. |
| Cost and fallback behavior are unclear | Record attempts, recipients, spend, retry reasons, and recovery outcomes. Enforce budget and routing limits outside agent-authored prompts. | Usage reconciliation, injected outage tests, and verified termination when limits are reached. |
| Production stability is needed now | Retain the current delivery path. Start with disposable tasks and advance only to supervised PR drafts. | Evidence of improvement and bounded failure under the selected conditions, not a promise of general production readiness. |
| Evals have not been run | Pre-register the task set, comparison arms, acceptance rules, failure handling, and decision thresholds. | A reproducible evidence packet including failures, withdrawals, uncertainty, and human interventions. |

The public repository explicitly describes its routing rationale as heuristics and disclaims quantitative quality and cost guarantees. Preserve that distinction when writing adoption guidance. A configuration validator or model-review verdict does not establish engineering effectiveness. [Model-mesh repository](https://github.com/bughunt8/model-mesh)

## Expand the theory without binding it to a harness

### State falsifiable hypotheses

Treat each proposition below as a hypothesis, not an established advantage.

- **Disciplined execution.** Explicit acceptance criteria, evidence gathering, bounded repair, and independent verification improve accepted-task yield or reduce human correction effort relative to the same model without the added method.
- **Role-specific routing.** Choosing models by observed task capability improves outcomes relative to a strong single-model version of the same method, without compensating for any objective regression.
- **Independent review.** A separate reviewer catches material defects often enough to justify its cost, latency, and false alarms. Merely using another model does not prove independence or effectiveness.
- **Controlled fallback.** Fallbacks recover useful work within the original data, permission, and budget constraints. When no eligible destination exists, stopping is a valid outcome.
- **Portability.** The method's workflow and control guarantees survive a harness change. Equal wording or syntactically valid configuration is insufficient evidence.
- **Bounded autonomy.** Granting more tool access or parallelism produces enough additional value to justify the added failure modes.

Replace universal model-family assertions with task-specific capability hypotheses. A restriction required by a particular harness prompt belongs in its adapter, not in the general theory. Provider accessibility, model ownership, hosting location, contractual data residency, retention, and training policy are separate properties.

### Separate the design into explicit parts

| Part | Proposed responsibility | What must not be assumed |
|---|---|---|
| Method | Define done, plan, execute within scope, verify, independently review, stop or escalate. | A particular agent name or vendor. |
| Policy | Data recipients, allowable tools, approved paths, spending, retries, approvals, retention. | A prompt can enforce its own restrictions. |
| Capability registry | Versioned model and harness capabilities, evidence date, known limits, provider endpoints. | A vendor family label proves suitability. |
| Workflow contract | Task identity, state transitions, role separation, cancellation, artifacts, evidence, terminal outcome. | All harnesses expose equivalent hooks. |
| Adapter | Translate the contract into one harness's invocation, events, configuration, and cancellation behavior. | Unsupported controls can be silently omitted. |
| Execution boundary | Restrict filesystem, processes, network, credentials, and writes outside the assignment. | A separate working directory is a security sandbox. |
| Evaluation | Measure outcomes against independent acceptance criteria and compare alternatives fairly. | Passing the repository's own tests proves the user's objective. |

Use semantic roles such as planner, implementer, verifier, reviewer, and approver. Roles need not always mean separate model calls. Small tasks may use fewer actors, but an implementer must not approve its own work.

A proposed adapter contract should declare task and attempt IDs, base revision, policy version, model endpoint, permitted context, available tools, resource limits, events, artifact hashes, cancellation acknowledgement, and terminal status. Missing mandatory capabilities should make an adapter ineligible for that risk class. Do not simulate support with optimistic documentation.

Proposed support labels are documented, mapped, conformance-tested, pilot-qualified, and production-approved for a named scope. Avoid a single unrestricted "supported" badge.

## Implementation choices

These components occupy different layers. They can be combined, so a flat contest between Orca, Qwen, Pi, and worktrees would be poorly defined.

| Candidate | Verified role | Proposed pilot role and uncertainty |
|---|---|---|
| OpenCode with oh-my-openagent | Model-mesh publishes role-routing configurations for this implementation. [Model-mesh](https://github.com/bughunt8/model-mesh) | Existing reference path, not a dependency of the method. Verify the exact version and effective runtime behavior. |
| Orca | Its documentation describes coordinating CLI agents, separate worktrees, and GitHub task/PR integration, including Pi and Qwen Code among supported CLIs. [Orca](https://github.com/stablyai/orca) | Optional coordination console. Qualify dispatch, cancellation, approvals, and evidence binding before treating it as a policy enforcement point. Product documentation is not proof of these controls. |
| Qwen Code | Its documentation describes a coding agent with headless operation, SDKs, and multiple provider protocols. [Qwen Code](https://github.com/QwenLM/qwen-code) | Candidate independent harness. Here "Qwen" means Qwen Code, pending your confirmation, rather than selecting a Qwen model by default. Audit the actual pinned release. |
| Pi | Its repository separates a multi-provider model API, an agent runtime, and a coding CLI. [Pi](https://github.com/badlogic/pi-mono) | Candidate for an explicit adapter with a small, inspectable integration. Do not assume built-in security enforcement; its documentation describes running with the launching process's permissions and external sandbox options. [Pi](https://github.com/badlogic/pi-mono) |
| Git worktrees with GitHub review | Git worktrees provide multiple checkouts with separate HEAD/index state while sharing repository data and normally configuration. They are not documented as process, credential, or network isolation. [Git worktree documentation](https://git-scm.com/docs/git-worktree) | Minimal coordination pattern: one assignment, one isolated execution environment and checkout, one branch, one independently verified change. GitHub would provide proposed issue, PR, and CI evidence handoffs, not the agent runtime. |

My provisional preference is to qualify one direct alternative harness first, with Pi and Qwen Code as candidates, using separate checkouts and controlled GitHub handoffs. Add Orca later if coordinating multiple concurrent workers solves a demonstrated problem. Do not build four adapters to prove a portability claim that two implementations can test.

This recommendation is about experimental clarity, not a claim that either harness is already safer or faster. The final choice depends on your installed environment, required controls, and tolerance for integration work.

## Auditing and enforceable guardrails

### Before execution

Propose a reviewed release manifest containing source revision, dependency lockfiles, artifact digests, configuration, prompt versions, enabled extensions, tool servers, and known vulnerabilities. Pin by immutable revision or digest where possible. A checksum establishes artifact identity; it does not establish that the artifact is safe.

Review installation separately from normal execution. Enumerate files written, shell startup changes, permissions requested, downloads, package lifecycle scripts, credentials read, hooks installed, and rollback behavior. Default to an empty temporary home and a disposable repository. No privileged installer, shared development credentials, or remote shell pipeline in the pilot.

Assign an owner for every control and record its status as proposed, inspected, exercised, or failed. Require independent sign-off on the exact version entering the pilot. Review changes to dependencies, prompts, adapters, policy, and model endpoints as material changes rather than assuming prior approval carries forward.

The same security boundary covers the installer, coordinator, evaluator, simulated users, tool servers, and worker. Upstream instructions are not authorization to run privileged code on the user's machine or a shared host. No host-root execution, host networking, exposed or world-writable container-control socket, or broad host mount may be accepted merely because a benchmark recommends it. If a suite needs privileged activity inside an independently approved disposable boundary, document and qualify that boundary first. If it cannot meet the common policy, defer the suite rather than waive a control.

### During execution

| Control | Proposed enforcement | Proposed negative test |
|---|---|---|
| Recipient eligibility | Trusted policy evaluates data class and exact provider endpoint before every primary, reviewer, fallback, or tool request. Unknown identity or missing policy stops the request. | Spoof vendor labels, remove policy, invoke an unapproved fallback, and request a new endpoint. Confirm no transmission. |
| Egress restrictions | Default-deny network controls around the worker, with a narrowly scoped gateway where required. Restrict all outbound routes, not only the model SDK. | Attempt shell, HTTP, DNS, tool-server, and telemetry exfiltration using synthetic canaries. |
| Secret handling | Short-lived scoped credentials outside the agent's writable workspace; redacted telemetry; no production secrets. | Ask the agent to read environment, credential files, host metadata, and another worker's secrets. |
| Write boundaries | Disposable sandbox with an approved checkout; no host socket, privileged container, broad mounts, or shared writable home. | Attempt path traversal, symlink escape, and writes to another assignment. |
| Tool permissions | Trusted command/tool broker and operating-system restrictions; prompt policy is supplementary. | Use shell indirection and an unapproved tool to bypass a denied action. |
| Change promotion | Worker can propose a patch, not merge, deploy, approve itself, alter required checks, or grant permissions. | Try direct protected-branch writes, workflow edits, and reuse of approval after a new commit. |
| Budget and retry bounds | Enforce call, token, elapsed-time, concurrency, repair-cycle, and monetary limits where usage is observable. Account for in-flight calls and reserve headroom. | Induce repeated errors and expensive fallbacks; measure stop behavior and any overshoot. |
| Cancellation | Supervisor revokes dispatch and write authority, terminates the process tree, and blocks stale attempts from publishing. | Cancel during a tool call, disconnect the coordinator, and replay an old completion. |
| Untrusted instructions | Treat repository prose, issue comments, retrieved pages, and tool output as data, not authority to change policy. | Plant prompt-injection instructions and verify they cannot change recipients or permissions. |
| Evidence integrity | Bind checks, review, and approval to an exact artifact digest or commit; store evidence outside worker write access. | Substitute another revision's green test output, truncate logs, or mutate code after review. |

Data residency needs an approved policy before a real-code pilot. Define where prompts, source, outputs, embeddings, traces, backups, and support-access records may be processed and stored. A model being available in Hong Kong, having open weights, or belonging to an approved vendor does not by itself satisfy that policy.

### Audit record and operating ownership

Record task/attempt identity, repository and revision, configuration hashes, effective permissions, model endpoint, actual recipient, policy decisions, tool invocations, retry and fallback reasons, usage, human intervention, cancellation, checks, review findings, and terminal outcome. Capture observable actions and decision summaries, not private model chain-of-thought.

Protect the audit store with separate write authority, access controls, retention limits, and integrity checks. Hash chaining alone cannot prevent a privileged actor from rewriting the entire store. Keep redacted operational events separate from any approved encrypted payload archive; logs themselves can contain sensitive code.

Audit at release approval, per-run conformance checking, periodic usage reconciliation, and incident review. Assign the policy owner, installer reviewer, acceptance evaluator, incident owner, and final promotion authority before execution. Missing mandatory evidence should invalidate the run's qualification claim rather than create a false green.

## Pilot sequence

### Agree the experiment

Use the selected benchmark suites to propose a non-sensitive evaluation population and freeze an acceptance rubric before running anything. Use the settled client-evidence purpose, priority order, comparison stages, repair rules, feedback categories, acceptance rule, and cap structure. Agree exact model/harness configurations, visible test and review procedures, safety boundaries, numeric caps, costs, and adoption evidence requirements through the remaining measurement questions. Do not reopen settled decisions or require useful-work discovery.

The agreed feasibility floor is two distinct cases per selected scenario, fourteen distinct cases across the seven scenarios. The scenario-to-stage assignment is settled below. Final case selection, counts beyond the minimum, repeats, and resource allocations remain open. Use task variability, the smallest worthwhile effect, available review capacity, the 10-hour/USD 100 ceilings, and the statistical evidence standard to assess feasibility. Do not assume that all selected suites, both stages, supplemental cases, repeats, and two-judge grading fit those limits. Return for an owner scope decision if the floor is infeasible; do not silently reduce it or claim that this small feasibility floor establishes a powered comparison.

The owner selected minimum breadth, then depth. First satisfy the two-distinct-case floor for each scenario in the feasibility proposal, using qualified selected benchmarks and necessary supplemental cases. Then allocate remaining capacity to repeated paired trials. Freeze the case manifest, repeats, stage allocation, and selection procedure before results. Assign each floor case one primary scenario so the fourteen-case minimum is not reduced by counting one case toward several scenario floors. A case reused in another arm or stage, a repair, or a repeated run is not a new distinct case. If the floor cannot fit safely within the aggregate limits, return to the owner for a scope decision before execution. No selection is silently dropped and no safety boundary is waived.

Count distinct underlying tasks, not distinct labels or prompts. Cases must differ in the actual defect, substantive dataset problem, requirements brief, target-system task, or office workflow being solved. Prompt paraphrases, cosmetic changes, revision changes, or different seeds alone do not qualify. A different repository or application is not additionally required when the underlying task differs. Record the underlying-task identity and reason for distinctness in the pre-run manifest so independent review can reject near-duplicates before they inflate the floor.

The selected case mix is two routine tasks per scenario. Define routine eligibility and any relevant complexity criteria before case selection and results; do not label a task routine merely because an arm solved it or replace a difficult outcome after seeing results. This scope supports routine-work observations only, not challenging-case reliability or representativeness of all client work. Mandatory security qualification and adversarial control tests remain separate requirements, and every confirmed defect still fails local acceptance.

Apply the fourteen-case floor across the whole pilot, not independently to both stages. Keep each scenario's two routine floor cases together in its assigned stage rather than splitting them or reusing the floor across both stages. The owner approved the following allocation. Within the assigned stage, run matched competing arms on each case; keeping two cases together does not mean assigning one case to each arm.

| Stage | Assigned scenarios | Distinct routine floor cases | Competing arms on every case |
|---|---|---|---|
| Method first | A01 regression bug repair; A03 behavior-preserving refactor; A05 security audit and remediation; A09 requirements and architecture planning | 8, two per scenario | `arm-baseline` versus `arm-method` |
| Routing second | A08 data reconciliation and analysis; A11 browser administration; A12 cross-application office work | 6, two per scenario | `arm-method` versus `arm-routing` |

The floor therefore entails fourteen matched case comparisons and twenty-eight initial arm attempts before repeats, with any permitted repair contained within its attempt. This is design arithmetic, not a claim that setup, execution, evaluation, or required controls fit the limits. These counts do not authorize dispatch, and actual cases, repeats, and resource reservations remain unapproved.

A scenario tested in the method stage does not establish a routing result, and the reverse also holds. Both stages remain required. Report the scenario-by-stage coverage matrix and limit each claim to its tested routine scope rather than pooling unlike stage populations to imply a broader effect. Any proposal for cases or cross-stage runs beyond the agreed floor requires an explicit allocation and feasibility review; no additional work is authorized by this design.

### Qualify controls before measuring productivity

Perform install and rollback review, adapter conformance checks, synthetic recipient tests, cancellation, boundary violations, and evidence-tampering tests. Use synthetic canaries rather than real secrets. Stop on any mandatory-control failure and do not start real-code trials.

### Isolate the method and routing effects

Within each stage, use the same task instances, base revisions, infrastructure class, tool access, safety policy, and agreed resource envelope for its competing arms. The two stages may use different predeclared subsets.

| Arm | Condition to configure and qualify | Question |
|---|---|---|
| `arm-baseline` | A declared single-model reference, with the common safety, feedback, and repair envelope. | What is the controlled reference for the method? |
| `arm-method` | Same harness and model, plus the explicit model-mesh loop. | Does the method help? |
| `arm-routing` | Same harness and loop, with predeclared role-specific model routing. | Does multi-model routing add value beyond the method? |

Stage one compares `arm-baseline` with `arm-method`; stage two compares `arm-method` with `arm-routing`. The stages are selected, not optional alternative designs. Hold each pair's declared conditions constant except for the intervention being tested. Exact models, prompts, tools, feedback, and reasoning settings remain to be pinned.

Do not use a deliberately weak reference. If a human-led or already multi-model operational baseline is later added, report that separately as a whole-system comparison. It must not replace or be mislabeled as either selected controlled stage.

Predeclare task-level resource limits by scenario or difficulty class within the pilot-wide ceilings. Assign task classes and cap rules before observing scored outcomes; apply the same caps to competing arms on the same task. Class definitions and numeric task-level time, token, cost, tool-call, concurrency, and retry limits remain open. Do not upgrade a difficult failed task's allowance after seeing its result.

Report outcomes within that matched envelope and each arm's actual operational cost. Count ordinary human acceptance review, but do not permit that review to coach repairs during the scored attempt.

### Pilot-wide time and cash limits

Set the clock at the first scored-task dispatch and allow at most 10 continuous elapsed hours for the scored phase through final evaluation. Execution, queues, retries, grading, and waits for owner adjudication all consume this same clock; there are no pauses or per-stage resets. This is neither a sum of CPU hours nor a cap on active human minutes.

Preparatory setup takes place before that clock, but no scored-task solving, rehearsal, or grading may be hidden as setup. Any preparation or calibration must preserve the separation from scored holdouts and remain subject to independent qualification. Setup before the scored clock is not authority to install or spend before the separate execution approval.

USD 100 covers all new pilot-related model, tool, and compute charges across the complete pilot, including setup, scored execution, repairs, both final judges, simulators, storage, and cleanup. New charges outside the scored clock still count. This is not an allowance per benchmark, model, worker, stage, or judge.

Record new paid provisioning, usage, upgrades, overages, and applicable billing charges in the cash ledger. Pre-existing sunk expenditure and owner labor are separately disclosed in economic cost accounting, not misrepresented as new cash payments. Pin billing rates, allocation, reconciliation, and storage/retention/cleanup reservations before execution; uncertain charges are not presumed free.

Before dispatch, account for spent, committed, and reserved charges, including in-flight work and final judging, rather than checking only the last invoice. Reserve capacity for safe termination and evidence retention. Specify enforceable usage bounds and cost assumptions first; if an activity's charge cannot be bounded within the remaining allowance, do not launch it.

Reaching a global ceiling must not reset the budget, create an extra repair attempt, or promote unfinished/disputed work to a pass. At the scored deadline, no additional scored task work or grading may be performed to finish a late result. Predeclare how in-flight work stops, how pending results are classified, and how reserved evidence retention and cleanup finish safely without extending the scored phase. Any new cleanup charges still count toward USD 100.

Later rescue requires separate authorization and an explicit remaining or additional resource envelope. If kept within this pilot, its new charges still count toward USD 100, and it cannot extend the scored phase. A separately approved follow-on effort must be labeled and reported separately, not used to retroactively expand this pilot's allowance or repair its score.

### Bounded repair and final evaluation

Allow at most one repair cycle after the initial submission. A cycle consists of permitted verification feedback, revision, and resubmission. A task that does not need repair may proceed directly to final submission; the cap is not a requirement to alter a successful artifact.

No human diagnoses, hints, clarification, or edits may rescue a scored attempt. Freeze the task brief before the attempt. Agents may use both predeclared executable checks and a separate agent's review against the frozen brief and visible evidence, within the common envelope. Use executable checks where they apply and record any predeclared lack of an executable check; do not fabricate automated coverage for a human-judged criterion. A human may stop unsafe execution, but that intervention does not produce a successful task or permission to continue beyond the boundary.

Freeze the final artifact and trace before independent final evaluation. The final evaluator's hidden answers, holdout tests, and findings must not be fed back into either repair feedback channel. A final failure cannot reopen an unused repair opportunity. Exact visible tests, agent-review prompts, reviewer configurations, and feedback delivery remain to be pinned, without reopening the selected feedback categories.

Measure defect quality on the final frozen artifact after the allowed repair, or on the initial artifact if submitted without repair. Do not add a separately scored first-handoff defect target. Retain attempt and repair traces for audit and account for all tool calls, retries, time, attention, and cost; the cycle limit does not allow unlimited work within a cycle.

At the last permitted submission, freeze the artifact and evaluate it; using the one allowed repair is not itself a failure. If the final artifact fails acceptance, or the attempt is terminated for breaching a resource limit, record a failure. Grade any available artifact without inventing defect findings for missing output. Report failures, incompletion, safety stops, and severity-specific defects separately; no-output tasks remain in the assigned-task denominator.

Continue the predeclared comparisons after an ordinary acceptance failure in either arm, including a confirmed cosmetic defect, provided mandatory controls and resource limits still permit work. Freeze and retain that failure and complete the planned matched counterpart when safe and within its limits; do not replace the failed task, add repair or rerun opportunities, modify configurations, or feed hidden final-evaluator findings into later scored work. The same continuation rule applies to all arms and both stages. Later cases cannot retroactively repair an earlier result.

Mandatory safety stops and global time/cash ceilings override continuation. An ordinary task failure does not prove a control failed, but an actual or unresolved mandatory-control problem cannot be relabeled ordinary to keep running. Classify events against frozen criteria and retain the evidence. Continuation is not adoption approval and does not relax the no-compensated-regression or uncertainty rules. Once the predeclared sample is exhausted, this rule does not authorize more trials.

Later rescue requires separate authorization and a separate run identity. It is unscored, may not replace or relabel the original failure, and must not contaminate other scored attempts. Disclose its time, human effort, and cost separately alongside all-in observed totals.

### Final task acceptance

Any confirmed defect against the frozen task and policy criteria makes the final task fail, including cosmetic defects. Passing an official benchmark grader is necessary where applicable but cannot override this stricter local acceptance rule or mandatory safety failures. Report the official grade separately.

Freeze an exact reference or template for each cosmetically graded output before the run, covering the applicable formatting, layout, naming, and presentation. Declare any variable content slots, exceptions, comparison representation, and normalization rules in advance. Do not substitute broad stylistic constraints, fuzzy visual similarity, or new preferences after seeing an output. Exact conformance is to that versioned reference/template and its declared exceptions, not an assertion that every file type should be compared byte-for-byte.

Make the required presentation template available equally to competing arms without revealing hidden correct answers, completed benchmark solutions, or final-evaluator findings. Separate task-visible formatting requirements from final-only correctness evidence. If those cannot be separated, the task design is not ready for execution.

Two independent AI judges apply the frozen rubric to the final artifact and evidence. The project owner resolves judge disagreements, conflicting checks, or uncertain defect findings after the artifact is frozen, without editing the output, providing repair feedback, or restarting the attempt. Either judge's disagreement or uncertainty triggers that dispute path; agreement still must satisfy the frozen checks and evidence. Record the finding, evidence, both judge decisions, owner disposition, artifact identity, and evaluation effort.

Allow eight continuous elapsed minutes from recorded dispute escalation for the owner's ruling, capped by the global scored deadline if sooner. Owner waiting does not pause the pilot clock. If no ruling is recorded by that cutoff, freeze the task as unresolved and not accepted. Preserve both judge findings and the evidence; a late ruling cannot retroactively change the scored outcome or reopen the attempt. Other eligible work may continue within the same resource limits.

Do not treat an unresolved finding as a pass or turn a suspected defect into a confirmed defect merely by assertion. The panel size, human dispute owner, eight-minute window, and unanswered-dispute disposition are settled. Exact judge models, calibration, evidence access, and escalation/notification mechanics remain to be agreed. Record when escalation occurs; a notification delay must not silently reset the timer. Do not silently accept a one-judge result if the other judge is unavailable. The selected workflow does not require the owner to rejudge every undisputed task.

Severity labels explain defects and inform analysis; they do not exempt minor or cosmetic defects from failure. A zero-confirmed-defect result is scoped to the declared rubric, checks, and observation window. It does not prove universal correctness or eliminate the possibility of an escaped defect.

### Test portability, then coordination

Replicate the selected condition on one alternative harness while holding models, tasks, policy, and evaluation as constant as feasible. Document differences in hidden prompts, reasoning controls, tools, context limits, and usage reporting. If identical model access is impossible, call this a system comparison, not a clean harness-effect estimate.

Only afterwards evaluate Orca or concurrent workers against the corresponding sequential workflow. Measure coordination overhead, lost work, conflict resolution, cancellation, and integration failures. Do not count worktree separation as security qualification.

### Supervised field trial and decision

If laboratory gates pass, consider a bounded field trial producing PR drafts only. A human remains the merge authority; no production deployment or automatic policy/model updates. Define the post-acceptance observation window before claiming escaped-defect performance.

Finish with one of four outcomes: reject, revise and retest, continue a limited pilot, or approve a narrowly specified use. An inconclusive result is a valid outcome. The approval applies only to the tested workflow, policy, versions, and task classes.

## Candidate measurement dictionary

The headline attention scope is settled as all active owner effort on the pilot, recorded with a timer plus activity log. Specific tooling, reconciliation and allocation procedures, and other operational definitions remain proposals unless fixed by an explicit decision. Apply the confirmed priority order: defects first, then your attention, then accepted-delivery time, then total cost. Retain non-negotiable safety gates separately. Avoid hiding unacceptable behavior inside a weighted overall score.

| Metric | Proposed operational definition | Trap to avoid |
|---|---|---|
| Accepted-task rate | Assigned tasks meeting all frozen criteria within budget, with no confirmed defect including cosmetic defects and no mandatory safety failure, divided by all eligible assigned tasks. | Dropping failed, timed-out, or abandoned tasks, or ignoring a cosmetic defect because the official grader passed. |
| Final-defect outcomes | Independently adjudicated defects and severity on the final frozen artifact after the permitted repair, alongside all-assigned completion and failure outcomes. Exact severity rules remain open. | Adding an unselected first-handoff quality target or hiding no-output failures behind a low defect count. |
| All pilot owner attention | All active owner minutes on preparation, setup, briefing, supervision, safety intervention, evaluation, disputes, record keeping, and cleanup. Report the pilot total, categories, and predeclared task/arm/stage attribution without double counting. Scored repairs receive no human coaching. | Excluding experiment-only adjudication or pre-clock setup, counting passive waiting as active effort, or attributing shared work opportunistically after results. |
| Fully loaded cost per accepted task | Total inference, retry, reviewer, tool, infrastructure, and priced human effort across all assigned work, divided by accepted tasks. Report setup cost separately and amortize transparently if requested. | Excluding failed attempts or claiming zero subscription cost. With no successes, report undefined, not zero. |
| Time to accepted change | Elapsed time from task release to independent acceptance; separately show queue, execution, review, and rework. | Reporting only successful latency while failures disappear. Show capped-run failures separately. |
| False acceptance | Independently adjudicated unacceptable outputs initially marked acceptable, divided by outputs initially marked acceptable. | Using the implementer's tests or verdict as the only truth. |
| Escaped defects | Accepted tasks later found to contain defects, including cosmetic defects, within a predefined review/test window; retain severity breakdowns and the original result history. | Restricting follow-up to material defects when acceptance rejects every confirmed defect, or claiming production defect reduction from a short offline pilot. |
| Reviewer effectiveness | Recall on seeded or adjudicated defects, precision of raised findings, and added human workload, with severity and cosmetic breakdowns. Report synthetic and natural defects separately. | Excluding cosmetic defects despite the acceptance rule, or counting long critiques or different model names as evidence of independence. |
| Fallback invocation and recovery | Tasks with fallback divided by started tasks; then accepted tasks with fallback divided by tasks with fallback. Also report event counts and reason categories. | Interpreting recovery as causal benefit without a paired or randomized fallback experiment. |
| Policy enforcement | Approved-request outcomes, denied-request outcomes, attempted violations, actual violations, and missing evidence, each with a defined test denominator. | Treating blocked unsafe attempts as successful exfiltration or treating zero observed violations as proof of no risk. |
| Stability and intervention | Terminal outcomes, crashes, hangs, retries, and safety interventions across all started attempts; later rescue is a separate disclosed activity. | Deleting infrastructure failures after seeing which arm lost or overwriting a failed attempt with its rescued successor. |
| Reproducibility | Repeated task success and result variance under the frozen setup, plus exact reconstruction of the declared environment. | Promising identical model output merely because source code is pinned. |
| Portability effort | Person-hours to map, implement, audit, and qualify the adapter; unsupported requirements and runtime differences. | Ignoring the engineering cost of moving to a new harness. |
| Parallel coordination | Lost changes, conflicting writes, duplicated work, stale approvals, integration repair, and accepted throughput per available human hour. | Rewarding agent activity or raw concurrent task count. |

Task success requires the frozen checks and independent AI-judge assessment, with human resolution of disputes or uncertainty. Apply the exact reference/template to cosmetic criteria and keep final evaluation outside worker write access. Do not assume AI-judge agreement is proof of correctness; calibration and validation checks must be specified before execution. Code volume, token count, number of agents, or a leaderboard score should not be primary success measures.

All active owner pilot effort belongs in the headline attention ledger even outside the scored runtime clock. Keep operational, setup, independent-evaluation, and separately authorized rescue categories distinct without dropping their pilot effort from the total. Passive waiting belongs in elapsed-time reporting; active monitoring during a wait counts as attention. Shared preparation and evaluation effort needs a fixed allocation rule before comparative analysis, with one raw total and no duplicated minutes across concurrent tasks. Separately authorized rescue cannot rewrite scored outcomes, and a separate follow-on effort must be disclosed separately rather than hidden or retroactively folded into scored success. These accounting rules grant no permission for human rescue or extra work.

The owner starts and stops a timer and tags each activity in the log, including pilot work outside the scored clock. Reconcile timer intervals with the activity log; preserve the original record and a reason for each correction. If a start or stop is missed, mark the affected interval missing. Do not reconstruct a duration from memory, the log, or event timestamps, and do not enter zero. Corrections may repair labels or transcription against existing valid timer evidence, but may not manufacture a missing timing observation. Prevent overlapping timers from duplicating the same active minute. Reconciliation effort itself counts as pilot attention. Exact tool, log fields, reconciliation cadence, and shared-effort allocation remain to be agreed; this specifies a measurement method without implementing it.

Retain the task and its other outcomes when attention timing is missing. Report observed active minutes as an incomplete observed sum, with missing interval identities and affected tasks, categories, arms, and stages; do not present it as the complete all-pilot total. The affected attention comparison is inconclusive unless a missing-data threshold and analysis procedure are approved before runs. No exception or tolerance has been selected. Any future procedure must preserve missingness, prohibit duration imputation and outcome-driven exclusions, and remain consistent with the no-compensated-regression rule. If uncertainty prevents that rule from being assessed, the conclusion remains inconclusive.

### Comparison and uncertainty

Pair comparisons by task and use clean environments for every arm. Randomize or counterbalance run order to reduce time-of-day and provider effects. Keep solutions, hidden tests, and previous run traces out of subsequent task contexts.

Use repeats to estimate variability if affordable, while retaining task identity in analysis. Repeated runs of the same task are not independent new tasks. Report paired task-level differences, uncertainty intervals, and breakdowns by task class; avoid treating a tiny sample's upper-percentile latency as stable.

Pre-register exclusions before results are seen. Report an all-assigned operational view and, if useful, a separately explained model-only analysis. Include outages and missing usage records in the operational evidence.

No numeric performance target is agreed yet. Adoption requires all mandatory controls to pass, complete mandatory evidence, and no accepted regression in any of the four objectives. Another objective's improvement cannot compensate for a regression. Assess any demonstrated improvements in the settled order: defects, your attention, accepted-delivery time, then total cost.

Uncertainty about a required condition means inconclusive, not an assumed pass. Before execution, agree the smallest improvement worth claiming, the statistical evidence standard, measurement-error handling, and stopping conditions. These unresolved decisions do not authorize a positive regression margin or relaxed safety gate. A finite pilot can bound uncertainty; it cannot prove universal equality or absence of risk.

## Claims and proposed documentation changes

Do not replace "no evidence" with "production-ready after audit." Proposed future documentation should distinguish method hypotheses, adapter capabilities, enforced controls, measured outcomes, and remaining limitations. Any result must name its task population, versions, resource envelope, comparator, and sample size.

Suggested future documents are a method specification, threat model, adapter contract, release audit checklist, qualification tests, measurement dictionary, pre-registered pilot protocol, and results card. These are proposed outputs, not files to implement in the code repository now.

The public adoption statement should eventually read along these lines: "Model-mesh is a portable engineering method with separately qualified harness adapters. Adoption requires recipient and tool policies, verified controls, and task-specific evaluation. Results apply to the tested setup." Until then, retain explicit experimental status.

## Measurement interview

We will resolve this in rounds rather than ask dozens of abstract questions at once. After each round, record the decision in plain language, turn it into a measurable definition, and challenge it with a counterexample.

### Settled inputs and current selections

- Purpose: a client offering supported by defensible evidence and successful projects.
- Usefulness: established; useful-work discovery is out of scope for now.
- Priorities: fewer defects, less of your attention, faster accepted delivery, lower total cost. No compensating trade-offs.
- Benchmark shortlist: B01 SWE-bench Verified, B06 GAIA, B10 TheAgentCompany, subject to qualification.
- Scenario selection: A01, A03, A05, A08, A09, A11, and A12. Do not require actual project examples at this stage.
- Comparison design: method effect first, then routing effect, in separate controlled stages.
- Defect measurement: after at most one repair cycle, with no human rescue.
- At the limit: count and freeze failure; separately authorized later rescue is unscored.
- After ordinary acceptance failure: continue the predeclared comparisons across either arm, with no extra repair, replacement task, configuration change, or hidden-evaluator feedback. Safety and resource stops still override continuation.
- Repair feedback: both executable checks and agent review, excluding hidden final-evaluator information.
- Final task acceptance: any confirmed defect, including cosmetic defects, fails.
- Resource envelope: predeclared by scenario or difficulty class, matched for competing arms on the same task.
- Final adjudication: two independent AI judges; the project owner personally resolves disputes or uncertain findings on frozen outputs.
- Dispute timing: eight elapsed minutes from escalation, or the global deadline if sooner; no ruling means frozen unresolved and not accepted.
- Sampling: at least two distinct cases per selected scenario, fourteen across the whole pilot rather than per stage, then repeated paired trials; approve the case manifest and stage subsets, and return for a scope decision if infeasible.
- Case mix and assignment: two routine cases per scenario, kept together. Method stage: A01, A03, A05, A09, with eight floor cases. Routing stage: A08, A11, A12, with six floor cases.
- Case identity: a different underlying task is required; paraphrases, cosmetic variants, revision changes, and seeds alone do not count. A different repository or application context is not also required.
- Attention: all active owner pilot effort, including setup and independent evaluation, with category breakdowns and no double counting; passive waiting is elapsed time.
- Attention recording: owner-operated timer plus tagged activity log, with reconciliation and preserved corrections. Missed start/stop intervals remain missing, never estimated or zero; no missing-data analysis exception is currently agreed.
- Cosmetic grading: exact reference or template, with exceptions declared before execution.
- Aggregate limits: 10 hours total elapsed pilot runtime and USD 100 combined model/tool/compute charges. These do not reset per task or stage.
- Clock boundary: first scored-task dispatch through final evaluation, continuously including queues, grading, and owner waits; setup precedes the clock.
- Cash boundary: all new pilot charges, including setup and cleanup; owner labor and sunk expenditure are separately reported.

### Next measurement round

- For each selected scenario, which versioned reference/template and correctness criteria define defects? Every confirmed defect already causes failure.
- Which judge configurations, calibration checks, and recorded escalation and notification mechanics implement adjudication within the settled eight-minute window? How are missing-judge cases and timely but inconclusive owner responses recorded without treating them as passes?
- Which exact model, harness, prompts, tools, reasoning settings, visible checks, and agent-review procedures define each selected stage?
- Which predeclared eligibility criteria and actual cases define routine work in each scenario under the settled stage assignment?
- Which timer/log tool, fields, reconciliation cadence, and shared-effort allocation will implement the settled recording method without double counting? The inclusion of setup and independent evaluation is settled.
- What evidence is sufficient to distinguish improvement, regression, and an inconclusive result without allowing a prohibited trade-off?

### Later rounds

- Define acceptance, unresolved-work classification, defect severity, and acceptance ownership without reopening the settled repair and rescue rules.
- Decide the data classes, jurisdictions, approved recipients, fallbacks, tools, and actions that must never be permitted.
- Price human effort, subscriptions, infrastructure, setup, and failed attempts; separate economic cost from cash expenditure.
- Agree task mix, class-level allocation, cost reservations, cutoff/cleanup mechanics, meaningful effect, and uncertainty standard within the settled clock and cash boundaries.
- Select the alternative harness and define what counts as portable, including adapter effort and unsupported capabilities.
- Challenge the proposed decision with adverse examples: a cheap but wrong patch, a perfect patch sent to an unapproved provider, a safe refusal, a very slow success, a green CI run on the wrong commit, and an experiment too small to distinguish the alternatives.

The interview is complete only when we can both apply the same rules to these examples and reach the same acceptance and adoption decision. Until then, this remains a discussion draft.
