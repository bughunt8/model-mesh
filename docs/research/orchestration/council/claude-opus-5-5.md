# Cross-harness orchestration matrix for model-mesh: council proposal (Claude Opus 5.5)

Design proposal; nothing measured. Facts dated 2026-10-11; "n.s." = not stated. Pilot data public/synthetic only, no secrets.

**My angle.** (a) Independence must hold across the **whole fallback chain**, so each profile gets three family pools that share no family (worker W, orchestrator O, reviewer R). (b) Licence and plan terms limit which harness may carry which model. (c) The repo's profiles already break the rule, and several model IDs are stale.

**Vendor neutrality.** I am an Anthropic model. Anthropic (AN) appears only in `global`, only as orchestrator (following omo's published recommendation), never as reviewer.

**Legend.** Harnesses: OC = OpenCode + omo; DSH; CX = Codex CLI; PI; QC = Qwen Code; AD = Aider; GO = Goose. Model families: DS DeepSeek, KM Kimi/Moonshot, GL Z.ai GLM, QW Qwen, MM MiniMax, MI Xiaomi MiMo, OA OpenAI, AN Anthropic, GG Google, XA xAI.

---

## 0. Findings that change the design (verify first)

| # | Finding | Effect |
|---|---|---|
| F1 | omo's `LICENSE.md` is the **Sustainable Use License 1.0**. It allows internal business use, and distribution only free of charge for non-commercial purposes ([omo LICENSE](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/LICENSE.md)). It is described as fair-code, not OSI, with PostHog telemetry on by default ([ai-heartland](https://ai-heartland.com/explain/oh-my-openagent/)). A SourceForge mirror says MIT (conflict). | OC+omo = OSS harness ([MIT](https://github.com/anomalyco/opencode/blob/dev/LICENSE)) plus a **source-available plugin**: `D46-EXCEPTION(plugin)`. omo names stay as a role contract. D05 client use needs a licence check. Set `OMO_DISABLE_POSTHOG=1`. |
| F2 | omo restricted Hephaestus to GPT-native models in v4.10.0 ([release](https://newreleases.io/project/github/code-yeongyu/oh-my-openagent/release/v4.10.0)). An earlier issue said it was limited to OpenAI/OpenCode providers ([#2133](https://github.com/code-yeongyu/oh-my-openagent/issues/2133)). omo v5.1.29 (2026-10-09) installation docs use the new names main agent / plan-consultant / plan-reviewer and an `architect` category ([install guide](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/guide/installation.md), [releases](https://github.com/code-yeongyu/oh-my-openagent/releases)). | Repo `ultimate` maps `hephaestus` to DeepSeek; current omo may reject it. Fallback: `atlas` + `deep`. Pin omo and check classic names load. |
| F3 | Codex runs HK-reachable models through **vendor-documented** custom providers. Kimi K3 uses `wire_api = "responses"` ([Kimi guide](https://platform.kimi.ai/docs/guide/codex-kimi)). DeepSeek's API is "specifically adapted for Codex" ([DeepSeek changelog](https://api-docs.deepseek.com/updates/)). Qwen APIs speak the Responses protocol for Codex ([Qwen3.8-Max blog](https://www.alibabacloud.com/blog/603421)). MiMo is "supported in the latest Codex" ([MiMo docs](https://mimo.mi.com/docs/welcome)). | CX is **available in `ultimate`** via these providers; CX on the OpenAI provider is UNAVAILABLE. Browser/Computer Use under custom providers: n.s. |
| F4 | GLM Coding Plan "is limited to use within the following officially supported tools": of our harnesses, only OpenCode, Codex, Pi, Goose ([Z.ai tools](https://docs.z.ai/devpack/tool/others)). | GLM on DSH, QC or AD needs metered API. Alibaba Model Studio lists `glm-5.3` in Hong Kong ([Model Studio](https://www.alibabacloud.com/help/en/model-studio/glm-5-3)): a **different-provider, same-family** lifeline. |
| F5 | ID churn. `deepseek-v4-flash` now routes to V4.1-Flash (`deepseek-flash`), and V4-Pro is continued ([DeepSeek V4.1](https://www.deepseek.com/en/news/deepseek-v4-1-flash/), [changelog](https://api-docs.deepseek.com/updates/)). MiMo V2.5 IDs become invalid on 2026-10-21 ([MiMo docs](https://mimo.mi.com/docs/welcome)), which breaks the repo's `mimo-v2.5-free`. | Update the IDs before any pilot. |
| F6 | Candidate check. Gemini 4 Argon is limited to Fairwind partners, with no public model ID ([Apidog](https://apidog.com/blog/gemini-4-argon-api/)). "GPT-6.1 Luna" is not found; GPT-6 Luna exists ([OpenAI](https://developers.openai.com/api/docs/models/gpt-6-luna)). Verified: GPT-6.1 Sol ([OpenAI](https://developers.openai.com/api/docs/models/gpt-6.1-sol)), Opus 5.5 ([Anthropic](https://platform.claude.com/docs/en/models/opus-5-5/overview)), Sonnet 5.5 ([Anthropic](https://platform.claude.com/docs/en/models/sonnet-5-5/overview)), Fable 5.1 ([Anthropic](https://platform.claude.com/docs/en/models/fable-5-1/overview)), Grok 4.7 ([xAI](https://docs.x.ai/developers/release-notes)), Gemini 3.8 Flash ([Google](https://ai.google.dev/gemini-api/docs/latest-model)), MiMo V2.6 Pro/Flash/Pro-UltraSpeed ([MiMo](https://mimo.mi.com/docs/welcome)), Kimi K3 ([OpenRouter](https://openrouter.ai/moonshotai/kimi-k3)), Qwen3.8-Max ([Alibaba](https://www.alibabagroup.com/document-2021044032125272064)). | Argon and "6.1 Luna" are excluded from every cell. |
| F7 | Repo self-audit. `momus` = `hephaestus` model in `ultimate.example.json` (DS V4-Pro) and `hybrid.example.json` (gpt-5.6-terra), same harness too. | Rule already broken; fixed in §4. |

Output prices (USD/1M): GLM-5.3 $4.40 and GLM-5.3-Flash $0.50 (repo, from [Z.ai pricing](https://docs.z.ai/guides/overview/pricing)); K2.7-code about $4.00 (repo); DS V4-Pro $3.96 at peak (repo); DS V4.1-Flash $0.60 ([OpenRouter](https://openrouter.ai/deepseek/deepseek-v4.1-flash)); MiniMax M3 $0.96 ([OpenRouter](https://openrouter.ai/minimax/minimax-m3)); MiMo-V2.6-Pro $0.87 ([MiMo](https://mimo.mi.com/models/zh-CN/mimo-v2.6-pro)); Qwen3.7-plus $1.60 list ([Requesty](https://www.requesty.ai/models/alibaba/qwen3.7-plus)); GPT-6 Luna $0.50; GPT-6.1 Sol $10; Kimi K3 about $15; Qwen3.8-max $6; Grok 4.7 $6; Sonnet 5.5 $10; Opus 5.5 $20. Gemini 3.8 Flash $3.75, **$7.50 from 2027-01-01** ([Google Cloud](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing)), over cap from then.

---

## 1. Harness capability table

**B** bundled (full weight); **O** official OSS add-on (setup cost); **C** community (no weight).

| Harness | Licence | Browser / Playwright | MCP | Memory | Audio/video/image input | LSP | Sandbox | Subagents / parallel | Headless / SDK / RPC | Worktree | Maturity risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| OC + omo | MIT core; omo SUL-1.0 (F1) | n.s.; Playwright MCP is O | B: local + remote ([docs](https://opencode.ai/docs/mcp-servers/)) | n.s. | image B; audio/video n.s. | B, off by default, 30+ servers ([LSP](https://opencode.ai/docs/lsp/)) | n.s. (permissions default to allow) | B: General/Explore/Scout; omo Team Mode (off) | B: `run` JSON, SDK abort | plugin context exposes `worktree`; native n.s. | Medium: v1.18.35; OpenCode 2 conflicts; omo licence/telemetry |
| DSH | MIT, public preview | C | C (`dsh-mcp-client`) | C | Voice input B (experimental); image n.s. | C (omo preset) | n.s. | B: Subagents plugin; Agent teams (experimental) | B: Python SDK over JSON-RPC stdio ([SDK](https://github.com/deepseek-ai/deepseek-harness/blob/master/python/sdk/README.md)) | C (`dsh-workflow-worktree`) | High: 0.1.x preview |
| CX | Apache-2.0 | B: Browser Use; Computer Use on macOS/Windows | B: stdio/HTTP; can also run as an MCP server | B, off by default | image B (`view_image`); video not supported ([Kimi guide](https://platform.kimi.ai/docs/guide/codex-kimi)) | n.s. (omo Light LSP MCP is SUL) | B: `sandbox_mode` | B: `multi_agent` (spawn/send/wait/close) | B: `codex exec` | n.s. | Low: 0.162.1 (2026-10-09); HK needs F3 |
| PI | MIT | n.s. | B with Codemode ([pi.dev](https://pi.dev/)) | C (packages) | n.s. | n.s. | **None built in**; containers via packages | **None built in**; C packages | B: print/JSON/RPC; steer, cancel, `agent_settled` ([RPC](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/rpc.md)) | C | Medium: v1.1.0, no permissions |
| QC | Apache-2.0 | n.s. (MCP can add it); Computer Use B | B: stdio/SSE/HTTP | B: Auto-Memory | B: image/PDF/audio/video; voice | B, experimental flag | B: `--sandbox` (off; Seatbelt allows network) ([sandbox](https://qwenlm.github.io/qwen-code-docs/en/users/features/sandbox/)) | B: subagents; Teams/Workflows experimental | B: `-p` stream-json, SDKs, `qwen serve`, ACP | B: subagent `working_dir` can pin a worktree | Low–medium; OAuth free tier ended 2026-04-15 ([auth](https://qwenlm.github.io/qwen-code-docs/en/users/configuration/auth/)) |
| AD | Apache-2.0 | `/web` URL fetch only | n.s. | n.s. | image `/add`/`/paste`; `/voice` | n.s. (repo map instead) | n.s. | n.s. (single agent; architect/editor model pair) | `--message` one-shot; Python API unofficial | n.s. (auto-commit) | **High**: last release v0.86.0 on 2025-08-09 ([releases](https://github.com/Aider-AI/aider/releases)) |
| GO | Apache-2.0 (AAIF) | B: Computer Controller (web automation); Playwright n.s. | B: extensions are MCP | B: Memory extension | n.s. | n.s.; Analyze (call graphs) B | Docker for extensions only | B: Summon (parallel, no nesting); sub-recipes | B: `goose run` recipes, JSON | n.s. | Low: v1.54.0 (2026-10-08) |

**Coordinators**

| Coordinator | Licence class | Harnesses named (of our 7) | Worktree isolation | Dispatch / steer / cancel evidence | Maintenance risk | OSS-default eligible |
|---|---|---|---|---|---|---|
| Orca | MIT | OC, DSH, CX, PI, GO, QC (+ any CLI) | Yes, per agent | `worker-start`, DAGs, ask/reply, `worker_done` settlement, `worker-stop`/`worker-abandon` ([orchestration](https://github.com/stablyai/orca/blob/main/skill-guides/orchestration.md)); examples only `codex`/`claude` | Low (ships daily) | **Yes: default** |
| Emdash | Apache-2.0 | OC, CX, QC | Yes (can be disabled) | Steer/cancel n.s. | Low–medium | Yes: alternate |
| Nimbalyst | MIT | CX; OC is alpha | Yes | n.s. | Medium | Yes, but used for review UI only |
| Vibe Kanban | Apache-2.0, sunsetting | OC, CX, QC | Cleanup flag only | n.s. | High (shutdown post) | Reference only |
| Warp | Client AGPL-3.0/MIT; **Oz and server proprietary** ([FAQ](https://github.com/warpdotdev/warp/blob/master/FAQ.md)) | CX (+ Warp Agent, Claude Code) | n.s. | Spawn one level deep; `CANCELLED` is a run state ([docs](https://docs.warp.dev/platform/orchestration/)) | Low | **Labelled exception** (needs Oz for cloud) |
| Superset | ELv2, source-available | OC, CX | Yes, but "not a sandbox" | CLI/SDK/MCP manage workspaces; cancel n.s. | Low | Labelled exception |
| Conductor | Licence n.s., Mac only | OC, CX | Yes | API present; cancel n.s. | Medium | Excluded (reference) |
| AQ | Not stated; hosted | OC, PI | Yes | n.s. | Unknown | Excluded |

---

## 2. Harness–model affinity

| Harness | Documented default or favoured models | Independent evidence | Verdict |
|---|---|---|---|
| OC + omo | omo: Hephaestus GPT-native; Sisyphus Claude/Kimi/GLM; visual Gemini → Qwen; MiniMax "never for Hephaestus/Oracle" ([model matching](https://omo.vibetip.help/docs/agents/model-matching)); main agent Opus 5.5 or GPT-6 ([install](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/guide/installation.md)). DeepSeek V4.1-Flash partner; built-in MiniMax M3 ([MiniMax](https://platform.minimax.io/docs/token-plan/other-tools.md)). | 50-task Terminal-Bench Pro subset: 50% (Qwen 3.6 Plus) / 46% (MiniMax M2.5), about 40× Goose's tokens ([scaffold study](https://arxiv.org/html/2607.22585v1)); older models | Role fit maintainer-asserted; harness fit `UNMEASURED` |
| DSH | SDK default `deepseek-flash`, effort `max` ([eval patch](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/evaluation/dsh-minimal.patch)). DeepSeek's own coding-agent benchmarks ran in "DeepSeek Harness minimal mode" ([changelog](https://api-docs.deepseek.com/updates/)). | None independent | "DSH best with DeepSeek Flash": **vendor-supported, `UNMEASURED`** |
| CX | Default `gpt-6.1-sol`; "works best with the recommended models" ([Codex models](https://www.codex-docs.com/en/docs/models)); Kimi/DeepSeek/Qwen/MiMo vendor docs (F3); Qwen3.8-Max RL-trained on Codex ([Qwen blog](https://www.alibabacloud.com/blog/603421)) | None | OA = vendor default; rest `UNMEASURED` |
| PI | `defaultModel: Automatic`; Z.ai and MiniMax list Pi | None | `UNMEASURED` |
| QC | "Qwen Code is deeply optimized for the Qwen series" ([Qwen blog](https://www.alibabacloud.com/blog/603421)). MiniMax repeats "optimized for the Qwen model family". | Qwen3.8-Max's RL harness list **omits Qwen Code** | "QC best with Qwen3.8": **`UNMEASURED`** (series-level vendor claim); tie-breaker only |
| AD | README: Claude 3.7, DeepSeek R1/V3, o1, o3-mini, GPT-4o (stale) | Polyglot leaderboard holds only 2025 models ([Steel](https://leaderboard.steel.dev/leaderboards/aider/)) | `UNMEASURED` |
| GO | "works best with Claude 4 models" (dated) ([providers](https://goose-docs.ai/docs/getting-started/providers)); Z.ai Coding Plan is a built-in provider | Most token-efficient in the scaffold study (28k tokens/solved task); 38% with MiniMax M2.5 | Weak independent token signal; affinity `UNMEASURED` |

---

## 3. Situation matrices

**Table rules:** W, O and R pools share no family, and every fallback stays in its pool. The reviewer harness is never a worker harness in the same cell. In-harness omo `momus`/`oracle` are internal gates only. Acceptance = frozen OSS check (pytest/Playwright Test/ZAP) plus the independent reviewer. "Controller" = the evaluation-1 pilot controller. Notation: `harness:agent@ladder`.

### 3.1 `ultimate` (Hong Kong-native: DS, KM, GL, QW, MM, MI only)

Ladders:
- **U-O** [GL]: GLM-5.3 (Z.ai) → GLM-5.3 (Alibaba HK region) → GLM-5.3-Flash.
- **U-W** [DS, KM]: DS V4-Pro max → Kimi K3 → K2.7-code.
- **U-Wf**: DS V4.1-Flash → K2.7-code.
- **U-Wv** [MM, KM]: MiniMax M3 → Kimi K3.
- **U-R** [QW, MI]: Qwen3.8-max → MiMo-V2.6-Pro → Qwen3.7-plus; reviewer utility: Qwen3.5-plus → MiMo-V2.6-Flash.
- **Swap (QC-worker rows):** worker U-Wq [QW, MI] = Qwen3.8-max → Qwen3.7-plus → MiMo-V2.6-Pro (vision: MiMo-V2.6-Pro); reviewer U-Rx [DS, KM] = DS V4-Pro → Kimi K3.

UNAVAILABLE in every row: CX with the OpenAI provider, and all OA/AN/GG/XA models. CX cells below use custom providers only (F3).

| # | Pattern / coordinator | Orchestrator | Worker: primary; alternate | omo sequence · categories | Independent reviewer | Rationale |
|---|---|---|---|---|---|---|
| A01 | P4 / controller | OC:sisyphus@U-O | OC:hephaestus@U-W (F2: else atlas); DSH@U-Wf | explore→hephaestus→momus(internal) · deep, quick | GO@U-R recipe; alt QC@U-R | OC LSP; Goose recipes + Analyze |
| A02 | P5 / Orca race | Orca + OC:sisyphus@U-O | OC:atlas@U-W; CX(K3)@U-W | prometheus→atlas→multimodal-looker@U-Wv · visual-engineering, deep | QC@U-R + Playwright Test | Orca race + Design Mode; CX Browser Use (unverified, custom provider) |
| A03 | P4 / controller | OC:sisyphus@U-O | OC:hephaestus@U-W; AD architect K3 / editor K2.7-code | explore→metis@U-W→hephaestus · deep | GO@U-R + differential tests | OC LSP rename; Goose call graphs; Aider repo map (risk: alternate only) |
| A04 | P2 / controller | OC:sisyphus@U-O | DSH@U-Wf; GO@U-W | explore→sisyphus-junior→hephaestus · quick, unspecified-high | CX(Qwen3.8-max)@U-R; alt QC@U-R | DSH SDK, vendor default; CX sandbox to reproduce |
| A05 | P5 / Orca | Orca + OC:sisyphus@U-O | CX(DS)@U-W; OC:hephaestus@U-W | librarian→oracle(internal)→hephaestus · ultrabrain, deep | R1 GO@U-R; R2 QC: MiMo-V2.6-Pro→Qwen3.7-plus; ZAP | CX bundled sandbox for exploit repro; two external reviewers |
| A06 | P3 + P4 / Orca fan-out | Orca + OC:sisyphus@U-O | (patch fixed, planted) | R1 GO:Qwen3.8-max; R2 DSH:DS V4-Pro | Adjudicator PI: Kimi K3→K2.7-code | Three families, three harnesses; Pi settle semantics |
| A07 | P2 / controller | OC:sisyphus@U-O | QC@U-Wq; GO@U-Wq | librarian→writing · writing, unspecified-high | DSH@U-Rx claim check; alt CX(K3)@U-Rx (`web_search` works with Kimi) | QC `web_fetch`/`web_search` (B with Token Plan) |
| A08 | P2 / controller | OC:sisyphus@U-O | QC@U-Wq; GO@U-Wq | explore→sisyphus-junior · unspecified-high | CX(DS)@U-Rx sandboxed recompute; alt DSH@U-Rx | QC headless batch analysis; known-answer checks decide |
| A09 | P1 + P4 / controller | OC:sisyphus@U-O | OC:prometheus@U-W; PI(RPC)@U-W | prometheus→metis→momus(internal) · ultrabrain, writing | QC@U-R traceability rubric; alt GO@U-R | omo planner chain; QC `/review` skill (B) |
| A10 | P2 / controller | OC:sisyphus@U-O | GO@U-W (`GOOSE_ALLOWLIST`, unanswered approval → blocked); CX(K3)@U-W | sisyphus-junior · unspecified-low/-high | QC@U-R + policy assertions; alt PI@U-R in a container | Goose allowlist; no silent approvals |
| A11 | P5 / Orca | Orca + OC:sisyphus@U-O | CX(K3)@U-W Browser Use (**verify**); GO@U-W Computer Controller | explore→multimodal-looker@U-Wv→atlas · visual-engineering | QC@U-R + Playwright Test final state; MiMo for screenshots | Bundled browser decides; CX-native is UNAVAILABLE |
| A12 | P5 / Orca | Orca + OC:sisyphus@U-O | QC@U-Wq (image/PDF/audio/video, Computer Use); CX(Qwen)@U-Wq | librarian→multimodal-looker@MiMo→writing · writing, unspecified-high | GO@U-Rx artifact-consistency recipe; alt DSH@U-Rx | Only QC bundles multimodal input + desktop control |

### 3.2 `hybrid` (default, global; cap $4.65 output on generalist, utility and orchestration rungs)

Ladders:
- **H-O** [GL]: GLM-5.3 ($4.40) → GLM-5.3-Flash.
- **H-W** [OA, KM], exempt flagship coder: GPT-6.1 Sol → Kimi K3 → K2.7-code.
- **H-Wf** [OA, QW], capped: GPT-6 Luna → Qwen3.5-plus.
- **H-Wv** [MM, QW]: MiniMax M3 → Qwen3.7-plus.
- **H-Wq** [QW, KM]: Qwen3.7-plus → K2.7-code. Qwen3.8-max ($6) only through `ultrawork`.
- **H-R** [DS, MI], capped momus: DS V4-Pro ($3.96) → MiMo-V2.6-Pro → DS V4.1-Flash.
- **H-Rx** [XA, DS], `oracle`-exempt: Grok 4.7 → DS V4-Pro.

| # | Pattern / coordinator | Orchestrator | Worker: primary; alternate | omo sequence · categories | Independent reviewer | Rationale |
|---|---|---|---|---|---|---|
| A01 | P4 / controller | OC:sisyphus@H-O | CX@H-W (GPT-6.1 Sol is the native default); OC:hephaestus@H-W | explore@H-Wf→hephaestus · deep, quick | DSH@H-R; alt GO@H-R | GPT-native Hephaestus fits CX; DS is the DSH default |
| A02 | P5 / Orca race | Orca + OC:sisyphus@H-O | CX@H-W vs OC:atlas@Kimi K3 | prometheus→atlas→multimodal-looker@H-Wv · visual-engineering, deep | GO@H-R + Playwright Test | Two worker families race; disjoint reviewer |
| A03 | P4 / controller | OC:sisyphus@H-O | OC:hephaestus@H-W; AD architect GPT-6.1 Sol / editor K2.7-code | explore→metis@H-Wq→hephaestus · deep | GO@H-R | LSP plus Goose Analyze |
| A04 | P2 / controller | OC:sisyphus@H-O | GO@H-Wf, escalate to CX@H-W; QC@H-Wq | sisyphus-junior→hephaestus · quick, unspecified-high | DSH@H-R | Goose token efficiency (weak signal) on capped rungs |
| A05 | P5 / Orca | Orca + OC:sisyphus@H-O | CX@H-W; OC:hephaestus@H-W | librarian→oracle(internal)→hephaestus · ultrabrain, deep | R1 DSH@H-R; R2 GO@H-Rx (oracle exempt); ZAP | Codex sandbox; strongest exempt reviewer |
| A06 | P3 + P4 / Orca | Orca + OC:sisyphus@H-O | (patch fixed) | R1 DSH: DS V4-Pro; R2 QC: Qwen3.7-plus | Adjudicator CX: GPT-6.1 Sol as oracle (exempt) | Three families, three harnesses |
| A07 | P2 / controller | OC:sisyphus@H-O | QC@H-Wq; CX@H-Wf with live `web_search` | librarian→writing · writing | DSH@H-R; alt GO@H-R | QC web tools; CX `web_search` modes (B) |
| A08 | P2 / controller | OC:sisyphus@H-O | QC@H-Wq; CX@H-Wf | explore→sisyphus-junior · unspecified-high | GO@H-R recompute recipe; alt DSH | Headless JSON; known-answer checks |
| A09 | P1 + P4 / controller | OC:sisyphus@H-O | OC:prometheus@Kimi K3 (exempt), oracle@GPT-6.1 Sol; PI@H-W | prometheus→metis@K2.7-code→oracle→momus(internal) · ultrabrain, writing | GO@H-Rx; alt DSH@H-R | Exempt architect plus exempt external reviewer |
| A10 | P2 / controller | OC:sisyphus@H-O | GO@H-Wf; CX@H-W (`approval_policy`) | sisyphus-junior · unspecified-low | DSH@H-R; alt PI@H-R (container) | Goose allowlist |
| A11 | P5 / Orca | Orca + OC:sisyphus@H-O | CX@H-W Browser Use (native); GO@K2.7-code | explore→multimodal-looker@H-Wv→atlas · visual-engineering | GO@H-R + Playwright Test (MiMo for vision); alt PI@H-R (built-in MCP plus Playwright MCP) | Bundled browser; GO reviews only when CX works |
| A12 | P5 / Orca | Orca + OC:sisyphus@H-O | QC@H-Wq + MiniMax M3 looker; CX@GPT-6.1 Sol Computer Use | librarian→multimodal-looker→writing · writing | GO@H-R; alt DSH@H-R | QC multimodal input (B) |

### 3.3 `b4b` (cap applied hard; the only exemption is `oracle` in A05 and A09)

Ladders:
- **B-O** [GL]: GLM-5.3-Flash → GLM-5.3.
- **B-W** [KM, OA, QW]: K2.7-code ($4.00) → GPT-6 Luna (max) → Qwen3.7-plus. Kimi K3 only as the second slot in `deep`.
- **B-Wf**: GPT-6 Luna → Qwen3.5-plus.
- **B-Wv**: MiniMax M3 → Qwen3.7-plus.
- **B-R** [MI, DS, GG]: MiMo-V2.6-Pro → DS V4.1-Flash → Gemini 3.8 Flash (**drops out on 2027-01-01**).
- **B-Rd** [DS] (DSH cells): DS V4.1-Flash → V4-Pro.
- **B-Rx** (oracle, A05/A09 only) [DS, GG]: DS V4-Pro max → Gemini 3.8 Flash.
- P5 only where worktree isolation is required.

| # | Pattern / coordinator | Orchestrator | Worker: primary; alternate | omo · categories | Reviewer | Rationale |
|---|---|---|---|---|---|---|
| A01 | P4 / controller | OC:sisyphus@B-O | OC:atlas@B-W; CX@B-Wf | explore@B-Wf→atlas · deep, quick | GO@B-R; alt DSH@B-Rd | Hephaestus needs GPT (F2): atlas |
| A02 | P4 / controller (no race) | OC:sisyphus@B-O | OC:atlas@B-W; CX@B-Wf | prometheus→atlas · visual-engineering | GO@B-R + Playwright Test | Racing is not worth the cost here |
| A03 | P4 / controller | OC:sisyphus@B-O | OC:atlas@B-W; AD@K2.7-code | explore→atlas · deep | GO@B-R + differential tests | LSP plus Analyze |
| A04 | P2 / controller | OC:sisyphus@B-O | GO@B-Wf; QC@B-W | sisyphus-junior · quick | DSH@B-Rd | Cheapest headless path |
| A05 | P5 / Orca | Orca + OC:sisyphus@B-O | CX@B-W; OC:atlas@B-W | librarian→atlas · deep | R1 DSH@B-Rx (oracle exempt); R2 GO@B-R; ZAP | Security keeps its exemption |
| A06 | P3 + P4 / controller | OC:sisyphus@B-O | (patch fixed) | R1 GO: MiMo-V2.6-Pro; R2 DSH: DS V4.1-Flash | Adjudicator QC: Qwen3.7-plus | Three cheap families |
| A07 | P2 / controller | OC:sisyphus@B-O | QC: Qwen3.7-plus→Qwen3.5-plus; CX@B-Wf | librarian→writing · writing | DSH@B-Rd | QC web tools |
| A08 | P2 / controller | OC:sisyphus@B-O | QC: Qwen3.7-plus; CX@B-Wf | sisyphus-junior · unspecified-low | GO@B-R | Deterministic checks dominate |
| A09 | P1 + P4 / controller | OC:sisyphus@B-O | OC:prometheus@B-W; PI@B-W | prometheus→metis→momus(internal) · writing | GO@B-Rx (oracle exempt) | Planning keeps its exemption |
| A10 | P2 / controller | OC:sisyphus@B-O | GO@B-Wf; CX@B-Wf | sisyphus-junior · unspecified-low | DSH@B-Rd | Allowlist |
| A11 | P5 / Orca | Orca + OC:sisyphus@B-O | CX@B-Wf Browser Use; GO@K2.7-code | multimodal-looker@B-Wv→atlas · visual-engineering | QC: MiMo-V2.6-Pro + Playwright Test | Bundled browser |
| A12 | P5 / Orca | Orca + OC:sisyphus@B-O | QC: Qwen3.7-plus + MiniMax M3; CX@B-Wf | librarian→writing · writing | GO@B-R; alt DSH@B-Rd | QC multimodal |

### 3.4 `global` (no region limit, no cap)

Ladders:
- **G-O** [AN, GL]: Opus 5.5 (omo's recommended main agent) → GLM-5.3.
- **G-W** [OA, KM]: GPT-6.1 Sol → GPT-6 Astra (`ultrawork`) → Kimi K3.
- **G-W2**: Kimi K3 → GPT-6.1 Sol.
- **G-Wf**: GPT-6 Luna → K2.7-code-highspeed.
- **G-Wv** [KM, MM]: Kimi K3 → MiniMax M3.
- **G-Wq** [QW, MM]: Qwen3.8-max → MiniMax M3.
- **G-R** [XA, GG]: Grok 4.7 → Gemini 3.8 Flash.
- **G-Rx** [DS, MI]: DS V4-Pro max → MiMo-V2.6-Pro.
- If AN is ever a worker (for example Fable 5.1 on A09), G-O drops to GLM-5.3.

| # | Pattern / coordinator | Orchestrator | Worker: primary; alternate | omo · categories | Reviewer | Rationale |
|---|---|---|---|---|---|---|
| A01 | P4 / controller | OC:sisyphus@G-O | CX@G-W; OC:hephaestus@G-W | explore@G-Wf→hephaestus · deep, quick | GO@G-R; alt DSH@G-Rx | CX vendor default |
| A02 | P5 / Orca race | Orca + OC:sisyphus@G-O | CX@G-W vs OC:atlas@G-W2 | prometheus→atlas→multimodal-looker@G-Wv · visual-engineering, deep | QC@G-R + Playwright Test | Race across families |
| A03 | P4 / controller | OC:sisyphus@G-O | OC:hephaestus@G-W; AD architect GPT-6.1 Sol | explore→metis@G-W2→hephaestus · deep | GO@G-R | LSP plus Analyze |
| A04 | P2 / controller | OC:sisyphus@G-O | CX@G-W; GO@G-Wf | sisyphus-junior→hephaestus · quick | DSH@G-Rx | CX sandbox |
| A05 | P5 / Orca | Orca + OC:sisyphus@G-O | CX@G-W (Astra `ultrawork`); OC:hephaestus@G-W | librarian→oracle(internal)→hephaestus · ultrabrain | R1 GO@G-R; R2 DSH@G-Rx; ZAP | Two external reviewers, four families |
| A06 | P3 + P4 / Orca, or Warp (exception) | Orca + OC:sisyphus@G-O | (patch fixed) | R1 GO: Grok 4.7; R2 DSH: DS V4-Pro | Adjudicator QC: Gemini 3.8 Flash | Warp's critic/verifier swarm only as a labelled exception |
| A07 | P2 / controller | OC:sisyphus@G-O | CX@G-W live `web_search`; QC@G-Wq | librarian→writing · writing | GO@G-R; alt DSH@G-Rx | CX `web_search` (B) |
| A08 | P2 / controller | OC:sisyphus@G-O | QC@G-Wq; CX@G-Wf | sisyphus-junior · unspecified-high | DSH@G-Rx recompute | Headless JSON |
| A09 | P1 + P4 / controller | OC:sisyphus@G-O | OC:prometheus@G-W2, oracle@GPT-6.1 Sol; PI@G-W | prometheus→metis→oracle→momus(internal) · ultrabrain, writing | GO@G-R; alt QC@G-Rx | Strongest planning chain |
| A10 | P2 / controller | OC:sisyphus@G-O | GO@G-W; CX@G-W | sisyphus-junior · unspecified-high | QC@G-R | Allowlist |
| A11 | P5 / Orca | Orca + OC:sisyphus@G-O | CX@G-W Browser Use; GO@G-W2 | multimodal-looker@G-Wv→atlas · visual-engineering | QC@G-R + Playwright Test (Gemini for vision) | Bundled browser |
| A12 | P5 / Orca | Orca + OC:sisyphus@G-O | CX@G-W Computer Use; QC@G-Wq | librarian→multimodal-looker→writing · writing | GO@G-Rx; alt DSH@G-Rx | CX Computer Use plus QC multimodal |

**Media-generation note (not coding models).** No situation needs generated media to pass. If an A02/A12 brief asks for assets, optional generators: GPT Image 2.5 Sunburst ([OpenAI](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst)), Seedance 2.5 ([ByteDance](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5)), Wan 3 ([fal](https://fal.ai/wan-3)) and Kling v3 ([Kling](https://kling.ai/document-api/apiReference/model/videoModels)). No US vendor in `ultimate`; media is never acceptance evidence.

---

## 4. Independence audit

| Check | Cells | Status / fix |
|---|---|---|
| Reviewer shares a harness with a worker | Only hybrid A11, if the GO alternate worker is picked | Fixed: switch to the listed alternate reviewer (PI); the controller enforces it. |
| Reviewer shares a family with a worker (whole chain) | None (disjoint pools). b4b A12: worker QW, reviewer GO@B-R (MI, DS, GG). | Clean |
| Orchestrator shares a harness with workers | P1/P2/P4 rows where OC hosts sisyphus and the worker | Accepted by design; orchestrator family always outside W and never reviews. |
| Orchestrator shares a family with the reviewer | None. GL is used only for O. In b4b, GG appears only in R. | Clean |
| omo-native momus/oracle | All rows | Internal gate only, not counted |
| Repo profiles (F7) | `ultimate` and `hybrid` example momus = hephaestus model | Replace with the R ladders above |
| A06 patch-author family | All profiles | Remove a known author family from R1, R2 and the adjudicator; otherwise record `AUTHOR-UNKNOWN`. |
| CX under custom provider (ultimate A02, A05, A11) | Feature support n.s. | Not an independence issue; use the alternate worker if unsupported |
| `ABSOLUTE-EXCEPTION` | **None required.** `ultimate` has six families and seven harnesses, enough for W, O, R1, R2 and an A06 adjudicator. | If QC and CX Computer Use both fail in `ultimate` A12, the reviewer checks frozen artifacts instead of replaying the desktop; still independent. |

---

## 5. Cross-situation rules

1. **Disjoint families across whole chains.** Partition families into W, O and R and keep every `fallback_models` entry in its pool. An outage then changes the provider, not the family; GLM-5.3 via Z.ai → via Alibaba HK meets the repo's lifeline rule.
2. **P4 is the floor for coding work; omo-native review never suffices.** Reviewer harnesses are chosen for headless evidence: Goose recipes/Analyze, Qwen Code `/review`/JSON, DSH SDK for DeepSeek.
3. **Use Orca only when ≥2 isolated worktrees run at once:** races (A02), parallel reviewers (A05, A06), browser/desktop state (A11, A12). Otherwise the pilot controller owns attempts, cancellation and the ledger. b4b drops races.
4. **The bundled browser decides A11.** CX Browser Use first, Goose Computer Controller second, else Playwright MCP (OSS add-on). Final state is always a frozen Playwright Test.
5. **Bundled multimodal input decides A12 and A07:** only QC bundles image/PDF/audio/video input plus web tools.
6. **Plan terms are routing constraints.** GLM Coding Plan covers only OC, CX, PI and GO here; DSH, QC and AD need metered GLM. Kimi Code returns 401 above plan entitlements ([Kimi Code](https://www.kimi.com/code/docs/en/kimi-code/models)).
7. **Vendor-default pairs (CX↔OA, DSH↔DS, QC↔QW) are tie-breakers only.** The one independent study shows harness choice moves tokens about 40× but pass rate at most 8 points.
8. **Hephaestus only on GPT-family models** (F2); otherwise `atlas` + `deep`/`ultrabrain`.

---

## 6. Risks and unknowns

| Risk | What would change the matrix | Verify first |
|---|---|---|
| omo is SUL-1.0 (F1) | OC+omo becomes a labelled exception everywhere; option: run omo names as a role contract on OSS-native subagents (CX `agents`, QC `.qwen/agents`, DSH Subagents) | 1. Licence at the pinned tag; D05 |
| omo v5 renames and Hephaestus GPT gate (F2) | `ultimate` A01/A03/A05 move to atlas | 2. Load `ultimate.example.json` with a pinned omo |
| CX custom-provider features | ultimate A02/A05/A11 primaries | 3. Synthetic smoke test per provider |
| DSH maturity (preview) | DSH reviewer cells move to GO/PI | 4. Pin DSH; SDK cancel/settle |
| Pi has no permission system | Pi runs in a container, read-only mount | Container profile |
| Aider stagnation | Drop AD alternates | Release cadence |
| ID churn (F5); Gemini Flash price step 2027-01-01 | B-R third rung, MiMo/DeepSeek IDs | 5. Validate IDs against vendor catalogues |
| Codex in `ultimate` | Custom provider only; OpenAI API is not HK-supported ([OpenAI countries](https://help.openai.com/en/articles/5347006-openai-api-supported-countries-and-territories)) | Config audit |
| Unmeasured affinities | All QC↔QW, DSH↔DS, GO token claims | Measure harness–model pairs as the unit ([scaffold study](https://arxiv.org/html/2607.22585v1)) |
| Warp/Superset licensing | Remain labelled exceptions | Warp local path licence |
| Orca examples show only `codex`/`claude` | Dispatch to OC/QC/GO/DSH unverified | `worker-start --agent` values |

---

## 7. Sources

Local: `mm-orch/research/*`; `open-model-method/profiles/*.example.json`, `docs/EXAMPLE-MAPPING.md`, `docs/ROUTING.md`, `docs/research/evaluation-1/*`.

- https://github.com/code-yeongyu/oh-my-openagent/blob/dev/LICENSE.md
- https://ai-heartland.com/explain/oh-my-openagent/
- https://github.com/code-yeongyu/oh-my-openagent/releases
- https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/guide/installation.md
- https://github.com/code-yeongyu/oh-my-openagent/blob/dev/packages/omo-codex/README.md
- https://newreleases.io/project/github/code-yeongyu/oh-my-openagent/release/v4.10.0
- https://github.com/code-yeongyu/oh-my-openagent/issues/2133
- https://omo.vibetip.help/docs/agents/model-matching
- https://github.com/anomalyco/opencode/blob/dev/LICENSE
- https://opencode.ai/docs/lsp/
- https://opencode.ai/docs/mcp-servers/
- https://opencode.ai/docs/agents/
- https://opencode.ai/docs/sdk/
- https://github.com/openai/codex
- https://www.codex-docs.com/en/docs/config-file/config-reference
- https://www.codex-docs.com/en/docs/models
- https://www.deepseek.com/en/harness/
- https://github.com/deepseek-ai/deepseek-harness/blob/master/python/sdk/README.md
- https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/blob/main/evaluation/dsh-minimal.patch
- https://api-docs.deepseek.com/updates/
- https://www.deepseek.com/en/news/deepseek-v4-1-flash/
- https://github.com/royenheart/dsh-plugin-opencode-omo
- https://pi.dev/
- https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/rpc.md
- https://github.com/QwenLM/qwen-code
- https://qwenlm.github.io/qwen-code-docs/en/users/features/sub-agents/
- https://qwenlm.github.io/qwen-code-docs/en/users/features/headless/
- https://qwenlm.github.io/qwen-code-docs/en/users/features/sandbox/
- https://qwenlm.github.io/qwen-code-docs/en/users/configuration/auth/
- https://www.alibabacloud.com/blog/603421
- https://github.com/Aider-AI/aider/releases
- https://leaderboard.steel.dev/leaderboards/aider/
- https://github.com/block/goose
- https://goose-docs.ai/docs/getting-started/using-extensions
- https://goose-docs.ai/docs/guides/context-engineering/subagents/
- https://goose-docs.ai/docs/tutorials/headless-goose/
- https://goose-docs.ai/docs/getting-started/providers
- https://arxiv.org/html/2607.22585v1
- https://github.com/stablyai/orca
- https://github.com/stablyai/orca/blob/main/skill-guides/orchestration.md
- https://www.vibekanban.com/blog/shutdown
- https://github.com/nimbalyst/nimbalyst
- https://github.com/generalaction/emdash
- https://github.com/superset-sh/superset
- https://www.conductor.build/docs
- https://docs.warp.dev/platform/orchestration/
- https://github.com/warpdotdev/warp/blob/master/FAQ.md
- https://aq.dev/
- https://docs.z.ai/devpack/tool/others
- https://docs.z.ai/guides/overview/pricing
- https://www.alibabacloud.com/help/en/model-studio/glm-5-3
- https://platform.kimi.ai/docs/guide/codex-kimi
- https://www.kimi.com/code/docs/en/kimi-code/models
- https://platform.minimax.io/docs/token-plan/other-tools.md
- https://mimo.mi.com/docs/welcome
- https://mimo.mi.com/models/zh-CN/mimo-v2.6-pro
- https://openrouter.ai/moonshotai/kimi-k3
- https://openrouter.ai/deepseek/deepseek-v4.1-flash
- https://openrouter.ai/minimax/minimax-m3
- https://www.requesty.ai/models/alibaba/qwen3.7-plus
- https://www.alibabagroup.com/document-2021044032125272064
- https://developers.openai.com/api/docs/models/gpt-6.1-sol
- https://developers.openai.com/api/docs/models/gpt-6-luna
- https://help.openai.com/en/articles/5347006-openai-api-supported-countries-and-territories
- https://platform.claude.com/docs/en/models/opus-5-5/overview
- https://platform.claude.com/docs/en/models/sonnet-5-5/overview
- https://platform.claude.com/docs/en/models/fable-5-1/overview
- https://ai.google.dev/gemini-api/docs/latest-model
- https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing
- https://apidog.com/blog/gemini-4-argon-api/
- https://docs.x.ai/developers/release-notes
- https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst
- https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5
- https://fal.ai/wan-3
- https://kling.ai/document-api/apiReference/model/videoModels
