# Council proposal: qualify the controller before choosing the model

Documentation checked 11 October 2026, Hong Kong time. Design proposal only. No installations, repository edits, model calls, benchmarks, or measured effectiveness.

## 1. Harness capability table

The first blocker is licensing. OpenCode is MIT, but the pinned omo v4.19.4 license restricts use and distribution to specified internal or non-commercial purposes. [OpenCode license][ocl] [Pinned omo license][omol] Therefore **OpenCode with omo is unavailable under D46**, even when its intended internal use might be permitted by that license. Keeping the eleven role names does not require shipping that plugin. The matrix proposes original role contracts on eligible harnesses, not copying omo implementation or restricted prompts. A bare-OpenCode variant would need separate scope approval.

`B` = bundled capability, not necessarily enabled; `O` = opt-in bundled capability; `A` = officially documented OSS add-on, setup required; `C` = community add-on, zero selection weight; `n.s.` = not established in the evidence. Image transport still needs a compatible model.

| Harness | Licence | Browser/Playwright | MCP | Memory | Audio/video/image input | LSP | Sandbox | Subagents/parallel | Headless/SDK/RPC | Worktrees | Maintenance risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| OpenCode + omo | MIT core; SUL plugin, ineligible [MIT license][ocl] [omo license][omol] | omo browser skill, ineligible; core n.s. [omo][omo] | B local/remote [MCP][ocm] | n.s. | image B; audio/video n.s. [OpenCode][oc] | B [agents][oca] | n.s. | B parallel General; omo unavailable [agents][oca] | CLI/SDK [SDK][ocs] | plugin receives worktree path, creation n.s. [plugins][ocp] | v1/v2 migration; plugin licence blocker |
| DSH | MIT [DSH repository][dsh] | n.s.; C GUI plugins | official n.s.; C bridge | official n.s.; C packages | voice experimental; image/video n.s. | official n.s.; C preset | n.s. | subagents; teams experimental | control protocol n.s.; launching Web UI is not an adapter | official n.s.; C isolation | Public preview, changing plugin APIs [DSH][dshsite] |
| Codex CLI | Apache-2.0 [Codex][codex] | Browser Use configuration documented; default/backend source n.s., no full weight [configuration][cc] | B stdio/HTTP | O, default off | image B; audio/video n.s. | n.s. | B configurable filesystem/network | B, default on | `exec`; SDK/RPC n.s. here | recognizes worktrees; creation n.s. | Active; custom-provider/browser qualification gaps [advanced configuration][ca] |
| Pi | MIT [Pi repository][pi] | n.s. | B Codemode [Pi][pis] | C packages; session trees are not task memory | n.s. | n.s. | no built-in permission boundary; documented external options | explicitly no built-in subagents; C packages | print/JSON/RPC/SDK; settled event [RPC][pir] | C packages | Active; extensions inherit process authority |
| Qwen Code | Apache-2.0 [Qwen Code][q] | A Playwright MCP, not bundled [Playwright setup][qp] | B stdio/SSE/HTTP | B Auto-Memory, configurable | image plus configurable audio/video; voice dictation | O experimental | O, default off | B subagents; parallel workflows/teams opt-in | headless JSON; SDKs; ACP/serve experimental | B; named subagent can use linked worktree; forks cannot [subagents][qa] | Active; evolving auxiliary models and counters [settings][qs] |
| Aider | Apache-2.0 [Aider][a] | URL text retrieval, not browser administration | n.s. | n.s. | image B; voice setup; video n.s. | repo map, not LSP | n.s. | architect/editor pair, not independent agents | one-message CLI; Python API unsupported [scripting][as] | native management n.s. | Last release Aug 2025; latest observed commit May 2026 |
| Goose | Apache-2.0 [Goose][g] | Computer Controller bundled; Playwright n.s. | B extensions | B Memory; Chat Recall | n.s. | Analyze call graphs, not LSP | extensions can use Docker; full-process boundary n.s. | B Summon, parallel supported, no nested subagents [subagents][gs] | `goose run`, recipes; CLI/API | n.s. native | Active; headless permission and extension inventory risks [extensions][ge] [headless][gh] |

Community DSH omo emulation has no established license in the supplied extract and a stock-alpha dependency. It receives no capability weight and is not an eligibility workaround. [DSH community plugin][dshomo]

### Coordinators

Eligibility is about the required coordinator software, not whether its website calls it open source.

| Coordinator | Licence class | Supported candidate harnesses | Worktree isolation | Dispatch/steer/cancel evidence | Maintenance risk | OSS-default eligibility |
|---|---|---|---|---|---|---|
| Orca | MIT | C,Q,G,P,OpenCode,DSH listed; Aider via "any CLI"; supervised examples Codex/Claude | per agent | dispatch attempts, messages, settlement; stop requires positive exit proof; exact cancel command n.s. | daily releases; each advertised adapter still unqualified | Yes, conditional on adapter conformance [Orca][or] [orchestration][oro] |
| AQ | licence n.s.; hosted, OSS unestablished | Codex, OpenCode, Pi; others n.s. | per workspace | live sessions, keyboard handoff; control API n.s. | early access | No; labelled proprietary/unverified exception only [AQ][aq] |
| Vibe Kanban | Apache-2.0 | Codex, OpenCode, Qwen | cleanup flag establishes worktree use; guarantees n.s. | workspace launch/diff comments; cancel n.s. | company shutdown, local community continuation | Legally yes; not primary [Vibe Kanban][vk] [shutdown notice][vks] |
| Nimbalyst | MIT | Codex; OpenCode alpha | per parallel session | UI sessions/replies; headless dispatch/cancel n.s. | active; alpha providers | Yes for supervised visual use [Nimbalyst][n] |
| Emdash | Apache-2.0 | Codex, OpenCode, Qwen, Oh My Pi; others n.s. | per task, can disable | launches parallel CLI agents; steer/cancel API n.s. | active; 34 advertised CLIs ≠ qualified adapters | Yes; UI-driven alternate [Emdash][em] |
| Superset | Elastic License 2.0, source-available | Codex, OpenCode; any CLI advertised | per workspace | CLI/SDK/MCP manage workspaces; cancel n.s. | active | No; labelled source-available exception [Superset][su] |
| Conductor | licence n.s.; presumed proprietary pending evidence | Codex, OpenCode | git worktrees | cloud HTTP/MCP workspace control; steer/cancel n.s. | Mac dependence; status n.s. | No; labelled exception [Conductor][co] |
| Warp/Oz | Warp client AGPL; Oz source/licence n.s. | Codex documented; other candidate adapters n.s. | n.s. | parent/child runs, message bus, cancellation state; one level deep | active; cloud dependency | Client potentially yes; Oz coordinator no pending source proof [Warp announcement][wb] [Oz orchestration][wo] |

## 2. Harness-model affinity

| Harness | Documented preference/default | Assessment |
|---|---|---|
| OpenCode | Zen curated models; 75+ providers; no single default established | "Best family" UNMEASURED. omo model-specific prompts do not prove comparative affinity. [OpenCode providers][ocv] [omo][omo] |
| DSH | official UI displays DeepSeek V4.1 Flash | First-party fit documented, superiority UNMEASURED. External coverage describes Pro/Flash use, not a controlled comparison against other harnesses. [DSH][dshsite] [DeepInfra review][di] [AIReiter][ar] |
| Codex | OpenAI default provider; custom Responses providers | OpenAI-oriented integration documented, "best with Sol" UNMEASURED. Qwen publishes a Responses-compatible custom-provider configuration. [Codex reference][cc] [Qwen release][q38] |
| Pi | multi-provider registry; no preferred model established | Every "best family" claim UNMEASURED. One commercial article reports community scores but supplies insufficient reproducibility evidence. [Pi][pis] [Regolo][reg] |
| Qwen Code | deep Qwen integration; headless example `qwen3-coder-plus` | "Best with Qwen3.8" UNMEASURED. Qwen's own release uses other harnesses in several evaluations, not independent proof of Qwen Code superiority. [Qwen Code][q] [Qwen release][q38] |
| Aider | README says best with older Claude, DeepSeek and OpenAI models | Historical recommendation, not evidence for current generations. Architect/editor mode is documented. [Aider][a] [Modes][am] |
| Goose | 15+ providers; subagent model configurable; no native model | All family superiority claims UNMEASURED. [Goose][g] [Subagents][gs] |

### Live candidate check

"API documented" means an official identifier and API path exist, not account entitlement or HK connectivity verified.

| Candidate | Current evidence and routing consequence |
|---|---|
| DeepSeek V4 Flash/Pro | Pro remains `deepseek-v4-pro`; old Flash IDs now serve V4.1 via `deepseek-flash`. Do not treat an accepted retired alias as a pinned checkpoint. [DeepSeek pricing][dp] |
| Kimi K3/K2.7-code | `kimi-k3`, `kimi-k2.7-code` documented; highspeed is a separate, more expensive choice. [Kimi overview][ki] [Kimi pricing][kp] |
| GLM 5.3/5.3-Flash | Both on official rate card. [Z.ai pricing][zp] |
| Qwen 3.8-max/3.7/3.6/3.5-plus | Official releases document APIs; 3.8 open weights were promised later, so API availability does not establish downloadable weights. [3.8][q38] [3.7][q37] [3.6][q36] [3.5][q35] |
| MiniMax M3 | `MiniMax-M3` API documented. [MiniMax][mm] |
| MiMo v2.6 flash/pro/pro-ultraspeed | All on official rate card; older v2.5 IDs scheduled to become invalid Oct 21. Ultraspeed exceeds capped non-exempt rungs. [MiMo pricing][mp] |
| GPT 6.1 Sol/6 Astra/6 Luna | All documented; **"GPT 6.1 Luna" UNVERIFIED**, not an alias to invent. [OpenAI models][models] [Sol][sol] [Astra][astra] [Luna][luna] |
| Claude Fable 5.1/Opus 5.5/Sonnet 5.5 | Official active model IDs; expensive non-exempt rungs excluded from capped profiles. [Fable][cf] [Opus][cop] [Sonnet][cs] |
| Gemini 3.8 Flash/4 Argon | Flash stable API documented. Argon's public ID/access UNVERIFIED in authoritative evidence collected; third-party pages report restricted rollout. Do not route it. [Gemini Flash][gf] [Argon report][ga] |
| Grok 4.7 | `grok-4.7` public API; Fast variant not public API. [xAI][xg] |

## 3. Situation matrix, per profile

All cells are proposals awaiting qualification. Role names remain exactly omo's names, implemented as original task contracts. No restricted omo code or community role plugin is required.

Harness codes: `Q` Qwen Code, `A` Aider, `G` Goose, `C` Codex, `P` Pi. `h/chain` binds harness to the entire ordered chain. `+` means peer workers, not fallback. Semicolon separates primary from acceptable alternate. Final chain exhaustion means **BLOCKED**, never silent substitution.

Role codes: `s` sisyphus; `e` explore; `l` librarian; `p` prometheus; `t` metis; `h` hephaestus; `a` atlas; `j` sisyphus-junior; `o` oracle; `m` momus; `v` multimodal-looker.

Category codes: `ve` visual-engineering; `ub` ultrabrain; `d` deep; `art` artistry; `q` quick; `lo` unspecified-low; `hi` unspecified-high; `w` writing. `ve/art` only apply to UI or slide-layout subcases. These are formatting/layout tasks, not media generation.

`m` runs on P/R; `s` runs on G/O and writes no deliverable. Main authors use the row's worker chain. Auxiliary `e,l,p,t,j` run Q/T, and `v` runs Q/V, even for Aider/Codex alternates. Hybrid A09's `o` alone uses Eh; its other planners use Th. P3 peers follow the shared contract without a central orchestrator. Goose media input is not assumed.

### Model and fallback definitions

Model shorthand: `DP` `deepseek-v4-pro`; `DF` `deepseek-flash`; `K3` `kimi-k3`; `K27` `kimi-k2.7-code`; `M3` `MiniMax-M3`; `MP` `mimo-v2.6-pro`; `MF` `mimo-v2.6-flash`; `Z` `glm-5.3`; `ZF` `glm-5.3-flash`; `Q35` `qwen3.5-plus`; `Q38` `qwen3.8-max`; `Sol` `gpt-6.1-sol`; `Astra` `gpt-6-astra`; `Luna` `gpt-6-luna`; `Opus` `claude-opus-5-5`; `Fable` `claude-fable-5-1`; `Gem` `gemini-3.8-flash`; `Grok` `grok-4.7`. Identifiers are supported by the candidate citations above.

| Profile | Orchestrator | Coding/ceiling | Utility/workflow | Vision | Reviewer |
|---|---|---|---|---|---|
| ultimate | Ou = Z→MF | Wu = K3→DP→K27 | Tu = K27→DF | Vu = K3→DF | Ru = M3→Q38 |
| global | Og = Z→Q38 | Wg = K3→Opus→DP; Eg = Fable→Opus→K3 | Tg = K27→DF | Vg = Gem→K3 | Rg = M3→Grok |
| hybrid | Oh = ZF→Q35 | Wh = K3→DP→K27; Eh = DP→K3→K27 | Th = DF→K27 | Vh = K27→DF | Rh = M3→MP |
| b4b | Ob = ZF→Q35 | Wb = DF→K27→DP | Tb = DF→K27 | Vb = DF→K27 | Rb = MP→M3 |

Codex chains: `Cu` = C/DP→C/DF→Q/K27, custom DeepSeek Responses provider only. `Cg` = C/Sol→C/Astra→C/Luna→Q/Wg. `Lh` = C/Luna→Q/Th; `Lb` = C/Luna→Q/Tb. Harness-changing fallback is explicit, not an invisible model replacement. Custom Responses providers and DeepSeek Responses support are documented; their combined runtime remains untested. [Codex][cc] [DeepSeek][dp]

For capped profiles, published output rates are DF ≤$1.20, DP ≤$3.96, K27 $4, ZF $0.50, Z $4.40, MP $0.87, MF $0.28, Luna $0.50 per million. Q35 Singapore is $2.40 or $3 by context tier; M3 Standard is $1.20 or $2.40. Pin that endpoint/tier, not merely the model name. [DeepSeek][dp] [Kimi][kp] [Z.ai][zp] [MiMo][mp] [Luna][luna] [Alibaba][ap] [MiniMax pricing][mprice]

Hybrid K3 is admitted only for flagship implementation and A09's oracle. All other roles use capped chains. B4b has no over-cap rung. This price policy is not a total-cost guarantee.

### ultimate

`U0` explicitly means **OpenCode+omo unavailable, D46; Codex/OpenAI unavailable, HK policy**. It applies in every row. Cu is the only admitted Codex route. Native access is the repo's stated assumption, not newly demonstrated; no geo-unlock proxy is proposed.

| Situation/priority | Pattern/coordinator | Orchestrator | Workers, primary; alternate | Sequence/categories | Reviewer | Rationale/availability |
|---|---|---|---|---|---|---|
| A01 regression repair, no adjacent defects | P2+P4/none | G/Ou | Q/Wu; A/Wu | s→e→h→m / d,q | P/Ru | Q headless/subagents; A lint/test alternate. U0 |
| A02 bounded feature, complete contract | P5+P4/Orca | G/Ou | Q/Wu; A/Wu | s→p→a→h→v→m / d,ve/art | P/Ru | parallel worktrees for separable modules. U0 |
| A03 refactor, preserve behavior | P5+P4/Orca | G/Ou | A/Wu; Q/Wu | s→e→a→h→m / d | P/Ru | A repo map; external differential tests. U0 |
| A04 CI/deploy diagnosis, reproducible rollback | P2+P4/none | G/Ou | Q/Tu; C/Cu | s→e→h→m / q,hi | P/Ru | JSON diagnosis; custom Codex sandbox alternate. U0 |
| A05 security, verified exploit closure | P5+P4/Orca | G/Ou | Q/Wu; A/Wu | s→t→e→h→m / ub,d | P/Ru | isolated audit/fix checkouts, not production scans. U0 |
| A06 change review, precision/recall | P2+P4/none | G/Ou | A/Tu; Q/Tu | s→e→o→m / lo,d | P/Ru | read-only ask/review contracts; no editing. U0 |
| A07 research, claim-level support | P3+P4/none | none | G/Tu+Q/Tu; G/Tu+A/Tu | l→t→j→m / w | P/Ru | source retrieval plus independent citation audit. U0 |
| A08 reconciliation, exact totals | P3+P4/none | none | G/Tu+Q/Tu; G/Tu+A/Tu | e→a→j→m / d | P/Ru | recipes and separate reproducible scripts. U0 |
| A09 architecture, constraint consistency | P2+P4/none | G/Ou | Q/Wu; A/Wu | s→p→t→o→m / ub,hi,w | P/Ru | named read-only planners; documents frozen before review. U0 |
| A10 policy workflow, authorized final state | P3+P4/none | none | G/Tu+Q/Tu; G/Tu+C/Cu | t→j→m / hi,q | P/Ru | allowlisted recipes and synthetic state simulator. U0 |
| A11 browser administration, correct records | P3+P4/none | none | G/Tu+Q/Vu; G/Tu+C/Cu | v→j→m / ve,q | P/Ru | official Q Playwright add-on; C uses local MCP too. U0 |
| A12 office work, consistent artifacts | P3+P4/none | none | G/Tu+Q/Vu; G/Tu+C/Cu | l→v→a→j→m / w,art | P/Ru | recipe/file work plus separate browser handoff. U0 |

### global

No region or unit-price cap. Extra spending is a permitted option, not evidence of higher quality.

| Situation/priority | Pattern/coordinator | Orchestrator | Workers, primary; alternate | Sequence/categories | Reviewer | Rationale |
|---|---|---|---|---|---|---|
| A01 repair, no adjacent defects | P2+P4/none | G/Og | Q/Wg; C/Cg | s→e→h→m / d,q | P/Rg | Q delegation; Codex sandbox alternate |
| A02 feature, complete contract | P5+P4/Orca | G/Og | Q/Wg; C/Cg | s→p→a→h→v→m / d,ve/art | P/Rg | independent module worktrees |
| A03 refactor, preserve behavior | P5+P4/Orca | G/Og | A/Wg; Q/Wg | s→e→a→h→m / d | P/Rg | repo map and explicit editor inventory |
| A04 diagnosis, reproducible rollback | P2+P4/none | G/Og | C/Cg; Q/Wg | s→e→h→m / q,hi | P/Rg | command sandbox, noninteractive exec |
| A05 security, exploit closure | P5+P4/Orca | G/Og | Q/Eg; C/Cg | s→t→e→h→m / ub,d | P/Rg | configurable tools and isolated remediation |
| A06 review, precision/recall | P2+P4/none | G/Og | A/Tg; Q/Tg | s→e→o→m / lo,d | P/Rg | bounded read-only findings |
| A07 research, claim support | P3+P4/none | none | G/Tg+Q/Tg; G/Tg+A/Tg | l→t→j→m / w | P/Rg | retrieval and separately assembled evidence |
| A08 reconciliation, exact totals | P3+P4/none | none | G/Tg+Q/Tg; G/Tg+A/Tg | e→a→j→m / d | P/Rg | reproducible script artifacts |
| A09 architecture, consistent constraints | P2+P4/none | G/Og | Q/Eg; A/Eg | s→p→t→o→m / ub,hi,w | P/Rg | explicit ceiling-model planning option |
| A10 policy, authorized state | P3+P4/none | none | G/Tg+Q/Tg; G/Tg+C/Cg | t→j→m / hi,q | P/Rg | recipe allowlists, simulator receipts |
| A11 browser, correct records | P3+P4/none | none | G/Tg+Q/Vg; G/Tg+C/Cg | v→j→m / ve,q | P/Rg | Q's OSS browser path; Codex browser backend not assumed |
| A12 office, artifact consistency | P3+P4/none | none | G/Tg+Q/Vg; G/Tg+C/Cg | l→v→a→j→m / w,art | P/Rg | multimodal transport on Q; document tooling on G |

### hybrid, default

| Situation/priority | Pattern/coordinator | Orchestrator | Workers, primary; alternate | Sequence/categories | Reviewer | Rationale |
|---|---|---|---|---|---|---|
| A01 repair, no adjacent defects | P2+P4/none | G/Oh | Q/Wh; A/Wh | s→e→h→m / d,q | P/Rh | exempt coder; bounded JSON handoff |
| A02 feature, complete contract | P5+P4/Orca | G/Oh | Q/Wh; A/Wh | s→p→a→h→v→m / d,ve/art | P/Rh | flagship implementation; worktree modules |
| A03 refactor, preserve behavior | P5+P4/Orca | G/Oh | A/Wh; Q/Wh | s→e→a→h→m / d | P/Rh | exempt implementation, repo map |
| A04 diagnosis, reproducible rollback | P2+P4/none | G/Oh | Q/Th; C/Lh | s→e→h→m / q,hi | P/Rh | capped troubleshooting; structured output |
| A05 security, exploit closure | P5+P4/Orca | G/Oh | Q/Wh; A/Wh | s→t→e→h→m / ub,d | P/Rh | exempt remediation, isolated patches |
| A06 review, precision/recall | P2+P4/none | G/Oh | A/Th; Q/Th | s→e→o→m / lo,d | P/Rh | cheap initial findings; external reviewer |
| A07 research, claim support | P3+P4/none | none | G/Th+Q/Th; G/Th+A/Th | l→t→j→m / w | P/Rh | capped retrieval, claim audit |
| A08 reconciliation, exact totals | P3+P4/none | none | G/Th+Q/Th; G/Th+A/Th | e→a→j→m / d | P/Rh | scripts, not verbal arithmetic |
| A09 architecture, consistent constraints | P2+P4/none | G/Oh | Q/Eh; A/Eh | s→p→t→o→m / ub,hi,w | P/Rh | K3 only oracle; other planning roles Th |
| A10 policy, authorized state | P3+P4/none | none | G/Th+Q/Th; G/Th+C/Lh | t→j→m / hi,q | P/Rh | capped allowlisted simulator work |
| A11 browser, correct records | P3+P4/none | none | G/Th+Q/Vh; G/Th+C/Lh | v→j→m / ve,q | P/Rh | capped vision; official browser add-on |
| A12 office, artifact consistency | P3+P4/none | none | G/Th+Q/Vh; G/Th+C/Lh | l→v→a→j→m / w,art | P/Rh | capped file/browser split |

### b4b

| Situation/priority | Pattern/coordinator | Orchestrator | Workers, primary; alternate | Sequence/categories | Reviewer | Rationale |
|---|---|---|---|---|---|---|
| A01 repair, no adjacent defects | P2+P4/none | G/Ob | A/Wb; Q/Wb | s→e→h→m / d,q | P/Rb | one-shot boundary; lint/test support |
| A02 feature, complete contract | P2+P4/none | G/Ob | Q/Wb; A/Wb | s→p→a→h→v→m / d,ve/art | P/Rb | avoid coordinator setup for bounded scope |
| A03 refactor, preserve behavior | P2+P4/none | G/Ob | A/Wb; Q/Wb | s→e→a→h→m / d | P/Rb | repo map; serial edits reduce merge work |
| A04 diagnosis, reproducible rollback | P2+P4/none | G/Ob | Q/Tb; C/Lb | s→e→h→m / q,hi | P/Rb | capped headless analysis |
| A05 security, exploit closure | P5+P4/Orca | G/Ob | Q/Wb; A/Wb | s→t→e→h→m / ub,d | P/Rb | isolation retained despite cost preference |
| A06 review, precision/recall | P2+P4/none | G/Ob | A/Tb; Q/Tb | s→e→o→m / lo,d | P/Rb | bounded initial scan |
| A07 research, claim support | P3+P4/none | none | G/Tb+Q/Tb; G/Tb+A/Tb | l→t→j→m / w | P/Rb | peer evidence batches, no added coordinator |
| A08 reconciliation, exact totals | P3+P4/none | none | G/Tb+Q/Tb; G/Tb+A/Tb | e→a→j→m / d | P/Rb | deterministic scripts |
| A09 architecture, consistent constraints | P2+P4/none | G/Ob | Q/Wb; A/Wb | s→p→t→o→m / ub,hi,w | P/Rb | DP escalation stays under cap |
| A10 policy, authorized state | P3+P4/none | none | G/Tb+Q/Tb; G/Tb+C/Lb | t→j→m / hi,q | P/Rb | synthetic receipts, limited tools |
| A11 browser, correct records | P3+P4/none | none | G/Tb+Q/Vb; G/Tb+C/Lb | v→j→m / ve,q | P/Rb | current DF vision; separate final-state check |
| A12 office, artifact consistency | P3+P4/none | none | G/Tb+Q/Vb; G/Tb+C/Lb | l→v→a→j→m / w,art | P/Rb | local document tools and draft-only handoffs |

A11 uses pinned local Playwright MCP, not the official example's personal browser profile. A12 proposes LibreOffice for document rendering/recalculation and simulated applications, not proprietary verification backends. Add-on setup counts toward attention/cost. [Qwen Playwright example][qp] [Playwright MCP][pm] [LibreOffice licensing][lib]

## 4. Independence audit

Audit covers every primary, alternate, fallback, auxiliary model, and artifact-producing role. Model family means vendor lineage, not provider route or deployment name.

| Profile/cells | Worker harness/family union | Reviewer harness/family union | Orchestrator overlap |
|---|---|---|---|
| ultimate A01–A12 | Q,A,G,C / Moonshot,DeepSeek | P / MiniMax,Qwen | none in P2/P5; absent P3 |
| global A01–A12 | Q,A,G,C / Moonshot,DeepSeek,Anthropic,OpenAI,Google | P / MiniMax,xAI | none in P2/P5; absent P3 |
| hybrid A01–A12 | Q,A,G,C / Moonshot,DeepSeek,OpenAI | P / MiniMax,Xiaomi | none in P2/P5; absent P3 |
| b4b A01–A12 | Q,A,G,C / Moonshot,DeepSeek,OpenAI | P / Xiaomi,MiniMax | none in P2/P5; absent P3 |

No cell needs `ABSOLUTE-EXCEPTION`. Goose workers occur only in P3, where Goose is not orchestrator. Qwen as harness is not Qwen as model family.

Fixes already applied: rejected native omo Momus review; removed worker-side Qwen/MiniMax utility substitutions; avoided MiMo workers in capped profiles; exposed Codex's harness-changing fallbacks. Aider's main/editor/weak models must stay inside the worker union. Qwen's fast/advisor/vision models and Goose subagent models must also obey it.

This is a static design audit, not a runtime pass. Reject any configuration that introduces reviewer-family work before review. If a reviewer authors a repair, allocate a new independent reviewer. Momus is the repair reviewer, not the existing protocol's complete two-judge final panel.

## 5. Cross-situation rules

1. Eligibility first. Never count an OSS client as clearance of a restricted plugin or proprietary verification backend.
2. Reserve review families before allocating workers. Apply exclusions to the union of every primary, alternate, fallback, editor and looker, not just the successful model.
3. Use P2 for bounded coding; add P5 only for separable modules or security isolation. Worktrees isolate checkouts, not authority or running processes.
4. P1 is unavailable as the literal omo plugin under D46, and native review would still fail independence. A separately approved original OSS implementation would still need P4.
5. Use P3 for file/app workflows when peers can exchange immutable artifacts. No personal browser profiles, unscoped databases, cross-task memory, or worker-writable final evaluator.
6. A bundled browser wins only after source/backend eligibility is established. Qwen's documented local Playwright path currently provides clearer OSS evidence than Codex's browser configuration. [Qwen example][qp] [Codex reference][cc]
7. Completion is a state transition, not a cheerful message. Freeze only after accepted artifact identity and settled execution; record cancellation separately. Pi requires `agent_settled`; Orca distinguishes enqueue from acceptance. [Pi RPC][pir] [Orca guide][oro]

## 6. Risks and unknowns

First verify the omo licensing conflict, then controller adapters. Orca advertises many agents but its supervised examples do not establish equivalent control for all seven; DSH's official material does not establish a headless dispatch/settlement protocol. Hence DSH is not a matrix default. [Orca][or] [Orchestration][oro] [DSH][dshsite]

Proposed handoff fields: task/attempt/dispatch IDs, immutable input/artifact hashes, source harness, effective model family, endpoint/tier, dependency IDs, action allowlist, cumulative usage, settlement status, and evidence pointers. Reject duplicate or superseded results. Cancellation must invalidate publication authority even if an external process finishes later. These are proposed requirements, not existing adapters. Original adapters require an OSS licence and qualification before use.

Qualify public/synthetic tests for delayed completion after cancellation, duplicate messages, hidden auxiliary models, truncated evidence and dropped browser sessions. Qwen's tool-call cap excludes subagent inner calls and some structured-output retries; maintain an outer cumulative ledger. [Qwen headless][qh] Pi has no built-in security permission boundary; Playwright MCP explicitly is not a security boundary. Use independent process/network isolation. [Pi][pi] [Playwright MCP][pm]

Alias drift is unusually important: retired DeepSeek Flash IDs remain accepted while changing the served model. Store the effective version and price revision, not just requested ID. MiMo v2.5 also has a dated retirement. [DeepSeek][dp] [MiMo][mp]

HK eligibility remains an assumption from the supplied [repository mapping](../../../EXAMPLE-MAPPING.md); endpoint location alone does not prove HK customer access. Codex custom-provider support is documented, not runtime-qualified. [Codex providers][cc] Block rather than replace Cu with OpenAI. No private data, secrets, real credentials, personal browser profiles, or production applications enter the future fixtures.

No affinity, task-success, latency or cost-per-accepted-task ordering has been measured. Preserve the existing fewer-defects → less-attention → faster-accepted-delivery → lower-total-cost priority, bounded repair, pilot scope and global limits. These 48 design rows do not authorize 48 runs or expand evaluation-1. [Repository decisions](../../evaluation-1/DECISIONS.md) [Benchmark scope](../../evaluation-1/BENCHMARKS.md)

Media generation capability note: none of the frozen twelve situations inherently requires generated image/audio/video. No media generator is routed; multimodal input and office rendering are separate capabilities.

## 7. Sources

Supplied harness/coordinator notes and raw extracts were read alongside all requested repository profiles, routing, mapping, omo example and evaluation-1 evidence. Fresh model/control extracts are saved in `mm-orch/sol-research/models.jsonl` and `controls.jsonl`.

- OpenCode: https://opencode.ai/docs/ ; https://opencode.ai/docs/agents/ ; https://opencode.ai/docs/mcp-servers/ ; https://opencode.ai/docs/plugins/ ; https://opencode.ai/docs/providers/ ; https://opencode.ai/docs/sdk/
- OpenCode license: https://raw.githubusercontent.com/anomalyco/opencode/dev/LICENSE
- omo: https://github.com/code-yeongyu/oh-my-openagent ; https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/LICENSE.md
- Codex: https://github.com/openai/codex ; https://developers.openai.com/codex/config-reference/ ; https://developers.openai.com/codex/config-advanced/
- DSH: https://github.com/deepseek-ai/deepseek-harness/ ; https://www.deepseek.com/en/harness/ ; https://github.com/royenheart/dsh-plugin-opencode-omo
- Pi: https://github.com/earendil-works/pi ; https://pi.dev/ ; https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/rpc.md
- Qwen Code: https://github.com/QwenLM/qwen-code ; https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/ ; https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/ ; https://qwenlm.github.io/qwen-code-docs/en/blog/cases/obsidian/
- Qwen headless: https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/
- Aider: https://github.com/Aider-AI/aider ; https://aider.chat/docs/scripting.html ; https://aider.chat/docs/usage/modes.html
- Goose: https://github.com/block/goose ; https://goose-docs.ai/docs/getting-started/using-extensions ; https://goose-docs.ai/docs/guides/context-engineering/subagents/ ; https://goose-docs.ai/docs/tutorials/headless-goose/
- Orca: https://github.com/stablyai/orca ; https://github.com/stablyai/orca/blob/main/skill-guides/orchestration.md
- Other coordinators: https://aq.dev/ ; https://github.com/BloopAI/vibe-kanban ; https://www.vibekanban.com/blog/shutdown ; https://github.com/nimbalyst/nimbalyst ; https://github.com/generalaction/emdash ; https://github.com/superset-sh/superset ; https://www.conductor.build/llms.txt
- Warp/Oz: https://www.warp.dev/blog/warp-is-now-open-source ; https://docs.warp.dev/platform/orchestration/
- DeepSeek: https://api-docs.deepseek.com/quick_start/pricing
- Kimi: https://platform.kimi.ai/docs/overview ; https://platform.kimi.ai/docs/pricing/chat
- Z.ai: https://docs.z.ai/guides/overview/pricing
- Qwen models/pricing: https://qwen.ai/blog?id=qwen3.8 ; https://qwen.ai/blog?id=qwen3.7-plus ; https://qwen.ai/blog?id=qwen3.6 ; https://qwen.ai/blog?id=qwen3.5 ; https://www.alibabacloud.com/help/en/model-studio/model-pricing
- MiniMax: https://www.minimax.io/models/text/m3 ; https://platform.minimax.io/docs/guides/pricing-paygo
- MiMo: https://mimo.mi.com/docs/en-US/pricing
- OpenAI: https://developers.openai.com/api/docs/models ; https://developers.openai.com/api/docs/models/gpt-6.1-sol ; https://developers.openai.com/api/docs/models/gpt-6-astra ; https://developers.openai.com/api/docs/models/gpt-6-luna.md
- Anthropic: https://platform.claude.com/docs/en/models/fable-5-1/overview ; https://platform.claude.com/docs/en/models/opus-5-5/overview ; https://platform.claude.com/docs/en/models/sonnet-5-5/overview
- Google/xAI: https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash ; https://docs.x.ai/developers/grok-4-7.md
- Non-authoritative Argon access report: https://gemini4argon.com/api/
- Affinity checks: https://deepinfra.com/blog/deepseek-harness-review ; https://aireiter.com/blog/deepseek-harness ; https://regolo.ai/harness-engineering-for-qwen3-8-27b-a-technical-guide-to-pi-opencode-and-kilo-code/
- Verification: https://github.com/microsoft/playwright-mcp ; https://www.libreoffice.org/about-us/licenses/

[ocl]: https://raw.githubusercontent.com/anomalyco/opencode/dev/LICENSE
[omol]: https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/LICENSE.md
[omo]: https://github.com/code-yeongyu/oh-my-openagent
[oc]: https://opencode.ai/docs/
[oca]: https://opencode.ai/docs/agents/
[ocm]: https://opencode.ai/docs/mcp-servers/
[ocp]: https://opencode.ai/docs/plugins/
[ocv]: https://opencode.ai/docs/providers/
[ocs]: https://opencode.ai/docs/sdk/
[dsh]: https://github.com/deepseek-ai/deepseek-harness/
[dshsite]: https://www.deepseek.com/en/harness/
[dshomo]: https://github.com/royenheart/dsh-plugin-opencode-omo
[codex]: https://github.com/openai/codex
[cc]: https://developers.openai.com/codex/config-reference/
[ca]: https://developers.openai.com/codex/config-advanced/
[pi]: https://github.com/earendil-works/pi
[pis]: https://pi.dev/
[pir]: https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/rpc.md
[q]: https://github.com/QwenLM/qwen-code
[qs]: https://qwenlm.github.io/qwen-code-docs/en/users/configuration/settings/
[qa]: https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/
[qp]: https://qwenlm.github.io/qwen-code-docs/en/blog/cases/obsidian/
[qh]: https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/
[a]: https://github.com/Aider-AI/aider
[as]: https://aider.chat/docs/scripting.html
[am]: https://aider.chat/docs/usage/modes.html
[g]: https://github.com/block/goose
[ge]: https://goose-docs.ai/docs/getting-started/using-extensions
[gs]: https://goose-docs.ai/docs/guides/context-engineering/subagents/
[gh]: https://goose-docs.ai/docs/tutorials/headless-goose/
[or]: https://github.com/stablyai/orca
[oro]: https://github.com/stablyai/orca/blob/main/skill-guides/orchestration.md
[aq]: https://aq.dev/
[vk]: https://github.com/BloopAI/vibe-kanban
[vks]: https://www.vibekanban.com/blog/shutdown
[n]: https://github.com/nimbalyst/nimbalyst
[em]: https://github.com/generalaction/emdash
[su]: https://github.com/superset-sh/superset
[co]: https://www.conductor.build/llms.txt
[wb]: https://www.warp.dev/blog/warp-is-now-open-source
[wo]: https://docs.warp.dev/platform/orchestration/
[di]: https://deepinfra.com/blog/deepseek-harness-review
[ar]: https://aireiter.com/blog/deepseek-harness
[reg]: https://regolo.ai/harness-engineering-for-qwen3-8-27b-a-technical-guide-to-pi-opencode-and-kilo-code/
[dp]: https://api-docs.deepseek.com/quick_start/pricing
[ki]: https://platform.kimi.ai/docs/overview
[kp]: https://platform.kimi.ai/docs/pricing/chat
[zp]: https://docs.z.ai/guides/overview/pricing
[q38]: https://qwen.ai/blog?id=qwen3.8
[q37]: https://qwen.ai/blog?id=qwen3.7-plus
[q36]: https://qwen.ai/blog?id=qwen3.6
[q35]: https://qwen.ai/blog?id=qwen3.5
[ap]: https://www.alibabacloud.com/help/en/model-studio/model-pricing
[mm]: https://www.minimax.io/models/text/m3
[mprice]: https://platform.minimax.io/docs/guides/pricing-paygo
[mp]: https://mimo.mi.com/docs/en-US/pricing
[models]: https://developers.openai.com/api/docs/models
[sol]: https://developers.openai.com/api/docs/models/gpt-6.1-sol
[astra]: https://developers.openai.com/api/docs/models/gpt-6-astra
[luna]: https://developers.openai.com/api/docs/models/gpt-6-luna.md
[cf]: https://platform.claude.com/docs/en/models/fable-5-1/overview
[cop]: https://platform.claude.com/docs/en/models/opus-5-5/overview
[cs]: https://platform.claude.com/docs/en/models/sonnet-5-5/overview
[gf]: https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash
[ga]: https://gemini4argon.com/api/
[xg]: https://docs.x.ai/developers/grok-4-7.md
[pm]: https://github.com/microsoft/playwright-mcp
[lib]: https://www.libreoffice.org/about-us/licenses/
