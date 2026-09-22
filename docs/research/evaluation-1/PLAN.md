# Model-mesh portable method and pilot plan

Discussion draft v0.4 | 22 September 2026 | Planning only

## Agreed priorities

Your confirmed priority order is fewer defects, less of your attention, faster accepted delivery, then lower total cost. Do not use a weighted score that allows lower-priority gains to compensate for higher-priority regressions. No compensating trade-offs are authorized.

Scenario and benchmark selections were made separately, including non-coding work. [The benchmark research and selection record](BENCHMARKS.md) supplies the original 12 scenarios and 10 benchmark options. [Analysis](ANALYSIS.md) records experiment-design implications, and [the decision log](DECISIONS.md) separates settled instructions from open questions.

The selected benchmark shortlist is B01 SWE-bench Verified, B06 GAIA, and B10 TheAgentCompany. All remain subject to access, evaluator, adapter, and security qualification. Selected scenarios are A01 regression bug repair, A03 behavior-preserving refactor, A05 security audit and remediation, A08 data reconciliation and analysis, A09 requirements and architecture planning, A11 browser administration, and A12 cross-application office work. Selection does not authorize execution.

The adoption purpose is now confirmed: offer model-mesh to clients, supported by measured success on your own projects. Prospective clients are the audience. Usefulness is established by your experience and is not the question this pilot needs to reopen.

For now, focus on evaluation scenarios and existing benchmarks that can substantiate defects, reliability, guardrails, and portability. Defer discovery or selection of personally useful work. Later client claims may combine measured project case studies and benchmark evidence, with their respective limits stated.

Two comparison stages are agreed: isolate the method first, then routing's added effect. Defect quality is measured after bounded repair, with at most one repair cycle after the initial submission, the same cap for both sides, and no human rescue. Any attempt still failing at its repair or resource limit is frozen and counted as a failure; separately authorized later rescue is unscored and cannot revise that result.

Exact comparator configurations, defect definitions, acceptance thresholds, resource caps, and the evidence standard remain unresolved. Continued planning does not authorize implementation.

## Decision sought

Determine what defensible claims can be made about an already-useful engineering method's quality, reliability, guardrails, and portability for a client offer. Do not reopen whether the work is useful. Neither qualification nor portability should depend on accepting an entire repository or trusting a model's self-review.

For each proposed client case study, require a named scope, initial state, comparator, task outcomes, independently checked defects, your active attention, accepted-delivery time, full cost, and limitations. Include unsuccessful eligible tasks in the evidence even if the public case study focuses on a successful project. Retrospective project success without a suitable comparator cannot establish that model-mesh caused the improvement.

This document proposes architecture, controls, experiments, and measurement definitions. No implementation, installation, pilot execution, repository modification, AWS deployment, or new scheduled task is authorized by this plan. Sample sizes, thresholds, duration, expenditure, repositories, and provider permissions remain open until agreed.

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

Use the selected benchmark suites to propose a non-sensitive evaluation population and freeze an acceptance rubric before running anything. Use the settled client-evidence purpose, priority order, comparison stages, and repair rules. Agree exact model/harness configurations, permitted feedback, safety boundaries, resource caps, costs, and thresholds through the remaining measurement questions. Do not reopen settled decisions or require useful-work discovery.

No task count or allocation is agreed. Choose the final count across the seven selected scenarios using task variability, the smallest worthwhile effect, available review capacity, resource limits, and the statistical evidence standard. Do not reuse an arbitrary coding-only task count for this broader selection or present a small feasibility sample as a powered comparison.

### Qualify controls before measuring productivity

Perform install and rollback review, adapter conformance checks, synthetic recipient tests, cancellation, boundary violations, and evidence-tampering tests. Use synthetic canaries rather than real secrets. Stop on any mandatory-control failure and do not start real-code trials.

### Isolate the method and routing effects

Use the same task instances, base revisions, infrastructure class, tool access, safety policy, and agreed resource envelope across comparisons.

| Arm | Condition to configure and qualify | Question |
|---|---|---|
| `arm-baseline` | A declared single-model reference, with the common safety, feedback, and repair envelope. | What is the controlled reference for the method? |
| `arm-method` | Same harness and model, plus the explicit model-mesh loop. | Does the method help? |
| `arm-routing` | Same harness and loop, with predeclared role-specific model routing. | Does multi-model routing add value beyond the method? |

Stage one compares `arm-baseline` with `arm-method`; stage two compares `arm-method` with `arm-routing`. The stages are selected, not optional alternative designs. Hold each pair's declared conditions constant except for the intervention being tested. Exact models, prompts, tools, feedback, and reasoning settings remain to be pinned.

Do not use a deliberately weak reference. If a human-led or already multi-model operational baseline is later added, report that separately as a whole-system comparison. It must not replace or be mislabeled as either selected controlled stage.

Predeclare resource limits. Report outcomes within a matched envelope and each arm's actual operational cost. Count ordinary human acceptance review, but do not permit that review to coach repairs during the scored attempt.

### Bounded repair and final evaluation

Allow at most one repair cycle after the initial submission. A cycle consists of permitted verification feedback, revision, and resubmission. A task that does not need repair may proceed directly to final submission; the cap is not a requirement to alter a successful artifact.

No human diagnoses, hints, clarification, or edits may rescue a scored attempt. Freeze the task brief before the attempt. Agents may use the predeclared tests and workflow feedback within the common envelope. A human may stop unsafe execution, but that intervention does not produce a successful task or permission to continue beyond the boundary.

Freeze the final artifact and trace before independent final evaluation. The final evaluator's hidden answers, holdout tests, and findings must not be fed back into repair. A final failure cannot reopen an unused repair opportunity. Which non-holdout test and agent-review feedback is permitted remains an explicit pre-execution decision, applied consistently within each comparison.

Measure defect quality on the final frozen artifact after the allowed repair, or on the initial artifact if submitted without repair. Do not add a separately scored first-handoff defect target. Retain attempt and repair traces for audit and account for all tool calls, retries, time, attention, and cost; the cycle limit does not allow unlimited work within a cycle.

At the last permitted submission, freeze the artifact and evaluate it; using the one allowed repair is not itself a failure. If the final artifact fails acceptance, or the attempt is terminated for breaching a resource limit, record a failure. Grade any available artifact without inventing defect findings for missing output. Report failures, incompletion, safety stops, and severity-specific defects separately; no-output tasks remain in the assigned-task denominator.

Later rescue requires separate authorization and a separate run identity. It is unscored, may not replace or relabel the original failure, and must not contaminate other scored attempts. Disclose its time, human effort, and cost separately alongside all-in observed totals.

### Test portability, then coordination

Replicate the selected condition on one alternative harness while holding models, tasks, policy, and evaluation as constant as feasible. Document differences in hidden prompts, reasoning controls, tools, context limits, and usage reporting. If identical model access is impossible, call this a system comparison, not a clean harness-effect estimate.

Only afterwards evaluate Orca or concurrent workers against the corresponding sequential workflow. Measure coordination overhead, lost work, conflict resolution, cancellation, and integration failures. Do not count worktree separation as security qualification.

### Supervised field trial and decision

If laboratory gates pass, consider a bounded field trial producing PR drafts only. A human remains the merge authority; no production deployment or automatic policy/model updates. Define the post-acceptance observation window before claiming escaped-defect performance.

Finish with one of four outcomes: reject, revise and retest, continue a limited pilot, or approve a narrowly specified use. An inconclusive result is a valid outcome. The approval applies only to the tested workflow, policy, versions, and task classes.

## Candidate measurement dictionary

All operational definitions below remain proposals. Apply the confirmed priority order: defects first, then your attention, then accepted-delivery time, then total cost. Retain non-negotiable safety gates separately. Avoid hiding unacceptable behavior inside a weighted overall score.

| Metric | Proposed operational definition | Trap to avoid |
|---|---|---|
| Accepted-task rate | Assigned tasks meeting all frozen functional, quality, and policy acceptance rules within the allowed budget, divided by all eligible assigned tasks. | Dropping failed, timed-out, or abandoned tasks. |
| Final-defect outcomes | Independently adjudicated defects and severity on the final frozen artifact after the permitted repair, alongside all-assigned completion and failure outcomes. Exact severity rules remain open. | Adding an unselected first-handoff quality target or hiding no-output failures behind a low defect count. |
| Human attention per task | Active briefing, supervision, ordinary final review, safety intervention, and other authorized operational attention, recorded for every task. Scored repairs receive no human coaching. | Ignoring review effort, silently treating human rescue as autonomous performance, or mixing post-score rescue into a successful scored attempt. |
| Fully loaded cost per accepted task | Total inference, retry, reviewer, tool, infrastructure, and priced human effort across all assigned work, divided by accepted tasks. Report setup cost separately and amortize transparently if requested. | Excluding failed attempts or claiming zero subscription cost. With no successes, report undefined, not zero. |
| Time to accepted change | Elapsed time from task release to independent acceptance; separately show queue, execution, review, and rework. | Reporting only successful latency while failures disappear. Show capped-run failures separately. |
| False acceptance | Independently adjudicated unacceptable outputs initially marked acceptable, divided by outputs initially marked acceptable. | Using the implementer's tests or verdict as the only truth. |
| Escaped material defects | Accepted tasks later found to contain agreed-severity defects within a predefined review/test window. | Claiming production defect reduction from a short offline pilot. |
| Reviewer effectiveness | Recall on seeded or adjudicated material defects, precision of raised findings, and added human workload. Report synthetic and natural defects separately. | Counting long critiques or different model names as evidence of independence. |
| Fallback invocation and recovery | Tasks with fallback divided by started tasks; then accepted tasks with fallback divided by tasks with fallback. Also report event counts and reason categories. | Interpreting recovery as causal benefit without a paired or randomized fallback experiment. |
| Policy enforcement | Approved-request outcomes, denied-request outcomes, attempted violations, actual violations, and missing evidence, each with a defined test denominator. | Treating blocked unsafe attempts as successful exfiltration or treating zero observed violations as proof of no risk. |
| Stability and intervention | Terminal outcomes, crashes, hangs, retries, and safety interventions across all started attempts; later rescue is a separate disclosed activity. | Deleting infrastructure failures after seeing which arm lost or overwriting a failed attempt with its rescued successor. |
| Reproducibility | Repeated task success and result variance under the frozen setup, plus exact reconstruction of the declared environment. | Promising identical model output merely because source code is pinned. |
| Portability effort | Person-hours to map, implement, audit, and qualify the adapter; unsupported requirements and runtime differences. | Ignoring the engineering cost of moving to a new harness. |
| Parallel coordination | Lost changes, conflicting writes, duplicated work, stale approvals, integration repair, and accepted throughput per available human hour. | Rewarding agent activity or raw concurrent task count. |

Task success should require hidden or independently owned checks where appropriate, plus human acceptance of requirements not captured by tests. Freeze the acceptance suite outside worker write access. Code volume, token count, number of agents, or a leaderboard score should not be primary success measures.

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

### Next measurement round

- For selected scenarios or benchmark tasks, which outcomes are defects and which severity levels are automatic failures?
- Who adjudicates defects, false positives, and disagreements between tests and reviewers?
- Which exact model, harness, prompts, tools, reasoning settings, and permitted feedback define the reference for each selected stage?
- Which activities count toward your attention, and how will active time be recorded?
- What evidence is sufficient to distinguish improvement, regression, and an inconclusive result without allowing a prohibited trade-off?

### Later rounds

- Define acceptance, unresolved-work classification, defect severity, and acceptance ownership without reopening the settled repair and rescue rules.
- Decide the data classes, jurisdictions, approved recipients, fallbacks, tools, and actions that must never be permitted.
- Price human effort, subscriptions, infrastructure, setup, and failed attempts; separate economic cost from cash expenditure.
- Agree the time horizon, task mix, resource envelope, meaningful effect, uncertainty tolerance, and stopping conditions.
- Select the alternative harness and define what counts as portable, including adapter effort and unsupported capabilities.
- Challenge the proposed decision with adverse examples: a cheap but wrong patch, a perfect patch sent to an unapproved provider, a safe refusal, a very slow success, a green CI run on the wrong commit, and an experiment too small to distinguish the alternatives.

The interview is complete only when we can both apply the same rules to these examples and reach the same acceptance and adoption decision. Until then, this remains a discussion draft.
