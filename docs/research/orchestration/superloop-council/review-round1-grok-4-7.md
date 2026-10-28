REQUEST CHANGES

I would not merge this. The success flag is the product, and a worker, a reviewer, or the goal author can forge it. Official checks pass. They never attempt these paths.

Reviewed `superloop/system-one-control-plane` at `20c61c2`, two commits on `daf9ac4`. I did not edit the repo. Reproducing command:

`python3 /home/user/workspace/s1-superloop/grok-probe/break_superloop.py`

Output is in `/home/user/workspace/s1-superloop/grok-probe/probe_output.txt`.

## Reproduced

### Blocker. Success does not look at the tree after review.

`scripts/superloop/control.py:369` hashes the tree. `scripts/superloop/control.py:421` then calls review. Review stores that same hash at `scripts/superloop/control.py:323` and returns it. The success test at `scripts/superloop/control.py:435` compares the two. It cannot fail.

The reviewer runs in the worktree. `scripts/superloop/workers.py:122` sets cwd to the worktree. The example reviewer sets `GOOSE_MODE` to `approve` at `examples/superloop/controller.example.json:20`, so the shipped command is allowed to edit.

Probe, reviewer deletes `a.txt` after the checks and writes `[]`. Result: `status=verified_pending_owner success=True iterations=1`. `a.txt` was gone. The acceptance command then exited 1.

The same path through `scripts/mm-superloop.py` exited 0. Validator errors were empty. Recheck exited 1.

Smallest fix: hash again after review. If the hash changed, run the checks again. Refuse success if they fail or if the hash is not the one just reviewed. A read-only reviewer mount would help. It is not a substitute for the recheck.

### Blocker. A findings file written before the reviewer runs is enough.

`scripts/superloop/control.py:308` runs the reviewer and then ignores `exit_code` and `timed_out`. `scripts/superloop/control.py:312` loads `findings-NNN-harness.json` without truncating it first.

Probe, worker plants `[]`, reviewer returns exit 2 and `timed_out` true and does not write. Result: `success=True`, `reviewer ran=['goose']`.

CLI, worker plants the file, reviewer command exits 2 and writes nothing, validator errors empty, process exit 0, `success` true, planted file still present.

Smallest fix: delete the findings path before the call. Require exit 0 and not timed out. Reject a file whose mtime is before the call.

### Blocker. The hash and the diff are not the worktree.

`scripts/superloop/control.py:56` and `scripts/superloop/control.py:62` run `git add -A` with excludes for `.superloop` and `.omo`. Git also skips ignored files. The comment says this is the full working tree. `docs/SUPERLOOP.md:64` says the control plane hashes the whole tree.

Probe, acceptance check reads `.superloop/win`. The review diff was 0 bytes and did not contain `win`. Result: `success=True`.

Probe, worker writes `secret.local` and gitignores it. The file existed. The diff did not contain the payload. Result: `success=True`.

Probe, worker rewrites `<worktree>/.omo/omo.jsonc` on batch 1. Setup had `disabled_hooks` `atlas`, `goal`, `start-work`, `todo-continuation-enforcer` and `goal.enabled` false. Batch 2 saw `disabled_hooks` empty and `goal.enabled` true. Result: `success=True` at iteration 2. `.omo` is not a protected path, so this is not `blocked_human`.

The file the control plane itself wrote also had `runtime_fallback.enabled` true and `team_mode.enabled` true. Those come from `scripts/materialize.py:17` and `scripts/materialize.py:24`. Materialize runs once, in setup at `scripts/superloop/control.py:224`.

I did not load that tampered file in a live omo process. The next omo batch would. The control plane did not notice.

Smallest fix: re-materialize `.omo/omo.jsonc` at the start of every iteration and treat that file as protected. Hash with a walk that includes ignored files, or `git add -A -f`, and do not exclude `.superloop` from the review diff except the status file the controller owns. Refuse a check whose path sits under an excluded directory.

### Blocker. The validator admits a reviewer that stamps an empty list.

L9 at `scripts/validate-superloop.py:196` allows `kind` `command` or `fake`. A command only needs a non-empty argv. L2 at `scripts/validate-superloop.py:115` accepts acceptance argv `["true"]`. `scripts/superloop/control.py:235` matches the harness name and does not look at the process.

`skills/mm-superloop/SKILL.md:28` tells the agent to write the goal. The next step tells it to pick the controller. The same author can supply both.

CLI, acceptance argv `true`, reviewer argv writes `[]`, harness name `goose` so it matches the A02 hybrid primary seat. Validator errors empty. `scripts/mm-superloop.py` exited 0 with `success` true.

A harness-name match is not an independent review.

Smallest fix: the controller must not supply reviewer argv. Pin the reviewer to a binary recorded outside the agent-written files, and refuse success until that process created the findings file. Reject `kind: fake` outside the self-test.

### Blocker. The wall clock can expire and the run can still succeed.

`scripts/superloop/control.py:343` checks the clock at iteration start. After the worker, `scripts/superloop/control.py:366` passes the max of 1.0 and remaining into the checks, so a negative remaining still runs them. `scripts/superloop/control.py:107` gives every check that same remaining, not a shrinking remainder. `scripts/superloop/control.py:308` gives the reviewer `per_call_seconds`, not remaining.

`docs/SUPERLOOP.md:85` says running out of a cap never counts as success.

Probe, injected clock jumps to 2825 inside the worker. Start was 1000. Cap is 1800. Facts event had `remaining_fraction=0.0`. Result: `success=True`.

Contrast, clock already past the cap at the iteration check: `cap_wall_clock`, iterations 0, `success=False`.

Probe, remaining was 40 seconds when checks started. Both checks were invoked with timeout 40. The reviewer was invoked with timeout 600. Result: `success=True`. If those checks had used their timeouts, the wall would have been exceeded before review finished, and review would still have been allowed 600 seconds.

`decide.ask` uses `time.time` at `scripts/superloop/decide.py:323`. `HttpBackend` sleeps on retries at `scripts/superloop/decide.py:265`. Neither uses the injected clock. I did not run a live retry. The call site is already outside the remaining check.

The self-test clock at `scripts/mm-superloop.py:183` adds 400 seconds on every call, so it trips at the iteration boundary. It does not jump the clock inside a worker that has already made the tree green.

Smallest fix: re-check remaining before the checks, before each check, before `ask`, and before review. Pass a shrinking remainder. If it is already spent, finish `cap_wall_clock` instead of success.

### Blocker. A missing review reservation is treated as zero, and that yields success.

`reserve` at `scripts/superloop/control.py:173` uses 0 when the kind is missing. L10 at `scripts/validate-superloop.py:204` only requires `worker_call` above zero. The rule text at `scripts/validate-superloop.py:28` says missing usage is not zero cost. `docs/SUPERLOOP.md:83` says the same.

Probe, `review_call` omitted, `budget_usd` 0.4, `worker_call` 0.4, checks green, review writes `[]`. Result: `success=True`, `reserved_usd=0.4`.

Same budget with `review_call` 0.15: `cap_budget`, `success=False`.

Validator, `review_call` omitted or set to 0: no L10 error.

Smallest fix: require a positive `review_call` and `decision_call` whenever that call can happen. A dual backend should reserve twice. I did not run dual. `ask` reserves `decision_call` once at `scripts/superloop/control.py:250` and then lets the dual backend make two HTTP calls.

### Blocker. Omitting prior_lineage lets a conflicting reviewer succeed.

With `prior_lineage` naming the reviewer harness and family, the run stopped `review_unavailable`. Without that field, the same reviewer returned `success=True`.

`scripts/superloop/ledger.py:18` truncates `events.jsonl` on every new `Run`. A second run in the same out dir replaced a `review_unavailable` terminal with `verified_pending_owner`.

`docs/SUPERLOOP.md:83` and `docs/SUPERLOOP.md:106` say resuming never resets the lineage and that earlier segments are in the ledger. `skills/mm-superloop/SKILL.md:49` says a new run lists earlier authors. Nothing enforces that. The agent that writes the goal can omit the field.

Smallest fix: refuse to reuse an out dir that already has a ledger, and append instead of truncating. If a previous ledger or the worktree HEAD shows a harness or family that is not in `prior_lineage`, refuse admission.

### Major. The no-progress cap is one batch late, and a moved defect walks past both progress caps.

`streak` starts at 0 at `scripts/superloop/control.py:334`. It increments only when the fingerprint matches, at `scripts/superloop/control.py:373`. The stop at `scripts/superloop/control.py:406` waits for `streak >= 2`. The message uses `streak + 1`, so it says 3 batches.

`docs/SUPERLOOP.md:78` says 2 batches with the same tree and the same failing checks. `skills/mm-superloop/SKILL.md:41` says two batches.

Probe, empty worker, cap 2. Result: `no_progress`, iterations 3, detail `same tree and failing checks for 3 batches`.

The official self-test names this case "no progress for two batches" and still passes. Its own detail string says 3 batches. `scripts/mm-superloop.py:177` checks the status only.

A new file each batch resets the streak. The failing set stayed `a,b`, so fix-verify still stopped at iteration 3 with `fix_cycles_exhausted`. That cap works for a stable failing set. It does not save the no-progress claim.

A blocker whose path changes each batch, plus a tree change, reached `cap_iterations` at 6. Caps were 6 iterations, fix-verify 3, no-progress 2. Neither progress cap fired. The finding key at `scripts/superloop/control.py:440` is path plus category, so moving the defect resets it.

Smallest fix: stop when the number of identical batches reaches the cap, and say that number. Do not reset the streak on a hash change that leaves the failing checks the same. Key fix-verify on the defect, not only the path.

### Major. A single-seat major does not block, and the default path has one seat.

`scripts/superloop/control.py:296` keeps one reviewer unless a brake or the smoke detector asks for all seats. `scripts/aggregate-findings.py:121` marks corroborated only when two families reported the cluster. Success at `scripts/superloop/control.py:435` requires no blocker and no corroborated major. One major cannot meet that bar.

The review event drops `open` at `scripts/superloop/control.py:426`. `final.json` stores the harness name, not the findings. The detail string says "no blocker" and drops the major.

Probe, one valid major: `success=True`. Probe, one valid blocker: `cap_iterations`, `success=False`.

`docs/SUPERLOOP.md:70` asks for no corroborated major. The letter is met. The extra gate is dead on the default path. `docs/REVIEW-PANEL.md:112` already says gates stop on blockers, so I am not calling this a spec contradiction. I am calling it a hole in the thing the owner is shown.

Smallest fix: a major from the only seat blocks success, or run every independent seat before success. Put open majors in `final.json`.

### Major. The reviewer conflict set is not the set the docs describe.

`admit` at `scripts/superloop/control.py:201` records the orchestrator, authors, and `prior_lineage`. Category routes are authors, because `scripts/superloop/assign.py:41` appends them. Matrix fallback rungs are included. I pointed the reviewer chain at the author's last rung and got `review_unavailable`.

The aggregator is not recorded. `conflicts` at `scripts/superloop/ledger.py:50` cannot see it. The decision-seat check at `scripts/superloop/control.py:214` does include aggregator families. Reviewer selection does not.

Shipped A02 hybrid primary: reviewer `goose` / `deepseek`, aggregator `goose` / `deepseek`. Provenance after a success was harness `opencode-omo` and families `alibaba`, `minimax`, `moonshot`, `zai`. The reviewer was used. The driver never calls the aggregator seat. It clusters in process. A ban on sharing the aggregator family would make this row `review_unavailable`. Say that in the docs, or record the aggregator and refuse the overlap. Do not claim the ledger already does it.

`profiles/hybrid.example.json` fallback models include family `deepseek`. That family is the reviewer family. It is not in provenance. The written config leaves `runtime_fallback.enabled` true, and the control plane does not add hook `runtime-fallback` to `disabled_hooks`. At v4.19.4 that hook is created when the runtime-fallback hook is enabled, in [create-session-hooks.ts](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/packages/omo-opencode/src/plugin/hooks/create-session-hooks.ts).

The reported model is not added to provenance. `scripts/superloop/control.py:362` only compares `expect_agents`, and only if a report exists.

Smallest fix: record every model family in the materialized config, disable `runtime-fallback` or intersect it with the matrix chain, and add the reported model family before review.

### Major. A missing agent report is not a refusal.

`scripts/superloop/workers.py:75` keeps the first `agent` or `agentName` key. `scripts/superloop/control.py:362` skips the check when `agent` is missing. L8 at `scripts/validate-superloop.py:183` does not require `expect_agents`. `pinned_version` is a string. Nothing compares it to the binary.

Probe, `expect_agents` set to `sisyphus`, worker reports no agent, checks pass, review writes `[]`. Result: `success=True`.

Probe, worker reports `hephaestus`. Result: `policy_denied`. That half works.

`parse_json_output` on a document whose first agent key is `hephaestus` and whose nested `agentName` is `sisyphus` returned `hephaestus`.

`docs/SUPERLOOP.md:119` says the control plane checks the agent the JSON output reports and refuses a mismatch. A missing report is not treated as a mismatch. `docs/research/orchestration/SUPERLOOP-COUNCIL.md:54` says the prototype checks the agent the JSON output reports. Same overclaim.

Smallest fix: require `expect_agents` for an omo worker, refuse a missing or mismatched report, and check the binary version at startup.

### Major. Qualification and the Hong Kong flag are fields the controller sets.

`qualified_threshold` at `scripts/superloop/control.py:140` matches model, question id, revision, locale, and a non-null threshold. It does not call `qualify.py`. L6 at `scripts/validate-superloop.py:166` checks that the method string is `learn-then-test-fixed-sequence`, `labelled` is at least 100, and the threshold is above 0 and at most 1. No dataset is read.

Probe, advisory, `labelled` 100, threshold 0.01, no dataset. Validator errors empty. Replay answered `blocked` at 0.02. Result: `blocked_human`, brake `pause_human`. That does not grant success. It does let a made-up record act.

L6 also accepts `base_family` `none` and `made-up-family`. It only rejects a missing family, `undisclosed`, and `unknown`.

L7 at `scripts/validate-superloop.py:180` checks a boolean. Ultimate profile, `https://127.0.0.1`, model id `stable-model`, `hk_reachable_verified` true: no L5 or L7 error. The alias regex at `scripts/validate-superloop.py:48` matches `latest` and does not match `stable`.

`docs/SUPERLOOP.md:95` says a remote endpoint must be verified as Hong Kong reachable. `docs/SUPERLOOP.md:100` says a threshold acts only through a record made by `qualify.py`. `skills/mm-superloop/SKILL.md:53` says the same. The code checks a JSON object.

I did not open the cited paper, so I am not treating "147 of 190" as a finding.

Smallest fix: require a qualification file produced by `qualify.py`, with a hash of the labelled set and the computed threshold. Do not trust a controller boolean for Hong Kong reachability. Reject `stable` and `default` the same way as `latest`.

### Major. The catalog says code requires an approval. There is no approval ledger.

`examples/superloop/questions.json:82` says code still requires a recorded approval for an irreversible change, a disclosure, a payment, or a permission change. `scripts/superloop/decide.py:192` returns true only for `touches_protected` or `outward_action`. The driver never sets `outward_action`. Nothing records an approval.

Smallest fix: delete the sentence, or add an approval record the driver checks before any outward action. A skill note is not that check.

### Major. An invalid blocker is dropped, and the next empty file can succeed.

`scripts/aggregate-findings.py:73` rejects unknown keys. `scripts/superloop/control.py:427` counts that as an invalid review and continues. Two invalid files stop the run. One invalid file does not.

Probe, iteration 1 writes a blocker plus a `note` field. The log says `unknown keys ['note']`. Iteration 2 writes `[]`. Result: `success=True`.

A valid blocker on the same seat does not succeed. The extra key is what lets the blocker disappear.

Smallest fix: an invalid findings file ends the run as `review_unavailable`. Do not continue into a later success. If the JSON contains a blocker even with an extra key, still treat it as a blocker.

### Major. L8 does not require atlas, and a command worker skips the hook rules.

`REQUIRED_HOOKS` at `scripts/validate-superloop.py:47` is `goal`, `todo-continuation-enforcer`, and `start-work`. An omo controller that omits `atlas` produced no L8 error.

`docs/SUPERLOOP.md:118` and `skills/mm-superloop/SKILL.md:31` say atlas is disabled. The example includes it. The validator does not.

`scripts/validate-superloop.py:194` applies the hook rules only when `kind` is `omo`. A `command` worker is admitted with no hook disable. The per-call timeout still bounds that one process. It does not make the process one batch.

Smallest fix: add `atlas` to `REQUIRED_HOOKS`. Apply the hook rules to every worker kind, or reject `command` workers in a run that claims one omo batch.

### Minor. Redaction misses common key shapes.

`scripts/superloop/state.py:20` catches `sk-` and `ghp_`. Probe: `sk_live_abcdefghijkl`, `xoxb-1234567890-abcdefgh`, `github_pat_11AAAAAAabcdefghijklmnopqrstuvwxyz`, and `AIzaSyA1234567890abcdef` came back unchanged. `docs/SUPERLOOP.md:111` says strings that look like keys are redacted.

Smallest fix: add those prefixes, and a JWT shape, and test them.

### Minor. The token-budget failure is not one behavior.

`scripts/superloop/state.py:93` raises if required facts do not fit. The loop catches that at `scripts/superloop/control.py:393`, logs `decision_skipped`, and can still succeed. Probe, budget 80 tokens: `decision_skipped` with `required facts do not fit the decision budget`, then `success=True`.

The first build, at `scripts/superloop/control.py:349`, is not in that try. Probe, budget 1 token: uncaught `ValueError`, no terminal status.

`docs/SUPERLOOP.md:111` says every answer becomes an abstention. The loop path abstains and then succeeds if checks and review are green. The startup path crashes.

Neither call passes spans. Offset checks exist in `scripts/superloop/state.py` and are unused by the driver.

Smallest fix: catch the first build too, and finish `policy_denied` or a dedicated budget status instead of continuing to success. Pass spans in, or delete the claim that the loop admits them.

### Minor. The example goal does not protect the tests its own check runs.

`examples/superloop/goal.example.json:8` runs pytest on `tests/unit`. `examples/superloop/goal.example.json:12` protects `tests/integration` and `scripts/check_rate_limit.py`. A worker can edit `tests/unit` and the unit check can go green. An honest reviewer might see it. A stamp will not.

Smallest fix: protect `tests/unit`.

### Nit. Two passages are speeches.

`docs/SUPERLOOP.md:9` opens with a railway. It does not change the rules. `docs/research/orchestration/SUPERLOOP-COUNCIL.md:46` is a paragraph of synthesis that restates the table above it. Cut both if you touch the docs.

I scanned the new superloop docs, the skill, `TESTING.md`, the council, `SYSTEM-ONE.md`, and `questions.json` for em dashes, en dashes, and curly quotes. None. The em dashes in `CHANGELOG.md` are in older entries, not in the 1.4.0 notes. Do not treat that as a style pass. The claims above are the problem.

## Suspected, not executed

`team_mode.enabled` true in the written config may start agents outside the recorded seats. I saw the flag. I did not run omo.

`disabled_commands` is not set. Hook creation for `goal`, `start-work`, `atlas`, and `todo-continuation-enforcer` is gated on `isHookEnabled` in the v4.19.4 sources I read: [create-session-hooks.ts](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/packages/omo-opencode/src/plugin/hooks/create-session-hooks.ts) and [create-continuation-hooks.ts](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/packages/omo-opencode/src/plugin/hooks/create-continuation-hooks.ts). I did not trace slash commands to a refusal. They may still be invocable.

The goal hook sources at v4.19.4 have no iteration counter. I read [index.ts](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/packages/omo-opencode/src/hooks/goal/index.ts), plus `controller.ts`, `types.ts`, `prompt.ts`, and `store.ts` in that directory. No `iteration` string. I did not run the plugin. The repo already says the live path is untested, at `docs/SUPERLOOP.md:121` and `TESTING.md:29`. That disclosure is accurate. It does not cover the success forgeries above.

The example goose argv is marked unverified at `examples/superloop/controller.example.json:4`. That note is honest. The bug is that any argv is admitted, which is the stamp blocker above.

## Not bugs, because I tried them and they held

A replayed `goal_met` of 0.99 with failing checks ended `no_progress`, not success.

A worker status file of `done` did not succeed. Only `blocked` stops the run, at `scripts/superloop/control.py:402`.

A clock already past the cap at iteration start ended `cap_wall_clock`.

A reviewer family set to an author fallback rung ended `review_unavailable`.

A reported agent outside `expect_agents` ended `policy_denied`.

A priced `review_call` under a budget that only covers the worker ended `cap_budget`.

An empty acceptance list cannot go green, because `scripts/superloop/control.py:413` requires at least one check. I did not need a run for that line.

Mode `control` and a brake effect `succeed` are rejected by the existing self-test. I did not re-break those.

Iteration counting uses `it > max_iterations` at `scripts/superloop/control.py:341`. A cap of N runs N iterations. That one is not late.

## Checks I ran

`python3 .github/checks.py` exited 0. All checks passed.

`python3 scripts/check-drift.py` exited 0. No drift detected.

`python3 scripts/validate-superloop.py --self-test` exited 0. 27 mutations, as `TESTING.md:15` and the 1.4.0 changelog say.

`python3 scripts/mm-superloop.py --self-test` exited 0. 26 scenarios and 16 unit checks, as `TESTING.md:16` says. Passing that file does not disprove the findings. The no-progress scenario does not check the iteration count. The wall-clock scenario trips before a green review.

## What I would fix before another review

Rehash and recheck after review. Refuse a findings file the reviewer did not just write. Hash the worktree the checks actually read, and rewrite `.omo/omo.jsonc` every batch. Stop treating a controller argv as an independent reviewer. Re-check the wall clock and charge a review even when the controller forgot the reservation. Refuse a second run that drops lineage. Until those hold, a green self-test is not evidence of success.
