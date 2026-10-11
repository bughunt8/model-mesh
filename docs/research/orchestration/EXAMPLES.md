# Worked examples

Four situations walked through with the real matrix values. Every task here is synthetic or public. Rows come from [MATRIX.md](MATRIX.md). Treat each as a rehearsal script, since nothing was executed.

## A01 regression bug repair

Scenario. A public sample project has a failing date-parsing test after a dependency bump. The fix must reproduce the failure first and show the regression test fails before and passes after.

| Profile | Orchestrator | Author seat | Independent reviewer |
|---|---|---|---|
| ultimate | opencode-omo sisyphus: glm-5.3 > glm-5.3-flash | opencode-omo atlas: deepseek-v4-pro > kimi-k3 | goose: qwen3.8-max > qwen3.7-plus |
| hybrid | opencode-omo sisyphus: glm-5.3 > glm-5.3-flash | opencode-omo hephaestus: gpt-5.6-terra > kimi-k3 | goose: deepseek-v4-pro > deepseek-v4-flash |
| b4b | opencode-omo sisyphus: glm-5.3-flash > glm-5.3 | opencode-omo atlas: kimi-k2.7-code > gpt-5.6-luna | goose: deepseek-v4-flash > deepseek-v4-pro |
| global | opencode-omo sisyphus: claude-sonnet-5-5 > glm-5.3 | opencode-omo hephaestus: gpt-6.1-sol > gpt-6-astra > kimi-k3 | goose: grok-4.7 > deepseek-v4-pro |

Flow in the default option.
1. The orchestrator seat splits the task: one `explore` pass finds the call sites, then the author seat writes a failing test and the fix in a throwaway worktree.
2. The author harness stops on a settled state. The frozen diff, the test output and an author manifest (harness, model, every fallback rung that fired) go to the reviewer.
3. The reviewer harness runs in read-only mode with the diff and the manifest. It must try to break the fix, for example with a boundary date, and report findings as structured JSON.
4. If the author primary hits a rate limit, the runtime walks the chain inside the same family pool. The reviewer pool never changes, so independence survives the outage.

Alternate for `ultimate`: dsh authors on deepseek-v4-pro > kimi-k3, goose reviews on qwen3.8-max > qwen3.7-plus. Alternate for `global`: dsh authors on gpt-6.1-sol > gpt-6-astra > kimi-k3, goose reviews on grok-4.7 > deepseek-v4-pro.

## A05 security audit and remediation

Scenario. A deliberately vulnerable public sample app has an injection flaw. The author must reproduce the exploit in isolation, patch it, and show the exploit now fails.

| Profile | Orchestrator | Author seat | Independent reviewer |
|---|---|---|---|
| ultimate | opencode-omo sisyphus: glm-5.3 > glm-5.3-flash | pi atlas: deepseek-v4-pro > kimi-k3 | goose: qwen3.8-max > qwen3.7-plus |
| hybrid | opencode-omo sisyphus: glm-5.3 > glm-5.3-flash | pi atlas: gpt-5.6-terra > kimi-k3 | goose: deepseek-v4-pro > deepseek-v4-flash |
| b4b | opencode-omo sisyphus: glm-5.3-flash > glm-5.3 | pi atlas: kimi-k2.7-code > gpt-5.6-luna | goose: deepseek-v4-flash > deepseek-v4-pro |
| global | opencode-omo sisyphus: claude-sonnet-5-5 > glm-5.3 | pi atlas: gpt-6.1-sol > gpt-6-astra > kimi-k3 | goose: grok-4.7 > deepseek-v4-pro |

Flow. Orca opens two worktrees, one for the audit and one for the fix, and waits for `worker_done` from each before the reviewer starts. Pi runs in a container with no credentials beyond the model key. The reviewer replays the exploit against the patched copy and tries a second payload that the author never saw. Production systems are never scanned.

Alternate for `ultimate`: codex authors on deepseek-v4-pro > kimi-k3, goose reviews on qwen3.8-max > qwen3.7-plus, conditional on the custom-provider route for Codex CLI. In `ultimate`, Codex CLI never uses an OpenAI model.

## A11 browser administration

Scenario. A local mock admin console, run from a container, needs a user disabled and a setting changed. Success is the final state, not the click log.

| Profile | Orchestrator | Author seat | Independent reviewer |
|---|---|---|---|
| ultimate | opencode-omo sisyphus: glm-5.3 > glm-5.3-flash | qwen-code atlas: qwen3.8-max > qwen3.7-plus | goose: deepseek-v4-pro > kimi-k3 |
| hybrid | opencode-omo sisyphus: glm-5.3 > glm-5.3-flash | qwen-code atlas: qwen3.7-plus > qwen3.5-plus | goose: deepseek-v4-pro > deepseek-v4-flash |
| b4b | opencode-omo sisyphus: glm-5.3-flash > glm-5.3 | qwen-code atlas: qwen3.7-plus > qwen3.5-plus | goose: deepseek-v4-flash > deepseek-v4-pro |
| global | opencode-omo sisyphus: claude-sonnet-5-5 > glm-5.3 | qwen-code atlas: qwen3.8-max > qwen3.7-plus | goose: grok-4.7 > deepseek-v4-pro |

Flow. Qwen Code drives the browser through the official Playwright MCP server with `trust` false, so each tool call asks first. A separate frozen Playwright test, written before the run, checks the final state. The reviewer gets only the end state, screenshots and the action log. The author never sees the test.

Alternate for `global`: goose authors on qwen3.8-max > qwen3.7-plus, pi reviews on grok-4.7 > deepseek-v4-pro.

## A12 cross-application office work

Scenario. A synthetic quarterly pack needs a spreadsheet total copied into a slide and a memo, then checked for exact agreement.

| Profile | Orchestrator | Author seat | Independent reviewer |
|---|---|---|---|
| ultimate | peers | qwen-code atlas: qwen3.8-max > qwen3.7-plus | goose: deepseek-v4-pro > kimi-k3 |
| hybrid | peers | qwen-code atlas: qwen3.7-plus > qwen3.5-plus | goose: deepseek-v4-pro > deepseek-v4-flash |
| b4b | peers | qwen-code atlas: qwen3.7-plus > qwen3.5-plus | goose: deepseek-v4-flash > deepseek-v4-pro |
| global | peers | qwen-code atlas: qwen3.8-max > qwen3.7-plus | goose: grok-4.7 > deepseek-v4-pro |

Flow. There is no AI orchestrator. The author seat writes the slide and memo from a frozen spreadsheet export and hands over immutable files. The reviewer recomputes the total from the spreadsheet and compares every quoted number and reference.

## When the row does not fit

If a task fits no situation, pick the closest by what decides success, then add the P4 reviewer. If two author options look equally good, prefer the one whose harness is bundled with the tools the task needs. Do not mix seats from different options, because the independence check is done per option.
