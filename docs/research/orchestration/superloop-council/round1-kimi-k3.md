# Round 1: The Researcher

## Finding

The hypothesis is false as an architectural claim. Anthropic explicitly permits routing by "a more traditional classification model/algorithm" and intermediate "programmatic checks". A System One model fits those jobs without replacing the generating LLM. That does not establish that Jev improves model-mesh, or that it can replace a planner. The article also carries a banner saying much of its tooling landscape has changed since December 2024, so I treat the six patterns as vocabulary, not a current product spec. [Anthropic](https://www.anthropic.com/research/building-effective-agents)

I recommend a bounded, shadow-mode decision controller, not an endless Jev orchestrator. The current repo already requires a shadow pilot and forbids System One from overriding validators, clearing cross-family blockers, or replacing independent review. Keep those restrictions. [Current System One policy](https://github.com/bughunt8/model-mesh/blob/orchestration/egm-lenses-and-gates/docs/research/orchestration/SYSTEM-ONE.md)

## Hypothesis test against the six patterns

The decisions and thresholds below are proposed interfaces, not measured operating points. Let `c` mean Jev's normalized Choice confidence and `p` a Noul yes-probability. They are different quantities. TypeSafe defines Choice confidence relative to the uniform distribution and warns that thresholds depend on the domain. [TypeSafe confidence documentation](https://docs.typesafe.ai/confidence.md)

| Pattern and article wording | Proposed System One decision | Limit and verdict |
|---|---|---|
| Prompt chaining: "You can add programmatic checks" on intermediate steps. [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Choice `chain_gate={advance,repair,human_review}` against a fixed checklist. Advance only at `c>=0.95` after deterministic checks pass. Otherwise repair or escalate. | Cannot write the outline, translation, or repair. Use ordinary code for mechanically checkable criteria. Hypothesis disproved. |
| Routing: "Routing classifies an input and directs it to a specialized followup task"; classification may use "a more traditional classification model/algorithm". [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Choice `situation={A01,...,A12,unknown}`. Route at `c>=0.90`; otherwise ask the planner or human. Profile eligibility remains a code check. | Cannot invent a route, certify model availability, or relax Hong Kong policy. This is the clearest counterexample. Hypothesis disproved. |
| Parallelization: outputs can be "aggregated programmatically" with "different vote thresholds to balance false positives and negatives". [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Noul `needs_another_independent_attempt`, `p>=0.70` requests another permitted attempt within budget. A typed model can also flag conflicting findings for review. | Cannot supply missing evidence or turn correlated votes into independence. Preserve deterministic aggregation and every blocker. Hypothesis disproved, although a rule may suffice. |
| Orchestrator-workers: "a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results". [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Choice `next={eligible_worker_id...,replan,human_review}` over a code-generated menu. Dispatch only at `c>=0.90`. | Cannot create the decomposition, worker instructions, or synthesis. It controls dispatch after a planner supplies tasks. Hypothesis partly disproved; replacement of the article's central LLM fails. |
| Evaluator-optimizer: one LLM generates while another provides "evaluation and feedback in a loop"; the evaluator decides "whether further searches are warranted". [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Choice `quality_gate={revise,verify_more,candidate_complete,human_review}`. `candidate_complete` requires `c>=0.99` and all evidence gates green. | Cannot write useful critique or fixes. A completion vote starts independent verification, never terminates successfully by itself. Hypothesis disproved for the bounded gate. |
| Autonomous agents: "LLMs using tools based on environmental feedback in a loop", with human checkpoints and "stopping conditions". [Anthropic](https://www.anthropic.com/research/building-effective-agents) | Choice `action_gate={allow_read,allow_reversible_write,confirm,deny}`. Allow a preauthorized low-risk action at `c>=0.99`; uncertainty means confirm. Code always requires human authorization for public, paid, destructive, or permission-changing actions. | Cannot generate a new tool program, grant authority, or override a stop. Hypothesis disproved for supervisory decisions, not for replacing the agent. |

Overall verdict: disproved. The useful question is whether a learned classifier beats rules or a constrained small LLM on these particular decisions. Presence in a diagram is not evidence of benefit.

## Superloop taxonomy

| Evidenced loop | Mapping to Anthropic patterns | Typed decision versus generated work |
|---|---|---|
| Huntley's original Ralph: `while :; do cat PROMPT.md \| claude-code; done`. [Geoffrey Huntley](https://ghuntley.com/ralph/) | Autonomous agent inside a repeated invocation; evaluator-optimizer only when feedback is actually supplied. | Stop, continue, or escalate is bounded. Code, revised prompts, and plans require generation. Repetition alone does not add evaluation. |
| Claude Code Ralph plugin intercepts Stop, feeds the same prompt back, and supports a completion promise and `--max-iterations`; the README lists the default as unlimited and recommends always setting a cap. [Plugin README](https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md) | Autonomous agent plus evaluator-optimizer when tests drive revisions. | Completion eligibility is typed. A self-written `<promise>` is a claim, not verification. |
| omo Goal persists an objective, reinjects continuation at `session.idle`, and expects a completion audit. `/ulw-loop` was removed as a slash command; `omo ulw-loop` remains a Codex passthrough. Goal defaults disabled, with a default continuation cap of 100. [omo feature reference](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/docs/reference/features.md) | Autonomous agent, evaluator-optimizer, and routing. | Continue, pause, replan, or request audit is typed. The agent still generates each next action. |
| omo todo continuation and boulder plan continuation resume unfinished work; `/stop-continuation` stops todo, Goal, and boulder continuation. [omo feature reference](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/docs/reference/features.md) | Prompt chaining and orchestrator-workers when checklist items delegate work. | Select a ready item, retry, or hand back. Plan production and implementation remain generated. |
| omo `mass ulw` coordinates an agent graph, while experimental Team Mode is off by default. [omo repository](https://github.com/code-yeongyu/oh-my-openagent) [Feature reference](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/docs/reference/features.md) | Parallelization, routing, orchestrator-workers. | Select approved workers and request additional review. Task decomposition and synthesis still need generation. |
| model-mesh PLAN, EXECUTE, VERIFY, AUDIT/REPORT, with a three-failed-cycle stop and no nesting inside GSD phases. [mm-loop](https://github.com/bughunt8/model-mesh/blob/orchestration/egm-lenses-and-gates/skills/mm-loop/SKILL.md) | Chaining around workers; routing at admission; parallel reviewers; evaluator-optimizer during repair; autonomous tools inside execution. | Stage transitions and escalation are bounded. Plans, fixes, and review arguments are generated artifacts. |

Do not put an outer endless loop around an inner endless loop. For a first implementation, let the outer driver own continuation and disable autonomous continuation inside each worker invocation. Otherwise Jev sees only the end of a potentially long internal run, not each consequential decision.

## What the evidence actually supports

I found no published, measured multi-agent result for System One. A promotional Jev guide on a site that says it is unaffiliated concedes the point, calling its multi-agent material "architecture, not result". [Made with Jev](https://madewithjev.com/jev-multi-agent)

The pentesting paper is a case study. Its initial comparison has one run per condition against one target: scenarios hit fell from 10/13 without System One to 9/13 with Jev, while wall time fell from 32m12s to 26m53s. The author says stochastic behavior could explain the difference, and the later re-test used a modified harness. [NeuroSploit paper](https://arxiv.org/html/2609.28940v1)

The paper also admits that false negatives may be "worse than running without the layer", because a finding the LLM would have reported can disappear. So Jev must not silently reject findings or prune required reviewers. [NeuroSploit paper](https://arxiv.org/html/2609.28940v1)

Independent benchmarks exist but test public classification sets, not loop control. System One Bench reports Jev 1.13 at index 79.0 with 6.1% calibration error; its operator is not named. A different third-party index ranks several open models above Jev 1.14, and rankings flip with the benchmark. [System One Bench](https://github.com/alilibx/system-one-bench/blob/main/README.md) [Jev alternatives listing](https://systemonemodels.org/guides/jev-alternatives/)

A newer reference audit gives the strongest warning on thresholds. A point-estimate gate broke its promised accuracy in 147 of 190 exchangeable evaluations; Learn then Test kept the promise in all 190. A gate calibrated in English kept a 95% promise in only 8 of 51 other locales. This is a preprint, not a model-mesh trial, but it kills the idea that `0.95` is a portable guarantee. [Confidence Is Not a Promise](https://arxiv.org/html/2610.36311v1)

So my thresholds are shadow-test starting points. Promotion needs held-out, traffic-matched labels, including Cantonese and Chinese, typos, conflicting evidence and incomplete states. Measure accepted-case error with a lower confidence bound, coverage, false-complete rate, missed blockers and cost per verified completion. Pin model and question versions, and requalify after either changes.

## CDMs and constrained decoding

Three different things share the name. Keep them apart.

1. **Grammar-constrained decoding** of an ordinary generating LLM (XGrammar, Outlines). The cited paper tests five models from 0.6B to 4B on 14 hand-designed tasks. Schema validity reached 100% under both tools, yet one small model still emitted only one of two required calls, which the schema allowed. A "hollow rescue" scored 1.000 on structure while the email body read "1. 2. 3. 4. 5.". The paper's own line: "Schema conformance is necessary but not sufficient for semantic correctness". It reports no significance tests, calibration or log-probability analysis, so it says nothing about thresholds. [Constrained-decoding paper](https://arxiv.org/html/2609.23742)
2. **Typed decision models** such as Jev: one forward pass, probabilities over a caller-supplied menu, no generated text. [System One definition](https://docs.typesafe.ai/concepts/system-one)
3. **ScaleDown's CDM product line**, launched 13 October 2026: Classify, Extract, Summarize, Compress. The first two point at things. The last two write. LangChain's own post keeps the agent model for planning and code. [LangChain integration](https://www.langchain.com/blog/building-long-running-agents-with-scaledown-and-deep-agents)

An ibl.ai post argues CDM is a product name for a known decoding-time technique, not a new architecture. ibl.ai sells a competing platform, so I weigh that as a skeptical take, not neutral evidence. [ibl.ai](https://ibl.ai/blog/constrained-decoding-models-not-a-new-architecture)

**Where CDMs fit the six patterns.** Classify occupies the same gates as Jev. Extract fits chaining (pull evidence fields before a gate), parallelization (fan out per document) and routing (extract the fields a router needs). Compress and Summarize fit orchestrator-workers and autonomous loops as context managers, shrinking history before the next turn. LangChain's drift example classifies `progressing/looping/drifting` after each model call and ends the run when a non-progress label scores above 0.8. In my design that is a `pause_and_review` signal. A run that stopped drifting has not finished anything. [LangChain integration](https://www.langchain.com/blog/building-long-running-agents-with-scaledown-and-deep-agents)

**What CDMs add beyond Jev.** Extract returns spans with confidence and character offsets, so a driver can check each value against the source text mechanically. Input is up to 1M tokens, against Jev's 32k state per question. Both ScaleDown facts are vendor statements, and the LangChain byline includes a Neal Patel, whom ibl.ai names as ScaleDown's co-founder and CEO, so I do not count that post as independent. [LangChain integration](https://www.langchain.com/blog/building-long-running-agents-with-scaledown-and-deep-agents) [ibl.ai](https://ibl.ai/blog/constrained-decoding-models-not-a-new-architecture) [Jev model limits](https://docs.typesafe.ai/models.md) One independent user test found every returned span verbatim in the source, 97.3% on 300 CLINC150 utterances, and that Extract was weaker on some fields. It was one engineer, small samples, and a small local model as baseline. [Ishank Choudhary's test](https://dev.to/ishank-dev/scaledown-cdms-fast-cheap-classify-extract-and-summarize-models-tested-1adp)

**What CDMs risk.**

- *A writer inside the decision path.* Summarize and Compress rewrite evidence, and a rewrite can drop the clause that forbids an action. Classify can return a free-form reason. LangChain's circuit-breaker example pastes `result['reasoning']` into the conversation as an `AIMessage`, so classifier-generated text re-enters the agent's context. I would disable it: `/v1/scaledown` does not expose reasoning, and `/classify` can set it off. [Decisions overview](https://docs.scaledown.ai/api-reference/decisions-overview.md) The audit above also finds confidence does not select faithful explanations. [Confidence Is Not a Promise](https://arxiv.org/html/2610.36311v1)
- *Poisoned inputs.* LangChain's Extract reads only user messages, never agent replies. Adopt that rule: extract from trusted-origin text only, keep policy and blockers outside compression, validate offsets, and never route an unverified summary into a success or authorization gate. A 369k-token test returned a summary that skipped one of two meeting series. [Ishank Choudhary's test](https://dev.to/ishank-dev/scaledown-cdms-fast-cheap-classify-extract-and-summarize-models-tested-1adp)
- *Vendor-only claims.* "200x faster" and "467x cheaper" have no stated baseline. The same tester measured 1.8x to 4.6x faster than a local 1.7B CPU model on classification and extraction, and about twice the list price of gpt-5-nano for short classification. The "77.2% on DecisionBench vs Jev's 72%" figure comes from the launch post; Jev Daily says nobody outside has run it, and the tester found no public source. [Jev Daily](https://jevdaily.com/issues/2026-10-14) [Ishank Choudhary's test](https://dev.to/ishank-dev/scaledown-cdms-fast-cheap-classify-extract-and-summarize-models-tested-1adp)
- *Not a Jev drop-in for structured state.* `/v1/scaledown` reads only `state.text` and `state.document`. System One Bench reports Classify-1 rejecting 3,050 of 3,250 cases for that reason, which is an adapter failure, not evidence of a weak classifier. Its choice answers also come from independent yes/no rubric judgments normalized by softmax, so Jev's calibration findings do not transfer. [Decisions overview](https://docs.scaledown.ai/api-reference/decisions-overview.md) [Classify overview](https://docs.scaledown.ai/api-reference/classify-overview.md) [System One Bench](https://github.com/alilibx/system-one-bench/blob/main/README.md)
- *Retention and region.* ScaleDown's public index claims zero retention, no training on customer data and a VPC option. I could not open the DPA itself. A third-party directory summarizing it says US-only inference and content-free logs for up to 90 days. That is a claim about a claim. [ScaleDown public index](https://scaledown.ai/llms.txt) [TrustedRouter](https://trustedrouter.com/providers/scaledown)

**How the schema-validity finding changes the design.** Layer the checks. First, syntax: constrained decoding or a typed API guarantees it. Second, meaning: allowed transitions, evidence hashes, fresh check results, and policy are verified by code that does not read model output. Third, authority: a human or independent reviewer. "Never makes a type error" is structural, not semantic, and it applies to Jev and Classify alike. For the fallback "LLM constrained to typed output", the paper validates only structure. Any threshold built on token probabilities would be unvalidated, so that fallback needs its own labelled calibration before it gates anything.

**Cross-vendor voting.** ScaleDown's endpoint is request-compatible with Jev, so a Jev plus Classify-1 vote is cheap to build. Agreement between two classifiers trained on overlapping public data is not independence. Measure their disagreement on local labels before treating a vote as stronger than one call. [ScaleDown decisions overview](https://docs.scaledown.ai/api-reference/decisions-overview.md)

## Assessing the proposed core

I would split the system into a deterministic controller, a typed adviser, a generative planner, configured omo workers, and independent verification. "System One at the core" can mean the adviser selects among executable transitions. It cannot mean Jev owns the plan: TypeSafe explicitly says System One does not generate replies, code, or explanations. [System One definition](https://docs.typesafe.ai/concepts/system-one)

Profiles are configurations, not autonomous workers. Freeze `ultimate`, `hybrid`, `b4b`, or `global` at admission, then select a complete validated situation option. Do not mix seats between options or switch profiles to bypass caps. Reviewer harness and family must differ from every author and the orchestrator across all fallback rungs; internal omo gates do not count as independent review. [Orchestration contract](https://github.com/bughunt8/model-mesh/blob/orchestration/egm-lenses-and-gates/docs/ORCHESTRATION.md)

Treat the decision model as an orchestration seat, because it picks the next transition. The rule says the orchestrator family shares nothing with authors or reviewers, and the validator derives family from the model ID prefix. [Orchestration contract](https://github.com/bughunt8/model-mesh/blob/orchestration/egm-lenses-and-gates/docs/ORCHESTRATION.md) Its prefix map has no Jev or ScaleDown entry, so those IDs resolve to "unknown". In the `ultimate` rows I read, authors and reviewers already use zai, deepseek, moonshot, alibaba and minimax; the only Hong Kong-eligible family left unused is xiaomi. A Qwen-based open-weight decider would collide with the alibaba reviewers, and I found no xiaomi typed decision model. (Sources: `scripts/validate-orchestration.py` and `docs/research/orchestration/MATRIX.md` in the local checkout.) My proposal is that a log-only shadow seat needs no family constraint. Once it can dispatch or gate, it inherits the orchestrator rule, with a provider, pinned version, base family and fallback chain recorded, and an undisclosed lineage counts as a failure, not a pass. Closed inference is not itself barred by D46; omo has an explicit licence exception, and client or commercial use needs a separate check.

Failure policy should be conservative:

- False rejection or false completion: retain findings, and require separate fresh completion evidence.
- Adversarial state: worker prose and fetched content are data, not instructions. Jev's own documentation says adversarial content can move answers; irrelevant context also hurts. Send a narrow, provenance-labelled state. [Jev jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13.md)
- Calibration drift: pin a version, never `jev-latest`, because the alias can change behavior. [Model version policy](https://docs.typesafe.ai/models.md)
- Outage: bounded retries for transient errors, then pause or use a separately qualified fallback. Jev documents 429 and 529 responses. Do not turn transport failure into approval. [API errors](https://docs.typesafe.ai/api/errors.md)
- Hong Kong and privacy: Jev's launch describes a West Coast US service; its DPA does not establish a fixed inference region or explicit request-retention period, and zero retention requires enterprise arrangements. `ultimate` remains unavailable for Jev until reach, policy, and data handling are approved. [Launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev) [DPA](https://typesafe.ai/legal/data-processing) [Legal documentation](https://docs.typesafe.ai/legal.md)

Fallback candidates are self-hosted open weights, a small LLM under XGrammar or Outlines, and plain rules. Laya is not an equivalent drop-in: System One Bench puts the stock Laya router at index 60.4 with 20.0% calibration error, and on one Apple M5 comparison Laya scored 0.510 accuracy against Jev's 0.755. That benchmark also lists Liquid AI's d1-3B at 78.4 with 2.4% calibration error but 1,134 ms median CPU latency. I did not check d1-3B's licence or whether it handles this task. [System One Bench](https://github.com/alilibx/system-one-bench/blob/main/README.md) No fallback inherits Jev's thresholds. My baseline is rules: red checks mean repair, missing evidence means verify, hard caps mean hand back.

## PR recommendation

Approve an experimental, offline-first PR. Do not add an adopted model to the production matrix yet.

### Files and contracts

- Update `docs/research/orchestration/SYSTEM-ONE.md`, `docs/ORCHESTRATION.md`, and `docs/REVIEW-PANEL.md` with advisory scope, state provenance, completion authority, and decision-seat independence.
- Add `docs/SUPERLOOP.md` and `skills/mm-superloop/SKILL.md`; make `mm-loop`, `mm-method`, and `mm-verify` cross-reference one continuation owner and the existing three-cycle bound.
- Add `examples/orchestration/decision/{controller.example.json,state.schema.json,questions.json,decision-log.schema.json}`. Include budget, region, data policy, pinned versions, fallback, and calibration-artifact fields. Generic templates contain placeholders; examples contain real IDs.
- Add `scripts/superloop.py`, `scripts/decision-client.py`, `scripts/omo-runner.py`, and `scripts/validate-superloop.py`. Extend orchestration validation to reject unknown decision families for consequential gates, missing budgets, invalid transitions, and reviewer overlap.
- Fix the omo adapter example first. It records a pinned schema v4.19.4, a note that newer omo docs rename agents, and no executed dry run. Then update `TESTING.md`, drift checks and CI. Leave the generated matrix unchanged until a decision seat is adopted. (Source: `examples/orchestration/harnesses/opencode-omo.example.json` in the local checkout.)

### Driver interface

Proposed command:

```text
python scripts/superloop.py --task TASK.json --profile hybrid \
  --situation A02 --option primary --worktree PATH \
  --policy controller.json --decision-backend replay --mode shadow
```

Inputs are immutable task/acceptance criteria, a validated complete seat assignment, allowlisted commands, and finite budgets. Outputs are `result.json`, append-only `events.jsonl`, raw worker streams, immutable evidence files, and a checkpoint. Exit codes distinguish verified completion, budget exhaustion, human gate, and infrastructure failure.

State contains task and plan hashes, ready task IDs, allowed next actions, changed-file hashes, fresh check results, unresolved findings, provenance/families, previous outcome, and remaining budgets. Never send credentials, whole transcripts by default, or worker assertions as authoritative check results. Optional compression preserves originals and cannot touch policy, blockers, or check records.

`questions.json` implements the table above plus Choice `progress={progressing,looping,drifting,unknown}`. At `c>=0.80`, looping or drifting requests pause. Any low-confidence dispatch goes to the planner or human. `candidate_complete` never bypasses independent review. Numeric scores may rank optional work, never erase required work.

### Non-interactive execution

Pin an omo edition and release first. Current documentation distinguishes Native from the OpenCode edition; a bare command name does not identify the same runtime. [omo repository](https://github.com/code-yeongyu/oh-my-openagent)

For the first PR, keep the OpenCode path the repo already documents and call it with an argv array, never a shell string:

```text
opencode run --dir WORKTREE --format json --agent AGENT \
  --model PROVIDER/MODEL "PROMPT"
```

These are documented flags. The page lists no exit codes, and `--auto` approves every permission not explicitly denied, so the repo's `ask` permissions would stall a headless run. Pre-set explicit allow and deny lists instead of using `--auto`. [OpenCode CLI](https://opencode.ai/docs/cli/) The omo-aware alternative is `bunx oh-my-openagent run`, which supports `--json`, `-m provider/model`, `-d directory` and `--session-id`, and exits only when the session is idle, todos are done and no continuation hook is active. It therefore absorbs omo's internal loops, which conflicts with letting the outer driver own continuation. [omo CLI reference](https://github.com/code-yeongyu/oh-my-openagent/blob/dfbeeec9/docs/reference/cli.md?plain=1) Do not invent a `--profile` flag. Materialize the profile into project configuration, then verify the effective config. omo now reads a unified `.omo/omo.jsonc`, and legacy files are imported once, not read at runtime, so confirm where `materialize.py` writes before trusting it. [omo feature reference](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/docs/reference/features.md)

Treat native `omo --print --mode json` as a separate later adapter. Public issues report successful exit codes with no work or a final provider error. Parse terminal events and fresh artifacts; process exit zero alone never proves success. [No-work issue](https://github.com/code-yeongyu/oh-my-openagent/issues/10592) [Provider-error issue](https://github.com/code-yeongyu/oh-my-openagent/issues/11014)

### Bounds, logs, and tests

Require explicit caps on total invocations, wall time, estimated/reserved spend, tokens, and child concurrency. Suggested pilot defaults are 10 invocations, 30 minutes, one writer, and a separately approved dollar cap. Preserve the existing three-failed-fix-cycle stop. Stop on two identical no-progress fingerprints, stale evidence, permission denial, or missing terminal output. The model cannot extend a cap.

Log state/question/config hashes, pinned model, raw probabilities, thresholds, selected action, deterministic vetoes, actual worker identity, timings, costs, evidence hashes, and stop reason. Reserve spend before dispatch; missing usage is not zero cost.

Offline tests use a fake executable, replay decisions, stub HTTP server, and network-denial guard. Cover false-complete, preserved blocker, injected state, option permutation, multilingual uncertainty, truncated output, exit-zero failure, timeout, 429/529 exhaustion, restart/idempotency, compression dropping a blocker, and ScaleDown's restricted state shape. Assert that all four profiles preserve policy and independence through fallback.

Out of scope: endless execution, model-written policy, automatic merge/push/deploy, real paid or destructive actions, training a custom decider, and replacing independent verification. No benefit claim until paired trials beat the rules baseline on verified completion without increasing missed blockers.

## What I could not verify

I did not test Hong Kong reachability of any API, open the ScaleDown DPA, check licences for d1-3B or Laya's base models, or run omo or OpenCode. No System One or CDM result in this report measures superloop control. Every number comes from public classification sets, a vendor, an academic preprint, or a single run.

## Questions for the owner

1. Target the pinned OpenCode edition first, or explicitly migrate to Native?
2. Which completion errors are tolerable, and what human-review cost justifies automation?
3. Who supplies labelled English and Chinese/Cantonese traffic and authorizes the data sent to vendors?
4. What finite dollar, invocation, and wall-time caps apply to each profile?
5. Does a decision seat inherit the orchestrator family rule once it can dispatch, given that only the xiaomi family is unused in `ultimate`?
6. Does the existing omo licence exception cover client or commercial superloop use, or does that need its own check?

My vote: approve the shadow controller and offline adapters. Reject the endless loop and reject Jev as the planner. Earn automatic dispatch with local evidence before granting it authority.
