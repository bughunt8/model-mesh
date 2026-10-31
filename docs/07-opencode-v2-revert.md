# OpenCode 2 Upgrade Attempt and Revert to V1

Date: 2026-10-18
Host: Pop!_OS, bash 5.1.16
Scope: OpenCode runtime, plugin loading, MCP configuration, session database

## Outcome

The upgrade from OpenCode 1.19.3 to OpenCode 2 (2.0.32) was reversed. `opencode` resolves to 1.19.3 again, and OpenCode 2 remains installed and callable as `opencode2`. The rollback was driven by one hard requirement: `oh-my-openagent` (omo) must function, and it has no functional V2 build.

No user configuration was modified during the upgrade attempt. `~/.config/opencode/opencode.json` retains its prior content; OpenCode 2 normalized it in memory only.

## Verification results

| Area | Result |
| --- | --- |
| Binary resolution | `opencode` = 1.19.3, `opencode2` = 2.0.32 |
| V1 server boot | Healthy, HTTP 200 on the sessions endpoint |
| V1 config parse | 11 providers, 132 models, `build` agent resolves |
| Session database | `integrity_check` = ok, foreign-key check clean |
| Session data | 152 sessions at backup time; all rows readable after revert |
| Warp plugin | Loads and emits notifications (verified functionally) |
| omo plugin | Loads under V1, v5.1.35, load counter incremented during verification |
| ponytail plugin | Loads without error |
| emdash notifications | Loads without error; inert unless its hook env vars are set |
| `crg-plugin.ts` | Fails to load; pre-existing breakage, see below |

## Warp plugin functional verification

Installed version 0.1.7. The plugin gates on `WARP_CLI_AGENT_PROTOCOL_VERSION`, which is present, so it registers hooks `event`, `chat.message`, `tool.execute.before`, and `tool.execute.after`, and logs `Warp plugin initialized`.

Driving the real plugin with synthetic V1 events inside a PTY produced 6 of 6 expected OSC 777 notifications, each at protocol `v=1` with correct session and project fields:

- `session_start`
- `permission_request`
- `prompt_submit`
- `question_asked`
- `tool_complete`
- `stop`

This confirms the payload builder, protocol negotiation, and `/dev/tty` delivery path, not merely that the module loaded.

## Pre-existing failure: crg-plugin.ts

`~/.config/opencode/plugins/crg-plugin.ts` fails on V1 with `app.on is not a function`. The identical error appears in local logs from 2026-09-21 under OpenCode 1.18.31, so this plugin was already broken before the upgrade and is unrelated to it. The plugin was written against an API that the current V1 plugin contract does not expose. Fixing it requires rewriting it against the V1 hook contract (`event`, `tool.execute.before`) rather than `app.on`.

## Log separation

Both OpenCode 1 and OpenCode 2 append to `~/.local/share/opencode/log/opencode.log`. V1 exposes no variable to relocate that path, so the split is done at invocation: `~/.local/bin/opencode-v1-debug` runs V1 with `--print-logs` and tees the same records to `~/.local/state/opencode-v1/logs/v1-<timestamp>.log`. Plain `opencode` is unaffected.

## Why omo cannot run on OpenCode 2 yet

- npm `oh-my-openagent` latest (5.1.35) targets the V1 plugin API only.
- The `dev` branch change that makes omo load on V2 explicitly does not run agents, tools, or hooks there.
- The real port is an unmerged slice series, tracked by issue #6169 and starting at PR #9391. That PR adds only a scaffold entry plus a parity matrix, and the remaining subsystems land slice by slice.
- A runtime-verified reference port exists in a private fork and cannot be consumed.

The practical consequence: any OpenCode 2 adoption that depends on omo's agents, categories, hooks, or team mode is blocked upstream, not locally fixable.

## Artifacts

- Database backup: `~/backups/opencode-pre-revert-2026-10-18/opencode.db` (833 MB, integrity ok)
- Configuration backup: `~/backups/opencode-pre-revert-2026-10-18/config/`
- Warp plugin harness and captured output: `~/.local/state/opencode-v1/warp-verify/`
- V1-only logs: `~/.local/state/opencode-v1/logs/`

## Reversing this state

- Re-upgrade to OpenCode 2: rename `~/.opencode/bin/opencode2-bin` back to `~/.opencode/bin/opencode`.
- Return to V1: the current arrangement; `opencode` already resolves to 1.19.3.

## Caveats

Verification was headless: server, API, config resolution, and the plugin hooks. No interactive TUI session was exercised. Session count rose from 152 to 155 during verification, attributed to long-running V1 sessions still attached to the same database; no rows were lost. OpenCode 2 left its own artifacts in place (`session_v2` table, `cli.json`, `service.json`), which V1 ignores and which make a future re-upgrade cheaper.
