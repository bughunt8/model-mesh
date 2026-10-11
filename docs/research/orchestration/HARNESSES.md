# Harness evidence and fit

Evidence fetched on 2026-10-11 HKT from the vendor pages and repositories cited in each section. "n.s." means the fetched page did not state the item, which is not proof that the feature is absent. Capabilities count as follows. Bundled in the default install counts in full. An official open-source add-on counts with its setup cost. A community add-on is listed and gets no weight.

## Fit by situation

The matrix in [MATRIX.md](MATRIX.md) uses these strengths as tie-breakers. They are judgements from documentation, not measurements.

| Harness | Documented strength | Situations it favours | Main risk |
|---|---|---|---|
| OpenCode with omo | LSP hooks, subagents, 75+ providers, omo role and fallback routing | A01, A02, A03, A09 as author and orchestrator | omo licence is Sustainable Use License 1.0; role names change after v4.19.4 |
| DSH | Python SDK over JSON-RPC, agent teams (experimental), voice (experimental) | A01, A04 as alternate author | Public preview; MCP, memory and worktrees only from community plugins |
| Codex CLI | Bundled Browser Use, Computer Use on macOS and Windows, `codex exec`, MCP, sandbox modes | A05 alternate; A11 where an OpenAI route is allowed | Custom-provider path for Hong Kong-reachable models has docs but no runtime proof |
| Pi | RPC and print modes with a settle event, small attack surface for read-only critique | A05, A06, A09 and reviewer seats | No built-in permissions or subagents; run in a container |
| Qwen Code | Bundled MCP, memory, image, PDF, audio and video input, headless JSON, SDKs | A07, A08, A11, A12 | Alibaba benchmarked its model in another harness, so the harness and model pairing is unmeasured |
| Aider | Repo map, architect and editor pair, auto lint and test, one-shot `--message` | A03 and A06 as alternate | Last release 2025-08-09; no MCP, subagents or sandbox; never an orchestrator |
| Goose | Built-in Developer, Computer Controller, Memory, Analyze and Skills extensions; recipes; `goose run` | A04, A08, A10 as author; default independent reviewer | Subagents stop at 25 turns and cannot nest |

Owner hypotheses are recorded as hypotheses. Qwen Code with Qwen3.8 and DSH with DeepSeek Flash are plausible, but the only evidence found is vendor assertion for the first and vendor documentation for the second. They break ties between otherwise equal options and carry no more weight.


## Evidence: OpenCode (opencode.ai/docs, github.com/sst/opencode -> anomalyco/opencode)
- Licence: LICENSE file listed, type n.s. on fetched pages (evaluation-1 report observed licence from raw LICENSE; re-verify). Latest v1.18.35 (2026-10-06); OpenCode 2 exists, cannot install side by side with 1 under default `opencode` command.
- Image input: drag image into prompt (docs/). Built-in subagents General (parallel, full tools), Explore, Scout (read-only) (docs/agents). Primary agents build/plan. Custom agents: .opencode/agents/*.md, `opencode agent create`. Task permissions `permission.task`.
- MCP client: local (`type: "local"`, `command`) and remote (`type: "remote"`, `url`, `oauth`, `headers`); per-agent tool enablement via glob; CLI `opencode mcp auth|list|logout|debug`. (docs/mcp-servers)
- Plugins: JS/TS hooks (events incl. lsp diagnostics, `tool.execute.before`, `session.idle`), custom tools, `plugin` array in opencode.json; plugin context exposes `worktree`. (docs/plugins)
- Providers: 75+ via AI SDK + Models.dev, incl. DeepSeek, Moonshot, MiniMax, Z.AI, OpenAI, Anthropic, xAI, Bedrock, Vertex, Ollama, LM Studio; custom OpenAI-compatible. Config `opencode.json(c)`, `~/.config/opencode/`. (docs/providers)
- Browser/Playwright, memory, voice/audio/video: n.s. (not bundled per fetched docs). Web fetch/search + lsp are permission keys (docs/agents).
- Headless/SDK: evaluation-1 report cites CLI/SDK docs (opencode.ai/docs/cli, /sdk). Not re-fetched here.
- Install: curl script, npm i -g opencode-ai, brew, etc. Desktop app BETA.

## Evidence: Codex CLI (github.com/openai/codex; config reference at codex-docs.com mirror)
- Apache-2.0. Latest 0.162.1 (2026-10-09). `codex`, `codex exec`, `codex app`, Codex Web.
- Config TOML `~/.codex/config.toml`, project `.codex/config.toml` (trusted projects only), profiles `$CODEX_HOME/<name>.config.toml` via `--profile`; `model`, `model_provider`, `model_providers.<id>` custom providers (openai, ollama, lmstudio, amazon-bedrock built in). Example model id in docs `gpt-6.1-sol`.
- Bundled: Browser Use (agent-driven browser; `browser_use` requirements), `web_search` modes disabled/cached/indexed/live (default cached), MCP (`mcp_servers.<id>`, stdio or streamable HTTP), memories (off by default, `features.memories`), `tools.view_image`, Computer Use on macOS/Windows, sandbox_mode (workspace-write / danger-full-access), skills/plugins. Voice/LSP n.s.
- Multi-agent: `features.multi_agent` (default on): spawn_agent/send_input/resume_agent/wait_agent/close_agent; `agents.max_concurrent_threads_per_session`; custom roles under `agents`. `codex exec` non-interactive with `approval_policy = "never"`.
- Region note: default provider is OpenAI; HK-native use needs a custom provider pointed at an HK-reachable model (docs show `model_providers.<id>`); no evidence in fetched pages that this is a supported/tested path.

## Evidence: DeepSeek Harness (DSH) (deepseek.com/en/harness, dsharness.io, github.com/deepseek-ai/deepseek-harness)
- MIT; open source; DeepSeek; PUBLIC PREVIEW, core plugins/APIs evolving; Cordis "everything is a plugin". UI label `DeepSeek-V41-Flash` (High). Launch: `npx @deepseek-ai/dsh web` (Node.js).
- Plugins listed: Agent teams (Experimental), Auto approval review (Exp), Scheduled tasks (Exp), Voice input (Exp), Terminal, Agent loop, Subagents. Creator mode. Browser/Playwright/MCP/memory/LSP/sandbox: n.s. on official page.
- Community (not official, dsharness.io says unaffiliated; awesome list): web search plugins, MCP via `dsh-plugin-mcp-support` (@deepseek-ai/dsh-mcp-client), memory plugins, worktree isolation `dsh-workflow-worktree`, screen/GUI agents, `dsh-model-router` (planner deepseek-v4-pro, executors deepseek-v4-flash), provider integrations (Grok, Copilot, Codex, Anthropic, OpenRouter, MiniMax, Kimi, Zhipu).
- omo emulation: community plugin `royenheart/dsh-plugin-opencode-omo` (licence n.s., 34 commits, last commit 2026-09-03, no releases; requires stock dsh 0.1.2-alpha.2): omo `task()` with category/subagent_type/load_skills/run_in_background; roles oracle, librarian, explore, metis, momus, multimodal-looker; `read_image`; LSP preset (typescript-language-server); `/team-mode` (TUI differs); settings `opencode-omo-roles`.
- Headless/SDK/RPC: n.s. officially. Browser automation not bundled officially.

## Evidence: Pi (pi.dev, github.com/earendil-works/pi)
- MIT. v1.1.0 (2026-10-07). "Pi 1.0 with Pi Durable". Node >= 22.19. Install `npm i -g @earendil-works/pi-coding-agent`.
- Minimal by design: NO built-in subagents or plan mode ("skips features like sub-agents and plan mode"); NO built-in permission system. Modes: interactive, print (`pi -p`), JSON (`--mode json`), RPC (`pi --mode rpc`), SDK. RPC supports prompt/steer/cancel concerns; `agent_settled` event.
- MCP: pi.dev says built in with Codemode (JS sandbox); extensions can `pi.registerMcpServer`. Skills, extensions (TS), prompt templates, packages (`pi install npm:<pkg>`). Memory via extensions/packages (e.g. pi-memoria). Sandboxing via packages/containers (Gondolin micro-VM, Docker, OpenShell).
- Subagents/teams/worktrees only via community packages: `@tintinweb/pi-subagents` (parallel, steering), `@quintinshaw/pi-dynamic-workflows` (fan-out, git-worktree isolation, model routing), `pi-herdsman`. Unvetted third-party.
- Providers: Anthropic, OpenAI, Google, Azure, Bedrock, Mistral, Groq, Cerebras, xAI, HF, Kimi For Coding, MiniMax, NVIDIA, OpenRouter, Ollama; custom via `models.json`. Browser/Playwright, image input, LSP: n.s.

## Evidence: Qwen Code (github.com/QwenLM/qwen-code; qwenlm.github.io/qwen-code-docs)
- Apache-2.0. 757 releases; SDK TS v0.1.18 (2026-10-05). Install `npm i -g @qwen-code/qwen-code@latest` (Node 22+), brew, curl.
- Bundled: MCP client (stdio/SSE/streamable HTTP), `web_fetch` tool, Auto-Memory (`memory.enableManagedAutoMemory`, team memory), QWEN.md context, voice dictation (`general.voice.enabled`, `voiceModel`), image input (`visionModel`, `modalities` image/PDF/audio/video), image generation (`imageModel`), LSP (experimental `--experimental-lsp`), sandbox (`--sandbox`, off by default; `--yolo` does not sandbox), Computer Use (desktop automation, README), skills (`.qwen/skills/`), hooks, extensions (also installs Gemini CLI / Claude Code marketplace extensions), built-in skills /review /batch /loop /bugfix. Browser automation: n.s. as bundled (MCP can provide).
- Multi-agent: subagents (`.qwen/agents/*.md`; `model` inherit|fast|id|authType:modelId; background by default; `list_agents`, `send_message`; `working_dir` can pin to a linked git worktree), forks, Agent Teams (`experimental.agentTeam`, default false), Workflows (`tools.workflowsEnabled`, default false, parallel subagents).
- Control: headless `qwen -p`, `--output-format text|json|stream-json`, `--input-format stream-json`, `--continue/--resume`, SDKs TS/Python/Java, `qwen serve` (HTTP+SSE, ACP, experimental), `--acp`. ACP clients can host Claude Code and Codex (subagents doc).
- Models: settings.json `model.name`, `modelProviders`, `fastModel`, `advisorModel`, `visionModel`, `modelFallbacks`; providers OpenAI, Anthropic, Gemini, Qwen APIs, Ollama, vLLM, third-party. "Deep integrations with Qwen models" (README) but no measured harness-model fit stated. Headless docs example model `qwen3-coder-plus`.
- Documented use cases: CI/CD, PR review, commit messages, API docs, release notes, batch/log analysis, goals, chat integrations (Telegram, DingTalk, WeChat, Feishu).

## Evidence: Aider (github.com/Aider-AI/aider; aider.chat/docs)
- Apache-2.0. MAINTENANCE SIGNAL: latest release v0.86.0 dated 2025-08-09; latest commit shown 2026-05-22 (page states no sunset). 
- Strengths documented: repo map (graph-ranked, `--map-tokens` default 1k), modes code/ask/architect/help (`--architect`, `--editor-model`, `--editor-edit-format editor-diff|editor-whole`), git auto-commit with undo, auto lint/test (`--lint-cmd`, `--test-cmd`, `--auto-test`, `--no-auto-lint`), `/voice`, images (`/add`, `/paste`), URL scrape `/web <url>`, scripting `--message/-m` (one-shot, exits), unofficial Python API (explicitly unsupported).
- NOT stated: MCP, subagents, parallel agents, worktrees, sandbox, plugins/skills, memory, LSP, headless server/RPC. Single-agent, model-centric tool. Models: "almost any LLM" via LiteLLM-style names (`--model deepseek|sonnet|o3-mini`, keys via `--api-key provider=key`); README says works best with Claude 3.7 Sonnet, DeepSeek R1 & V3, o1, o3-mini, GPT-4o (dated, pre-2026 model list).

## Evidence: Goose (github.com/block/goose; goose-docs.ai) - now Agentic AI Foundation (Linux Foundation); CLI download from github.com/aaif-goose
- Apache-2.0. v1.54.0 (2026-10-08), 155 releases, commit 2026-10-09. Rust; desktop app, CLI, API.
- Bundled built-in extensions (MCP servers): Developer (default), Computer Controller (webscraping, file caching, automations), Memory, Tutorial, Auto Visualiser. Platform extensions: Analyze (code structure/call graphs, default), Apps, Chat Recall, Code Mode, Extension Manager, Skills (default), Summon (delegate/load subagents, default), Todo, Top of Mind (persistent instructions). 70+ MCP extensions; goose checks external extensions for malware before activation; extensions can run in Docker `--container`. Browser automation/Playwright/LSP/voice/image input: n.s. as bundled (a Fetch MCP is an example).
- Multi-agent: subagents via Summon `delegate` (sequential default, parallel supported, max turns 25, timeout 5 min, no nested subagents, `GOOSE_SUBAGENT_MODEL`/`GOOSE_SUBAGENT_PROVIDER`); recipes (YAML) with sub-recipes run concurrently; scheduled recipes; goose can drive Codex as a stdio MCP server (`cmd: codex args: [mcp-server]`). 
- Headless: `goose run` with recipe (`--recipe`, `--params`, `--sub-recipe`, `--no-session`), env `GOOSE_PROVIDER`, `GOOSE_MODEL`, `GOOSE_MODE`, `GOOSE_MAX_TURNS`, `GOOSE_ALLOWLIST`. Permission default autonomous mode per evaluation-1 report.
- Config YAML `~/.config/goose/config.yaml`; providers 15+ (Anthropic, OpenAI, Google, Ollama, OpenRouter, Azure, Bedrock) and ACP bridging of Claude/ChatGPT/Gemini subscriptions. No native model.
- Documented headless use cases: CI/CD code review, test-failure analysis, doc updates, bulk code modernisation, multi-repo maintenance, DB migrations, scheduled security scans, dependency updates, server maintenance.
