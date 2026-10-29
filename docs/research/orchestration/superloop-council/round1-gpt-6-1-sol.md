# First-principle report: System One belongs in the controller, not above the evidence

28 October 2026. Round 1. This is an architecture proposal, not a measured improvement.

## Verdict

The hypothesis that Jev or another System One model has no place in Anthropic's six patterns is disproved for all six. But "Jev replaces the planner and loops endlessly until success" does not follow.

Here OMO means oh-my-openagent running inside OpenCode, with model-mesh configuration profiles. It is not a separate inference API. [Repository harness contract](https://github.com/bughunt8/model-mesh/blob/daf9ac42a9e86700a2f6c1c8b10353cd998a2a09/examples/orchestration/harnesses/opencode-omo.example.json)

The distinction is simple. Planning produces possible actions. A policy selects an action. Execution changes the world. Verification establishes what actually happened. These are different jobs.

A decision policy can be written as \(a_t=\pi(s_t,A_t)\), where \(A_t\) contains the actions permitted now. Selecting an action ID does not require generating prose. Generating a new plan, patch, tool argument or explanation often does. Jev is TypeSafe's System One model; its documented interface supplies Choice, Score and Noul answers to supplied questions, rather than generated text. [TypeSafe System One documentation](https://docs.typesafe.ai/concepts/system-one)

My recommendation is a bounded, evidence-driven controller with an optional System One decision service. Keep a generative planner. Keep independent reviewers. The controller, not Jev, owns authority.

## 1. Test the hypothesis against Anthropic's actual patterns

All thresholds below are proposed starting policies, not validated calibration claims. Choice decisions require both maximum option probability at least 0.85 and a gap of at least 0.15 over the runner-up. Otherwise, use a deterministic safe default or ask a person. Do not confuse TypeSafe's distribution-based `confidence` field with a measured probability of correctness. [Choice documentation](https://docs.typesafe.ai/primitives/choice)

| Pattern and Anthropic's wording | Exact proposed decision | Limit and verdict |
|---|---|---|
| Prompt chaining: "Prompt chaining decomposes a task into a sequence of steps". [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Noul `handoff_supported`: "Does this output satisfy every stated input requirement of the next stage?" Advance only with `noul >= 0.95` AND all deterministic prerequisites satisfied. Otherwise repair or clarify. | It cannot produce the next stage's content. Existing schema checks should remain ordinary code. **Disproved:** semantic handoff gates are a place. |
| Routing: "Routing classifies an input and directs it to a specialized followup task." [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Choice `route`: "Which eligible execution assignment should handle this task?" Options are live assignment IDs resolving to approved `b4b`, `hybrid`, `ultimate` or `global` configurations, plus `human`. Apply the Choice threshold above. | It cannot create workers, grant regional access or prove a profile is best. **Disproved:** this is directly a classification problem. |
| Parallelization: "LLMs can sometimes work simultaneously on a task". [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Choice `fanout`: "Which permitted execution arrangement fits this task?" Options `single`, `partition`, `vote`, `human`; same threshold. Host dependency checks and reserved budget must permit the arrangement. | It cannot write the independent subtasks or synthesize their findings. Never use the classifier to silently discard minority security findings. **Disproved:** fanout selection and aggregation triage are bounded decisions. |
| Orchestrator-workers: "a central LLM dynamically breaks down tasks". [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Choice `next_task`: "Which ready task should run next?" Options are currently ready task IDs, `request_plan`, `human`; same threshold. Dependency readiness is calculated in code. | It cannot dynamically invent the decomposition. A planner must supply task descriptions and acceptance criteria. **Disproved:** scheduling belongs here, but sole-planner replacement does not. |
| Evaluator-optimizer: "one LLM call generates a response while another provides evaluation and feedback in a loop." [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Score `readiness`: "How ready is this artifact for independent review?" Ordered criteria `unsupported`, `major_gaps`, `minor_gaps`, `ready_for_review`. Request review at `score >= 2.5` AND `P(level 3) >= 0.85`; never accept directly. | A number cannot supply corrective feedback or repair an artifact. Score is a weighted mean over ordinal levels, not "percent complete". **Disproved:** triage has a place. [Score documentation](https://docs.typesafe.ai/primitives/score) |
| Autonomous agents: "They are typically just LLMs using tools based on environmental feedback in a loop." [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Choice `next_action`: "Which permitted transition should happen next?" Options `plan`, `execute`, `verify`, `review`, `replan`, `pause`, `request_completion_audit`, `human`; same threshold. Host removes illegal transitions first. | It cannot generate arbitrary new tool calls or prove completion. **Disproved:** a bounded action policy can control a tool-using loop, with generative workers supplying novel content. |

The logical result is stronger than a performance claim. A place exists in every pattern. Whether replacing a particular rule or LLM decision improves outcomes remains an experiment.

## 2. What "superloop" actually contains

These are different continuation mechanisms, not six mutually exclusive products.

| Evidenced loop | Mapping to the six patterns | Typed decision versus generated work |
|---|---|---|
| Fresh-process Ralph loop. Huntley's basic implementation repeatedly supplies a prompt to an agent through a shell loop. [Ralph](https://ghuntley.com/ralph/) | Autonomous outer loop; can wrap chaining or evaluator-optimizer. | Continue, pause and request verification are bounded. Each fresh attempt still needs generated work and persistent evidence. |
| Feedback/refinement loop. [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Evaluator-optimizer, often chaining inside it. | Readiness and retry selection are typed. Critique and revision need text. |
| Persistent-session Goal loop, reinjecting an objective on `session.idle`. [OMO features](https://github.com/code-yeongyu/oh-my-openagent/blob/v5.1.48/docs/reference/features.md) | Autonomous loop containing routing and orchestrator-workers. | Active/paused/complete is bounded. Completion evidence and implementation are not supplied by that status. |
| Todo continuation, which checks unfinished todos, background activity and interruption state before reinjection. [OMO continuation implementation guide](https://github.com/code-yeongyu/oh-my-openagent/blob/bd1310b65df8d772bba604e958e79956dc3e89a2/packages/omo-opencode/src/hooks/todo-continuation-enforcer/AGENTS.md) | Chaining and orchestrator-workers under an autonomous outer loop. | Todo status is usually a code predicate, not a reason to buy inference. A semantic "blocked or merely unfinished?" decision can use System One. |
| Plan/Boulder continuation. Pinned documentation describes `/start-work` with Atlas; current general documentation describes `/ulw-execute` and persisted plan progress. [Pinned features](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/docs/reference/features.md), [current orchestration guide](https://github.com/code-yeongyu/oh-my-openagent/blob/bd1310b65df8d772bba604e958e79956dc3e89a2/docs/guide/orchestration.md) | Chaining, routing and orchestrator-workers. | Select/resume the next approved task with code or Choice. Writing or changing the plan needs a planner. |
| Dependency-graph waves, called `mass-ulw` in the current general guide. [OMO orchestration guide](https://github.com/code-yeongyu/oh-my-openagent/blob/bd1310b65df8d772bba604e958e79956dc3e89a2/docs/guide/orchestration.md) | Parallelization plus orchestrator-workers, with routing by category. | Ready-node selection is bounded. Decomposition and synthesis need text. This guide covers the Senpi edition, not an automatically available OpenCode API. |
| Model-mesh's bounded code/review/rework loop. [mm-loop](https://github.com/bughunt8/model-mesh/blob/daf9ac42a9e86700a2f6c1c8b10353cd998a2a09/skills/mm-loop/SKILL.md) | Evaluator-optimizer with parallel independent reviews. | Retry/escalate/stop can be typed. Patches, findings and owner decisions cannot. |

Version and edition matter. The current OpenCode-specific documentation retains Sisyphus, Hephaestus, Prometheus, Oracle, Metis, Momus and Atlas, while the general guide describes a main agent and curated `plan-consultant`/`plan-reviewer` roles. Do not treat those as interchangeable configuration schemas. [OpenCode edition reference](https://github.com/code-yeongyu/oh-my-openagent/blob/v5.1.48/docs/reference/opencode-config.md)

The released feature reference says legacy `ralph_loop` configuration migrates to `goal` and the `/ulw-loop` slash command has been removed. Do not dispatch old continuation commands without a version-specific adapter. [Released features](https://github.com/code-yeongyu/oh-my-openagent/blob/v5.1.48/docs/reference/features.md)

There is also a concrete stopping trap. Version 5.1.48 documents that `goal.default_max_iterations` is retained for migration but the Goal hook does not enforce the cap; the inspected hook reinjects while the goal remains active without a counter check. An outer watchdog is mandatory. [Released features](https://github.com/code-yeongyu/oh-my-openagent/blob/v5.1.48/docs/reference/features.md), [inspected runtime](https://github.com/code-yeongyu/oh-my-openagent/blob/bd1310b65df8d772bba604e958e79956dc3e89a2/packages/omo-opencode/src/hooks/goal/index.ts)

## 3. The architecture I would approve

```text
Owner-approved goal and limits
  -> deterministic policy and eligible-action builder
  -> optional System One selection
  -> deterministic transition validation and budget reservation
  -> generative planner or isolated OMO worker batch
  -> deterministic checks and independent external review
  -> evidence ledger
  -> repeat, succeed, pause or stop
```

Call System One the "core decision policy" if desired. Calling it the whole orchestrator hides the planner, scheduler, permission checks and verifier that make the system work.

Profiles are configuration bundles, not workers. The existing matrix already binds complete author, orchestrator and reviewer arrangements, and requires reviewer independence across harness and model family. Select a validated assignment, not merely a profile label. [Orchestration rules](https://github.com/bughunt8/model-mesh/blob/daf9ac42a9e86700a2f6c1c8b10353cd998a2a09/docs/ORCHESTRATION.md)

### Independence must survive profile switching

A01 demonstrates the problem. Its ultimate OMO assignment includes DeepSeek authors, while its hybrid OMO assignment uses DeepSeek for external review. Each assignment can be valid alone; switching between them can make a reviewer review its own family's earlier work. [Matrix](https://github.com/bughunt8/model-mesh/blob/daf9ac42a9e86700a2f6c1c8b10353cd998a2a09/docs/research/orchestration/MATRIX.md)

Maintain a cumulative provenance ledger for the artifact lineage. Filter every prospective reviewer, fallback model and orchestrator against all actual author families and harnesses, not just the latest cycle. Reserve independent review capacity before spending on authors. If no valid arrangement remains, pause. Treat unknown decision-model lineage as an unresolved independence requirement, not a conveniently new family.

### Reject "endless"

Completion needs a finite contract: required artifacts, verification commands, expected results, review gates and owner approvals. "Worker says done", all todos checked and a high Noul are insufficient.

With independent per-attempt false acceptance probability \(\epsilon>0\), the probability of at least one false acceptance over \(n\) opportunities is \(1-(1-\epsilon)^n\). That is an illustrative assumption, not a Jev measurement. Endless retries can amplify error as readily as progress.

Proposed defaults are six outer cycles, 30 minutes, two unchanged-evidence cycles and two retries of the same failure fingerprint. An owner-approved currency budget is required. Stop as `succeeded`, `budget_exhausted`, `blocked`, `policy_denied`, `cancelled` or `service_unavailable`; exhaustion never means success.

Success requires every acceptance check to pass on the final artifact hash, independent gates to pass, no unresolved blockers, and required human approval. Any subsequent edit invalidates prior acceptance receipts.

### The most important failure is missing evidence

The September case study reports an initial credential-exposure finding downgraded after the structured evidence field was empty; an evidence-salvage change later restored the correct severity. It also reports only one initial run per condition on one target, with coverage of 10/13 without the layer and 9/13 with it. This supports investigating evidence contracts, not claiming established speed or accuracy gains. [Jev/Laya case study](https://arxiv.org/html/2609.28940v1)

Send relevant evidence content, not just hashes or a worker's summary. Mark omitted, truncated or missing evidence as `unknown`. Preserve rejected findings for independent appeal. A classifier must not silently erase possible security defects.

Treat repository text, tool output and proposed plans as untrusted model inputs. JSON serialization does not remove semantic manipulation. The study explicitly identifies false negatives and adversarial-state manipulation as risks. [Case-study limitations](https://arxiv.org/html/2609.28940v1)

Pin the decision version and question revision. TypeSafe documents that aliases can move and change answers without application changes. Recalibrate on held-out local tasks after any model, prompt, state-packing or candidate-menu change. [Model documentation](https://docs.typesafe.ai/models)

For Hong Kong use, Jev's reachability, policy eligibility and contractual approval remain admission checks. Do not infer them from API accessibility. TypeSafe says its services are US-hosted and that no-training does not imply no retention; retention depends on agreements, data and any agreed ZDR arrangement. Send minimal redacted evidence and obtain approval for cross-border processing. [Privacy policy](https://typesafe.ai/legal/privacy-policy), [data handling explanation](https://help.typesafe.ai/articles/5974925716-how-is-submitted-data-used-or-retained)

OMO's Sustainable Use License restricts use and redistribution; it is the owner's explicit exception, not evidence that OMO meets the general open-source rule. Keep the driver and verification stack openly licensed and preserve the separate licensing gate for client deployments. [OMO license](https://github.com/code-yeongyu/oh-my-openagent/blob/v5.1.48/LICENSE.md), [repository exception](https://github.com/bughunt8/model-mesh/blob/daf9ac42a9e86700a2f6c1c8b10353cd998a2a09/docs/ORCHESTRATION.md)

## CDMs and constrained decoding

Separate a decoding mechanism from a product name. Chavan's paper evaluates grammar-constrained generation using Outlines and XGrammar, not ScaleDown's product or System One models. Across five small models, 14 tasks and 210 evaluations, constrained decoding eliminated observed schema failures but not all instruction-semantic failures. One output scored 1.000 on the paper's function-call metric while its email body was "1. 2. 3. 4. 5." Even the semantic metric missed the point. [Constrained-decoding paper](https://arxiv.org/html/2609.23742)

This changes the fallback design. Grammar-valid `{"action":"deploy"}` can still be the wrong action. Encode expressible invariants in schemas, then verify permissions, evidence and postconditions separately. Do not accept generated confidence numbers as calibrated probabilities. The paper does not evaluate calibration or agent outcomes. [Paper](https://arxiv.org/html/2609.23742)

ScaleDown's product adds a different capability set. LangChain describes Classify, span Extract, abstractive Summarize and query-aware Compress, advertising up to 1M input tokens. Its speed and cost comparisons are vendor-reported, not measurements of this proposed loop. [LangChain integration](https://www.langchain.com/blog/building-long-running-agents-with-scaledown-and-deep-agents)

The six-pattern placement is direct:

- Chaining: extract source-backed handoff fields.
- Routing: classify the next eligible assignment.
- Parallelization: collect spans from separate workers and classify whether another specialist is needed.
- Orchestrator-workers: assemble task evidence and select a ready task, without inventing decomposition.
- Evaluator-optimizer: extract checkable defects and triage readiness, without replacing critique.
- Autonomous agents: maintain bounded context and classify looping or drift.

These are proposed placements, not demonstrated OMO results. LangChain supplies an actual drift-breaker example: after each model call, stop when the top label is not `progressing` and its score exceeds 0.8. I would map that to `paused_for_review`, never `succeeded`. [LangChain drift example](https://www.langchain.com/blog/building-long-running-agents-with-scaledown-and-deep-agents)

The architectural addition is a state builder before the decision model. Prefer source-linked extraction over rewriting for consequential decisions. Extract supplies offsets and source-derived context, but the documentation inconsistently calls offsets characters and byte positions. Test Unicode and verify every selected span against the immutable original bytes before admitting it. A matching span proves presence, not relevance or completeness. [Extract contract](https://docs.scaledown.ai/api-reference/extract)

Summarize writes text, and Compress returns transformed context without documented source offsets. That puts another model between reality and the decision. A 1M-token input allowance does not prove preservation of a single negation or blocker. Keep owner policy, budget state, failed checks and unresolved dissent outside compression. Preserve originals and record transformation provenance; two decision vendors reading the same defective summary do not provide independent evidence. [LangChain model descriptions](https://www.langchain.com/blog/building-long-running-agents-with-scaledown-and-deep-agents), [Compress contract](https://docs.scaledown.ai/api-reference/compress)

There is also a concrete compatibility trap. ScaleDown documents a Jev-compatible Decisions shape, but defines Choice `confidence` as the selected option's probability; Jev defines a distribution-based confidence. Its Decisions endpoint produces no free-form reason, unlike its separate classification route. Normalize raw distributions, not similarly named fields, and pin the exact endpoint and model. [ScaleDown Decisions](https://docs.scaledown.ai/api-reference/decisions), [Jev Choice](https://docs.typesafe.ai/primitives/choice)

ScaleDown advertises zero retention and self-hosting, but the fetched homepage supplies neither processing-region facts nor contractual scope for those claims. Hong Kong eligibility, route-specific retention and licensing remain unresolved admission checks, not reasons to assume no retention. [ScaleDown homepage](https://scaledown.ai/)

Add a `scaledown` shadow backend and optional span-based state builder to the PR. Leave rewriting/compression disabled by default. Test lost negations, omitted blockers, offset mismatches and superficially perfect JSON with wrong actions. This is the first-principle lesson: a narrower output language limits what a model can say, not what it can misunderstand.

## 4. Recommended PR

Title: `Add a bounded System One control plane with replayable OMO execution`.

### Files and responsibilities

- Expand `docs/research/orchestration/SYSTEM-ONE.md` from its existing router/triage pilot into an executable decision contract. The note already calls absence an omission, not a finding against decision models; preserve that distinction and its shadow-first requirement. [Current note](https://github.com/bughunt8/model-mesh/blob/daf9ac42a9e86700a2f6c1c8b10353cd998a2a09/docs/research/orchestration/SYSTEM-ONE.md)
- Update `docs/ORCHESTRATION.md`, `docs/REVIEW-PANEL.md`, `skills/mm-method/SKILL.md`, `skills/mm-loop/SKILL.md` and `skills/mm-verify/SKILL.md` with the lifecycle, evidence contract, cumulative independence and terminal outcomes.
- Add `docs/SUPERLOOP.md`, `schemas/superloop.schema.json`, `schemas/decision.schema.json`, `templates/superloop-goal.json` and `examples/superloop/hybrid-A01.json`.
- Add `scripts/mm-superloop.py`, `scripts/mm-decision.py`, `tests/test_superloop.py` and `tests/fixtures/superloop/`.
- Extend `scripts/materialize.py` with an assignment input and pruning of forbidden model chains. Today it wraps a profile in `[opencode]`; it does not resolve matrix assignments or enforce cumulative independence. [Materializer](https://github.com/bughunt8/model-mesh/blob/daf9ac42a9e86700a2f6c1c8b10353cd998a2a09/scripts/materialize.py)
- Preserve O1-O18 and add runtime-policy tests, rather than weakening the existing validator to admit a non-generative model into generative seats. [Validator](https://github.com/bughunt8/model-mesh/blob/daf9ac42a9e86700a2f6c1c8b10353cd998a2a09/scripts/validate-orchestration.py)

### Interfaces and execution

Proposed commands:

```text
python3 scripts/mm-superloop.py --config run.json --mode shadow
python3 scripts/mm-superloop.py --resume RUN_ID --mode route
python3 scripts/mm-decision.py --backend replay --request request.json --out answer.json
python3 scripts/materialize.py hybrid --assignment assignment.json --out PATH/omo.jsonc
```

`run.json` contains the immutable goal, situation A01-A12, allowed profile set, acceptance checks, version locks, permissions, reviewer bindings, currency/token/time limits and maximum cycles. Default to hybrid only. Ultimate and global require explicit admission; a router cannot bypass Hong Kong or policy restrictions.

Each batch gets an isolated worktree and private configuration home. Write the pruned assignment into `.omo/omo.jsonc` under `[opencode]`, plus the OpenCode configuration. Never rewrite the user's shared profile file.

Invoke the installed, pinned OpenCode executable with an argument array:

```text
opencode run --dir WORKTREE --agent sisyphus --format json PROMPT
```

Those are documented non-interactive flags; JSON output is an event stream, not an acceptance receipt. OpenCode merges configuration sources, so `OPENCODE_CONFIG` alone is not isolation. Validate the effective configuration and deny-by-default permissions before launch. [CLI](https://opencode.ai/docs/cli/), [configuration precedence](https://opencode.ai/docs/config/)

Do not invent `omo --profile`. The adapter materializes profiles. Disable competing automatic continuation and unapproved fallback mechanisms, run one bounded batch, then return control to the driver. Use a process-group watchdog covering child sessions and servers. Unexpected permission prompts become `blocked`, never automatic approval.

### State and exact decision contract

Request shape follows TypeSafe's `state`, `model`, `questions` interface. [Primitive documentation](https://docs.typesafe.ai/primitives/noul)

State includes `run_id`, `epoch`, immutable goal/hash, acceptance criteria, artifact hashes and relevant redacted excerpts, host-observed check results, blockers, task dependencies, cumulative model/harness provenance, eligible assignments, remaining reserved budget, recent failure fingerprints, and evidence-coverage flags. Workers cannot edit controller state or approval receipts.

Use the six exact questions and criteria in section 1 only at applicable phases. Add:

- Noul `irreversible_effect`: "Would this action cause an irreversible effect not explicitly approved for this run?"
- Noul `sensitive_release`: "Would this action disclose sensitive data to an unapproved recipient?"
- Noul `authority_expansion`: "Would this action require permissions or financial commitments outside the approved scope?" Pause if any safety Noul is at least 0.20. Deterministic policy requires approval regardless of these answers.
- Choice `progress`: "What does the new evidence establish?" Criteria `advanced` = new independently supported acceptance progress; `stalled` = no supported progress; `regressed` = a prior verified property failed; `unknown` = insufficient evidence. Apply the standard Choice threshold; uncertainty cannot reset the stagnation counter.

The normalized answer contains probabilities, selected IDs, model version, question hash, state hash and epoch. Reject unknown IDs, stale epochs, nonfinite values, invalid probability sums and truncated required evidence. The model never returns executable commands.

Output is an append-only JSONL event log and final JSON receipt containing terminal status, artifact/check/review hashes, actual model IDs, cost reservations and usage, decisions, overrides, failures and approval IDs. Keep sensitive payloads separately with access controls.

### Budgets, fallbacks and proof before activation

Distinguish the profile's model-price ceiling from the run's total spending limit. Reserve worst-case worker, fallback, decision and review costs before dispatch. If token/turn limits and metering cannot bound in-flight requests, do not advertise a hard currency cap; refuse hard-cap live mode.

Backends are `rules`, `replay`, `typesafe`, `laya`, `scaledown` and `llm-json`. Rules are the default fallback for scheduling; ambiguous or consequential decisions pause. A constrained LLM is wire-compatible, not equivalent in calibration or independence. Disable its probability gates unless a separately validated scorer supplies them.

Laya is an open-weight candidate, not a drop-in safety guarantee. Its own documentation warns about uncalibrated checkpoints, near-chance zero-shot typed decisions and confident mistakes on negated requests. Validate the exact checkpoint, wording and state budget before admission. [Laya documentation](https://github.com/NandhaKishorM/laya/blob/main/README.md)

Offline CI must disable network and use fake executables plus recorded decision fixtures. Test malformed answers, outages, hangs, hostile state, false completion, omitted evidence, resumed budgets, duplicate dispatch, concurrent reservations, configuration contamination, profile-switch independence and edits after verification. Replaying the same log must produce the same host transitions.

Then compare rules against shadow System One on the same task set. Measure verified task success, false completion, suppressed valid findings, human interventions, total cost and wall time. No claimed savings before that comparison.

Out of scope: new model rankings, automatic merges/deployments, unlimited retries, autonomous permission changes, replacing external reviewers, training a new decision model, and migrating OMO editions in the same PR.

## 5. Owner decisions still required

1. Which OMO/OpenCode release and edition becomes the supported executable target?
2. Which irreversible actions always require approval, and what exact acceptance evidence defines success?
3. What are the run-level budget, review reserve and permitted profile escalations?
4. Is US-hosted processing of redacted project evidence acceptable, under which agreement?
5. What provenance establishes the decision backend's family independence?
6. What measured false-completion and false-negative rates would justify moving beyond shadow mode?

My vote is yes to a small, bounded control-plane PR. No to an endless model-led loop. The central problem is not choosing a cleverer next action. It is making sure that action is permitted, affordable, independently checked and based on evidence the decision model actually received.
