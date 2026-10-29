# Staging integration index confirmation

## Verdict

Index confirmed. Approve this staged tree. No integration nit from the last review remains.

`git write-tree` is `73cb4919a4bce176277c5d0a17e0dae9009b6048`. That is not a `787` prefix. Use this tree id. I did not commit.

## What I checked

`git diff` is empty, so the worktree matches the index. `git ls-files -u` is empty. `git ls-files --others --exclude-standard` is empty. Every path in HEAD `66391b3` and every path in `github/staging` at `923ff02` is in this tree. `git diff --cached HEAD` is empty for `scripts/superloop/`, `scripts/mm-superloop.py`, `scripts/validate-superloop.py`, `examples/superloop/`, `profiles/`, and `skills/mm-superloop/`. I am not reopening the driver review.

The cached checks workflow at `.github/workflows/checks.yml:4` pushes to `main` and `staging`. The Linux installer test is at `.github/workflows/checks.yml:21`. The Windows job is at `.github/workflows/checks.yml:72` and runs the PowerShell installer test. Cached `install.sh:17` and `install.ps1:14` copy all five skills. `docs/REPOSITORY-MAP.md` and `scripts/test-install.py` are in the index. Plugin version stays `1.4.0` at `.plugin/plugin.json:4`. Staged `README.md:13` matches the workflow triggers, and `README.md:225` still treats the benchmark as candidate evidence, not task success.

The four nits are closed in the index, not only in a side edit.

`CONTRIBUTING.md:5` no longer says real model IDs are allowed only in a short list. `CONTRIBUTING.md:32` names the benchmark exceptions and says the self-test defines the complete set. That set is still the union I already checked, locked at `.github/checks.py:159` and `.github/checks.py:177`.

`CHANGELOG.md:21` puts the benchmark detail under 1.4.0 and says staging's 1.3.0 at `923ff02` is not the review-panel 1.3.0. The 1.3.0 section no longer carries those benchmark claims.

`BENCHMARK.md` differs from staging by one paragraph. It says the snapshot evaluates candidate configurations, not the current routing profiles, and it links the repository map. The snapshot findings below that paragraph are unchanged.

`.github/checks.py:225` now requires `mm-superloop` with the other four skills.

The earlier review is archived at `docs/research/orchestration/superloop-council/review-staging-integration-grok-4-7.md` and still says not to publish the old index. That sentence is about the tree I rejected. This confirmation is about `73cb4919`.

I did not re-run the release suite or the driver self-test in this pass. The confirmation is the index.
