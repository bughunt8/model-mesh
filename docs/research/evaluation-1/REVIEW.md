# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 22 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker was found in the D32/D33 update. The coverage floor applies across the combined pilot, with both matched comparison stages preserved and claims limited to tested combinations. The headline attention measure includes all active owner pilot effort, including setup and experimental evaluation, without counting passive waiting or duplicating shared minutes. This verdict applies to the five substantive document versions fingerprinted below. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [BENCHMARKS.md](BENCHMARKS.md), [DECISIONS.md](DECISIONS.md), [README.md](README.md))

## Scope and method

I reviewed the uncommitted changes on local branch `evaluation-1`, based on HEAD `d7507cee307be51ab242e3535b4e32cedff9c828`. That commit identifies the baseline, not the new working-tree content.

I inspected the complete diff to all five substantive documents, checked related coverage, stage matching, attention, allocation, overhead, rescue, claim, and authorization wording across the package, and read the previous review record for continuity. I verified that each committed substantive baseline document matches its fingerprint in my preceding dispute-and-sampling review, including its two resolved cleanup notes.

I subsequently inspected the exact matching-scope clarification in `PLAN.md`. Reversing that replacement in memory reproduced the preceding reviewed hash; the other four documents were unchanged. The fingerprints below identify the final reviewed versions.

I made no target-file, branch, or git-state changes. This report was authored outside the repository for incorporation as `REVIEW.md` and preserves the prior review history.

## Prior review history

The original two-document review returned REVISE with R1 through R3. The corrected two-document package then received SHIP for documentation only. Reviews of the expanded package and subsequent owner decisions through D31 also returned SHIP within that boundary. Two nonblocking D30/D31 wording notes were subsequently corrected and independently rechecked. None of these reviews authorized execution or established runtime safety, effectiveness, feasibility, or statistical adequacy.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording allowed compensated regressions and weakened mandatory controls. | High | Resolved. Mandatory controls and evidence remain required; objective regressions cannot be compensated by other improvements, and uncertainty remains inconclusive without an unauthorized regression margin. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. The client purpose and priorities remain fixed, and useful-work discovery remains deferred. ([Plan: Measurement interview](PLAN.md#measurement-interview), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review did not cover the complete execution stack adequately. | High | Resolved. Whole-stack qualification and deferral for unmet controls remain mandatory. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The expanded-package review confirmed consistent selections, explicit coverage gaps, cautious causal attribution, separate accounting, and the distinction between documentation and measured outcomes. These protections remain present. ([BENCHMARKS.md](BENCHMARKS.md), [ANALYSIS.md](ANALYSIS.md))

The previously reviewed decisions remain intact:

- D14 through D18: method-first and routing-second comparisons, final post-repair defect scoring, at most one repair inside the task envelope, no scored human rescue, frozen failures, and separately authorized unscored rescue without rewriting outcomes. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [DECISIONS.md](DECISIONS.md))
- D19 through D25: checks plus agent-review repair feedback without hidden final-evaluator information; failure for every confirmed defect including cosmetic defects; matched class-based caps; exact references/templates with advance exceptions; two independent AI judges; and personal owner dispute resolution after artifact freeze. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D26 through D29: a continuous 10-hour clock from first scored-task dispatch including grading and owner waits, no concealed scored solving during setup, and USD 100 covering all new pilot model/tool/compute charges including setup and cleanup. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [DECISIONS.md](DECISIONS.md))
- D30 and D31: eight elapsed minutes from recorded dispute escalation or the earlier global deadline, unanswered disputes frozen as unresolved and not accepted, no late score rewrite, and minimum breadth followed by repeated paired trials with an owner scope decision if the floor is infeasible. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [DECISIONS.md](DECISIONS.md))

## Current findings

**No new substantive blockers.**

### Whole-pilot coverage floor

D32 applies the minimum floor across the combined pilot, not independently to each stage. Stage subsets may differ, but neither the method comparison nor the routing comparison may be omitted. The plan requires matched arms on the same tasks within each stage, a predeclared scenario-by-stage matrix, and approval of numeric floor and stage allocation rather than inventing a sample count. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Decision D32](DECISIONS.md#settled-decisions))

Evidence from a scenario in one stage cannot fill the missing comparison in another. The analysis expressly prohibits pooling unlike stage populations into an inferred overall method-plus-routing effect, and the benchmark document warns that including a suite somewhere does not establish both effects for it. This prevents pilot-wide breadth from becoming an unsupported claim about every stage/scenario combination. ([Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification), [BENCHMARKS.md](BENCHMARKS.md))

### All active owner effort is included

D33 is reflected in the headline metric, analysis ledgers, benchmark rules, index, and decision log. Preparation/setup, briefing, supervision, safety intervention, independent evaluation, disputes, record keeping, and cleanup all count as active owner pilot attention. Being experiment-only or outside the scored clock is not an exclusion. Operational-only attention may be shown as a diagnostic subset but cannot replace the all-pilot headline. ([Plan: Candidate measurement dictionary](PLAN.md#candidate-measurement-dictionary), [Analysis: Human attention and cost boundaries](ANALYSIS.md#human-attention-and-cost-boundaries), [Decision D33](DECISIONS.md#settled-decisions))

Passive waiting belongs in elapsed-time reporting, while active monitoring during a wait consumes attention. Economic amortization does not erase observed active minutes. The raw owner-time total is therefore distinct from the 10-hour scored clock and the USD 100 charged-resource ceiling. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))

### Allocation, double counting, and comparative claims

The package requires one raw pilot total plus category breakdowns and predeclared attribution across tasks, arms, and stages. Shared setup, evaluation, and simultaneous monitoring cannot duplicate the same owner minutes. Allocation rules cannot be moved opportunistically after results, and a raw total spanning unlike populations cannot alone demonstrate an attention improvement. ([Plan: Candidate measurement dictionary](PLAN.md#candidate-measurement-dictionary), [Analysis: Human attention and cost boundaries](ANALYSIS.md#human-attention-and-cost-boundaries))

This preserves the distinction between complete workload reporting and a causal comparison. Exact recording and allocation procedures remain open, but the scope of included effort is settled rather than left available for later exclusion. ([Decision log: Open questions](DECISIONS.md#open-questions), [ANALYSIS.md](ANALYSIS.md))

### Rescue and authorization boundaries

Active owner effort for separately authorized rescue that remains part of this pilot is included under its own identity, without changing the original failure, success denominator, or accepted-delivery outcome. A separate follow-on must be disclosed separately. These accounting provisions do not authorize rescue, additional work, execution, or spending. ([Plan: Candidate measurement dictionary](PLAN.md#candidate-measurement-dictionary), [Analysis: Human attention and cost boundaries](ANALYSIS.md#human-attention-and-cost-boundaries))

B01, B06, and B10 remain the selected benchmarks, and A01, A03, A05, A08, A09, A11, and A12 remain the selected scenarios. No compensated tradeoff, useful-work rediscovery, silent scope removal, or security waiver is introduced. Original PR #3 remains the documented publication route without direct main changes. ([README.md](README.md), [DECISIONS.md](DECISIONS.md))

## Resolved consistency note

The nonblocking matching-scope ambiguity from the first D32/D33 review is resolved. `PLAN.md`, "Isolate the method and routing effects," line 154, now states:

> Within each stage, use the same task instances, base revisions, infrastructure class, tool access, safety policy, and agreed resource envelope for its competing arms. The two stages may use different predeclared subsets.

This explicitly confines matching to competing arms within each stage while preserving different predeclared stage subsets. It is consistent with D32 and does not change the approved design. No substantive blocker or unresolved consistency note remains from this review. ([Plan: Isolate the method and routing effects](PLAN.md#isolate-the-method-and-routing-effects), [Plan: Agree the experiment](PLAN.md#agree-the-experiment))

## Nonblocking details before execution

- Propose and approve the numeric whole-pilot coverage floor and scenario-by-stage matrix, preserving both matched comparisons and the distinction between distinct cases and repeats.
- Limit stage-specific and combined claims to supported task populations. Do not infer untested routing effects from method-stage coverage or vice versa.
- Define how all active owner pilot work is captured, including preparation before scored dispatch and evaluation/cleanup afterward. Missing time records must not be treated as zero effort.
- Predeclare allocation of shared setup, evaluation, and concurrent monitoring before outcomes influence attribution. Reconcile allocated minutes and any explicit shared/unallocated category to the single raw total.
- Preserve raw attention totals, diagnostic categories, and comparable task-level attribution without subtracting experiment-only effort or using different stage populations as an improvement baseline.
- Complete comparator and judge configurations, templates, class caps, sample design, cutoff rules, reservations, security qualification, and separate execution authorization within the existing limits.

These details implement D32/D33; they do not reopen the whole-pilot floor, all-attention headline, no-compensation rule, or no-human-rescue boundary. ([Decision log: Open questions](DECISIONS.md#open-questions), [PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `516f7359fb412c67b8856434c9c343090025907b50c15f38233b2ccb1940297d` |
| `PLAN.md` | `eae0582515ccfe505b83497a653b90418357f94a8fbd56446cb801ccba8dcb53` |
| `BENCHMARKS.md` | `c2a2df1c964c7ddb744e62e9f361befc9265156c0bda932e17709f96b94569dc` |
| `ANALYSIS.md` | `a40145d121b705effdfa32c6356691223faa9e334b3b921e92478247209ca6a9` |
| `DECISIONS.md` | `14a94db8949a52bcb176b4efa0a11f959a625c881184a24ae6d09ffbe967c1c8` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to substantive documents require renewed review.

## Limits

- This is an independent read-only document review, not execution or expenditure approval, runtime certification, a benchmark result, or a guarantee of improved outcomes.
- I performed no installation, benchmark execution, model runtime test, penetration test, implementation audit, cost simulation, or feasibility trial. None is required for this documentation-only update.
- I did not run or certify repository gates. They remain the integrating agent's separate responsibility.
- No external research was performed for these owner-decision changes. Earlier source checks were selective rather than exhaustive verification of every benchmark, license, dependency, or execution requirement.
- Fidelity was assessed against supplied owner decisions and review context, not an independently authenticated transcript of every historical discussion.
- I did not change or independently verify the remote state of PR #3, either branch, or main.

**Final disposition: SHIP the fingerprinted documentation through the existing PR workflow, subject to separately run repository gates. No pilot execution or expenditure is authorized.**
