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
