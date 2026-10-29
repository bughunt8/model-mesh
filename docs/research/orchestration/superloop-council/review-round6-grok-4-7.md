APPROVE WITH NITS.

The round 5 deputy is closed. I replayed it against feda4d6 with a real stub worker and a real pinned bubblewrap. The session export now starts through the same launcher as the version check and the batch. It ran the planted hook, inside bubblewrap, and the hook could not write `/usr/local/bin` or `/var/tmp`. The run did not succeed. I did not find another process the driver starts for the worker that still runs outside the jail while `worker_isolation_enforced` is true.

HEAD is feda4d6. I did not edit the repo.

## Round 5 items closed

The major is closed. Probe `grok-probe/round6_break.py`, clean log `grok-probe/round6_clean.txt`.

```text
CASE deputy status=cap_iterations success=False w_enf=True c_enf=True isolation=bwrap jail=bwrap host=False export_cwd_dir=False detail=2 iterations
  version-jail.txt proc1 /usr/bin/bwrap ... ver nowrite 30
  jail.txt worker uid 2000 | worker proc1 /usr/bin/bwrap ... worker nowrite /var/tmp/deputy 30 | worker nowrite /usr/local/bin/deputy 30
  export-jail.txt cwd /tmp/r6-deputy-1r0ax0wi/wt | uid 2000 | proc1 /usr/bin/bwrap ... hook True | hook_ran | child 1
  hook-ran.txt ran | nowrite /var/tmp/deputy 30 | nowrite /usr/local/bin/deputy 30 | nowrite /run/r6-deputy 30
```

The version check, the batch, and the export each have `/usr/bin/bwrap` as proc1. The export's working directory was the worktree, so it found `.export-hook` and ran it. The hook and a child of the export both failed to create `/usr/local/bin/deputy`. Errno 30, read-only. The host file was absent when the check ran. Status `cap_iterations`, not success. Both flags true, and this time the jail applied to the process that used to be the deputy.

The minor is disclosed, not re-tested. `docs/SUPERLOOP.md:26` and the boundary note at `scripts/superloop/control.py:416` say the driver trusts the pinned file to be bubblewrap, and that the admission namespace test does not bind later calls. I did not re-pin a wrapper.

The three nits are fixed. `scripts/superloop/control.py:32` no longer mentions a protected flag. `scripts/mm-superloop.py:24` says eleven bubblewrap scenarios, and `TESTING.md:16` says 82 scenarios, eleven of which need bubblewrap, and 21 unit checks. The self-test printed `self-test passed` with 103 ok lines, which is that split. `docs/SUPERLOOP.md:152` now says the check jail has no network, and the next sentence says the worker jail shares it.

## What I tried besides the deputy

A check that reads `/dev/shm/r6shm` also ended `cap_iterations`, `success=False`, `host=False`. The hook reported a write to `/dev/shm` from inside the jail. That write did not survive on the host, and the check did not see it. Both jails use `--dev /dev`, so each gets its own `/dev`. Not a host side channel. Log is the `r6shm` case in `grok-probe/round6_clean.txt`.

An escaping symlink planted by the same hook ended `policy_denied` before I removed it. That is the existing symlink refusal, not a new success. First log, `grok-probe/round6_output.txt`.

With `worker.isolation` left as `container`, the same hook export did not run the worktree file. Its report landed in `<out>/export-cwd` and says `hook False`, proc1 `/sbin/init`. `worker_isolation_enforced` was false. The unjailed worker itself could still write `/usr/local/bin`, and the run succeeded because the checks only looked at the tree. That is the disclosed same-user unjailed worker. I am not re-filing it. It does confirm the new sentence that, without the worker jail, the export's working folder is not the worktree.

I looked for another process the driver starts on the worker's behalf. `OmoWorker.version`, `OmoWorker.run`, and the session export all go through `_launch` at `scripts/superloop/workers.py:185`. `ran_jailed` at `scripts/superloop/workers.py:199` is true only if at least one of those calls was jailed and none was not. `Run.boundary` at `scripts/superloop/control.py:411` reads that property. The old post-call assignment is gone. `materialize` and the git rev-parse in setup run as the driver, on the driver's fragment and the driver's git dir, before the worker has written anything. The reviewer is not a worker process. The checks are the check jail. On the jailed runs, the tags the driver wrote were the version stderr, the worker stdout, the export stderr, and the check logs. I did not see a worker-side tag whose proc1 was the host init while the flag was true.

## Nit. The new scenario does not prove the hook ran

`scripts/mm-superloop.py:644` expects success, the outside file absent, and the worker flag true. The stub export at `scripts/mm-superloop.py:616` swallows `OSError` if `.export-hook` is missing. If the export's working directory were not the worktree, the hook would never run, the outside file would still be absent, and the scenario would still pass. My probe is what shows the hook actually ran and the write failed. The scenario does catch the old bug, where the file was created. It would not catch a future bug that skips the hook.

Smallest fix: have the planted hook also write a marker in the worktree, and require that marker in the tree and the outside file absent.

## Docs

The trust boundary at `docs/SUPERLOOP.md:24` matches what I ran. It names the version check, each batch, and each session export. The empty-folder sentence at `docs/SUPERLOOP.md:28` matches the unjailed export report. It does not claim an unjailed worker cannot write the run folder. That residual stays in the same paragraph.

`docs/research/orchestration/SUPERLOOP-COUNCIL.md:150` matches the code and this replay. I confirmed the new scenario passes. I did not replay the old commit, so I am not second-guessing the negative control they describe. The last sentence, that these fixes had not been re-reviewed, was true of the commit. The skill at `skills/mm-superloop/SKILL.md:29` still says the driver jails the worker and every check. That is no longer missing the export, because the export is one of the worker launches. I do not see an overclaim there.

## Checks

`python3 scripts/mm-superloop.py --self-test` printed `self-test passed`, exit 0. Log `grok-probe/round6_selftest.txt`. `python3 .github/checks.py` printed `all checks passed`. `python3 scripts/check-drift.py` printed `No drift detected`. `python3 scripts/validate-superloop.py --self-test` printed `self-test passed`.

Not re-filed, as asked: the pin race, a pinned file that is not bubblewrap, stated isolations, a same-user unjailed worker, a weak check, and the worker's session record in its writable folders.
