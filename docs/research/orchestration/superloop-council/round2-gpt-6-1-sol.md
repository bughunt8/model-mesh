# First-principle rebuttal: one continuation owner, one shadow fork

28 October 2026. Round 2. Proposed policy, not a measured improvement.

## 1. What changes my recommendation

I accept The Practical's narrow pilot. My six-backend proposal tried to answer too many questions at once. I would now merge rules/replay plus one pinned Jev shadow router over situations A01-A12, without production dispatch authority. No ScaleDown backend or extraction model in this PR.

One fork is enough to discover whether the model adds useful information. Multiple new backends would make failure harder to attribute. I also accept The Researcher's calibration objection: my round 1 numerical thresholds must not authorize actions without local qualification.

## 2. Three claims I reject after re-verification

1. **The Goal cap is not a reliable version distinction.** Both the Researcher's dev-cap claim and the Explainer's claimed v4.19.4 protection fail source inspection: the Goal hook has the identical Git blob, `7957411a9d3bca57cfddad7c4f9aab2351eb8324`, at v4.19.4, v5.1.48 and inspected dev, and contains no iteration counter or cap check. [v4.19.4 implementation](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/packages/omo-opencode/src/hooks/goal/index.ts), [v5.1.48 implementation](https://github.com/code-yeongyu/oh-my-openagent/blob/v5.1.48/packages/omo-opencode/src/hooks/goal/index.ts), [inspected dev implementation](https://github.com/code-yeongyu/oh-my-openagent/blob/bd1310b65df8d772bba604e958e79956dc3e89a2/packages/omo-opencode/src/hooks/goal/index.ts)

   The v4 documentation calls `default_max_iterations` a cap, but its hook construction does not pass that setting; the v5 documentation explicitly acknowledges non-enforcement. [v4 documentation](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/docs/reference/features.md), [v4 hook construction](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/packages/omo-opencode/src/plugin/hooks/create-session-hooks.ts), [v5 documentation](https://github.com/code-yeongyu/oh-my-openagent/blob/v5.1.48/docs/reference/features.md) Pinning v4 therefore does not replace an outer watchdog.

2. **"No published retention policy" is outdated.** Contrary to the Practical and Adversarial reports, TypeSafe publishes DPA retention criteria, although not a fixed deletion interval. [TypeSafe DPA](https://typesafe.ai/legal/data-processing) Enterprise ZDR requires confirmation and activation, and still retains operational telemetry; neither the DPA nor a no-training promise makes ordinary API traffic zero-retention. [TypeSafe ZDR explanation](https://help.typesafe.ai/articles/9520184411-do-you-offer-zdr)

3. **Made with Jev is not the vendor's guide.** The Practical repeatedly attributes it to TypeSafe, but the site explicitly says it is independent and unaffiliated, and describes its architecture as a design rather than a benchmark result. [Made with Jev](https://madewithjev.com/jev-multi-agent)

## 3. Decisions

**D1. Loop ownership.** The outer driver owns continuation; use the OMO-aware wrapper with `goal.enabled=false`, disabled hooks `goal`, `todo-continuation-enforcer`, `start-work` and `atlas`, fresh sessions, and an external process-group watchdog. [Pinned hook names](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/packages/omo-opencode/src/config/schema/hooks.ts) The wrapper's completion checks establish quiescence, not goal success. [Wrapper completion checks](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/packages/omo-opencode/src/cli/run/completion.ts)

PR worker command, using the declared binary alias from a lockfile-pinned v4.19.4 install, with no runtime package download: [package manifest](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/package.json), [CLI flags](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/docs/reference/cli.md)

```text
./node_modules/.bin/oh-my-openagent run --agent sisyphus --json --directory WORKTREE "PROMPT"
```

**D2. Target.** Stay on v4.19.4 OpenCode; migrating editions would confound this pilot. Treat the inspected v4.19.4, v5.1.48 and dev Goal paths as lacking an enforced iteration cap, as established by the identical implementations above. [Inspected Goal implementation](https://github.com/code-yeongyu/oh-my-openagent/blob/bd1310b65df8d772bba604e958e79956dc3e89a2/packages/omo-opencode/src/hooks/goal/index.ts)

**D3. Decision family.** Any consequential dispatch/gating seat must satisfy orchestrator-family disjointness across every fallback rung and the complete artifact lineage; Qwen/Gemma derivatives inherit their base family, while unknown provenance blocks activation. Exempt a log-only shadow seat only when its outputs cannot affect execution, including through prompts visible to acting agents.

**D4. Profile choice.** The owner sets the profile and optional escalation ladder; the model may request a change, never approve it. Validate each complete replacement assignment against cumulative lineage: A01's ultimate DeepSeek authors and hybrid DeepSeek reviewer demonstrate why validating the latest profile alone is insufficient. [Assignment matrix](https://github.com/bughunt8/model-mesh/blob/daf9ac42a9e86700a2f6c1c8b10353cd998a2a09/docs/research/orchestration/MATRIX.md)

**D5. Done authority.** Advisory smoke detector only, able to request early independent review. Never let its vote end the loop or become a mandatory third completion gate.

**D6. Thresholds.** Require Learn-then-Test-style qualification before activation, proposing accepted-decision accuracy of at least 99% with 95% confidence, separate learning/testing data, and a predeclared threshold grid; this is a population-level claim under assumptions, not per-answer certainty, and distribution shift invalidates its application. [Reference audit and limitations](https://arxiv.org/html/2610.36311v1) Calibrate each backend/question/locale separately: Jev's derived Choice confidence, ScaleDown's selected-option probability and Noul probability must remain distinct fields, while shadow cutoffs authorize nothing. [Jev Choice](https://docs.typesafe.ai/primitives/choice), [ScaleDown Choice](https://docs.scaledown.ai/api-reference/decisions), [Noul](https://docs.typesafe.ai/primitives/noul)

**D7. Pilot caps.** Six outer iterations, 30 minutes total wall clock, two consecutive no-progress iterations, and three failed fix-verify cycles per issue across the run. Resuming or changing profile never resets these counters.

**D8. Validator.** Add O19+ now for the decision contract, nonoperative shadow mode, finite budgets, activation qualification and cumulative family provenance. Unknown provenance must fail activation, without pretending that a production decision seat has already been adopted.

### D9. CDMs and constrained decoding

Neither a ScaleDown backend nor an Extract builder belongs in this PR; no Summarize or Compress integration either. A later worker-context experiment may use derived text, but policy and acceptance evidence must retain originals, since constrained decoding does not establish semantic correctness. [Constrained-decoding study](https://arxiv.org/html/2609.23742)

**D10. "Endless."** "Continue autonomously within my approved finite budget until the goal is independently verified or the system reports an honest stopping reason; only I may renew that budget."

**D11. Hypothesis.** Disproved in all six patterns: a bounded decision can occupy part of each, and Anthropic explicitly permits traditional classification in routing and describes its patterns as combinable building blocks. [Anthropic](https://www.anthropic.com/research/building-effective-agents) Whether a typed classifier alone can invent decomposition and synthesize results is a different proposition, which I reject.

## 4. Corrections and clarifications to my round 1

- Replace my bare `opencode run --agent sisyphus` recommendation with the pinned wrapper above. Its resolver normalizes agent names, but can fall back when an agent is disabled, so preflight must verify the actual resolved agent and model bindings rather than trusting the requested name. [Pinned resolver](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/packages/omo-opencode/src/cli/run/agent-resolver.ts) This corrects my unverified binding assumption; it does not establish that every bare invocation fails.
- My ScaleDown compatibility discussion omitted two consequential differences: only `state.text`/`state.document` are read, and usage sums the internal question calls. [ScaleDown Decisions contract](https://docs.scaledown.ai/api-reference/decisions-overview) A future adapter must serialize the full canonical state into `state.text` and budget accordingly.
- Add precise limits: Jev 1.14 defaults to 64k tokens for state plus all questions and 32k for state plus any one question; 262k is an explicit long-context opt-in, not the default. [Jev model limits](https://docs.typesafe.ai/models)
- Laya's English 512-token budget includes the question and options; neither 512 nor "about 320" is a universal state allowance, because its encoder computes remaining room per question and can truncate state. [Laya encoder](https://github.com/NandhaKishorM/laya/blob/main/laya/common.py) Admission must inspect actual tokenization and reject lost required evidence.

These are source-level findings. I have not demonstrated a successful live superloop or measured an advantage over rules.
