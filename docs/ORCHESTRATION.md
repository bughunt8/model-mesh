# Multi-agent orchestration

model-mesh started as one agent routing work to sub-agents inside one harness. This document extends the direction to several agents across several harnesses, still using oh-my-openagent (omo) role and category names as the shared vocabulary.

Status: a design proposal dated 2026-10-11. The matrix is checked for structure and policy in CI. No row has been run, installed or measured. The [review record](research/orchestration/REVIEW.md) lists what a reviewer challenged.

## Four profiles, same names

| Profile | Rule | Orchestrator pool | Notes |
|---|---|---|---|
| `ultimate` | Hong Kong-native. Only models whose developer API is reachable from Hong Kong, no geo-unlock proxy | Z.ai GLM family | Unchanged from before; see [PROVIDERS.md](PROVIDERS.md) |
| `hybrid` | Default. Output-price cap on generalist, utility and orchestration rungs. Flagship coder, architect and ultrawork are exempt | Z.ai GLM family | Cap placement is enforced in CI |
| `b4b` | Same cap, applied harder | Z.ai GLM family, cheap rung first | |
| `global` | New. The unrestricted twin of `ultimate`. No region limit and no budget cap | An Anthropic-family mid-tier model, with the top Anthropic tier kept as an escalation | The retired Google family stays retired. Evidence in [GLOBAL-PROFILE.md](research/orchestration/GLOBAL-PROFILE.md) |

Real model IDs live only in example files and research notes. Hybrid and b4b cells use only rungs under the cap, with the flagship coder allowed in the exact slots the cap policy already exempts. Prices are in [PRICE-REFERENCE.md](research/orchestration/PRICE-REFERENCE.md). Generic files use role placeholders, as before.

## Twelve situations

Each row of the matrix is one kind of work. The set comes from the evaluation plan.

| ID | Situation | What decides the choice |
|---|---|---|
| A01 | Regression bug repair | Reproduction and regression discrimination |
| A02 | Bounded feature delivery | Acceptance completeness, integration risk |
| A03 | Behavior-preserving refactor | Observable equivalence |
| A04 | CI or deployment diagnosis | Reproducible diagnosis, bounded tools |
| A05 | Security audit and remediation | Exploit discrimination, independent review of the fix |
| A06 | Independent change review | Finding precision and provenance |
| A07 | Source-grounded research brief | Claim evidence, contrary findings |
| A08 | Data reconciliation and analysis | Known-answer arithmetic |
| A09 | Requirements and architecture planning | Traceability, contradiction discovery |
| A10 | Policy-constrained business workflow | Authorization and final state |
| A11 | Browser administration | Correct target, final state, bounded authority |
| A12 | Cross-application office work | Artifact consistency, exact references |

## Five patterns

| Pattern | Name | Use it when |
|---|---|---|
| P1 | omo-native | One harness runs the whole role chain and the work is a single stream |
| P2 | Harness executor | omo plans and delegates, another harness executes one seat |
| P3 | Peers with a shared contract | Seats exchange immutable artifacts, with no AI orchestrator |
| P4 | Independent reviewer | Always added. A second harness and a second model family review |
| P5 | External coordinator | Two or more isolated worktrees or human decision gates exist; Orca is the default |

A cell names one author pattern plus P4. The coordinator value is `orca` only with P5 and `none` otherwise.

## The independence rule

Do not review generated work with the harness and model that produced it. A cell passes only if all of these hold, and the validator checks them over every fallback rung, not only the primary.

1. The reviewer harness differs from every author harness and from the orchestrator harness.
2. The reviewer model families share nothing with every rung of every author seat and every category route. Helper roles, editor models and multimodal lookers count as authors.
3. The orchestrator family shares nothing with authors or reviewers.
4. omo `momus` and `oracle` run inside the worker harness, so they are internal gates only and never the independent review. The `momus` label in a reviewer seat means an original task contract run in the reviewer's own harness, not a call to the omo plugin.
5. The validator derives each family from the model ID, not from labels in the data, and rejects any `absolute_exception` key. The owner can grant an exception in a later change. None exists now.

When authorship is unknown, as in A06, the cell requires an author provenance manifest. A judge cannot certify independence from a patch with no known author.

## Seven harnesses

OpenCode with omo, the DeepSeek Harness (DSH), Codex CLI, Pi, Qwen Code, Aider and Goose. Each has bundled strengths and gaps, summarised in [HARNESSES.md](research/orchestration/HARNESSES.md). Capabilities count in three tiers. Bundled features count in full. Official open-source add-ons count with their setup cost. Community add-ons are listed and get no weight. A harness favours a situation when its bundled tools match what decides that situation, for example a bundled browser for A11 or bundled image and PDF input for A07 and A12.

Pairings between a harness and its maker's model, such as a harness with its maker's own model, are treated as unmeasured tie-breakers until independent evidence exists.

## Coordinators

Orca is the default when a cell has parallel worktrees. Emdash and Nimbalyst are open-source alternates. Vibe Kanban, Superset, Conductor, Warp and AQ are reference only because of shutdown, licence or hosting. [COORDINATORS.md](research/orchestration/COORDINATORS.md) has the evidence. Without parallel worktrees, one pilot controller replaces a coordinator.

## Openness and the omo exception

Harnesses and the verification stack must be open source, as before. Inference models and hosting are outside that rule. omo itself is under the Sustainable Use License 1.0, which allows internal business or non-commercial use and restricts distribution. The owner accepted omo as an explicit exception. Every non-primary option therefore replaces omo orchestration with an open-source harness, and the validator rejects an alternate whose orchestrator is omo. Client or commercial use of omo needs its own licence check before it starts.

## Reading and using the matrix

The generated table is [MATRIX.md](research/orchestration/MATRIX.md), built from [matrix.example.json](../examples/orchestration/matrix.example.json). Each option is a complete assignment, so do not mix seats between options. Worked cases are in [EXAMPLES.md](research/orchestration/EXAMPLES.md), and seven harness configuration examples are in [examples/orchestration/harnesses](../examples/orchestration/harnesses).

To adopt a row, pick the profile, pick the primary or alternate option, apply the harness example, then run the loop in [AGENTS.md](../AGENTS.md). Check the result with `python scripts/validate-orchestration.py`.

## What is not proven

Nothing was installed, loaded or dry-run. The harness examples match vendor documentation only. Model IDs are reference routes, and some are changing: one vendor's cheap model alias is moving to a new model, and the older MiMo IDs stop working on 2026-10-21. The Codex CLI route to Hong Kong-reachable models has vendor guides but no runtime evidence. Whether any harness pairing beats another is unmeasured. The orchestration validator proves structure and policy, not that a harness can execute a row.
