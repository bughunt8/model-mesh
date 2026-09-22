# Model-mesh pilot task and benchmark options

Selection record and research | 22 September 2026 | Research and planning only

See [the plan](PLAN.md), [analysis](ANALYSIS.md), and [decision log](DECISIONS.md). Options are preserved for traceability; the explicit owner selections govern the proposed scope.

## Rules already settled

Your priorities are fewer defects, less of your attention, faster accepted delivery, and lower total cost, in that order. There is no authority to trade a higher-priority regression for a lower-priority benefit. We will not use a blended score that conceals those regressions.

Keep safety and recipient-policy compliance as mandatory gates, not productivity metrics that can be averaged away. No pilot implementation, benchmark execution, installation, live business action, or deployment is included in this selection step.

The comparison stages are settled: method effect first, then routing effect. Score final defect quality after at most one repair cycle with no human rescue, using the same cap on both sides. A failed scored attempt stays failed even if later separately authorized, unscored rescue succeeds. These local pilot rules must be reported alongside the official benchmark grade rather than presented as an unchanged official evaluation protocol.

Both executable checks and agent review may inform repair, excluding hidden final-evaluator information. Any confirmed defect, including cosmetic defects against predeclared criteria, fails local task acceptance even if the official benchmark grade passes. Task-level caps are predeclared by scenario or difficulty class, not chosen after observing results; class allocations within the settled pilot ceilings remain open.

Two independent AI judges evaluate final frozen outputs, with the project owner personally resolving disagreements or uncertain findings. Cosmetic grading uses an exact reference or template, with any exceptions declared before execution. Formatting templates may be task-visible; hidden answers and completed benchmark solutions must remain final-evaluator-only.

The selected suites share a continuous 10-hour scored-phase clock starting with the first scored-task dispatch, including queues, grading, and owner waits. Setup is before the clock, but all new pilot model/tool/compute charges, including setup and cleanup, share the USD 100 ceiling. No per-suite reset is allowed, and these limits do not imply that full runs of every suite fit. Task subsets and resource allocations remain to be approved.

Sampling follows minimum breadth, then depth: propose a minimum floor across the seven selected scenarios, then repeated paired trials with remaining capacity. Qualify B01, B06, and B10 and retain explicit supplemental coverage gaps. Neither one benchmark task nor one repeated case automatically covers every mapped scenario. If the proposed floor is infeasible or a selected suite cannot meet security requirements, return for a scope decision; do not substitute a benchmark or waive controls silently.

The floor applies across the whole pilot rather than separately to each stage. Freeze and report a scenario-by-stage matrix; stage subsets may differ, but matched comparisons and claims remain local to the tested stage and scenarios. A suite's inclusion somewhere in the pilot does not establish both method and routing results for it.

All active owner pilot attention is included in the headline, including benchmark setup, evidence preparation, evaluation, disputes, record keeping, and cleanup as well as operational work. Report categories separately without excluding experiment-only effort or duplicating shared minutes. Passive waiting is elapsed time, not active attention.

The owner has eight elapsed minutes from recorded dispute escalation to rule, capped by the global deadline. An unanswered dispute freezes as unresolved and not accepted under the local protocol. Keep this local outcome separate from the official benchmark grade, without adding late scored grading.

This document separates two choices. Evaluation scenarios define capabilities and failure modes to test. Benchmarks provide reusable test material and evaluation procedures. A benchmark is not the baseline workflow: a comparative improvement claim will still require a declared comparator.

The confirmed business purpose is to offer model-mesh to clients using measured success on your own projects as evidence. Usefulness is already established and is not being reassessed. For now, defer personally useful task discovery and project selection; focus on qualification scenarios, external benchmarks, and defensible claims.

Proposed client evidence should show what was attempted, what succeeded or failed, what the comparator was, and which conditions limited the result. Do not credit model-mesh for an entire project's historical success without evidence of its actual contribution. Publication would need a separate review for confidentiality and claim accuracy.

## Selected benchmark shortlist

You selected B01 SWE-bench Verified, B06 GAIA, and B10 TheAgentCompany. The other seven options remain researched alternatives, not selected scope. The scenario selection below is separate from the benchmark choice.

All three selected suites require qualification before execution. TheAgentCompany remains conditional on a safe boundary for its installer, orchestrator, evaluator, tool servers, simulated colleagues, and worker. Upstream setup instructions do not waive the pilot's security policy.

## Selected scenarios and coverage gaps

The selected scenarios are A01, A03, A05, A08, A09, A11, and A12. A02, A04, A06, A07, and A10 are not selected. The earlier T-prefixed scenario labels are replaced with A-prefixed labels; the numbers and meanings are unchanged.

The following is a proposed coverage assessment, not a claim that we have inspected and qualified every task in each suite. Do not add an unselected benchmark to fill a gap without approval.

| Selected scenario | Proposed evidence route | Gap to resolve before execution |
|---|---|---|
| A01. Regression bug repair | B01 SWE-bench Verified as the main standardized test. | Add independent defect adjudication and attention measurement; hidden test success is not a complete defect audit. |
| A03. Behavior-preserving refactor | Supplemental bounded refactoring cases with independent differential tests. | Do not relabel repository bug-fix tasks as a refactoring benchmark. Case construction and grading remain to be specified. |
| A05. Security audit and remediation | Supplemental seeded vulnerabilities with controlled exploit and repair checks. | The selected suites are not substitutes for a dedicated security-audit evaluation. Agree severity and false-positive handling. |
| A08. Data reconciliation and analysis | Inspect B06 GAIA and B10 TheAgentCompany for suitable task subsets. | If coverage is inadequate, propose supplemental known-answer data cases rather than silently claiming benchmark coverage. |
| A09. Requirements and architecture planning | Supplemental frozen briefs, exact output templates, traceability checks, independent AI judges, and human dispute resolution. | No selected benchmark has yet been qualified as a complete architecture-planning evaluation. Define the rubric, judge calibration, and dispute procedure. |
| A11. Browser administration | Inspect B10 TheAgentCompany for browser-based workflow tasks. | Separate browser-admin completion from answer retrieval; qualify permissions and final-state checks. B08 WebArena is not selected. |
| A12. Cross-application office work | Inspect B10 TheAgentCompany for multi-application deliverables; use B06 only where appropriate. | Check artifact consistency and handoffs rather than assuming a correct final answer proves the entire workflow. |

## Twelve candidate evaluation scenarios

These are proposed evaluation cases, not descriptions of existing benchmarks or requests to justify usefulness. The menu is retained as the selection record. Only A01, A03, A05, A08, A09, A11, and A12 are selected, and selection does not authorize execution.

| ID and task | Example pilot assignment | Proposed acceptance evidence | A result that must fail despite looking successful |
|---|---|---|---|
| A01. Regression bug repair | Fix a reproducible defect in a small service using a frozen issue and base revision. | Independent reproduction fails before the patch and passes after it; regression and edge-case checks pass. | The agent suppresses the error, removes coverage, or breaks an adjacent behavior. |
| A02. Bounded feature delivery | Add a small API, command, or UI capability from a frozen acceptance specification. | Required positive and negative behaviors work; compatibility and relevant accessibility checks pass. | The happy path works but authorization, validation, or failure behavior is wrong. |
| A03. Behavior-preserving refactor | Simplify a module or remove duplication without changing its public contract. | Independent differential tests, compatibility checks, and an agreed maintainability review. | Tests pass only because they miss a changed edge case, or the refactor creates needless complexity. |
| A04. CI or deployment diagnosis | Diagnose and repair a broken build or deployment specification in a disposable environment. | Reproducible diagnosis, corrected build, retained security checks, and tested rollback instructions. | The build becomes green by disabling checks or broadening permissions. No production deployment. |
| A05. Security audit and remediation | Inspect a seeded vulnerable component, identify material findings, and propose or test repairs. | Independent exploit reproductions, severity adjudication, verified repairs, and false-positive accounting. | A long report misses the exploitable flaw, leaks a secret, or introduces another vulnerability. |
| A06. Independent change review | Review a patch containing planted defects and legitimate but unusual code. | Defect recall, finding precision, severity agreement, and minutes required to adjudicate findings. | The reviewer approves a dangerous patch or floods you with plausible but false objections. |
| A07. Source-grounded research brief | Answer a real technology or business decision question using an agreed evidence corpus or bounded web search. | Claim-level evidence checks, contrary evidence, freshness, and traceable conclusions. | Citations exist but do not support the claims, or the conclusion omits a decisive limitation. |
| A08. Data reconciliation and analysis | Reconcile two datasets, explain discrepancies, and produce a reproducible analysis. | Known-answer checks, reconciled totals, explicit exclusions, and repeatable calculations. | A persuasive chart hides missing rows, duplicate records, incorrect units, or unsupported causal claims. |
| A09. Requirements and architecture planning | Turn a brief into acceptance criteria, design choices, risk analysis, and a delivery plan. | Traceability to the brief, contradiction checks, constraint compliance, and independent rubric-based review. | Polished documents contradict one another or require capabilities that do not exist. |
| A10. Policy-constrained business workflow | Resolve a simulated account or service request using tools under a written approval policy. | Correct final state, authorized actions, complete required steps, and appropriate escalation. | The user appears satisfied but the agent violates policy or performs an unauthorized change. |
| A11. Browser administration | Complete a multi-step update across disposable project, content, or issue-management websites. | Verified final state, correct target records, no unintended changes, and an audit trail. | The right-looking page hides duplicate records, wrong recipients, or changes to the wrong account. |
| A12. Cross-application office work | Assemble a decision pack from files, a spreadsheet, and a simulated communication thread. | Consistent figures, complete required artifacts, correct references, and verified handoffs. | Each artifact looks fine but the figures disagree, an attachment is missing, or a draft is sent prematurely. |

### Interpretation of the selected scope

The seven selected scenarios include engineering, assurance, analysis, planning, browser work, and office work. Do not pool them into one percentage that hides a regression in a selected category. Independent review is still part of the quality process even though A06 is not a separately selected evaluation scenario.

## Ten researched benchmark options

The following descriptions use primary benchmark documentation, reviewed on 22 September 2026. Fit, cautions, and proposed pilot use are my recommendations. Listed capabilities do not constitute a security audit or prove an adapter is ready.

### Engineering and tool use

| ID and option | What it actually tests | Proposed use and task mapping | Constraint or interpretation limit |
|---|---|---|---|
| B01. SWE-bench Verified | Real repository issue resolution using a human-validated subset; patches must pass issue-specific and regression tests in containerized environments. [Official description](https://openai.com/index/introducing-swe-bench-verified/) | A familiar reference for A01 and selected A02 cases. Use the same task and environment across arms. | The source flags static-dataset and pretraining-contamination limitations. [Official description](https://openai.com/index/introducing-swe-bench-verified/) I would use it for comparability, not as the sole evidence of current real-world quality. |
| B02. SWE-Bench Pro, public set | Long-horizon software engineering with issue-specific and regression testing; the public benchmark uses reproducible Docker environments. [Scale Labs](https://labs.scale.com/leaderboard/swe_bench_pro_public) | A stronger candidate for sustained repository work spanning A01, A02, A03, and selected A05 cases. Inspect actual tasks before claiming coverage of each category. | Private and held-out portions are not publicly available. [Scale Labs](https://labs.scale.com/leaderboard/swe_bench_pro_public) Use the public set only, review its repository licenses, and do not compare different harness settings as though they were identical. |
| B03. Terminal-Bench 2.0 | Hard terminal tasks inspired by real workflows, each with its own environment, a human-written solution, and verification tests. [Benchmark paper](https://arxiv.org/abs/2601.11868) | Useful for A04 and command-line portions of A08, as well as technical work beyond editing application code. | My caution: environment competence and setup failures can dominate results. Keep infrastructure failures visible and validate the selected task subset. |
| B04. Berkeley Function Calling Leaderboard V4 | Function and tool-call accuracy, with public reproduction code and data; its overall accuracy combines subcategories. [BFCL documentation](https://gorilla.cs.berkeley.edu/leaderboard.html) | A component diagnostic for tool selection and arguments in A10, A11, and A12. Use it to investigate a suspected tool-use weakness. | My caution: this is not sufficient evidence of full workflow success, human attention savings, or security. Preserve its subcategory results rather than importing its aggregate as our pilot score. |

### Research and policy-bound interaction

| ID and option | What it actually tests | Proposed use and task mapping | Constraint or interpretation limit |
|---|---|---|---|
| B05. τ-bench, text workflows | The current repository describes policy-guided tool-agent-user interactions across service domains and now includes a newer τ³-bench release alongside text and voice modes. [Official repository](https://github.com/sierra-research/tau2-bench) | Candidate for A10. Start with text tasks so voice recognition and synthesis do not obscure the method's contribution. | The repository warns that results across a documented evaluator-fix boundary are not comparable. [Official repository](https://github.com/sierra-research/tau2-bench) Pin the release, domain, split, evaluator, user simulator, and mode; do not silently combine historic τ² scores with current runs. |
| B06. GAIA | General-assistant questions requiring reasoning, multimodal handling, web browsing, and tool use; some answers are withheld for the official leaderboard. [Research description](https://ai.meta.com/research/publications/gaia-a-benchmark-for-general-ai-assistants/) | Broad candidate for A07 and selected A08 or A12 task patterns. Inspect the accessible evaluation subset before scheduling a local run. | My caution: answering a question correctly does not establish that a long report is complete, well sourced, or safe. We need our own claim-level and human-attention measurements. |
| B07. BrowseComp | Difficult fact-seeking browsing problems with short, verifiable answers; the benchmark is open-sourced through OpenAI's simple-evals repository. [Official description](https://openai.com/index/browsecomp/) | Focused test of evidence retrieval for A07. Useful if finding obscure but correct facts is a real bottleneck. | Its authors explicitly say it does not represent common or open-ended queries and that generalization to real-user performance is uncertain. [Official description](https://openai.com/index/browsecomp/) Treat it as a retrieval stress test, not a report-quality test. |

### Browser, desktop, and company work

| ID and option | What it actually tests | Proposed use and task mapping | Constraint or interpretation limit |
|---|---|---|---|
| B08. WebArena | Long-horizon web tasks in reproducible website environments covering commerce, forums, collaborative development, and content management, judged by functional task completion. [Benchmark paper](https://arxiv.org/abs/2307.13854) | Direct candidate for A11. It lets us test outcomes without modifying your real accounts. | My caution: the worker needs a qualified browser interface, and benchmark-site success does not prove it will handle the permissions and failures of your actual SaaS tools. |
| B09. OSWorld, pinned 2.1 release | Long-horizon computer-use tasks; the current repository recommends `osworld-v2.1` and matching tasks, assets, and images rather than its development branch. [Official repository](https://github.com/xlang-ai/OSWorld-V2) | Candidate for A12 and desktop portions of A11. Choose it if GUI interaction is part of the capability you need to establish. | Full tasks/assets require gated access; setup involves provider images and hosted test services, and verified leaderboard evaluation requires maintainer coordination. [Official repository](https://github.com/xlang-ai/OSWorld-V2) This would need a separate environment feasibility check. |
| B10. TheAgentCompany | Work in a simulated software company, including coding, communication, mathematical reasoning, image processing, and text comprehension; grading includes final results and subcheckpoints. [Official repository](https://github.com/TheAgentCompany/TheAgentCompany) | The broadest candidate here for multi-tool professional workflows across A08, A09, A10, and A12. Actual task coverage must be checked before selecting a subset. | The instructions include privileged setup and evaluation, host networking, and permissive Docker-socket access. [Official repository](https://github.com/TheAgentCompany/TheAgentCompany) Selection is conditional on security feasibility across the complete installation and evaluation stack. Defer it if the common boundary cannot be satisfied; do not waive controls. |

### Earlier recommendation, retained as rationale

The user selection above supersedes this recommendation. Do not substitute the proposed alternatives below for B01, B06, and B10.

For coding, I would shortlist B02, then B03 if command-line or infrastructure work matters. B01 remains useful if published comparability is a major objective.

For non-coding, I would shortlist B05 for policy-bound workflows, B06 for general research/tool use, or B10 for simulated company work. Choose based on the tasks you select, not on which benchmark has the most impressive leaderboard.

B04 is best considered a diagnostic supplement. B07 is deliberately narrow. B08 and B09 become priorities only if browser or desktop interaction is a required part of the method's scope.

## How benchmark evidence will count

Security requirements apply to every selected suite, including installation, orchestration, evaluation, tools, and workers. Do not run benchmark-required privileged operations on the user's or a shared host, expose a host container-control socket, or grant host networking to satisfy an upstream quickstart. Any necessary privilege inside a separate disposable boundary requires explicit security qualification first. Inability to meet the common policy means deferral, not an exemption.

Run our selected systems under matched, declared conditions rather than importing someone else's leaderboard number as a result for model-mesh. Any benchmark subset must be named as a subset, selected before seeing outcomes, and reported separately from a full official score.

Keep the official grading result separate from the additional pilot measurements. Add our own defect adjudication, active human minutes, accepted-delivery time, spend, recipient checks, and attempted/actual policy violations. Do not average unrelated benchmark scores into a synthetic quality claim.

Use public benchmarks as one evidence layer and unseen representative tasks as another. A strong benchmark score cannot substitute for validation on the work you intend to delegate.

Freeze dataset, environment, evaluator, adapter, model, prompt, and policy versions. Record unavoidable differences. Judge-model and user-simulator costs belong in evaluation overhead, separately identified from the cost of the system doing the task.

## Measurement questions that remain open

Your priority order is settled. These questions concern definitions and evidence, not a request to renegotiate it.

- Which versioned references/templates and correctness criteria define defects in each task class? Every confirmed defect already makes the task fail.
- Which AI-judge configurations, calibration checks, and human dispute-resolution procedure apply? The adjudication model is already selected.
- How much repeated evidence is required before calling a difference an improvement rather than run-to-run noise?
- How should an uncertain comparison be treated? My recommendation is inconclusive, not an assumed pass.
- How will all active owner pilot attention be recorded and allocated, including setup and independent evaluation, without double counting shared effort?
- Which exact configurations, visible checks, and agent-review procedures define each selected comparison stage? The feedback categories are already settled.
- Deferred until requested: project case-study selection and publication permissions. Do not use this as a reason to delay benchmark selection.

After selections, I will propose a concrete defect taxonomy and acceptance examples for those task types. We will resolve those before sample size, thresholds, or implementation.
