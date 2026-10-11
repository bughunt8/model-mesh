# Council synthesis

Four models researched the same brief on 2026-10-11 HKT: Claude Opus 5.5, GPT 6.1 Sol, Kimi K3 and GLM 5.3. Their raw reports are in [council/](council/README.md). All of it is proposal material. Nothing here was run, and agreement between models is not evidence of quality. DeepSeek was invited and dropped after its API failed on large calls, as the owner instructed.

A tick below means the report states the point or builds its cells on it. The first synthesis draft ticked all four models on rules that only one or two reports state. An independent review caught that, and each tick was rechecked against the raw reports. Where only one report supports a rule, the rule appears in the unique table and this package labels it as its own decision.

## Where the models agree

| Finding | Claude Opus 5.5 | GPT 6.1 Sol | Kimi K3 | GLM 5.3 | Evidence |
|---|---|---|---|---|---|
| The reviewer sits in a different harness and a different model family from the worker in the same cell. | ✓ | ✓ | ✓ | ✓ | Opus 5.5 and Sol state it as a table rule. Kimi K3 and GLM 5.3 check it cell by cell in their independence audits. |
| omo's own `momus` and `oracle` run inside the worker harness, so they are internal gates and never the independent review. | ✓ | ✓ | ✓ | | Opus 5.5 ([report](council/claude-opus-5-5.md)), Sol ([report](council/gpt-6-1-sol.md)) and Kimi K3 ([report](council/kimi-k3.md)) say the independent reviewer is never omo. Kimi K3 still lists omo `momus` as a second reviewer in some cells, and GLM 5.3 does not state the rule. |
| Independence must hold over the whole fallback chain. | ✓ | ✓ | | | Opus 5.5 builds disjoint family pools per profile. Sol binds a harness to its entire ordered chain. |
| A bundled browser decides browser administration (A11). Codex CLI has Browser Use, and Qwen Code has Computer Use. | ✓ | | ✓ | ✓ | [Codex config reference](https://www.codex-docs.com/en/docs/config-file/config-reference), [Qwen Code MCP docs](https://qwenlm.github.io/qwen-code-docs/en/users/features/mcp/). Sol puts the source and backend eligibility first. |
| Qwen Code is a primary or alternate author where bundled web, image or office-file tools matter (A07, A11, A12). | ✓ | | ✓ | | [Qwen Code model-provider docs](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/model-providers/). |
| Pi has no built-in sandbox. Containers or micro-VMs come from packages. | ✓ | | ✓ | ✓ | [Pi settings](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/settings.md) and the Pi docs the reports cite. |
| The Codex CLI route to Hong Kong-reachable models rests on vendor guides, not a runtime test. | ✓ | | ✓ | ✓ | [Kimi guide for Codex](https://platform.kimi.ai/docs/guide/codex-kimi). GLM 5.3 marks the cell unavailable if the route fails. |

## Where the models disagree

| Topic | Claude Opus 5.5 | GPT 6.1 Sol | Kimi K3 | GLM 5.3 | Why they differ |
|---|---|---|---|---|---|
| Is OpenCode with omo allowed? | Keeps it and discloses the Sustainable Use License | Unavailable under the open-source rule | Lists OpenCode as MIT and uses omo `momus` as a reviewer in some cells | Same as Kimi K3 | Only Opus 5.5 and Sol read the omo LICENSE file. Kimi K3 and GLM 5.3 cited a DeepWiki page about OpenCode alone. The owner then chose an explicit exception. |
| Is an independence exception needed? | None | None | One, in ultimate A02 | None, unless Codex CLI cannot run an HK-reachable model | Kimi K3 counted the six-family Hong Kong pool as too small for one cell. |
| Role of DSH | Reviewer in several cells | Not checked | Not checked | Alternate worker in A04 only | The community omo plugin and preview status weigh differently. This package keeps DSH as an alternate author only. |
| Orca coverage | Only when two or more isolated worktrees run at once | Rows with separable modules | No coordinator in any cell | P5 with Orca on A04, A09 and A11 | They disagree on when worktree isolation pays for the overhead. This package follows Opus 5.5 and uses Orca on A02 and A05 only. |
| Gemini in matrix cells | Adjudicator and reviewer rungs | Do not route Gemini 4 Argon | Gemini rungs in several cells | Gemini rungs in several cells | Gemini has been retired from this repository since v1.1.1 and nobody was asked to reverse it. This package keeps every Gemini model out. |
| Global orchestrator | An Anthropic-family model | GLM, then Qwen | Not compared | Not compared | Opus 5.5 followed omo's published guidance. Sol kept orchestration on the ultimate pool. |
| Who reviews A11? | Goose, with a Playwright test | Not checked | OpenCode on a DeepSeek model | Aider on a DeepSeek model | They differ on which second harness is trusted. This package picks harnesses by what the seat needs and checks independence by rule. |

## Unique discoveries

| Model | Finding | Why it matters |
|---|---|---|
| Claude Opus 5.5 | omo's LICENSE is the Sustainable Use License 1.0 (finding F1), and the shipped ultimate and hybrid profiles give `momus` the same model as `hephaestus` (F7). | Both facts changed the design. The licence was checked against the LICENSE file. |
| Claude Opus 5.5 | GLM Coding Plan terms limit use to OpenCode, Codex, Pi and Goose ([Z.ai tools](https://docs.z.ai/devpack/tool/others)). | GLM on DSH, Qwen Code or Aider would need metered access, so those cells avoid it. |
| Claude Opus 5.5 | omo restricts Hephaestus to GPT-native models from v4.10.0, and Goose recipes with an allowlist suit CI-shaped rows (A04, A10). | The matrix uses `atlas` where a chain is not wholly OpenAI-family, and puts Goose on those rows. |
| GPT 6.1 Sol | Gemini 4 Argon has no public model ID and should not be routed. If a reviewer authors a repair, a new independent reviewer is needed. | Matches the live check. The second point backs the rule that a reviewer who writes becomes an author. |
| Kimi K3 | Alibaba benchmarked Qwen3.8-Max inside Claude Code, not Qwen Code. | The Qwen Code plus Qwen3.8 pairing stays an unmeasured tie-breaker. |
| GLM 5.3 | Aider is a worker alternate and a reviewer, never an orchestrator. | This package adopts the rule and the validator enforces it. |

The A06 author provenance manifest and the open-source-only alternate on every cell are this package's own decisions. No report proposed them. The Pi container rule comes from Claude Opus 5.5, whose report says Pi runs in a container with a read-only mount, and the validator now enforces it.

## Analysis

The four reports converge on one structural point and diverge on policy. All four place the reviewer in a different harness and family from the worker. Opus 5.5, Sol and Kimi K3 also say that omo's own `momus` and `oracle` cannot count, and Opus 5.5 and Sol add that independence must hold on every rung of the fallback chain. The repository already breaks the first rule: `momus` shares a model with `hephaestus` in the shipped ultimate and hybrid profiles.

The disagreements were about eligibility and scope rather than facts. Sol excluded omo on licence grounds under the open-source rule. Opus 5.5 disclosed the same licence and kept omo. Kimi K3 and GLM 5.3 never noticed the omo licence. The owner resolved this with an explicit exception, and each cell carries an alternate that replaces omo orchestration with an open-source harness so the exception can be withdrawn without a redesign. Kimi K3 asked for one independence exception in ultimate A02 because it counted the Hong Kong pool as too small. Splitting families into worker, orchestrator and reviewer pools per profile removes the need, and the validator rejects any exception.

Several claims in the reports were checked and corrected. Gemini models appeared in several cells even though the repository retired Gemini in v1.1.1. GPT 6.1 Luna does not exist, while GPT 6 Luna does. Gemini 4 Argon has no public ID. DeepSeek and MiMo model IDs are changing, so the matrix avoids the retiring MiMo V2.5 route. The owner's affinity hypotheses are tie-breakers: the evidence for Qwen Code with Qwen3.8 is vendor assertion, and Kimi K3 found that Alibaba benchmarked it elsewhere. For DSH with DeepSeek Flash the evidence is vendor documentation.

Adopt the matrix as a design for review, then qualify one row per harness before relying on it. Start with A01 on OpenCode with omo and Goose review, A04 on Goose with Pi review, and A11 on Qwen Code with the official Playwright MCP, because those three exercise the most different harness paths.
