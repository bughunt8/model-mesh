# Coordinator evidence

Coordinators sit above the harnesses and start, watch and settle several workers. Evidence was fetched on 2026-10-11 HKT. "n.s." means not stated on the fetched page.

## Verdicts

Open source by default. Anything proprietary or source-available appears only as a labelled exception that needs owner approval before use.

| Coordinator | Licence | Verdict | Reason |
|---|---|---|---|
| Orca | MIT | Default coordinator when a cell has two or more isolated worktrees or decision gates | Worker start, task DAGs, ask and reply, settlement rules |
| Emdash | Apache-2.0 | Open-source alternate | 34 detected CLI agents, worktrees, cron, ACP; steer and cancel not stated |
| Nimbalyst | MIT | Alternate for review UI only | Codex and Claude Code first-class, OpenCode alpha |
| Vibe Kanban | Apache-2.0 | Reference only | Vendor shutdown notice dated 2026-04-10; community-maintained |
| Superset | Elastic License 2.0 | Labelled exception | Source-available, not OSI open source |
| Conductor | Not stated | Reference only | Mac only, licence not shown |
| Warp | Client open source, Oz and server proprietary per the project FAQ | Labelled exception | One-level-deep orchestration, critic and verifier patterns |
| AQ | Not stated | Excluded | Hosted service, early-access queue |

When no cell has parallel worktrees, a single pilot controller replaces the coordinator. The matrix uses only `none` and `orca` as coordinator values, and the validator rejects the rest.


## Evidence: Orca (github.com/stablyai/orca; onorca.dev docs)
- MIT (README), free, macOS/Windows/Linux desktop ADE; v1.4.224 (2026-10-10), "we ship daily". Worktree per agent; fan one prompt across 5 agents, compare, merge winner; mobile app monitors/steers; Design Mode (click UI element in real Chromium -> HTML/CSS/screenshot to agent); Computer Use; CLI `orca worktree create`, `orca terminal send/read/wait/create`, browser snapshot/click/fill, scheduled automations, artifacts (opt-in). 
- Orchestration layer (skill-guides/orchestration.md): Runs, Tasks, authoritative Dispatch attempts, supervised workers, `worker-start --spec ... --worktree current --agent codex|claude --json`, `task-create` + `worker-start --task`, worker messages, blocking ask/reply, `worker_done`/escalation/question waits, task DAGs, decision gates, coordinator loops; "start a full independent wave before waiting"; prefer parallel waves over dependency chains deeper than 3-4. Settlement + stop/abandon/retain/release rules.
- Supported agents (README list, 35+): Claude Code, Codex, Grok, Cursor, Copilot, Muse, DeepSeek Harness, OpenCode, Pi, oh-my-pi, Goose, Qwen Code, Amp, Kimi, Kiro, Cline, Droid etc. and any CLI agent. Orchestration examples name only `codex`, `claude` as --agent values.
- n.s.: MCP client/server, memory, sandboxing, headless/SDK, cancel command. Permissions defaults n.s. (worktrees = checkout isolation only, per your Orca pilot spec).

## Evidence: Vibe Kanban (github.com/BloopAI/vibe-kanban; vibekanban.com/blog/shutdown)
- Apache-2.0. SUNSETTING: bloop shutting down (post dated 2026-04-10); remote services removed after 30 days (kanban issues, comments, projects, orgs); community-maintained open source continues; local workspaces keep working. Latest release v0.1.44 (2026-04-24); a 2026-09-19 commit bumps to 0.1.45. Agents: Claude Code, Codex, Gemini CLI, Copilot, Amp, Cursor, OpenCode, Droid, CCR, Qwen Code. `npx vibe-kanban`. Kanban + workspace (branch, terminal, dev server) per agent; diff comments; built-in browser preview. Worktree isolation not explicitly stated except cleanup flag. Verdict input: community-maintained, reduced; treat as reference/labelled exception.

## Evidence: Nimbalyst (github.com/nimbalyst/nimbalyst; nimbalyst.com)
- MIT (desktop+iOS). v0.80.6 (2026-10-09). Visual workspace: parallel sessions each in own git worktree, Kanban, WYSIWYG markdown/mockup/diagram editors, red/green diff review, MCP connect (any server), extensions SDK, iOS voice replies. Providers: Codex, Claude Code first-class; OpenCode and Copilot ALPHA; Gemini via extension. "Built around Claude Code". Subagents/headless/dispatch/cancel n.s. Teams share docs/trackers; agent sessions not shared.

## Evidence: Emdash (github.com/generalaction/emdash; emdash.com)
- Apache-2.0 (README, blog). v1.2.7 (2026-09-27), 171 releases, YC W26. Parallel agents each in own worktree+branch; 34 CLI agents auto-detected (Claude Code, Codex, Cursor, OpenCode, Amp, Devin, Qwen Code, Droid, Copilot, Antigravity, Oh My Pi...); tickets from Linear/GitHub/Jira/GitLab/Asana etc.; in-app browser preview; MCP server management; skills/prompts; cron-scheduled recurring agents; remote SSH/tmux; ACP chat UI; PR + CI checks. Worktrees can be disabled per task. Subagent/headless API/steer/cancel n.s.

## Evidence: AQ (aq.dev) 
- Hosted cloud multiplayer workspace; isolated git worktree per workspace; agents: Claude Code, Codex, Kimi Code, Grok, Cursor, Antigravity, Command Code, Devin, OpenCode, Pi; AQ Composer (own agent routed through AQ gateway); Linear `ai-task` sync; licence not stated; early-access queue (work Google account, reviewed in 1-2 days). Not open source as stated -> labelled exception / excluded from matrix cells.

## Evidence: Superset (github.com/superset-sh/superset; docs.superset.sh)
- Elastic License 2.0 = SOURCE-AVAILABLE, NOT OSI open source (page: may use/fork/modify/self-host; cannot resell as a service). Desktop v1.37.0 (2026-10-08), 246 releases, ships daily. Parallel workspaces each isolated git worktree+branch; CLI, TypeScript SDK and MCP server can manage workspaces; CLI launches agents, reads terminals, manages automations; built-in `superset:*` skills (orchestrate parallel agents, schedule automations); recipes "race agents", "fan out a refactor", "wake up to an audit"; `.superset/config.json` (setup/teardown/run); model picker + reasoning effort per agent; providers OpenRouter, Bedrock, Vertex, Vercel AI Gateway. Worktrees "do not sandbox processes or prevent merge conflicts". Agents named: Claude Code, Codex, Amp, Gemini, OpenCode, Cursor Agent. -> labelled licence exception under OSS-by-default rule.

## Evidence: Conductor (conductor.build; Melty Labs)
- Licence NOT stated (Mac app; treat as not open source until shown). Docs: isolated workspaces (git worktrees), parallel agents, diff viewer, checks, agent modes, Conductor API (HTTP, cloud workspaces), MCP server for cloud workspaces, `.conductor/settings.toml`. Harnesses: Claude Code, Codex, Cursor, OpenCode. Mac-only. -> labelled exception / reference only.

## Evidence: Warp (docs.warp.dev/platform/orchestration; warp.dev newsroom 2026-04-28)
- Core product open-sourced 2026-04-28; licence type NOT stated on fetched pages (verify before listing as OSS; OpenAI is flagship sponsor). Oz = cloud orchestration platform.
- Orchestration doc (updated 2026-10-09): one parent spawns children, EXACTLY ONE LEVEL DEEP (children cannot spawn children); local/cloud mixes; children can run a different runtime (Warp Agent, Claude Code, Codex); independent lifecycle/transcript/credits per child; durable server-backed message bus; `/orchestrate`, `/plan`; Oz CLI; API `POST /agent/runs` with `mode: orchestrate|plan`, `GET /agent/runs/{runId}`; cancel is a run state (no command stated); documented patterns: supervisor/worker queue, fan-out/fan-in across modules/files/test targets/MODELS, CRITIC/VERIFIER review cycles, cloud review swarm for open PRs, dependency DAGs. Models: Kimi, MiniMax, Qwen open-weight options added; harness/model configurable per child.
