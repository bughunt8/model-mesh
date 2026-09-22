# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 22 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker was found in the acceptance, repair-feedback, and resource-cap update. The package faithfully records decisions D19 through D21 while retaining the previously settled comparison stages, bounded repair, no-human-rescue rule, no compensated regressions, and prohibition on runtime authorization. This verdict applies to the five substantive document versions fingerprinted below. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [BENCHMARKS.md](BENCHMARKS.md), [DECISIONS.md](DECISIONS.md), [README.md](README.md))

## Scope and method

I reviewed the uncommitted documentation changes on local branch `evaluation-1`, based on HEAD `83b57cfed3a6cc7737482caa2792f94d2b4a63a8`. That commit identifies the baseline, not the new working-tree content.

I inspected the complete diff to all five substantive documents and checked related acceptance, severity, cosmetic, feedback, cap, rescue, uncertainty, and claim language across the package. I verified that the committed baseline of each substantive document exactly matches its fingerprint in my preceding bounded-repair review.

I made no target-file or branch changes. I authored this report outside the repository for incorporation as `REVIEW.md`. It replaces the prior attestation while preserving its review history.

## Prior review history

The original two-document review returned REVISE with three substantive findings. The corrected two-document package then received SHIP for documentation only. A subsequent independent review of the expanded package, including analysis and decision log, also returned SHIP. The next review assessed D14 through D18 and returned SHIP for the bounded-repair documentation. None of those reviews approved execution or certified runtime safety or effectiveness.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording allowed prohibited tradeoffs and weakened mandatory controls. | High | Resolved. All mandatory controls and evidence are required, no objective regression may be compensated by another improvement, and uncertainty is inconclusive without a silently authorized regression margin. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. These inputs remain settled, useful-work discovery is deferred, and remaining questions concern genuine protocol details. ([Plan: Measurement interview](PLAN.md#measurement-interview), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review did not adequately cover the surrounding execution stack. | High | Resolved. Installer, coordinator, evaluator, simulated users, services, and worker remain within the qualification boundary. Inability to meet policy requires deferral rather than an upstream-instruction exception. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The expanded-package review established consistency of benchmark/scenario selections, explicit coverage gaps, cautious causal attribution, cost-accounting boundaries, and the separation of reviewed specifications from measured results and adoption claims. These protections remain in place. ([BENCHMARKS.md](BENCHMARKS.md), [ANALYSIS.md](ANALYSIS.md))

D14 through D18 remain intact: method effect is assessed before routing effect in separate comparisons; defect scoring concerns the frozen final artifact after at most one repair; human rescue is prohibited during scored work; and later separately authorized rescue cannot replace a frozen failed outcome. Final-evaluator information cannot reopen repair or contaminate another scored attempt, and rescue expenditure remains separately disclosed. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [Analysis: Human attention and cost boundaries](ANALYSIS.md#human-attention-and-cost-boundaries), [Decision log](DECISIONS.md))

## Current findings

**No new substantive blockers.**

### Repair feedback and comparison isolation

D19 permits both executable checks and agent review without exposing hidden final-evaluator information through either channel. Visible checks, review prompts, and delivery mechanisms remain to be pinned, and the plan expressly avoids fabricating automated coverage where no executable check applies. These are implementation details still awaiting a protocol, not a retreat from the selected feedback categories. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [Decision D19](DECISIONS.md#settled-decisions))

The analysis requires the repair-reviewer configuration to remain constant during the method-effect comparison. Any reviewer-role routing change in stage two must be declared as treatment, while final grading stays independent and matched. It correctly distinguishes equal feedback-access rules from identical feedback content on different outputs. ([Analysis: Define defects before optimizing anything](ANALYSIS.md#define-defects-before-optimizing-anything))

### Strict task acceptance without moving criteria

D20 is reflected consistently: every confirmed defect, including cosmetic defects, fails final task acceptance; mandatory safety failures remain disqualifying. Cosmetic requirements must be frozen before scored execution, so an evaluator cannot introduce new aesthetic preferences after observing an output. Severity labels are explanatory rather than exemptions from failure. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [Decision D20](DECISIONS.md#settled-decisions))

The documents distinguish confirmed deviations from unsupported or disputed findings, prohibit treating unresolved findings as a default pass, and leave adjudication procedures explicitly open. They do not present a zero-confirmed-defect observation as proof of universal correctness or absence of undiscovered defects. ([Plan: Final task acceptance](PLAN.md#final-task-acceptance), [Analysis: Define defects before optimizing anything](ANALYSIS.md#define-defects-before-optimizing-anything))

The official benchmark grade remains separate from stricter local acceptance, so an official pass cannot override a confirmed cosmetic defect or policy breach. Escaped-defect and reviewer-effectiveness metrics now include cosmetic defects and preserve severity breakdowns, consistent with the acceptance rule. ([BENCHMARKS.md](BENCHMARKS.md), [Plan: Candidate measurement dictionary](PLAN.md#candidate-measurement-dictionary))

### Predeclared resource classes

D21 specifies scenario or difficulty classes rather than post-outcome budget choices. Class definitions and assignment are established before scored execution, the same task receives identical caps across competing arms, and failed or expensive tasks cannot be reclassified to obtain a larger allowance. Numeric limits remain undecided. ([Plan: Isolate the method and routing effects](PLAN.md#isolate-the-method-and-routing-effects), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification), [Decision D21](DECISIONS.md#settled-decisions))

The single repair remains inside the total task envelope rather than receiving a fresh allocation after initial work. Class-specific results must remain visible so that a different task mix cannot conceal regression. This preserves matched comparisons without pretending that the numeric resource protocol is already complete. ([Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))

### Scope and evidence boundaries

The update does not add a first-handoff quality target, human coaching, an extra repair cycle, a compensated tradeoff, or a universal performance claim. B01, B06, and B10 remain the selected benchmarks, and A01, A03, A05, A08, A09, A11, and A12 remain the selected scenarios. The original PR workflow and execution prohibition remain explicit. ([README.md](README.md), [PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))

## Nonblocking decisions before execution

The documentation may ship while these required protocol details remain open:

- Freeze correctness and cosmetic criteria per scenario, including reproducible examples and how equivalent acceptable presentations are handled. Decide adjudication ownership, disputed findings, unresolved outcomes, and the observation window without exempting confirmed minor defects.
- Pin visible checks, repair-review prompts, reviewer configurations, channel access, and independent final grading. Preserve stage-one matching and declare any stage-two reviewer routing treatment.
- Define class taxonomy and pre-execution assignment procedure; set numeric time, token, monetary, tool-call, concurrency, and retry caps covering initial work plus the one repair.
- Pre-register task allocation, repeats, uncertainty standards, stopping rules, exclusions, and class-specific reporting without inventing statistical proof or allowing unauthorized regression margins.
- Finalize operational, experimental, setup, and rescue accounting, including the total-cost horizon and attention allocation.
- Pin benchmark releases, subsets, evaluators, models, adapters, and policies; qualify the whole execution boundary; design supplemental coverage cases; obtain separate execution authorization.

These are unresolved protocol details, not permission to renegotiate the settled feedback categories, every-defect failure rule, class-based cap structure, one-repair limit, or no-human-rescue instruction. ([Decision log: Open questions](DECISIONS.md#open-questions), [PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `01e2a17faa000f423285b00f81feee4099ea13fd65e9199c238b27e8b59f50da` |
| `PLAN.md` | `3dbd0ea181fe2134d8df5fce8015e202a11997d5d76e275187a07dcd2966b7de` |
| `BENCHMARKS.md` | `1051d19dafa8a277fdc0b78abb34feb064008efb90cfade4bcd1827e7950deec` |
| `ANALYSIS.md` | `475754c14191a6b84c1b437da8417984c294b1d4d2790ffd5b7a492a23a697d2` |
| `DECISIONS.md` | `a5c3a7a8ffdb3fa4c27566edc52f009bd8558d6cf2f44c9ae6c59648a74bf2fc` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to the substantive documents require renewed review.

## Limits

- This is an independent read-only documentation review, not execution approval, runtime certification, a benchmark result, or a guarantee of safety or improved outcomes.
- I performed no installation, benchmark execution, model runtime test, penetration test, or implementation audit. None is required for this documentation-only change.
- I did not run or certify repository gates. They remain the integrating agent's separate responsibility.
- No external re-research was performed for this owner-decision update. Earlier citation verification was selective and does not certify every benchmark description, license, dependency, or execution requirement.
- Fidelity was assessed against supplied owner decisions and review context, not an independently authenticated transcript of every historical discussion.
- I did not change or independently verify the remote state of PR #3, either branch, or main.

**Final disposition: SHIP the fingerprinted documentation through the existing PR workflow, subject to separately run repository gates. No pilot execution is authorized.**
