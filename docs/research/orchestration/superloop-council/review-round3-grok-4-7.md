REQUEST CHANGES.

I re-ran the success path on 3d3a9d7. The round 2 forgeries I replayed are closed. Three new ones are not. Each one returns success with `isolation` set to `container`, and the worker only writes inside the worktree. The trust boundary says that is the case the driver holds. It does not. I would not ship that paragraph. A later reader will quote it as the security claim, and the code does not meet it.

Probes live outside the repo, in `grok-probe/round3_break.py` and `grok-probe/round3_lineage.py`. Logs are `grok-probe/round3_output.txt` and `grok-probe/round3_lineage_output.txt`. I did not edit the repo. `git status` was clean at 3d3a9d7.

## Round 2 items

Closed, from my probes unless I say the official self-test.

- Findings file overwrite. Closed. A blocker on stdout stops the run. A `[]` file in the review folder does not count. My run ended `no_progress`, not success. The self-test case "a findings file in the review folder is ignored" ended `fix_cycles_exhausted`.
- Pin checked only at admission. Closed for a swap that is visible at the next call. My run ended `policy_denied` on a pin mismatch. The self-test case "a reviewer replaced after admission is refused at the call" matches. The small window between hash and exec is still in `workers.py:229` to `workers.py:240`. I did not win that race this round. The council already says the window remains. That residual is honest.
- Check reads `.git` relative to the working directory. Closed. `no_progress`. Same for the split status path. `no_progress`.
- Clean filter in the repo config. Closed. `policy_denied`. A filter added during the batch is refused too, per the self-test.
- No-op checks that already pass. Closed by the official self-test, "checks that already pass on the baseline are refused". I did not replay that one myself.
- Nested repos, empty and committed. Closed by the self-test. Both `policy_denied`, no crash. Escaping symlink too.
- Branch rename plus a new goal id. Closed. Second run `review_unavailable`, "no reviewer is independent of this run's lineage". Keys did not differ. Families from the first run were inherited.
- Deleted lineage file. Closed. Missing registry is `policy_denied`. A same-user delete and recreate is still possible. The docs say so. I did not replay the recreate.
- Controller names the omo binary or the export command. Closed. `validate_controller` rejects `worker.binary`. The self-test refuses an export program replaced during the batch, and refuses a reviewer whose script is not pinned.
- `mode` read as an agent. Closed. The self-test unit check passed, and `parse_session` only collects `agent` and `agentName`.
- Findings-file mtime slack. Closed. No findings file is read.
- Agent-written `human` labels. Not a success path. `qualify.py` is not in this diff. The docs now say the owner has to read the dataset before pinning the record. I did not re-test the qualifier.

## Blocker. Replace refs

The git helper at `control.py:75` does not pass `--no-replace-objects`. Neither does `extract_tree` at `control.py:105` and `control.py:118`, nor `write_diff` at `control.py:144`. A worker can write a replace ref under `.git/refs/replace`. That is inside the worktree. Git then shows a different blob than the one the tree object names.

The check was a normal read of `a.txt`. It had to be exactly `ok`. The worker wrote `SECRET` and replaced that blob with `ok`. The reviewer returns a blocker if the diff contains `SECRET`, otherwise `[]`.

```text
python3 grok-probe/round3_break.py
CASE replace_ref: status=verified_pending_owner success=True
isolation=container
blob=b'SECRET\n'
reviewer_saw_secret=False
diff_tail=... -no +ok
```

`git --no-replace-objects cat-file` of the blob in the success tree is `SECRET`. The reviewer was shown `+ok`. Success is a lie about the tree the owner would get from that hash with replace refs off.

The smallest fix is to pass `--no-replace-objects` from the git helper and from both direct git subprocesses in `extract_tree`. I checked the flag on git 2.53.0. With it, `cat-file` returns the stored blob and `git diff` shows `+ok` only when the blob is `ok`.

## Blocker. A worktree hook runs as the driver

`tree_hash` at `control.py:97` runs `git add`. `GIT_SAFE` at `control.py:68` turns off fsmonitor. It does not set `core.hooksPath`. Git 2.53.0 runs `.git/hooks/post-index-change` on that add, with no config change. I confirmed the default hook fires, and that `git -c core.hooksPath=<empty dir>` stops it even when config sets `hooksPath`.

The hook inherits `GIT_INDEX_FILE`, so it knows the scratch directory. In the probe it started a side process that rewrote `a.txt` in the check snapshot to `ok`, and rewrote `change.patch` so the diff said `+ok`. The tree blob stayed `SECRET`. The check does not sleep. The reviewer waits 0.4 seconds before reading the diff, which is less than a model review, and I am not going to pretend that wait is zero. The snapshot rewrite did not need it. The diff rewrite used it. Both happened, and the run succeeded.

```text
CASE hook_post_index: status=verified_pending_owner success=True
isolation=container
hook_marker=True
index_env=.../run/scratch/superloop.index
blob=b'SECRET\n'
reviewer_after=... -no +ok
```

This breaks the isolation claim itself. The worker never writes outside the worktree. The driver's git runs the hook, and the hook can write the run folder.

The smallest fix is to pass `-c core.hooksPath=` on every git invocation, pointing at an empty directory the driver creates outside the worktree. Do not use `/dev/null`. It has to be a directory.

## Blocker. The check is not jailed

`run_checks` at `control.py:496` sets the working directory to the snapshot and passes a copy of the process environment plus the goal's argv. Nothing stops the process from opening other paths. The comment at `control.py:85` says bytes outside the tree cannot make a check pass. That is false.

Two runs, both `verified_pending_owner`, `success=True`, `isolation=container`, diff length 0, `WIN` absent from the diff. The worker only wrote `.git/superloop-win`.

The first check embeds the worktree path and reads that file. The second does not contain the path. It walks `/proc` for an ancestor argv that includes `--worktree`, which is how `scripts/mm-superloop.py` is launched. Child exit code 0.

`docs/SUPERLOOP.md:71` says the check sees exactly the bytes the diff describes, including nothing under `.git`. `docs/SUPERLOOP.md:141` says owner checks are trusted and the driver cannot tell a weak test from a strong one. The second sentence does not license the first being false. A weak test of the snapshot is not the same thing as a test that reads the live `.git`.

The smallest fix is to run the check with a cleared environment and a filesystem view that contains only the snapshot. Dropping absolute paths from argv is not enough. The `/proc` walk has no absolute path in the argv.

## Major. A binary diff kills the process

`write_diff` at `control.py:144` asks for `--binary` and writes the result as text. The git helper at `control.py:75` uses `text=True`. A file containing the byte `0x8d` makes `git diff --binary` return bytes that are not UTF-8. `UnicodeDecodeError` is not in the handler at `control.py:644`. The process dies. `final.json` was not written.

```text
CASE binary_diff: UnicodeDecodeError
final False
```

Same crash on the gitdir follow-up, at `control.py:144`, after `review` had already chosen a reviewer. This is not a success. It is the round 2 empty-nested crash in a new shape. Any worker can plant one binary file and skip a clean stop.

The smallest fix is to capture the diff as bytes and write those bytes. Do not decode it.

## Major. A gitdir pointer drops the lineage key

`admit` at `control.py:367` keys the registry by the realpath of `--git-common-dir`. A worker can replace `.git` with a gitfile or a symlink to a new directory inside the worktree. The path changes. `prior` at `ledger.py:112` then misses the old families unless the goal id matches.

On the first probe the baseline check blocked the second run. The keys still differed, `wt/.git` versus `wt/alt.git`. On the second probe the baseline check fails. That run reached `write_diff`, which only happens after a usable reviewer is selected. The reviewer for A01 ultimate is goose on alibaba. The first run's authors included alibaba. That reviewer should have been refused. It was not. Success was not returned, because the binary diff crashed first. If you fix only the crash, this path is open.

A branch rename does not do this. That case stayed `review_unavailable`.

The smallest fix is to record an owner repository id outside the worktree, and refuse the run when the resolved common dir differs from the one stored for that id. Refusing every gitfile would also stop this probe, and it would break linked worktrees, which the docs want on the same key.

## Major. The documented output directory cannot succeed inside the worktree

`skills/mm-superloop/SKILL.md:32` and `docs/SUPERLOOP.md:154` tell you to pass `--out runs/RUN_ID`. If that path is inside the worktree, the review folder is created after the hash and the post-review hash fails.

```text
CASE out_inside: status=policy_denied
detail=the worktree changed during the review
```

The check is at `control.py:629`. This is not a forged success. It is a documented command that cannot finish. The smallest fix is to refuse an output directory inside the worktree, and stop implying `runs/RUN_ID` sits in the repo.

## Docs

`docs/SUPERLOOP.md:22` says everything below holds against a worker that cannot write outside its worktree, and that a success under `none` reads as unprotected because `final.json` repeats the isolation. The field is real. `control.py:335` writes it. I saw `isolation=container` next to `success=True` on the forgeries above. Repeating the field does not make the boundary true. `skills/mm-superloop/SKILL.md:29` and `CHANGELOG.md:6` repeat the same assumption.

The Round 2 table in `docs/research/orchestration/SUPERLOOP-COUNCIL.md` is accurate about the changes it names. Findings on stdout, pin rehash, snapshot copies, admission checks, nested repos, branch rename, a missing registry, and pins on absolute paths match the code I re-ran. Line 120 is honest about the pin window and about a same-user worker deleting the lineage file.

It overclaims in one place. Line 111 says checks and review use the stored blobs, and that a repo filter is refused because git would run it as the driver. The filter refusal is real. The stored-blob claim is not, while replace refs are honored. And the driver still runs a worktree hook as itself, which is the same class of mistake the filter fix was meant to close. Line 103 says most of the new holes rely on the worker being the driver's OS user. That was a fair summary of round 2. It is the wrong residual to leave standing next to this code.

`docs/SUPERLOOP.md:71` should not say the check sees exactly the diff bytes until the check is jailed.

## Checks

All four exited 0. Counts match `TESTING.md`. I am not flagging them.

- `python3 .github/checks.py` exited 0. All checks passed.
- `python3 scripts/check-drift.py` exited 0. No drift detected.
- `python3 scripts/validate-superloop.py --self-test` exited 0. 3 preamble lines and 59 mutation lines.
- `python3 scripts/mm-superloop.py --self-test` exited 0. 63 scenarios and 21 unit checks.

## Not reproduced

I did not win the pin race. The window is still in the code, and the docs admit it. I did not re-test a global git filter. The scanner at `control.py:89` only looks at `--local` and `--worktree`, which the code comment allows. I did not re-test omo config rewriting beyond the call sites, and I did not re-test qualification records.
