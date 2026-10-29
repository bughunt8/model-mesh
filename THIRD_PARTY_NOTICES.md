# Third-Party Notices

## fable-method (MIT)

The loop skills in `skills/` (`mm-method`, `mm-loop`, `mm-verify`, `mm-domain`) and the
`install.sh` / `install.ps1` scripts are **adapted from and integrated with**:

- Project: fable-method
- Author: Sahir619
- Source: https://github.com/Sahir619/fable-method
- License: MIT

Changes made in model-mesh:
- Skills renamed from the upstream fable-method naming to `mm-*`, and command names updated.
- All real model/provider names removed and replaced with behavioral descriptions.
- The bundled `eval/` trap-suite and its data were **not** included in this repo.
- Documentation rewritten for model-mesh.

The upstream MIT copyright is retained in `LICENSE`. This notice fulfills the MIT
attribution condition for the copied portions.

## oh-my-openagent

The routing configs target the oh-my-openagent / opencode framework
(https://github.com/code-yeongyu/oh-my-openagent). The strings `oh-my-openagent`,
`opencode`, the `[opencode]` config key, and the schema URL are that framework's
real identifiers, intentionally retained so the config loads. They are not vendor
model names.

## matt-pocock/skills (concepts adapted)

By Matt Pocock (https://github.com/mattpocock/skills).

The mm-method loop integrates ideas adapted from several skills in
https://github.com/mattpocock/skills:

- **grilling / grill-me** -> Step 1 requirement-sharpening interview (one question at a time, decisions vs facts).
- **prototype** -> Step 3.5 conditional throwaway-prototype phase (logic/UI branches, throwaway rules).
- **tdd** -> Step 4 test-first vertical-slice method (seams, red->green, anti-patterns).
- **code-review** -> Step 4 close two-axis review (Spec + Standards, Fowler smell baseline).

These are conceptual adaptations rewritten into model-mesh's loop and prose; no files were copied verbatim.
Consult that repository for the original, fuller skills. Licensing per that repository.

## debug-pipeline2 (concepts adapted)

The evidence discipline folded into the loop is adapted from the `debug-pipeline2`
audit-fix-prove protocol (author: ronald-ng, MIT):

- **Machine-checkable evidence** (a claim carries a reproducible command + real output) -> Step 2 capture, Step 5 verify, and `references/evidence.md`.
- **Negative tests** ("a check is only trustworthy once seen to fail") -> the TDD observed-red rule and the evidence standard.
- **False-green defence** ("re-execute and reproduce, never rubber-stamp a report") -> Step 5, conditional on non-trivial work.
- **Independent-reviewer isolation** (reviewers spawned fresh, artifacts-only, never told each other's verdict) -> the Step 4-close two-axis review.

Conceptual adaptations rewritten for generic coding; the pipeline-specific machinery
(on-disk state contracts, OMO agent mapping, run budgets) was not carried over.

## Elephant-Goldfish Model

The review panel design in `docs/REVIEW-PANEL.md` was informed by the Elephant-Goldfish Model, https://github.com/google/elephant-goldfish-model, licensed Apache-2.0. The ideas studied are zero-context reviewer subagents, role-based review lenses, staged design review, and a drift report. No source text, persona prompt or template was copied. The lens prompts, standards and scripts in this repository are original. The study is in `docs/research/orchestration/EGM-ANALYSIS.md`.

## emilkowalski/skills (cited source, MIT)

By Emil Kowalski (https://github.com/emilkowalski/skills), MIT.

The motion/animation domain adapter (`skills/mm-method/references/domains/motion.md`)
cites this repository as an authoritative open-source reference for motion craft: whether a
surface should animate at all, purpose-first motion decisions, easing and duration
selection, interruption and exit handling, and the render-and-inspect verification loop.

No files were copied. The adapter is original prose written to model-mesh's own
`references/domains/TEMPLATE.md` schema; this repository is named in the adapter's Sources
section as the upstream reference a reader should consult for the fuller craft material.
Licensing per that repository (MIT).

## iart-ai/web-animation-skills (cited source, MIT)

By iart.ai (https://github.com/iart-ai/web-animation-skills), MIT.

The motion/animation domain adapter cites this repository as an authoritative
open-source reference for the render-and-inspect verification loop (render a frame,
capture it, check it) and for per-technique implementation guidance across scroll-driven
timelines, micro-interactions, page transitions, and frame-budget work.

No files were copied. Same arrangement as above: original prose against model-mesh's
adapter schema, with the upstream named in the adapter's Sources section. Licensing per
that repository (MIT).

The related `iart-ai/motion-skills` repository is cited in the same adapter's Sources as
a pack index only. It is a directory of per-audience motion packs and contains no skill
files itself; nothing from it was imported. Licensing per that repository (MIT).

## Skills assessed and NOT adopted

Ten external skill repositories were assessed for integration in October 2026. Two are
cited above; the other eight were declined or deferred, and the reason for each is
recorded in `docs/research/2026-10-skill-repo-assessment.md`. The two that were declined
for licensing reasons are recorded there specifically so a future contributor does not
re-attempt them without a license change: one bundles a third-party runtime under a
non-open-source license that its own NOTICE confirms is not covered by its Apache grant,
and one carries no repository-level license at all.

No files from any declined repository were copied into this project.
