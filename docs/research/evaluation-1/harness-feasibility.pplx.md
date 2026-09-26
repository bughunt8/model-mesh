# Five-harness feasibility assessment for model-mesh

Research checked 26 September 2026, Hong Kong time. Documentation assessment only; no installation, adapter implementation, benchmark execution, model call, or spending authorization.

## Finding

Keep all five requested implementations in the feasibility assessment: OpenCode, pi-agent, Qwen Code, Aider, and Goose. Each has a documented noninteractive entry point, but that is only an integration starting point, not evidence that the pilot's repair, isolation, judging, or spending controls work. OpenCode exposes CLI/SDK interfaces, Pi provides RPC, Qwen Code exposes headless JSON streams, Aider supports one-message CLI execution, and Goose supports structured headless runs ([OpenCode CLI](https://opencode.ai/docs/cli/), [Pi RPC](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/rpc.md), [Qwen headless mode](https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/), [Aider scripting](https://aider.chat/docs/scripting.html), [Goose CLI](https://goose-docs.ai/docs/guides/goose-cli-commands/)).

The recommendation is a common external evaluation controller with thin, separately qualified adapters. Do not make every harness emulate oh-my-openagent's named agents, and do not treat a native permission dialog as the execution boundary. The controller, not a prompt inside an agent, should own attempts, final submission, the one permitted repair opportunity, evidence freezing, cancellation, and budget admission.

All five remain candidates. None has been runtime-qualified, and this report neither selects a winner nor silently expands the scored pilot to five full implementations.

## Identity and open-source scope

The name pi-agent is interpreted here as the Pi coding-agent CLI, not an arbitrary package with a similar name. The previously referenced `badlogic/pi-mono` URL currently resolves to the `earendil-works/pi` project; the exact installed package, executable, and release must still be confirmed before a run ([Pi repository](https://github.com/badlogic/pi-mono), [Pi site](https://pi.dev/)).

| Requested target | Project assessed and license | Scope qualification |
|---|---|---|
| OpenCode | OpenCode, MIT ([license](https://raw.githubusercontent.com/anomalyco/opencode/dev/LICENSE)). | OpenCode is the harness target. Whether oh-my-openagent is present, and its version and role in the treatment, must be declared rather than inherited silently. |
| pi-agent | Pi Agent Harness / coding-agent CLI, MIT ([repository](https://github.com/badlogic/pi-mono)). | Distinguish the coding CLI from agent-core, model API, and optional extension packages. |
| Qwen Code | QwenLM/qwen-code, Apache-2.0 ([repository](https://github.com/QwenLM/qwen-code)). | Selecting the harness does not select a Qwen model or its hosted authentication path. |
| Aider | Aider-AI/aider, Apache-2.0 ([repository](https://github.com/Aider-AI/aider)). | Assess the CLI first, not an assumed stable Python embedding API. |
| Goose | The former `block/goose` URL currently identifies `aaif-goose/goose`, Apache-2.0 ([repository](https://github.com/block/goose)). | Pin the actual project and release; do not rely on an old organization name or unversioned recipe. |

These are source-license observations, not clearance of every dependency, browser binary, plugin, provider, hosted service, or distribution obligation. Inspect a pinned dependency manifest and license inventory before qualification. The open-source tooling requirement does not itself settle model weights, inference providers, or whether all execution infrastructure must also be self-hosted.

## Native interfaces and evidence gaps

The following table describes documentation, not tested behavior. `n.a.` means not established in the reviewed material, not a claim that the product cannot provide it.

| Target | Documented automation and evidence | Important documented behavior | Adapter implication, proposed |
|---|---|---|---|
| OpenCode | `opencode run` supports raw JSON events; `export` emits session JSON and `stats` reports token/cost statistics. The SDK supports event subscription and `session.abort` ([CLI](https://opencode.ai/docs/cli/), [SDK](https://opencode.ai/docs/sdk/)). | JSON-schema output has a documented default of two validation retries. Most permissions default to allow; `--auto` approves requests not explicitly denied ([SDK](https://opencode.ai/docs/sdk/), [permissions](https://opencode.ai/docs/permissions/)). | Capture session and artifact identities. Account for schema retries as additional model work; do not let them create an extra post-submission repair. Prove cancellation beyond the SDK acknowledgement. |
| pi-agent | RPC uses JSONL stdin/stdout, request IDs, and streamed session events. `agent_end` is not the final settled boundary; `agent_settled` is the documented signal that automatic continuation has finished ([RPC](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/rpc.md)). | Extensions can run with the process's OS permissions and make nested model calls; continued work can follow a low-level run ending. The repository explicitly says there is no built-in permission system restricting filesystem, process, network, or credential access ([extensions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md), [repository](https://github.com/badlogic/pi-mono)). | Use an external security boundary and explicit extension inventory. Do not freeze a result on `agent_end`. Exact usage reconciliation and safe cancellation need pinned-version conformance evidence. |
| Qwen Code | `-p` supports `json` and `stream-json`; examples expose result/usage data. Settings document wall-time and tool-call limits ([headless](https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/), [settings](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/)). | Opt-in unattended retry can retry 429/529 indefinitely. Stream-JSON input is described as under construction and resets budget counters per user message; tool-result text can be truncated to previews. `--yolo` does not enable sandboxing ([headless](https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/)). | Enforce an outer, non-resetting attempt and pilot ledger. Reject hidden unlimited retries. Preserve evidence independently of truncated model-facing output. Qualify the actual transport before adopting bidirectional mode. |
| Aider | `--message` / `--message-file` process one instruction and exit. The Python API is explicitly unofficial and may change without backwards compatibility ([scripting](https://aider.chat/docs/scripting.html)). | Auto-lint defaults on and Aider can attempt fixes after failed tests; separate main, weak, and editor models are configurable. Auto-commits default on ([lint/test](https://aider.chat/docs/usage/lint-test.html), [options](https://aider.chat/docs/config/options.html)). | Prefer a CLI subprocess adapter, immutable filesystem snapshots, independent test output, and provider accounting. A stable structured event/usage contract is n.a. in the reviewed pages; this is a qualification gap, not a reason to fabricate one. |
| Goose | `goose run` supports JSON/stream-JSON, explicit provider/model, recipes, no-session operation, and a maximum-turn setting. Session JSON export includes history, metadata, and settings ([CLI](https://goose-docs.ai/docs/guides/goose-cli-commands/)). | Autonomous mode is the documented default. Headless operation cannot ask for approval. Configured tools and extension settings can expose writes; CLI cost display is an estimate, not a billing cap ([modes](https://goose-docs.ai/docs/guides/managing-tools/goose-permissions/), [headless](https://goose-docs.ai/docs/tutorials/headless-goose/), [configuration](https://goose-docs.ai/docs/guides/config-files/)). | Freeze the recipe, extensions, provider, and permissions. Convert unresolved approval requests into a declared blocked outcome, not human rescue or silent auto-approval. Cancellation and complete charge reconciliation remain unverified. |

## Candidate-specific qualification

### OpenCode

OpenCode already exposes useful control points, including explicit model selection, event streams, session export, and SDK abort. Those interfaces make a controller adapter plausible, but they do not demonstrate that spawned processes, remote tools, or already-issued model requests terminate when the session is aborted ([CLI](https://opencode.ai/docs/cli/), [SDK](https://opencode.ai/docs/sdk/)).

The main experimental risk is confusing OpenCode, oh-my-openagent, and model-mesh's method. Freeze the same underlying harness and extension inventory within each paired comparison. If the method arm adds both the model-mesh instructions and a new orchestration plugin, the intervention has two components and cannot be described as an instruction-only effect.

Qualification must expose schema-validation retries, compaction, subagent calls, fallbacks, and all effective configuration. Automatic permission approval is not an acceptable substitute for a fixed allowlist; the documented permission system permits both broad allow settings and more specific rules ([permissions](https://opencode.ai/docs/permissions/)).

### pi-agent

Pi has a direct process protocol, but completion semantics matter: accepted prompt, low-level run ending, and fully settled work are different events. The adapter must correlate request IDs and capture terminal outcomes only after the agreed settled boundary, or after its own explicit timeout/cancellation outcome ([RPC](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/rpc.md)).

Extensions are executable dependencies, not merely reusable prose. They can inspect context and credentials, add tools, change models, and initiate nested calls under the process's authority ([extensions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/extensions.md)). Proposed qualification should disable unapproved extensions and project resources, pin approved ones, and measure all nested work.

Pi's lack of a built-in security permission system is explicit in its repository, which recommends external container or sandbox options ([repository](https://github.com/badlogic/pi-mono)). Do not count extension-based confirmation UI as independent enforcement against the same process that executes the extension.

### Qwen Code

Qwen Code exposes detailed headless configuration, but a comprehensive configuration inventory is necessary. The settings document lists auxiliary model roles, fallbacks, telemetry options, tool discovery, and retry behavior; pinning only `--model` is insufficient to define a single-model experimental arm ([settings](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/)).

Its sandbox guide describes workspace and `~/.qwen` mounts in container mode, and the default macOS Seatbelt profile allows outbound network access. The same guide states that sandboxing reduces rather than eliminates risk ([sandbox guide](https://qwenlm.github.io/qwen-code-docs/en/users/features/sandbox/)). The proposed pilot must use a clean approved configuration and scoped credentials, not inherit the user's normal home directory.

There are two evidence traps to test. Session counters may reset per incoming message, and tool-result previews may omit the exact failure needed for independent adjudication ([headless](https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/)). The outer controller needs a cumulative ledger and original artifact capture outside worker write access.

### Aider

Aider's one-message CLI is a useful process boundary, but its automatic lint/test repair behavior must be separated from the pilot's formal repair opportunity. The documentation describes automatic linting and attempted fixes after failed test commands ([scripting](https://aider.chat/docs/scripting.html), [lint/test](https://aider.chat/docs/usage/lint-test.html)).

Proposed qualification should either disable automatic lint/test repair and have the controller provide the agreed feedback, or explicitly bound and account for native work inside the initial attempt before final submission. The choice must be the same for both arms where it is not the treatment. A native repair loop may not reopen a frozen result.

Main, weak, and editor model settings must all be declared; otherwise the nominal single-model arm may perform work using additional models ([options](https://aider.chat/docs/config/options.html)). Browser administration and cross-application office work remain integration questions. The reviewed Aider pages do not establish a qualified MCP/browser/office adapter; do not convert that gap into either assumed compatibility or an unsupported claim of impossibility.

### Goose

Goose supplies headless structured output and recipes, and its extension system supports local and remote tool connections. These are plausible inputs to an adapter contract, not approval of the recipe's contents or any remote extension ([CLI](https://goose-docs.ai/docs/guides/goose-cli-commands/), [configuration](https://goose-docs.ai/docs/guides/config-files/)).

Its documented autonomous default and inability to ask for clarification in headless mode make unattended permission behavior a specific conformance test. A failed or unavailable approval path must not turn into automatic permission under the pilot's no-human-rescue rule ([modes](https://goose-docs.ai/docs/guides/managing-tools/goose-permissions/), [headless](https://goose-docs.ai/docs/tutorials/headless-goose/)).

Use an explicit provider/model, extension list, recipe digest, turn limit, and external time/cash enforcement. A displayed estimated token cost is useful diagnostic evidence but not a complete invoice or proof that in-flight work fits the remaining allowance ([configuration](https://goose-docs.ai/docs/guides/config-files/)).

## Common adapter contract, proposed

These requirements are design recommendations for all five targets. They have not been implemented.

| Contract area | Required evidence before qualification |
|---|---|
| Identity | Executable/package version, immutable source or artifact digest, harness configuration, extension/tool inventory, model endpoint and role mapping. |
| Clean context | New attempt/session, isolated checkout and home/config state, no prior solutions, hidden answers, or other harness outcomes in worker context. |
| Attempt control | Separate initial work, optional single repair, final freeze, and final evaluation. Distinguish API retry, assertion polling, test rerun, and a new repair attempt. |
| Tool equivalence | Same task inputs and approved tool semantics within each pair. Record any unavoidable capability difference instead of claiming equivalence. |
| Evidence | Original commands, exit status, stdout/stderr, tool receipts, artifact hashes, start/end times, and explicit incomplete/truncated output markers. |
| Cancellation | Prove that the controller stops dispatch, local process trees, remote work where controllable, and stale result publication. Record outstanding charges and incomplete work. |
| Accounting | One non-resetting ledger for spent, committed, and reserved model/tool/compute charges, including auxiliary models, judges, setup, retention, and cleanup. |
| Security | Independent filesystem/process/network boundary, approved recipients, scoped credentials, untrusted-input handling, and no shared host socket or production account state. |
| Failure | Frozen failed outcomes remain visible; ordinary failures continue the declared sample, while safety and resource stops override continuation. |

Qualification cases should include a silent provider stream, duplicate/replayed completion, a late tool result after cancellation, a truncated tool error, a hidden auxiliary model call, a permission request in headless mode, and a configuration injected through a parent directory. Use public/synthetic fixtures and count this work inside the separately approved qualification budget.

## What assessing all five does to the experiment

The settled task floor remains fourteen distinct routine cases, allocated as eight method-stage cases and six routing-stage cases. A single fully covered implementation would require twenty-eight initial arm attempts before repeats, subject to qualification and the existing global limits.

If a later decision enrolls all five in that complete grid, the arithmetic becomes 140 initial arm attempts on the same fourteen task identities, before repairs, repeats, setup, or control tests. Two final judges per submitted final deliverable could then require 280 judge assessments if all 140 attempts submit one. This is a conditional workload calculation, not an authorized sample or a cost estimate.

Do not quietly give each harness USD 100 or ten hours. Do not rotate different harnesses through the baseline and treatment arms of one comparison. Cross-harness comparison requires its own declared interpretation, order controls, and treatment of shared setup effort; different wrappers and native tools may otherwise dominate the apparent result.

A written feasibility assessment can cover all five without installing them. Runtime enrollment, qualification order, exact versions, models, and a sample allocation that fits the shared envelope still require decisions. All five remain in scope for research even if one is later deferred from execution.

## Proposed decision sequence

- **Configuration audit.** Freeze exact releases, all model roles, native loops, extensions, and tool interfaces for each candidate. Do not infer an installed version from documentation checked today.
- **Common control qualification.** Require the same minimum attempt, cancellation, evidence, and isolation contract. Mark unsupported or unverified requirements explicitly.
- **Scenario fit.** Validate the actual public/synthetic cases and their tool needs. A coding CLI description does not establish browser or office-work compatibility.
- **Feasibility decision.** Compare total proposed work against the one shared time/cash envelope, including qualification and judging. Return for scope approval if it does not fit.
- **Scored execution.** Only after separate authorization, run the frozen comparisons and preserve all failures, missing evidence, and deviations.

No measured ranking of defect rate, attention, delivery time, price, or reliability exists from this assessment. Current evidence supports adapter questions and control requirements, not performance winners.
