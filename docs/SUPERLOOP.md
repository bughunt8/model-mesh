# Superloop

A superloop is an outer loop that keeps sending work to agents until a goal is met. This page defines the model-mesh version: code owns the loop, omo workers do the work in bounded batches, a typed decision model answers bounded questions at fixed points, and only evidence ends the loop.

Status: design plus a driver tested offline, dated 2026-10-29. No live run has happened. No decision model is adopted: the shipped configs run the decision model in shadow mode, where its answers are logged and change nothing. Every speed, cost and accuracy figure for any decision model is unmeasured for model-mesh. The research and the council debate behind this page are in [SUPERLOOP-COUNCIL.md](research/orchestration/SUPERLOOP-COUNCIL.md) and [SYSTEM-ONE.md](research/orchestration/SYSTEM-ONE.md).

## The four parts

Think of a railway. The trains are the omo workers. The timetable writer is the omo planner agent, which writes plans in prose. The signalman is the decision model: he pulls one lever from a fixed set, shows red or green, or reads a gauge, and he cannot lay track or write the timetable. The interlocking is plain code that refuses an unsafe route whatever the signalman wants. The track circuits are the acceptance checks.

| Part | What it does | What it may never do |
|---|---|---|
| Control plane (`scripts/mm-superloop.py`) | Owns the loop, the caps, the budget, the lineage ledger, the stop rules and the log | Trust a worker's own report of success |
| Decision model | Answers typed questions (choice, yes or no, ordered score) about a state built from facts | Write plans, prompts or code. End the loop as a success. Skip a check. Change the profile. Approve an action |
| Workers | One omo batch per iteration in the run's worktree, under the frozen profile and matrix option | Run their own continuation loop inside the superloop |
| Verifier | Acceptance checks, then a zero-context review in a harness and model family that never authored in this run | Be replaced or overruled by the decision model |

"Decision model at the core" therefore means the control plane asks it at every fork. It does not mean it plans. Planning stays with a generating model.

## Where a decision model fits the six patterns

The six patterns are from Anthropic's [Building effective agents](https://www.anthropic.com/research/building-effective-agents). The hypothesis that a decision model has no place in them is false: each pattern contains at least one bounded decision. It holds only for the planner seat itself, because breaking down a task and synthesising results need generated text.

| Pattern | Decision the model can make | What still needs a generating model or code |
|---|---|---|
| Prompt chaining | The gate between steps: does this output meet the step's contract | Every step's content. Gates that code can check stay in code |
| Routing | Which situation, A01 to A12, fits the goal. Anthropic names "a more traditional classification model" as an option here | The specialised follow-up work |
| Parallelization | Whether two findings describe one defect, or whether a seat should add a reviewer | The parallel work itself. Counting votes is code |
| Orchestrator-workers | Which ready task or worker comes next, from a menu code builds | Breaking down the task and synthesising results |
| Evaluator-optimizer | The verdict half: ready for review, or not | The feedback half, which is prose |
| Autonomous agents | Progressing, stalled, regressing or drifting. Blocked on a person or not | Every tool call and edit |

## Loop types

| Loop | Mechanism | What stops it |
|---|---|---|
| Fresh-process loop ("Ralph") | A shell loop feeds the same prompt to an agent; state lives in files | A person watching, or a completion string |
| Stop-hook or idle-hook loop (omo Goal) | The harness re-injects a continuation when the agent goes idle | The agent's own claim. The Goal iteration setting is not enforced in the inspected omo code, in 4.19.4 or later |
| Todo continuation | Idle agents are pushed back to unfinished todos | An empty todo list, which the agent wrote. In 4.19.4 it also gives up after repeated stagnant or failed continuations |
| Plan continuation | A frozen plan is executed step by step and resumed after interruption | The plan's checklist |
| Dependency-graph waves | A planned graph runs in parallel waves | The graph completing |
| mm-loop | Plan, execute, verify, report, with a hard bound of 3 failed fix-verify cycles | Evidence, or the cycle bound |
| Superloop (this page) | Code runs bounded batches and asks typed questions between them | Evidence, a cap or a hand-back, in code |

Loops that end on the agent's own claim are the weak ones. A loop whose only exit is "done" teaches the worker to say "done". The superloop has honest exits for "blocked", "no progress" and "out of budget", and its success exit does not read the worker's claim at all.

## The authority rule

The decision model may brake. It may never accelerate.

| Allowed in advisory mode, with a qualified threshold | Never allowed, in any mode |
|---|---|
| Pause the run for a person (`blocked`, `needs_human`) | End the run as a success |
| Stop the run for no progress (`progress`) | Skip or overrule an acceptance check or a review |
| Add review seats when the checks pass but the facts look thin (`goal_met`, as a smoke detector) | Change the profile, the option or the caps |
| | Approve an irreversible, outward, paid or permission-changing action |

A wrong brake costs one look from a person or one review call. A wrong acceleration could ship broken work, so there is no way to accelerate. The question catalog is [questions.json](../examples/superloop/questions.json), and the validator rejects any question whose authority goes beyond braking.

## One iteration

1. Interlocks, with no model call: stop file, iteration cap, wall clock, and the budget reservation for the next batch.
2. One worker batch: `oh-my-openagent run --agent sisyphus --json --directory <worktree> "<prompt>"` from a local, pinned omo 4.19.4 install. The prompt is built by code from the goal, the failing checks and the open review findings. The worker is told not to declare the goal complete.
3. Acceptance checks run as argv lists with timeouts. The control plane hashes the whole tree and the protected paths.
4. Facts: check results, tree change, unchanged streak, regressions, protected-path changes, the worker's exit and timeout, and the last review's counts.
5. Decision questions: `progress`, `blocked`, `needs_human`, `goal_met` and `next_action`, plus `situation` once at the start. The rules baseline answers the same questions, and both answers are logged.
6. Brakes, if advisory mode and a qualified answer crosses its threshold.
7. Stop rules in code: protected path changed, worker reported blocked, no progress, fix-verify cycles exhausted.
8. Review, when every check passes, when a brake adds one, or on an optional cadence. The reviewer gets the diff and its lenses and nothing else.
9. Success, only when every check passes on the current tree and a cross-family review of that same tree found no blocker and no corroborated major finding.

## Stops and defaults

| Cap | Default | Source |
|---|---|---|
| Outer iterations | 10 | Council, three of five members |
| Wall clock | 30 minutes | Council, unanimous |
| No-progress streak | 2 batches with the same tree and the same failing checks | Council, unanimous |
| Fix-verify cycles on one failure | 3 | The existing mm-loop bound |
| Per call | 600 seconds | Proposed |
| Budget | Set by the owner. The example uses 5 USD | Owner decision |

Spend is reserved before each call from the controller's per-call reservations, because missing usage is not zero cost. Resuming a run or carrying work into a new run never resets the lineage: earlier authors go in the goal's `prior_lineage`.

Terminal states: `verified_pending_owner` or `verified` (success), `cap_iterations`, `cap_wall_clock`, `cap_budget`, `no_progress`, `fix_cycles_exhausted`, `blocked_human`, `review_unavailable`, `worker_failure`, `policy_denied`, `cancelled`. Running out of a cap never counts as success.

## Endless, in a sentence the owner can sign

"The superloop is a standing service. It keeps taking goals, but each goal ends on verified evidence, a cap or a hand-back, and only I renew a cap."

## Modes and qualification

| Mode | What the decision model's answers do | Admission |
|---|---|---|
| `shadow` (default) | Logged next to the rules baseline. Nothing else | Any backend. Under ultimate, a remote endpoint must be verified as Hong Kong reachable, because shadow calls still send the state |
| `advisory` | A qualified brake or smoke answer may act, within the authority rule | A disclosed base family that shares nothing with any seat in the run, and a qualification record per question |

There is no mode in which the decision model controls the loop.

A point threshold such as 0.8 is a label, not a promise. One audit found point-chosen gates broke their promise in 147 of 190 evaluations, while learn-then-test kept it in all 190 ([Confidence Is Not a Promise](https://arxiv.org/html/2610.36311v1)). So a threshold acts only through a qualification record made by [qualify.py](../scripts/superloop/qualify.py): a fixed-sequence learn-then-test procedure over at least 100 labelled decisions from model-mesh's own runs, with stated alpha and delta, for one backend, one pinned model, one question revision and one locale. Labels come from people or deterministic ground truth, never from the decision model. The control plane reads raw probabilities and computes its own top probability and margin, because vendors define "confidence" differently.

## Independence

- The decision seat is an orchestration seat once it can act. In advisory mode its base family must be disclosed and must share nothing with any author, orchestrator, reviewer or aggregator family in the run. A model fine-tuned from an open base takes the base model's family. Undisclosed lineage blocks advisory mode.
- A shadow seat is exempt from the family rule because its answers reach no acting agent, but its provider, pinned model and lineage are logged.
- The lineage ledger records every harness and family that authored or orchestrated, across all fallback rungs and earlier segments. A reviewer that shares any of them is refused. If none is left, the run stops with `review_unavailable`.
- The profile and matrix option are frozen at admission. Switching mid-run could put a reviewer over its own family's earlier work: in A01, one profile uses a family as an author and another uses the same family as the reviewer.

## What the decision model sees

The state is built from facts the control plane observed: check results, hashes, counters, review counts and the owner's goal text. A worker's narrative never enters as a fact. Its status file is kept under `claims`, marked untrusted, and only a "blocked" claim is used, because that can only stop the run. Evidence spans from any extractor are admitted only when the text at the stated character or byte offsets of the original file equals the span. Summaries and compressed context never enter the state, because a rewrite can drop the one line that matters and cannot be checked against its source. Strings that look like keys are redacted. If the required facts do not fit the backend's token budget, every answer becomes an abstention.

Schema-valid output is not correct output. A paper on constrained decoding found that grammar constraints made five small models 100 percent schema-valid while one output still scored 1.000 with an email body of "1. 2. 3. 4. 5." ([Chavan](https://arxiv.org/html/2609.23742)). The control plane therefore checks the meaning of every answer in code: the option must be on the menu it offered, the probabilities must sum to about 1, the chosen option must be the most probable, and no answer can stand in for a check.

## The omo link

- Pin omo 4.19.4, the version the repo's schema follows, and run its local binary, not a runtime package download.
- The control plane materializes the profile into `<worktree>/.omo/omo.jsonc` with `goal.enabled` false and the `goal`, `todo-continuation-enforcer`, `start-work` and `atlas` hooks disabled, so each call is one batch and the superloop owns continuation.
- `opencode run --agent` looks the agent up by exact host key, and omo registers display names. The omo wrapper resolves config keys. Either way the control plane checks the agent the JSON output reports against the expected names and refuses a mismatch.
- Known gap: with the todo enforcer disabled, the wrapper still waits while todos are open, so a worker that stops with open todos waits until the per-call timeout. A follow-up can attach to an `opencode serve` instance and stop on idle with open todos.
- None of this has been run against a live omo install. The first live run should be a dry run that records the effective config, the resolved agent and the exit behavior.

## What is not built

- No decision model is adopted, and the orchestration matrix has no decision seat. Matrix rules for a decision seat wait until one is adopted.
- No vendor-specific backend code. The generic `http` backend sends one request shape to any compatible endpoint; the example config points it at one vendor in shadow mode.
- No extraction, summarization or compression service.
- No migration to omo 5.x or its native edition.
- No measurement. The pilot's job is to produce the labelled log that a decision model must beat the rules baseline on.

## Commands

```text
python scripts/validate-superloop.py
python scripts/mm-superloop.py --goal GOAL.json --controller CONTROLLER.json --worktree PATH --out runs/RUN_ID
python scripts/mm-superloop.py --self-test
```

Templates: [goal.example.json](../examples/superloop/goal.example.json), [controller.example.json](../examples/superloop/controller.example.json) for a shadow pilot, and [controller.rules.example.json](../examples/superloop/controller.rules.example.json) for the offline rules baseline. The agent-facing instructions are in [skills/mm-superloop/SKILL.md](../skills/mm-superloop/SKILL.md).
