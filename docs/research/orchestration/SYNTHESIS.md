# Council synthesis

Four models researched the same brief on 2026-10-11 HKT: Claude Opus 5.5, GPT 6.1 Sol, Kimi K3 and GLM 5.3. Their raw reports are in [council/](council/README.md). All of it is proposal material. Nothing here was run, and no model's ranking of another model is evidence of quality. DeepSeek was invited and dropped after its API failed on large calls, as the owner instructed.

## Where the models agree

| Finding | Claude Opus 5.5 | GPT 6.1 Sol | Kimi K3 | GLM 5.3 | Evidence |
|---|---|---|---|---|---|
| omo's own `momus` and `oracle` run inside the worker harness, so they cannot count as the independent review. The shipped ultimate and hybrid profiles already break the rule by giving `momus` the same model as `hephaestus`. | ✓ | ✓ | ✓ | ✓ | Opus 5.5 audited the profile files (finding F7). The other three place the independent review in a second harness. |
| The reviewer sits in a different harness and a different model family from every author rung, not only the primary. | ✓ | ✓ | ✓ | ✓ | Each report defines disjoint worker, orchestrator and reviewer pools per profile. |
| A bundled browser decides the browser-admin row (A11). Codex CLI has Browser Use, Qwen Code and Goose have computer-control tools, and the official Playwright MCP is the add-on path. | ✓ | ✓ | ✓ | ✓ | [Codex config reference](https://www.codex-docs.com/en/docs/config-file/config-reference), [Qwen Code MCP docs](https://qwenlm.github.io/qwen-code-docs/en/users/features/mcp/). |
| Bundled multimodal input favours Qwen Code on research and office rows (A07, A12). | ✓ | ✓ | ✓ | ✓ | [Qwen Code model-provider docs](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/model-providers/). |
| Orca is worth a coordinator only when two or more isolated worktrees or human decision gates exist. Otherwise a single pilot controller is enough. | ✓ | ✓ | ✓ | ✓ | [Orca orchestration guide](https://github.com/stablyai/orca). |
| DSH is an alternate only. It is public preview, and its MCP, memory and omo emulation come from community plugins. | ✓ | ✓ | ✓ | ✓ | [DSH SDK README](https://github.com/deepseek-ai/deepseek-harness/blob/master/python/sdk/README.md). |
| Pi must run in a container, Aider is never an orchestrator, and the Codex custom-provider route has vendor docs but no runtime proof. | ✓ | ✓ | ✓ | ✓ | [Pi settings](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/settings.md), [Kimi guide for Codex](https://platform.kimi.ai/docs/guide/codex-kimi). |

## Where the models disagree

| Topic | Claude Opus 5.5 | GPT 6.1 Sol | Kimi K3 | GLM 5.3 | Why they differ |
|---|---|---|---|---|---|
| Is OpenCode with omo allowed? | Keeps it and discloses the Sustainable Use License | Unavailable under the open-source rule (D46) | Lists OpenCode as MIT and uses omo `momus` as a reviewer in some cells | Same as Kimi K3 | Only Opus 5.5 and Sol read the omo LICENSE file. Kimi K3 and GLM 5.3 cited a DeepWiki page about OpenCode alone. The owner then chose an explicit exception. |
| Is an independence exception needed? | None | None | One, in ultimate A02 | None, unless Codex CLI cannot run an HK-reachable model | Kimi K3 counted the six-family Hong Kong pool as too small for one cell. |
| Global orchestrator | An Anthropic-family model | GLM then Qwen | Not compared | Not compared | Opus 5.5 followed omo's published guidance. Sol kept orchestration on the same open-weight pool as ultimate. |
| Gemini in matrix cells | Adjudicator and reviewer rungs | Do not route Gemini 4 Argon | Gemini rungs in several cells | Gemini rungs in several cells | Gemini is retired from this repository since v1.1.1 and nobody was asked to reverse it. This package keeps every Gemini model out. |
| Who reviews browser-admin work in ultimate (A11)? | Qwen Code worker, separate harness reviewer | Different harness and family | Qwen Code worker, OpenCode reviewer on a DeepSeek model | Codex CLI worker through a custom provider, Aider reviewer | Whether the Codex custom-provider route counts as proven. It is not proven. |

## Unique discoveries

| Model | Finding | Why it matters |
|---|---|---|
| Claude Opus 5.5 | omo's own LICENSE is the Sustainable Use License 1.0 (finding F1), and the shipped ultimate and hybrid profiles give `momus` the same model as `hephaestus` (F7). | Both facts changed the design. I confirmed the licence against the LICENSE file. |
| Claude Opus 5.5 | GLM Coding Plan terms limit use to OpenCode, Codex, Pi and Goose ([Z.ai tools](https://docs.z.ai/devpack/tool/others)). | GLM on DSH, Qwen Code or Aider would need metered access, so those cells avoid it. |
| Claude Opus 5.5 | omo restricts Hephaestus to GPT-native models in v4.10.0. | The matrix puts `atlas` in the author seat wherever the chain is not OpenAI-family. |
| GPT 6.1 Sol | A reviewer needs an author provenance manifest. An independent judge cannot invent who wrote a patch. | A06 carries the `author-provenance-required` constraint. |
| GPT 6.1 Sol | Gemini 4 Argon has no public model ID and should not be routed. | Matches the live check. |
| Kimi K3 | Alibaba benchmarked Qwen3.8-Max in Claude Code, not Qwen Code. | The Qwen Code plus Qwen3.8 pairing stays an unmeasured tie-breaker. |
| GLM 5.3 | Goose recipes suit CI-shaped rows such as A04 and A10. | Goose is primary author on those rows. |

## Analysis

The four reports converge on structure and diverge on policy. All of them found the same hole in the current repository: `momus` shares a model with `hephaestus`, and both run in one harness, so the review gate the loop relies on is not independent. They also agree that independence has to be checked over the whole fallback chain, because a reviewer whose third fallback shares a family with an author is not independent after one outage.

The disagreements were about eligibility and exceptions rather than facts. Sol excluded omo on licence grounds under the open-source rule. Claude Opus 5.5 disclosed the same licence and kept omo. Kimi K3 and GLM 5.3 never noticed the omo licence at all. The owner resolved this with an explicit exception, and the package keeps an open-source-only alternate in every cell so the exception can be withdrawn without redesign. Kimi K3 asked for one independence exception in ultimate A02 because it counted a six-family Hong Kong pool as too small. Splitting the families into worker, orchestrator and reviewer pools per situation removes the need, and the validator treats any exception as an error unless it carries a written reason.

Four claims in the reports were checked and corrected. Gemini models appeared in several cells even though the repository retired Gemini in v1.1.1. GPT 6.1 Luna does not exist, GPT 6 Luna does. Gemini 4 Argon has no public ID. DeepSeek and MiMo model IDs are changing, so the matrix avoids the retiring MiMo V2.5 route and flags the DeepSeek Flash alias. The owner's affinity hypotheses were treated as ties to break, not facts: the only evidence found for Qwen Code with Qwen3.8 is vendor assertion, and for DSH with DeepSeek Flash it is vendor documentation.

The recommendation is to adopt the matrix as a design for review, then qualify one row per harness before relying on it. Start with A01 on OpenCode with omo and Goose review, A04 on Goose with Pi review, and A11 on Qwen Code with the official Playwright MCP, because those three exercise the most different harness paths.
