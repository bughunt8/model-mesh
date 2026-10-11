# Council report: harness + model use-case matrix for model-mesh (Kimi K3 member)

Council member: Kimi K3 (Moonshot AI) | 2026-10-11 HKT | Basis: repo checkout `open-model-method`, evidence notes `mm-orch/research/*` (2026-10-11), live web verification same day.

Bias control: Kimi models are my own lab's; no Moonshot model reviews Moonshot work here, and Moonshot is not privileged over better-evidenced families.

**Distinctive contribution: a dated model-lifecycle correction that changes the repo's chains.** DeepSeek retired V4-Flash and is phasing out V4-Pro: since 2026-09-14 all `deepseek-v4-pro` requests route to V4.1-Flash at V4.1 rates, "until V4.1-Pro launches" ([announcement](https://www.deepseek.com/en/news/deepseek-v4-1-flash/), [changelog](https://api-docs.deepseek.com/updates/)). Xiaomi ships MiMo-V2.6-Pro (open-weight, vendor-claimed AA Index 46) at **$0.87/1M out**; V2.5 IDs auto-route to V2.6 from 2026-10-14 ([release](https://mimo.mi.com/docs/en-US/news/latest/v2-6), [pricing](https://mimo.mi.com/docs/en-US/pricing)). Both break `profiles/*.example.json` assumptions (V4-Pro as `open-reason-xl`; MiMo v2.5 rungs). Matrices re-anchor on **V4.1-Flash, MiMo-V2.6-Pro, GLM-5.3, Kimi K3, Qwen3.8-Max** with affected cells flagged.

---

## 1. Harness capability table

From `mm-orch/research/notes-harnesses.md` (2026-10-11) unless cited; `n.s.` = not stated on the fetched page.

| Harness | Licence | Bundled browser | MCP | Memory | A/V/image input | LSP | Sandbox | Subagents | Headless/SDK/RPC | Worktree | Maturity risk |
|---|---|---|---|---|---|---|---|---|---|---|---|
| OpenCode (+omo) | MIT ([DeepWiki](https://deepwiki.com/sst/opencode/10.2-license-and-contributing)) | n.s. (web fetch/search are permission keys) | Yes, local+remote, per-agent tool glob | n.s. | Image in; audio/video n.s. | Plugin hook for lsp diagnostics; bundled n.s. | n.s. | Yes (General/Explore/Scout + custom) | CLI+SDK, JSON events, `session.abort` | Plugin context exposes `worktree` | Low: v1.18.35 (2026-10-06); OpenCode 2 cannot co-install with 1 |
| DSH | MIT | n.s. officially | Community plugin only | Community plugin only | `read_image` via omo plugin; rest n.s. | Community omo preset only | n.s. | Agent teams (exp.) | n.s. officially | Community plugin `dsh-workflow-worktree` | Medium-high: PUBLIC PREVIEW; omo plugin 34 commits, no releases, pins dsh 0.1.2-alpha.2 |
| Codex CLI | Apache-2.0 | **Yes** (Browser Use; Computer Use macOS/Windows) | Yes (stdio/HTTP) | Yes (off by default) | `tools.view_image`; voice n.s. | n.s. | Yes (`sandbox_mode`) | Yes (`features.multi_agent` default on) | `codex exec` non-interactive | n.s. | Low: 0.162.1. Default provider OpenAI — HK needs custom `model_providers.<id>`, path unevidenced |
| Pi | MIT | n.s. | Built in (Codemode JS sandbox) | Via packages | n.s. | n.s. | Via packages (Gondolin, Docker) | **None built in**; community pkgs | `pi -p`, json, **RPC** (steer/cancel; `agent_settled`), SDK | Community pkg only | Low-med: v1.1.0; **no built-in permission system** |
| Qwen Code | Apache-2.0 | n.s. bundled (MCP can supply) | Yes (stdio/SSE/HTTP) | Yes (Auto-Memory) | Yes: image/PDF/audio/video; voice; image gen | Yes (exp. `--experimental-lsp`) | Yes (`--sandbox`, off default) | Yes: subagents, forks, Agent Teams/Workflows (exp.) | `qwen -p`, json/stream-json, 3 SDKs, `qwen serve`, ACP | Yes (`working_dir` pins worktree) | Low: 757 releases; multi-agent features experimental |
| Aider | Apache-2.0 | n.s. | n.s. | n.s. | Images, `/voice`, `/web` | n.s. | n.s. | **None** (single-agent) | One-shot `--message`; unofficial Python API | n.s. | **High: last release 2025-08-09, last commit 2026-05-22** |
| Goose (AAIF) | Apache-2.0 | n.s. bundled (Computer Controller ext. does automation) | Yes (70+ MCP ext., malware-checked; Docker `--container`) | Yes (Memory ext.) | n.s. | n.s. | Extensions in Docker | Yes (Summon `delegate`, parallel, no nesting; sub-recipes) | `goose run`, json/stream-json, recipes, `--no-session` | n.s. | Low: v1.54.0 (2026-10-08); Linux Foundation |

### Coordinator table

| Coordinator | Licence class | Supported harnesses | Worktree isolation | Dispatch / steer / cancel evidence | Maintenance risk | OSS-default eligibility |
|---|---|---|---|---|---|---|
| Orca | MIT | 35+ CLIs (Codex, Claude Code, OpenCode, DSH, Pi, Goose, Qwen Code…) | Yes, worktree per agent | `task-create`, `worker-start --task --agent`, worker messages, blocking ask/reply, task DAGs, decision gates, parallel waves, settlement (stop/abandon/retain/release); explicit cancel n.s. | Low (ships daily) | **Yes** |
| AQ | Licence n.s.; hosted early access | Codex, Claude Code, Kimi Code, OpenCode, Pi… | Yes | Hosted; Linear `ai-task` sync | Early-access queue | **No — excluded** |
| Vibe Kanban | Apache-2.0 | Claude Code, Codex, Gemini CLI, OpenCode, Qwen Code… | Not explicit | Kanban + branch/terminal/dev-server per agent | **Sunsetting** (bloop closed 2026-04-10; community fork) | Reference / labelled exception |
| Nimbalyst | MIT | Codex, Claude Code first-class; OpenCode ALPHA | Yes, per-session worktree | Dispatch/steer/cancel n.s. | Low | Yes |
| Emdash | Apache-2.0 | 34 auto-detected CLIs | Yes, worktree+branch per agent | Tickets from Linear/GitHub/Jira; cron agents; steer/cancel n.s. | Low | Yes |
| Superset | **Elastic-2.0 — source-available, not OSI** | Claude Code, Codex, Amp, Gemini, OpenCode, Cursor | Yes (not a sandbox) | CLI, TS SDK, MCP server; race/fan-out recipes | Low | Labelled licence exception only |
| Conductor | Licence n.s. (Mac app) | Claude Code, Codex, Cursor, OpenCode | Yes | HTTP API; MCP server | n.s. | Not OSS until shown — reference only |
| Warp | Client open-sourced 2026-04-28, **AGPL-3.0 + MIT UI crates** ([Warp blog](https://www.warp.dev/blog/warp-is-now-open-source)); **Oz orchestration stays proprietary** ([datastudios](https://www.datastudios.org/post/warp-terminal-open-source-client-agent-orchestration-and-oz-pricing-explained)) | Warp Agent, Claude Code, Codex as children | Local/cloud children, exactly one level deep | `/orchestrate`, Oz CLI, `POST /agent/runs`, durable bus; cancel is a run state | AGPL copyleft; OpenAI founding sponsor | Client yes; **Oz = labelled proprietary exception** |

---

## 2. Harness-model affinity

| Harness | Documented favoured families / ship defaults | Citation | Verdict |
|---|---|---|---|
| OpenCode + omo | Provider-agnostic (75+ providers). omo upstream defaults skew Anthropic/OpenAI: sisyphus `claude-opus-5-5`, hephaestus `gpt-5.6-sol`, ultrabrain `gpt-6-astra`, visual-engineering `claude-fable-5-1` | [omo AGENTS.md](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/packages/omo-opencode/src/agents/AGENTS.md) | Affinity is omo-config, not OpenCode. "omo best with GPT/Claude": **UNMEASURED** — defaults are curations |
| DSH | UI label `DeepSeek-V41-Flash`; community `dsh-model-router` (planner v4-pro / executors v4-flash) | notes-harnesses.md (unaffiliated awesome list) | "DSH best with DeepSeek Flash": **UNMEASURED**. v4-pro/v4-flash IDs now resolve to V4.1-Flash server-side ([changelog](https://api-docs.deepseek.com/updates/)) |
| Codex CLI | Default provider OpenAI; docs example `gpt-6.1-sol`; custom providers supported | notes-harnesses.md; [GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/) | Favours OpenAI by default. Non-OpenAI fit: **UNMEASURED** |
| Pi | 15+ providers incl. Kimi For Coding, MiniMax; custom via `models.json` | pi.dev (notes) | No affinity claim; **UNMEASURED** |
| Qwen Code | "Deep integrations with Qwen models" (README); headless example `qwen3-coder-plus` | notes-harnesses.md | "Qwen Code best with Qwen3.8": **UNMEASURED**. Alibaba's own Qwen3.8-Max evals ran inside **Claude Code**, not Qwen Code ([Qwen3.8 blog](https://qwen.ai/blog?id=qwen3.8)) — evidence against a first-party advantage |
| Aider | README: "works best with Claude 3.7 Sonnet, DeepSeek R1 & V3, o1, o3-mini, GPT-4o" | [aider.chat/docs/llms](https://aider.chat/docs/llms.html) | Vendor-stated, dated pre-2026; current fit **UNMEASURED** |
| Goose | Docs: "works best with Claude 4 models"; tool-calling required | [Goose providers doc](https://goose-docs.ai/docs/getting-started/providers/) | Vendor-stated, not benchmarked per-harness: **UNMEASURED** |

Media note: Seedance 2.5, Wan 3, Kling v3, GPT Image 2.5 Sunburst are not coding models; usable only as optional asset generators in A11/A12, never as workers/reviewers.

---

## 3. Situation matrix, per profile

Cell format: pattern · coordinator · orchestrator · workers primary + alt · reviewer (diff harness AND family from every worker) · omo agents · categories · rationale. Chains: primary → fallbacks. All unmeasured design proposals.

### Profile `ultimate` (HK-native; DeepSeek / Moonshot / Z.ai / Alibaba / MiniMax / Xiaomi only; no proxy)

Base chains (lifecycle-corrected): reasoner = **deepseek-v4.1-flash** (V4-Pro routes here) → kimi-k3 → glm-5.3; coding = kimi-k3 → qwen3.8-max → glm-5.3; orchestration = glm-5.3 → qwen3.7-plus; lifeline = **mimo-v2.6-pro** ($0.87). Codex CLI **unavailable** (default provider OpenAI, not HK-reachable; custom-provider path unevidenced).

| # | Pattern · Coord | Orchestrator | Workers (primary; alt) | Independent reviewer | omo agents · categories | Rationale |
|---|---|---|---|---|---|---|
| A01 regression repair | P1+P4 · none | OpenCode/omo sisyphus on glm-5.3 | OpenCode/omo hephaestus on deepseek-v4.1-flash → kimi-k3 → qwen3.8-max; alt: atlas on kimi-k3 | Qwen Code headless on **qwen3.8-max** (Alibaba ≠ DeepSeek/Moonshot workers) | sisyphus→explore→oracle→hephaestus→momus(triage) · deep, quick | omo ships the 11 named agents; Qwen Code headless + exp. LSP favours fix verification; qwen3.8-max frontier-class agentic ([NYU RITS](https://rits.shanghai.nyu.edu/ai/qwen3-8-max-draws-level-with-the-frontier-on-agentic-benchmarks/)) |
| A02 bounded feature | P1+P4 · none | OpenCode/omo sisyphus on glm-5.3 | hephaestus on kimi-k3 (DeepSWE 67.5, TB-2.1 88.3 — [K3 repo](https://github.com/MoonshotAI/Kimi-K3)) → deepseek-v4.1-flash; alt: Qwen Code subagent on qwen3.8-max | Goose recipe on **glm-5.3** (Z.ai) | sisyphus→prometheus→hephaestus→momus · deep, unspecified-high | K3 1M-ctx agentic coding fits whole-feature delivery; Goose recipe = reproducible second opinion |
| A03 refactor | P1+P4 · none | OpenCode/omo sisyphus on glm-5.3 | hephaestus on kimi-k3 → qwen3.8-max; alt: atlas on qwen3.8-max | Qwen Code on **glm-5.3** | sisyphus→oracle→hephaestus→momus · deep | Behavior preservation wants cross-family diff scrutiny; Qwen Code worktree-pinned subagent isolates it |
| A04 CI/deploy diagnosis | P2 · none | Goose recipe on glm-5.3 | Goose on glm-5.3 → mimo-v2.6-pro; alt: OpenCode/omo explore+hephaestus on deepseek-v4.1-flash | OpenCode/omo momus on **kimi-k3** | metis→explore→hephaestus→momus · quick, deep | Only Goose documents CI/deployment headless workflows; recipes freeze the run contract |
| A05 security audit + remediation | P4+P2 · none | OpenCode/omo oracle on glm-5.3 (CyberGym 84.5% vendor-run — [z.ai](https://docs.z.ai/release-notes/new-released), UNMEASURED) | Worker A: OpenCode/omo hephaestus on glm-5.3 (audit); Worker B: Qwen Code on qwen3.8-max (patch) | **Pi RPC on deepseek-v4.1-flash** (DeepSeek ≠ both workers) | oracle→explore→hephaestus→momus · deep, ultrabrain | Split audit/patch across families so the patch writer cannot grade its own vuln claims |
| A06 independent change review | P4 only · none | none (review is the task) | Reviewer 1: Qwen Code `/review` on qwen3.8-max; alt: Goose on glm-5.3 | Reviewer 2: OpenCode/omo momus on kimi-k3 → deepseek-v4.1-flash | momus→oracle · deep | Two-family panel matches two-judge rule (D24) |
| A07 research brief | P1+P4 · none | OpenCode/omo sisyphus on glm-5.3 | librarian on qwen3.6-plus + explore on deepseek-v4.1-flash; `writing` on glm-5.3; alt: Goose on MiniMax-M3 | Goose on **MiniMax-M3** | librarian→explore→metis→momus · unspecified-high, writing | omo librarian/explore pair is built for retrieval; reviewer checks claim-citation support |
| A08 data reconciliation | P1+P4 · none | OpenCode/omo sisyphus on glm-5.3 | prometheus on kimi-k3 → qwen3.8-max; alt: Aider one-shot on qwen3.8-max | Pi RPC on **mimo-v2.6-pro** (Xiaomi ≠ workers; [AA-46 claim](https://mimo.mi.com/docs/en-US/news/latest/v2-6)) | prometheus→librarian→momus · deep, unspecified-high | Reconciliation wants second-family recomputation, not style review |
| A09 requirements/architecture | P1+P4 · none | OpenCode/omo sisyphus on glm-5.3 | oracle on deepseek-v4.1-flash → qwen3.8-max; metis on glm-5.3; alt: Qwen Code on qwen3.8-max | Goose on **kimi-k3** | oracle→metis→prometheus→momus · ultrabrain, writing | oracle = architecture seat; cross-family review catches self-consistent-but-wrong plans |
| A10 policy workflow | P2+P4 · none | Goose recipe + `GOOSE_ALLOWLIST` on glm-5.3 | Goose on glm-5.3 → mimo-v2.6-pro; alt: OpenCode/omo on qwen3.7-plus | OpenCode/omo momus on **deepseek-v4.1-flash** | metis→sisyphus-junior→momus · unspecified-low, deep | Allowlist + no-session makes the approval boundary explicit |
| A11 browser administration | P2+P4 · none | Qwen Code (bundled Computer Use + MCP browser) on qwen3.8-max | Qwen Code on qwen3.8-max → glm-5.3; alt: Goose + Playwright MCP on glm-5.3 | OpenCode/omo momus on **deepseek-v4.1-flash** | multimodal-looker→sisyphus-junior→momus · visual-engineering, quick | Only HK-compatible bundled Computer Use; Playwright MCP (Apache-2.0) satisfies D46 |
| A12 cross-app office | P2+P4 · none | Goose recipe on glm-5.3 | Goose on glm-5.3 → MiniMax-M3 ([1M-ctx multimodal](https://www.minimax.io/blog/minimax-m3)); alt: Qwen Code on qwen3.8-max | Pi RPC on **kimi-k3** | librarian→prometheus→momus · deep, writing | Recipes chain multi-app flows; consistency reviewed cross-family |

Unavailable cells in `ultimate`: none after the remap, but **flagged**: chains starting at `deepseek-v4-pro` now start at `deepseek-v4.1-flash`; `mimo-v2.5-*` rungs become `mimo-v2.6-*` from 2026-10-14.

### Profile `global` (unrestricted twin of ultimate; any vendor; no cap)

Adds OpenAI, Anthropic, Google, xAI. Top tier: gpt-6-astra ([OpenAI](https://openai.com/research/index/release/)), claude-opus-5.5 / fable-5-1 ([Anthropic](https://support.claude.com/en/articles/12138966-release-notes)), gemini-4-argon ([TechTimes](https://www.techtimes.com/articles/328384/20261002/gemini-4-argon-leads-knowledge-work-where-it-still-trails-before-you-commit.htm)), grok-4.7 ([xAI](https://docs.x.ai/developers/release-notes)). Codex CLI is the only bundled agent-browser, so it takes A11.

| # | Pattern · Coord | Orchestrator | Workers (primary; alt) | Independent reviewer | omo agents · categories | Rationale |
|---|---|---|---|---|---|---|
| A01 | P1+P4 · none | OpenCode/omo sisyphus on claude-opus-5.5 | hephaestus on gpt-6-astra → claude-opus-5.5 → kimi-k3; alt: atlas on kimi-k3 | Qwen Code on **qwen3.8-max** (Alibaba ≠ OpenAI/Anthropic) | sisyphus→explore→oracle→hephaestus→momus · deep, quick | Same structure as ultimate; flagship tier now OpenAI/Anthropic |
| A02 | P1+P4 · none | sisyphus on claude-opus-5.5 | hephaestus on gpt-6.1-sol (near-Astra at 1/5 price — [OpenAI](https://openai.com/index/introducing-gpt-6-1-sol/)) → kimi-k3; alt: Qwen Code on qwen3.8-max | Goose on **gemini-3.8-flash** | sisyphus→prometheus→hephaestus→momus · deep, unspecified-high | Cost-efficient flagship for routine features |
| A03 | P1+P4 · none | sisyphus on claude-opus-5.5 | hephaestus on claude-fable-5-1 → gpt-6.1-sol; alt: atlas on kimi-k3 | Qwen Code on **qwen3.8-max** | sisyphus→oracle→hephaestus→momus · deep | Fable-5.1 is omo's upstream refactor default; still reviewed by Alibaba family |
| A04 | P2 · none | Goose recipe on gemini-3.8-flash | Goose on gemini-3.8-flash → glm-5.3; alt: OpenCode/omo on deepseek-v4.1-flash | OpenCode/omo momus on **kimi-k3** | metis→explore→hephaestus→momus · quick, deep | Goose CI recipes; flash-tier suffices for log triage |
| A05 | P4+P2 · none | oracle on claude-opus-5.5 | Worker A: OpenCode/omo on glm-5.3 (UNMEASURED cyber claim); Worker B: Codex CLI sandboxed on gpt-6.1-sol (patch) | **Qwen Code on qwen3.8-max** | oracle→explore→hephaestus→momus · deep, ultrabrain | Codex `sandbox_mode` is the strongest harness-level containment for exploit code |
| A06 | P4 · none | none | Reviewer 1: Qwen Code `/review` on qwen3.8-max; alt: Goose on gemini-4-argon | Reviewer 2: OpenCode/omo momus on claude-opus-5.5 | momus→oracle · deep | Cross-vendor panel (Alibaba + Anthropic) |
| A07 | P1+P4 · none | sisyphus on claude-opus-5.5 | librarian on qwen3.6-plus + explore on gemini-3.8-flash; writing on claude-opus-5.5 | Goose on **MiniMax-M3** | librarian→explore→metis→momus · unspecified-high, writing | As ultimate |
| A08 | P1+P4 · none | sisyphus on claude-opus-5.5 | prometheus on gpt-6-astra → kimi-k3; alt: Aider one-shot on qwen3.8-max | Pi RPC on **mimo-v2.6-pro** | prometheus→librarian→momus · deep, unspecified-high | Astra for hardest analysis; Xiaomi recomputes |
| A09 | P1+P4 · none | sisyphus on claude-opus-5.5 | oracle on gpt-6-astra → claude-fable-5-1; metis on glm-5.3; alt: Qwen Code on qwen3.8-max | Goose on **kimi-k3** | oracle→metis→prometheus→momus · ultrabrain, writing | omo defaults ultrabrain to gpt-6-astra — curation, not evidence |
| A10 | P2+P4 · none | Goose recipe + allowlist on gpt-6.1-sol | Goose on gpt-6.1-sol → gemini-3.8-flash; alt: OpenCode/omo on qwen3.7-plus | OpenCode/omo momus on **deepseek-v4.1-flash** | metis→sisyphus-junior→momus · unspecified-low, deep | As ultimate |
| A11 | P2+P4 · none | **Codex CLI** (bundled Browser Use + Computer Use) on gpt-6.1-sol | Codex on gpt-6.1-sol → gpt-6-astra; alt: Qwen Code Computer Use on qwen3.8-max | OpenCode/omo momus on **kimi-k3** | multimodal-looker→sisyphus-junior→momus · visual-engineering, quick | Only bundled agent-browser evidence; that capability decides the cell |
| A12 | P2+P4 · none | Goose recipe on gpt-6.1-sol | Goose on gpt-6.1-sol → gemini-3.8-flash; alt: Qwen Code on qwen3.8-max | Pi RPC on **claude-fable-5-1** | librarian→prometheus→momus · deep, writing | Anthropic reviewer differs from OpenAI/Google workers |

### Profile `hybrid` (default; cap ≤$4.65/1M output on generalist/utility/orchestration rungs; flagship coder, oracle, ultrawork exempt)

Cap check on corrected rungs: deepseek-v4.1-flash (V4-family peak $3.96; V4.1 rates — verify), glm-5.3 $4.40, qwen-plus tiers, mimo-v2.6-pro **$0.87**, kimi-k2.7-code $4.00 ([Cloudflare](https://developers.cloudflare.com/workers-ai/models/kimi-k2.7-code/)) — all under cap. Exempt: kimi-k3 ($15), qwen3.8-max ($6, flagged where used). gpt-5.6-terra via apiyi kept per repo mapping.

| # | Pattern · Coord | Orchestrator (≤cap) | Workers (primary; alt) | Independent reviewer | omo agents · categories | Rationale |
|---|---|---|---|---|---|---|
| A01 | P1+P4 · none | sisyphus on glm-5.3 | hephaestus on gpt-5.6-terra(apiyi) → deepseek-v4.1-flash; alt: atlas on kimi-k2.7-code | Qwen Code on **qwen3.6-plus** (Alibaba ≠ workers) | sisyphus→explore→oracle→hephaestus→momus · deep, quick | Routine bugs need no exempt coder; k2.7-code alt under cap |
| A02 | P1+P4 · none | sisyphus on glm-5.3 | hephaestus on kimi-k3 (exempt flagship coder) → gpt-5.6-terra; alt: atlas on kimi-k2.7-code | Goose on **gemini-3.8-flash** | sisyphus→prometheus→hephaestus→momus · deep, unspecified-high | Feature delivery keeps the exempt coder only where defect risk is highest |
| A03 | P1+P4 · none | sisyphus on glm-5.3 | hephaestus on kimi-k2.7-code → gpt-5.6-terra; alt: atlas on mimo-v2.6-pro | Qwen Code on **qwen3.6-plus** | sisyphus→oracle→hephaestus→momus · deep | Refactors are mechanical enough for the mid coder at $4.00 |
| A04 | P2 · none | Goose on glm-5.3 | Goose on deepseek-v4.1-flash → mimo-v2.6-pro; alt: OpenCode/omo explore on qwen3.5-plus | OpenCode/omo momus on **kimi-k2.7-code** | metis→explore→hephaestus→momus · quick, deep | Log/CI triage is a utility loop — cheap rungs only |
| A05 | P4+P2 · none | oracle on gpt-5.6-sol (exempt architect rung, apiyi) | Worker A: OpenCode/omo on glm-5.3; Worker B: Qwen Code on kimi-k2.7-code (patch) | **Pi RPC on mimo-v2.6-pro** | oracle→explore→hephaestus→momus · deep, ultrabrain | Security review keeps the exempt oracle; patch stays capped |
| A06 | P4 · none | none | Reviewer 1: Qwen Code `/review` on qwen3.6-plus; alt: Goose on glm-5.3 | Reviewer 2: OpenCode/omo momus on gpt-5.6-terra | momus→oracle · deep | Review panel entirely on capped rungs — cheapest cell in the matrix |
| A07 | P1+P4 · none | sisyphus on glm-5.3 | librarian qwen3.6-plus + explore deepseek-v4.1-flash; writing on glm-5.3 | Goose on **MiniMax-M3** ($0.96 out — [OpenRouter](https://openrouter.ai/minimax/minimax-m3)) | librarian→explore→metis→momus · unspecified-high, writing | Retrieval/writing rungs are all capped by design |
| A08 | P1+P4 · none | sisyphus on glm-5.3 | prometheus on kimi-k3 (exempt) → gpt-5.6-terra; alt: Aider one-shot on qwen3.6-plus | Pi RPC on **mimo-v2.6-pro** | prometheus→librarian→momus · deep, unspecified-high | Analysis correctness justifies the exempt planner |
| A09 | P1+P4 · none | sisyphus on glm-5.3 | oracle on gpt-5.6-sol (exempt); metis on glm-5.3; alt: Qwen Code on qwen3.7-plus | Goose on **kimi-k2.7-code** | oracle→metis→prometheus→momus · ultrabrain, writing | Architecture seat is the named exemption; everything else capped |
| A10 | P2+P4 · none | Goose + allowlist on glm-5.3 | Goose on glm-5.3 → mimo-v2.6-pro; alt: OpenCode/omo on qwen3.5-plus | OpenCode/omo momus on **deepseek-v4.1-flash** | metis→sisyphus-junior→momus · unspecified-low, deep | Policy workflow is mostly tool orchestration; capped communicator suffices |
| A11 | P2+P4 · none | **Codex CLI via custom provider on qwen3.8-max** — only if that path verifies; else Qwen Code Computer Use | Qwen Code on qwen3.8-max → glm-5.3; alt: Goose + Playwright MCP on glm-5.3 | OpenCode/omo momus on **kimi-k2.7-code** | multimodal-looker→sisyphus-junior→momus · visual-engineering, quick | Browser capability decides; qwen3.8-max $6 exceeds cap but no cheaper bundled-browser path exists — flagged cap-exception candidate, not assumed exempt |
| A12 | P2+P4 · none | Goose on glm-5.3 | Goose on MiniMax-M3 → glm-5.3-flash; alt: Qwen Code on qwen3.7-plus | Pi RPC on **deepseek-v4.1-flash** | librarian→prometheus→momus · deep, writing | Office pack assembly is multimodal-heavy; M3 at $0.96 is the cheapest native-vision rung |

### Profile `b4b` (cap applied more aggressively; kimi-k3 only as deep-category fallback per repo)

| # | Pattern · Coord | Orchestrator | Workers (primary; alt) | Independent reviewer | omo agents · categories | Rationale |
|---|---|---|---|---|---|---|
| A01 | P1+P4 · none | sisyphus on glm-5.3 | hephaestus on gpt-5.6-terra → deepseek-v4.1-flash; alt: atlas on kimi-k2.7-code | Qwen Code on **qwen3.6-plus** | sisyphus→explore→oracle→hephaestus→momus · deep, quick | Same as hybrid A01 |
| A02 | P1+P4 · none | sisyphus on glm-5.3 | hephaestus on kimi-k2.7-code → gpt-5.6-terra; alt: atlas on mimo-v2.6-pro | Goose on **gemini-3.8-flash** | sisyphus→prometheus→hephaestus→momus · deep, unspecified-high | b4b drops the exempt k3 primary |
| A03 | P1+P4 · none | sisyphus on glm-5.3 | hephaestus on mimo-v2.6-pro → kimi-k2.7-code; alt: Aider on qwen3.6-plus | Qwen Code on **glm-5.3** (Z.ai ≠ Xiaomi/Alibaba workers) | sisyphus→oracle→hephaestus→momus · deep | Cheapest credible worker (MiMo $0.87) leads |
| A04 | P2 · none | Goose on glm-5.3-flash | Goose on deepseek-v4.1-flash → mimo-v2.6-flash ($0.28); alt: OpenCode/omo explore on qwen3.5-plus | OpenCode/omo momus on **kimi-k2.7-code** | metis→explore→hephaestus→momus · quick | Flash-tier throughout; diagnosis is volume work |
| A05 | P4+P2 · none | oracle on gpt-5.6-terra (b4b oracle uses flagship-mid, not sol) | Worker A: OpenCode/omo on glm-5.3; Worker B: Qwen Code on kimi-k2.7-code | **Pi RPC on mimo-v2.6-pro** | oracle→explore→hephaestus→momus · deep | Cheaper oracle rung; same split-family audit structure |
| A06 | P4 · none | none | Reviewer 1: Qwen Code on qwen3.6-plus; alt: Goose on glm-5.3-flash | Reviewer 2: OpenCode/omo momus on deepseek-v4.1-flash | momus · quick, deep | Review-only cell on the cheapest two families |
| A07 | P1+P4 · none | sisyphus on glm-5.3-flash | librarian qwen3.6-plus + explore deepseek-v4.1-flash; writing on glm-5.3-flash | Goose on **MiniMax-M3** | librarian→explore→metis→momus · unspecified-low, writing | glm-5.3-flash ([$0.50 out](https://docs.z.ai/guides/overview/pricing)) replaces glm-5.3 in orchestration |
| A08 | P1+P4 · none | sisyphus on glm-5.3 | prometheus on kimi-k2.7-code → gpt-5.6-terra; alt: Aider on qwen3.6-plus | Pi RPC on **mimo-v2.6-pro** | prometheus→librarian→momus · deep | k3 absent from b4b primaries (repo rule); mid coder plans |
| A09 | P1+P4 · none | sisyphus on glm-5.3 | oracle on gpt-5.6-terra → deepseek-v4.1-flash; metis on glm-5.3; alt: Qwen Code on qwen3.7-plus | Goose on **kimi-k2.7-code** | oracle→metis→prometheus→momus · deep, writing | ultrabrain seat downgraded to deep under b4b |
| A10 | P2+P4 · none | Goose + allowlist on glm-5.3-flash | Goose on mimo-v2.6-flash → glm-5.3-flash; alt: OpenCode/omo on qwen3.5-plus | OpenCode/omo momus on **deepseek-v4.1-flash** | metis→sisyphus-junior→momus · unspecified-low | Cheapest possible orchestration chain |
| A11 | P2+P4 · none | Qwen Code Computer Use on **qwen3.7-plus** (cheaper; capability UNMEASURED — flagged) | Qwen Code on qwen3.7-plus → glm-5.3; alt: Goose + Playwright MCP on glm-5.3-flash | OpenCode/omo momus on **kimi-k2.7-code** | multimodal-looker→sisyphus-junior→momus · quick, visual-engineering | Whether 3.7-plus can drive Computer Use is unverified — test first |
| A12 | P2+P4 · none | Goose on glm-5.3-flash | Goose on MiniMax-M3 → mimo-v2.6-flash; alt: Qwen Code on qwen3.5-plus | Pi RPC on **deepseek-v4.1-flash** | librarian→prometheus→momus · deep, writing | Same shape as hybrid with flash-tier orchestrator |

---

## 4. Independence audit

Checked all 48 cells: reviewer must differ from every worker in harness AND model family.

| Cell | Issue found | Resolution |
|---|---|---|
| A01–A03, A09 (all profiles) | omo momus/oracle run **inside OpenCode**, the worker harness — same-harness review fails the rule (brief §2). | omo momus kept only for in-loop triage; the independent reviewer is always the named external cell (Qwen Code / Goose / Pi). No exception. |
| ultimate A01–A03 (first draft: reviewer glm-5.3) | Reviewer family (Z.ai) = orchestrator family; §2 asks review/orchestration kept separate "as much as possible". | **Fixed** A01: reviewer → qwen3.8-max. A02: kept Goose/glm-5.3 as `ABSOLUTE-EXCEPTION`: the six-family HK pool is exhausted (DeepSeek+Moonshot workers, Z.ai orchestrator, Alibaba/MiniMax/Xiaomi in other seats); reviewer still differs from every worker in harness AND family, so the mandatory rule holds. A03: kept — qwen3.8-max is the worker alternate there, so Z.ai is the only non-colliding third family. |
| A11 (hybrid/global) | Orchestrator = worker harness by design (single-CLI P2). | Rule mandates only worker≠reviewer; reviewer (OpenCode/kimi) differs on both axes. Compliant. |
| A06 (all profiles) | Both reviewers are the "workers" (review IS the task). | The two seats differ in harness AND family in every profile. Compliant. |
| All A05 cells | Split worker (audit X, patch Y) + reviewer Z | Verified: ultimate = Z.ai audit / Alibaba patch / DeepSeek review — 3 families, 3 harnesses. Compliant. |

No remaining violations. One `ABSOLUTE-EXCEPTION` (ultimate A02; reviewer family = orchestrator family, worker-independence intact).

---

## 5. Cross-situation rules

1. **omo-native (P1) suffices when the deliverable is code or text in one repo.** OpenCode alone ships the 11 named agents and 8 categories; a coordinator adds plumbing without changing roles. A01–A03, A07–A09 use P1.
2. **The independent reviewer is never omo.** momus/oracle share the worker harness, so every cell names a P4 reviewer on a second harness (Qwen Code headless, Goose recipe, Pi RPC) AND family. Pi RPC is the preferred review substrate: `agent_settled` is the cleanest completion boundary here.
3. **A bundled browser decides A11.** Codex (Browser Use + Computer Use) wins where OpenAI is allowed; in `ultimate`, Qwen Code's documented Computer Use is the only HK-compatible bundled path; else Goose + Playwright MCP (Apache-2.0, D46-compliant) — never an unvetted community plugin.
4. **Goose owns CI-shaped work (A04, A10, A12).** Only harness with documented headless CI/CD, scheduled recipes, allowlists; recipes double as the frozen run contract.
5. **Coordinators (P5) only for genuine multi-repo or >3-agent fan-out.** No A-row as scoped needs Orca's worktree waves, so no cell spends coordinator overhead. If the pilot fans out later: Orca (MIT) default, Emdash alternate; AQ/Conductor excluded (licence unknown); Superset (Elastic-2.0) and Warp's proprietary Oz are labelled exceptions only.
6. **Family rotation across the six HK vendors.** No `ultimate` row repeats a family in worker + reviewer seats; DeepSeek/Moonshot/Z.ai/Alibaba/Xiaomi/MiniMax rotate so one vendor outage or blind spot never covers a row.
7. **Exempt rungs buy defect-risk reduction, not convenience.** kimi-k3 ($15) in hybrid only at A02/A08 primaries and deep fallbacks; qwen3.8-max ($6) in metered profiles only where a bundled capability or independence leaves no cheaper compliant option, always flagged.
8. **Lifecycle beats mapping.** Chains pointing at `deepseek-v4-pro`/`v4-flash`/`mimo-v2.5-*` must be re-pinned: DeepSeek routes those IDs to V4.1-Flash server-side (silently changing the model under a frozen config); MiMo V2.5 IDs die 2026-10-21. Frozen pilot configs must pin V4.1-Flash / V2.6 explicitly and re-qualify.

## 6. Risks and unknowns

- **Biggest change risk: DeepSeek V4.1-Pro launch.** V4-Pro routes to V4.1-Flash "until V4.1-Pro launches" ([announcement](https://www.deepseek.com/en/news/deepseek-v4-1-flash/)); the `open-reason-xl` seat should then move after re-qualification. Verify first.
- **Codex custom-provider path is unevidenced.** Every ultimate Codex cell and hybrid A11 depend on Codex running an HK-reachable model via `model_providers.<id>`; docs show the mechanism, no tested evidence. Verify first.
- **V4.1-Flash pricing** not in the evidence notes; cap-compliance inferred from V4-family rates ([ofox.ai](https://ofox.ai/blog/deepseek-v4-pro-0813-price-weights-benchmarks-api-access-2026/)). Confirm on the rate card.
- **All harness-model affinities are UNMEASURED** (§2). Alibaba benchmarked Qwen3.8-Max inside Claude Code, not Qwen Code — the "first-party harness advantage" hypothesis currently has evidence against, not for.
- **MiMo-V2.6-Pro's AA-46 claim is vendor-reported** ([release](https://mimo.mi.com/docs/en-US/news/latest/v2-6)); if it holds, it becomes the default cheap reviewer everywhere (different family from almost everything, $0.87).
- **DSH should be dropped from matrix seats.** Its omo emulation is a 34-commit community plugin pinned to an alpha; community add-ons carry no weight (rule 5), so DSH adds nothing OpenCode+omo lacks. Research target only.
- **Aider maintenance signal** (last release 2025-08-09) makes it a scored-harness risk; used only as alternate one-shot executor.
- **GLM-5.3 CyberGym claim is vendor-run** ([emergent.sh](https://emergent.sh/learn/glm-5-3-benchmarks)); A05's glm-5.3 audit worker needs independent evidence pre-pilot.
- **Warp/AGPL and Superset/Elastic-2.0** are labelled exceptions only; the zero-exception coordinator shortlist is Orca, Emdash, Nimbalyst.

## 7. Sources

Models: https://www.deepseek.com/en/news/deepseek-v4-1-flash/ · https://api-docs.deepseek.com/updates/ · https://mimo.mi.com/docs/en-US/news/latest/v2-6 · https://mimo.mi.com/docs/en-US/pricing · https://github.com/MoonshotAI/Kimi-K3 · https://www.kimi.ai/resources/kimi-k2-7-code · https://platform.kimi.com/docs/models · https://developers.cloudflare.com/workers-ai/models/kimi-k2.7-code/ · https://docs.z.ai/release-notes/new-released · https://docs.z.ai/guides/overview/pricing · https://emergent.sh/learn/glm-5-3-benchmarks · https://qwen.ai/blog?id=qwen3.8 · https://www.datacamp.com/blog/qwen3-8-max · https://rits.shanghai.nyu.edu/ai/qwen3-8-max-draws-level-with-the-frontier-on-agentic-benchmarks/ · https://www.minimax.io/blog/minimax-m3 · https://openrouter.ai/minimax/minimax-m3 · https://openai.com/index/introducing-gpt-6-1-sol/ · https://openai.com/research/index/release/ · https://support.claude.com/en/articles/12138966-release-notes · https://www.techtimes.com/articles/328384/20261002/gemini-4-argon-leads-knowledge-work-where-it-still-trails-before-you-commit.htm · https://docs.x.ai/developers/release-notes · https://ofox.ai/blog/deepseek-v4-pro-0813-price-weights-benchmarks-api-access-2026/

Harnesses/coordinators: https://github.com/code-yeongyu/oh-my-openagent/blob/dev/packages/omo-opencode/src/agents/AGENTS.md · https://aider.chat/docs/llms.html · https://goose-docs.ai/docs/getting-started/providers/ · https://www.warp.dev/blog/warp-is-now-open-source · https://itsfoss.com/news/warp-goes-open-source/ · https://www.datastudios.org/post/warp-terminal-open-source-client-agent-orchestration-and-oz-pricing-explained · https://deepwiki.com/sst/opencode/10.2-license-and-contributing

Repo evidence: `mm-orch/research/{notes-harnesses,notes-coordinators}.md`, `fetched.json`; `open-model-method/docs/{EXAMPLE-MAPPING,ROUTING}.md`, `profiles/*.example.json`, `docs/research/evaluation-1/*`, `BENCHMARKS.md`, `DECISIONS.md`
