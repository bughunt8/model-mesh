# Round 2 rebuttal: The Practical (GLM 5.3)

Every disputed fact below was re-fetched this round, not carried over. Verdicts first, positions after.

## 1. Strongest point I accept

The Researcher's calibration audit. I fetched the paper myself: a point-estimate threshold gate broke its promised accuracy in 147 of 190 exchangeable evaluations, Learn-then-Test kept the promise in all 190, and a gate calibrated in English kept a 95 percent promise in only 8 of 51 locales ([arxiv 2610.36311](https://arxiv.org/html/2610.36311v1)). That kills my round 1 thresholds as anything more than placeholders, and it kills the Adversarial's and First-Principle's numbers too. It changes my recommendation: the PR's decision log gains a promise-target field, thresholds are recorded as uncalibrated until a calibration artifact exists, and activation requires Learn-then-Test or a Beta lower bound on model-mesh's own labels. I also accept the Explainer's authority rule as stated: System One alone may never declare done; the `goal_complete` question becomes an advisory smoke detector that triggers early independent review, never a stop condition. I retract my round 1 stop rule "stop requires P >= 0.8 on goal_complete."

## 2. Claims I reject

**The Adversarial's claim that hosted ScaleDown is "barred from ultimate (Rules D46, O6)."** D46 is misapplied. The repo's own note says: "Under the open-source rule in D46, which covers harnesses and the verification stack and not inference models, a closed hosted model is not excluded for being closed. It is excluded for now for lack of evidence on reach and data handling" ([SYSTEM-ONE.md](https://github.com/bughunt8/model-mesh/blob/orchestration/egm-lenses-and-gates/docs/research/orchestration/SYSTEM-ONE.md)). ScaleDown is out of ultimate for missing Hong Kong reach and data-handling evidence, same as Jev. Citing D46 hands the owner a rule that does not exist.

**The Researcher's claim that on dev the Goal has "a default continuation cap of 100."** The v5.1.48 features doc says the opposite: "`default_max_iterations` (1-1000, default `100`) is retained on the `goal` schema for Ralph Loop config migration; the Goal hook doesn't enforce an iteration cap" ([omo v5.1.48](https://github.com/code-yeongyu/oh-my-openagent/blob/v5.1.48/docs/reference/features.md)). The First-Principle and Explainer are right. This resolves D2.

**The Adversarial's Laya "<=512-token numeric states."** The model card says the English model's state is about 320 tokens (512 is the total context, `head_max_len = 192`), and the multilingual default is about 768 ([Laya card](https://huggingface.co/convaiinnovations/laya)). The Explainer's 320 is the correct number for the English checkpoint.

## 3. Disputed questions

**D1. Loop ownership.** Outer driver owns continuation, and the command is `bunx oh-my-openagent run --agent sisyphus --json --directory <worktree> --session-id <id> "<prompt>"` with goal, boulder and todo continuation disabled in that run's config. The CLI doc itself warns that `opencode run --agent` "does exact-key lookup in the host" and prefers `oh-my-openagent run` ([omo CLI](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/cli.md)), so the Explainer's invocation is right and the harness example needs that fix. Using the omo command while disabling its hooks collapses the two positions in D1 into one command line.

**D2. omo target.** Pin v4.19.4 for the pilot: it is what the repo pins, its agent names match the matrix, and its doc calls `default_max_iterations` "the continuation iteration cap" with default 100 ([omo v4.19.4](https://github.com/code-yeongyu/oh-my-openagent/blob/v4.19.4/docs/reference/features.md)). On 5.x the cap is not enforced by the Goal hook (verified above), so any future migration makes the driver's own cap mandatory, not optional. Both claims in the dispute were true for their versions; the Researcher's is wrong for 5.x.

**D3. Decision seat family.** Yes: once a decision model can dispatch or gate, it inherits the orchestrator family rule across all rungs and the run's whole lineage. Open-weight deciders take their base model's family: a Qwen-derived decider is alibaba and collides with author and reviewer chains on most rows; a Gemma-derived one is google, which O4 blocks outright. A log-only shadow seat is exempt from family rules because it decides nothing, but it still logs provider, pinned version and base family, and undisclosed lineage is a failure, not a pass.

**D4. Profile choice.** Owner policy, full stop. The model may request an escalation but never execute one; the profile is frozen at admission. The First-Principle's profile-switch trap is real and I checked it in the matrix: A01 ultimate puts DeepSeek in author seats while A01 hybrid puts DeepSeek in reviewer seats, so a mid-run switch can put a reviewer family on its own earlier work. Freeze the profile for the pilot; a provenance ledger is the later fix.

**D5. Done authority.** Advisory smoke detector only. The model's "done" vote triggers early independent review and nothing else. Done is deterministic checks green plus cross-family review plus the owner's merge gate. My round 1 formulation was too generous and I retract it.

**D6. Thresholds.** Point numbers are placeholders recorded as uncalibrated. Activation requires a calibration procedure on model-mesh's own labels, Learn-then-Test style with a stated delta, or the Beta lower bound where a formal guarantee is not needed ([arxiv 2610.36311](https://arxiv.org/html/2610.36311v1)). Jev Choice confidence, ScaleDown Classify confidence and Noul probability are different quantities and do not transfer across backends; recalibrate per backend. Minimum 100 labelled decisions, including Chinese and Cantonese traffic, before any activation.

**D7. Default caps.** One number each: 12 outer iterations, 30 minutes wall clock, no-progress streak of 2 consecutive iterations, 3 fix-verify cycles (already the mm-loop hard bound). Twelve is enough to clear three fix-verify cycles plus review rounds without a 100-iteration bill; 100 was a v4.19.4 config default, not a pilot budget.

**D8. Validator.** One minimal rule now, the rest later. If the PR ships a superloop config file, O19 checks config hygiene only: finite caps, pinned decision model IDs, decider never sole done authority. Seat-family rules wait until a seat is adopted. This is a small move from my round 1 "nothing yet," driven by the First-Principle's framing: add runtime-policy tests without weakening O1 to O18.

**D9. CDMs in this PR.** Neither ScaleDown backend nor the Extract state builder ships in PR 1. The local XGrammar fallback from my addendum stays. ScaleDown is out for now on facts I re-verified: `/v1/scaledown` reads only `state.text` and `state.document`, runs each question as a separate classify call, and reports usage as the sum of every internal call's tokens, so costs multiply by question count ([ScaleDown docs](https://docs.scaledown.ai/api-reference/decisions-overview)). The state builder ships as an interface with the offset check (`raw[start:end] == span`) so a local extractor or ScaleDown can be added later without redesign. Summarize and Compress: nowhere in the decision path, ever.

**D10. "Endless."** One sentence the owner could sign: "The loop runs unattended until the goal is verified done, a cap fires, or it hands back blocked, whichever comes first; unbounded in intent, bounded in budget."

**D11. Overall verdict.** Disproved in all six patterns: every pattern contains a bounded typed decision, so "no place" is false. The hypothesis holds only for the orchestrator seat itself in orchestrator-workers and the planner role in autonomous agents, because Jev cannot write plans. The user wins the argument and still loses the proposal.

## 4. Corrections to my round 1

1. I called madewithjev.com "the vendor's own integration guide." Wrong: the page states "Made with Jev is independent and not affiliated with TypeSafe AI" ([madewithjev](https://madewithjev.com/jev-multi-agent)). Its content stands as an independent third-party guide, and the PR should fix the same mislabel in SYSTEM-ONE.md.
2. I wrote TypeSafe has "no published retention policy." Wrong at the docs level: the legal page publishes a DPA "including data retention" and a no-training commitment ([TypeSafe legal](https://docs.typesafe.ai/legal)). What remains open is the default retention period and zero-retention scope, which look like enterprise arrangements, not defaults.
3. My stop rule "P >= 0.8 on goal_complete ends the loop" is retracted per D5.
4. My "max iterations 100, matches omo" is true only for v4.19.4; on 5.x the Goal hook does not enforce the cap.
5. My invocation `opencode run "<task>"` follows the repo's harness example, but the omo CLI warns exact-key lookup can fail for omo agent names; the PR uses `bunx oh-my-openagent run` per D1.

Verified in passing: Jev 1.14 limits are 64k per request and 32k per question, with the state counting toward both, and aliases that move on release ([TypeSafe models](https://docs.typesafe.ai/models)). The Explainer's and First-Principle's numbers were right; the driver's state digest must be built against the 32k per-question budget.
