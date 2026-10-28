REQUEST CHANGES

The round 1 forgeries I re-ran are mostly shut. The success bit is still forgeable. A worker on the same user as the driver can erase a blocker, replace a pinned reviewer after the hash check, or satisfy a check with bytes the review diff never contains. I would not ship this.

Command for the runs below: `python3 /home/user/workspace/s1-superloop/grok-probe/round2_break.py`. Full log: `/home/user/workspace/s1-superloop/grok-probe/round2_output.txt`. Fakes were passed only as `deps` with `allow_fakes` true, except the stub omo case, which set `allow_fakes` false. Reported worker shapes used `agents` and `models`.

## Round 1 findings

1. CLOSED. A reviewer that deletes `a.txt` during the review no longer succeeds. Status `policy_denied`, success false, detail `the worktree changed during the review`. The file was gone after the run. The post-review hash at `scripts/superloop/control.py:536` and the recheck at `scripts/superloop/control.py:659` hold for this case.

2. CLOSED for the old plant and the ignored exit code. A reviewer that exits 2 and writes nothing is `review_unavailable`, not success. The fresh review directory plus the remove at `scripts/superloop/control.py:509` kills a file planted before the call. A file written during the call by someone other than the reviewer is a new hole. See the first new blocker.

3. PARTLY. An ignored `secret.local` now appears in the diff, payload included. A worker rewrite of `.omo/omo.jsonc` is `policy_denied`. The written config has `goal.enabled` false, `runtime_fallback.enabled` false, `team_mode.enabled` false, the five required hooks, and `disabled_commands` of `goal` and `start-work`. Those keys match the 4.19.4 schema and the hook gates I checked. See the [omo schema](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/v4.19.4/assets/omo.schema.json), the [session hooks](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/v4.19.4/packages/omo-opencode/src/plugin/hooks/create-session-hooks.ts), and the [continuation hooks](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/v4.19.4/packages/omo-opencode/src/plugin/hooks/create-continuation-hooks.ts). The hash still does not cover the bytes a check can read. `.git`, a clean filter, and a committed nested git directory all returned success. The council sentence that the hash leaves out only the status file and the omo config is false. `docs/SUPERLOOP.md:67` and `docs/research/orchestration/SUPERLOOP-COUNCIL.md:84`.

4. PARTLY. A controller `argv` of `true` is refused at admission. A reviewer `argv` in the controller is refused. Fake adapters without `allow_fakes` are refused. `test 1 -eq 1` and `/usr/bin/env true` are admitted and both succeeded on an empty diff. `sh -c true;` is admitted. I did not run that third spelling. The denylist at `scripts/validate-superloop.py:166` only matches a few exact texts.

5. CLOSED. A clock jump inside the worker to 2000 seconds past the start is `cap_wall_clock` during the checks, not success. `scripts/superloop/control.py:397` and `scripts/superloop/control.py:666`.

6. CLOSED. Dropping `review_call` is `policy_denied` at admission, L10. `scripts/superloop/control.py:261` returns false for a missing reservation, so a bypass of the validator still would not treat it as free.

7. PARTLY. Omitting `prior_lineage` on the same branch, and a new goal id on that same branch, both refuse the reviewer that an earlier run recorded. A reused output directory is `policy_denied`. A renamed branch plus a new goal id succeeds with that same reviewer. Deleting the registry file and starting again also succeeds. `docs/SUPERLOOP.md:88` says the lineage is never reset. The code resets it.

8. CLOSED for the off by one and for a finding that moves path. Two idle batches stop: status `no_progress` at iteration 2, detail says 2 batches. Three reviews in a row with a major, on a tree that changes every batch, stop as `fix_cycles_exhausted`. I did not re-run a rotation of failing check names. The cycle key is still the failing set at `scripts/superloop/control.py:603`. That residual is suspected, not re-proven.

9. CLOSED. A lone major does not succeed. On a stable green tree the run stops as `no_progress` at iteration 3, before a third review. On a changing tree it stops as `fix_cycles_exhausted` after 3 reviews. `scripts/superloop/control.py:650`.

10. CLOSED as a spec change, not as a code accident. The written config families were `alibaba`, `minimax`, `moonshot`, `zai`. The reviewer family `deepseek` was not among them. `runtime_fallback` and `team_mode` were off. The aggregator is still `goose` / `deepseek`, the same seat as the reviewer, and the docs now say that family is not in the conflict set. `docs/SUPERLOOP.md:113`. I agree with the code. I do not agree that this should be described as a fix for independence. It is a decision to leave the aggregator family eligible to review. The old success path is now allowed on purpose.

11. PARTLY. An empty agent report is refused, and a reported model outside the cell is refused. The version string is checked. A controller-chosen binary that prints `4.19.4`, writes `from-hephaestus`, and an `export_argv` that prints `sisyphus` plus `moonshot/kimi-k2.7-code` still succeeds, with `allow_fakes` false. The reported record was `sisyphus`. The agent check trusts the export command the controller named. `scripts/superloop/workers.py:142`.

12. PARTLY. A missing record, an edited threshold, a model-labelled dataset, a made-up family, and a remote ultimate URL are refused. I also tried decimal and hex loopback spellings and `127.0.0.1.nip.io`. Those were refused. `http://127.0.0.1`, `localhost`, and `[::1]` are admitted, which the docs already say. A dataset of 100 rows, all correct, all `label_source` `human`, verifies at threshold 0.9. The string is not a person. That cannot by itself cause success. It can arm a brake the owner did not label.

13. CLOSED. `examples/superloop/questions.json:82` now says there is no approval path. The old ledger claim is gone.

14. CLOSED. An extra key on a blocker stops the run as `review_unavailable`. It does not fall through to an empty file and succeed.

15. CLOSED. Omitting `atlas` is an L8 error in the self test. A command worker is refused. The driver also adds the hook names at `scripts/superloop/control.py:183`.

16. CLOSED. `sk-`, `sk_live_`, `rk_test_`, `xoxb-`, `github_pat_`, `AIza`, `ghp_`, and `glpat-` all redact. `scripts/superloop/state.py:26`.

17. CLOSED. A token budget of 1 no longer crashes. It logs `decision_skipped` and can still succeed. `docs/SUPERLOOP.md:119` says that on purpose. Success still required the checks and the review. I do not like the skip, and it is no longer a lie.

18. CLOSED. `examples/superloop/goal.example.json:42` protects `tests`, which covers `tests/unit`.

19. CLOSED. I scanned `docs/SUPERLOOP.md`, `skills/mm-superloop/SKILL.md`, `TESTING.md`, the 1.4.0 changelog lines, `docs/research/orchestration/SUPERLOOP-COUNCIL.md`, and `examples/superloop/questions.json`. No em dashes, en dashes, or curly quotes.

## New findings

### Blocker. The worker can erase a blocker while the honest reviewer is still running.

`scripts/superloop/control.py:508` to `scripts/superloop/control.py:533`. The driver removes the findings file, starts the reviewer, then accepts any file whose mtime is within a second of the start and whose JSON is a valid list. It does not check which process wrote it. The out directory is owned by the same user as the worker.

Reproduced. The reviewer script wrote a valid blocker, then slept 0.8 seconds. A thread started by the worker overwrote `findings-*.json` with `[]` during that sleep. Status `verified_pending_owner`, success true, review ran `goose`. The pin on the reviewer script was intact. This defeats a root-owned reviewer binary too, because the findings path is still user-owned.

Smallest fix: stop using a file in a directory the worker can write. Take the findings from the reviewer process stdout. Refuse the run if that stream is empty.

### Blocker. The pin is checked at admission and not again at the call.

`scripts/superloop/workers.py:206` to `scripts/superloop/workers.py:211`, called from `scripts/superloop/control.py:348`. `docs/SUPERLOOP.md:114` says a pin that does not match stops the run. That is true only for the bytes on disk at admission.

Reproduced. The registry pinned an honest script that writes a blocker. After admission, the worker replaced that script with one that writes `[]`. Status `verified_pending_owner`, success true. The hash the owner pinned never ran.

Smallest fix: hash every pinned path immediately before `exec`, and refuse on mismatch. Exec the pinned realpath, not a PATH lookup.

### Blocker. A check can pass on a file under `.git`, and the diff is empty.

`scripts/superloop/control.py:72` hashes with `git add -A -f`. Git will not index `.git`. `docs/SUPERLOOP.md:67` says only the status file and the omo config are left out. That sentence is false.

Reproduced. The only acceptance check reads `.git/superloop-win` for `WIN`. L2 is clean, because the argv does not contain `.superloop/status.json` or `.omo/`. The worker writes that file and nothing else. Status `verified_pending_owner`, success true, diff length 0, `WIN` absent from the diff. An honest reviewer of an empty diff writes `[]`. There is nothing to flag.

Smallest fix: do not use `git add` as the acceptance hash. Walk the worktree and hash raw file bytes, including `.git`, and exclude only paths the driver itself writes. Refuse success if that walk fails.

### Blocker. L2's ban on reading the status file is a string match, and the hash omits that file.

`scripts/validate-superloop.py:79` and `scripts/validate-superloop.py:156`. `HASH_EXCLUDE` is `scripts/superloop/control.py:42`.

Reproduced. The check joins `.superloop` and `status.json` in Python and looks for `WIN`. L2 is clean. The worker writes `WIN` into the status file and a harmless `a.txt`. Status `verified_pending_owner`, success true. The diff contains `a.txt` and does not contain `WIN`. A reviewer who reads the diff never sees the bytes the check used.

Smallest fix: stop excluding the status file from the hash, and keep the blocked claim in the out directory instead. A string denylist will keep losing to a split path.

### Blocker. A clean filter shows the reviewer different bytes from the ones the check read.

Same hash path, `scripts/superloop/control.py:72`. `git add` runs clean filters. The worker can set the filter in `.git/config`.

Reproduced. The check is `grep -q SECRET secret.txt`. The worktree file contains `SECRET`. The diff contains `secret.txt filter=benign` and a blob of `ok`. Status `verified_pending_owner`, success true. `SECRET` is not in the diff. A careful reviewer can see the filter line and might flag it. The success rule does not require that. I would not call this a review of the tree the checks ran on.

Smallest fix: hash raw bytes with filters disabled, and refuse the run if `.gitattributes` or the repo config defines a filter. Refusing the filter is the smaller patch. Hashing raw bytes is the one that also covers the `.git` hole.

### Blocker. The no-op denylist misses commands that always exit 0, and an unmet goal then succeeds.

`scripts/validate-superloop.py:166`. `docs/SUPERLOOP.md:135` and `docs/research/orchestration/SUPERLOOP-COUNCIL.md:85` say the validator refuses no-op checks. It refuses `true` and a few exact `python -c` texts. It admits the rest.

Reproduced. `test 1 -eq 1` and `/usr/bin/env true` both pass L2. The worker writes nothing. The reviewer writes `[]`. Both return `verified_pending_owner`, success true, diff length 0. An honest reviewer agrees with the empty diff. The goal was not met. The check was a tautology. `sh -c true;` is also admitted. I did not run that spelling.

Smallest fix: at admission, run each check in an empty directory. If it already exits 0, refuse it. A denylist will not finish this job.

### Major. A committed nested git directory succeeds on content the diff does not contain. An empty one crashes the driver.

`docs/SUPERLOOP.md:136` discloses that a nested git repository is hashed as a link. The driver still returns success. `scripts/superloop/control.py:68` raises if `git add` fails, and `scripts/superloop/control.py:594` does not catch it.

Reproduced. A nested repo with one commit and `WIN` in `nested/win.txt` returns `verified_pending_owner`, success true. The diff is a mode `160000` gitlink. `WIN` is absent. An empty nested repo raises `RuntimeError` from `git add`, and `final.json` is not written. The first is a success on unseen bytes. The second is an uncaught crash a worker can force. I rate the success major rather than a blocker only because the doc already admits the hash gap and the diff at least shows a gitlink. The crash should still be a terminal `policy_denied`.

Smallest fix: if the hashed tree contains a gitlink, or a directory contains `.git`, stop as `policy_denied`. Catch `RuntimeError` from `git` and finish with that status instead of a traceback.

### Major. Renaming the branch and changing the goal id drops the lineage, and the next run succeeds.

`scripts/superloop/control.py:310` builds `repo_key` as common dir plus branch name. `scripts/superloop/ledger.py:92` matches that key or the goal id. A miss on both is an empty history.

Reproduced. Run 1 recorded the reviewer harness `goose` through `prior_lineage`. The same branch refused that reviewer even with a new goal id. After `git branch -m hidden-branch` and a new goal id, the next run returned `verified_pending_owner`, success true, review `goose`. The registry keys were `.../.git#master` and then `.../.git#hidden-branch`. A worker with a shell in the worktree can run that rename. The owner who starts the next run in the same checkout does not get the inheritance `docs/SUPERLOOP.md:88` promises.

Smallest fix: key the registry by the common dir only. Treat the branch name as a label, not as part of the identity.

### Major. Deleting the lineage file is an empty history, and the next run succeeds.

`scripts/superloop/ledger.py:94` swallows a missing file. `skills/mm-superloop/SKILL.md:65` tells the agent not to edit the file. The driver does not notice if the agent does.

Reproduced. After a run that should have poisoned `goose`, deleting the registry and starting again on the same goal returned `verified_pending_owner`, success true. The default path is under the user's home. The worker is that user.

Smallest fix: a missing registry must not mean an empty ledger. Require the file to exist once the owner has named it, and stop with `review_unavailable` if it is absent. A same-user worker can still delete a file the user owns. The branch-name fix does not solve that. Say so in the doc, and do not say the lineage is never reset.

### Major. The session agent check trusts a command the controller names, and the binary is not hash pinned.

`scripts/superloop/workers.py:142` and `scripts/validate-superloop.py:238`. L8 checks that `export_argv` is a list containing `{session_id}`. It does not pin the binary or the export program. `docs/SUPERLOOP.md:128` says the control plane refuses a batch it cannot verify. It refuses a batch whose export text looks wrong. It does not read the session.

Reproduced with `allow_fakes` false. A stub binary printed `oh-my-openagent 4.19.4`, wrote `from-hephaestus` into `a.txt`, and emitted a `sessionId`. The export stub printed `sisyphus` and `moonshot/kimi-k2.7-code`. Status `verified_pending_owner`, success true. The worker event reported `sisyphus`. Checks and review still ran, so this does not skip those. It skips the agent and model gate the council lists as closed. `docs/research/orchestration/SUPERLOOP-COUNCIL.md:92`.

Smallest fix: drop `export_argv` from the controller. Pin the omo binary and a fixed export command in the owner registry, and re-hash both at the call. A version regex is not a pin.

### Major. A pin of the interpreter alone satisfies L11 and the runtime. The recipe script is never hashed.

`scripts/validate-superloop.py:280` only checks that some pin's basename matches `argv[0]`. `scripts/superloop/workers.py:207` only requires the resolved executable to be in the pins. Admission never calls `validate_reviewer_registry`. `docs/SUPERLOOP.md:114` says the registry holds a hash for the executable and any recipe or script.

Reproduced. A registry whose only pin was the Python binary, with argv pointing at an unpinned script that writes `[]`, passed L11 as clean and returned `verified_pending_owner`, success true. The self test pins the script. The production check does not require that.

Smallest fix: every argv element that is a file must be pinned, at admission and again immediately before exec. Call the registry validator from `admit`, not only from the example check.

### Minor. `parse_session` treats `mode` as an agent name.

`scripts/superloop/workers.py:90`. A one-object export with `agent` `sisyphus` and `mode` `build` parses as agents `build` and `sisyphus`. If `expect_agents` is only `sisyphus`, that batch is refused. Fail closed, so this is not a success path. I did not fetch a live `opencode export`. The docs already say that format was not checked. If a real export carries `mode`, the first live run will false-deny. Drop `mode` from the agent keys unless a live export shows it is the agent name.

### Minor. A qualification record the agent writes, labelled `human`, verifies.

`scripts/superloop/qualify.py:114` checks the string `human` or `ground_truth`. I wrote 100 correct rows with that string and `verify_record` returned threshold 0.9 and no error. `docs/SUPERLOOP.md:105` says the labels come from people or ground truth. The code cannot tell. This cannot cause success. It can make advisory mode act on a dataset the decision model's author composed. Pin the record file the way reviewers are supposed to be pinned, or accept that the owner must read the dataset and say that in the admission log.

### Nit. The one-second mtime slack is sloppy, and I did not need it.

`scripts/superloop/control.py:521` accepts a findings file written up to a second before `started`. The remove just above makes that window hard to use. The overwrite blocker does not depend on it. Compare against the mtime taken after the remove, and require the file to be newer than that stamp.

## Suspected, not run this round

A rotation of failing check names still looks able to walk to the iteration cap. The key at `scripts/superloop/control.py:603` is unchanged. I did not re-execute it.

A symlink is stored as the link text, not the target bytes. I did not run that case. Same family as the clean filter if a check follows the link.

The final hash is compared, then `finish` returns. A thread that changes the tree in that gap could win. I did not catch it. I would not spend a fix on it before the findings-file hole, which is reliable.

HTTP retries inside `decide.ask` still use wall time of their own. After they return, the next gate saw a blown cap in the injected-clock case and did not succeed. I did not re-run a sleeping HTTP backend.

Subagent sessions are still unread. The docs say so. I did not live-run omo, so I cannot show a subagent model outside the restricted config. The written config no longer contains a reviewer family. That part of the old suspicion is weaker than it was.

## Checks

`python3 .github/checks.py`, `python3 scripts/check-drift.py`, `python3 scripts/validate-superloop.py --self-test`, and `python3 scripts/mm-superloop.py --self-test` all exited 0. The validator log has 53 ok lines: 3 preamble checks and 50 mutations, matching `TESTING.md`. The driver log has 67 ok lines, matching 48 scenarios plus 19 unit checks. Those counts are not a finding. The self test does not cover the new success paths above. The council line that every reproduced finding now has a regression scenario can be true of round 1 and still leave these holes open. `docs/research/orchestration/SUPERLOOP-COUNCIL.md:78`.

The library success flag is what the CLI turns into exit 0. `scripts/mm-superloop.py:46`. I did not re-run the CLI. A `verified_pending_owner` from these probes would be an exit 0 if the owner launched them that way.
