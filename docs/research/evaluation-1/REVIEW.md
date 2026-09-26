# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 26 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker or required correction was found in the eight-document package. D43 through D45 expand research to five harnesses, verification architecture, and open-source verification tooling without authorizing runtime enrollment, skill or template changes, installation, spending, or benchmark execution. ([README.md](README.md), [DECISIONS.md](DECISIONS.md#settled-decisions))

## Scope and method

I reviewed the complete changes to the five original substantive documents and read all three new research reports. The local branch is `evaluation-1`, based on HEAD `273c83b1fefa095b5fdfb952d48ae8d60a28568a`; this identifies the baseline, not the reviewed working-tree content.

I read the preceding review and verified that all five original committed documents match its D42 fingerprints. I checked the research against relevant local skill, evidence, domain-template, mirrored-instruction, and CI source passages at that baseline, inspected the supplied rendered article extracts, recalculated the conditional attempt/judge counts, and selectively fetched primary documentation for high-risk claims.

The working-tree changes are limited to the evaluation documentation, with three new research reports. Operational skills, templates, CI, and runtime files are not changed by this package. I made no target-file or git-state changes. This report was authored outside the repository for incorporation as `REVIEW.md`.

## Prior review history

The original two-document review returned REVISE for R1 through R3. Corrected versions received SHIP for documentation only, as did the expanded planning package and subsequent owner-decision updates through D42. Earlier nonblocking wording notes were corrected and independently rechecked. No previous verdict certified runtime safety, measured effectiveness, or feasibility.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording allowed compensated regressions and weakened mandatory controls. | High | Resolved. Mandatory controls and evidence remain required; no objective regression can be compensated by another improvement, and uncertainty cannot silently pass. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. The client purpose and priorities remain fixed; useful-work discovery is deferred. ([Plan: Agreed priorities](PLAN.md#agreed-priorities), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review omitted parts of the execution stack. | High | Resolved. Installers, coordinators, evaluators, simulated users, tools, and workers share the mandatory boundary; unmet controls require deferral rather than waiver. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The original menus remain twelve scenarios and ten benchmarks. Selected suites remain B01 SWE-bench Verified, B06 GAIA, and B10 TheAgentCompany; coverage gaps and supplemental cases remain explicit rather than being claimed as qualified standardized coverage. ([BENCHMARKS.md](BENCHMARKS.md))

Previously reviewed decisions remain in force:

- D14 through D18 retain separate method-first and routing-second comparisons, final post-repair scoring, at most one repair within the matched envelope, no scored human rescue, frozen failures, and separately authorized unscored rescue without score replacement. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D19 through D25 retain checks plus agent review without hidden final-evaluator feedback, failure for every confirmed defect including cosmetic defects, matched class-based caps, exact templates with advance exceptions, two independent final AI judges, and personal owner dispute resolution after artifact freeze. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D26 through D29 retain the continuous 10-hour clock from first scored dispatch and the global USD 100 ceiling for all new pilot model/tool/compute charges, including setup and cleanup. Neither resets per arm, suite, or harness. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [Harness workload implications](harness-feasibility.pplx.md#what-assessing-all-five-does-to-the-experiment))
- D30 through D33 retain the eight-minute dispute window capped by the global deadline, unresolved/not-accepted timeout outcomes, minimum breadth before depth, whole-pilot coverage with stage-local matched claims, and all active owner attention without duplicated minutes. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))
- D34 through D37 retain fourteen distinct underlying cases, two per selected scenario, timer-plus-log recording, task distinctness without a different-context requirement, and missing rather than estimated or zero forgotten intervals. No missing-data analysis exception is currently agreed. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))
- D38 through D40 retain two routine cases per scenario and matched arms on every case, with each scenario pair in one stage. Method covers A01/A03/A05/A09 and routing covers A08/A11/A12, giving eight and six cases, fourteen matched comparisons and twenty-eight initial attempts per complete implementation before repeats. These are design counts, not independent attempt identities or a powered sample. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))
- D41 continues only the predeclared comparisons after ordinary acceptance failure in any arm, preserving outcomes without extra repair, replacement, tuning, or hidden-grader leakage. Safety and resource stops override continuation. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation))
- D42 limits task material to eligible public and genuinely synthetic inputs across preparation, retrieval, tools, review, judging, and evidence. Public status neither grants permissions nor makes secrets and owner records public; excluded content invokes incident handling, and results do not establish confidential-client performance. ([Plan: Public and synthetic task-data boundary](PLAN.md#public-and-synthetic-task-data-boundary), [ANALYSIS.md](ANALYSIS.md#what-the-evaluation-can-establish))

## Current findings

### Research scope and authority are consistent

All five requested harnesses have explicit coverage: OpenCode, pi-agent interpreted as the Pi coding-agent CLI, Qwen Code, Aider, and Goose. Each has a documented entry point, source-license observation, native-loop or permission risks, and adapter qualification questions; no candidate is silently dropped or described as runtime-qualified. ([Harness assessment: Native interfaces and evidence gaps](harness-feasibility.pplx.md#native-interfaces-and-evidence-gaps), [Harness assessment: Candidate-specific qualification](harness-feasibility.pplx.md#candidate-specific-qualification))

The prior preference for researching only one alternative is superseded for research. Remaining references to a second harness describe the minimum evidence needed for portability, not a reduced research population; actual scored enrollment, releases, models, and qualification order remain open. ([PLAN.md](PLAN.md#implementation-choices), [ANALYSIS.md](ANALYSIS.md#distinguish-the-experiments-causes), [DECISIONS.md](DECISIONS.md#open-questions))

D44 and D45 request assessment, not implementation. The proposed verification contracts, driver operations, templates, MCP interfaces, diagnostics, and soak plans are labeled proposals rather than existing tools, approved thresholds, or new benchmark selections. ([Verification framework research](verification-framework-research.pplx.md#proposed-reusable-artifacts), [Open-source stack: MCP boundary](open-source-verification-stack.pplx.md#mcp-boundary-proposed), [BENCHMARKS.md](BENCHMARKS.md#rules-already-settled))

### Conditional counts do not expand the scored design

Fourteen cases times two competing arms times five harnesses equals 140 initial attempts; two judges for each submitted final deliverable would yield 280 assessments only if every attempt submitted one. I recalculated these quantities, and the report explicitly treats them as conditional workload arithmetic on fourteen task identities, not 140 independent tasks, approved enrollment, a cost estimate, or statistical power. ([Harness assessment: What assessing all five does to the experiment](harness-feasibility.pplx.md#what-assessing-all-five-does-to-the-experiment))

Both required stages, their scenario mapping, the one-repair rule, no-human-rescue restriction, and global limits remain unchanged. Native retries and initial-work loops require explicit accounting and matched configuration; they cannot reopen final failure or leak grader evidence into later work. ([PLAN.md](PLAN.md), [Harness assessment: Common adapter contract](harness-feasibility.pplx.md#common-adapter-contract-proposed), [Framework: Maintain skills between experiments](verification-framework-research.pplx.md#maintain-skills-between-experiments-not-inside-a-frozen-one))

### Article analysis does not import promotional claims

The supplied rendered article extracts support identifying both pieces as Signadot-sponsored articles by Arjun Iyer and show the fivefold-shipping and mathematical-proof language being criticized, rather than adopted as model-mesh results. The framework report separates those claims from testable recommendations about environments, structured feedback, and verification capacity. ([CI/CD article](https://thenewstack.io/coding-agents-cicd-fix/), [Distributed-systems article](https://thenewstack.io/agentic-verification-distributed-systems/), [Framework article assessment](verification-framework-research.pplx.md#what-the-two-articles-actually-argue))

The report treats the 2,000-PR anecdote as a reported workflow claim without a controlled quality denominator, rejects ordinary testing as mathematical proof, and does not assert that mocks are always useless or request routing alone isolates distributed state. Its state inventory includes databases, caches, queues, asynchronous workers, side effects, and telemetry, with explicit negative checks. ([Framework: Adopt the mechanisms, not the absolutes](verification-framework-research.pplx.md#adopt-the-mechanisms-not-the-absolutes), [Framework: Environment isolation requires a state inventory](verification-framework-research.pplx.md#environment-isolation-requires-a-state-inventory))

### Repository gaps are grounded and deferred correctly

The report's principal source observations match the inspected baseline: generic loop defaults permit more repair cycles than evaluation-1, `mm-verify` requests reruns and offers a caveated verdict, ordinary evidence need not contain hashes, the domain template is prose-oriented, and the method introduction contains an unmeasured model-superiority assertion. The proposed evaluation-profile precedence, immutable evidence, safe replay, and narrower claims address those gaps without pretending they are already implemented. ([Method snapshot](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-method/SKILL.md), [Verifier snapshot](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-verify/SKILL.md), [Evidence snapshot](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-method/references/evidence.md), [Framework gap table](verification-framework-research.pplx.md#current-framework-skill-and-template-gaps))

The research report's "Required" and "High" implementation findings are future qualification work, not defects silently repaired by this PR. Their presence means current operational skills cannot be assumed to enforce this evaluation merely because the documentation ships. ([Framework: Current framework, skill, and template gaps](verification-framework-research.pplx.md#current-framework-skill-and-template-gaps), [Framework: Prioritized change proposal](verification-framework-research.pplx.md#prioritized-change-proposal))

### Open-source eligibility is checked across components

The stack report separates engine, MCP server, required plugin, and backend eligibility rather than treating an open connector or free tier as sufficient. Figma is excluded from the all-OSS verification backend proposal, and Signadot is not qualified as an end-to-end OSS dependency. Those exclusions are supported by Figma's restricted service-access terms and Signadot's documented hosted control plane, without making a broader claim that every related component is proprietary. ([Stack eligibility and exclusions](open-source-verification-stack.pplx.md#exclusions-and-non-equivalences), [Figma terms](https://www.figma.com/legal/tos/), [Signadot FAQ](https://www.signadot.com/docs/concepts/faq))

The pstack example is explicitly fictionalized, omits its CLI and driver implementation, and did not establish a license on the inspected repository page. The package therefore proposes original templates rather than presenting that public example as cleared reusable code. The delivered documentation does not add a copied driver or operational template. ([Example repository](https://github.com/poteto/verification-skill-example), [Framework reusable artifacts](verification-framework-research.pplx.md#proposed-reusable-artifacts))

The reports distinguish core project license observations from pinned dependency clearance, hosted service eligibility, and deployment obligations. Extending the all-OSS requirement to hosting and inference remains an explicit question, not a presumed proprietary verification-backend exception. ([Stack: Eligibility rule](open-source-verification-stack.pplx.md#eligibility-rule), [DECISIONS.md](DECISIONS.md#open-questions))

### MCP access is not a test oracle or security boundary

The stack separates deterministic final test engines from worker-side browser access, independent judges, immutable design references, and monitoring views. A dashboard, tool response, or model-authored success statement cannot replace the frozen checks or authoritative application state. ([Stack: Browser and design validation](open-source-verification-stack.pplx.md#browser-and-design-validation), [Stack: Logs, traces, and monitoring](open-source-verification-stack.pplx.md#logs-traces-and-monitoring))

Powerful tool capabilities are disclosed rather than assumed safe: Penpot plugin code execution, Browser Use nested-agent delegation and security-disable settings, Grafana mutation/raw-query controls, load generators, and active security scans all require bounded policy and qualification. The report does not authorize enabling those features. ([Stack tool assessment](open-source-verification-stack.pplx.md#tool-and-license-assessment), [Penpot MCP](https://github.com/penpot/penpot-mcp), [Browser Use MCP](https://docs.browser-use.com/open-source/customize/integrations/mcp-server), [Grafana MCP](https://github.com/grafana/mcp-grafana))

The soak proposal specifies workload, completed duration, invariants, abort/cleanup behavior, and generator health without inventing approved thresholds or treating a curtailed run as a full pass. The k6 checks-versus-thresholds warning is supported by the primary documentation and directly addresses a false-green risk. ([Stack: Load, soak, and fault validation](open-source-verification-stack.pplx.md#load-soak-and-fault-validation), [k6 thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/))

## Selective source checks

The following load-bearing documentation claims were re-fetched during this review. These checks establish documentary support, not runtime behavior:

| Claim checked | Finding |
|---|---|
| Pi settled completion differs from a low-level run ending. | Supported. `agent_settled` follows session-level automatic continuation; `agent_end` alone does not establish that boundary. ([Pi RPC](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/rpc.md)) |
| Qwen can have opt-in indefinite transient retries, per-message budget resets, and bounded tool-result previews. | Supported by the headless documentation, including the warning that `--yolo` does not enable a sandbox. ([Qwen headless guide](https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/)) |
| OpenCode permissions are broadly permissive by default, and Goose defaults to autonomous mode. | Supported; neither default is treated as pilot authorization. ([OpenCode permissions](https://opencode.ai/docs/permissions/), [Goose permissions](https://goose-docs.ai/docs/guides/managing-tools/goose-permissions/)) |
| Penpot MCP is MPL-2.0, executes plugin code, and requires the plugin connection to stay open. | Supported, without evidence of an independently enforced read-only or headless guarantee. ([Penpot MCP](https://github.com/penpot/penpot-mcp)) |
| Browser Use local MCP includes delegated agent execution and a security-disable setting. | Supported; these are capabilities to restrict, not security guarantees. ([Browser Use local MCP](https://docs.browser-use.com/open-source/customize/integrations/mcp-server)) |
| Grafana MCP is Apache-2.0 and has read-only flags, raw-query exclusions, and explicit overrides. | Supported. Qualification still needs least-privilege backend credentials, exact tool restrictions, and query bounds; the flag alone is not universal enforcement. ([Grafana MCP](https://github.com/grafana/mcp-grafana)) |
| k6 checks alone do not fail the process, while failed thresholds affect exit status. | Supported. ([k6 thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/)) |
| The pstack example omits executable drivers; Signadot uses a hosted control plane; Figma terms are not an OSS backend license. | Supported within the inspected pages and the report's cautious licensing language. ([pstack example](https://github.com/poteto/verification-skill-example), [Signadot FAQ](https://www.signadot.com/docs/concepts/faq), [Figma terms](https://www.figma.com/legal/tos/)) |

## Open prerequisites, not documentation blockers

Before implementation or execution, separately approve the actual scored harness population, qualification order, immutable releases, model-role inventories, common adapter contract, and actual case manifest. Keep every comparison matched within its stage and retain the approved scenario mapping. ([Harness proposed sequence](harness-feasibility.pplx.md#proposed-decision-sequence), [DECISIONS.md](DECISIONS.md#open-questions))

The future implementation needs evidence for profile precedence, bounded native loops, isolation, cancellation, late-result rejection, protected grader assets, complete accounting, telemetry integrity, safe replay, and cleanup. Documented APIs and OSS licenses do not satisfy those tests. ([Framework: Prioritized change proposal](verification-framework-research.pplx.md#prioritized-change-proposal), [Harness common contract](harness-feasibility.pplx.md#common-adapter-contract-proposed))

Pin and qualify only the test tools justified by actual cases, including license/dependency review, recipients, transport permissions, secrets, retention, and relevant backend controls. Numeric load/soak plans, resource allocations, cutoff classifications, and statistical evidence requirements remain open; return for a scope decision if the selected work cannot fit without weakening controls. ([Stack: Admission and measurement implications](open-source-verification-stack.pplx.md#admission-and-measurement-implications), [DECISIONS.md](DECISIONS.md#open-questions))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `9bb5d96ebba0fe5cf3b44928517feeabd2625075541082c0768d0fe34fc2b86a` |
| `PLAN.md` | `85ac484cacc9dbc1f80d647adbf3c54f3d237cdeeb0cad84fb7f4716cc9c3450` |
| `BENCHMARKS.md` | `d7b889f01064afcc2270e9449e0c6c390b820ac4c279db4d71618b8cde4a166f` |
| `ANALYSIS.md` | `52ec4547afdb55b35554dbcd5d081b847e2e6c419ee8b2a3eb1170068b8045ca` |
| `DECISIONS.md` | `f0d4cc84bba855b8c843f5340c24a96a814b710dcc4039f9451634fb539aa1c1` |
| `harness-feasibility.pplx.md` | `7fcd48b80d9edc9aff0c24e43463fd63f1cee5c22923bed5589bce63a58a1b64` |
| `verification-framework-research.pplx.md` | `a5c582e7bfc2fd8d82dc3d2e058998ec65c9878ce38082087275dfc1bfe81251` |
| `open-source-verification-stack.pplx.md` | `a61775788b57495da8e02cd6f0e3e02eae7d1df63cda46e11f259b929182ee64` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to any substantive document require renewed review.

## Limits

- This is a documentation and selective source-support review, not runtime certification, implementation approval, execution authority, license clearance, privacy clearance, or evidence of effectiveness.
- No installations, benchmark runs, model-runtime tests, browser-task trials, scans, load generation, soak tests, penetration tests, or feasibility/cost trials were performed. They are not required for this documentation-only decision.
- Source verification was selective. I did not independently re-fetch every citation, validate every core license and transitive dependency, or reproduce DORA/METR analyses. The supplied rendered article extracts were read; I did not repeat the article browser collection.
- Upstream documentation is mutable. Its current statements do not identify the user's installed release or prove behavior at a future pinned version.
- Repository source observations were checked read-only at the stated baseline. The whitespace diff check passed, but repository CI gates and runtime conformance were not run or certified.
- Fidelity was assessed against the supplied owner decisions and review history, not an independently authenticated transcript of every discussion.
- Actual task-data eligibility, credential isolation, negative controls, and resource enforceability remain unqualified. No claim is made that all five grids or meaningful soak coverage fit the global limits.
- Remote PR, branch, and main state were not independently verified or changed. The existing PR workflow and separately run repository gates remain the integrating agent's responsibility.

**Final disposition: SHIP the eight fingerprinted documents through the existing PR workflow. No operational skill/template changes, installation, pilot execution, or expenditure are authorized.**
