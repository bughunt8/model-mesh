# Staging integration review

## Verdict

Do not publish this index. The working tree is the integration I reviewed, and that content is close. It is not the tree a merge commit would record.

Once the commit matches the working tree, the content verdict is approve with nits. Publishing the index as it stands would drop the installer change, the staging release-check trigger, the repository map, and the installer test, and it would ship a README that still says this repo has no benchmark data.

I did not edit the repo and I did not push.

## Working tree

No path from `github/staging` at `923ff02` is missing, and no path from HEAD `66391b3` is missing. The imported benchmark files match staging with an empty diff: `BENCHMARK.md`, `configs/`, `data/`, `docs/01-methodology.md` through `docs/06-handover.md`, `scripts/score.py`, `scripts/validate.sh`, `skills/mm-method/references/domains/motion.md`, and `.github/workflows/benchmark.yml`. Motion wiring is still in `skills/mm-method/SKILL.md:30`, `skills/mm-method/references/flowcharts.md:21`, and `skills/mm-verify/SKILL.md:25`. The extra verify text versus staging is the machine-readable finding section at `skills/mm-verify/SKILL.md:34`, from the superloop line, not a lost motion rule.

`git diff HEAD` is empty for `scripts/superloop/`, `scripts/mm-superloop.py`, `scripts/validate-superloop.py`, `examples/superloop/`, `profiles/`, and `skills/mm-superloop/`. Those files do not mention `omo.recommended.jsonc` or the score CSVs. I am not reopening the driver review.

The denylist exemptions in the working `.github/checks.py` are the exact union of the two parents. Ours keeps `scripts/validate-orchestration.py` and the `docs/research/` prefix. Theirs adds `BENCHMARK.md`, `docs/01-methodology.md` through `docs/06-handover.md`, and the `configs/` and `data/` prefixes. The self-test expected set at `.github/checks.py:159` matches that union, and the prefix check at `.github/checks.py:177` is `configs/`, `data/`, and `docs/research/`. The negative list at `.github/checks.py:185` includes `scripts/score.py`, `scripts/test-install.py`, `docs/REPOSITORY-MAP.md`, and the nearby leak names. `scripts/score.py` stays scanned. That part of the claim holds.

Third-party headings are the union. Staging's motion citations start at `THIRD_PARTY_NOTICES.md:62`, the "not adopted" section is present, and the Elephant-Goldfish notice from this line is still there. The benchmark copyright line at `LICENSE:5` is the staging line, kept. `.gitignore:9` only gains the staging ignores. The worktree plugin manifest stays at 1.4.0 in `.plugin/plugin.json:4`. Taking staging's plugin blob would downgrade the version to 1.3.0. Do not do that.

The named docs do separate candidates from runtime authority, in the working tree.

`docs/REPOSITORY-MAP.md:11` says the eleven benchmark seats are not the four routing profiles. `docs/REPOSITORY-MAP.md:14` says decision-model answers are shadow-only by default and evidence, not model confidence, determines success. `docs/REPOSITORY-MAP.md:19` says a benchmark rank cannot override region, retirement, licence, budget, or independent review. `docs/REPOSITORY-MAP.md:20` says the superloop does not load `configs/omo.recommended.jsonc` and does not pick a model from scores. `docs/research/orchestration/SYNTHESIS.md:58` says the roster does not reverse a retirement, region, licence, or independence decision, and that this integration note is not a new claim of council agreement. `docs/research/orchestration/SUPERLOOP-COUNCIL.md:9` says benchmark candidates do not change the matrix, the frozen profile, or the shadow-only recommendation. `docs/SUPERLOOP.md:7` repeats the same boundary. `README.md:225` no longer says the repo ships no benchmark data. It says the snapshot supports candidate comparisons and does not establish task success, reviewer effectiveness, Hong Kong reachability, or live superloop compatibility. `AGENTS.md:11` says seat scores are not authority to change profiles or the frozen cell. That is the right split. I would not let a score in `data/` move a profile.

`examples/README.md:14` and `examples/README.md:67` now say `momus.disable`. That matches rule R9 in `scripts/validate-full-config.py:23` and the rejection of `enabled` at `scripts/validate-full-config.py:293`. The old `momus.enabled` sentences were stale. This correction is right.

Both working installers copy five skills, including `mm-superloop`, and move an existing directory aside before the copy. See `install.sh:17` and `install.ps1:14`. I ran `python3 scripts/test-install.py --self-test --shell bash` in this tree. It passed. The destination name contains spaces. The test compares every file in every `mm-*` skill that has a `SKILL.md`, writes a local file into each installed skill, reinstalls, and checks that the single backup matches the pre-reinstall tree and the new copy matches the source. An unrelated file in the destination was left alone. I archived `66391b3` outside the repo and ran the same test there. It failed: `first install omitted or changed mm-superloop`. The regression claim is real.

This machine has no `pwsh`. I did not run the PowerShell path. The script looks up `pwsh` at `scripts/test-install.py:27`, not Windows PowerShell 5. GitHub-hosted runners include PowerShell 7, and `pwsh` is the default shell on Windows, per the [PowerShell Actions guide](https://docs.github.com/en/actions/tutorials/build-and-test-code/powershell) and the [workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax). The Windows job is plausible. It is not something I executed.

In the working `.github/workflows/checks.yml:4` pushes to `main` and `staging` run the release job. `pull_request` at `.github/workflows/checks.yml:5` has no branch filter, so a pull request into staging runs too. A push to some other branch does not, unless it is also a pull request. The Linux job runs the bash installer test at `.github/workflows/checks.yml:20`. The `install-windows` job at `.github/workflows/checks.yml:72` runs only the PowerShell installer test, on `windows-latest`. `.github/workflows/benchmark.yml:4` already covers pushes to `main` and `staging`, and its `pull_request` trigger is also unfiltered. That workflow is staged. The release-check change is not.

## The index is the wrong tree

Five paths are still unmerged: `.github/checks.py`, `.plugin/marketplace.json`, `.plugin/plugin.json`, `CHANGELOG.md`, and `THIRD_PARTY_NOTICES.md`. The working text has no conflict markers, and the resolutions I read are the ones I would keep. Git still has no resolved blob for them. A merge commit cannot be created until those paths are added. Adding only those five is not enough.

The staging trigger and the installer steps exist only as unstaged edits to `.github/workflows/checks.yml`. The staged workflow still limits pushes to `main` and has no installer step and no Windows job. The staged `install.sh` still copies four skills. `docs/REPOSITORY-MAP.md` and `scripts/test-install.py` are untracked. `TESTING.md`, `docs/SUPERLOOP.md`, both synthesis files, `examples/README.md`, and `scripts/check-drift.py` are modified in the worktree and not in the index. `README.md`, `AGENTS.md`, and `CONTRIBUTING.md` are staged and then edited again. The staged README still says the repo ships no benchmark data, in the same file that describes `BENCHMARK.md`. The working `README.md:225` is the correction.

`CHANGELOG.md:18` and `docs/REPOSITORY-MAP.md:33` describe CI that the working workflows have and the index does not. If those sentences land without the unstaged workflow and the untracked test, they will be false on the commit that gets pushed.

Add the worktree versions of the unmerged files, the unstaged edits, and the two untracked files. Then look at `git status` and `git diff --cached` before committing. I would refuse a commit whose cached `install.sh` still lists four skills or whose cached checks workflow still says `branches: [main]`.

## Nits

These stay even after the index matches the worktree. None of them is a dropped staging file or a lost runtime control.

`CONTRIBUTING.md:32` says the exact-path and exact-prefix exemptions cover the benchmark files and nothing else. That is false. `.github/checks.py:159` also exempts `scripts/validate-full-config.py`, the landscape source files, `scripts/landscape/CRON_TASK.md`, and `scripts/validate-orchestration.py`. The prefix list also covers all of `docs/research/`. The earlier "only" sentence at `CONTRIBUTING.md:5` has the same hole. The useful rule is the next sentence: do not carry benchmark model IDs into any other file. Say that, and point at the self-test for the full set. As written, a later edit could "correct" the gate by deleting an exemption the other line still needs. The self-test would catch the deletion. The sentence should not invite it.

`CHANGELOG.md:42` files the benchmark additions, limitations, and exemption note under 1.3.0. On this line, 1.3.0 is the review-panel release. Staging used 1.3.0 for a different tree. A reader will think main's 1.3.0 shipped the scorecard. It did not. The short note at `CHANGELOG.md:17` is the honest place. Move the benchmark detail there, or label it as the staging line's 1.3.0, not as part of the review-panel release. `CHANGELOG.md:54` saying no other path gains an exemption is the same overclaim in miniature.

`BENCHMARK.md:40` still says three profiles are structurally misconfigured and that one model should appear in none of four chains. That file has no pointer to the repository map. Preserving it verbatim was the right merge. Leaving it as the benchmark front door without one sentence of scope is how someone treats a candidate verdict as a profile edit. I would add that sentence before publication. I would not rewrite the staging findings to do it.

`.github/checks.py:225` still requires four skills. Both parents had that list, so the merge did not drop a fifth check. The new installer test is what fails if `mm-superloop` is not copied. The release gate's own skill section does not know the fifth skill exists. Name it there too, or the next person who deletes the installer step will not hear about a missing skill from `checks.py`.

## Left alone

I did not re-run `scripts/mm-superloop.py --self-test`. The merge does not change that driver. `docs/SUPERLOOP.md:5` says round 6 approved with one test nit and that the nit is fixed. That matches the recorded round 6 result and the message on `66391b3`. I did not re-prove the fix in this pass. Known limits from that review stay open at `docs/research/orchestration/SUPERLOOP-COUNCIL.md:172`. I am not re-filing them.

PRs 5 and 6 were not merged and should stay open.
