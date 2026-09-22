# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 23 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker was found in the D34/D35 update. The package faithfully specifies a feasibility floor of two distinct cases per selected scenario, fourteen distinct cases across the whole pilot before repeats, and an owner-operated timer plus tagged activity log for all active owner pilot attention. It does not claim that the floor is powered, affordable, executable, or already implemented. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [BENCHMARKS.md](BENCHMARKS.md), [DECISIONS.md](DECISIONS.md), [README.md](README.md))

## Scope and method

I reviewed the uncommitted changes on local branch `evaluation-1`, based on HEAD `79034dc217a7500d3cd25e4b5a0b35116b170b0a`. That commit identifies the baseline, not the new working-tree content.

I inspected the complete diff to all five substantive documents and checked case distinctness, floor counting, stage allocation, timer/log recording, corrections, missing data, overlapping intervals, dates, remaining questions, and authorization wording. I read the preceding review record and verified that each committed substantive baseline document matches its fingerprint in my preceding coverage-and-attention attestation, including its resolved matching-scope clarification.

I made no target-file, branch, or git-state changes. This report was authored outside the repository for incorporation as `REVIEW.md` and preserves the prior review history.

## Prior review history

The original two-document review returned REVISE with R1 through R3. The corrected two-document package received SHIP for documentation only. Independent reviews of the expanded package and later owner-decision updates through D33 also returned SHIP within that boundary. Earlier nonblocking wording notes were corrected and independently rechecked. None of those reviews authorized execution, certified runtime safety, established effectiveness, or guaranteed feasibility.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording allowed compensated regressions and weakened mandatory controls. | High | Resolved. Mandatory controls and evidence remain required, objective regressions cannot be compensated by improvements elsewhere, and uncertainty remains inconclusive without an unauthorized regression margin. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. The client purpose and priorities remain fixed; useful-work discovery remains deferred. ([Plan: Measurement interview](PLAN.md#measurement-interview), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review did not adequately cover the full execution stack. | High | Resolved. Whole-stack qualification and deferral for unmet controls remain mandatory. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The expanded-package review confirmed consistent selections, explicit coverage gaps, cautious causal claims, separate accounting, and the distinction between documentation and measured outcomes. Those protections remain present. ([BENCHMARKS.md](BENCHMARKS.md), [ANALYSIS.md](ANALYSIS.md))

Previously reviewed decisions remain intact:

- D14 through D18: method-first and routing-second comparisons, final post-repair defect scoring, at most one repair within the task envelope, no scored human rescue, frozen failures, and separately authorized unscored rescue without rewriting outcomes. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [DECISIONS.md](DECISIONS.md))
- D19 through D25: checks plus agent-review repair feedback without hidden final-evaluator information; failure for every confirmed defect including cosmetic defects; matched class-based caps; exact references/templates with advance exceptions; two independent AI judges; and personal owner dispute resolution after artifact freeze. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D26 through D29: a continuous 10-hour clock from first scored-task dispatch including grading and owner waits, no concealed scored solving during setup, and USD 100 covering all new pilot model/tool/compute charges including setup and cleanup. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [DECISIONS.md](DECISIONS.md))
- D30 and D31: eight elapsed minutes from recorded escalation or the earlier global deadline, unanswered disputes frozen as unresolved and not accepted, no late score rewrite, and minimum breadth followed by paired depth with an owner scope decision if infeasible. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))
- D32 and D33: the coverage floor applies across the combined pilot rather than separately to each stage, both matched comparisons remain required, claims stay within tested scope, and all active owner pilot effort is included with category breakdowns and no duplicated minutes. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [DECISIONS.md](DECISIONS.md))

## Current findings

**No new substantive blockers or required corrections.**

### Distinct-case floor

D34 consistently fixes two distinct cases for each of the seven selected scenarios, yielding a minimum of fourteen distinct cases across the whole pilot. The plan gives each floor case one primary scenario, so one case cannot satisfy several scenario floors. Reuse in another arm or stage, repairs, and repeated runs cannot inflate the distinct-case total. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Decision D34](DECISIONS.md#settled-decisions), [BENCHMARKS.md](BENCHMARKS.md))

The floor is not imposed separately on each stage, and it is not represented as fourteen executions or a fixed final sample size. The existing design still requires matched competing arms within each stage, explicit allocations to both stages, and claims limited to tested stage/scenario combinations. Case selection, additional cases, repeats, and the stage matrix remain open. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Plan: Isolate the method and routing effects](PLAN.md#isolate-the-method-and-routing-effects), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))

### Feasibility and scope safeguards

The package explicitly distinguishes the feasibility floor from a powered statistical design and does not claim that fourteen cases, both stages, repeats, two judges, and required controls fit the 10-hour/USD 100 limits. Infeasibility requires a new owner scope decision before execution, not silent case reduction, selection removal, benchmark substitution, or a security waiver. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification), [BENCHMARKS.md](BENCHMARKS.md))

### Timer plus activity log

D35 is implemented as a measurement requirement: the owner starts and stops a timer, tags activities in a log, and reconciles the records. The plan requires preservation of original entries and reasons for corrections. Missing or estimated intervals must be labeled rather than converted to zero effort or represented as precise timed observations. No recording tool is claimed to exist or to have been deployed. ([Plan: Candidate measurement dictionary](PLAN.md#candidate-measurement-dictionary), [Decision D35](DECISIONS.md#settled-decisions))

The method covers pilot work outside the scored clock as well as operational work. Time spent recording and reconciling itself counts as attention. Passive waiting remains elapsed time, active monitoring remains attention, overlapping records cannot duplicate the same active minute, and equivalent recording procedures apply across arms. ([Plan: Candidate measurement dictionary](PLAN.md#candidate-measurement-dictionary), [Analysis: Human attention and cost boundaries](ANALYSIS.md#human-attention-and-cost-boundaries))

### Missing data and claim integrity

The analysis requires reporting recording gaps and their effect on comparative conclusions. A forgotten timer cannot establish zero effort; reconstructed durations cannot be passed off as precise observations; insufficient attention evidence remains inconclusive rather than proving an improvement. Existing predeclared shared-effort allocation and raw-total reporting remain in place. ([Analysis: Human attention and cost boundaries](ANALYSIS.md#human-attention-and-cost-boundaries))

### Remaining questions and dates

The current questions concern implementation details: final case manifest, additional cases, repeats, stage allocations, numeric resource caps, timer/log tooling, fields, reconciliation cadence, missing-data handling, and shared-effort attribution. They do not reopen the two-case floor, whole-pilot scope, all-attention headline, or timer-plus-log choice. General references to open sample sizes are consistent with an agreed minimum and an unagreed final statistical design. ([Plan: Measurement interview](PLAN.md#measurement-interview), [Benchmark measurement questions](BENCHMARKS.md#measurement-questions-that-remain-open), [Decision log: Open questions](DECISIONS.md#open-questions))

Document update dates and D34/D35 use 23 September 2026, while the benchmark research statement retains its 22 September 2026 review date. This separates a planning update from an assertion that external sources were reverified on the new date. ([BENCHMARKS.md](BENCHMARKS.md), [DECISIONS.md](DECISIONS.md))

### Preserved authority boundaries

B01, B06, and B10 remain the selected benchmarks, and A01, A03, A05, A08, A09, A11, and A12 remain the selected scenarios. No useful-work rediscovery, compensated tradeoff, human-rescue permission, runtime change, or direct main update is introduced. Original PR #3 remains the documented publication route, and implementation and spending require separate authorization. ([README.md](README.md), [PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))

## Nonblocking details before execution

- Approve a case manifest with at least fourteen distinct case identities and one primary floor scenario per case. Define distinctness sufficiently to avoid relabeling the same case as new coverage.
- Allocate cases and repeats to both matched comparison stages, preserve stage-local claims, and assess feasibility without treating the minimum as evidence of statistical power.
- Select the timer/log tool and fields, start/stop conventions, reconciliation cadence, correction provenance, and missing/estimated interval procedure. Preserve raw records and do not treat missing data as zero.
- Predeclare overlap handling and shared-effort allocation across categories, tasks, arms, and stages. Reconcile attributed records to one all-pilot owner-time total.
- Define the evidence treatment of incomplete timing records before making an attention-improvement claim; a chosen timer does not itself establish measurement accuracy.
- Complete comparator and judge configurations, templates, class caps, sampling/evidence rules, budget reservations, cutoff mechanics, whole-stack qualification, and separate execution authorization.

These details implement D34/D35 rather than reopen the settled floor or recording method. ([Decision log: Open questions](DECISIONS.md#open-questions), [PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `fd00d05a8d7cd9db229b6f4a88efbe8c4237703223b6496a112ce375fa0a4a31` |
| `PLAN.md` | `a796b607aff0cbd1f442e71f5e15251ebe23f6a895e5263ca53719c8bc1e5819` |
| `BENCHMARKS.md` | `743a61fee85b10b7b33e07b82e1ab2aaab84e4c506242b4a7fe1acc971d6783a` |
| `ANALYSIS.md` | `1904613e5afc17a6a2eb0de03110ecdc9bf83bfe2a375d32251276a81185bf21` |
| `DECISIONS.md` | `b3d73ef4609531cb571646ada11f35bf30895d41ecce96b1f8ff019d3411726a` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to substantive documents require renewed review.

## Limits

- This is an independent read-only document review, not execution or expenditure approval, runtime certification, a benchmark result, or a guarantee of improved outcomes.
- I performed no installation, benchmark execution, model runtime test, penetration test, implementation audit, time-measurement trial, cost simulation, or feasibility trial. None is required for this documentation-only update.
- I did not run or certify repository gates. They remain the integrating agent's separate responsibility.
- No external research was performed for these owner-decision changes. Earlier source checks were selective rather than exhaustive verification of every benchmark, license, dependency, or execution requirement.
- Fidelity was assessed against supplied owner decisions and review context, not an independently authenticated transcript of every historical discussion.
- I did not change or independently verify the remote state of PR #3, either branch, or main.

**Final disposition: SHIP the fingerprinted documentation through the existing PR workflow, subject to separately run repository gates. No pilot execution or expenditure is authorized.**
