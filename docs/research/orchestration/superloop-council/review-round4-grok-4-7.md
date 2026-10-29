REQUEST CHANGES.

The round 3 worktree-only forgeries I replayed are closed. `protected: true` is not. A same-user worker writes the pass file outside the worktree, the jailed check reads it, the diff does not contain it, and `final.json` still says success and protected. I would not treat that flag as a result. It is two strings copied from the controller.

Probe: `grok-probe/round4_break.py`. Log: `grok-probe/round4_output.txt`. I did not edit the repo. HEAD is 55fc962.

## Round 3 items

Closed, from this round's probes unless I say the official self-test.

- Replace refs. Closed. A store trial kept the blob as `SECRET` and did not run the worker's filter or hook. A full run with `git replace -f` ended `cap_iterations`, not success. The check wanted `ok` and did not get it.
- `post-index-change` in the worktree. Closed. `hook_ran=False`, status `no_progress`.
- Check reads the live `.git` by absolute path. Closed under `bwrap`. `no_progress`.
- Check walks `/proc` for the worktree. Closed under `bwrap`. The walk did not read the win file. Status `cap_iterations`, not success.
- Binary diff crash. Closed. `final.json` exists. The diff was written, including the `0x8d` byte, and the process did not die.
- `.git` pointed at a new directory. Closed. Second run `policy_denied`. The repository id stayed bound to the old common dir.
- Output directory inside the worktree. Closed. `policy_denied`.
- Escaping symlink. Closed. `policy_denied`, `symlink a.txt points outside the tree`.

## Blocker. The jail is not a snapshot, and protected is still true

`jail_argv` at `control.py:198` bind-mounts `/` read-only, then puts a tmpfs on `/tmp`, the worktree, the git dir and the run folder. The snapshot is bound back. Everything else on the host stays readable. `finish` at `control.py:392` sets `protected` from `worker.isolation` and `check_jail`. It does not look at what the check opened, or at whether the worker was actually another user.

The worker wrote `WIN` to `/var/tmp`, which is not `/tmp` and not the worktree, and wrote `a.txt` in the worktree so the tree would differ from admission. The check passes only if that outside file is `WIN` and `a.txt` exists. The reviewer returns `[]` if the diff does not contain `SECRET`. The diff does not contain `WIN`.

```text
python3 grok-probe/round4_break.py
CASE outside_write: status=verified_pending_owner success=True
protected=True jail=bwrap isolation=container

EVIDENCE outside_write status=verified_pending_owner success=True
protected=True isolation=container jail=bwrap
diff_has_WIN=False diff_len=228
```

This is not the disclosed "same user edits the driver or the run folder" residual. The worker did not touch those. The check read a path the hide list never names. A denylist of `/var/tmp` is the wrong fix. The next writable directory will do the same thing.

The smallest fix is to stop binding the host root into the check. Mount the snapshot, and the loader paths the interpreter needs, and nothing else. Until isolation is measured, do not set a boolean named protected. Echo the two controller fields and say they were not checked.

`docs/SUPERLOOP.md:25` says each check sees only its snapshot. The next sentence, about a read-only host with a few directories replaced, is the one the code matches. Step 6 at `docs/SUPERLOOP.md:78` goes back to the false version: the copy is all the check can see. `docs/research/orchestration/SUPERLOOP-COUNCIL.md:130` says the same, and that protected means an isolated worker with jailed checks. I ran the opposite. `skills/mm-superloop/SKILL.md:29` tells the owner that `protected: true` means both guarantees held.

A separate run read `/etc/passwd` from inside the same jail and also returned success with `protected` true. That one is a crafted check plus a trivial tree edit, which a weak snapshot check could also do. I am not counting it as a second forge. It is the same hole: the check is not confined to the snapshot.

## Docs

The Round 3 table is right about the git store, the hook path, the binding, the inside output folder, and the binary diff. I re-ran those and they held. It is wrong about the jail. Line 130 marks the absolute-path and `/proc` finding closed by saying the check sees only its snapshot. The worktree hide does close those two paths. I confirmed both. It does not close the class. A path outside the hide list still decides the check.

`docs/SUPERLOOP.md:27` is careful about `protected: false`. It does not say the converse. The flag name and the council do. A success with `protected: true` in this run was staged by the worker.

`TESTING.md:16` has a broken sentence, "which CI sets of the state builder". The counts beside it match the self-test. Nit only.

## Checks

All four exited 0. Counts match `TESTING.md`. I am not flagging them.

- `python3 .github/checks.py` exited 0. All checks passed.
- `python3 scripts/check-drift.py` exited 0. No drift detected.
- `python3 scripts/validate-superloop.py --self-test` exited 0. 66 ok lines, 3 preamble and 63 mutations.
- `python3 scripts/mm-superloop.py --self-test` exited 0. 96 ok lines, 75 scenarios and 21 unit checks.

## Not reproduced

I planted `core.fsmonitor` and a `post-index-change` hook. The leftover `rev-parse` in `control.py:525` does not run the fsmonitor. `git status` does, and the driver does not run status on the worker repo. I am not filing that call. The pin race and a same-user edit of the run folder are still open, and the docs already say so. I did not re-test them.
