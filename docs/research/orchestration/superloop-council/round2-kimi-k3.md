# Round 2 rebuttal: The Researcher (Kimi K3)

## 1. The point I accept: the cumulative provenance ledger (First-Principle)

The First-Principle's warning that a mid-run profile switch can put a reviewer on its own family's earlier work changes my recommendation. In round 1 I treated family disjointness as a property of one profile. It is a property of the whole run.

I checked it against [MATRIX.md](../MATRIX.md). Ultimate A01 authors are deepseek-v4-pro then kimi-k3, with qwen3.8-max reviewing. Hybrid A01 uses deepseek-v4-pro as the momus reviewer. A run that starts in ultimate and drops to hybrid after a cap therefore has DeepSeek reviewing DeepSeek's earlier commits.

New requirement: the driver keeps an append-only ledger of (artifact, author model, author family, segment). Every review is checked against the whole ledger, not the current profile. If a switch would break disjointness, the run stops for a human.

## 2. Claims I reject

**(a) "`opencode run --agent sisyphus` is the worker call" (First-Principle, Adversarial, and my own round 1).**
OpenCode v1.19.4 looks the name up once. If it is missing, it prints a warning and falls back to the default agent, so it does not fail ([run.ts](https://raw.githubusercontent.com/sst/opencode/v1.19.4/packages/opencode/src/cli/cmd/run.ts)). omo ships its own resolver that lists the registered agents and matches the exact name, then the configured display name, then the config-key equivalent ([runnable-agent-resolver.ts](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/v4.19.4/packages/omo-opencode/src/cli/run/runnable-agent-resolver.ts)). Its wrapper also resolves `--agent`, `OPENCODE_DEFAULT_AGENT` and `default_run_agent` in a fixed order ([agent-resolver.ts](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/v4.19.4/packages/omo-opencode/src/cli/run/agent-resolver.ts)). That resolver exists because the bare key can miss. I read the code but did not run it live, so I do not claim the plain command always misses. I claim the PR must not trust either command and must assert the agent and model that actually ran from the JSON output.

**(b) "Default cap of 100 matches omo" (Practical) and "4.19.4 enforces 100, dev does not" (Explainer).**
Both are wrong, and so was my round 1. The dev docs say ["the Goal hook doesn't enforce an iteration cap"](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/docs/reference/features.md), and v5.1.48 carries [the same wording](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/v5.1.48/docs/reference/features.md). The v4.19.4 docs [claim an iteration cap](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/v4.19.4/docs/reference/features.md), but the v4.19.4 hook [has no counter in its code](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/v4.19.4/packages/omo-opencode/src/hooks/goal/index.ts). The documentation is the error. The Practical's boulder cap of 8 comes from [a senpi commit](https://github.com/code-yeongyu/oh-my-openagent/commit/3a56234e3), not from the OpenCode edition the pilot pins. A cap of 100 is not an omo default for anything this PR runs.

**(c) "No published retention policy" (Practical, Adversarial).**
The [TypeSafe DPA](https://typesafe.ai/legal/data-processing) has a criteria-based retention clause ("retained for as long as necessary taking into account the purpose of the Processing"). The same page gives no deletion procedure and does not mention zero data retention. TypeSafe's help center has a [dedicated zero-data-retention article](https://help.typesafe.ai/articles/9520184411-do-you-offer-zdr). So the Explainer is right that the repo note is outdated, but the ZDR claim lives in a help-center article and must be confirmed in the contract before any HK-eligible use. On madewithjev, the Practical's "vendor guide" is wrong. The site's [about page](https://madewithjev.com/about) says it is run by one person, is independent, and is not paid for or reviewed by TypeSafe. That is a self-declaration by a solo curator. It is fine for usage examples and not evidence of Jev's accuracy.

## 3. Positions

**D1. Loop ownership.** The driver owns continuation. The worker call is omo's `run`, used as a per-call barrier, not as the loop. omo's `run` waits for boulder, ralph-loop and todo markers ([continuation-state.ts](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/v4.19.4/packages/omo-opencode/src/cli/run/continuation-state.ts)). It does not wait on Goal, and Goal is gated on `goal.enabled`, which defaults to off ([AGENTS.md](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/AGENTS.md)). The PR line:

`timeout "$REMAINING_SECONDS" bunx oh-my-openagent@4.19.4 run --agent sisyphus --json --directory "$WORKTREE" "$PROMPT"`

Goal stays off, and `/goal` and `/start-work` are never sent. The `@4.19.4` pin on `bunx` is unverified, so the PR should test the resolved version at startup.

**D2. omo target.** Pin v4.19.4 for the pilot. On the Goal cap: no version enforces it in code. v4.19.4 has no counter, and dev and v5.1.48 say so in their docs. The First-Principle and the Explainer are right about 5.x. The Explainer is wrong about 4.19.4, and I was wrong about dev. Support for 5.x or OmO Native is a separate adapter in a later PR.

**D3. Decision seat family.** The rule applies to any seat that can dispatch, choose a worker or profile, or let work skip a check. A brake-only seat (stop, or add a check) is exempt from disjointness but must log its lineage. Qwen-derived deciders count as alibaba. Gemma-derived deciders count as google, which O4 blocks. Laya has a published [ModernBERT-large base](https://systemonemodels.org/models/laya/), so its lineage is clear. Jev's internals are [not disclosed](https://github.com/forrepid/open-jevs/blob/main/docs/jev-research-2026-09-20.md), so Jev cannot hold a dispatching or gating seat. A log-only shadow seat is exempt only if the controller never reads its output, and the O6 egress and policy rule still applies.

**D4. Profile choice.** An owner-approved escalation ladder that the model may only request. Profile never moves down mid-run, and every move is checked against the ledger from section 1.

**D5. Done authority.** Advisory smoke detector only. If sensors are green but noul P(yes) on `goal_met` is low, it triggers an early independent review. It never ends the loop. No third gate in the pilot, because a third gate adds a seat whose false-green rate nobody has measured.

**D6. Thresholds.** Calibrate before any activation, in the Learn-then-Test style. Point thresholds such as 0.80 or 0.95 are shadow-only and logged, never acted on. The [calibration paper](https://arxiv.org/html/2610.36311v1) I cited in round 1 reports 147 of 190 point-threshold failures, and I found no Jev-version transfer test, so calibrate per model version. Concrete target: at least 150 labelled, traffic-matched iterations and an upper 90% bound on false-green of at most 0.05. Zero errors in 150 gives \(1-0.1^{1/150}\approx 0.015\), which passes. The three quantities differ:

- Jev choice confidence is rescaled, \(\frac{p_{max}-1/n}{1-1/n}\) ([Jev docs](https://docs.typesafe.ai/confidence.md)).
- ScaleDown choice confidence is the chosen option's probability ([ScaleDown](https://docs.scaledown.ai/api-reference/decisions.md)).
- Noul is P(yes).

Log raw probabilities and never compare across seats.

**D7. Pilot caps, one number each.** 10 outer invocations. 30 minutes wall clock. 2 identical no-progress fingerprints (same diff hash and same failing-check set). 3 fix-verify cycles. Three fix-verify cycles need about six calls, plus plan and final review, so 10 leaves slack without reaching 100. A dollar cap needs the owner's number, and I will not invent one.

**D8. Validator.** No O19 and up in this PR. A rule for a seat that is not adopted cannot be tested against real behavior. Ship the rules with the first adoption. The ledger check ships now as a runtime test, not a validator rule.

**D9. CDMs in this PR.** Neither as shipped code. Ship a stub interface and a fixture that checks offsets (`raw[start:end] == span`). ScaleDown's `/v1/scaledown` [reads only `state.text` and `state.document`, and `usage` is the sum of every internal call](https://docs.scaledown.ai/api-reference/decisions-overview.md), so a state builder cannot pass structured fields through. Summarize and Compress stay out of the decision path, because they rewrite the evidence the seat is judging. Laya's English limit is [512 tokens, with 192 reserved for question and options, leaving about 320 for state](https://systemonemodels.org/models/laya/). The 320 and 512 figures are both right, and the Adversarial's 380-token state overflows it. Jev 1.14 allows [64k per request and 32k per question](https://docs.typesafe.ai/models.md), so size is not the Jev constraint.

**D10. "Endless".** There is no defensible reading as literally endless. A sentence the owner could sign: "The loop persists until independent review confirms the goal is met, or until a hard cap or a human gate stops it."

**D11. Verdict.** The hypothesis is disproved as a claim about the six patterns. A bounded, typed-decision seat is defensible in each one, and none of them needs it to write code. It holds for the orchestrator seat itself, because task breakdown and synthesis need generation, and a typed-answer model cannot produce that. So "disproved in all six, holding for the orchestrator" are both true, and the PR should say so.

## 4. Corrections to my round 1 report

1. **Goal cap.** I stated a default cap of 100 on dev from stale cached docs. Fresh dev docs and v4.19.4 code show no enforced cap, as in D2.
2. **PR command.** I proposed `opencode run --agent sisyphus`. Use the omo wrapper in D1 and assert the agent that ran.
3. **What `run` absorbs.** `run` waits on boulder, ralph-loop and todo markers, not on Goal. Round 1 blurred this.
4. **Retention wording.** Add the DPA's criteria-based clause and the help-center ZDR article. "No published policy" was an overstatement.
5. **Unverified inference.** My round 1 inference about a TypeSafe leadership role rested on one blog post (ibl.ai), and I did not re-verify it this round. Treat it as unconfirmed.
