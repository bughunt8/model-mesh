# Skill-repo integration assessment (October 2026)

Reusable reference for registry decisions. Assesses ten external skill repositories offered
for integration into model-mesh, records the decision and its reason per repository, and
fixes the exact next step for anything deferred. Later refreshes re-assess against this
record rather than from memory.

- **Compiled:** 2026-10-14
- **Scope:** ten repos proposed for integration. Every one was cloned and inspected at
  source; no verdict below rests on a README's self-description.
- **Reading rule:** stars measure attention, not fit. The two decisive axes here are
  **license** (can we redistribute the text at all) and **the release gate** (does the text
  survive `.github/checks.py`). Popularity is recorded for context and never argues a case.

## Why this file is denylist-exempt

`docs/research/` is exempt from the vendor-name denylist by design (`checks.py`,
`DENY_EXEMPT_PREFIXES`). That exemption exists so research can cite real tool names
honestly. This file uses it for exactly that: an assessment that has to name the agent
harnesses a candidate repo is written *for*. It is a research record, not shipped config.

## The gate that decides most of these

`model-mesh` enforces vendor neutrality as its first release gate: `checks.py` fails the
build if certain agent-harness and model tokens appear in file contents or paths. Most
candidate skills are authored *for* one of those harnesses — their prose says "run this in
harness X", their frontmatter lists harness X's tool names. Copying such a skill verbatim
therefore fails CI on the first commit.

Two honest resolutions exist, and the choice is per-repo:

1. **Rewrite into model-mesh's vocabulary.** The method is retargeted to "the agent's
   current harness", losing nothing that matters for a harness-agnostic repo.
2. **Decline the import.** When the harness coupling is not cosmetic but load-bearing —
   the skill invokes specific harness-only MCP tools by name and does not run without them
   — rewriting it produces a skill that no longer does its job.

## Inventory

The "gate hits" column counts Markdown files in the candidate repo that contain at least
one gated token, over the total Markdown files. It is the size of the rewrite obligation,
measured rather than estimated.

| Repository | Stars | License | Skill files | Gate hits | Decision |
|---|---:|---|---:|---:|---|
| `emilkowalski/skills` | 46.1k | MIT | 15 | 0 / 25 | **Adopt as cited source** |
| `iart-ai/web-animation-skills` | 41 | MIT | 9 | 1 / 31 | **Adopt as cited source** |
| `coreyhaines31/marketingskills` | 54.7k | MIT | 50 | 108 / 389 | Cite from the marketing adapter |
| `LearnPrompt/awesome-seedance` | 2.1k | MIT | 15 | 100 / 136 | Cite from the motion adapter |
| `wanshuiyin/ARIS-Movie-Director` | 71 | MIT | 16 | 51 / 62 | Out of method scope |
| `akseolabs-seo/cinematic-ui` | 75 | MIT | 1 | 11 / 40 | Out of method scope |
| `Tejashmakwana/motionmaxxing` | 445 | Apache-2.0 + GSAP | 1 | 8 / 23 | License-blocked |
| `Mood-…/How-to-Clone-Website` | 113 | **None at root** | 0 | — | License-blocked |
| `iart-ai/motion-skills` | 810 | MIT | 0 | — | Not a skill repo |
| `arco-design/arco-design` | 5.7k | MIT | 0 | — | Not a skill repo |

## Findings

**Two clean adoptions.** `emilkowalski/skills` and `iart-ai/web-animation-skills` are the
only candidates that are both properly licensed and essentially gate-clean. Both are
authored as agent skills (`name` + `description` frontmatter), and both teach exactly the
craft the design/UX adapter names but does not cover: whether to animate at all, easing and
duration selection, the render-and-inspect loop, and per-technique implementation. Their
zero-to-one gate-hit counts mean their claims can be cited verbatim, which is stronger than
an adapted paraphrase.

**Two license blockers, one of which is not a judgment call.**

- `Tejashmakwana/motionmaxxing` is Apache-2.0 for its own work, but its `NOTICE` states the
  bundled animation runtime is **not open source** and that the Apache grant does not extend
  to it. Folding that repo into an MIT project would re-export a license we cannot grant.
- `Mood-Global-Services/How-to-Clone-Website---Claude-Skills` has **no `LICENSE` at the repo
  root**; the MIT text present sits inside a vendored zip of a third party's template. No
  license grant from the repo owner means no redistributable right. Separately, its core
  function is pixel-cloning arbitrary third-party websites, which is an ethics and
  copyright question independent of its own licensing.

**Two are not skill repositories at all.** `iart-ai/motion-skills` is a link hub: its README
indexes seventeen *other* packs and the repo contains zero skill files. It is worth
citing as a directory, not importing. `arco-design/arco-design` is a React UI component
library (a published design-system package), not a skill source; the right relationship is
the one `design-ux` already prescribes — consult the project's design system — not vendoring.

**Two are out of method scope.** `wanshuiyin/ARIS-Movie-Director` is a full comic-and-movie
production pipeline whose skills invoke six specific harness-only MCP tools hundreds of
times; it does not run without them, so a rewrite would produce a non-functional skill.
`akseolabs-seo/cinematic-ui` is a strong design skill but its bulk is reference data — a
large design-DNA corpus and per-director grammars — where an adapted prose skill, not a
vendored corpus, is the honest fit.

**One may deserve promotion later.** `coreyhaines31/marketingskills` (50 skills, MIT) is
well-built and its domain — marketing and content — already has a model-mesh adapter. The
gate-hit count is high but concentrated in harness-naming prose rather than load-bearing
tool calls, so it is a rewrite candidate rather than a decline. It is recorded here as the
leading future candidate; promoting it is a separate, larger decision than this pass.

## Decision

Adopt the two clean repos as **cited authoritative sources** for a new motion/animation
domain adapter, and cite the remaining relevant repos from where they belong. Do **not**
vendor any repository's files: model-mesh's own `skills/` tree is four hand-written `mm-*`
packages, and the established pattern for outside work is attribution plus conceptual
adaptation, as `THIRD_PARTY_NOTICES.md` already does for its three upstreams. Vendoring was
also declined because it would require widening the vendor-neutral release gate, the one
gate that keeps this repo honest about being vendor-neutral.

Delivered in v1.2.0:

- `skills/mm-method/references/domains/motion.md` — the new adapter, citing the two clean
  repos and the platform authorities in its Sources section.
- `THIRD_PARTY_NOTICES.md` — attribution entries for the two repos relied on.
- This assessment, for the eight deferred repos and the reasons.

## What would change these verdicts

- A `motionmaxxing` release that removes the non-open-source runtime, or a license clarification
  for `How-to-Clone-Website`, unblocks those two.
- A harness-agnostic fork of the comic-pipeline skills would move that repo from "out of scope"
  to a real candidate.
- If model-mesh ever ships a vendored-skill directory with its own denylist exemption, the two
  clean repos become direct-import candidates rather than cited sources.
