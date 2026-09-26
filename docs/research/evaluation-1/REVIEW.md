# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 26 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker or required correction was found in D46. All eight documents consistently require open-source harnesses and verification software, while allowing consideration of inference models and hosting infrastructure that need not be open source. Consideration is not selection, qualification, or execution approval. ([README.md](README.md), [PLAN.md](PLAN.md#verification-research-and-open-source-tools), [DECISIONS.md](DECISIONS.md#settled-decisions))

## Scope and method

I reviewed the complete uncommitted diff across all eight substantive documents on local branch `evaluation-1`, based on HEAD `779ec7007ba878f3b49b2c740517ddcaab15cb1f`. The commit identifies the baseline, not the reviewed working-tree content.

I read the preceding independent review, verified that all eight committed baseline documents match its fingerprints, and searched the current documents for stale unresolved-license wording and conflicting hosting, inference, provider, and backend rules. Unchanged research was assessed through that verified baseline and the relevant current passages, not re-researched. The whitespace diff check passed.

I made no target-file, branch, or git-state changes. This report was authored outside the repository for incorporation as `REVIEW.md`.

## Prior review history

The original two-document review returned REVISE for R1 through R3. Their corrected versions received SHIP for documentation only, as did the expanded planning package and successive owner-decision reviews through D45. Earlier nonblocking wording notes were corrected and independently rechecked. No prior verdict certified runtime safety, effectiveness, affordability, or execution readiness.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording allowed compensated regressions and weakened mandatory controls. | High | Resolved. Mandatory controls and evidence remain required; objective regressions cannot be compensated by other gains, and uncertainty cannot silently pass. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. The client purpose and priorities remain fixed; useful-work discovery remains deferred. ([Plan: Agreed priorities](PLAN.md#agreed-priorities), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review omitted parts of the execution stack. | High | Resolved. Installers, coordinators, evaluators, simulated users, tools, and workers share the mandatory security boundary, with deferral rather than waiver where controls cannot be met. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The twelve-scenario and ten-benchmark menus remain recorded, with B01 SWE-bench Verified, B06 GAIA, and B10 TheAgentCompany selected and supplemental coverage gaps explicit. ([BENCHMARKS.md](BENCHMARKS.md))

Previously reviewed decisions remain in force:

- D14 through D18 retain separate method-first and routing-second comparisons, final post-bounded-repair scoring, at most one repair within matched caps, no scored human rescue, frozen failures, and separately authorized unscored rescue without rewriting outcomes. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D19 through D25 retain checks plus agent-review feedback without hidden final-evaluator information, failure for every confirmed defect including cosmetic defects, matched class-based caps, exact templates with advance exceptions, two independent AI judges, and personal owner dispute resolution after artifact freeze. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D26 through D29 retain the continuous 10-hour clock from first scored dispatch and one USD 100 ceiling for all new pilot model/tool/compute charges, including setup and cleanup, with no per-arm, suite, or harness reset. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits))
- D30 through D33 retain the eight-minute dispute window capped by the global deadline, unresolved/not-accepted timeout outcomes, minimum breadth before depth, whole-pilot coverage with matched stage-local claims, and all active owner attention without duplicated minutes. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))
- D34 through D37 retain fourteen distinct underlying cases across the pilot, two per selected scenario, timer-plus-log attention recording, no different-context requirement, and missing rather than estimated or zero forgotten intervals. No missing-data analysis exception is currently agreed. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))
- D38 through D40 retain two routine cases per scenario, intact scenario pairs within a stage, and both matched arms on every case. Method covers A01/A03/A05/A09; routing covers A08/A11/A12, giving eight and six cases and twenty-eight initial attempts per complete implementation before repeats. These are not twenty-eight independent task identities or a powered sample. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))
- D41 continues the predeclared sample after ordinary acceptance failure in any arm without extra repair, replacement, tuning, or hidden-grader leakage. Frozen outcomes remain visible, and safety and resource stops override continuation. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation))
- D42 restricts task material to eligible public and genuinely synthetic inputs throughout preparation, retrieval, tools, review, judging, and derived evidence. Private records and real credentials are excluded; operational records retain separate controls, and excluded content invokes incident handling rather than ordinary-failure continuation. ([Plan: Public and synthetic task-data boundary](PLAN.md#public-and-synthetic-task-data-boundary))
- D43 through D45 expand research to OpenCode, pi-agent, Qwen Code, Aider, and Goose; assess the two supplied articles and framework gaps; and require open-source verification engines, MCP interfaces, required plugins, and backends. They do not authorize implementations, installations, five scored grids, or new budgets. D46 now resolves the previously open extent of the license requirement. ([DECISIONS.md](DECISIONS.md), [Harness assessment](harness-feasibility.pplx.md), [Framework assessment](verification-framework-research.pplx.md), [Stack assessment](open-source-verification-stack.pplx.md))

The expanded-research review checked the article extracts, relevant repository source at snapshot `273c83b1fefa095b5fdfb952d48ae8d60a28568a`, and selected primary documentation. It supported the distinction between sponsored productivity claims and measured evidence, the documented native-loop/tool risks, and deferred implementation gaps; it did not certify every citation or runtime behavior. Those findings remain the prior review basis, not newly repeated checks.

The research still treats the 140-attempt five-harness grid and possible 280 final-judge assessments as conditional arithmetic on fourteen task identities, not an approved sample, an independent sample count, a performance result, or an affordability claim. ([Harness workload implications](harness-feasibility.pplx.md#what-assessing-all-five-does-to-the-experiment))

## Current findings

### The owner-selected license boundary is faithfully recorded

D46 explicitly covers harnesses and the verification stack while excluding inference models and hosting infrastructure from the open-source mandate. The plan applies this distinction to worker, reviewer, judge, and auxiliary-model calls, rather than accidentally exempting a model role from recipient or budget controls. ([Decision D46](DECISIONS.md#settled-decisions), [Plan: Verification research and open-source tools](PLAN.md#verification-research-and-open-source-tools))

The same distinction appears in the README, benchmark rules, analysis, harness identity section, framework implications, and stack eligibility section. No document selects a provider, model, host, or deployment merely because the license requirement no longer excludes it. ([README.md](README.md), [BENCHMARKS.md](BENCHMARKS.md#rules-already-settled), [ANALYSIS.md](ANALYSIS.md#distinguish-the-experiments-causes), [Harness license scope](harness-feasibility.pplx.md#identity-and-open-source-scope), [Framework implications](verification-framework-research.pplx.md#open-source-tools-and-mcp-implications), [Stack eligibility](open-source-verification-stack.pplx.md#eligibility-rule))

### Hosting does not create a proprietary-backend exception

The plan and stack report distinguish the commercial infrastructure on which eligible software runs from the software supplying verification. Proprietary design, monitoring, browser-automation, or testing backends remain outside the approved license boundary even when accessed through open-source MCP interfaces. The decision log expressly rejects relabeling a proprietary verification backend as hosting. ([PLAN.md](PLAN.md#verification-research-and-open-source-tools), [Stack eligibility](open-source-verification-stack.pplx.md#eligibility-rule), [DECISIONS.md](DECISIONS.md#superseded-or-constrained-proposals))

Figma remains excluded from the all-OSS verification proposal; hosted Browser Use is not silently substituted for the assessed local path; enterprise-only monitoring functions and Signadot remain unqualified as required OSS verification dependencies. The report's local/self-managed default is a recommendation, not a claim that approved commercial hosting is prohibited. ([Stack exclusions](open-source-verification-stack.pplx.md#exclusions-and-non-equivalences), [Stack eligibility](open-source-verification-stack.pplx.md#eligibility-rule))

### Policy and experimental controls are not broadened

Recipient eligibility, public/synthetic task content, residency, retention, permissions, isolation, bounded charges, and the shared global budget remain binding. The analysis preserves matched models, hosts, settings, and conditions where required by each controlled comparison rather than treating license eligibility as freedom to vary an arm after results. ([PLAN.md](PLAN.md#verification-research-and-open-source-tools), [ANALYSIS.md](ANALYSIS.md#distinguish-the-experiments-causes), [Harness license scope](harness-feasibility.pplx.md#identity-and-open-source-scope))

No execution, installation, network call, expenditure, skill/template modification, new case selection, repair opportunity, acceptance relaxation, or proprietary verification service is approved by D46. The benchmark document also makes clear that this decision neither qualifies a benchmark nor changes its own license. ([PLAN.md](PLAN.md#verification-research-and-open-source-tools), [BENCHMARKS.md](BENCHMARKS.md#rules-already-settled), [Stack eligibility](open-source-verification-stack.pplx.md#eligibility-rule))

### Stale unresolved-scope wording has been removed

The prior open question about extending OSS requirements to inference and hosting is replaced in O17 with component qualification and provider/host policy approval. The plan, harness report, framework remaining-decisions section, and stack eligibility rule now treat license scope as settled. Actual deployments and their dependency inventories remain legitimately unresolved. ([DECISIONS.md](DECISIONS.md#open-questions), [PLAN.md](PLAN.md#verification-research-and-open-source-tools), [Harness license scope](harness-feasibility.pplx.md#identity-and-open-source-scope), [Framework remaining decisions](verification-framework-research.pplx.md#decisions-still-needed), [Stack eligibility](open-source-verification-stack.pplx.md#eligibility-rule))

The plan advances to v0.18. No external-source facts are newly established by this owner decision, and the older research dates remain evidence dates rather than claims of new source verification. ([PLAN.md](PLAN.md), [BENCHMARKS.md](BENCHMARKS.md#ten-researched-benchmark-options), [Harness assessment](harness-feasibility.pplx.md), [Framework assessment](verification-framework-research.pplx.md), [Stack assessment](open-source-verification-stack.pplx.md))

## Open prerequisites, not documentation blockers

Before implementation or execution:

- Pin the harnesses and verification engine/MCP/plugin/backend versions and inspect their dependency and license inventories.
- Approve exact inference endpoints, model roles, hosting environments, recipients, residency, retention, credentials, permissions, and resource accounting.
- Classify managed offerings by the actual verification components they supply, not their marketing label as hosting or infrastructure.
- Freeze actual cases, scored harness enrollment, matched configurations, templates, judges, numeric task caps, repeats, and the evidence standard.
- Complete external enforcement, cancellation, evidence protection, native-loop, tool-permission, and whole-stack security qualification.
- Establish feasible reservations and cutoff procedures within the unchanged global limits; return for a scope decision if the required work cannot fit safely.

These are remaining qualification and authorization matters, not a request to reopen the settled D46 boundary. ([Decision log: Open questions](DECISIONS.md#open-questions), [Harness proposed sequence](harness-feasibility.pplx.md#proposed-decision-sequence), [Stack eligibility](open-source-verification-stack.pplx.md#eligibility-rule))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `c3613f17651884b3bf8bb24c7da54e7d0673933dc9fb144429e94456b185e8ab` |
| `PLAN.md` | `b17461f74bced98840bb13eaa640a0a7f30cefc33b6877e9caadeea16579be21` |
| `BENCHMARKS.md` | `7f4b0cc53e60a146bbbc4cab6d8e21a24a77a1b7d34039c665a1a9e77b049f5a` |
| `ANALYSIS.md` | `e726dc4e1cf80431047fef6c8060c46bb4d6d23cdf48d401f1dbf1a27f25ab1f` |
| `DECISIONS.md` | `74006dd677683cdfdd2a7b86256463353b540d9a10778d0d874a8a6b94927c3f` |
| `harness-feasibility.pplx.md` | `0bfeafb563c1e1cc966d0a77d720ed8b83db9237cb4e28f08f42d75f8d77520c` |
| `verification-framework-research.pplx.md` | `e3ed73218e9133f6cedf801350b749fc02d8e81808351e9db5dec181391d8611` |
| `open-source-verification-stack.pplx.md` | `255bc4aaffe0cfaec6f61bdf9593e05c3f6b99c42348bbd15fb4162d0e25ca8b` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to any substantive document require renewed review.

## Limits

- This is a read-only documentation review, not license clearance, privacy clearance, provider or host approval, runtime certification, execution authority, or a guarantee of effectiveness.
- No new external research was performed for D46. Earlier selective source checks are preserved as history, not represented as an exhaustive or newly refreshed source audit.
- No installations, benchmark execution, model-runtime calls, scans, load/soak tests, timing trials, cost simulations, or feasibility trials were performed. None is required for this docs-only change.
- No core skill/template/CI or runtime changes were made or authorized. Existing implementation gaps remain qualification prerequisites.
- The whitespace diff check was performed; repository gates and runtime conformance were not run or certified and remain the integrating agent's responsibility.
- Fidelity was assessed against the supplied owner answer and review history, not an independently authenticated transcript of every discussion.
- No remote PR, branch, or main state was independently verified or changed.

**Final disposition: SHIP the eight fingerprinted documents through the existing PR workflow, subject to separately run repository gates. No provider, host, implementation, pilot execution, or expenditure is approved by this review.**
