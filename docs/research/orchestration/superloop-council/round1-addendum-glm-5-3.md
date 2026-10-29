# Round 1 addendum: CDMs and constrained decoding (The Practical, GLM 5.3)

Verified against the [arxiv paper](https://arxiv.org/html/2609.23742) and the [LangChain post](https://www.langchain.com/blog/building-long-running-agents-with-scaledown-and-deep-agents). Two different things share the name "CDM," and the addendum's framing is correct: the paper studies grammar-constrained decoding of ordinary small LLMs, and ScaleDown sells task-specific models. Keep them apart or the debate turns to mush.

## Where they fit

The paper's constrained decoding is a technique, not a model. It takes my round 1 fallback, "an LLM constrained to typed output," from hypothesis to evidenced: XGrammar made all five models 100 percent schema-valid, at 4 to 8 ms schema compile and 1.6 to 3.7 percent throughput cost ([arxiv](https://arxiv.org/html/2609.23742)). That is cheap enough to run anywhere, including inside the driver's offline test path, and it satisfies the open-source rule D46 outright: open tools, open weights, no vendor.

ScaleDown's product line maps to the six patterns as follows. Classify scores text against caller-defined labels with a probability each, which is the routing pattern's classifier, the same seat I gave Jev. Extract pulls fields with confidence and character offsets into the source, which feeds prompt chaining and evaluator-optimizer inputs. Summarize and Compress cut context, which is state preparation for parallelization and for the superloop. The drift detector in the LangChain post is the piece I care about most: classify the conversation after each model call and stop the run when the top label is not "progressing" above a threshold. That is a vendor implementation of the no-progress stop I demanded in round 1, sitting in the autonomous agents pattern where the article puts checkpoints and stopping conditions.

## What they add beyond System One

Three things Jev cannot do. Span extraction with character offsets is auditable: the driver can check the span against the source text, which makes Extract the safest of the four. Query-aware compression and summarization build state that Jev's text-only input needs, and the 1M-token input ceiling dwarfs anything in my round 1 design. Classify returns a reason alongside the probability, which is debuggable in a way a bare noul is not. And the paper's CD path gives a fully local, self-hosted typed-output option with no vendor dependency at all, which Jev has never had.

## What they risk

The paper's own finding is the headline risk, and it applies to Jev, to ScaleDown, and to every typed decision model in my round 1 plan: schema validity is structure, not meaning. The paper's hollow rescue case is the example to keep: Llama-1B under XGrammar scored 1.000, both calls present, all parameters present, while the email body read "1. 2. 3. 4. 5." A green schema check masked garbage ([arxiv](https://arxiv.org/html/2609.23742)). Second, Summarize and Compress write text, which puts a generating model inside the decision path, and a summary cannot be checked against its source the way an offset can. That is an injection surface. Third, plain constrained decoding under greedy decoding gives no calibrated probability, so thresholds read off token log-probabilities are weak; the paper does no calibration analysis. Fourth, every ScaleDown speed and cost number is a vendor claim, and reach, retention, licence and regions are unstated in what I read, the same gap that keeps Jev out of the ultimate profile.

## How this changes the PR

My round 1 recommendation survives. Shadow first, one fork, stop rules in code, no endless loop, no production seat. Three concrete amendments:

1. The driver's checks must not stop at the schema. The paper's line, "CD's reach ends exactly where schema conformance ends," becomes a rule in `scripts/superloop.py`: every typed answer gets a deterministic semantic check before it is honored. A `goal_complete` answer requires the done evidence to exist in the ledger. A chosen option must exist in the current state. The decision log gains a semantic-check column, and the pilot pass condition adds "no schema-valid but semantically wrong answer honored."
2. The `--decision-backend stub` option gains a `local` sibling: a small model constrained with XGrammar, evidenced by this paper as the open-source fallback. Still shadow-first. This strengthens D46 compliance without touching any profile.
3. The no-progress stop gets a second implementation: classify each iteration's ledger delta as progressing, stuck or regressing, and treat "not progressing" as a stop signal. My in-code detector (todo count unchanged two iterations) stays as the fallback that needs no vendor.

One non-change worth stating plainly: two typed-decision vendors now exist, which makes cross-vendor decision voting possible for consequential gates, in the spirit of the independence rule. Every accuracy number involved is a vendor claim, and none of it enters this PR. Cross-vendor voting is a follow-up only if the single-vendor pilot produces labels worth voting on.

## Bottom line

Constrained decoding is the cheapest, most open piece of this whole debate, and the paper hands us the lesson for free: structure is solved, meaning is not. So the driver checks meaning in code, the pilot runs in shadow, and nothing I said in round 1 gets bigger. It gets one more mandatory check.
