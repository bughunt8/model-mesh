REQUEST CHANGES.

The jailed stub worker cannot write `/var/tmp` or `/usr/local/bin`. That round 4 path is closed when the worker is a real process under bubblewrap. I still got a success with both boundary flags true. The driver runs the session export outside the worker jail, in the worktree, as the driver user. The worker planted a hook. The export ran it. The check read the file the export wrote. The omo process itself was jailed.

HEAD is 554d855. I did not edit the repo.

## Major. The session export is not in the worker jail

`OmoWorker.run` wraps the omo argv at `scripts/superloop/workers.py:213` and does not wrap the export at `scripts/superloop/workers.py:225`. That `run_bounded` call uses the worktree as its working directory. `Run.boundary` at `scripts/superloop/control.py:411` sets `worker_isolation_enforced` from the jail object on the worker, not from every process in the batch. `scripts/superloop/control.py:830` sets the flag after `worker.run` returns if `self.worker.jail` is set.

The probe export is not the stock stub. The stock stub at `scripts/mm-superloop.py:612` only prints JSON. Mine reads `.export-hook` from its working directory, runs that file, then prints the session JSON. I did not test a live opencode export. The skill already says that format was not checked live. The gap is still in the driver. It chooses the working directory, it does not jail that process, and it then marks the worker jail enforced.

Reproduced. The first full run of `python3 /home/user/workspace/s1-superloop/grok-probe/round5_break.py` died in the deputy case on a null byte in my hook. That log is `grok-probe/round5_output.txt` and is not this result. After the hook string was fixed, the deputy case alone wrote `grok-probe/round5_deputy.txt`.

```text
CASE deputy status=verified_pending_owner success=True w_enf=True c_enf=True isolation=bwrap jail=bwrap host_win={'deputy': True} diff_has_WIN=True detail=checks pass twice on the reviewed tree and an independent review found no blocker and no major
  jail.txt label deputy | uid 2000 | proc1 /usr/bin/bwrap --die-with-parent --new-session --unshare-all --share-net --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --ro-bind /tmp/r5-deputy-_4id4761/omo-stub /tmp/r5-deput | nowrite /var/tmp/deputy 30 | nowrite /usr/local/bin/deputy 30 | WROTE /tmp/r5-deputy-_4id4761/deputy |
```

`proc1` is `/usr/bin/bwrap`. The jailed process recorded 30, read-only, on both host targets. `/usr/local/bin/deputy` existed on the host when the check ran. The review patch at `/tmp/r5-deputy-_4id4761/run/scratch/review-001/change.patch` contains the hook source, which is why `diff_has_WIN` is true. It does not contain the host file. The check does not read the hook. It reads `/usr/local/bin/deputy`. The stub reviewer printed `[]`.

The hook is visible in the diff. A person reading the branch would see it. The system's reviewer did not. Success under the system's own rule still happened. `/usr` is one of the system folders the check jail mounts read-only, so a file the export writes there is visible to the check and invisible to the jailed worker as a writable path.

Smallest fix: pass the export argv through `self._wrap` before `run_bounded`, the same wrap the omo run already gets. The worker jail keeps the host read-only and the worktree writable, so a session file on the host stays readable and a write under `/usr` fails. If a real export needs a cache outside the worktree, the owner already has `writable` for that.

## Minor. The admission smoke test does not bind later calls

`scripts/superloop/control.py:531` runs one argv: the pinned binary, `--unshare-all`, `--ro-bind`, `/`, `/`, `--`, `true`. A wrapper can delegate that call to real bubblewrap and exec everything else after `--`. I pinned that wrapper. Both flags came back true. The worker was not jailed. The check was not jailed. Success. `WIN` is not in the diff.

```text
python3 /home/user/workspace/s1-superloop/grok-probe/round5_break.py
CASE fakebwrap status=verified_pending_owner success=True w_enf=True c_enf=True isolation=bwrap jail=bwrap host_win={'fakebwrap': True} diff_has_WIN=False
  jail.txt label fakebwrap | uid 2000 | proc1 /sbin/init  | WROTE /var/tmp/fakebwrap | WROTE /usr/local/bin/fakebwrap | WROTE /tmp/r5-fakebwrap-s2e4wqo0/fakebwrap |
```

Log: `grok-probe/round5_output.txt`.

This is not a jailed-worker escape. The owner pinned the wrapper. A same-user writer of the tools registry can also edit the driver. I am not re-filing the pin race. I am filing the claim. `docs/SUPERLOOP.md:26` says the driver refuses if bubblewrap is unpinned, changed, or cannot create namespaces. The wrapper is unchanged for the one admission call and creates namespaces there. Later calls are not that binary. `scripts/superloop/control.py:412` says enforced means the driver started that process under the pinned bubblewrap. That sentence is true only if the pin is bubblewrap.

Smallest fix: say the pin is trusted as bubblewrap, and that the smoke test does not bind later invocations. Do not pretend the namespace test proves the later process was confined.

## Nits

`scripts/superloop/control.py:36` still says `final.json` repeats both with a protected flag. `protected` is gone. The record is `boundary` at `scripts/superloop/control.py:411`. This commit edited the file and left the sentence.

`scripts/mm-superloop.py:24` still says the four check-jail scenarios. The self-test registers seven check-jail scenarios and three jailed-omo scenarios inside the bubblewrap gate. `TESTING.md:16` already says ten need bubblewrap. The docstring does not.

`docs/SUPERLOOP.md:152` says the jail has no network. The worker jail passes `--share-net` at `scripts/superloop/control.py:219`. The check jail does not. The next clause is about a check that needs a download. Name the check jail.

## Docs that do not overclaim the omo process

The trust boundary at `docs/SUPERLOOP.md:20` matches the real bubblewrap path for the omo process and the checks. It says enforced means the driver started that process under the pinned bubblewrap. It says a fake is never enforced. It says a check can still read system folders and check mounts, and that a same-user worker without a jail can write a world writable `/usr/local/bin`. It does not say the export is jailed. That omission is the major above, not a second false sentence.

`skills/mm-superloop/SKILL.md:29` says set both to `bwrap` so the driver jails the worker and every check, and read the boundary record because only what it marks enforced was enforced. That matches the omo process and the checks. It does not mention the export.

`docs/research/orchestration/SUPERLOOP-COUNCIL.md:138` matches the code and the parent's rerun. It does not claim a jailed worker was tested against `/var/tmp`. The last sentence, that these round 4 fixes have not been re-reviewed, was true of the commit. I am reviewing them here.

## Round 4 items closed

From `grok-probe/round4_rerun_output.txt`, fake worker, this commit.

Replace refs ended `policy_denied`. The worktree hook ended `no_progress` and `hook_ran` was false. An absolute `.git` read under the check jail ended `no_progress`. The `/proc` walk ended `policy_denied` because the check already passed on the baseline, not success. The binary diff ended `no_progress` and `final.json` exists. An output folder inside the worktree ended `policy_denied`. A moved `.git` ended `policy_denied`. A fake worker writing `/var/tmp` ended `no_progress` with `worker_isolation_enforced` false.

From this round, real jailed stub, `grok-probe/round5_output.txt`.

The escape case ended `cap_iterations`, `success=False`, both flags true, `host_win` false. The jailed process recorded 30 on `/var/tmp/escape` and `/usr/local/bin/escape`. `proc1` was `/usr/bin/bwrap`. The round 4 forge does not succeed when the worker is the stub under real bubblewrap.

The honest case ended `verified_pending_owner` with both flags true and `host_win` false. That is the intended path, not a break. The jailed process reported a write of a sibling under its temp parent. I listed `/tmp/r5-honest-8v5ohq1t`. There is no `honest` sibling on the host.

A writable folder of `/usr/local/bin` ended `policy_denied`. The detail names an overlap with a system folder.

Not re-filed, as asked: the pin race, stated isolations, a same-user unjailed worker, a weak check that reads `/etc`, and the worker's session record in its writable folders. The parent's rerun `host_read` still succeeds with `check_jail_enforced` true and `worker_isolation_enforced` false. That is the disclosed `/etc` read.

## Checks

`python3 .github/checks.py` printed `all checks passed`. `python3 scripts/check-drift.py` printed `No drift detected`. `python3 scripts/validate-superloop.py --self-test` printed `self-test passed`. `python3 scripts/mm-superloop.py --self-test` printed `self-test passed`, exit 0. The log has 102 ok lines, 81 scenarios and 21 unit checks. Ten of those scenarios sit behind the bubblewrap gate. That matches `TESTING.md:16`. Not a finding. Log: `grok-probe/round5_selftest.txt`.

## Suspected, not a success

`scripts/superloop/control.py:649` sets `checks_ran_jailed` before `run_bounded` returns. `scripts/superloop/control.py:830` sets `worker_ran_jailed` from the jail object after `worker.run` returns, including when the call failed. I did not get a success from a process that never started under bubblewrap, except the pinned-wrapper case above. The first deputy run was `policy_denied` with both flags true, and that worker had been jailed, so it does not show a false flag.
