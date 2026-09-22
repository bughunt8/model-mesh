# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 22 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker was found in the D28/D29 update. The documents faithfully fix the continuous 10-hour clock at first scored-task dispatch and include all new pilot model/tool/compute charges in the aggregate USD 100 ceiling, including setup and cleanup. They preserve the separation between unresolved enforcement details and settled limits, without granting execution or spending permission. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [BENCHMARKS.md](BENCHMARKS.md), [DECISIONS.md](DECISIONS.md), [README.md](README.md))

## Scope and method

I reviewed the uncommitted changes on local branch `evaluation-1`, based on HEAD `fe4758d00967455236bc8448371f01d63bd1dd34`. That commit identifies the baseline, not the new working-tree content.

I inspected the complete diff to the five substantive documents, checked related clock, setup, charges, cleanup, cutoff, rescue, accounting, and authorization wording across the package, and read the previous review record for continuity. I verified that the committed baseline of each substantive document exactly matches its fingerprint in my preceding panel-and-budget review.

I made no target-file, branch, or git-state changes. This report was authored outside the repository for incorporation as `REVIEW.md`. It replaces the previous attestation while preserving the review history.

## Prior review history

The original two-document review returned REVISE with R1 through R3. The corrected two-document package received SHIP for documentation only. Independent reviews of the expanded package and subsequent owner-decision updates through D27 also returned SHIP within that same boundary. None certified runtime safety, measured effectiveness, feasibility, or execution readiness.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording allowed compensated regressions and weakened mandatory controls. | High | Resolved. Mandatory controls and evidence remain required; no objective regression can be compensated by another improvement. Uncertainty remains inconclusive without an unauthorized regression margin. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. The client purpose and priorities remain fixed, and useful-work discovery remains deferred. ([Plan: Measurement interview](PLAN.md#measurement-interview), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review did not cover the complete execution stack adequately. | High | Resolved. Whole-stack qualification remains mandatory; unmet controls require deferral rather than an exception based on upstream instructions. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The expanded-package review confirmed consistent selections, explicit coverage gaps, cautious causal claims, separate accounting, and the distinction between documentation and measured outcomes. Those protections remain intact. ([BENCHMARKS.md](BENCHMARKS.md), [ANALYSIS.md](ANALYSIS.md))

The previously reviewed decisions remain consistent:

- D14 through D18 preserve method-first and routing-second comparisons, final post-repair defect scoring, at most one repair within the task envelope, no human rescue during scored work, frozen failures, and separately authorized unscored rescue that cannot rewrite outcomes. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [DECISIONS.md](DECISIONS.md))
- D19 through D21 preserve checks plus agent-review feedback without hidden final-evaluator information, failure for every confirmed defect including cosmetic defects, and predeclared matched scenario/difficulty-class caps. ([PLAN.md](PLAN.md), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))
- D22 and D23 preserve AI judging with human dispute resolution, exact versioned references/templates with advance exceptions, and protection against answer leakage through task-visible templates. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [DECISIONS.md](DECISIONS.md))
- D24 through D27 preserve two independent judges, personal dispute resolution by the owner, elapsed rather than active-human time, and aggregate rather than per-arm or per-suite spending limits. D28/D29 now settle the previously open clock and new-charge boundaries. ([DECISIONS.md](DECISIONS.md), [README.md](README.md))

## Current findings

**No new substantive blockers. No required corrections.**

### Continuous clock fidelity

D28 starts the scored-phase clock at first scored-task dispatch. Execution, queues, retries, grading, and owner-adjudication waits all consume the same continuous 10-hour window, without pauses or stage resets. The text does not reinterpret elapsed runtime as CPU hours or active owner minutes. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [Decision D28](DECISIONS.md#settled-decisions))

Setup is outside that scored clock, but the plan expressly prohibits hiding scored-task solving, rehearsal, or grading in preparation. Calibration must remain separate from scored holdouts, and pre-clock setup is not authorization to install or spend before separate execution approval. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits))

### All new charges are included

D29 includes all new pilot model/tool/compute charges in USD 100, including setup, scored execution, repairs, both judges, simulators, storage, and cleanup. Being before or after the scored clock is not a cash exemption. New provisioning, usage, upgrades, overages, and applicable billing charges are included; delayed invoices or pilot-incurred post-run storage remain attributable to the pilot. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification), [Decision D29](DECISIONS.md#settled-decisions))

Pre-existing sunk expenditure and owner labor remain separately disclosed in economic accounting rather than being falsely labeled new cash charges. That distinction does not waive new subscription upgrades, overages, setup, cleanup, or uncertain charges. The cash ceiling is not presented as a valuation of owner time or a proof of lower total economic cost. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [Analysis: Human attention and cost boundaries](ANALYSIS.md#human-attention-and-cost-boundaries))

### Cutoff cannot add scored time

At the deadline, the plan prohibits additional scored task work or grading to finish a late result. Pending disputes cannot be promoted to accepted outcomes. Shutdown, evidence retention, cleanup, and classifications for pending or in-flight work still require a protocol, but that open procedure cannot extend the scored phase. New cleanup charges remain within USD 100. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification), [Open question O14](DECISIONS.md#open-questions))

Later rescue requires separate authorization. If retained within this pilot, its new charges still count toward USD 100 and it cannot extend scoring. A separately approved follow-on must be separately identified and cannot retroactively expand this pilot's allowance or repair its score. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits))

### Enforcement and feasibility boundaries

The plan retains admission checks against spent, committed, reserved, and in-flight charges, with capacity reserved for safe termination and evidence retention. It prohibits launching activity whose charge cannot be bounded within the remaining allowance. Rates, allocation, reconciliation, storage retention, and non-overlapping reservations remain genuine implementation questions rather than exclusions from the cap. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits), [Open question O15](DECISIONS.md#open-questions))

The package does not claim that all selected suites, scenarios, both stages, repeats, and judging fit the limits or support a statistically adequate comparison. It preserves predeclared subset proposals or deferral rather than silently weakening controls, dropping difficult tasks, or extending the pilot. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))

B01, B06, and B10 remain the selected benchmarks; A01, A03, A05, A08, A09, A11, and A12 remain the selected scenarios. No compensated tradeoff, useful-work rediscovery, direct main update, or runtime authorization is introduced. Original PR #3 remains the documented publication route. ([README.md](README.md), [DECISIONS.md](DECISIONS.md))

## Nonblocking decisions before execution

The documentation may ship while these protocol details remain open:

- Define the recorded dispatch event, deadline enforcement, task admission headroom, and cancellation of in-flight work. Setup and calibration must remain separate from scored solving and holdouts.
- Predeclare treatment of pending, in-flight, unstarted, and disputed work at cutoff, including required evidence. Do not hide assigned failures, complete late scoring, or convert missing judgments into passes.
- Specify safe shutdown, evidence retention, and cleanup, with finite retention and termination arrangements covered by reservations. Any later observation or follow-on activity must not silently become extra scored evaluation.
- Pin billing rates and a non-overlapping reservation/reconciliation ledger. Include setup, both judges, storage, cleanup, applicable new billing charges, and delayed invoices; uncertain charges are not presumed free.
- Set numeric task/class allocations, sample design, two-judge configurations, owner response procedures, exact templates, comparator settings, and supplemental cases within the fixed boundaries.
- Complete whole-stack security qualification and obtain separate execution and spending authorization. The cost and clock decisions alone do not supply that authority.

These are implementation details within settled D28/D29, not permission to reopen the first-dispatch start, pause owner waits, exclude new setup or cleanup charges, or increase the scored allowance. ([Decision log: Open questions](DECISIONS.md#open-questions), [PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `914c7ac214e22caf069937ba1c1535e3c98b98cbf6dd6cde104adcf69fdd1a4a` |
| `PLAN.md` | `e2d04e4d97808c86c26a8dfc129da2629f1ec3ecf831adfe88dd2d336abbc0aa` |
| `BENCHMARKS.md` | `01db4032f2eab19729d1be11b971fc87192cdd280aa731e4796909b1325832f9` |
| `ANALYSIS.md` | `187727e2be21eb0c4e7809ef41c55e5f56e1d57585c658fe3bfe2c383e8d3da3` |
| `DECISIONS.md` | `42315718321e596ea58d43bc2cf42c717f8ba3aa8942e7aed815e5eafd769ce9` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to substantive documents require renewed review.

## Limits

- This is an independent read-only document review, not execution or expenditure approval, runtime certification, a benchmark result, or a guarantee of improved outcomes.
- I performed no installation, benchmark execution, model runtime test, penetration test, implementation audit, cost simulation, or feasibility trial. None is required for this documentation-only change.
- I did not run or certify repository gates. They remain the integrating agent's separate responsibility.
- No external research was performed for this owner-decision update. Earlier source checks were selective, not exhaustive verification of every benchmark, license, dependency, or execution requirement.
- Fidelity was assessed against supplied owner decisions and review context, not an independently authenticated transcript of every historical discussion.
- I did not change or independently verify the remote state of PR #3, either branch, or main.

**Final disposition: SHIP the fingerprinted documentation through the existing PR workflow, subject to separately run repository gates. No pilot execution or expenditure is authorized.**
