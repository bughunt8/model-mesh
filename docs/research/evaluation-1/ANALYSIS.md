# Evaluation 1 analysis

Design analysis, not experimental results | 22 September 2026

## What the evaluation can establish

The client-facing goal requires separating three claims: a workflow can complete specified tasks, it improves on a declared comparator, and its controls behave as required under tested failure conditions. Passing one does not establish the others.

The existing model-mesh repository presents its routing rationale as heuristics and disclaims general quantitative quality and cost guarantees. Evaluation should produce evidence for narrower claims rather than remove those caveats pre-emptively. [Model-mesh repository](https://github.com/bughunt8/model-mesh)

A future client statement must identify the evaluated scope, model and harness versions, task population, controls, comparator, sample size, failures, and uncertainty. Successful historical projects can demonstrate experience, but cannot by themselves identify which part of the method caused improvement.

## Distinguish the experiment's causes

Proposed comparisons should isolate the disciplined loop, role-specific model routing, harness portability, and optional parallel orchestration. Changing all four at once gives a system comparison, not an estimate of the method's individual contribution.

If the chosen reference is a compatible single-model harness, use the staged comparisons in [PLAN.md](PLAN.md). If the relevant reference is human-led or already multi-model, either add a separately named controlled reference or limit claims to whole-system differences. Do not rename an unmatched system comparison a controlled method-effect test.

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
- **Architecture planning.** Freeze a brief and constraint set, then independently assess traceability, feasibility, and contradictions. Document assessor disagreement; an LLM score alone is not sufficient evidence.

Supplemental case construction is a proposal awaiting the final protocol. It is not already performed, approved for execution, or an official score from a selected public benchmark.

## Define defects before optimizing anything

The primary objective is fewer defects, not a higher completion score alone. Report both task-level outcomes and severity-specific defect outcomes across the full assigned population.

The next protocol must distinguish a defect caught before submission, a defect reaching the reviewer, a false acceptance, an escaped defect within a declared observation window, an incomplete task, and a correct safe refusal. Do not reward a system that avoids all defects by refusing every feasible task; completion, required behavior, and safety must be interpreted together.

Within each scenario, freeze what counts as an opportunity for failure and how duplicate findings are deduplicated. Do not compare defect counts across tasks of very different scope without their task-level denominators.

Do not average a serious defect away with many trivial successes. Severity thresholds and the adjudication owner remain unresolved, and therefore cannot yet be used to make an adoption claim.

## Human attention and cost boundaries

Keep three ledgers distinct:

| Ledger | Proposed contents | How it affects interpretation |
|---|---|---|
| Operational delivery | Briefing, clarifications, supervision, ordinary review, agent reviewer calls, corrections, recovery, tool and inference usage. | Counts in workflow attention, time, and cost. Normal model-mesh review is not experiment-only overhead. |
| Independent evaluation | Hidden tests, benchmark grading, independent defect adjudication, simulator calls used only for evaluation, and experimental record keeping. | Report separately; apply equivalent evaluation requirements to comparison arms. |
| Setup and qualification | Adapter work, installation audit, sandbox qualification, environment provisioning, and operator training. | Report cash and person-hours. Any amortization must state a horizon and deployment volume before comparison. |

If one action serves both delivery and evaluation, predeclare the allocation rule and report it once. Do not move inconvenient costs between ledgers after seeing results.

The lower-total-cost objective must have a declared scope and horizon. A low steady-state token bill does not establish lower total adoption cost when setup or review effort is omitted. No rate for owner time or amortization horizon has been agreed.

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
