# Elephant-Goldfish Model compared with model-mesh

This is the study behind [REVIEW-PANEL.md](../../REVIEW-PANEL.md). EGM is Apache-2.0. Text here is original and quotes only short phrases. No EGM text or prompts were copied into model-mesh.

Date: 2026-10-26. Scope: [google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model) (EGM, Apache-2.0, 9 commits from 2026-10-21 to 2026-10-23, read from a local clone). Evidence is marked as repo fact or judgement. I read the seven skills, the nine agent personas, the Claude and Codex integration docs, the harness guide, TESTING.md, the unit tests, the CI workflows, the PR template and AI_POLICY. I skimmed the design docs and did not read the Rensin essay.

## What EGM is

EGM is a design-stage review protocol, not a routing system. The flow is brainstorm, draft, review, resolve, with drift reporting and README bootstrap as side skills ([skills/](https://github.com/google/elephant-goldfish-model/tree/main/skills)).

- Elephant: the long-context session that holds the history and writes the artifact.
- Goldfish: a fresh subagent with no conversation history, given a persona from [agents/](https://github.com/google/elephant-goldfish-model/tree/main/agents) and a standard from [resources/document_standards/](https://github.com/google/elephant-goldfish-model/tree/main/resources/document_standards).
- Review pipeline: [egm_review](https://github.com/google/elephant-goldfish-model/blob/main/skills/egm_review/SKILL.md) runs stages 5 to 9 in order (zoom-out, comprehension, critic, intermediate zoom-out, implementation readiness). Reviewers run in parallel only within a stage.
- Aggregation: [agents/synthesizer.md](https://github.com/google/elephant-goldfish-model/blob/main/agents/synthesizer.md) collects free-text findings, deduplicates them and groups them as Blocker, Major or Nit.
- Brainstorm: six lenses run in parallel (contrarian, cost, UX, migration, SRE, tech debt) ([egm_brainstorm](https://github.com/google/elephant-goldfish-model/blob/main/skills/egm_brainstorm/SKILL.md)).
- Packaging: one repo ships manifests for Claude Code, Cowork, Codex, ChatGPT and Antigravity ([docs/harnesses.md](https://github.com/google/elephant-goldfish-model/blob/main/docs/harnesses.md)).
- Tests: tier 1 offline checks cover frontmatter, link integrity, a 24,000-byte skill body cap (the cap is Antigravity's, per the test message) and one `test_scenarios.yaml` per skill. Opt-in live runs record harness version, date and result in [TESTING.md](https://github.com/google/elephant-goldfish-model/blob/main/TESTING.md).

## The central difference

Repo fact: EGM reviewer adapters declare `model: inherit` ([.claude-plugin/agents/zoom_out.md](https://github.com/google/elephant-goldfish-model/blob/main/.claude-plugin/agents/zoom_out.md)). A reviewer therefore runs the same model and the same harness as the author. EGM isolates by context and tools: reviewers get read-only tools, no parent transcript and no CLAUDE.md ([docs/claude.md](https://github.com/google/elephant-goldfish-model/blob/main/docs/claude.md)). The doc says this is not filesystem isolation. The interactive review preset also runs checkpoint gates between stages ([egm_review](https://github.com/google/elephant-goldfish-model/blob/main/skills/egm_review/SKILL.md)).

Before this change model-mesh isolated by harness and model family and said little about context hygiene. The two rules cover different failure modes, so they combine without conflict.

## Do multiple angles work?

Judgement, not measured. I found no measured defect-detection rate or false-positive data in the repo. Its design doc labels each `test_scenarios.yaml` an evaluation benchmark for precision and recall ([docs/designs/review.md](https://github.com/google/elephant-goldfish-model/blob/main/docs/designs/review.md)), but the example file I read holds pattern assertions, not rates. Its claim that context-free review reduces hallucinations ([docs/index.md](https://github.com/google/elephant-goldfish-model/blob/main/docs/index.md)) is asserted. The tests check protocol compliance with regex assertions, not review quality.

- Coverage: yes, plausibly. Different rubrics prompt different questions, which finds different classes of defect.
- Independence: no. Six lenses on one model share training biases, so they tend to agree on the same blind spots. A same-family reviewer can look thorough while repeating the author's error.
- Noise: a stage runs one or three reviewers, and the synthesizer can launch two instances of each, so up to six reviews per stage ([agents/synthesizer.md](https://github.com/google/elephant-goldfish-model/blob/main/agents/synthesizer.md)). The findings overlap, and the dedupe step is an LLM summarising free text.

Working position: lens count adds breadth and family count adds independence. Treat them as separate axes.

## Scaling

- EGM scales by nesting. Claude Code allows a synthesizer to spawn reviewers up to 3 levels deep. Cowork cannot nest, so the main context dispatches directly. Bootstrap spawns sub-orchestrators per subtree, unbounded once the user approves ([bootstrap design](https://github.com/google/elephant-goldfish-model/blob/main/docs/designs/bootstrap.md)).
- Gaps: no cost model, no per-run fan-out budget, no rule for choosing the number of lenses, and an aggregator that shares the author's model.
- model-mesh has profile cost caps but no lens fan-out. Crossing lenses with families multiplies cost, so a budget per situation tier is required.

## Proposed improvements, in priority order (as built)

1. Zero-context reviewer contract. Add to docs/ORCHESTRATION.md: reviewers receive only the artifact, the standard and explicit context, with read-only tools and no parent transcript or instruction files. This is cheap and orthogonal to the existing independence rule.
2. Lens library mapped to reviewer seats. Define named lenses and let each reviewer seat be lens times family. Within a situation, spread lenses across the families the profile allows, so angles add coverage and independence together.
3. Separate aggregator seat. Keep the dedupe and triage seat outside the author and orchestrator families, require a structured finding schema (severity, location, lens, family) and dedupe on a deterministic key before any LLM merge. EGM's synthesizer is the weak point I would not copy.
4. Spec-first gate before implementation situations. EGM's feature-spec and implementation-readiness standards fit as a pre-gate. Use cross-family reviewers, not `inherit`.
5. Drift check as a post-merge situation. EGM's [drift report](https://github.com/google/elephant-goldfish-model/blob/main/skills/egm_drift_report/SKILL.md) compares design docs with code. model-mesh validators already cover config against docs, so extend the idea to method docs against skills.
6. Effectiveness measurement. Neither project has it. A seeded-defect corpus per situation would test whether lens count or family count catches more. Until then, mark the ranking as a proposal.
7. Cheap adoptions: a skill body size test, a TESTING.md table with harness version, date and result, and per-skill scenario files.

Do not adopt: unbounded swarms, interactive per-stage human gates inside autonomous profiles, and `model: inherit` for reviewers.

## Where each proposal landed

| # | Proposal | Built as |
|---|---|---|
| 1 | Zero-context reviewer contract | Constraint `zero-context-review` on all 104 options, rule O15, [REVIEW-PANEL.md](../../REVIEW-PANEL.md) |
| 2 | Lens library and lens-by-family seats | [lenses.json](../../../examples/orchestration/lenses.json), `lenses` on every situation and reviewer seat, spread tier for A05 and A06 with a second reviewer family, rule O17 |
| 3 | Separate aggregator and deterministic merge | `aggregator` seat on all options, rule O16, [finding.schema.json](../../../examples/orchestration/finding.schema.json), [aggregate-findings.py](../../../scripts/aggregate-findings.py) |
| 4 | Spec-first gate | `gates.pre` on A02 and A03, [spec-readiness.md](../../../examples/orchestration/standards/spec-readiness.md), rule O18 |
| 5 | Drift check | `gates.post` on A02 and A03, [drift.md](../../../examples/orchestration/standards/drift.md), and [check-drift.py](../../../scripts/check-drift.py) for the method docs |
| 6 | Effectiveness measurement | [score-review.py](../../../scripts/score-review.py) and [SEEDED-DEFECTS.md](SEEDED-DEFECTS.md). No corpus has been run |
| 7 | Cheap adoptions | Skill size cap and per-skill scenarios in [validate-scenarios.py](../../../scripts/validate-scenarios.py), and [TESTING.md](../../../TESTING.md) |

Differences from the original proposal: the skill size cap is 24,000 bytes with a lower grandfathered ceiling for mm-method, which is already larger than the cap. The scenario files are static pattern checks on each skill, not live runs.

## Licence and process notes

EGM is Apache-2.0 and model-mesh is MIT. Ideas are free to reuse and model-mesh copies no EGM text, but [THIRD_PARTY_NOTICES.md](../../../THIRD_PARTY_NOTICES.md) credits the source. EGM's two-stage design-doc PR rule and [AI_POLICY](https://github.com/google/elephant-goldfish-model/blob/main/AI_POLICY.md) are not adopted because model-mesh is a one-owner repo.

## Limits of this review

Judgements above come from reading the repo's text. I did not run EGM, and the live harness results in TESTING.md are the maintainers' claims.
