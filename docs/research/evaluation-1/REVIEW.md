# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 23 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker was found in the D40 update. All five substantive documents consistently assign A01, A03, A05, and A09 to the method stage and A08, A11, and A12 to the routing stage. The floor arithmetic is correct: eight method cases plus six routing cases, fourteen matched case comparisons, and twenty-eight initial arm attempts before repeats. The package does not treat those attempts as independent task identities or as authority to execute. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [BENCHMARKS.md](BENCHMARKS.md), [DECISIONS.md](DECISIONS.md), [README.md](README.md))

## Scope and method

I reviewed the uncommitted changes on local branch `evaluation-1`, based on HEAD `bb5e7e71d5da7efcdbde4cc1a2feb62e0f15d0a2`. That commit identifies the baseline, not the new working-tree content.

I inspected the complete diff to all five substantive documents, checked scenario mappings and case/attempt arithmetic, and searched related assignment, allocation, partition, coverage, independence, remaining-question, and authorization language. I read the prior review record and verified that every committed substantive baseline matches its fingerprint in my preceding routine-stage-pairs review.

I made no target-file, branch, or git-state changes. This report was authored outside the repository for incorporation as `REVIEW.md` and preserves the prior review history.

## Prior review history

The original two-document review returned REVISE with R1 through R3. The corrected two-document package received SHIP for documentation only. Independent reviews of the expanded package and subsequent owner-decision updates through D39 also returned SHIP within that boundary. Earlier nonblocking wording notes were corrected and independently rechecked. None of those reviews authorized execution, certified runtime safety, established measured effectiveness, or guaranteed feasibility.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording allowed compensated regressions and weakened mandatory controls. | High | Resolved. Mandatory controls and evidence remain required; objective regressions cannot be compensated by improvements elsewhere, and uncertainty remains inconclusive without an unauthorized regression margin. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. The client purpose and priorities remain fixed; useful-work discovery remains deferred. ([Plan: Measurement interview](PLAN.md#measurement-interview), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review did not adequately cover the complete execution stack. | High | Resolved. Whole-stack qualification and deferral for unmet controls remain mandatory. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The expanded-package review confirmed consistent selections, explicit coverage gaps, cautious causal claims, separate accounting, and the distinction between documentation and measured outcomes. Those protections remain present. ([BENCHMARKS.md](BENCHMARKS.md), [ANALYSIS.md](ANALYSIS.md))

Previously reviewed decisions remain in force as refined by subsequent owner choices:

- D14 through D18 retain method-first and routing-second comparisons, final post-repair defect scoring, one repair within the task envelope, no scored human rescue, frozen failures, and separately authorized unscored rescue without rewriting outcomes. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D19 through D25 retain checks plus agent-review feedback without hidden final-evaluator information, failure for every confirmed defect including cosmetic defects, matched class-based caps, exact templates with advance exceptions, two independent judges, and personal owner dispute resolution after artifact freeze. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D26 through D29 retain the continuous 10-hour clock from first scored dispatch and USD 100 covering all new pilot model/tool/compute charges, including setup and cleanup, without hidden pre-clock solving or spending authority. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [DECISIONS.md](DECISIONS.md))
- D30 through D33 retain the eight-minute dispute window capped by the global deadline, unresolved/not-accepted timeout outcomes, minimum breadth before depth, whole-pilot coverage with stage-local matched claims, and all active owner attention without duplicated minutes. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))
- D34 through D37 retain two distinct cases per selected scenario, fourteen across the pilot, timer-plus-log attention recording, underlying-task distinctness without a different-context requirement, and missing rather than estimated or zero forgotten intervals. No missing-data analysis exception is currently agreed. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [DECISIONS.md](DECISIONS.md))
- D38 and D39 retain two routine cases per scenario, eligibility fixed before selection and outcomes, intact scenario pairs within one stage, matched arms on each case, and mandatory adversarial security qualification. D40 now settles the previously open scenario partition. ([PLAN.md](PLAN.md), [BENCHMARKS.md](BENCHMARKS.md), [DECISIONS.md](DECISIONS.md))

## Current findings

**No new substantive blockers or required corrections.**

### Exact scenario assignment

The reviewed mapping agrees with D40 throughout the package. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Decision D40](DECISIONS.md#settled-decisions), [README.md](README.md))

| Stage | Assigned scenarios | Distinct routine floor cases | Matched comparison on every case |
|---|---|---:|---|
| Method first | A01, A03, A05, A09 | 8 | `arm-baseline` versus `arm-method` |
| Routing second | A08, A11, A12 | 6 | `arm-method` versus `arm-routing` |

The mapping preserves both required stages and keeps each scenario's two distinct routine cases together. It does not assign one case to each arm or require the fourteen-case floor separately in both stages. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))

### Case and attempt arithmetic

Four method scenarios with two cases each give eight cases; three routing scenarios with two cases each give six. Each of the fourteen cases is compared under two arms, yielding twenty-eight initial arm attempts before repeats. Any permitted repair remains inside its attempt and existing resource envelope; it is not another distinct floor case. These are design counts, not completed runs. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Decision D40](DECISIONS.md#settled-decisions))

The analysis explicitly states that twenty-eight attempts are not twenty-eight independent task identities. The earlier warning that different underlying tasks can still be correlated also remains. The arithmetic therefore does not inflate the independent sample size or establish statistical power. ([Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))

### Claims stay within the tested stage

The method-stage scenarios cannot establish routing benefits for A01, A03, A05, or A09. The routing-stage scenarios cannot establish method benefits for A08, A11, or A12. Differences between stage aggregates cannot be attributed to method versus routing because their scenario populations differ. Claims remain limited to tested routine tasks and their assigned effect. ([Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification), [Plan: Agree the experiment](PLAN.md#agree-the-experiment))

### Scenario assignment is not benchmark qualification

The benchmark document expressly separates approved scenario allocation from actual benchmark task IDs, supplemental-case selection, and coverage qualification. B01, B06, and B10 remain the selected suites, but their selection or presence in the pilot does not certify coverage or both effects for a scenario. Supplemental refactoring, security, and architecture cases still require design and approval. ([BENCHMARKS.md](BENCHMARKS.md), [ANALYSIS.md](ANALYSIS.md))

### No affordability, power, or dispatch claim

The plan labels the case/attempt counts as design arithmetic and expressly states that they do not establish whether setup, execution, judging, repairs, or required controls fit the 10-hour/USD 100 envelope. Actual cases, repeats, and resource reservations remain unapproved. Infeasibility still requires an owner scope decision rather than silent reduction, extra spending, or waived controls. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))

### Remaining questions do not reopen D40

The earlier explicit statements that the scenario partition remains open have been replaced. D31, D32, D34, and D39 now point to D40, and O11 concerns routine eligibility, actual cases, task limits, repeats, and resource allocation. The next measurement round asks for actual cases under the settled assignment, not a new choice of stage mapping. General requirements to freeze case manifests or stage subsets concern concrete task selection and resources, not permission to reassign scenarios. ([DECISIONS.md](DECISIONS.md), [Plan: Measurement interview](PLAN.md#measurement-interview))

No useful-work rediscovery, compensated tradeoff, human-rescue permission, runtime change, or direct main update is introduced. The original PR #3 workflow and the requirement for separate execution approval remain explicit. ([README.md](README.md), [PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))

## Nonblocking details before execution

- Select and approve two distinct routine underlying tasks for each scenario under the fixed mapping, with primary-scenario and routine-eligibility evidence.
- Freeze benchmark task IDs, supplemental cases, exact templates, checks, grading procedures, and a case-level stage matrix without treating scenario assignment as coverage certification.
- Pin both matched comparison configurations and budget the twenty-eight initial arm attempts plus any approved repeats, repairs, both judges, setup, storage, and cleanup.
- Determine numeric resource limits and statistical evidence requirements without treating attempt counts as independent task counts or a powered sample.
- Preserve stage-local conclusions, failed outcomes, and all-active-owner attention recording; forgotten timing intervals remain missing under the currently agreed rule.
- Complete whole-stack security qualification, reservations, cutoff procedures, and separate execution authorization. Return for a scope decision if the approved floor cannot fit safely.

These details implement D40 rather than reopen its scenario mapping or imply approval of an actual run. ([Decision log: Open questions](DECISIONS.md#open-questions), [PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `2955249517d5bcb2f95ee41af23ba27131ce642d3355c94c755384adccff5aa9` |
| `PLAN.md` | `16b28e5af87d305240cf6ef3d9d1e400653955f9556fdf75f15d69557aa7a2b5` |
| `BENCHMARKS.md` | `52613eb8a6cd6777fcdaf73288271d84208dd71ff888332bb125bd0288f8077c` |
| `ANALYSIS.md` | `f9625565b797d00cb56e20d6daabd693cb949553911156565968512ab0d54e66` |
| `DECISIONS.md` | `c63edfbb10ae9581934cc3a56ea8c752c96bdb9ae40e6db711e95664f2dddc54` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to substantive documents require renewed review.

## Limits

- This is an independent read-only document review, not execution or expenditure approval, runtime certification, a benchmark result, or a guarantee of improved outcomes.
- I performed no installation, benchmark execution, model runtime test, penetration test, implementation audit, time-measurement trial, cost simulation, or feasibility trial. None is required for this documentation-only update.
- I did not run or certify repository gates. They remain the integrating agent's separate responsibility.
- No external research was performed for this owner-decision change. Earlier source checks were selective rather than exhaustive verification of every benchmark, license, dependency, or execution requirement.
- Fidelity was assessed against supplied owner decisions and review context, not an independently authenticated transcript of every historical discussion.
- I did not change or independently verify the remote state of PR #3, either branch, or main.

**Final disposition: SHIP the fingerprinted documentation through the existing PR workflow, subject to separately run repository gates. No pilot execution or expenditure is authorized.**
