# Superloop

A superloop is an outer loop that keeps sending work to agents until a goal is met. This page defines the model-mesh version: code owns the loop, omo workers do the work in bounded batches, a typed decision model answers bounded questions at fixed points, and only evidence ends the loop.

Status: design plus a driver tested offline, dated 2026-10-29, hardened over two rounds of independent review on another model family, which reproduced thirteen ways to forge a success (see [the review record](research/orchestration/SUPERLOOP-COUNCIL.md#independent-review)). No live run has happened. No decision model is adopted: the shipped configs run the decision model in shadow mode, where its answers are logged and change nothing. Every speed, cost and accuracy figure for any decision model is unmeasured for model-mesh. The research and the council debate behind this page are in [SUPERLOOP-COUNCIL.md](research/orchestration/SUPERLOOP-COUNCIL.md) and [SYSTEM-ONE.md](research/orchestration/SYSTEM-ONE.md).

## The four parts

Think of a railway. The omo workers are the trains and the decision model is the signalman: he pulls one lever from a fixed set and cannot lay track or write the timetable. The interlocking is plain code that refuses an unsafe route whatever he wants, and the track circuits are the acceptance checks.

| Part | What it does | What it may never do |
|---|---|---|
| Control plane (`scripts/mm-superloop.py`) | Owns the loop, the caps, the budget, the lineage ledger, the stop rules and the log | Trust a worker's own report of success |
| Decision model | Answers typed questions (choice, yes or no, ordered score) about a state built from facts | Write plans, prompts or code. End the loop as a success. Skip a check. Change the profile. Approve an action |
| Workers | One omo batch per iteration in the run's worktree, under the frozen profile and matrix option, with only the cell's author and orchestrator model families in their config | Run their own continuation loop inside the superloop. Edit their own config |
| Verifier | Acceptance checks, then a zero-context review in a fresh folder by a reviewer whose harness and families never authored in this run, then the checks again | Be replaced or overruled by the decision model |

"Decision model at the core" therefore means the control plane asks it at every fork. It does not mean it plans. Planning stays with a generating model.

## Trust boundary

The driver's guarantees need two things it does not provide by itself.

- The worker can write only inside its worktree. A worker running as the driver's own OS user can edit the driver, the registries and the run folder, attach to the reviewer process, or delete the lineage, and no check in the driver can stop that. Run the worker as another OS user or in a container where only the worktree is writable. omo's and OpenCode's own permission settings are not a sandbox.
- Each acceptance check sees only its snapshot. An unjailed check is an ordinary process: it can open the live worktree, including `.git`, by path, or find it through `/proc`. With `check_jail: bwrap` the driver runs each check under bubblewrap, with the filesystem read-only, the live worktree, its git directory and the run folder replaced by empty folders, only the snapshot writable, its own process and network namespaces and an environment built from nothing. bubblewrap needs Linux with unprivileged user namespaces; the driver tests it at admission and refuses the run if it does not work.

The controller states both: `worker.isolation` (`separate_user`, `container` or `none`) and `check_jail` (`bwrap` or `none`). The driver cannot verify the first. `final.json` repeats both and sets `protected` to true only for `container` or `separate_user` together with `bwrap`. A success with `protected: false` says the checks and the review passed; it does not say a worker could not have staged them.

Inside that boundary, the driver itself never runs git in the worker's repository. It keeps its own object store in the run folder, outside the worktree, and reads the worktree as plain files: no repository config, hooks, filters, replace refs or attributes from the worker's side take part.

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
2. The control plane rewrites `.omo/omo.jsonc` from the frozen config.
3. One worker batch: `oh-my-openagent run --agent sisyphus --json --directory <worktree> "<prompt>"` from a local, pinned omo 4.19.4 install. The prompt is built by code from the goal, the failing checks and the open review findings. It tells the worker not to declare the goal complete, not to edit protected paths or the omo config, and not to send, publish, pay, change permissions or delete outside the worktree.
4. Batch checks: the omo config must be unchanged, and the session's agents and models, read through the pinned export command, must be readable, all in `expect_agents`, and all in the cell's families. Otherwise the run stops with `policy_denied`.
5. The control plane hashes the worktree's files into its own git store, through a fresh private index, ignored files included. System and global git config, hooks, replace objects and attributes are all off, so the stored blobs are the bytes in the files. Left out are every `.git`, the worker's status file and the controller's omo config (checked on its own). A nested repository, a symlink that leaves the tree, or a `.git` that moved during the batch stops the run.
6. Acceptance checks run as argv lists on a fresh copy of that tree, written from the stored blobs, never in the live worktree, with an environment built from nothing (`PATH`, a private `HOME`, `TMPDIR` and a locale). Under `check_jail: bwrap` the copy is all the check can see, so it sees the bytes the reviewer's diff describes and nothing under `.git`. Under `none` that holds only for checks that stay in their working folder. Each check gets the smaller of its own timeout and the wall-clock time left. A check that needs another variable passes it in its argv, for example through `env`.
7. Facts: check results, tree change, idle streak, regressions, protected-path changes, the worker's exit and timeout, and the last review's counts.
8. Decision questions: `progress`, `blocked`, `needs_human`, `goal_met` and `next_action`, plus `situation` once at the start. The rules baseline answers the same questions, and both answers are logged.
9. Brakes, if advisory mode and an answer crosses a verified threshold.
10. Stop rules in code: protected path changed, worker reported blocked, no progress, fix-verify cycles exhausted.
11. Review, when every check passes, when a brake adds one, or on an optional cadence. The reviewer runs in a fresh folder holding only the diff from the admission tree to the current tree and its lenses. Its pins are hashed again just before it starts. It must exit 0 within its timeout and print its findings as a JSON list on the last line of its output, which the driver reads through a pipe; no findings file is trusted. Invalid or missing findings stop the run. If the worktree changed during the review, the run stops.
12. Success, only when the review found no blocker and no major finding, the tree is still the reviewed tree, every check passes a second time on a new copy of it, and wall-clock time is left.

Before the first batch, the checks also run once on the admission tree. If every one of them already passes, the run is refused: a check that cannot fail before the work cannot show the work was done.

## Stops and defaults

| Cap | Default | Source |
|---|---|---|
| Outer iterations | 10 | Council, three of five members |
| Wall clock | 30 minutes, checked before every call and after every check | Council, unanimous |
| No-progress streak | 2 batches in a row that leave the tree and the failing checks unchanged | Council, unanimous |
| Fix-verify cycles | 3 batches with the same failing checks, or 3 reviews in a row with a blocker or major | The existing mm-loop bound |
| Per call | 600 seconds | Proposed |
| Budget | Set by the owner. The example uses 5 USD | Owner decision |

Spend is reserved before each call from the controller's per-call reservations, because missing usage is not zero cost. Worker and review reservations must be above zero, and so must the decision reservation when a remote backend is used. A dual backend reserves two decision calls. A reservation the controller leaves out stops the run instead of counting as free.

The driver never resets the lineage itself. Earlier authors go in the goal's `prior_lineage`, and every admitted run also appends its lineage to a registry outside the worktree (`~/.local/state/model-mesh/superloop-lineage.jsonl` by default). The owner creates it once with `--init-registry`; a missing registry stops the run, because a missing registry is not an empty history. Entries are keyed by the controller's `repository`, the owner's name for the repository, and by goal id, so renaming a branch or a goal does not escape them. The first run under a name binds it to the worktree's git directory, and a later run whose git directory differs is refused, so a worker that points `.git` somewhere new between runs cannot start a fresh lineage. Every branch and linked worktree of one clone shares the git directory. This is conservative: unrelated earlier work in the same clone also counts. A worker that runs as the owner's user can still delete and recreate the file, which is why the trust boundary above matters. A run refuses an output directory that already holds a log.

Terminal states: `verified_pending_owner` or `verified` (success), `cap_iterations`, `cap_wall_clock`, `cap_budget`, `no_progress`, `fix_cycles_exhausted`, `blocked_human`, `review_unavailable`, `worker_failure`, `policy_denied`, `cancelled`. Running out of a cap never counts as success. `final.json` lists any open blocker or major findings, the stated isolation, the check jail and whether the run was `protected`. Any error the driver did not expect also ends in `final.json` as `policy_denied`, with the error type in the reason.

## Endless, in a sentence the owner can sign

"The superloop is a standing service. It keeps taking goals, but each goal ends on verified evidence, a cap or a hand-back, and only I renew a cap."

## Modes and qualification

| Mode | What the decision model's answers do | Admission |
|---|---|---|
| `shadow` (default) | Logged next to the rules baseline. Nothing else | Any backend, except that the ultimate profile admits only local or offline backends, because shadow calls still send the state. No controller flag overrides that until a reachability and data-policy check exists |
| `advisory` | A brake or smoke answer above a verified threshold may act, within the authority rule | A base family on the known family list that shares nothing with any seat in the run, and a verified qualification record per acting question |

There is no mode in which the decision model controls the loop.

A point threshold such as 0.8 is a label, not a promise. One audit found point-chosen gates broke their promise in 147 of 190 evaluations, while learn-then-test kept it in all 190 ([Confidence Is Not a Promise](https://arxiv.org/html/2610.36311v1)). So a threshold acts only through a qualification record file written by [qualify.py](../scripts/superloop/qualify.py): a fixed-sequence learn-then-test procedure over at least 100 labelled decisions from model-mesh's own runs, with stated alpha and delta, for one backend, one pinned model, one question revision and one locale. Every label must name a person or deterministic ground truth as its source, never the decision model. The controller only points at the record, and the owner pins the record's SHA-256 in the tools registry. At admission the driver checks that pin, checks that the dataset still matches its recorded hash, and re-runs the procedure; a record whose threshold does not come out the same is refused. Code cannot tell whether a row marked `human` was labelled by a person, so the owner has to read the dataset before pinning the record. The control plane reads raw probabilities and computes its own top probability and margin, because vendors define "confidence" differently.

## Independence

- The omo config is restricted to the frozen cell. A profile config names models from many families, and omo can call any of them through delegation, categories or fallback. So the control plane keeps only models whose family belongs to the cell's author and orchestrator seats, disables an agent with none left, gives an empty category the run agent's model, turns runtime fallback and team mode off, and refuses the run if any other family remains. Without this step no reviewer in the shipped matrix would be independent.
- The decision seat is an orchestration seat once it can act. In advisory mode its base family must be on the known family list and must share nothing with any author, orchestrator, reviewer or aggregator family in the run. A model fine-tuned from an open base takes the base model's family. Undisclosed lineage blocks advisory mode.
- A shadow seat is exempt from the family rule because its answers reach no acting agent, but its provider, pinned model and lineage are logged.
- The lineage ledger records every harness and family that authored or orchestrated: all fallback rungs of the cell's seats, every family left in the config, every model a session reported, `prior_lineage` and the registry entries. A reviewer that shares any of them is refused. If none is left, the run stops with `review_unavailable`.
- Aggregation is code (`scripts/aggregate-findings.py`), not a model call. This is a decision, not a fix: the matrix's aggregator seat is not used, so its family is left out of the reviewer conflict set and may review. In the shipped cells the aggregator and the reviewer are the same seat.
- Workers and reviewers are not defined in the controller. The controller names a reference. The owner's tools registry, outside every worktree (`~/.config/model-mesh/superloop-tools.json` by default, template in `examples/superloop/tools.example.json`), holds each argv and a SHA-256 for the executable and every absolute path in the argv, such as a recipe, a script, the omo entry file and the export program. The driver hashes every pin again immediately before each call, runs the resolved real path, and stops the run on a mismatch. A small window between the hash and the start of the process remains.
- The profile and matrix option are frozen at admission. Switching mid-run could put a reviewer over its own family's earlier work: in A01, one profile uses a family as an author and another uses the same family as the reviewer.

## What the decision model sees

The state is built from facts the control plane observed: check results, hashes, counters, review counts and the owner's goal text. A worker's narrative never enters as a fact. Its status file is kept under `claims`, marked untrusted, and only a "blocked" claim is used, because that can only stop the run. Evidence spans from any extractor are admitted only when the text at the stated character or byte offsets of the original file equals the span. Summaries and compressed context never enter the state, because a rewrite can drop the one line that matters and cannot be checked against its source. Strings that look like keys or tokens are redacted: common provider key prefixes, bearer tokens, JWTs and key=value pairs. That is a backstop, not a guarantee. If the required facts do not fit the backend's token budget, that fork is logged as `decision_skipped` and every answer is an abstention; success never depends on an answer, so the run goes on under the rules and the caps. The driver passes no extracted spans today, because no extractor is wired in; the offset check is the contract one would have to meet.

Schema-valid output is not correct output. A paper on constrained decoding found that grammar constraints made five small models 100 percent schema-valid while one output still scored 1.000 with an email body of "1. 2. 3. 4. 5." ([Chavan](https://arxiv.org/html/2609.23742)). The control plane therefore checks the meaning of every answer in code: the option must be on the menu it offered, the probabilities must sum to about 1, the chosen option must be the most probable, and no answer can stand in for a check.

## The omo link

- Pin omo 4.19.4, the version the repo's schema follows, and run a local install named in the tools registry, not a runtime package download. The control plane checks the version the binary reports before the first batch. The pins cover the entry files and the lockfile, not every installed dependency.
- The control plane writes `<worktree>/.omo/omo.jsonc` from the profile, restricted to the cell's families, with `goal.enabled` false, runtime fallback and team mode off, the `goal`, `todo-continuation-enforcer`, `start-work`, `atlas` and `runtime-fallback` hooks disabled, and the `goal` and `start-work` commands disabled. It rewrites the file before every batch and stops the run if a batch changed it.
- `opencode run --agent` looks the agent up by exact host key, and omo registers display names. The omo wrapper resolves config keys.
- In 4.19.4 the `--json` result has only `sessionId`, `success`, `durationMs`, `messageCount` and `summary` ([types.ts](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/v4.19.4/packages/omo-opencode/src/cli/run/types.ts)), so it cannot show which agent or model ran. The control plane reads the session through the export command pinned in the tools registry (for example `opencode export <sessionId>`) and refuses the batch if it cannot read an agent and a model, if any agent is outside `expect_agents`, or if any model family is outside the cell. Subagent sessions are not read; their models come from the restricted config. The export format was not checked on a live install.
- Known gap: with the todo enforcer disabled, the wrapper still waits while todos are open, so a worker that stops with open todos waits until the per-call timeout. A follow-up can attach to an `opencode serve` instance and stop on idle with open todos.
- None of this has been run against a live omo install. The first live run should be a dry run that records the effective config, the export output, the resolved agent and the exit behavior.

## What is not built

- No decision model is adopted, and the orchestration matrix has no decision seat. Matrix rules for a decision seat wait until one is adopted.
- Owner-written acceptance checks are trusted. The validator refuses obvious no-ops and the driver refuses checks that all pass before the work, but neither can tell a weak test from a strong one. That stays the owner's job, together with listing the tests under `protected_paths`.
- No check jail outside Linux. On macOS or Windows, run the driver inside a Linux container or accept `check_jail: none` and `protected: false`.
- The jail has no network. A check that needs a download fails under `bwrap`; fetch dependencies before admission.
- Hashing and copying ignored files makes a large dependency folder in the worktree slow: every batch writes a full copy for the checks. Nested repositories are refused rather than hashed.
- Rotating which checks fail can avoid the fix-verify count; the iteration cap still bounds it.
- No vendor-specific backend code. The generic `http` backend sends one request shape to any compatible endpoint; the example config points it at one vendor in shadow mode.
- No extraction, summarization or compression service.
- No migration to omo 5.x or its native edition.
- No measurement. The pilot's job is to produce the labelled log that a decision model must beat the rules baseline on.

## Commands

```text
python scripts/validate-superloop.py
python scripts/mm-superloop.py --init-registry
python scripts/mm-superloop.py --goal GOAL.json --controller CONTROLLER.json --worktree PATH --out ~/.local/state/model-mesh/runs/RUN_ID
python scripts/mm-superloop.py --self-test
```

Templates: [goal.example.json](../examples/superloop/goal.example.json), [controller.example.json](../examples/superloop/controller.example.json) for a shadow pilot, [controller.rules.example.json](../examples/superloop/controller.rules.example.json) for the offline rules baseline, and [tools.example.json](../examples/superloop/tools.example.json) for the owner's tools registry. The agent-facing instructions are in [skills/mm-superloop/SKILL.md](../skills/mm-superloop/SKILL.md).
