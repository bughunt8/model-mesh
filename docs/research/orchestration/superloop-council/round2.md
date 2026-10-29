# Round 2: rebuttal

Read all five round 1 reports and the Practical's CDM addendum in /home/user/workspace/s1-council/ (files round1-*.md). Stay in your persona. Write at most 1,500 words to /home/user/workspace/s1-council/round2-<your file name> and send the full text to the parent as your final message. Do not edit other files.

## Answer in this order

1. The strongest point another member made that you now accept and that changes your recommendation. Name the member's persona.
2. Up to three claims by other members you reject, with evidence you re-verified.
3. Your position on each disputed question below, one or two sentences each, with a concrete value where one is asked.
4. Any factual correction to your own round 1 report.

## Disputed questions

D1. Loop ownership. Should the outer driver own continuation and disable omo's internal loops (Goal, todo continuation, boulder) for each worker call, or should the worker call be `bunx oh-my-openagent run`, which only exits when omo's internal loops are idle? Which command line goes in the PR?
D2. omo target. Stay on pinned v4.19.4 OpenCode edition, or support the 5.x line? Members disagree on whether `goal.default_max_iterations` is enforced: the Researcher reports a default cap of 100 on dev, while the First-Principle and Explainer report that the 5.x/dev Goal hook does not enforce it. Re-verify and say which is true for which version.
D3. Decision seat family. Once a decision model can dispatch or gate, does it inherit the orchestrator family rule (no overlap with any author, reviewer or aggregator family across all rungs and across the run's whole lineage)? How are open-weight deciders fine-tuned from Qwen or Gemma treated? Is a log-only shadow seat exempt?
D4. Profile choice. Is the profile (b4b, hybrid, ultimate, global) a model decision, an owner policy, or an owner-approved escalation ladder the model may only request? What about the First-Principle's point that switching profile mid-run can put a reviewer on its own family's earlier work?
D5. Done authority. May a decision model ever vote on completion? Options: never asked; asked only as an advisory smoke detector that can trigger early review but never end the loop; or a third gate after deterministic checks and independent review.
D6. Thresholds. Point thresholds such as 0.80 or 0.95 as shadow starting points, or a Learn-then-Test style calibration procedure before any activation? Note that Jev Choice confidence, ScaleDown Choice confidence and Noul probability are different quantities.
D7. Default caps for the pilot: maximum outer iterations, wall clock, no-progress streak, fix-verify cycles. Give one number each. Round 1 proposals ranged from 5 to 100 iterations.
D8. Validator. Add decision-seat rules (O19 and up) in this PR, or wait until a seat is adopted?
D9. CDMs in this PR. Include a ScaleDown backend, an offset-verified Extract state builder, both, or neither? Summarize and Compress anywhere?
D10. "Endless". Is there any defensible reading of the owner's "endless loop to achieve the goal"? If so, state it in one sentence the owner could sign.
D11. Overall verdict on the hypothesis: disproved in all six patterns, or disproved in some and holding for the orchestrator seat itself?

## Facts in dispute (re-verify, do not repeat)

- TypeSafe retention: "no published retention policy" (Practical, Adversarial) versus "DPA with retention terms and enterprise zero retention" (First-Principle, Explainer, Researcher).
- madewithjev.com: vendor guide (Practical) versus independent and unaffiliated (Explainer, Researcher).
- ScaleDown /v1/scaledown reads only state.text and state.document, and bills the sum of internal calls (Adversarial, Researcher).
- Jev 1.14 limits (64k per request, 32k per question) and Laya state budget (about 320 versus 512 tokens).
- Whether `opencode run --agent` resolves omo agent names correctly, given the omo CLI warning about exact-key lookup.
