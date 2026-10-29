# Round 1 report: The Practical (GLM 5.3)

Date: 2026-10-28. Repo state read: branch orchestration/egm-lenses-and-gates, commit daf9ac4. All vendor claims below are labeled as vendor claims. Nothing in this report was run against a live Jev or omo loop.

## Where I stand

The user's hypothesis is wrong, and so is half of the proposal built on top of it. The six Anthropic patterns each contain at least one bounded typed decision, and the article's own wording names them: gates, classification, checkpoints, stopping conditions. So a System One model has a place in all six. What it cannot be is the "core orchestrator" the article describes, because that seat writes plans and Jev cannot write anything. And "endless loop until the goal" fails on the evidence: every production loop I can find ships with a stop rule. The deliverable that survives is a shadow-mode pilot with one fork, one driver script, and hard stop rules in code. That is what I recommend, and it is deliberately smaller than what was asked for.

## 1. Hypothesis test, per pattern

Quotes are from the [Anthropic article](https://www.anthropic.com/research/building-effective-agents). Question types are from the [TypeSafe docs](https://docs.typesafe.ai/concepts/system-one): choice, score, noul (yes/no probability).

### Prompt chaining

The article: "You can add programmatic checks (see 'gate' in the diagram below) on any intermediate steps to ensure that the process is still on track."

A gate is exactly a typed decision. Question: noul `step_on_track`, "given this intermediate output and the step's acceptance criterion, is the step on track?" Threshold: below 0.5, retry or abort. What Jev cannot do here: write the next step's prompt. Verdict: hypothesis disproved for this pattern.

### Routing

The article: "Routing classifies an input and directs it to a specialized followup task," and routing works "where classification can be handled accurately, either by an LLM or a more traditional classification model/algorithm."

That sentence is the article itself inviting a non-generative classifier into the pattern. This is the strongest fit of all six. Question: choice `situation` over the twelve model-mesh situations A01 to A12, plus `unrouted`. The vendor says choices support "a cardinality up to 255" ([launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev)), so twelve options is trivial. What Jev cannot do: build the specialized followup prompts. Verdict: disproved, hardest of the six.

### Parallelization

The article: outputs "aggregated programmatically," with voting as "running the same task multiple times to get diverse outputs."

The aggregation the article describes is already deterministic code, and that should stay code. The fuzzy parts are: do two outputs agree (noul `outputs_agree`), and which output wins a vote (score). Verdict: partly disproved. Keep the merge in `aggregate-findings.py`, add a typed question only where agreement judgement is fuzzy.

### Orchestrator-workers

The article: "a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results."

Breakdown and synthesis are text generation. Jev cannot do them: System One models "do not write replies, produce code, or generate explanations of their reasoning" ([TypeSafe docs](https://docs.typesafe.ai/concepts/system-one)). Delegation, though, is a choice: `worker_for_task` over the worker menu that exists right now. Verdict: the hypothesis holds for the orchestrator seat itself, and is disproved for the routing decisions inside it. Partly disproved.

### Evaluator-optimizer

The article: "one LLM call generates a response while another provides evaluation and feedback in a loop," effective "when we have clear evaluation criteria."

The accept/reject decision is a typed question. The Jev multi-agent guide gives this exact answer space: "Is the research good enough: accept / verify_more / reject" ([TypeSafe guide](https://madewithjev.com/jev-multi-agent)). What needs text: the feedback the worker acts on. Verdict: partly disproved. The decision is typed; the coaching is not.

### Autonomous agents

The article: agents "gain 'ground truth' from the environment at each step," "pause for human feedback at checkpoints or when encountering blockers," and "it's also common to include stopping conditions (such as a maximum number of iterations) to maintain control."

Checkpoints, blocker pauses, and stopping conditions are noul and choice questions. This pattern is the superloop. Questions: noul `goal_complete`, choice `next_action` over `continue`, `retry_verification`, `escalate_human`, `stop_degraded`. Verdict: disproved.

### Overall verdict

Hypothesis disproved. Four of six patterns have a clean typed decision; the other two have one each inside a text-generating shell. But note the asymmetry the user missed: disproving the hypothesis does not prove Jev can be the core orchestrator. The orchestrator in the article writes plans. Jev cannot. That is the whole argument of section 3.

## 2. Superloop taxonomy

Loops I can evidence, mapped to the six patterns:

| Loop | Evidence | Pattern | Typed or text decisions |
|---|---|---|---|
| Ralph Wiggum loop | "In its purest form, Ralph is a Bash loop" ([ghuntley.com/ralph](https://ghuntley.com/ralph)) | Autonomous agents | Done detection is a string match in code; task selection is text |
| omo ulw-loop / ralph-loop | Features doc: max iterations default 100, ends on completion, max iterations, or cancel ([omo docs](https://github.com/code-yeongyu/oh-my-openagent/blob/9ef62aa720eb5db87853df7c31a9884ae27db06a/docs/reference/features.md)) | Autonomous agents plus evaluator-optimizer | Done detection: `<promise>DONE</promise>`, now gated on an Oracle VERIFIED result ([commit f31537f](https://github.com/code-yeongyu/oh-my-openagent/commit/f31537f1)) |
| omo goal feature | "Goal feature (replaces ralph-loop)" in the repo AGENTS.md ([omo AGENTS.md](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/AGENTS.md)) | Autonomous agents | Goal state tools, typed by the host |
| omo boulder / start-work continuation | Work-plan continuation capped at 8 consecutive continuations ([omo commit 3a56234](https://github.com/code-yeongyu/oh-my-openagent/commit/3a56234e3)) | Prompt chaining with gates | Continuation decision is a hook rule in code |
| omo ulw-execute | Five gates per checkbox, evidence to a ledger ([omo orchestration docs](https://github.com/code-yeongyu/oh-my-openagent/blob/dfbeeec9/docs/guide/orchestration.md)) | Evaluator-optimizer | Gates produce evidence artifacts; verification is code |
| Spec-driven Ralph variants | Acceptance criteria 100% met before `<promise>DONE</promise>` ([fstandhartinger/ralph-wiggum](https://github.com/fstandhartinger/ralph-wiggum)) | Evaluator-optimizer | Criteria checks are code |
| Evaluator-optimizer itself | [Anthropic article](https://www.anthropic.com/research/building-effective-agents) | Evaluator-optimizer | Accept/reject is typed; feedback is text |

Two corrections to the brief's own framing. First, the omo loop names are moving targets: the repo's AGENTS.md says the goal feature "replaces ralph-loop," with the legacy hook directory "retained but no longer wired" ([omo AGENTS.md](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/AGENTS.md)). The harness example in model-mesh pins omo schema v4.19.4 and warns that newer docs rename agents; that warning is now concretely true. Second, Ralph's core insight is fresh context per iteration with state on disk ([ghuntley.com/ralph](https://ghuntley.com/ralph)); that is a state contract a decision model can read, which matters for section 4.

Bounded typed questions in loops: continue, stop, retry, escalate, route, done, agree, severity, triage. Need generated text: task selection, plans, feedback, synthesis, next-step prompts.

## 3. The proposal: System One core, omo workers, endless loop

Three corrections, then what survives.

### "Core orchestrator" must mean control plane, not planner

The article's orchestrator-workers and agents patterns require the central model to break down tasks and synthesize results. Jev returns typed answers with probabilities and produces no text ([TypeSafe docs](https://docs.typesafe.ai/concepts/system-one)). So the architecture that actually works is: a Python driver owns the while loop; omo sisyphus plans and manages workers using the matrix profiles; Jev answers the fork questions between iterations. The vendor's own guide frames it this way: Jev owns "a bounded question with a confidence, not a generated plan," and "the surrounding system owns the workflow" ([TypeSafe guide](https://madewithjev.com/jev-multi-agent)). Control plane, not planner. If the user wants Jev to write the plan, the proposal is dead on arrival.

### "Endless loop" is rejected

No evidenced production loop is endless. Ralph ends on a completion promise or an iteration cap ([ghuntley.com/ralph](https://ghuntley.com/ralph)). The omo loop defaults to 100 iterations and stops on completion or cancel ([omo docs](https://github.com/code-yeongyu/oh-my-openagent/blob/9ef62aa720eb5db87853df7c31a9884ae27db06a/docs/reference/features.md)). Boulder continuation is capped at 8 ([omo commit 3a56234](https://github.com/code-yeongyu/oh-my-openagent/commit/3a56234e3)). The article itself recommends stopping conditions "to maintain control" and warns of "higher costs, and the potential for compounding errors" ([Anthropic](https://www.anthropic.com/research/building-effective-agents)). An endless loop on paid inference with no budget is a runaway bill attached to an error compounding machine. The driver ships with hard stop rules in code, listed in section 4.

### Evidence status: nothing is measured, and one study points the wrong way

Vendor claims, labeled as such: 70 to 500 ms responses, $0.042 per million input tokens, free output ([launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev)). The same post admits the evaluations were built by the vendor's own team, "so some bias could exist," and that its demo "paints our model in an advantageous light." The service is US West Coast based with no published retention policy, which the repo note already flags ([SYSTEM-ONE.md](../SYSTEM-ONE.md)). The one independent study is exploratory: one target, one run per condition, and with Jev the harness hit 9 of 13 seeded vulnerabilities against 10 of 13 without it. The authors state that a miscalibrated System One layer cannot create false positives but "can cause false negatives: real findings may be downgraded or suppressed," that the worst case for false negatives "is worse than running without the layer," and that adversarial inputs are untested ([arxiv 2609.28940](https://arxiv.org/html/2609.28940v1)). Hong Kong reach is unverified, so the ultimate profile cannot admit it under rule O6.

Practical conclusion: no production seat today. Shadow mode first, which is both what the repo note already prescribes and what the vendor's own integration guide recommends: "Run it in shadow first. Let Jev answer and let the real system do what it already did; log the disagreements, then switch it on" ([TypeSafe guide](https://madewithjev.com/jev-multi-agent)). The council is not being asked to bless a result; per the owner's standing rule 2, this is a proposal, not a result.

### Failure modes the driver must handle

False negatives: Jev may lower confidence, flag for review, or prune a candidate list. It may not override the deterministic validator, restore a rejected finding, or clear a cross-family reviewer blocker. This is already codified in [SYSTEM-ONE.md](../SYSTEM-ONE.md); keep it verbatim. Adversarial state: the state text sent to Jev is attacker-influenced in security situations ([arxiv](https://arxiv.org/html/2609.28940v1)); hash it, log it, and never let a probability authorize an action: "A decision model that returns a high confidence has told you it is sure, not that it is allowed" ([TypeSafe guide](https://madewithjev.com/jev-multi-agent)). Calibration drift: pin the model version and re-score against labels periodically. Outage: kill switch env var, fallback to plain rules (iteration cap plus reviewer blockers). Independence: Jev generates no text, so it cannot become an author, reviewer, or aggregator seat, but the driver must keep the decision model from grading work it routed; the guide says "separate deciding from verifying completion."

## 4. PR recommendation

Scope: one PR, mergeable and CI-clean with no Jev account, no network, no omo install. Files:

### New: docs/research/orchestration/SUPERLOOP.md

The taxonomy from section 2 with links, the control-plane design, the stop rules, and the shadow pilot protocol with pass conditions. Pass condition, stated before the run: no seeded blocker suppressed or downgraded, and calibration holds on model-mesh's own labels, not the vendor's. This extends [SYSTEM-ONE.md](../SYSTEM-ONE.md) rather than replacing it.

### New: scripts/superloop.py

Stdlib-only Python driver, MIT, same style as [validate-orchestration.py](../../../../scripts/validate-orchestration.py).

Inputs: `--profile {ultimate,hybrid,b4b,global}`, `--goal`, `--situation A01..A12`, `--max-iterations 100`, `--budget-usd`, `--deadline-minutes`, `--decision-backend {stub,jev,none}`, `--questions examples/orchestration/decision-questions.json`, `--dry-run`, `--shadow`.

How it invokes omo: per the harness example, `opencode run "<task>"` inside a git worktree, with model routing materialized to omo.jsonc by the existing `scripts/materialize.py` from `profiles/<name>.json` ([opencode-omo.example.json](../../../../examples/orchestration/harnesses/opencode-omo.example.json)). After each iteration the driver collects state: `.omo/boulder.json`, todo counts, `.omo/ulw-execute/ledger.jsonl`, review findings validated against finding.schema.json, git status. State sent to the decision model is a bounded text digest (goal, checkbox states, verification results, clustered findings, spend, iteration count), size-capped, hash-logged.

Exact typed questions:

- choice `route_situation`: options A01 to A12 plus `unrouted`. Asked once per run, at the fork. This is the one fork the pilot activates.
- noul `goal_complete`: "Given the state, is the goal met with the verification evidence shown?" Stop requires P >= 0.8 AND all checkboxes done AND zero cross-family blockers.
- choice `next_action`: `continue`, `retry_verification`, `escalate_human`, `stop_degraded`. Only options that exist in the current state.
- choice `finding_triage` per clustered finding: `confirm`, `needs_review`, `reject`. score `severity` 0 to 3.
- noul `needs_human`: escalate when P >= 0.6 or after 3 failed fix-verify cycles.

Stop rules, in code, not in the model: iteration cap 100 (matches omo default), 3 failed fix-verify cycles on one issue (matches the mm-loop hard bound), budget cap, deadline, no-progress detector (todo count and ledger unchanged for 2 consecutive iterations), any cross-family reviewer blocker (the model can never clear it), kill switch env var `MM_SUPERLOOP_BYPASS`.

Logs: `logs/superloop/<run-id>/decisions.jsonl`, one line per decision: timestamp, run id, iteration, state hash, question id, answer, probability, latency, what the process actually did, disagreement flag in shadow mode. This log is the pilot's currency; without it there is no label set and no pass condition.

Offline testing: `--decision-backend stub` reads canned answers from a fixture keyed by question id. `--dry-run` runs the loop against a fake `opencode` script in `tests/fixtures/`. `--self-test` mutates a valid run and expects each stop rule to fire, same pattern as the orchestration validator's self-test. The Jev client is a thin adapter behind an interface; the API key lives in an env var and never in the repo, which keeps the open-source rule D46 intact: the driver and stub are open source, the inference model is not required to be.

### New: examples/orchestration/decision-questions.json

The versioned question catalog with thresholds. Real IDs stay out, consistent with the example-file convention.

### Edit: skills/mm-loop/SKILL.md

Add a short superloop section: when a goal needs more than one loop, point at the driver, restate the stop rules, note that the decision model never clears blockers. Keep the skill model-agnostic.

### Edit: docs/research/orchestration/SYSTEM-ONE.md

Add the pilot results template: labels, disagreement counts, suppressed-finding count, calibration check, reachability test result. Update the "what would change this assessment" section to reference the driver.

### Not in this PR: validate-orchestration.py changes

Do not add a decision-seat rule yet. The validator proves policy, and today there is no policy to prove; a rule for a seat that does not exist is noise. If the pilot passes, add rule O19 in the follow-up PR that adds the seat.

### Explicitly out of scope

Replacing the omo orchestrator seat. Adding Jev to any profile, ultimate included. Production activation of any decision. Endless mode. Letting the decision model touch the aggregator, clear blockers, or grade its own routing. Any claim of measured speed, cost, or accuracy.

## 5. Open questions for the owner

1. Budget number: what USD and wall-clock cap should the hard stop rules carry by default? I need one number each, not a principle.
2. Which fork pilots first: situation routing (A01 class of work) or finding triage (A06)? Routing is cheaper to check; triage is where the false-negative risk lives.
3. Is a paid TypeSafe key acceptable with no published retention policy, or does the pilot wait for the open-weight route ([stephenlb/system-one-model](https://github.com/stephenlb/system-one-model)) to mature?
4. omo target surface: goal feature or ulw-loop? The loop names changed under us (ralph-loop is deprecated), and the harness example pins schema v4.19.4. Do we pin, or track dev?
5. If a paid engagement needs this loop, the omo Sustainable Use License needs its own check first ([ORCHESTRATION.md](../../../ORCHESTRATION.md) already flags this). Confirm commercial use is out of scope for now.

## Bottom line

Disprove the hypothesis: yes, done above. Build "System One as the core orchestrator with an endless loop": no. Build a shadow-mode control plane around the existing omo loop with stop rules in code and a decision log that produces labels: yes, this PR, and nothing larger until the pilot returns data.
