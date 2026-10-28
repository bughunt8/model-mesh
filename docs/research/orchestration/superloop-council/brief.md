# Council brief: System One decision models at the core of an omo superloop

Date: 2026-10-28, Asia/Hong_Kong. Owner: Ron Ng, Hong Kong. Repo: github.com/bughunt8/model-mesh (MIT). Local checkout: /home/user/workspace/open-model-method on branch orchestration/egm-lenses-and-gates (open PR #6). Read-only for you: do not edit, commit or push anything in that checkout.

## The user's request (verbatim)

"Hypothesis - there is no place for JEV or System One in the 6 Agentic flows (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, and autonomous agents) described by Anthropic blog article: https://www.anthropic.com/research/building-effective-agents

Disprove this.

Research the types of superloop using the 6 Agentic workflows and in the content of OMO, propose using JEV or System One as the core orchestrator whilst using OMO profiles in an endless loop to achieve the goal. Debate this with model council (The First-Principle: Strips complexity. Questions core assumptions. Builds arguments from foundational truths. The Adversarial: Aggressive challenger. Stress-tests every claim. Actively hunts for logical flaws; The Explainer: Simplifies data. Uses clear analogies. Bridges complex research to the audience; The Practical: Focuses on execution. Rejects over-intellectualizing. Demands realistic, achievable results; The Researcher: Fact-skeptic. Re-verifies everything. Rejects surface data to find hidden flaws.) Then give me a recommendation for a PR to improve the model-mesh method and skills and templates - AND scripts that will be used to link and drive OMO profiles using System One at the core."

## Terms

- JEV / Jev: TypeSafe AI's System One model. A System One model takes a `state` and typed `questions` (choice, score, noul = yes/no probability) and returns typed answers with probabilities, no generated text. Start at https://docs.typesafe.ai/concepts/system-one and https://typesafe.ai/blog/introducing-system-one-models-and-jev. Open alternatives exist (for example https://github.com/stephenlb/system-one-model, the Laya project discussed in https://arxiv.org/html/2609.28940v1, and the listing at https://systemonemodels.org/guides/jev-alternatives/). Verify everything yourself.
- OMO / omo: oh-my-openagent (formerly oh-my-opencode), the OpenCode plugin with agents such as Sisyphus, Hephaestus, Prometheus, Atlas, Oracle, Momus, Metis, Librarian, Explore and categories such as ultrabrain, deep, quick, visual-engineering. It has loop features (for example ultrawork, a Ralph-style loop, todo continuation, boulder or plan continuation). Verify the current names and behavior in its repository and docs yourself; do not trust this list.
- OMO profiles in model-mesh: `profiles/ultimate.json`, `hybrid.json`, `b4b.json`, `global.json` and their `.example.json` twins with real model IDs. ultimate = best quality but Hong Kong reachable and policy eligible only; hybrid = default with a cost cap; b4b = best bang for buck with a hard cap; global = unrestricted twin of ultimate.
- Superloop: the user's word for an outer loop that keeps re-invoking agents until a goal is met, such as the "Ralph Wiggum" loop popularised by Geoffrey Huntley. Research what loop types exist and map them to the six Anthropic patterns.

## Repo context you must read first

- docs/ORCHESTRATION.md (profiles, situations A01 to A12, patterns P1 to P5, independence rule, omo exception)
- docs/research/orchestration/MATRIX.md (generated matrix)
- docs/REVIEW-PANEL.md (zero-context reviewers, lenses, aggregator, gates)
- docs/research/orchestration/SYSTEM-ONE.md (the current note saying why no System One model is in the matrix)
- skills/mm-loop/SKILL.md, skills/mm-method/SKILL.md, skills/mm-verify/SKILL.md
- examples/orchestration/harnesses/opencode-omo.example.json, profiles/*.example.json
- scripts/validate-orchestration.py (rules O1 to O18)

## Owner's standing rules (apply them)

1. Independence: for coding or generation, an adversarial review never uses the author's own harness and model; reviewer harness and model family differ from every author and from the orchestrator. Orchestration and review seats stay separate from workers where possible.
2. Evidence over assertion: affinity, speed, cost and accuracy claims are unmeasured unless independently evidenced. Label vendor claims as vendor claims. Council output is a proposal, not a result.
3. Open-source rule (decision D46): harnesses and the verification stack must be open source; inference models need not be.
4. Hong Kong reach: the ultimate profile admits only models marked Hong Kong reachable and policy eligible.
5. Style: no em dashes, straight quotes, sentence-case headings, no filler.

## What each member must produce

1. Hypothesis test, per pattern. For each of the six patterns, quote the article's own wording, say whether a System One model has a place, exactly which decision it would make (question type, options, thresholds), and what it cannot do there. Give a verdict: hypothesis disproved, partly disproved, or holds, per pattern and overall.
2. Superloop taxonomy. Name the loop types you can evidence (with links), including the omo ones, and map each to the six patterns. Say which loop decisions are bounded typed questions and which need generated text.
3. The proposal. Assess "System One as the core orchestrator, omo profiles as the workers, endless loop until the goal". Be precise about what "core orchestrator" can mean when the model cannot write plans: control plane versus planner. Cover stopping, budgets, safety, human gates, the independence rule, failure modes (false negatives, adversarial state, calibration drift, outage), Hong Kong reach and data handling, and fallbacks (open-weight System One, an LLM constrained to typed output, plain rules).
4. PR recommendation. Concrete files to add or change in model-mesh: method docs, skills, templates and scripts. For scripts, give the interfaces: inputs, outputs, how the driver invokes omo or OpenCode non-interactively per profile, what state it sends to the decision model, the exact typed questions, the thresholds, the stop rules, the logs, and how it is tested offline without network access. Say what must stay out of scope.
5. Open questions for the owner.

Write your persona's view sharply. Disagree with the user where the evidence says so. Use web search and fetch to verify; cite sources inline as Markdown links. Keep it under about 3,500 words.
