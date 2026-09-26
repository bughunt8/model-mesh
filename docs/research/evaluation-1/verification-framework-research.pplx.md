# Agentic verification and the changes model-mesh needs

Research and repository assessment, 26 September 2026, Hong Kong time. This report proposes changes; it does not implement them or authorize a pilot, deployment, scan, or expenditure.

## Executive assessment

Model-mesh should strengthen its verification contract, existing skills, and reusable templates. The useful change is a separation between the agent producing work, the environment in which that work is exercised, and the independent machinery that decides what the evidence establishes. It is not a switch to a particular vendor, unlimited self-repair, or automatic production promotion.

The two supplied articles correctly direct attention to verification capacity and programmable runtime access, but both are sponsored by Signadot and written by its CEO, Arjun Iyer. Their general architectural recommendations deserve examination; their productivity multipliers and claims of mathematical proof should not become model-mesh promises ([CI/CD article](https://thenewstack.io/coding-agents-cicd-fix/), [distributed-systems article](https://thenewstack.io/agentic-verification-distributed-systems/)).

Model-mesh already requires observed checks, independent review, authorization, and negative evidence. The inspected operational skills do not yet express the complete environment identity, state isolation, tool authority, immutable evidence, and asynchronous completion contract needed to enforce the evaluation plan across five harnesses ([method snapshot](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-method/SKILL.md), [evidence standard snapshot](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-method/references/evidence.md)).

The recommended direction is:

- **Keep the portable method.** Define observable requirements and independent acceptance without binding the theory to oh-my-openagent.
- **Add a verification control layer.** Own environment leases, frozen plans, evidence, permissions, cancellation, and budgets outside worker-controlled context.
- **Extend existing skills first.** Introduce app-local feature maps and executable checks without duplicating the coding domain or replacing every skill.
- **Use an open-source verification stack.** Prefer deterministic engines and bounded interfaces; add MCP only where agent interaction needs it.
- **Keep evaluation claims narrow.** Preserve the settled routine/public-synthetic scope, one-repair rule, two judges, stage allocation, and global limits.

Companion reports cover [all five harnesses](harness-feasibility.pplx.md) and the [open-source verification stack](open-source-verification-stack.pplx.md). Neither contains measured runtime results.

## Scope and evidence

This assessment inspected the model-mesh checkout at baseline commit `273c83b1fefa095b5fdfb952d48ae8d60a28568a`, including `AGENTS.md`, the four shipped skills, evidence/gate/domain references, the domain template, and the repository check workflow. It also read the current evaluation package. Source inspection is not a runtime security audit.

The New Stack pages initially failed the content-fetch service's crawler checks; both were then read through their rendered public pages. Their article bodies, author/date information, sponsor disclosures, and original pstack link were inspected. Primary technical documentation, the original pstack post and public example, DORA material, and METR's later study update were used to challenge the articles' stronger claims.

No proprietary code, client material, credentials, or production telemetry was used. No advertised throughput, price, safety, or quality benefit was imported as a result for model-mesh.

## What the two articles actually argue

| Article | Key points | Evidence status |
|---|---|---|
| "Why coding agents will break your CI/CD pipeline (and how to fix it)," 2 April 2026 | Code generation moves the bottleneck toward validation; shared staging becomes congested; full-stack copies can be expensive; combine per-change environments with skills that run integration checks, inspect logs, and iterate before PR review ([article](https://thenewstack.io/coding-agents-cicd-fix/)). | Sponsored architectural argument, not a controlled study of model-mesh or all engineering teams. The asserted fivefold shipping advantage is not supported by a comparative experiment in the article. |
| "One engineer shipped 2,000 PRs a month to production. Verification is the key," 19 September 2026 | Starts from Lauren Tan's pstack workflow, emphasizes a CLI and feature map, then argues distributed systems need realistic dependencies, concurrent per-change isolation, delta-sized environments, rapid provisioning, and CLI/MCP access ([article](https://thenewstack.io/agentic-verification-distributed-systems/)). | Sponsored interpretation of a personal workflow report. Its architectural discussion is distinct from proof of the reported volume, quality, or general productivity benefit. |

The second article's original link leads to Tan's pstack post, which describes a verification meta-skill, a small application-control CLI, a feature map, and recurring maintenance. The author reports 2,000 PRs per month and suggests much larger team-output multipliers, but does not provide a controlled comparison, independently audited PR dataset, or quality denominator in that post ([original pstack post](https://x.com/poteto/status/2094457600259842065)).

The public verification-skill example is explicitly fictionalized. It contains an app-local skill and a feature-map structure, but omits the referenced `control-atlas.mjs` CLI and driver scripts; it is not a ready-to-run verification platform or a benchmark result ([example repository](https://github.com/poteto/verification-skill-example)). No open-source license was established from the inspected repository, so this assessment recommends original templates rather than copying that material.

### Adopt the mechanisms, not the absolutes

| Article proposition | Assessment | Model-mesh implication |
|---|---|---|
| Validation capacity can limit delivery. | Useful hypothesis to measure, not a universal claim that coding is solved. DORA's 2025 survey reports positive throughput relationships alongside negative stability relationships, and its 2026 material warns about verification overhead and raw token metrics ([2025 DORA summary](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report), [2026 DORA insights](https://dora.dev/insights/)). | Measure accepted outcomes, queues, review effort, failure and rework, not generated code or PR volume alone. |
| Agents need runtime access and structured feedback. | Strong engineering recommendation. The pstack example describes feature-oriented inspection and evidence, while omitting the actual driver implementation ([example](https://github.com/poteto/verification-skill-example)). | Specify the driver contract, evidence schema, fixtures, and acceptance oracle; do not call a skill paragraph an implemented capability. |
| Only real dependencies make verification meaningful. | Too absolute. FoundationDB documents extensive deterministic simulation of network, machine, and failure behavior; useful evidence can come from simulation when its model and limits are explicit ([FoundationDB testing](https://apple.github.io/foundationdb/testing.html)). | Use a verification ladder: unit/property tests, contract tests, component fixtures, integration, then bounded system/load/fault checks where risk requires them. |
| Request routing provides isolated full-stack views. | Plausible for qualified paths, not complete isolation by itself. Signadot's own docs require separate data strategies and explicit queue-consumer cooperation ([FAQ](https://www.signadot.com/docs/concepts/faq), [Kafka isolation](https://www.signadot.com/docs/guides/set-up-message-queue-isolation/kafka)). | Verify database, cache, queue, background-job, callback, storage, and outbound side-effect boundaries, not just HTTP routing. |
| Repeating checks until green mathematically proves correctness. | Reject as stated. Formal specification/model checking is a different discipline with explicit system/environment models; ordinary runtime tests do not become formal proof by being automated ([AWS formal methods](https://cacm.acm.org/research/how-amazon-web-services-uses-formal-methods/)). | Use "observed under these checks and conditions." Preserve uncertainty and the pilot's bounded repair/final-freeze rules. |
| More autonomous output establishes more value. | Unsupported without outcomes and cost. METR's later experiment explicitly discusses selection effects, unreliable time accounting under concurrent agents, and limits on its current productivity estimate ([METR update](https://metr.org/blog/2026-02-24-uplift-update/)). | Keep all owner attention, setup, failure, and verification costs visible. Do not transfer another team's PR count into a forecast. |

The DORA evidence is observational, not proof that a particular tool causes improvement. METR's controlled task assignment answers a narrower question in its participant/task population and its 2026 update warns that selection and measurement issues impair interpretation ([DORA summary](https://cloud.google.com/blog/products/ai-machine-learning/announcing-the-2025-dora-report), [METR update](https://metr.org/blog/2026-02-24-uplift-update/)). These sources justify careful measurement, not a universal positive or negative verdict on agents.

## Architecture analysis

### Verification is a capacity and authority problem

Proposed architecture separates five responsibilities:

| Responsibility | Owner | Boundary |
|---|---|---|
| Task and acceptance contract | User-approved protocol and independent evaluator | Worker may not rewrite done criteria or the exact reference. |
| Execution | OpenCode, pi-agent, Qwen Code, Aider, or Goose adapter | Same harness within each comparison; no implicit authority from an agent's request. |
| Environment and tools | Trusted controller and isolated infrastructure | Only approved artifacts, destinations, data, privileges, and resource leases. |
| Evidence and adjudication | Independent test runner, protected records, two AI judges, owner disputes | Implementer output is evidence to inspect, not the final authority. |
| Promotion | Separately authorized release process | Passing a task is not permission to merge, deploy, publish, or use private data. |

A shared verification service must admit work only while capacity and reserved resources remain available. Queue time and environment startup count toward accepted-delivery time; generating more tasks cannot hide the bottleneck. Separate quotas for workers, test jobs, judges, and telemetry prevent an unbounded worker fan-out from consuming the resources needed to finish or safely stop.

This is a framework recommendation. It is not a claim that the current repository implements a scheduler, policy gateway, artifact store, or environment lease manager.

### Environment isolation requires a state inventory

The article's request-level routing pattern is useful when only changed services are duplicated and the unchanged baseline is genuinely shareable. Its own vendor documentation says shared databases use partitioned data by default and recommends stronger options for schema changes; Kafka consumers need separate groups plus message routing, or separate topics with the relevant producers configured appropriately ([Signadot FAQ](https://www.signadot.com/docs/concepts/faq), [Kafka guide](https://www.signadot.com/docs/guides/set-up-message-queue-isolation/kafka)).

Proposed environment manifest:

| State or boundary | Required declaration and negative check |
|---|---|
| Code and configuration | Candidate artifact digest, baseline digest, dependency versions, feature flags, and effective config. Reject a green result from another revision. |
| Synchronous calls | Trusted environment identity, allowed entry points, propagation and fallback behavior. Test a missing, forged, expired, and wrong-environment identity. |
| Database and schema | Per-case database/schema/tenant policy, fixture identity, permissions, migration and cleanup strategy. Test cross-case reads/writes and destructive schema changes. |
| Cache and object storage | Per-case namespace or separate instance/bucket, TTL, invalidation, and cleanup receipt. Test key collisions and stale values. |
| Queues and workers | Topic/group/consumer policy, message identity, duplicate/reorder/delay behavior, background jobs, and dead-letter handling. Verify no other case consumes or mutates the work. |
| External side effects | Local sinks or synthetic endpoints for email, payments, webhooks, and office actions. Deny production targets and uncontrolled callbacks. |
| Resource isolation | CPU, memory, storage, network, process count, concurrency, and quota reservations. Test cancellation and orphan cleanup. |
| Observability | Run-scoped logs/metrics/traces, trusted correlation, bounded retention, and verification that telemetry actually arrived. |

Kubernetes namespaces require additional authorization, network, and data-plane controls; a namespace alone is not a hard sandbox. The Kubernetes documentation also notes that NetworkPolicy objects depend on a supporting network implementation ([multi-tenancy guidance](https://kubernetes.io/docs/concepts/security/multi-tenancy/)). Worktrees are checkout management, not a substitute for these controls.

Do not introduce a shared-cluster routing layer as the default for this small pilot. A disposable local application stack may be simpler to qualify. A routing-based shared baseline is a later option only when the selected case needs it and state-isolation tests pass within the approved envelope.

### Programmable access is necessary; arbitrary access is not

The pstack source usefully emphasizes machine-readable responses, health/inspection commands, feature maps, and cleanup ([original post](https://x.com/poteto/status/2094457600259842065)). Model-mesh should adopt those contract ideas while restricting what agents can invoke.

Proposed driver operations are `describe`, `health`, `inspect`, `run_check`, `collect_evidence`, `cancel`, and `cleanup`, each bound to a known job and artifact. These are proposed semantic operations, not implemented commands. Mutation and provisioning must be separately authorized and performed through a trusted broker, not through a generic shell tool accepting arbitrary agent text.

MCP does not replace access control. Its security guidance requires audience validation, prohibits unsafe token passthrough, and rejects treating a session handle as authentication ([MCP security guidance](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)). Tool descriptions, web content, and returned logs remain untrusted data.

### Stronger testing is layered, not one giant end-to-end suite

Use the cheapest evidence that can falsify the claim, then add higher-fidelity checks for the risks left open. A mock can test a boundary assumption; a contract test can test that the assumption still matches a dependency; integration tests can exercise the actual interaction. No layer should claim coverage that belongs to another.

For concurrency and distributed-state changes, propose explicit invariants such as no duplicated committed effect, no acknowledged work lost after restart, no cross-case state access, and bounded completion or a declared terminal failure. Deterministic simulation and fault injection can make failures reproducible, but remain scoped to their modeled conditions ([FoundationDB testing](https://apple.github.io/foundationdb/testing.html)). Formal modeling may be warranted for a high-risk state machine, but is not required for every routine task and is not implemented here.

## Current framework, skill, and template gaps

The findings below concern the inspected source snapshot, not an allegation that a runtime exploit or false pass was observed. "Required" means required before claiming the proposed controlled evaluation is enforceable.

| Priority | Observed starting point | Recommended change | Acceptance evidence for a future implementation PR |
|---|---|---|---|
| Required | `evidence.md` requires claim, command, output, and conditional time context, while explicitly avoiding mandatory hashes for ordinary coding ([snapshot](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-method/references/evidence.md)). | Add a risk-scoped distributed/evaluation evidence profile requiring task/attempt/arm identity, artifact and environment digests, timestamps, tool versions, and completeness. Preserve the lightweight ordinary-work profile. | A stale revision's green output, missing environment ID, and truncated failure transcript cannot satisfy the gate. |
| Required | `mm-verify` asks the reviewer to rerun every claimed check and says judging changes nothing; it offers VERIFIED WITH CAVEATS ([snapshot](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-verify/SKILL.md)). | Require a safe execution target and declared side effects before reruns. Separate PASS, FAIL, BLOCKED, and INCONCLUSIVE; a missing mandatory check cannot become a passing caveat. | A test that writes to a real account is blocked; missing mandatory evidence cannot yield accepted status; safe disposable reruns remain possible. |
| Required | The generic method permits two review/fix rounds and three failed fix/verify cycles, and `mm-loop` sends findings back to execution ([method](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-method/SKILL.md), [loop](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-loop/SKILL.md)). | Add explicit execution-profile precedence. Evaluation-1's single repair, final freeze, no human rescue, and no grader-feedback leakage override generic development-loop defaults. | Adversarial fixtures cannot reopen an unused repair after final failure, add a second repair, or trigger hidden-grader-driven edits. |
| Required | The loop supports parallel evidence and attacker agents and mentions worktree isolation for overlapping files ([loop](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-loop/SKILL.md)). | Add bounded admission, environment leases, cancellation acknowledgements, late-result rejection, resource reservations, and per-case state isolation. | Cancel during a tool call; replay its completion; verify no later write or promotion and account for outstanding work. |
| Required | The domain template specifies prose workflow, evidence, authority, verification, frauds, and sources ([template](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-method/references/domains/TEMPLATE.md)). | Add linked verification-plan and environment/evidence schemas rather than forcing every field into a short domain paragraph. Include explicit unsupported checks and protected expected results. | An incomplete mandatory contract fails schema validation; an adapter cannot omit isolation or call a missing check optional after a failure. |
| Required | Current CI runs repository/configuration checks and landscape tests ([workflow](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/.github/workflows/checks.yml)). | Keep these checks and add separate conformance fixtures for new contracts/adapters in a future PR. Label documentation/configuration validation separately from executed system verification. | CI can distinguish a valid document, a passing adapter conformance test, and a completed qualified runtime experiment. |
| High | `mm-method` opens with a universal mid-tier-versus-stronger-model performance assertion ([snapshot](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-method/SKILL.md)). | Replace universal superiority language with an explicit, task-scoped hypothesis and evidence requirements. Synchronize mirrored instructions such as `AGENTS.md` when implementation is approved. | No unmeasured quality or cost guarantee remains in the framework's normative introduction. |
| High | The DevOps adapter already requires observed live state, blast radius, post-change health, and authorization ([snapshot](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-method/references/domains/devops.md)). | Extend it with leased disposable environments, state inventory, bounded load/soak plans, telemetry freshness, cleanup verification, and no production-side-effect defaults. | A clean HTTP check cannot hide a leaking queue, stale deployment, missing telemetry, or orphan environment. |
| High | The pstack example demonstrates a feature map but omits its driver implementation ([example](https://github.com/poteto/verification-skill-example)). | Create original project-local feature-map and driver-contract templates; do not copy an unlicensed fictional CLI or pretend it exists. | Every selected feature maps to a real entry point, fixture, observable state, independent oracle, and implemented command. |
| High | The existing evidence standard rejects screenshots without context and unobserved absence claims ([snapshot](https://raw.githubusercontent.com/bughunt8/model-mesh/273c83b1fefa095b5fdfb952d48ae8d60a28568a/skills/mm-method/references/evidence.md)). | Add positive observability controls and original-result receipts for dashboards/log queries; freeze design references outside worker write access. | Wrong time windows, missing log ingestion, changed references, and success text without state change fail verification. |

Additional coherence debt found in the local inspection should be recorded, not silently fixed in this research PR: `mm-verify` ends with an unfilled suite-mode heading, and `mm-loop`'s restricted report-artifact wording is narrower than the method's later gate artifacts. These need a focused follow-up specification and regression fixtures rather than another undocumented exception.

## Proposed reusable artifacts

These are schemas to implement in a separate approved PR, not files or tools that already exist.

| Proposed artifact | Required content | Owning role |
|---|---|---|
| Verification plan | Claim IDs; risk class; selected check layers; immutable test/reference IDs; required versus optional evidence; preconditions; expected failures; limits; terminal-status rules. | Protocol owner and independent verifier. |
| Feature map | Feature/subfeature; entry point; user-visible intent; fixture; success/cancel/error/empty/persistence paths; API/DOM/storage observations; known limitations. | Application owner, reviewed independently. |
| Environment manifest | Candidate/baseline digests; dependency topology; database/cache/queue/object-store isolation; secrets references; network policy; lease; quota; cleanup and rollback scope. | Trusted environment controller. |
| Evidence record | Run/case/attempt/arm/harness/environment IDs; artifact/test/policy digests; command/tool; timestamps; exit/status; original outputs; trace/query IDs; redactions; missingness; integrity receipt. | Independent runner/evidence store. |
| Tool capability manifest | Tool/server identity; pinned version and license; transport; allowed operations; recipients; read/write scope; credential reference; costs; output limits; cancellation behavior. | Tool-policy owner. |
| Load/soak plan | Target allowlist; workload model; duration; warm-up; business invariants; resource/latency/error thresholds; observability; abort/cooldown/cleanup; generator limits. | Performance-test owner. |
| Adjudication record | Frozen artifact; deterministic check results; both judge configurations and independent findings; dispute deadline; owner ruling; unresolved state; no repair feedback. | Final evaluator. |
| PR evidence summary | What changed; exact artifacts verified; passed/failed/blocked/inconclusive checks; scope not tested; budget/attention; approval boundary. | Integrating agent, checked by reviewer. |

For a browser-admin case, an original feature-map entry might require a synthetic record to change exactly once, survive reload, emit the expected audit event, and leave unrelated records untouched. For a data-reconciliation case, it might require row-level provenance, no hidden exclusions, and a known-answer reconciliation check. These are illustrative acceptance patterns, not selected pilot cases or approved templates.

### Evidence should be replayable without granting extra authority

An evidence record should contain enough information for an independent party to repeat a safe check, but replay must not mean unrestricted re-execution against whatever target is currently configured. Bind replay to an approved disposable environment, immutable inputs, redacted secrets references, and a declared side-effect policy.

No worker may replace expected outputs, verification scripts, reference templates, thresholds, or final-grade records. A legitimate correction to those assets requires a new approved version; after scored runs start, it must not retroactively rewrite outcomes.

### Maintain skills between experiments, not inside a frozen one

The pstack source recommends recurring maintenance of verification skills ([original post](https://x.com/poteto/status/2094457600259842065)). For model-mesh, skill maintenance should produce a reviewed revision, new conformance evidence, and an explicit effective date.

During an evaluation, freeze skills, prompts, tests, models, tool schemas, and references. Findings may inform a later protocol revision, but cannot silently improve one arm mid-run, leak holdout findings to later cases, or manufacture a new passing result.

## Open-source tools and MCP implications

Use the companion [open-source stack report](open-source-verification-stack.pplx.md) as the tool-level assessment. The main distinctions are architectural:

- **Playwright Test versus Playwright MCP.** The deterministic test engine should own frozen assertions; MCP helps an agent explore and interact. The MCP project explicitly states that it is not a security boundary ([Playwright MCP](https://github.com/microsoft/playwright-mcp)).
- **Browser Use direct tools versus delegated browser agents.** Its local MCP includes both low-level tools and a tool that delegates a task to another AI agent, so model calls, permissions, and repair accounting can change unless frozen ([local MCP guide](https://docs.browser-use.com/open-source/customize/integrations/mcp-server)).
- **Penpot versus Figma.** Penpot and its official MCP server have open-source licenses; Figma service access and an MCP endpoint are not equivalent to an open-source design backend ([Penpot](https://github.com/penpot/penpot), [Penpot MCP](https://github.com/penpot/penpot-mcp), [Figma terms](https://www.figma.com/legal/tos/)).
- **Monitoring versus acceptance.** Prometheus, Loki, Tempo, and Grafana can expose observations, but the acceptance rule must still name the target, query, time window, and invariant. Grafana MCP includes mutation capabilities that require explicit restriction ([Grafana MCP](https://github.com/grafana/mcp-grafana)).
- **Load generation versus an enforceable gate.** k6 checks alone do not change the exit status; thresholds are needed to make specified failures fail the test process ([k6 thresholds](https://grafana.com/docs/k6/latest/using-k6/thresholds/)).

Do not install the entire catalog to demonstrate seriousness. Tool selection follows the actual check, and every component consumes qualification effort, attack surface, retention obligations, and potentially money.

## Pilot effects and measurements

The existing decisions remain in force. Method scenarios are A01/A03/A05/A09; routing scenarios are A08/A11/A12. Each has two routine public/synthetic cases, with matched arms on each case, at most one repair, no human rescue, two final judges, and ordinary-failure continuation subject to safety/resource stops.

All five harnesses are now research targets. Whether all five enter the scored matrix remains a separate unresolved execution-design decision. A complete shared fourteen-case grid across five harnesses would entail 140 initial arm attempts before repeats, not 140 independent tasks. Do not assign a fresh budget to each harness.

Proposed additional diagnostic measurements:

| Diagnostic | Definition to freeze | Why it matters |
|---|---|---|
| Verification coverage | Required check IDs completed against the correct frozen artifact, with missing checks visible. | Stops a partial suite being reported as a full pass. |
| Time to actionable feedback | Dispatch-to-first reproducible result, separating queue, startup, execution, and telemetry delay. | Locates the bottleneck the articles describe. |
| Verification yield | Independently confirmed defects found per declared task/check opportunity, with false alarms and duplicates separated. | Avoids rewarding long reviews or large test counts. |
| Environment interference | Cross-case state access, misrouted events, shared-resource contention, and stale-baseline effects. | Tests whether parallel validation is actually isolated. |
| Evidence completeness | Required identity, command, output, timing, provenance, and integrity fields present. | Prevents unsupported trust in dashboard summaries or final prose. |
| Soak completion and drift | Actual completed duration and declared resource/latency/error/state trends. | Prevents a short run being described as long-duration reliability. |
| Cleanup debt | Resources, credentials, processes, messages, or storage remaining after termination. | Includes operational cost and failure consequences. |

These are proposed diagnostics under the existing objective order, not new weighted objectives or approved numeric thresholds. They cannot compensate for a defect, attention regression, or other prohibited regression.

The fourteen-case routine floor is not evidence of broad reliability, and the global ten-hour/USD 100 envelope may be insufficient for five full harness grids plus qualification and meaningful soak tests. If the required work does not fit, return for an explicit scope decision. Do not shorten a required test and report it as complete.

## Prioritized change proposal

### Before any scored implementation

Define the common verification/evidence/environment contract and evaluation-profile precedence. Map all five harnesses to it, including their hidden retries, auxiliary models, configuration sources, terminal events, tool permissions, and cancellation behavior. Freeze actual cases and a resource plan; this report does not do that work by implication.

The first implementation PR should contain original schemas/templates and deterministic negative fixtures, not production deployment. Its fixtures should reject stale artifacts, changed references, missing mandatory evidence, cross-case access, late completion after cancellation, and attempts to reopen final failure.

### Before networked integration or soak claims

Qualify the selected open-source test tools and telemetry path in disposable environments. Validate the state inventory, identity propagation, side-effect sinks, bounded MCP access, failure-signalling behavior, cleanup, and safe shutdown. For shared distributed environments, prove the relevant asynchronous and storage boundaries before claiming per-change isolation.

### Before client-facing effectiveness claims

Run a separately authorized frozen experiment, report all assigned outcomes and missing evidence, and apply the settled no-compensation rule. Keep observations from public/synthetic routine cases distinct from confidential-client performance, production readiness, and universal benefit. A documentation SHIP verdict and green repository checks are prerequisites for a well-formed proposal, not evidence that the method works.

## Decisions still needed

The largest remaining decisions concern the scored harness population, exact versions/models, actual task manifest, permitted providers and tool endpoints, numeric task/resource limits, statistical evidence standard, and the desired scope of the open-source requirement across hosting and inference. They should be resolved before more implementation detail is mistaken for approval.

No changes to operational skills, templates, profiles, installers, CI behavior, infrastructure, or runtime tools were made by this assessment. Only the evaluation documentation and research reports are proposed through the existing PR.
