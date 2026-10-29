# Superloop council: a decision model at the core of an omo loop

This is the synthesis of the council that shaped [SUPERLOOP.md](../../SUPERLOOP.md). The raw reports, the brief, the CDM addendum and the round 2 instructions are in [superloop-council/](superloop-council/README.md), unedited apart from trailing whitespace and repaired relative links.

Date: 2026-10-29. Five members on five model families, two rounds plus an addendum on constrained decoding models (CDMs). Roles: GPT 6.1 Sol was the First-Principle, Gemini 4 Argon the Adversarial, Claude Opus 5.5 the Explainer, GLM 5.3 the Practical and Kimi K3 the Researcher. Grok 4.7 stayed off the council so it could review the resulting PR independently. Everything below is a proposal from the council, not a measured result.

The question: the owner's hypothesis is that a System One decision model such as Jev has no place in the six agentic patterns from Anthropic's [Building effective agents](https://www.anthropic.com/research/building-effective-agents). The council was asked to disprove it, map the loop types onto the six patterns, debate using a decision model as the core orchestrator of an endless loop of omo profiles, and recommend a PR.

## Where models agree

| Finding | GPT 6.1 Sol | Gemini 4 Argon | Claude Opus 5.5 | GLM 5.3 | Kimi K3 | Evidence |
|---|---|---|---|---|---|---|
| The hypothesis is false: each of the six patterns has a bounded fork a typed decision model can answer. It holds only for the planner seat, because breaking down a task and synthesising results need generated text | ✓ | ✓ | ✓ | ✓ | ✓ | Anthropic names "a more traditional classification model/algorithm" as an option for routing ([Anthropic](https://www.anthropic.com/research/building-effective-agents)). TypeSafe says System One models do not write text ([TypeSafe docs](https://docs.typesafe.ai/concepts/system-one)) |
| Code owns the loop. Each omo call is one batch with omo's goal and todo continuation disabled, and an exit code of 0 means quiet, not done | ✓ | ✓ | ✓ | ✓ | ✓ | omo's run wrapper waits until todos are done and no continuation hook is active ([omo CLI reference](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/cli.md)) |
| The decision model may brake but never declare success. A "goal met" answer is at most a smoke detector that triggers an early review | ✓ | ✓ | ✓ | ✓ | ✓ | GLM 5.3 retracted its round 1 stop rule "P >= 0.8 on goal_complete" |
| Point thresholds such as 0.8 are shadow labels. Acting on one needs learn-then-test qualification per backend, and the vendors' "confidence" figures are different quantities | ✓ | ✓ | ✓ | ✓ | ✓ | Point gates broke their promise in 147 of 190 evaluations, and an English-calibrated gate held in 8 of 51 locales ([Brom audit](https://arxiv.org/html/2610.36311v1)). Jev's choice confidence is rescaled ([TypeSafe confidence](https://docs.typesafe.ai/confidence.md)), while ScaleDown's is the raw probability ([ScaleDown decisions API](https://docs.scaledown.ai/api-reference/decisions)) |
| The profile is frozen at admission, and reviewers are checked against the run's whole author lineage | ✓ | ✓ | ✓ | ✓ | ✓ | In A01, one profile uses DeepSeek as an author and another uses it as the reviewer, so a mid-run switch would put DeepSeek over its own work (repo matrix) |
| "Endless" is rejected. What the owner can sign is a run that ends on verified evidence, a cap or a hand-back | ✓ | ✓ | ✓ | ✓ | ✓ | Five one-sentence versions, listed under disagreements |
| Summaries and compressed context stay out of the decision path, and no extraction service ships in this PR | ✓ | ✓ | ✓ | ✓ | ✓ | ScaleDown's extraction page calls offsets characters in one place and bytes in another, and caps each scalar field at 30 values ([ScaleDown extract](https://docs.scaledown.ai/api-reference/extract)) |
| omo's Goal iteration setting is not enforced in code in v4.19.4, v5.1.48 or dev, so the driver's cap is the only cap | ✓ | ✓ | ✓ | | ✓ | The Goal hook is byte-identical across those versions and has no counter ([v4.19.4 hook](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/packages/omo-opencode/src/hooks/goal/index.ts)). The dev docs say "the Goal hook doesn't enforce an iteration cap" ([omo features](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/features.md)) |

## Where models disagree

| Topic | GPT 6.1 Sol | Gemini 4 Argon | Claude Opus 5.5 | GLM 5.3 | Kimi K3 | Why they differ |
|---|---|---|---|---|---|---|
| Worker command line | Local binary from a lockfile-pinned 4.19.4 install, with an outside process-group watchdog | `bunx oh-my-openagent run` with the hooks disabled | Driver-owned `opencode serve`, attach per call, and poll for "idle with open todos" | `bunx oh-my-openagent run` with a session id | `timeout ... bunx oh-my-openagent@4.19.4 run`, then assert the version at startup | Different weight on supply-chain pinning and on hang detection. Claude Opus 5.5 alone traced that the wrapper waits forever on open todos |
| Outer iteration cap | 6 | 10, plus a 5 USD reserved spend cap | 10 | 12 | 10. Will not invent a dollar figure | Different assumptions about how many fix-verify cycles and reviews one goal needs. No member had data |
| Does a brake-only decision seat need the family rule? | Yes. Only a seat whose output can never reach an acting agent is exempt | Yes. Stopping a run counts as gating | Yes. Only log-only shadow is exempt | Yes. Only log-only shadow is exempt | No. A seat that can only stop or add a check is exempt, but must log its lineage | Different reading of risk: Kimi K3 weighs the cost of a wrong brake as low, the others count any effect on the run as authority |
| Validator rules in this PR | Add O19 and up now | Add O19 to O22 in the matrix validator now | A separate run-config validator, no matrix rules | One config-hygiene rule only | None now; runtime tests instead | Different views on testing rules for a seat that does not exist yet |
| A ScaleDown backend in this PR | No | Yes, shadow-only, sending state as text | No | No. Add a local constrained-decoding fallback instead | No | Gemini 4 Argon wants a second vendor to compare against. The others want one shadow fork so failures can be attributed |
| How many labels before activation | Not a count. 99 percent accepted-decision accuracy at 95 percent confidence | Held-out English and Chinese or Cantonese runs | Per backend, model version, question revision and locale | At least 100, including Chinese and Cantonese | At least 150, with a 90 percent upper bound on false-green of 0.05 | Different statistical framing of the same learn-then-test idea |
| The signable sentence for "endless" | "Continue autonomously within my approved finite budget until the goal is independently verified or the system reports an honest stopping reason; only I may renew that budget." | Loops unattended until checks and cross-family review pass, or a declared cap halts it as incomplete | "A standing service: it keeps taking goals, but each goal ends on verified evidence, a cap or a hand-back, and only I renew a cap." | "Unbounded in intent, bounded in budget" | "Persists until independent review confirms the goal is met, or until a hard cap or a human gate stops it" | Same content, different emphasis: owner control, unattended operation, or evidence |

## Unique discoveries

| Model | Unique finding | Why it matters |
|---|---|---|
| Claude Opus 5.5 | With the todo enforcer disabled, omo's run wrapper still refuses to exit while any todo is open, and its poll loop has no deadline ([completion.ts](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/packages/omo-opencode/src/cli/run/completion.ts)). The cap of 8 others cited belongs to a different edition ([omo commit](https://github.com/code-yeongyu/oh-my-openagent/commit/3a56234e33d5eab69bc55eea40e16cc79135316d)) | The council's own consensus command can hang. The prototype bounds it with a per-call timeout; an idle-with-open-todos poll is a follow-up |
| Kimi K3 | OpenCode falls back to the default agent when an `--agent` name is missing, rather than failing ([OpenCode run.ts](https://raw.githubusercontent.com/sst/opencode/v1.19.4/packages/opencode/src/cli/cmd/run.ts)). It also found the calibration audit | A silent fallback means the driver must check which agent actually ran. omo 4.19.4's run result does not name it, so the prototype reads the session through an export and refuses a batch it cannot verify |
| GPT 6.1 Sol | Profile switching breaks independence unless lineage is cumulative. The A01 case | It became the provenance ledger and the frozen-profile rule |
| Gemini 4 Argon | With a 30-value cap per field, 30 harmless warnings ahead of a fatal error would drop error 31 before the decision model saw it | A concrete reason to keep extracted fields out of the decision state unless each span is verified and counts are complete |
| GLM 5.3 | Citing the open-source rule against a hosted model misreads it. That rule covers harnesses and the verification stack, not inference models. Hosted decision models are out of ultimate for lack of reach and data-handling evidence | Keeps the exclusion on the right grounds, so it can be lifted with evidence |

## Comprehensive analysis

The strongest result is the one all five members reached on their own in round 1 and kept after cross-examination: the hypothesis that a System One model has no place in the six agentic patterns is false. Every pattern contains a fork with a small, fixed set of answers. A chain has a gate between steps, routing has a classifier (and Anthropic's article names a traditional classification model as an option for it), parallelization has a vote or a dedupe, orchestrator-workers has a choice of the next ready task, evaluator-optimizer has a verdict, and an autonomous agent has the question "is this still progressing". The members agreed just as firmly on the one place the hypothesis holds. The planner seat breaks down a task and synthesises results in prose, and a model that returns probabilities over options cannot do that. Five members on five families converging on this is the most reliable part of the debate, because each got there from different evidence: the article's own wording, the vendor's statement that the model writes no text, the repo's seat definitions and the outside studies.

The second strong result is about authority. In round 1, GLM 5.3 made a confident "goal complete" answer a required stop condition. By round 2 every member, GLM 5.3 included, held that the decision model may brake and never accelerate. The reasons stack. A typed answer can be schema-valid and still wrong, as in Chavan's constrained-decoding paper, where a 1B model scored 1.000 while writing an email body of "1. 2. 3. 4. 5." ([Chavan](https://arxiv.org/html/2609.23742)). Point thresholds break their promises most of the time, as in the Brom audit. And the one outside test of Jev in a security pipeline found 9 of 13 seeded vulnerabilities with it against 10 of 13 without ([pentest case study](https://arxiv.org/html/2609.28940v1)). A wrong brake costs a look from a person. A wrong "done" ships broken work.

The council also agreed that code, not omo, must own continuation, and that omo's own loops are weaker than they look. Four members checked the Goal hook and found no iteration counter in any inspected version. The documentation at 4.19.4 promised one that the code never had. This means the outer driver's caps are the only caps, and it is why each omo call is materialized as a single batch with the goal and todo hooks disabled.

The disagreements are mostly about calibration of numbers and scope, not direction. The iteration cap ranged from 6 to 12. Three members chose 10, and no member had data, so 10 is a starting value to be replaced by pilot evidence. The validator split was real: GPT 6.1 Sol and Gemini 4 Argon wanted matrix rules now, while Kimi K3 wanted none until a seat exists. Claude Opus 5.5's middle path, a separate validator for the run config, was adopted because it checks what the PR actually ships without inventing rules for a seat nobody has adopted. Gemini 4 Argon's ScaleDown backend lost four to one, on the grounds that one shadow fork is easier to interpret than two. The prototype's generic HTTP backend can still reach a Jev-shaped endpoint with text-encoded state if the owner wants that comparison later. Kimi K3's dissent on brake-only seats is the most interesting open point. A seat that can only stop a run does little harm when wrong, but a seat that can stop a run can also stall one forever, and a stall is a decision. The prototype follows the majority and records the dissent.

Two single-member findings changed the design. Claude Opus 5.5 traced that omo's run wrapper refuses to exit while a todo is open even with the todo enforcer disabled, which means the council's own preferred command can hang. Kimi K3 traced that OpenCode quietly falls back to the default agent when the requested one is missing. Both are now handled in the prototype: a per-call timeout bounds the first, and the second is caught by reading the session's agents and models through a session export, because omo's run result does not name them. Neither has been seen on a live install, and the first live run should confirm both.

On CDMs, the two things sharing the name were kept apart. Constrained decoding is a technique that guarantees format, not meaning. ScaleDown's task models are products whose extraction offsets are documented inconsistently and whose speed and cost figures come from the vendor. The LangChain drift breaker, which stops an agent when its classifier stops saying "progressing", is the brake-only use the council endorsed. Its 0.8 threshold is the post's choice and is not qualified ([LangChain](https://www.langchain.com/blog/building-long-running-agents-with-scaledown-and-deep-agents)).

The recommendation is to ship the superloop as a control plane in code with the decision model in shadow mode only. Workers are single omo batches under a frozen profile. Success means checks pass on the final tree and a reviewer from a family that never authored in the run finds no blocker. Caps are 10 iterations, 30 minutes, a no-progress streak of 2 and 3 fix-verify cycles, with the dollar budget set by the owner. A separate run-config validator enforces all of it. The pilot's purpose is to produce the labelled log a decision model must beat the rules baseline on, per locale, before it may brake anything. Jev stays shadow-only, because its base lineage is undisclosed and its Hong Kong reachability is unverified.

## What the PR adopted

| Question | Adopted | Where |
|---|---|---|
| D1 loop ownership | Code owns continuation. Local pinned omo binary with its version checked, goal and todo hooks disabled, per-call process-group timeout, the session's agents and models checked through a session export | [control.py](../../../scripts/superloop/control.py), [workers.py](../../../scripts/superloop/workers.py) |
| D2 omo target | 4.19.4 only. The driver's caps are the only caps | [SUPERLOOP.md](../../SUPERLOOP.md) |
| D3 decision seat family | Advisory mode needs a disclosed base family that shares nothing with any seat in the run. Shadow is exempt but logged. Kimi K3's brake-only exemption is recorded as a dissent and not adopted | Rule L6 in [validate-superloop.py](../../../scripts/validate-superloop.py) |
| D4 profile | Owner policy, frozen at admission. Cumulative lineage ledger, with `prior_lineage` for earlier segments | [ledger.py](../../../scripts/superloop/ledger.py) |
| D5 done authority | Smoke detector only | Question `goal_met` in [questions.json](../../../examples/superloop/questions.json) |
| D6 thresholds | Shadow labels only. Advisory needs a learn-then-test record on at least 100 labels per backend, model, question revision and locale | [qualify.py](../../../scripts/superloop/qualify.py) |
| D7 caps | 10 iterations, 30 minutes, no-progress streak 2, 3 fix-verify cycles. The budget is the owner's | [controller.example.json](../../../examples/superloop/controller.example.json) |
| D8 validator | A separate run-config validator now. No matrix rules until a decision seat is adopted | [validate-superloop.py](../../../scripts/validate-superloop.py) |
| D9 CDMs | No vendor backend, no extraction builder, no summaries. An offset-verified span contract | [state.py](../../../scripts/superloop/state.py) |
| D10 endless | The Explainer's standing-service sentence | [SUPERLOOP.md](../../SUPERLOOP.md) |
| D11 verdict | Disproved in all six patterns. Holds for the planner seat | [SUPERLOOP.md](../../SUPERLOOP.md) |

## Independent review

Grok 4.7 reviewed the driver after the council. It is on the xai family, sat outside the council, and differs from the author (Claude Opus 5.5). It was told to break the success path and wrote probes against the code. All three rounds ended REQUEST CHANGES. The reports are [round 1](superloop-council/review-round1-grok-4-7.md), [round 2](superloop-council/review-round2-grok-4-7.md) and [round 3](superloop-council/review-round3-grok-4-7.md). Every reproduction from all three rounds now has a regression scenario in `scripts/mm-superloop.py --self-test` or a mutation in `scripts/validate-superloop.py --self-test`. A self-test that passes shows these attacks fail; it does not show no other attack works.

### Round 1

| Finding (severity) | Change |
|---|---|
| Success compared the review's tree hash with itself, so a reviewer could edit the tree after the checks (blocker) | Reviewers run in a fresh folder. The tree is hashed again after the review, the run stops if it changed, and the checks run a second time before success |
| A findings file planted before the reviewer ran counted, and the reviewer's exit code was ignored (blocker) | The findings file is removed before the call, must be written during it, and the reviewer must exit 0 within its timeout |
| The hash and the diff skipped ignored files and the `.superloop` and `.omo` folders, and a worker could rewrite the omo config (blocker) | The hash includes ignored files and leaves out only the status file and the controller's omo config. The config is rewritten before each batch and a changed config stops the run |
| A controller could define a stamping reviewer and a `true` check (blocker) | Reviewers come from the owner's registry with pinned hashes, not the controller. Fake adapters work only in the self-test. The validator refuses no-op checks |
| The wall clock was checked only at the start of an iteration (blocker) | Checked before and after every check, before decisions, before and after the review, and before success. Each check gets a shrinking share |
| A missing review reservation counted as free (blocker) | Worker and review reservations must be above zero, a missing one stops the run, and a dual backend reserves two calls |
| Dropping `prior_lineage` or reusing an output directory reset the lineage (blocker) | A lineage registry outside the worktree, keyed by branch and goal, and a refusal to reuse an output directory |
| The no-progress stop came one batch late, and a defect that moved path dodged the cycle count (major) | The stop fires after exactly 2 idle batches. Three review rounds in a row with a blocker or major stop the run, whatever the paths |
| A lone major did not block success (major) | Any major blocks success, and open findings go into `final.json` |
| The reviewer conflict set missed the profile config's other families and runtime fallback (major) | The config is restricted to the cell's families with runtime fallback and team mode off, and every reported model family enters the ledger. Aggregation is code, so the aggregator seat is not used. The reviewer pointed out, correctly, that this is a decision to let the aggregator's family review, not a fix for independence |
| A missing agent report was accepted (major) | omo 4.19.4's run result does not name the agent, so the driver reads the session through an export and refuses a batch it cannot verify. The omo version is checked |
| Qualification records and the Hong Kong flag were controller fields (major) | Records are files from `qualify.py`, re-verified at admission. Ultimate admits only local or offline backends, with no flag |
| The catalog promised an approval ledger that did not exist (major) | The sentence now says there is no approval path, and the worker prompt forbids outward actions |
| An invalid findings file with a blocker was skipped (major) | An invalid findings file stops the run |
| atlas was not required, and command workers skipped the hook rules (major) | atlas and runtime-fallback are required, and the worker must be omo |
| Redaction missed common key shapes, the first decision state could crash, and the example goal left its unit tests unprotected (minor) | Wider patterns, the first state handled like the rest, and the example protects `tests` |

### Round 2

Round 2 closed most of round 1 and found new holes. Several rely on a worker running as the driver's own OS user, which led to a stated trust boundary as well as code changes. Round 3 showed that boundary was not enough on its own, as recorded below.

| Finding (severity) | Change |
|---|---|
| A worker overwrote the reviewer's findings file while the reviewer ran (blocker) | Findings are the JSON list on the reviewer's last output line, read through a pipe. No file counts |
| A pinned reviewer was replaced after admission (blocker) | Every pin is hashed again right before each call, and the resolved real path runs |
| A check passed on a file under `.git`, and the diff was empty (blocker) | Checks run on a fresh copy of the hashed tree, written from the stored blobs, never in the live worktree |
| A check read the status file through a split path (blocker) | Same copy: the status file is not in it |
| A clean filter showed the reviewer different bytes (blocker) | A filter or diff driver in the repository's own config was refused. Round 3 found this fix too narrow: replace refs and hooks in the same `.git` still took part. Round 3 replaced it |
| `test 1 -eq 1` and other tautologies passed as checks (blocker) | The checks run once on the admission tree, and the run is refused if every one already passes |
| A nested repository passed on unseen bytes, and an empty one crashed the driver (major) | Nested repositories and escaping symlinks are refused, and git errors end as `policy_denied` |
| Renaming the branch and the goal dropped the lineage (major) | The registry is keyed by repository only |
| Deleting the lineage registry gave an empty history (major) | The registry must exist; the owner creates it once, and a missing one stops the run. A same-user worker can still recreate it, which the docs now say |
| The agent check trusted an export command from the controller (major) | The omo command and the export command come from the tools registry with pins, re-hashed before each call |
| A pin on the interpreter alone was accepted (major) | Every absolute path in an argv must be pinned, and admission validates the registry |
| `mode` was read as an agent name, an agent-written `human` label verified, and the mtime check had slack (minor and nit) | `mode` is dropped, the owner pins qualification records and must read the dataset, and no findings file is used |

Not changed, and stated in the docs: a worker that runs as the owner's OS user can defeat any file-based record, rotating failing checks can dodge the fix-verify count until the iteration cap, and a small window remains between hashing a pin and starting the process.

### Round 3

Round 3 confirmed every replayed round 2 forgery closed, and found three more that returned success with `isolation: container` and a worker that wrote only inside its worktree. So the stated boundary did not hold, and the round 2 claim that checks and review used the stored blobs was false while git honoured the worker's replace refs.

| Finding (severity) | Change |
|---|---|
| A replace ref under `.git/refs/replace` made git show the reviewer and the checks a different blob (blocker) | The driver no longer runs git in the worker's repository. It keeps its own object store in the run folder and reads the worktree as plain files, with system and global config, hooks, replace objects and attributes all off. The repository-filter refusal is gone because the worker's config is never read |
| A `post-index-change` hook in the worktree ran as the driver during hashing and rewrote the snapshot and the diff (blocker) | Same change: the driver's store has no hooks and points `core.hooksPath` at an empty folder |
| A check read the live `.git` by absolute path, or found the worktree through `/proc` (blocker) | Checks get an environment built from nothing. With `check_jail: bwrap` each check runs under bubblewrap and sees only its snapshot. `final.json` sets `protected` only for an isolated worker with jailed checks. Checks that start passing on the tree that failed them at admission are refused, jail or not |
| A binary file in the diff crashed the driver before `final.json` (major) | The diff stays bytes, and any unexpected error ends in `final.json` as `policy_denied` |
| Pointing `.git` at a new directory gave the next run a fresh lineage key (major) | The controller names the repository. The registry binds that name to one git directory and refuses a run where it differs. A `.git` moved during a batch stops the run |
| The documented `--out runs/RUN_ID` inside the worktree could never succeed (major) | An output folder inside the worktree is refused, and the docs put it under `~/.local/state/model-mesh/runs/` |
| The trust boundary paragraph overclaimed (docs) | Rewritten: it names the two conditions, worker isolation and the check jail, and what `protected: false` does and does not say |

Grok's probes, rerun on the new code: the hook case ends `no_progress` and the hook never ran; the replace-ref case ends `policy_denied`, but only because the probe's own `git replace` fails on the second batch, so the self-test carries the clean version, which ends `no_progress`; the absolute-path and `/proc` checks end `no_progress` under `bwrap` and still succeed under `none` with `protected: false`; the moved `.git` and the inside output folder are refused. The pin race and a same-user worker remain open, as before. These round 3 fixes have not been re-reviewed.
