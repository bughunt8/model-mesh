---
name: mm-superloop
description: Run a long goal as a bounded outer loop of omo worker batches, with code owning continuation, a typed decision model answering logged questions in shadow mode, and success only on passing checks plus a cross-family review of the same tree. Use when a goal needs many worker batches and the owner can state machine-checkable acceptance checks. Do not use for one-batch tasks; use mm-loop instead.
---

# mm-superloop

This skill runs `scripts/mm-superloop.py`, the outer loop described in [docs/SUPERLOOP.md](../../docs/SUPERLOOP.md). Read that page once before the first run. The mm-method rules still govern the work inside each batch; this skill only says how the batches are driven and stopped.

## When to use it

Use it when all of these hold:

- The goal needs more than one worker batch, for example a feature with tests across several modules.
- The owner can write acceptance checks as commands that exit 0 on success. "Looks good" is not a check.
- The situation, A01 to A12, has an author seat on OpenCode with omo under the chosen profile and option. Admission refuses the run otherwise.

Do not use it for a task that fits one batch (use mm-loop), for work with no machine-checkable acceptance, or for anything that sends, publishes, pays, deletes or changes permissions. Those need a person at each step.

## The rule that decides everything

The decision model may brake. It may never accelerate. It can pause the run for a person, stop it for no progress, or add review seats. It can never end the run as a success, skip a check, change the profile or approve an action. Code enforces this, and `scripts/validate-superloop.py` rejects any question catalog that grants more.

A worker saying "done" is a claim, not a fact. Its status file lands under `claims` and is marked untrusted. Only a "blocked" claim is used, because that can only stop the run.

## Steps

1. **Write the goal file with the owner.** Start from `examples/superloop/goal.example.json`. Fill in `id`, `objective`, `situation`, `profile`, `option` and at least one acceptance check. Each check is an argv list, never a shell string, with a timeout and a one-line description. You may draft the checks; the owner approves them, because the loop trusts them. List every test and fixture path the checks run under `protected_paths`, so a worker that edits its own tests stops the run. If an earlier run or another profile already authored part of this work, list those harnesses and families under `prior_lineage`; the lineage registry also adds earlier runs on the same branch or goal.
2. **Pick the controller.** Use `examples/superloop/controller.rules.example.json` for an offline run with the rules baseline only. Use `examples/superloop/controller.example.json` for a shadow pilot that also logs a remote decision model's answers. Keep `mode` as `shadow` unless a qualification record exists for every question that would act (see Modes below). Leave the caps at their defaults unless the owner sets others: 10 iterations, 30 minutes, a no-progress streak of 2 and 3 fix-verify cycles. The budget is the owner's number, and every reservation the run will use must be set above zero. The worker and each reviewer are a `ref` into the owner's tools registry (`~/.config/model-mesh/superloop-tools.json`, template in `examples/superloop/tools.example.json`), which holds the argv and pinned hashes. Do not write or edit that registry yourself; ask the owner. Set `worker.isolation` to what is true: `separate_user`, `container` or `none`. The guarantees below assume the worker cannot write outside its worktree; with `none`, say so next to any result.
3. **Validate.** Run `python scripts/validate-superloop.py GOAL CONTROLLER`. Fix every error before going on. Do not loosen a rule to make it pass. The owner creates the lineage registry once with `python scripts/mm-superloop.py --init-registry`; a run refuses to start without it. At least one acceptance check must fail before the work, or the run is refused.
4. **Prepare the worktree.** Use a clean git worktree on its own branch. The control plane writes `.omo/omo.jsonc` there, keeps only the models whose family belongs to the cell's authors and orchestrator, and disables the goal hook, the todo continuation enforcer, start-work, atlas, runtime fallback and team mode, so each call is a single batch. It rewrites the file before every batch and stops the run if a worker changed it.
5. **Run.** `python scripts/mm-superloop.py --goal GOAL --controller CONTROLLER --worktree PATH --out runs/RUN_ID`, with a new `RUN_ID` every time; a used output directory is refused. Exit code 0 means success, 2 means an honest stop, and 3 means the run was refused.
6. **Read the result.** `runs/RUN_ID/final.json` has the terminal status, the reason, reserved spend, the decision count, how often the decision model and the rules baseline disagreed, the lineage and any open blocker or major findings. `events.jsonl` is hash-chained, one event per line.
7. **Hand back.** Report the terminal status in plain words with the evidence: which checks pass, which review found what, and what the owner must do next. On `verified_pending_owner`, the owner reviews and merges. Nothing is merged or pushed by the loop.

## Terminal states and what to tell the owner

| Status | Meaning | Next step |
|---|---|---|
| `verified_pending_owner` | Every check passes on the final tree, a cross-family review of that tree found no blocker and no major finding, the tree did not change during the review, and the checks passed again | Owner reviews the branch |
| `no_progress` | Two batches in a row left the tree and the failing checks unchanged | Say which checks still fail. Ask the owner whether the goal or the checks need changing |
| `fix_cycles_exhausted` | Three batches with the same failing checks, or three reviews in a row with a blocker or major | Same as no progress, with the failing evidence and the open findings |
| `blocked_human` | A worker or a qualified brake reported a need for a person | Name what is needed: a credential, a decision, an approval |
| `review_unavailable` | No reviewer is left whose harness and families never authored in this run, or the reviewer failed, timed out or printed no valid findings list | Ask the owner for a reviewer from an unused family, or report the reviewer failure |
| `cap_iterations`, `cap_wall_clock`, `cap_budget` | A cap ran out | Report progress so far. Only the owner renews a cap |
| `policy_denied` | Admission refused the run, or a batch broke a rule: the omo config changed, a pinned tool no longer matched, the session's agent or model could not be read or was outside the cell, a nested repository, an escaping symlink or a repository-level git filter appeared, or the worktree changed during a review | Quote the reason. Do not work around it |
| `worker_failure`, `cancelled` | The worker failed or the stop file was set | Report and stop |

A cap running out is never success. Do not raise a cap, reset the lineage or start a fresh run to get around a stop. A new run on the same work lists the earlier authors under `prior_lineage`.

## Modes

- `shadow` is the default. The decision model's answers are logged next to the rules baseline and change nothing. The ultimate profile admits only local or offline decision backends, because shadow calls send the state.
- `advisory` lets a qualified brake act. It needs a base family for the decision model on the known family list that shares nothing with any seat in the run, and a qualification record per acting question for that backend, pinned model, question revision and locale. A record is a file from `scripts/superloop/qualify.py`, run on at least 100 decisions from model-mesh's own runs labelled by people or ground truth; the driver re-checks the dataset hash and re-runs the procedure at admission. A point threshold such as 0.8 from a vendor post is a label, not a qualification.
- There is no control mode.

## Rules you must not break

- Never treat a worker's report, a decision model's "goal met" answer or a schema-valid response as evidence of success. Success is checks plus review, computed by code.
- Never switch the profile or option mid-run. The assignment is frozen at admission.
- Never pick a reviewer whose harness or any family appears in the lineage, including fallback rungs and earlier segments.
- Never put a summary or compressed context into the decision state. Extracted spans enter only when the text at the stated offsets of the original file matches.
- Never put a key in a goal, a controller or a prompt. The controller names an environment variable; the control plane redacts key-like strings from the state.
- Never run omo's own continuation loops inside the superloop. One batch per call.
- Never edit `.omo/omo.jsonc`, the tools registry or the lineage registry. The run stops or loses its independence if you do.

## Known gaps

- The live omo path is untested. In 4.19.4 the run result does not name the agent or model, so the driver reads them from `opencode export <sessionId>`; that format was not checked live. The first live run is a dry run: record the effective config, the export, the agent that actually ran and the exit behavior.
- With the todo enforcer disabled, a worker that stops with open todos waits until the per-call timeout.
- No decision model is qualified or adopted. The pilot produces the labelled log that one must beat the rules baseline on.
