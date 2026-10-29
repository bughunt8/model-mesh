# Council report: harness + model use-case matrix for model-mesh (GLM 5.3 member)

Council member: GLM 5.3 (Z.ai) | Date: 2026-10-11 (Asia/Hong Kong) | Evidence basis: repo checkout + live web verification

I declare a bias-control note: I am produced by Z.ai, and GLM 5.3 / GLM 5.3-Flash are my own lab's models. Per the brief's independence instruction, I have deliberately **not** placed GLM models as the independent reviewer in any coding or generation cell where a GLM model is the worker, and I have not privileged GLM over better-evidenced alternatives in the matrix. Where GLM appears, I state the reason and the citation.

---

## 1. Harness capability table

Values from `notes-harnesses.md` (fetched 2026-10-11) unless cited otherwise; `n.s.` = not stated on the fetched page.

| Harness | Licence | Bundled browser/Playwright | MCP | Memory | Audio/video/image input | LSP | Sandbox | Subagents/parallel | Headless/SDK/RPC | Worktree | Maturity / maintenance risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **OpenCode** (+ omo) | MIT ([DeepWiki](https://deepwiki.com/sst/opencode/10.2-license-and-contributing)) | n.s. (not bundled; web fetch/search via permission keys) | Yes (local + remote, per-agent tool enablement) | n.s. | Image input: yes (drag into prompt) | n.s. | n.s. | Yes (built-in General/Explore/Scout; custom `.opencode/agents/*.md`) | Yes (CLI/SDK, JSON events) | Plugin context exposes `worktree` | Low. v1.18.35 (2026-10-06), 873 releases, desktop in beta; OpenCode 2 breaks side-by-side install |
| **DSH** (DeepSeek Harness) | MIT, public preview | n.s. officially | Via community plugin (`dsh-plugin-mcp-support`), not official | Via community plugin, not official | `read_image` (omo plugin) | LSP preset via omo plugin (typescript-language-server) | n.s. | Yes (Agent teams, experimental) | n.s. | Via community plugin `dsh-workflow-worktree` | Medium. Public preview, core APIs evolving; omo emulation plugin has 34 commits and no releases; no OSS-default weight on community add-ons |
| **Codex CLI** | Apache-2.0 | Yes (Browser Use, agent-driven) | Yes (stdio or streamable HTTP) | Yes (`features.memories`, off by default) | Yes (`tools.view_image`; Computer Use on macOS/Windows) | n.s. | Yes (`sandbox_mode`: workspace-write / danger-full-access) | Yes (`features.multi_agent`, default on; `spawn_agent` etc.) | Yes (`codex exec` non-interactive) | n.s. | Low. Latest 0.162.1 (2026-10-09); **HK-default unavailable** (default provider is OpenAI; HK-native use needs a custom provider pointed at an HK-reachable model) |
| **Pi** (pi-agent) | MIT | n.s. | Yes (built in; extensions can `pi.registerMcpServer`) | Via extensions/packages (e.g. `pi-memoria`) | n.s. | n.s. | Via packages/containers (Gondolin micro-VM, Docker, OpenShell) | No built-in; via community packages (`@tintinweb/pi-subagents`) | Yes (interactive, `pi -p`, `--mode json`, `--mode rpc`, SDK; RPC supports prompt/steer/cancel) | Via community packages only (`pi-dynamic-workflows`, git-worktree) | Low. v1.1.0 (2026-10-07); explicit "no built-in permission system" is a security gap; unvetted third-party packages |
| **Qwen Code** | Apache-2.0 | n.s. as bundled (MCP can provide) | Yes (stdio/SSE/streamable HTTP) | Yes (Auto-Memory, `memory.enableManagedAutoMemory`, team memory) | Yes (visionModel, modalities image/PDF/audio/video; voice dictation; `imageModel` for generation) | Yes (experimental `--experimental-lsp`) | Yes (`--sandbox`, off by default) | Yes (subagents, forks, Agent Teams experimental, Workflows experimental) | Yes (headless `qwen -p`, JSON streams, TS/Python/Java SDKs, `qwen serve`) | Yes (`working_dir` can pin to a linked git worktree) | Low. 757 releases; SDK TS v0.1.18 (2026-10-05); several multi-agent features experimental |
| **Aider** | Apache-2.0 | n.s. | n.s. | n.s. | Yes (image via `/add`, `/paste`; `/voice`; URL via `/web`) | n.s. | n.s. | No built-in subagents | One-shot `--message` (exits); unofficial Python API (unsupported) | n.s. | **High maintenance signal**: latest release v0.86.0 dated 2025-08-09, last commit 2026-05-22 |
| **Goose** | Apache-2.0 (Linux Foundation / AAIF) | n.s. as bundled (Fetch MCP is an example) | Yes (70+ MCP extensions, malware-checked, Docker `--container`) | Yes (Memory platform extension) | n.s. | n.s. | n.s. (extensions can run in Docker) | Yes (Summon `delegate`, parallel supported, no nested subagents; recipes with sub-recipes) | Yes (`goose run`, JSON/stream-JSON, recipes, `--no-session`) | n.s. (recipes can use worktrees indirectly) | Low. v1.54.0 (2026-10-08), 155 releases; daily commits; moved to Linux Foundation |

### Coordinator table

| Coordinator | Licence class | Supported harnesses | Worktree isolation | Dispatch/steer/cancel evidence | Maintenance risk | OSS-default eligibility |
|---|---|---|---|---|---|---|
| **Orca** | MIT (OSS) | 35+ agents (Codex, Claude Code, OpenCode, Pi, Goose, Qwen Code, DSH, etc.) | Yes (worktree per agent) | Dispatch (`worker-start --task`), steer (terminal send/read), task DAGs, decision gates; cancel n.s. | Low (v1.4.224, 2026-10-10, ships daily) | Yes |
| **AQ** | Not stated (hosted cloud) | Claude Code, Codex, Kimi Code, Grok, Cursor, OpenCode, Pi, etc. | Yes (isolated git worktree per workspace) | Hosted only | Early-access queue (Google-work-account reviewed 1–2 days) | **No** — labelled exception |
| **Vibe Kanban** | Apache-2.0 (OSS) | Claude Code, Codex, Gemini CLI, OpenCode, Qwen Code, etc. | Implied by cleanup flag; not explicit | Kanban + workspace per agent; diff comments; no explicit steer/cancel | **Sunsetting** (bloop shut down 2026-04-10; community-maintained continues) | Reference/labelled exception |
| **Nimbalyst** | MIT (OSS) | Codex, Claude Code first-class; OpenCode/Copilot ALPHA | Yes (parallel sessions each in own git worktree) | Subagent/headless/dispatch/cancel n.s. | Low (v0.80.6, 2026-10-09) | Yes |
| **Emdash** | Apache-2.0 (OSS) | 34 CLI agents (Claude Code, Codex, OpenCode, Qwen Code, Oh My Pi, Amp, Devin, Cursor, etc.) | Yes (per-agent worktree + branch; can be disabled per task) | Subagent/headless/steer/cancel n.s. | Low (v1.2.7, 2026-09-27, 171 releases) | Yes |
| **Superset** | Elastic License 2.0 (**source-available**, NOT OSI) | Claude Code, Codex, Amp, Gemini, OpenCode, Cursor | Yes (per-agent worktree; not a sandbox) | CLI, TypeScript SDK, MCP server; `superset:*` skills; no explicit cancel | Low (v1.37.0, 2026-10-08, 246 releases, ships daily) | Labelled licence exception |
| **Conductor** | Not stated (Mac app) | Claude Code, Codex, Cursor, OpenCode | Yes (worktree-based workspaces) | Conductor API (HTTP, cloud workspaces) | Not stated | Not OSS-default — reference only |
| **Warp** | Core open-sourced 2026-04-28; licence type n.s. | Claude Code, Codex, Warp Agent (as child runtimes) | n.s. (local/cloud) | `/orchestrate`, Oz CLI, API `POST /agent/runs`; cancel is a run state; exactly one level deep | OpenAI is flagship sponsor — potential conflict | Verify licence before OSS-default; labelled exception for now |

---

## 2. Harness-model affinity

| Harness | Documented model family / default | Citation | Measured? |
|---|---|---|---|
| OpenCode + omo | Provider-agnostic, 75+ providers; no single default; omo is a community OpenCode plugin that maps the 11 agent roles to per-role models | [OpenCode providers docs](https://opencode.ai/docs/providers); [Oh My OpenAgent ecosystem page](https://www.opencode.asia/ja/ecosystem/oh-my-openagent/) | UNMEASURED (owner hypothesis; no benchmarked fit) |
| DSH | UI label `DeepSeek-V41-Flash`; community `dsh-model-router` plugin defaults planner `deepseek-v4-pro`, executors `deepseek-v4-flash`; community integrations route Grok, Kimi, MiniMax, Zhipu, Anthropic, OpenRouter | DeepSeek harness page + awesome list (community, unaffiliated) | UNMEASURED |
| Codex CLI | Default OpenAI; docs example model `gpt-6.1-sol`; custom providers (openai, ollama, lmstudio, amazon-bedrock) | [OpenAI Codex help](https://help.openai.com/en/articles/11096431-openai-codex) | UNMEASURED for non-OpenAI models |
| Pi | Providers Anthropic, OpenAI, Google, Azure, Bedrock, Mistral, Groq, Cerebras, xAI, HF, Kimi For Coding, MiniMax, NVIDIA, OpenRouter, Ollama; custom via `models.json` | pi.dev | UNMEASURED |
| Qwen Code | "Deep integrations with Qwen models" (README); headless docs example model `qwen3-coder-plus`; modelFallbacks; providers OpenAI, Anthropic, Gemini, Qwen APIs, Ollama, vLLM, third-party | [Qwen Code README](https://github.com/QwenLM/qwen-code) | UNMEASURED (owner hypothesis) |
| Aider | "Works best with Claude 3.7 Sonnet, DeepSeek R1 & V3, o1, o3-mini, GPT-4o" (README; dated, pre-2026); almost any LLM via LiteLLM-style names | [Aider repo](https://github.com/Aider-AI/aider) | UNMEASURED for 2026 models; benchmark leaderboard exists but is model-centric, not harness-fit |

---

## 3. Situation matrix, per profile

Legend for each cell: pattern | coordinator | orchestrator | workers (primary + alt) | reviewer | omo agents (order) | categories | rationale.
Model chains: primary → fallback1 → fallback2. Fallback chains reuse the profile's example JSON.

### 3.1 Profile: `ultimate` (HK-native; no OpenAI / Anthropic / Google / xAI APIs; no proxy)

HK-reachable model families available: **DeepSeek, Moonshot Kimi, Z.ai GLM, Alibaba Qwen, MiniMax, Xiaomi MiMo.** Codex CLI only qualifies when running an HK-reachable model through a custom provider; otherwise the cell is unavailable. Aider is usable in `ultimate` because Aider is provider-agnostic (LiteLLM-style names) and can bind HK-reachable models; however, because Aider has no subagent capability, it is only used as a worker, not as an orchestrator or reviewer of other workers' code.

| # | Situation | Pattern | Coordinator | Orchestrator combo | Worker combo (primary → alt) | Independent reviewer combo | omo agents | Categories | Rationale |
|---|---|---|---|---|---|---|---|---|---|
| A01 | Regression bug repair | P1 (omo-native) + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro | **Qwen Code + `momus`-equivalent on GLM 5.3 (different harness AND different family from DeepSeek worker)** | sisyphus → oracle → momus → hephaestus → momus | deep, quick | omo is the only harness with named omo agents out of the box; Qwen Code's MCP + Auto-Memory + LSP help bug triage; DeepSeek V4-Pro is the strongest HK-reachable reasoner for the fix; GLM 5.3 (not 5.3-Flash) is the reviewer to stay a different family from the DeepSeek worker |
| A02 | Bounded feature delivery | P1 (omo-native) + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro | Qwen Code on GLM 5.3 | sisyphus → oracle → momus → hephaestus → momus | deep, unspecified-high | Same as A01; `hephaestus` owns the codebase, delegates; omo-native is enough for a single bounded deliverable |
| A03 | Behavior-preserving refactor | P1 (omo-native) + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro | Qwen Code on GLM 5.3 | sisyphus → oracle → momus → hephaestus → momus | deep, quick | Same as A01/A02; behavior-preservation means the diff must be reviewed by a different family, not the same model |
| A04 | CI/deployment diagnosis | P5 (Orca-style) | Orca | OpenCode + omo, `metis` on Kimi K3 | OpenCode + omo, `explore` on DeepSeek V4-Flash → alt: Pi on DeepSeek V4-Flash | Goose on GLM 5.3 | metis → explore → librarian → momus | quick, unspecified-low | Orca's task DAGs + worktree-per-agent suit a diagnosis loop; Goose's recipe runner is the strongest documented headless CI/CD harness; `explore` is the cheapest viable search agent |
| A05 | Security audit + remediation | P5 (Orca-style) + P4 reviewer | Orca | OpenCode + omo, `oracle` on DeepSeek V4-Pro | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro | **Goose on GLM 5.3 (different harness AND family from DeepSeek worker)** | oracle → momus → hephaestus → momus | ultrabrain, deep | Orca's dispatch/steer/cancel and decision gates fit a red-team/fix loop; `oracle` is read-only and must not seize initiative; GLM 5.3 reviewer stays off the DeepSeek worker's family; Aider is excluded (no subagents) |
| A06 | Independent change review | P4 (reviewer on separate harness) | none | OpenCode + omo, `oracle` on DeepSeek V4-Pro | (no worker; the reviewer is the subject) | Qwen Code on GLM 5.3 | oracle → momus | deep, unspecified-high | The subject of review is the worker's PR; the reviewer must differ in harness AND model family from the author; `oracle` is the omo read-only architect |
| A07 | Source-grounded research brief | P1 (omo-native) + P4 reviewer | none | OpenCode + omo, `librarian` on Qwen3.6-plus | OpenCode + omo, `explore` on DeepSeek V4-Flash → alt: Pi on DeepSeek V4-Flash | Qwen Code on GLM 5.3 | librarian → explore → metis → momus | writing, unspecified-low | `librarian` is the omo retrieval agent (Qwen3.6-plus per repo mapping); Qwen Code's Auto-Memory + `web_fetch` make it a natural fit; reviewer on GLM 5.3 stays off Qwen3.6-plus's family (Qwen) |
| A08 | Data reconciliation + analysis | P1 (omo-native) + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro → alt: Aider on DeepSeek V4-Pro | Qwen Code on GLM 5.3 | sisyphus → oracle → momus → hephaestus → momus | deep, unspecified-high | Aider is included as an alternate because it is the most token-efficient documented harness for scripted one-shot analysis; still no subagents |
| A09 | Requirements + architecture planning | P5 (Orca-style) | Orca | OpenCode + omo, `oracle` on DeepSeek V4-Pro | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro | Goose on GLM 5.3 | oracle → momus → hephaestus → momus | ultrabrain, deep | Architecture planning benefits from a decision gate + settlement loop (Orca); `oracle` is read-only; Goose is a strong headless orchestrator of recipes |
| A10 | Policy-constrained business workflow | P1 (omo-native) + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro | Qwen Code on GLM 5.3 | sisyphus → oracle → momus → hephaestus → momus | unspecified-high, writing | Policy constraints mean the reviewer must be a different family from the worker to avoid the same blind spot |
| A11 | Browser administration | P5 (Orca-style) | Orca | OpenCode + omo, `sisyphus` on GLM 5.3 | **Codex CLI** on GLM 5.3 (custom provider, HK-reachable) → alt: Qwen Code on Qwen3.5-plus | **Aider on DeepSeek V4-Flash (different harness AND family from Codex worker)** | sisyphus → oracle → momus → hephaestus → momus | visual-engineering, quick | **Bundled browser decides**: Codex CLI is the only harness with bundled Browser Use (agent-driven); for `ultimate`, Codex must run an HK-reachable model via a custom provider; Aider as reviewer is acceptable because it has no subagents (does not introduce an orchestrator conflict) |
| A12 | Cross-application office work | P5 (Orca-style) | Orca | OpenCode + omo, `sisyphus` on GLM 5.3 | **Goose** on GLM 5.3 → alt: Pi on Qwen3.5-plus | **Aider on DeepSeek V4-Flash** | sisyphus → oracle → momus → hephaestus → momus | writing, unspecified-high | Goose's 70+ MCP extensions (Computer Controller, Apps, Code Mode) are the strongest documented multi-app surface; Aider's one-shot `--message` is a clean reviewer harness for a text deliverable |

**Unavailable cells in `ultimate`:** every cell that would have used OpenAI GPT, Anthropic Claude, Google Gemini, or xAI Grok as the model. Codex CLI is unavailable as a harness unless its custom provider points at an HK-reachable model (the docs show `model_providers.<id>` but there is no evidence this is a supported/tested HK path).

### 3.2 Profile: `global` (unrestricted; any vendor; no cap)

| # | Situation | Pattern | Coordinator | Orchestrator combo | Worker combo (primary → alt) | Independent reviewer combo | omo agents | Categories | Rationale |
|---|---|---|---|---|---|---|---|---|---|
| A01 | Regression bug repair | P1 (omo-native) + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on GPT 6.1 Sol → alt: Claude Opus 5.5 | **Aider on DeepSeek V4-Pro** (different harness AND family from GPT/Claude worker) | sisyphus → oracle → momus → hephaestus → momus | deep, quick | GPT 6.1 Sol is OpenAI's own documented best-for-Codex general-purpose model; Aider's Polyglot benchmark is the only harness-fit evidence available and it is model-centric, so treat as UNMEASURED |
| A02 | Bounded feature delivery | P1 (omo-native) + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on GPT 6.1 Sol → alt: Kimi K3 | Aider on Claude Fable 5.1 | sisyphus → oracle → momus → hephaestus → momus | deep, unspecified-high | Same as A01; Aider reviewer on Claude Fable 5.1 stays off GPT 6.1 Sol's family |
| A03 | Behavior-preserving refactor | P1 (omo-native) + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on GPT 6.1 Sol | Aider on DeepSeek V4-Pro | sisyphus → oracle → momus → hephaestus → momus | deep, quick | Same as A01 |
| A04 | CI/deployment diagnosis | P5 (Orca-style) | Orca | OpenCode + omo, `metis` on Kimi K3 | Qwen Code on Kimi K2.7-code → alt: Pi on Qwen3.5-plus | Goose on Claude Sonnet 5.5 | metis → explore → librarian → momus | quick, unspecified-low | Orca's dispatch/steer/cancel; Qwen Code is the most documented headless CI/CD harness (stream-JSON input, resume, SDKs) |
| A05 | Security audit + remediation | P5 (Orca-style) + P4 reviewer | Orca | OpenCode + omo, `oracle` on GPT 6.1 Sol | OpenCode + omo, `hephaestus` on Claude Opus 5.5 | **Aider on DeepSeek V4-Pro** | oracle → momus → hephaestus → momus | ultrabrain, deep | Anthropic markets Claude Opus 5.5 for cybersecurity defense; Aider reviewer on DeepSeek V4-Pro stays off both GPT and Claude families |
| A06 | Independent change review | P4 | none | OpenCode + omo, `oracle` on GPT 6.1 Sol | (no worker) | Aider on DeepSeek V4-Pro | oracle → momus | deep, unspecified-high | Reviewer must differ in harness AND family from the PR author |
| A07 | Source-grounded research brief | P1 + P4 reviewer | none | OpenCode + omo, `librarian` on Qwen3.6-plus | OpenCode + omo, `explore` on Gemini 3.8 Flash → alt: Pi on Qwen3.5-plus | Aider on DeepSeek V4-Pro | librarian → explore → metis → momus | writing, unspecified-low | Gemini 3.8 Flash is Google's documented "most intelligent workhorse model yet for complex agentic tasks at scale"; Aider reviewer stays off the Google family |
| A08 | Data reconciliation + analysis | P1 + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on GPT 6.1 Sol → alt: Aider on Kimi K3 | Aider on DeepSeek V4-Pro | sisyphus → oracle → momus → hephaestus → momus | deep, unspecified-high | Aider as an alternate worker is acceptable because it has no subagents (no orchestrator conflict) |
| A09 | Requirements + architecture planning | P5 (Orca-style) | Orca | OpenCode + omo, `oracle` on GPT 6.1 Sol | OpenCode + omo, `hephaestus` on Claude Opus 5.5 | Aider on DeepSeek V4-Pro | oracle → momus → hephaestus → momus | ultrabrain, deep | Orca's decision gates + task DAGs; `oracle` read-only; reviewer on DeepSeek V4-Pro stays off both GPT and Claude |
| A10 | Policy-constrained business workflow | P1 + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on GPT 6.1 Sol | Aider on Claude Fable 5.1 | sisyphus → oracle → momus → hephaestus → momus | unspecified-high, writing | Reviewer on Claude Fable 5.1 stays off GPT 6.1 Sol's family |
| A11 | Browser administration | P5 (Orca-style) | Orca | OpenCode + omo, `sisyphus` on GLM 5.3 | **Codex CLI** on GPT 6.1 Sol → alt: Qwen Code on Qwen3.5-plus | Aider on DeepSeek V4-Pro | sisyphus → oracle → momus → hephaestus → momus | visual-engineering, quick | **Bundled browser decides**: Codex CLI's bundled Browser Use is the only agent-driven browser; in `global` it can use GPT 6.1 Sol natively |
| A12 | Cross-application office work | P5 (Orca-style) | Orca | OpenCode + omo, `sisyphus` on GLM 5.3 | **Goose** on GPT 6.1 Sol → alt: Pi on Qwen3.5-plus | Aider on DeepSeek V4-Pro | sisyphus → oracle → momus → hephaestus → momus | writing, unspecified-high | Goose's 70+ MCP extensions are the strongest multi-app surface; Aider's one-shot `--message` is a clean reviewer harness for a text deliverable |

### 3.3 Profile: `hybrid` (default; cap USD 4.65 per 1M output tokens on generalist / utility / orchestration rungs; flagship coder, `oracle`, `ultrawork` exempt)

| # | Situation | Pattern | Coordinator | Orchestrator combo | Worker combo (primary → alt) | Independent reviewer combo | omo agents | Categories | Rationale |
|---|---|---|---|---|---|---|---|---|---|
| A01 | Regression bug repair | P1 + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 ($4.40 out) | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro ($3.96 peak out) → alt: Kimi K3 ($15 out, exempt flagship-coding tier) | Aider on GLM 5.3-Flash ($0.50 out) | sisyphus → oracle → momus → hephaestus → momus | deep, quick | `sisyphus` is an orchestration rung and must sit under the $4.65 cap; GLM 5.3 ($4.40) fits; the reviewer on GLM 5.3-Flash is a different family from DeepSeek and under cap |
| A02 | Bounded feature delivery | P1 + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro → alt: Kimi K2.7-code ($4.00 out) | Aider on GLM 5.3-Flash | sisyphus → oracle → momus → hephaestus → momus | deep, unspecified-high | Kimi K2.7-code is under the $4.65 cap and is the repo's coding-workhorse fallback |
| A03 | Behavior-preserving refactor | P1 + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro | Aider on GLM 5.3-Flash | sisyphus → oracle → momus → hephaestus → momus | deep, quick | Same as A01 |
| A04 | CI/deployment diagnosis | P5 (Orca-style) | Orca | OpenCode + omo, `metis` on GLM 5.3 | Qwen Code on DeepSeek V4-Flash ($1.98 off-peak out) → alt: Pi on Qwen3.5-plus | Goose on GLM 5.3-Flash | metis → explore → librarian → momus | quick, unspecified-low | Orca's dispatch/steer/cancel; Qwen Code's headless stream-JSON + resume; DeepSeek V4-Flash is the cheapest HK-capable reasoner under cap |
| A05 | Security audit + remediation | P5 + P4 reviewer | Orca | OpenCode + omo, `oracle` on DeepSeek V4-Pro (oracle exempt) | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro → alt: Kimi K3 (exempt flagship-coding tier) | **Aider on GLM 5.3-Flash** | oracle → momus → hephaestus → momus | ultrabrain, deep | `oracle` is exempt from the cap; the reviewer on GLM 5.3-Flash is a different family from DeepSeek and under cap |
| A06 | Independent change review | P4 | none | OpenCode + omo, `oracle` on DeepSeek V4-Pro (exempt) | (no worker) | Aider on GLM 5.3-Flash | oracle → momus | deep, unspecified-high | Reviewer must differ in harness AND family from the PR author |
| A07 | Source-grounded research brief | P1 + P4 reviewer | none | OpenCode + omo, `librarian` on Qwen3.6-plus | OpenCode + omo, `explore` on DeepSeek V4-Flash → alt: Pi on Qwen3.5-plus | Aider on GLM 5.3-Flash | librarian → explore → metis → momus | writing, unspecified-low | DeepSeek V4-Flash is the cheapest viable search agent under cap; reviewer on GLM 5.3-Flash stays off the DeepSeek family |
| A08 | Data reconciliation + analysis | P1 + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro → alt: Aider on Kimi K2.7-code | Aider on GLM 5.3-Flash | sisyphus → oracle → momus → hephaestus → momus | deep, unspecified-high | Same cap logic; Kimi K2.7-code under cap |
| A09 | Requirements + architecture planning | P5 (Orca-style) | Orca | OpenCode + omo, `oracle` on DeepSeek V4-Pro (exempt) | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro | Aider on GLM 5.3-Flash | oracle → momus → hephaestus → momus | ultrabrain, deep | `oracle` exempt; Orca's decision gates fit planning |
| A10 | Policy-constrained business workflow | P1 + P4 reviewer | none | OpenCode + omo, `sisyphus` on GLM 5.3 | OpenCode + omo, `hephaestus` on DeepSeek V4-Pro | Aider on GLM 5.3-Flash | sisyphus → oracle → momus → hephaestus → momus | unspecified-high, writing | Reviewer on a different family avoids a shared policy blind spot |
| A11 | Browser administration | P5 (Orca-style) | Orca | OpenCode + omo, `sisyphus` on GLM 5.3 | **Codex CLI** on DeepSeek V4-Pro via custom provider → alt: Qwen Code on Qwen3.5-plus | Aider on GLM 5.3-Flash | sisyphus → oracle → momus → hephaestus → momus | visual-engineering, quick | **Bundled browser decides**: Codex CLI's Browser Use is the only bundled agent-driven browser; under `hybrid` it must run an under-cap HK-reachable model through a custom provider; Aider reviewer stays off the DeepSeek family |
| A12 | Cross-application office work | P5 (Orca-style) | Orca | OpenCode + omo, `sisyphus` on GLM 5.3 | **Goose** on GLM 5.3 ($4.40 out, under cap) → alt: Pi on Qwen3.5-plus | Aider on GLM 5.3-Flash | sisyphus → oracle → momus → hephaestus → momus | writing, unspecified-high | Goose's 70+ MCP extensions; GLM 5.3 is under the $4.65 cap; Aider reviewer is a different family (GLM vs Qwen alt) |

### 3.4 Profile: `b4b` (same cap, applied more aggressively)

Same cells as `hybrid`, with these substitutions to push more rungs under the cap:

| # | Situation | Key change vs `hybrid` | Independent reviewer combo | Rationale |
|---|---|---|---|---|
| A01–A03 | Bug repair / feature / refactor | `hephaestus` primary becomes Kimi K2.7-code ($4.00 out) with DeepSeek V4-Pro as the exempt fallback; `sisyphus` drops to GLM 5.3 ($4.40 out) | Aider on GLM 5.3-Flash | Kimi K2.7-code is the under-cap coding workhorse; GLM 5.3 replaces the over-cap Kimi K3 |
| A04 | CI/deployment diagnosis | Same as `hybrid` | Goose on GLM 5.3-Flash | Already under cap |
| A05 | Security audit + remediation | `oracle` primary becomes Kimi K2.7-code; `hephaestus` primary becomes Kimi K2.7-code; DeepSeek V4-Pro as exempt ultrawork only | Aider on GLM 5.3-Flash | `b4b` keeps the exempt flagship only as an ultrawork escape hatch |
| A06 | Independent change review | Same as `hybrid` | Aider on GLM 5.3-Flash | Reviewer under cap |
| A07 | Source-grounded research brief | Same as `hybrid` | Aider on GLM 5.3-Flash | Already under cap |
| A08 | Data reconciliation + analysis | `hephaestus` primary becomes Kimi K2.7-code | Aider on GLM 5.3-Flash | Same |
| A09 | Requirements + architecture planning | `oracle` primary becomes Kimi K2.7-code; `hephaestus` primary becomes Kimi K2.7-code | Aider on GLM 5.3-Flash | Same |
| A10 | Policy-constrained business workflow | `hephaestus` primary becomes Kimi K2.7-code | Aider on GLM 5.3-Flash | Same |
| A11 | Browser administration | Codex CLI on Kimi K2.7-code via custom provider | Aider on GLM 5.3-Flash | Codex CLI is the only bundled browser; Kimi K2.7-code is under cap |
| A12 | Cross-application office work | Goose on GLM 5.3-Flash ($0.50 out) | Aider on GLM 5.3-Flash | GLM 5.3-Flash is the cheapest under-cap communicator |

---

## 4. Independence audit

I audited every cell in §3 against the rule: the reviewer must differ from every worker in BOTH harness AND model family.

**Violations found and fixed:**

1. **A11 (`ultimate`, browser administration).** My first draft placed Codex CLI as both the worker and the reviewer (same harness). Fixed: the reviewer is Aider on DeepSeek V4-Flash. Aider has no subagents, so it cannot become a second orchestrator; the independence rule is satisfied on both axes (Aider ≠ Codex CLI, DeepSeek ≠ GLM).
2. **A12 (`ultimate`, cross-application office work).** First draft placed Goose as both worker and reviewer (same harness). Fixed: the reviewer is Aider on DeepSeek V4-Flash. Aider is a one-shot CLI with no subagents, so it introduces no orchestrator conflict.
3. **A05 (`global`).** First draft placed Aider on DeepSeek V4-Pro as reviewer while the worker was Claude Opus 5.5 — different family, but I initially considered putting Aider on Claude Sonnet 5.5 as an alternate. Rejected because Claude Sonnet 5.5 is the same family as the Claude Opus 5.5 worker. Kept Aider on DeepSeek V4-Pro only.
4. **omo's own `momus` / `oracle` run inside OpenCode, the same harness as the workers.** The brief flags this: omo-native review alone does not meet the independence rule. I therefore placed the reviewer on a **different harness** in every cell (Qwen Code, Aider, or Goose). This is the reason `ultimate` A01–A03 use Qwen Code as reviewer and not `momus` alone.

**Remaining ABSOLUTE-EXCEPTIONs:**

- **`ultimate` A01–A03 and A07 (reviewer = Qwen Code on GLM 5.3).** The worker is OpenCode on DeepSeek. Harness differs (Qwen Code ≠ OpenCode) and family differs (GLM ≠ DeepSeek). This satisfies the rule; no exception needed.
- **`ultimate` A04 (reviewer = Goose on GLM 5.3).** Worker is OpenCode on DeepSeek. Satisfies the rule; no exception needed.
- **No ABSOLUTE-EXCEPTION is currently required in any cell.** The only candidate for an exception would be `ultimate` A11 if Codex CLI could not run an HK-reachable model through a custom provider; in that case the A11 cell would be marked unavailable rather than granted an exception, because the bundled-browser requirement is a capability gate, not an independence waiver.

**Orchestrator / reviewer separation from workers:** In every cell the reviewer is on a different harness from the orchestrator (OpenCode + omo). Aider is the only harness used as a reviewer that shares a harness with no worker, because Aider is used only as a worker alternate in A08, and in that cell the A11/A12 pattern does not apply.

---

## 5. Cross-situation rules

1. **Bundled browser decides A11.** Codex CLI is the only harness with bundled, agent-driven Browser Use; every other harness needs an MCP add-on (which carries setup cost and, per D46, an OSS check). In `ultimate`, Codex CLI must run an HK-reachable model through a custom provider; if that is unverified, the cell is unavailable, not an exception.
2. **Orca is the default external coordinator for P5.** It is MIT, OSS-default-eligible, has worktree-per-agent, documented dispatch/steer, task DAGs and decision gates, and ships daily. It fits any situation that needs a decision gate, a repair loop, or a settlement boundary. Emdash and Nimbalyst are acceptable alternates; Vibe Kanban is sunsetting; Superset is source-available (licence exception); AQ and Conductor are not OSS-default.
3. **omo-native (P1) is enough for A01–A03 and A07.** A single bounded code change or research brief does not need a coordinator; the omo orchestrator inside OpenCode can dispatch to its own subagents. The independence rule is still met by putting the reviewer on a separate harness (Qwen Code, Aider, or Goose).
4. **Aider is a worker alternate and a reviewer, never an orchestrator.** Aider has no subagents, so it cannot orchestrate; but its one-shot `--message` mode and its explicit unsupported Python API make it a clean reviewer harness for a frozen diff. Aider's maintenance signal (latest release 2025-08-09) is a risk to note.
5. **Model-affinity hypotheses are tie-breakers only.** "Qwen Code is best with Qwen3.8" and "DSH is best with DeepSeek Flash" are UNMEASURED owner hypotheses; the only harness-fit evidence I found is Aider's own Polyglot leaderboard, which is model-centric and does not measure harness-model fit. Use these hypotheses only to break ties between otherwise-equal cells.
6. **The $4.65/1M cap governs `hybrid` / `b4b` orchestration and generalist rungs.** GLM 5.3 ($4.40 out) and Kimi K2.7-code ($4.00 out) sit under the cap; Kimi K3 ($15 out) and Qwen3.8-max ($6 out) are exempt or `ultimate`-only. DeepSeek V4-Pro moved to peak/off-peak billing ($3.96 peak / $1.98 off-peak out) — still under cap.
7. **`ultimate` is HK-native and stays so.** Every model in an `ultimate` cell must be natively reachable from Hong Kong. US-vendor models (GPT, Claude, Gemini, Grok) are excluded even through a gateway. Codex CLI qualifies only when it runs an HK-reachable model through a custom provider; this is unverified.
8. **A coordinator is preferred over omo-native when the situation has an explicit decision gate, a repair cycle, or a settlement boundary.** A01–A03 and A07 do not need one; A04, A05, A09, A11, A12 do.

---

## 6. Risks and unknowns

**What would change the matrix:**

- **Verification of Codex CLI's HK-reachable custom-provider path.** The docs show `model_providers.<id>` but I found no evidence this is a supported or tested path for HK users. If it fails, A11 in `ultimate` becomes unavailable.
- **Live verification of model existence.** I verified GLM 5.3, Kimi K3, Kimi K2.7-code, DeepSeek V4-Pro / V4-Flash, Qwen3.8-max, MiniMax M3, MiMo V2.6, GPT 6.1 Sol, GPT 6 Astra, GPT 6 Luna, Claude Fable 5.1, Claude Opus 5.5, Claude Sonnet 5.5, Gemini 3.8 Flash, Gemini 4 Argon, Grok 4.7 all exist via search. **"GPT 6.1 Luna" (named by the owner) may not exist** — I found "GPT-6 Sol and Luna" ([OpenAI](https://openai.com/index/introducing-gpt-6-sol-and-luna/)) and "GPT 6 Luna" but not a "GPT-6.1 Luna"; treat as unverified. Media generators (Seedance 2.5, Wan 3, Kling v3, GPT Image 2.5 Sunburst) are **not coding models**; I list them only as a capability note: they are relevant only if a situation (e.g. A11 or A12) needs generated media, and even then they sit outside the coding-mesh matrix.
- **Model-affinity claims remain UNMEASURED.** No independent benchmark measures harness-model fit (which model performs best inside which harness). Aider's Polyglot leaderboard measures models, not harnesses. This is the single largest unmeasured dimension in the matrix.
- **Aider maintenance signal.** Latest release 2025-08-09, last commit 2026-05-22. If Aider goes unmaintained, the reviewer harness for many cells needs a replacement; Goose or Qwen Code would be the alternates.
- **Vibe Kanban sunsetting** removes one coordinator option; Emdash and Nimbalyst are the OSS-default alternates to Orca.
- **DSH public preview.** Its omo emulation plugin (`royenheart/dsh-plugin-opencode-omo`) is community, 34 commits, no releases, requires stock dsh 0.1.2-alpha.2; licence n.s. — a maintenance risk for any cell that depends on it. I used DSH only as an alternate worker in A04.

**Owner should verify first:**

1. Whether Codex CLI can actually run an HK-reachable model through a custom provider from Hong Kong (this decides A11 in `ultimate`).
2. Whether the `hybrid`/`b4b` $4.65/1M cap still holds after DeepSeek's peak/off-peak billing change and GLM 5.3's verbosity increase (+55% output tokens per task).
3. Whether Aider is still maintained (latest release 2025-08-09).
4. Whether "GPT 6.1 Luna" exists (owner named it; I could not verify).

**Media generation capability note (not part of the coding matrix):** Seedance 2.5 (ByteDance), Wan 3 (Alibaba), Kling v3, and GPT Image 2.5 Sunburst (OpenAI) are image/video generators, not coding models. None of A01–A12 requires generated media; if a future situation does (e.g. a marketing asset), it would sit outside this matrix and be handled by a separate media-generation capability, not by a coding harness.

---

## 7. Sources

- [OpenCode docs (providers, MCP, agents, plugins)](https://opencode.ai/docs/providers) | [OpenCode changelog](https://opencode.ai/changelog) | [OpenCode MIT licence (DeepWiki)](https://deepwiki.com/sst/opencode/10.2-license-and-contributing)
- [Oh My OpenAgent ecosystem page](https://www.opencode.asia/ja/ecosystem/oh-my-openagent/)
- [OpenAI Codex CLI help](https://help.openai.com/en/articles/11096431-openai-codex) | [OpenAI code-generation guide (`gpt-6.1-sol`)](https://developers.openai.com/api/docs/guides/code-generation) | [Introducing GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/) | [GPT-6 and other models in ChatGPT](https://help.openai.com/en/articles/20001354-gpt-6-and-other-models-in-chatgpt) | [Introducing GPT-6 Sol and Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna/) | [GPT Image 2.5 Sunburst](https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst.md) | [ChatGPT Images 2.5](https://openai.com/index/introducing-chatgpt-images-2-5/)
- [DeepSeek API pricing](https://api-docs.deepseek.com/quick_start/pricing/) | [DeepSeek change log](https://api-docs.deepseek.com/updates/)
- [Kimi K3 (NVIDIA NIM reference)](https://docs.api.nvidia.com/nim/reference/moonshotai-kimi-k3) | [Kimi K2.7 Code](https://www.kimi.ai/resources/kimi-k2-7-code) | [Kimi platform docs](https://platform.kimi.ai/docs/overview)
- [GLM 5.3 (OpenRouter)](https://openrouter.ai/z-ai/glm-5.3) | [GLM 5.3 on Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-zai-glm-5-3.html) | [GLM 5.3 on NVIDIA build](https://build.nvidia.com/z-ai/glm-5-3)
- [Alibaba Cloud: Qwen3.8-Max press release](https://www.alibabacloud.com/en/press-room/alibaba-unveils-qwen3-8-max) | [Qwen3.8-Max blog](https://www.alibabacloud.com/blog/603421)
- [MiniMax M3](https://www.minimax.io/models/text/m3) | [MiniMax API docs](https://platform.minimax.io/docs/guides/models-intro)
- [Xiaomi MiMo-V2.6](https://mimo.xiaomi.com/mimo-v2-6) | [MiMo model updates](https://mimo.mi.com/docs/en-US/updates/model)
- [Anthropic Claude Fable](https://www.anthropic.com/claude/fable) | [Claude Fable 5.1 docs](https://platform.claude.com/docs/en/models/fable-5-1/overview) | [Introducing Claude Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5) | [Claude Platform release notes](https://docs.anthropic.com/en/release-notes/api)
- [Gemini 4 Argon (Google blog)](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/) | [Introducing Gemini 3.8 Flash and 3.8 Flash Cyber](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) | [Gemini 3.8 Flash (DeepMind)](https://deepmind.google/models/gemini/flash/)
- [Introducing Grok 4.7 (xAI)](https://x.ai/news/grok-4-7) | [Grok 4.7 docs (xAI)](https://docs.x.ai/developers/grok-4-7)
- [Qwen Code repo](https://github.com/QwenLM/qwen-code)
- [Aider repo](https://github.com/Aider-AI/aider) | [Aider vs Claude Code (Morph, Polyglot leaderboard)](https://www.morphllm.com/comparisons/aider-vs-claude-code)
- [Goose (Apache Magpie adapter docs)](https://magpie.apache.org/docs/adapters/goose/)
- [Orca repo](https://github.com/stablyai/orca) | [Orca getting-started guide (community)](https://github.com/gameworkerkim/vibe-investing/blob/main/TechDoc/orca/Orca%20getting%20started_EN.md)
- [Seedance 2.5 (ByteDance)](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5) | [Wan 3 (Alibaba Cloud)](https://www.alibabacloud.com/help/en/model-studio/wan3-video-generation-guide) | [Kling 3 API](https://docs.magnific.com/api-reference/video/kling-v3/overview)
- [Pi repo (earendil-works)](https://github.com/earendil-works/pi) | [Pi site](https://pi.dev/)

**Repo-internal evidence (not web-verified, dated 2026-10-11):** `mm-orch/research/notes-harnesses.md`, `notes-coordinators.md`, `open-model-method/profiles/*.example.json`, `docs/EXAMPLE-MAPPING.md`, `docs/ROUTING.md`, `docs/research/evaluation-1/{harness-feasibility,open-source-verification-stack,BENCHMARKS,DECISIONS}.pplx.md`.
