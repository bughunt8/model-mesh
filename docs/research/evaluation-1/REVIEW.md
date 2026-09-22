# Evaluation 1 independent adversarial review

**Verdict: SHIP — documentation only.**
**Review date:** 22 September 2026 (Hong Kong time)
**Reviewer:** Independent read-only adversarial review agent

No substantive blocker remains in the expanded documentation package. The prior corrections are preserved, and the new analysis and decision log are consistent with the settled priorities, selected scope, evidence limits, and prohibition on execution authorization. This verdict is limited to the five substantive document versions fingerprinted below. ([PLAN.md](PLAN.md), [BENCHMARKS.md](BENCHMARKS.md), [ANALYSIS.md](ANALYSIS.md), [DECISIONS.md](DECISIONS.md), [README.md](README.md))

## Scope and method

I reviewed the five substantive documents and the existing review-history placeholder in `docs/research/evaluation-1/`. I read the new index, analysis, and decision log in full, and inspected the complete changes to the plan and benchmark document against the two-document versions I had previously reviewed. I verified that those baseline versions had exactly the hashes recorded in my earlier SHIP assessment.

The local review was performed on branch `evaluation-1`, with base HEAD `a87fe04264b7fa1484ab9694f4baeb4fe2b8eda8`; the expanded package was an uncommitted working-tree proposal at review time. The hashes below identify the actual content reviewed rather than implying that the base commit already contained it.

The review focused on methodological defects, contradictory instructions, unauthorized tradeoffs, evidence and causality, comparison design, coverage, versioning, privilege boundaries, and decision-log consistency. I did not modify any target document or branch. I authored this report outside the repository for incorporation as `REVIEW.md`.

## Prior findings and disposition

| Finding | Original severity | Disposition in the expanded package |
|---|---|---|
| R1 — The proposed adoption rule allowed attention or cost gains to compensate for quality regression and weakened mandatory safety gates. | High | **Resolved.** Adoption requires all mandatory controls, complete evidence, and no accepted regression in any of the four objectives; uncertainty is inconclusive and does not authorize a positive regression margin. These requirements remain explicit in the plan and analysis. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty), [Analysis: Enforce the no-trade-off instruction](ANALYSIS.md#enforce-the-no-trade-off-instruction)) |
| R2 — Mandatory interview questions reopened the settled business purpose, usefulness, priorities, and actual-project discovery. | Medium | **Resolved.** Settled inputs are recorded, actual project examples are not required at this stage, and remaining questions concern definitions, adjudication, comparator, attention, and evidence. The decision log records useful-work discovery as deferred. ([Plan: Measurement interview](PLAN.md#measurement-interview), [Decision log](DECISIONS.md)) |
| R3 — Benchmark privilege review did not adequately cover the evaluator and surrounding execution stack. | High | **Resolved.** The boundary covers installers, coordinators, evaluators, simulated users, tool servers, and workers. Upstream privileged instructions do not authorize unsafe operations on the user/shared host. Necessary privilege within a separately approved disposable boundary requires qualification; inability to satisfy policy means deferral. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count), [Analysis: Security feasibility](ANALYSIS.md#security-feasibility-is-part-of-benchmark-selection)) |

## Expanded-package findings

**No new substantive blockers.**

1. **Selected scope is consistent.** The package retains B01 SWE-bench Verified, B06 GAIA, and B10 TheAgentCompany, alongside A01, A03, A05, A08, A09, A11, and A12. The full twelve-scenario and ten-benchmark menus remain available for traceability; unselected alternatives are not silently added. ([README.md](README.md), [Selected scope and coverage](BENCHMARKS.md#selected-scenarios-and-coverage-gaps), [Decisions D09–D11](DECISIONS.md#settled-decisions))

2. **Coverage is not overstated.** Refactoring, security audit/remediation, and architecture planning need supplemental cases rather than relabeled public-benchmark results. GAIA and TheAgentCompany task coverage remains conditional on inspecting suitable subsets, and supplemental construction is expressly a proposal rather than an approved or completed experiment. ([Benchmark coverage table](BENCHMARKS.md#selected-scenarios-and-coverage-gaps), [Analysis: Coverage](ANALYSIS.md#coverage-across-selected-scenarios))

3. **Causal comparisons are appropriately constrained.** The analysis distinguishes controlled method/routing comparisons from whole-system comparisons, handles human-led or already-multimodel baselines without falsely attributing a method effect, and distinguishes scenario labels from future comparison-arm labels. ([Analysis: Distinguish the experiment's causes](ANALYSIS.md#distinguish-the-experiments-causes))

4. **Measurement risks receive substantive treatment.** The analysis distinguishes severity-specific defects, incomplete work, false acceptance, escaped defects, and safe refusals. Its separate operational, independent-evaluation, and setup/qualification ledgers reduce the risk of hiding routine reviewer effort or adoption costs. Measurement resolution and an evidence standard remain unresolved without granting permission for compensated regressions. ([Analysis: Defects](ANALYSIS.md#define-defects-before-optimizing-anything), [Analysis: Attention and cost](ANALYSIS.md#human-attention-and-cost-boundaries), [Analysis: No tradeoffs](ANALYSIS.md#enforce-the-no-trade-off-instruction))

5. **Decision and evidence boundaries remain intact.** The decision log separates owner selections from recommendations and unresolved protocol decisions. The claim ladder does not turn reviewed documentation, repository checks, or historical project success into runtime certification, universal effectiveness, or causal evidence. ([DECISIONS.md](DECISIONS.md), [Analysis: Proposed claim ladder](ANALYSIS.md#proposed-claim-ladder))

6. **Repository intent is consistent with the requested workflow.** The package specifies `evaluation-1`, retention of original PR #3, synchronization of the existing PR head branch to the reviewed commit, and no direct main update or replacement PR. This is a documented procedure, not my attestation that any remote branch or PR has already been updated. ([README.md](README.md), [Decisions D12–D13 and change protocol](DECISIONS.md))

## Nonblocking decisions required before execution

The following are legitimate open protocol decisions, not reasons to withhold a documentation-only SHIP:

- Select the comparator and claim type; preserve the distinction between absolute qualification, controlled component effects, and whole-system differences.
- Freeze scenario-specific defect definitions, severity thresholds, denominators, adjudication ownership, refusal/incompletion handling, and observation windows.
- Agree the statistical evidence standard, measurement resolution, sample allocation, repeats, stop rules, and treatment of inconclusive comparisons without silently introducing regression allowances.
- Set operational-versus-experimental accounting rules and the scope, time horizon, and allocation of setup and qualification costs.
- Pin accessible benchmark releases, splits, subsets, environments, graders, simulators, and adapter/model/policy configurations.
- Qualify the complete execution boundary, including TheAgentCompany's installation and evaluation stack, and obtain separate execution authorization with permissions and resource limits.
- Specify and independently grade supplemental A03, A05, and A09 cases; defer project-case selection and publication permissions until requested.

These unresolved items are already identified in the package and must be completed through the later protocol rather than inferred from this review. ([Decision log: Open questions](DECISIONS.md#open-questions), [PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))

## Reviewed document fingerprints

SHA-256 of the five substantive documents, relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `c65a29de392882aaf826dfa9e08eaf1431c36841abe3de71dafb84b4871b2978` |
| `PLAN.md` | `2d4ad13ff44b6d86dc1a538e1b8d18a5789c05da238ca82e79c1f5d809c689d3` |
| `BENCHMARKS.md` | `9dce198cac144884c673d2e7f7b7f6351a3524f169e83c3914f0b7b331967b07` |
| `ANALYSIS.md` | `925ab14d16cea5c498e15210e8ef268eb739394966c794ca0ff42672400cee3a` |
| `DECISIONS.md` | `4fba927566d63a243340e64815832c0f4e9287718b6cf09d4a3efbfc19669f94` |

`REVIEW.md` is intentionally excluded from the fingerprint set to avoid a self-referential hash. Incorporating this reviewer-authored report does not change the reviewed substantive documents. Material changes to those documents require renewed review.

## Limits of this attestation

- This is an independent document review, not an execution-ready protocol approval, security certification, benchmark result, production adoption decision, or performance guarantee.
- I performed no installation, model runtime test, benchmark execution, penetration test, or implementation audit. None is required to approve the documentation-only scope.
- Repository gates are separate and are to be run by the integrating agent. I did not run or certify their results.
- Source checking was selective in the earlier review, not an exhaustive verification of every benchmark description, license, release, dependency, or transitive privilege requirement. I did not re-research every citation for this expansion. The previously checked privilege concern is supported by [TheAgentCompany's published setup and evaluation instructions](https://github.com/TheAgentCompany/TheAgentCompany).
- I checked decision-log consistency against the supplied owner instructions and review context, not an independently authenticated transcript of every historical decision.
- I did not update or independently verify the remote state of PR #3, either branch, or main.

**Final disposition: SHIP the reviewed documentation package through the existing PR workflow, subject to the separately run repository gates. No pilot execution is authorized by this disposition.**
