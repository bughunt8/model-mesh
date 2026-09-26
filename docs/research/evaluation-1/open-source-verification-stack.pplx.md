# Open-source verification, validation, and soak-test stack

Research checked 26 September 2026, Hong Kong time. Proposed architecture and tool shortlist only; no tool installation, MCP connection, credentials, scans, load generation, or deployments are authorized.

## Recommendation

Use open-source test engines as the source of executable evidence, with a small, allowlisted MCP layer where interactive agent access is useful. MCP should expose capabilities such as inspecting a browser, retrieving a design reference, or querying a run's telemetry. It should not be the authority that decides a test passed, grants permission, or extends a budget.

The smallest candidate stack is a deterministic runner with Playwright Test where a browser is needed, structured application logs, OpenTelemetry collection where instrumentation is needed, and Prometheus-compatible metrics for long-running checks. Add local Playwright MCP for worker-side exploration, self-hosted Grafana/Loki and a read-only Grafana MCP connection when searchable telemetry justifies them, and k6 when a task actually needs load or soak validation. These are recommendations, not approved dependencies.

Penpot is the suitable open-source design candidate. Figma's documented service and MCP access do not meet the all-open-source criterion established for this shortlist; a community open-source bridge would not change the licensing of its Figma backend ([Penpot repository](https://github.com/penpot/penpot), [Penpot MCP](https://github.com/penpot/penpot-mcp), [Figma service terms](https://www.figma.com/legal/tos/), [Figma MCP guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server)).

## Eligibility rule

For the proposed verification stack, inspect the license and source availability of the engine, MCP server, required plugin, and backend separately. A free tier, public API, downloadable client, or open connector is not sufficient.

Use local/self-managed open-source components, not cloud-only features, in the default proposal. This does not silently change existing GitHub PR hosting or select open-weight inference models. If the owner intends the open-source requirement to include the entire hosting and inference supply chain, that further scope must be made explicit before execution.

License findings below apply to the observed core projects. A pinned release still needs a dependency/license inventory and a review of relevant redistribution or network-service obligations. No legal clearance of a deployment is implied.

## Tool and license assessment

`n.a.` in the MCP column means a native MCP interface was not established by the reviewed engine documentation. It does not mean a wrapper is required or that one does not exist elsewhere.

| Component | Open-source evidence | Verification role | MCP decision and qualification limit |
|---|---|---|---|
| Playwright Test / library | Apache-2.0 ([repository](https://github.com/microsoft/playwright)). | Browser assertions, isolated browser contexts, trace capture, network observations, and cross-browser testing are documented ([repository](https://github.com/microsoft/playwright)). | Use the test runner directly for frozen final checks. MCP is not needed to execute a deterministic suite. |
| Playwright MCP | Apache-2.0 ([repository](https://github.com/microsoft/playwright-mcp)). | Accessibility snapshots, browser interaction, screenshots, and console/network tools are exposed through MCP ([repository](https://github.com/microsoft/playwright-mcp)). | Useful for exploration and permitted repair feedback. The project explicitly says it is not a security boundary and exposes powerful code/browser operations; qualify tools and isolate the process. |
| Browser Use, local core and local MCP | MIT core; local stdio MCP is documented separately from the hosted service ([repository](https://github.com/browser-use/browser-use), [local MCP guide](https://docs.browser-use.com/open-source/customize/integrations/mcp-server)). | Low-level navigation, state, extraction, screenshots, and an optional agent-delegation tool ([local MCP guide](https://docs.browser-use.com/open-source/customize/integrations/mcp-server)). | Alternative to Playwright MCP for a declared workflow, not an automatic second browser layer. Disable or explicitly account for nested-agent delegation; hosted Browser Use is not the default OSS implementation. |
| Penpot | MPL-2.0; self-hosting and SVG/CSS/HTML/JSON-oriented design inspection are documented ([repository](https://github.com/penpot/penpot)). | Versioned design references, tokens, components, and inspectable layout evidence. | Optional only where a selected case has design/template assertions. A design file does not prove the implemented browser behavior. |
| Penpot official MCP | MPL-2.0; local Streamable HTTP/SSE and plugin communication are documented ([repository](https://github.com/penpot/penpot-mcp)). | Query and manipulate design information through the Penpot plugin. | High-privilege interface: the model can execute code in the plugin environment, and the plugin must remain open. Do not assume a read-only mode or headless operation has been proven. Prefer immutable exports for final grading. |
| OpenTelemetry Collector | Apache-2.0 ([license](https://raw.githubusercontent.com/open-telemetry/opentelemetry-collector/main/LICENSE)); receives, processes, and exports telemetry ([repository](https://github.com/open-telemetry/opentelemetry-collector)). | Common collection and redaction path for traces, metrics, and logs. | Native MCP n.a. Collector ingestion is not an agent tool. Query approved backends through bounded interfaces. |
| Prometheus | Apache-2.0; metric collection, rules, and alerts are documented ([repository](https://github.com/prometheus/prometheus)). | Resource use, error rates, queue depth, throughput, and latency metrics defined by the target application. | Native MCP n.a. Use its API or the Grafana MCP server's supported datasource queries; exact query permissions require qualification. |
| Grafana OSS | AGPL-3.0-only ([repository](https://github.com/grafana/grafana)). | Human-readable dashboards and data-source views for metrics, logs, and traces. | A dashboard is supporting evidence, not the immutable test verdict. Do not require enterprise/cloud-only capabilities in the OSS proposal. |
| Loki | AGPL-3.0-only; log storage and queries with a single-host deployment option are documented ([repository](https://github.com/grafana/loki)). | Query task-scoped application and controller logs. | Access through an approved query API or Grafana MCP. A log saying success is not proof of the expected business state. |
| Tempo | AGPL-3.0-only; distributed trace storage with local-disk support is documented ([repository](https://github.com/grafana/tempo)). | Optional dependency-path and asynchronous-operation evidence. | Query integration and exact MCP coverage are version-specific qualification items. Add only where traces answer a real verification question. |
| Grafana MCP | Apache-2.0; stdio and HTTP transports, datasource queries, and `--disable-write` are documented ([repository](https://github.com/grafana/mcp-grafana)). | Read-only access to qualified OSS dashboards, Prometheus/Loki queries, and alert inspection. | Restrict tools, datasources, time ranges, query cost, and credentials. Exclude paid-backend-only functions and confirm writes/raw queries remain unavailable. |
| k6 OSS | AGPL-3.0; local CLI/CI load generation and configurable metrics/thresholds are documented ([repository](https://github.com/grafana/k6)). | HTTP/gRPC/browser workload generation and bounded load/soak tests. | Native MCP n.a. Prefer a controller invoking a frozen script. A custom bounded MCP job interface is optional proposed work, not an existing verified server. |
| Locust | MIT; Python load scripts, headless operation, distributed execution, and exported results are documented ([repository](https://github.com/locustio/locust)). | Alternative where Python workload definitions fit the project better. | Native MCP n.a. Choose k6 or Locust for a test, not both by default. No measured performance comparison was conducted. |
| Toxiproxy | MIT; TCP fault injection and Prometheus metrics are documented ([repository](https://github.com/Shopify/toxiproxy)). | Controlled delay, connection disruption, bandwidth constraints, and reset scenarios. | Native MCP n.a. Use a predeclared fault schedule in disposable environments, not arbitrary agent-selected disruptions. |
| ZAP | Apache-2.0; open-source web vulnerability scanning and manual security testing are documented ([repository](https://github.com/zaproxy/zaproxy)). | Conditional web-security validation for an authorized target. | Native MCP n.a. Prefer a pinned CLI/API automation plan. Active scanning needs explicit target and intensity approval; it is not a default step for every case. |
| Podman | Apache-2.0; rootless OCI containers are documented ([repository](https://github.com/podman-container-tools/podman)). | Candidate local environment runner without requiring a privileged shared-host socket. | This is infrastructure, not an MCP prerequisite. Rootless operation still has the launching user's authority; compatibility and containment must be tested for each suite. |

The catalog is deliberately larger than the proposed initial installation. Optional components are not automatically charged, enabled, or counted as mandatory pilot work.

## Exclusions and non-equivalences

- **Figma.** The official MCP guide describes a Figma-hosted remote endpoint or the Figma desktop application, and the service terms grant restricted service access rather than an open-source software license ([MCP guide](https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server), [terms](https://www.figma.com/legal/tos/)). Exclude it from the all-OSS stack; use self-hosted Penpot or frozen open-format references.
- **Hosted Browser Use.** The local open-source MCP path and cloud service are different deployment choices ([local MCP guide](https://docs.browser-use.com/open-source/customize/integrations/mcp-server)). Qualify the local path and chosen model connection; do not substitute a hosted API under the same product name.
- **Grafana Cloud and enterprise-only functions.** Grafana MCP can target both self-managed Grafana and cloud features ([MCP repository](https://github.com/grafana/mcp-grafana)). Only functions backed by the selected open-source deployment belong in the proposed stack.
- **Signadot as an assumed OSS dependency.** Its documentation describes a Signadot-hosted control plane coordinating customer-cluster workloads, but the reviewed FAQ does not establish an end-to-end open-source distribution ([FAQ](https://www.signadot.com/docs/concepts/faq)). Treat its architecture as a research input, not an eligible default dependency.
- **The pstack example as reusable licensed code.** The example repository is public and fictionalized, with its CLI omitted, and no license was established from the repository inspection ([example](https://github.com/poteto/verification-skill-example)). Do not copy it as an approved open-source implementation; author original templates from the general concepts.

## Browser and design validation

Proposed separation:

1. Worker-side browser tools explore the isolated application and collect visible repair feedback.
2. Frozen Playwright Test checks independently verify acceptance against the final artifact.
3. The two independent AI judges assess remaining rubric criteria and evidence; owner disputes follow the agreed eight-minute window.
4. Final tests, exact templates, and their expected outcomes remain outside worker write access.

Playwright assertions can poll until a condition is met, while test retries rerun failed tests and classify a retry-only success as flaky rather than an initial pass ([assertions](https://playwright.dev/docs/test-assertions), [retries](https://playwright.dev/docs/test-retries)). The protocol must distinguish assertion waiting, diagnostic test reruns, and the single allowed agent repair. None may silently convert a confirmed defect or time-limit breach into acceptance.

For exact visual/template checks, propose pinning reference digest, viewport, browser build, fonts, locale, timezone, fixture data, and explicitly permitted variable fields. Compare DOM and application state as well as pixels. Any visual comparison tolerance must be approved before runs and must not quietly permit the cosmetic defects the user has already rejected.

Penpot MCP can write and execute plugin code, so final reference retrieval should use a frozen export or independently enforced read-only access, not the same unrestricted tool used by the worker to edit a design ([Penpot MCP](https://github.com/penpot/penpot-mcp)). Do not let a failing agent redraw the reference to make itself pass.

Browser Use's local MCP includes `retry_with_browser_use_agent`, which delegates a complete task to another AI agent, and documents a setting that disables browser security ([local MCP guide](https://docs.browser-use.com/open-source/customize/integrations/mcp-server)). Proposed policy should deny unapproved delegation and security-disable settings, record every auxiliary model call, and prevent access to real user browser profiles.

## Logs, traces, and monitoring

Proposed correlation fields are `evaluation_id`, `case_id`, `attempt_id`, `arm`, `harness_id`, `environment_id`, `artifact_digest`, `trace_id`, and `policy_version`. Put high-cardinality task identifiers in controlled logs/traces; select bounded metric labels rather than multiplying every identifier into every metric series.

Keep raw evidence and the verdict outside worker write access. A Grafana panel or a model-written log summary should link back to the query, time window, target environment, and original result. Empty results need a positive observability control proving the right system was queried and the ingestion path was functioning.

OpenTelemetry baggage can propagate across services and onward to third parties, and has no built-in integrity check establishing that its values are trustworthy ([baggage documentation](https://opentelemetry.io/docs/concepts/signals/baggage/)). Consequently, a routing or trace label must not be treated as authorization. Use trusted admission, authenticated run identity, bounded propagation, and explicit redaction; no credentials or personal records in baggage.

Read-only Grafana MCP mode is a useful control, not the entire policy. Its documentation includes writable tools and authentication warnings for non-loopback HTTP binding ([MCP repository](https://github.com/grafana/mcp-grafana)). Proposed qualification must confirm backend credentials cannot mutate protected data, expensive queries are bounded, and a worker cannot modify dashboards, thresholds, or evidence used to grade its own output.

## Load, soak, and fault validation

k6 describes soak tests as extended average-load testing aimed at degradation, resource consumption, availability, and stability, commonly lasting hours or days ([soak guide](https://grafana.com/docs/k6/latest/testing-guides/test-types/soak-testing/)). The current ten-hour whole-pilot ceiling does not authorize a separate long soak for each case or each harness.

Use these labels accurately:

| Proposed test class | Question | Required predeclared evidence |
|---|---|---|
| Smoke | Does the verification path reach the intended revision and observe the expected state? | Positive and negative controls, run identity, basic assertions, cleanup receipt. |
| Bounded load | Does the system meet approved behavior and resource criteria under the named workload? | Arrival/concurrency model, duration, payload distribution, failure/latency metrics, business invariants, generator health. |
| Soak | Does behavior remain acceptable throughout a stated sustained window? | Full completed window, resource trends, leak/queue/backlog indicators, errors, state invariants, recovery and cleanup. |
| Fault/recovery | Does the system preserve required invariants under a named disruption? | Fault schedule, fault actually injected, expected degraded behavior, recovery condition, no cross-case damage. |

No test duration, traffic level, numeric threshold, or extra pilot budget is approved by this report. A curtailed soak is not a full-duration pass. If a required qualification test cannot complete, record blocked or incomplete qualification; scored attempts that hit their task limits still follow the pilot's existing failure rules.

There is a concrete false-green trap: k6 checks alone do not change the exit status, while failed thresholds produce a nonzero exit status ([threshold documentation](https://grafana.com/docs/k6/latest/using-k6/thresholds/)). A proposed verification skill must assert its required checks through frozen thresholds or an independent result parser, and test the failure path.

Toxiproxy supplies transport faults, not proof of message ordering, business idempotency, or transactional correctness ([repository](https://github.com/Shopify/toxiproxy)). Add domain assertions for no duplicate effects, no lost accepted work, bounded recovery, and isolation. Use fault tests only on disposable authorized targets.

## MCP boundary, proposed

Expose a small job interface rather than generic shell access:

| Proposed capability | Allowed shape | Required restriction |
|---|---|---|
| Start verification job | Approved plan ID, immutable artifact digest, approved environment ID. | No arbitrary command, destination, image, or test modification supplied by the worker. |
| Read job result | Job ID and bounded output selector. | Read only; result tied to the same artifact and policy. |
| Query telemetry | Approved datasource/query template, case/run ID, bounded time window. | No raw unrestricted SQL, writes, or cross-case access. |
| Inspect browser/design | Disposable browser context or immutable reference. | No personal profiles, reference mutation, cloud fallback, or arbitrary outbound target. |
| Cancel job | Owned job ID. | Stops execution and records unfinished work; cannot rewrite prior evidence. |

These capability names are proposed contract concepts, not claims of existing MCP tools. Use native APIs or CLI wrappers where they are simpler and safer. A wrapper itself needs an open-source license, tests, and security qualification before inclusion.

MCP's security guidance rejects token passthrough, requires audience validation, and warns that session handles are not authentication ([security guidance](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)). Bind every request to an authenticated principal and explicit job scope. Prefer local stdio where appropriate; an HTTP endpoint still needs caller authentication, restricted binding, and an approved transport policy.

## Admission and measurement implications

Add verification-environment startup time, queue wait, active test time, telemetry delay, cleanup time, and retained-resource cost to the proposed measurement dictionary. These are diagnostics beneath the settled priority order, not new objectives that may compensate for defects or attention regressions.

All new infrastructure, telemetry storage, browser runtime, model delegation, and cleanup charges belong in the existing USD 100 ceiling. Setup effort and recording effort still belong in owner attention. No claim is made that the full catalog, fourteen-case floor, five candidate harnesses, and meaningful soak coverage fit the current envelope.

For the first execution proposal, require only components justified by actual selected cases. A Penpot service is not mandatory for a pure data-reconciliation case, Tempo is not mandatory where traces add no information, and a load generator is not a substitute for ordinary correctness checks. Approve additions only after their purpose, operational cost, permissions, and evidence contract are named.
