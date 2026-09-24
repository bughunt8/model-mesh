# Evaluation 1 independent adversarial review

**Verdict: SHIP for documentation only.**

Review date: 25 September 2026, Hong Kong time.

Reviewer: Independent read-only adversarial review agent.

No substantive blocker or required correction was found in D42. The five documents consistently limit initial task material to eligible public and synthetic inputs, retain separate permissions and controls, and prohibit treating the resulting evidence as demonstrated performance on confidential client work. ([README.md](README.md#settled-scope), [PLAN.md](PLAN.md#public-and-synthetic-task-data-boundary), [BENCHMARKS.md](BENCHMARKS.md#rules-already-settled), [ANALYSIS.md](ANALYSIS.md#what-the-evaluation-can-establish), [DECISIONS.md](DECISIONS.md#settled-decisions))

## Scope and method

I inspected the complete uncommitted diff across the five substantive documents on local branch `evaluation-1`, based on HEAD `9299b381621077d822be0c42fb8dc56d1b4caaa5`. That commit identifies the baseline, not the reviewed working-tree content.

I checked the changes against the supplied D42 owner choice, read the preceding review, and examined related data, credential, evidence, incident, permission, claim, and open-question language. All five committed baseline documents match the fingerprints in the preceding D41 review. Unchanged rules were reviewed through that verified baseline and relevant current passages, rather than treating this update as a new external-source audit.

I made no target-file, branch, or git-state changes. This report was authored outside the repository for incorporation as `REVIEW.md`.

## Prior review history

The original two-document review returned REVISE for R1 through R3. Their corrections received SHIP for documentation only, as did the expanded package and subsequent owner-decision reviews through D41. Earlier nonblocking wording notes were corrected and independently rechecked. None of those verdicts certified runtime behavior or authorized execution.

| Finding | Original severity | Current disposition |
|---|---|---|
| R1: Adoption wording allowed compensated regressions and weakened mandatory controls. | High | Resolved. Mandatory controls and evidence remain required, no objective regression can be compensated by another improvement, and uncertainty cannot silently pass. ([Plan: Comparison and uncertainty](PLAN.md#comparison-and-uncertainty)) |
| R2: Discovery questions reopened settled purpose, usefulness, and priorities. | Medium | Resolved. Client purpose and priorities remain fixed; useful-work discovery remains deferred. ([Plan: Agreed priorities](PLAN.md#agreed-priorities), [DECISIONS.md](DECISIONS.md)) |
| R3: Benchmark privilege review omitted parts of the execution stack. | High | Resolved. Installers, coordinators, evaluators, simulated users, tools, and workers share the mandatory boundary; unmet controls require deferral rather than waiver. ([Plan: Before execution](PLAN.md#before-execution), [Benchmark evidence rules](BENCHMARKS.md#how-benchmark-evidence-will-count)) |

The selected suites remain B01 SWE-bench Verified, B06 GAIA, and B10 TheAgentCompany; the original twelve scenarios and ten benchmark options remain recorded, with supplemental coverage gaps rather than claims of complete standardized coverage. ([BENCHMARKS.md](BENCHMARKS.md))

The previously reviewed decisions remain in force:

- D14 through D18 establish method-first and routing-second comparisons, final post-repair scoring, at most one repair within matched caps, no scored human rescue, frozen failures, and separately authorized unscored rescue that cannot rewrite outcomes. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D19 through D25 retain checks plus agent-review feedback without hidden evaluator information, failure for any confirmed defect including cosmetic defects, matched class-based caps, exact templates with advance exceptions, two independent final AI judges, and personal owner dispute resolution after artifact freeze. ([PLAN.md](PLAN.md), [DECISIONS.md](DECISIONS.md))
- D26 through D29 retain the continuous 10-hour clock from first scored dispatch and the global USD 100 ceiling for all new pilot model/tool/compute charges, including setup and cleanup, without hidden pre-clock solving or spending authority. ([Plan: Pilot-wide time and cash limits](PLAN.md#pilot-wide-time-and-cash-limits))
- D30 through D33 retain the eight-minute dispute window capped by the global deadline, unresolved/not-accepted timeout outcomes, minimum breadth before depth, whole-pilot coverage with stage-local matched claims, and all active owner attention without duplicated minutes. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md))
- D34 through D37 retain fourteen distinct underlying cases across the pilot, two per selected scenario, timer-plus-log attention recording, distinct tasks without a different-context requirement, and missing rather than estimated or zero forgotten intervals. No missing-data analysis exception is currently agreed. ([PLAN.md](PLAN.md), [ANALYSIS.md](ANALYSIS.md), [DECISIONS.md](DECISIONS.md))
- D38 through D40 retain two routine cases per scenario and both matched arms on each case, with each scenario pair kept in one stage. Method covers A01/A03/A05/A09; routing covers A08/A11/A12, giving eight and six cases respectively, fourteen matched comparisons and twenty-eight initial attempts before repeats, not twenty-eight independent tasks or a powered sample. ([Plan: Agree the experiment](PLAN.md#agree-the-experiment), [Analysis: Resource-cap classification](ANALYSIS.md#resource-cap-classification))
- D41 continues only the predeclared comparisons after ordinary acceptance failure in any arm, retaining frozen outcomes with no extra repairs, replacements, tuning, or hidden-grader feedback. Safety and resource stops override continuation, which is neither acceptance nor adoption or execution approval. ([Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [DECISIONS.md](DECISIONS.md))

## Current findings

### The task-content restriction matches the owner choice

D42 permits eligible public benchmark tasks, public repository content, and fabricated business data while excluding private project material, client information, personal records, and real account credentials from task content. It applies to preparation, prompts, snapshots, attachments, supplemental cases, retrieval, tool responses, simulated users, repair review, final judging, and derived task evidence. Private examples and calibration fixtures are not exceptions. ([Plan: Agreed priorities](PLAN.md#agreed-priorities), [Plan: Public and synthetic task-data boundary](PLAN.md#public-and-synthetic-task-data-boundary), [DECISIONS.md](DECISIONS.md#settled-decisions))

The plan prohibits copying excluded records and merely changing names to label them synthetic. It requires fabricated business documents and disposable simulated accounts, not the owner's or a client's real account state. The analysis likewise requires genuinely fabricated fixtures rather than copied excluded records. ([PLAN.md](PLAN.md#public-and-synthetic-task-data-boundary), [ANALYSIS.md](ANALYSIS.md#what-the-evaluation-can-establish))

### Eligibility is separate from public availability and evaluator access

The case manifest must record provenance, permitted use, and exclusion screening before runs. A public label or URL does not override excluded content or real-secret screening, and cases that require prohibited material or cannot be qualified must be deferred for a scope decision. Transforming a case requires advance declaration and cannot retain an unchanged official-benchmark identity by assertion. ([PLAN.md](PLAN.md#public-and-synthetic-task-data-boundary), [BENCHMARKS.md](BENCHMARKS.md#rules-already-settled))

Eligible source material does not make holdout answers worker-visible. Hidden answers and evidence remain protected, supplemental answers stay out of worker context, and public source status does not establish model-level novelty or absence of contamination. ([PLAN.md](PLAN.md#public-and-synthetic-task-data-boundary), [BENCHMARKS.md](BENCHMARKS.md#how-benchmark-evidence-will-count))

### Public content is not trusted code or general permission

Public and synthetic material remains untrusted input and cannot grant permissions or bypass recipient, network, secret, or execution controls. Whole-stack qualification, sandbox and privilege restrictions, and recipient approval remain applicable; this selection does not authorize access, uploads, provider calls, or real-account actions. ([Plan: Agreed priorities](PLAN.md#agreed-priorities), [Plan: Before execution](PLAN.md#before-execution), [Plan: Public and synthetic task-data boundary](PLAN.md#public-and-synthetic-task-data-boundary))

### Service authentication and operational records are distinct

The plan distinguishes separately approved scoped runtime-authentication credentials from task material and keeps them outside model context, task files, and ordinary telemetry. This is not permission to obtain credentials or use real accounts. Operational metadata and owner attention records retain their own access and retention controls rather than becoming public merely because the tasks are public. ([PLAN.md](PLAN.md#public-and-synthetic-task-data-boundary), [ANALYSIS.md](ANALYSIS.md#what-the-evaluation-can-establish))

### Excluded content triggers incident handling, not D41 continuation

Unexpected excluded content requires stopping the affected access or transmission path under the incident procedure, without forwarding it to reviewers or judges or repeating it in ordinary logs. This does not waive the broader mandatory-control stop rules; D41 cannot be used to relabel a control incident as ordinary task failure. ([Plan: Public and synthetic task-data boundary](PLAN.md#public-and-synthetic-task-data-boundary), [Plan: Bounded repair and final evaluation](PLAN.md#bounded-repair-and-final-evaluation), [ANALYSIS.md](ANALYSIS.md#what-the-evaluation-can-establish))

### Open questions and client claims remain bounded

O06 and the later measurement questions now ask how to screen exact eligible cases and approve recipients, jurisdictions, retention, credential controls, and tools, rather than reopening the selected task-data classes. Successful public/synthetic cases do not establish performance on confidential client work, and any later private-data evaluation needs separate scope and approval. ([DECISIONS.md](DECISIONS.md#open-questions), [DECISIONS.md](DECISIONS.md#superseded-or-constrained-proposals), [Plan: Measurement interview](PLAN.md#measurement-interview), [ANALYSIS.md](ANALYSIS.md#what-the-evaluation-can-establish))

The plan advances to v0.16 while retaining the 25 September decision date, and the benchmark research still identifies its separate 22 September review date. No new external research or benchmark result is implied by D42. ([PLAN.md](PLAN.md), [BENCHMARKS.md](BENCHMARKS.md#ten-researched-benchmark-options), [DECISIONS.md](DECISIONS.md))

## Nonblocking details before execution

These are execution prerequisites, not blockers to the documentation PR:

- Define exact screening criteria and evidence for eligible public sources, fabricated fixtures, permitted use, attachments, retrieved material, and derived artifacts.
- Specify trusted intake and tool-response handling, incident containment, restricted evidence retention, and safe termination without forwarding excluded content to a model for diagnosis.
- Approve provider endpoints, tools, recipients, jurisdictions, retention, service-secret handling, and access to operational and attention records.
- Select qualified routine cases under D40 without silent replacements or weakened coverage; return for an owner scope decision if D42 makes the floor infeasible.
- Freeze comparator and judge configurations, templates, visible feedback, case manifests, task caps, repeats, reservations, cutoff classifications, and measurement procedures.
- Complete whole-stack qualification and obtain separate execution authority within the settled clock and cash limits.

The decision log retains these unresolved qualification, protocol, measurement, and permission matters without changing the settled task-data scope or promising feasibility. ([Decision log: Open questions](DECISIONS.md#open-questions), [PLAN.md](PLAN.md))

## Reviewed document fingerprints

SHA-256 values are relative to `docs/research/evaluation-1/`:

| Document | SHA-256 |
|---|---|
| `README.md` | `e6cad972b730c3c247f5f9b9d3c6644ca4665c6067460ee5acf853b5d23b2719` |
| `PLAN.md` | `81155b2602f4020acf3c6f1f4f871716b06ba6a8af7cfe36c4d90558e055c514` |
| `BENCHMARKS.md` | `408756534764ec87190b4cfa7207a80e5889317c76814b8ed9288b3bbd5bd192` |
| `ANALYSIS.md` | `76192cd46d0354804b326419eb01920fc1ff685b3181adaf7b929da680e32eae` |
| `DECISIONS.md` | `1efbfb5d279bfb6e2764273df99631dfd8000b26e66f7e7c4a77ce1db483c2d7` |

`REVIEW.md` is excluded to avoid a self-referential hash. Material changes to substantive documents require renewed review.

## Limits

- This is a read-only documentation review, not a runtime certification, privacy or license clearance, benchmark result, execution or expenditure approval, or guarantee of improved outcomes.
- No case contents, repositories, datasets, provider policies, or synthetic fixtures were newly inspected for actual D42 eligibility. The screening procedure is proposed, not implemented or exercised.
- No installation, benchmark execution, model runtime test, penetration test, timing trial, cost simulation, or feasibility trial was performed. None is required for this docs-only update.
- Repository gates were not run or certified. The integrating agent remains responsible for them before updating the original PR.
- No new external research was performed. Earlier source checks were selective, not exhaustive verification of all benchmark, dependency, license, or execution requirements.
- Fidelity was assessed against supplied owner decisions and review history, not an independently authenticated transcript of every discussion.
- No remote PR or branch state was independently verified or changed.

**Final disposition: SHIP the fingerprinted documentation through the existing PR workflow, subject to separately run repository gates. No pilot execution or expenditure is authorized.**
