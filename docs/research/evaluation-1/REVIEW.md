# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 23 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker was found in the D38/D39 update. The package specifies two distinct routine cases per selected scenario and keeps each scenario's two-case floor together in one comparison stage. Both stages remain required, each case still receives matched competing-arm attempts, and claims remain limited to tested routine work and the effect actually evaluated. Mandatory security qualification is not weakened. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [BENCHMARKS.md](BENCHMARKS.md), [DECISIONS.md](DECISIONS.md), [README.md](README.md))

## Scope and method

I reviewed the uncommitted changes on local branch `evaluation-1`, based on HEAD `82738369ae2e5880fb222c5eb9a5947d324226d0`. That commit identifies the baseline, not the new working-tree content.

I inspected the complete diff to all five substantive documents and checked routine eligibility, task distinctness, fourteen-case coverage, scenario pairing, within-stage matching, both-stage participation, failure retention, security gates, budget claims, remaining questions, and authorization wording. I read the preceding review record and verified that every committed substantive baseline matches its fingerprint in my preceding distinctness-and-missing-time review.

I made no target-file, branch, or git-state changes. This report was authored outside the repository for incorporation as `REVIEW.md` and preserves the prior review history.

## Prior review history

The original two-document review returned REVISE with R1 through R3. The corrected two-document package received SHIP for documentation only. Independent reviews of the expanded package and owner-decision updates through D37 also returned SHIP within that boundary. Earlier nonblocking wording notes were corrected and independently rechecked. None authorized execution or established runtime safety, effectiveness, affordability, or statistical adequacy.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording allowed compensated regressions and weakened mandatory controls. | High | Resolved. Mandatory controls and evidence remain required; objective regressions cannot be compensated by other improvements, and uncertainty remains inconclusive without an unauthorized regression margin. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. The client purpose and priorities remain fixed; useful-work discovery remains deferred. ([Plan: Measurement interview](PLAN.md#measurement-interview), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review did not adequately cover the complete execution stack. | High | Resolved. Whole-stack qualification and deferral for unmet controls remain mandatory. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The expanded-package review confirmed consistent selections, explicit coverage gaps, cautious causal claims, separate accounting, and the distinction between documentation and measured outcomes. Those protections remain present. ([BENCHMARKS.md](BENCHMARKS.md), [ANALYSIS.md](ANALYSIS.md))

Previously reviewed decisions remain in force as refined by subsequent owner choices:

- D14 through D18 retain method-first and routing-second comparisons, final post-repair defect scoring, one repair within the task envelope, no scored human rescue, frozen failures, and separately authorized unscored rescue without rewriting outcomes. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D19 through D25 retain checks plus agent-review feedback without hidden final-evaluator information, failure for every confirmed defect including cosmetic defects, matched class-based caps, exact templates with advance exceptions, two independent judges, and personal owner dispute resolution after artifact freeze. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D26 through D29 retain a continuous 10-hour clock from first scored dispatch and USD 100 covering all new pilot model/tool/compute charges, including setup and cleanup, without concealed pre-clock solving or spending authority. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [DECISIONS.md](DECISIONS.md))
- D30 through D33 retain the eight-minute dispute window capped by the global deadline, unresolved/not-accepted timeout outcomes, minimum breadth before depth, whole-pilot coverage with stage-local matched claims, and all active owner attention without double counting. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [DECISIONS.md](DECISIONS.md))
- D34 through D37 retain the fourteen-distinct-case floor, owner-operated timer plus activity log, underlying-task distinctness without an additional context requirement, and missing rather than estimated or zero timing intervals. No missing-data analysis exception is currently agreed, and unassessable attention comparisons remain inconclusive. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [DECISIONS.md](DECISIONS.md))

## Current findings

**No new substantive blockers or required corrections.**

### Two routine cases per scenario

D38 consistently chooses two routine cases for each selected scenario's floor, not one routine plus one challenging case or two challenging cases. Routine eligibility and relevant complexity criteria must be declared before case selection and results. Upstream benchmark labels alone do not establish suitability for the local routine-work scope. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [BENCHMARKS.md](BENCHMARKS.md), [Decision D38](DECISIONS.md#settled-decisions))

The fourteen-case floor remains across the whole pilot, not fourteen cases per stage. The underlying-task distinctness rule remains unchanged: paraphrases, cosmetic variants, revision changes, seeds, arm/stage reuse, and repeats cannot inflate the count. Routine cases need not share an identical task and do not become independent statistical observations merely because they are separately identified. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))

### Scenario pairs stay in one stage

D39 requires each scenario's two routine floor cases to stay together in one assigned stage. The seven scenarios are partitioned between method and routing comparisons, with both stages populated; no particular partition or numeric stage allocation has been invented. The assignment must be fixed before outcomes. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Decision D39](DECISIONS.md#settled-decisions), [README.md](README.md))

The plan explicitly prevents the key comparison error: keeping two cases together does not mean assigning one case to each arm. Each individual case still receives matched attempts from both competing arms within its assigned stage. Stage one remains the baseline-versus-method comparison and stage two the method-versus-routing comparison. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Plan: Isolate the method and routing effects](PLAN.md#isolate-the-method-and-routing-effects))

Reusing all fourteen floor cases in both stages is not silently selected. Extra cases or cross-stage runs require explicit allocation and feasibility review, not automatic expansion of the work. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Decision log: Superseded or constrained proposals](DECISIONS.md#superseded-or-constrained-proposals))

### No relabeling failures or broad reliability claims

Failed or unexpectedly difficult cases retain their assigned outcomes. The routine label cannot be chosen because a model succeeded or changed afterward to remove failures. The new task mix does not establish challenging-case reliability, full-suite performance, or representativeness of all client work. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification), [BENCHMARKS.md](BENCHMARKS.md))

Claims remain local to tested routine tasks and their assigned effect. A scenario tested for method effect does not establish a routing result, and the reverse also holds. Differences between stage aggregates with different scenario populations cannot be attributed to method versus routing. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))

### Routine productivity scope does not waive adversarial controls

Mandatory security qualification, boundary attacks, evidence-tampering checks, and every-confirmed-defect acceptance remain required. The analysis explicitly separates these control gates from challenging productivity cases, so the routine-case choice cannot be used to omit them or exempt a benchmark from whole-stack qualification. ([Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification), [BENCHMARKS.md](BENCHMARKS.md), [Plan: Qualify controls before measuring productivity](PLAN.md#qualify-controls-before-measuring-productivity))

### Feasibility, questions, and authority

The package retains the 10-hour and USD 100 ceilings without claiming that routine cases make the design affordable, complete, powered, or ready to run. The final cases, routine criteria, scenario partition, repeats, task-level caps, and other protocol details remain open; infeasibility still requires an owner scope decision rather than silent reduction or a waiver. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Decision log: Open questions](DECISIONS.md#open-questions))

The remaining questions ask which scenarios belong to each stage and how routine eligibility will be defined, not whether to split scenario pairs or choose challenging cases instead. B01, B06, and B10 and scenarios A01, A03, A05, A08, A09, A11, and A12 remain selected. No useful-work rediscovery, compensated tradeoff, human-rescue permission, runtime change, or direct main update is introduced. ([Plan: Measurement interview](PLAN.md#measurement-interview), [README.md](README.md), [DECISIONS.md](DECISIONS.md))

## Nonblocking details before execution

- Approve routine-eligibility criteria before selecting tasks. Record why each case qualifies without using scored outcomes as the definition of routine work.
- Freeze a manifest containing two different underlying routine tasks per selected scenario, primary scenario identities, and distinctness rationales.
- Approve a nonempty scenario allocation to each required stage, keeping every floor pair together and matching competing arms on each individual case.
- Define repeats and any proposed additional work within the fixed limits. Do not infer approval to duplicate the whole floor across both stages.
- Preserve failed and unexpectedly difficult cases, use the scenario-by-stage matrix in reporting, and limit claims to tested routine populations and effects.
- Complete control qualification, exact templates, comparator and judge configurations, resource reservations, timer/log implementation details, cutoff handling, statistical evidence rules, and separate execution authorization.

These details implement D38/D39 rather than reopen the routine-only floor, divide a scenario pair between stages, weaken matching, or waive security gates. ([Decision log: Open questions](DECISIONS.md#open-questions), [PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `4093f0b5391ef5a61cdb853380fef0220ed05a69492a75065dc6e434769df43a` |
| `PLAN.md` | `2ef582da987e94f0b8b180f8edd85342921fb13230572ee1424a9c276e17a1ba` |
| `BENCHMARKS.md` | `58cf3a18387724d4f0f60ec82a6a816b332d1f93b9d0631ecf4b7f58332e0df8` |
| `ANALYSIS.md` | `f638b35c731d869320656dcf296d3221a55ea4e99a098c15da90cea3b58b8f6b` |
| `DECISIONS.md` | `5b504f5e9dd0a60dd7d5faa40e0ea0a8401dc843b12469406580f6ce30aa4f66` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to substantive documents require renewed review.

## Limits

- This is an independent read-only document review, not execution or expenditure approval, runtime certification, a benchmark result, or a guarantee of improved outcomes.
- I performed no installation, benchmark execution, model runtime test, penetration test, implementation audit, time-measurement trial, cost simulation, or feasibility trial. None is required for this documentation-only update.
- I did not run or certify repository gates. They remain the integrating agent's separate responsibility.
- No external research was performed for these owner-decision changes. Earlier source checks were selective rather than exhaustive verification of every benchmark, license, dependency, or execution requirement.
- Fidelity was assessed against supplied owner decisions and review context, not an independently authenticated transcript of every historical discussion.
- I did not change or independently verify the remote state of PR #3, either branch, or main.

**Final disposition: SHIP the fingerprinted documentation through the existing PR workflow, subject to separately run repository gates. No pilot execution or expenditure is authorized.**
