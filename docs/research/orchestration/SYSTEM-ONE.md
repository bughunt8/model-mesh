# System One decision models: why they are not in the matrix

Date: 2026-10-28, updated 2026-10-29. Status: assessment note. No System One model is in the matrix, the profiles or the validator, and no row has been run with one. This note records why, where one could fit later, and what a pilot would have to show first. All claims about speed, cost and accuracy below are the vendors' or outside authors', and are unmeasured for model-mesh.

The 2026-10-29 update corrects two errors in the first version, adds the limits, the confidence definitions and the other decision models found since, and records the outcome of a five-model council on using a decision model at the core of a superloop. The superloop design that came out of it is in [SUPERLOOP.md](../../SUPERLOOP.md).

## What they are

A System One model takes a state and a set of typed questions and returns typed answers with probabilities, not text. The three question types are choice, score and noul (a yes or no probability). It accepts text only, and it does not write replies, produce code or explain its reasoning ([TypeSafe docs](https://docs.typesafe.ai/concepts/system-one)). Jev from TypeSafe AI is the first and the commercial one. The vendor says it launched on 2026-09-15 in early access, supports choices of up to 255 options, and quotes 70 to 500 ms responses and $0.042 per million input tokens with free output ([TypeSafe launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev)). The vendor's own post says the service is based on the US West Coast. Correction: the first version said no retention policy was stated. The help centre says Jev is not trained on customer requests or responses, and that retention "depend[s] on the data involved, applicable agreements and legal requirements, and any agreed Zero Data Retention (ZDR) arrangement", with no fixed period ([TypeSafe help: data use](https://help.typesafe.ai/articles/5974925716-how-is-submitted-data-used-or-retained)). ZDR "is available by request to enterprise customers" ([TypeSafe help: ZDR](https://help.typesafe.ai/articles/9520184411-do-you-offer-zdr)).

Open or self-hostable options exist. [stephenlb/system-one-model](https://github.com/stephenlb/system-one-model) is built on a 12B open-weight base and runs locally. Its README reports a 39-case hand-written comparison and states no licence and no training method. A listing at [systemonemodels.org](https://systemonemodels.org/guides/jev-alternatives/) describes hosted alternatives post-trained from another open base. I did not verify those.

## Why it is absent

1. It was not assessed. The orchestration work (PR #4) and the review panel work (PR #6) did not consider decision models. This note is the first look. The absence is an omission and not a finding against them.
2. It does not fit any seat the matrix defines. Every seat in the matrix is an author, orchestrator, reviewer or aggregator that writes code or prose. A System One model cannot write code or explain a finding, so it cannot be an author, an orchestrator or a reviewer. Reviews also need a claim with evidence, which the finding schema requires as text.
3. The validator has no place for it. Model families are derived from model names, and rules O5 and O16 reason about harness and family overlap between seats that generate text. A decision seat needs its own rules before it can be added.
4. The evidence is thin and mostly from the vendor. The vendor's workflow comparisons score Jev against the probabilities of large reference models, not against ground-truth labels. The vendor also says the evaluations were built by its own team, so bias is possible, and that its simplified demo flatters it ([TypeSafe launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev)). The one outside study I found is an [independent exploratory paper](https://arxiv.org/html/2609.28940v1) with one target, one run per condition and a changed harness for its second test. With Jev, 9 of 13 seeded vulnerabilities were hit, against 10 of 13 without it. The paper's own limits section says calibration transfer is unestablished, that the layer can suppress real findings through low confidence, and that adversarial inputs are untested.
5. Reachability is unverified. The ultimate profile only admits models marked Hong Kong eligible. A US-hosted early-access API has no such mark, and nothing here shows it is reachable or allowed. Under the open-source rule in D46, which covers harnesses and the verification stack and not inference models, a closed hosted model is not excluded for being closed. It is excluded for now for lack of evidence on reach and data handling.

## Where one could fit

None of these are adopted. Each is a decision about a narrow question that code or a person already makes.

| Candidate seat | Question it would answer | Today |
|---|---|---|
| Situation router | Which situation row applies, and does the triviality gate apply | The orchestrator and the method's gate |
| Finding triage | Is a clustered finding confirmed, needs review or rejected, and what is its severity | The aggregator seat and a person |
| Tool and action gate | Does this action need a person's approval | Authorization rules in A10 and A11 |

If any of these is piloted, three rules from the outside paper's design apply. The model may lower confidence, flag for review or prune a candidate list. It may not override a deterministic validator or restore a rejected finding. It may not clear a blocker raised by a cross-family reviewer. It never replaces a reviewer from another harness and family. That last point matters because a calibrated probability still comes from one model, and the paper notes that a false negative can leave results worse than running without the layer.

## What a pilot would have to show first

1. Run it in shadow only. It answers, the existing process acts, and disagreements are logged. An integration guide recommends the same sequence ([Made with Jev multi-agent guide](https://madewithjev.com/jev-multi-agent)). Correction: the first version called this the vendor's guide. The site states it "is independent and not affiliated with TypeSafe AI", and it lists sponsors.
2. Label a set of model-mesh decisions with the answer a person would give: situation routing, finding triage and severity. Use the seeded-defect protocol in [SEEDED-DEFECTS.md](SEEDED-DEFECTS.md) as the template and extend [score-review.py](../../../scripts/score-review.py) to score a decision arm.
3. Set pass conditions before the run. A reasonable starting condition, which is a judgement and not a measured threshold, is that no seeded blocker is suppressed or downgraded and that its calibration holds on model-mesh's own labels and not only the vendor's.
4. Check reachability from Hong Kong, retention terms, the early-access limits and the licence of any open weights, and record the results in this file.
5. Test an adversarial case: a finding whose evidence text tries to talk the decision model into a low score.

## What would change this assessment

Evidence from a run on model-mesh's own labels, a published retention and region policy, or a licensed open-weight model with a stated training method would each justify adding a decision seat and the validator rules that go with it. A vendor claim alone would not.

## Update 2026-10-29: limits and definitions that matter

- Model IDs are `jev-1.14.0` and `jev-1.13.0`. The aliases `jev-latest` and `jev-preview` move when a release ships, "so their answers can change without any change to your code", so a pilot pins a version. Default limits are 64k tokens per request and 32k per question, or 262k with a long-context header ([TypeSafe models](https://docs.typesafe.ai/models)).
- "Confidence" is not the top probability. For a choice with n options it is \((p_{max} - 1/n)/(1 - 1/n)\). A score has its own formula, and a noul answer has no confidence field, only the probability of yes ([TypeSafe confidence](https://docs.typesafe.ai/confidence.md)). A threshold copied from one vendor means something different on another, so the superloop logs raw probabilities and computes its own figures.
- A point threshold is not a guarantee. An audit of Jev 1.13 and five Laya checkpoints found that point-chosen thresholds broke their promise in 147 of 190 evaluations, while learn-then-test held in all 190. A gate calibrated in English held a 95 percent accuracy promise in 8 of 51 locales ([Brom, Confidence Is Not a Promise](https://arxiv.org/html/2610.36311v1)). For a Hong Kong owner, qualification has to be per locale.

## Other decision models

| Model | What it is | What matters here |
|---|---|---|
| Laya | Open weights under Apache 2.0, built on a ModernBERT-large encoder, about 421M parameters ([Hugging Face](https://huggingface.co/convaiinnovations/laya)) | The English checkpoint has 512 tokens of context with about 320 for state, and the typed-decisions checkpoint about 768. The card says the shipped checkpoints "ship over-confident" and need temperatures refitted on your own data. Its server binds to all interfaces with no authentication unless `LAYA_API_KEY` is set |
| ScaleDown decisions | A hosted endpoint with a Jev-shaped request ([ScaleDown decisions overview](https://docs.scaledown.ai/api-reference/decisions-overview)) | Only `state.text` and `state.document` are read, so structured state must be sent as text. Reported usage is the sum of internal calls. No reasoning field is returned. Its choice confidence is "the chosen option's probability" ([ScaleDown decisions API](https://docs.scaledown.ai/api-reference/decisions)), which is not Jev's quantity |
| stephenlb/system-one-model | Local, 12B open-weight base | No licence or training method stated, as in the first version |

ScaleDown also sells extraction, summarization and compression models. Its extraction page describes span offsets as character offsets in one place and as byte positions in another, and caps each scalar field at 30 values ([ScaleDown extract](https://docs.scaledown.ai/api-reference/extract)). The superloop therefore admits a span only after checking the text at the stated offsets of the original file, in either unit, and never admits a summary or compressed context into a decision state.

[LangChain's post on long-running agents with ScaleDown](https://www.langchain.com/blog/building-long-running-agents-with-scaledown-and-deep-agents) uses a classifier as a drift breaker: stop the agent when the top label is not "progressing" and its score is above 0.8. That is the brake-only use the superloop allows. The 0.8 is the post's choice, not a qualified threshold, and the post's speed and cost comparisons are the vendor's.

## Constrained decoding

[Chavan's paper on constrained decoding](https://arxiv.org/html/2609.23742) tested five small models on 14 tasks, 210 evaluations. Grammar-constrained decoding raised schema validity to 100 percent for all five, but a semantic gap remained. In one case a 1B model scored 1.000 on a multi-call task while the email body it wrote was "1. 2. 3. 4. 5.". For model-mesh this means schema validity is a format check, not a correctness check, whether the typed answer comes from a decision model or a constrained generator. The superloop checks every answer's meaning in code and never lets one replace an acceptance check.

## Council outcome, 2026-10-29

Five members on five model families debated whether a decision model has a place in the six agentic patterns and whether it should be the core of an endless omo superloop. The record is in [SUPERLOOP-COUNCIL.md](SUPERLOOP-COUNCIL.md). In short:

- The claim that a decision model has no place in the six patterns is false. Every pattern has a bounded fork it can answer, and routing is the clearest fit. The claim holds only for the planner seat.
- "Core orchestrator" can only mean the control plane asks it at each fork. Planning stays with a generating model, and the loop belongs to code.
- "Endless" was rejected. What the owner can sign is a standing service whose every goal ends on verified evidence, a cap or a hand-back.
- A decision model may brake and may never declare success.
- Once a decision seat can act, it takes the orchestrator's family rule across the whole lineage, and an undisclosed lineage blocks it. Jev's base lineage is undisclosed, so Jev can run in shadow mode only. One member argued a brake-only seat should be exempt; that is recorded as a dissent.

The matrix still has no decision seat. What changed is that the superloop can now collect the labelled shadow log a pilot needs.
