# Testing

What runs, what it proves, and what it does not. All commands run from the repository root. CI uses Python 3.12 and the scripts were also run on 3.14 and no installed packages, except the landscape YAML check which needs `pyyaml`.

## Offline checks (run in CI on every pull request)

| Command | Checks | Self-test |
|---|---|---|
| `python .github/checks.py` | Vendor denylist, manifests, skills, profiles, links | none |
| `python scripts/validate-full-config.py` | The full deployable config example, rules R1 to R14 | none |
| `python scripts/validate-orchestration.py` | Matrix, harness examples, review panel data, rules O1 to O18 | `--self-test` plants 74 mutations and each must be caught |
| `python scripts/validate-scenarios.py` | Skill front matter, size cap, scenario patterns, rules S1 to S4 | `--self-test` |
| `python scripts/aggregate-findings.py` | Merges review findings, rejects invalid ones | `--self-test` |
| `python scripts/score-review.py` | Scores review runs against seeded defects | `--self-test` |
| `python scripts/validate-superloop.py` | Superloop goal and controller examples, the tools registry template and the decision question catalog, rules L1 to L12 | `--self-test` plants 66 mutations and each must be caught |
| `python scripts/mm-superloop.py --self-test` | The superloop driver: 81 end-to-end scenarios, including every success forgery the four independent review rounds reproduced and runs of the real omo adapter against stub binaries, and 21 unit checks of the state builder, session parsing, backends and qualification. Ten scenarios need bubblewrap; without it they are skipped, or fail when `MM_SUPERLOOP_REQUIRE_JAIL=1`, which CI sets | built in |
| `python scripts/check-drift.py` | Docs against data and scripts, rules D1 to D9. It reads text with patterns and does not know what a sentence means | `--self-test` |
| `python scripts/landscape/landscape_scan.py --self-test` | The landscape scorer | built in |
| `python scripts/landscape/review_gate.py --self-test` | The landscape review-gate parser | built in |

The generated matrix table is rebuilt with `python scripts/validate-orchestration.py --render`. The check fails when the committed file differs.

## What offline checks do not show

- The review panel contract is checked as data. Whether a runner starts reviewers with zero context and read-only tools is not tested.
- A skill scenario is a static pattern test. It shows a rule is still written in the skill. It does not show an agent follows the rule.
- The orchestration matrix is checked for structure and policy. No row has been run.
- The seeded-defect scorer runs on an invented fixture. It measures nothing about any model, harness or lens.
- The superloop driver is tested with fake workers, fake reviewers, stub omo and session-export binaries, one real pinned command reviewer and replayed decision answers. No omo install, session export, live decision endpoint or live reviewer harness has been run. The HTTP backend is tested only for its offline guard and its answer parsing.

## Live runs

No live run is recorded yet. When one is made, add a row with the date, the harness and its version, the model route, the task, the result and a link to the evidence. Do not record a run that was not executed.

| Date | Harness and version | Model route | Task | Result | Evidence |
|---|---|---|---|---|---|
| none | | | | | |
