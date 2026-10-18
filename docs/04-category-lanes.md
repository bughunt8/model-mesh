# 04 — Category Lanes

Categories are routing lanes, not primary agents. Their chains are consulted
only when a `task(category=...)` spawn occurs, so the evaluation weights
**diversity and coverage** more heavily than a single head's peak score.

| Category | Core focus | Head | Head Fit | Chain Score | Grade | Key finding |
|---|---|---|---:|---:|---|---|
| **architect** | System design, cross-module trade-offs | `claude-sonnet-5-5` high | 81.6 | 79.8 | B+ | Sonnet's IF regression is a risk; consider Opus 5.5 |
| **visual-engineering** | Frontend, UI/UX, design taste | `claude-sonnet-5-5` high | 78.2 | 76.4 | B | No design-specialist credential |
| **ultrabrain** | Hard logic, critical planning | `gpt-6-astra` high | 86.8 | 84.1 | A- | Correct head; Astra is the reasoning ceiling |
| **deep-low** | Backend/logic/multi-step implementation | `gpt-6.1-sol` medium | 82.4 | 81.0 | A- | Correct; Sol medium is the documented default |
| **deep-high** | Unsettled trade-offs, high-risk changes | `gpt-6.1-sol` high | 84.4 | 82.6 | A- | Correct; consider Astra xhigh for escalation |
| **artistry** | Creative, high-impact visual components | `claude-sonnet-5-5` high | 76.8 | 75.2 | B+ | No creative-coding specialist |
| **quick** | Trivial tasks, single-file changes | `deepseek-flash` off | 88.0 | 85.4 | A | Best category in the config |
| **unspecified-low** | Contained general work | `claude-sonnet-5-5` medium | 78.4 | 76.8 | B | Correct family; medium effort appropriate |
| **unspecified-high** | Substantial multi-module work | `gpt-6.1-sol` high | 85.2 | 83.0 | A- | Strong; add Opus 5.5 for a genuine Claude rung |
| **writing** | Documentation, prose, commit copy | `qwen3.8-max` max | 72.0 | 70.4 | B- | Qwen has weak instruction-following for a prose contract |

## Two category-level structural findings

### 1. `visual-engineering` and `artistry` have no specialist head

Both are frontend/creative-coding lanes, and both lead with a generalist Claude
model. The documented heads are Fable 5.1 or Opus 5.5 at max. Sonnet 5.5 is a
reasonable second choice but is not a design-taste specialist.

### 2. `writing` leads with Qwen3.8-Max at max

Qwen has the highest SkillsBench score in the roster (70.2), which sounds right
for a procedure-following writing task. But its instruction-following rank is
#36 (69.1) — the wrong property for a category whose output is prose with a
fixed format. Kimi K3 at `low` is the documented writing head and has a better
instruction-following profile.

## Category-key hygiene

The current engine set is ten keys, not eight: `architect`, `artistry`,
`deep-low`, `deep-high`, `quick`, `ultrabrain`, `unspecified-high`,
`unspecified-low`, `visual-engineering`, `writing`.

`deep` is a deprecated alias for the `deep-low`/`deep-high` pair and is on a
removal clock. Any `task(category="deep-low")` or `"architect"` call against a
config that only defines `deep` bypasses your overrides entirely and falls
through to built-in defaults that reference first-party provider lanes.

