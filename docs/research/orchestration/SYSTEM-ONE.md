# System One decision models: why they are not in the matrix

Date: 2026-10-28. Status: assessment note. No System One model is in the matrix, the profiles or the validator, and no row has been run with one. This note records why, where one could fit later, and what a pilot would have to show first. All claims about speed, cost and accuracy below are the vendors' or one outside author's, and are unmeasured for model-mesh.

## What they are

A System One model takes a state and a set of typed questions and returns typed answers with probabilities, not text. The three question types are choice, score and noul (a yes or no probability). It accepts text only, and it does not write replies, produce code or explain its reasoning ([TypeSafe docs](https://docs.typesafe.ai/concepts/system-one)). Jev from TypeSafe AI is the first and the commercial one. The vendor says it launched on 2026-09-15 in early access, supports choices of up to 255 options, and quotes 70 to 500 ms responses and $0.042 per million input tokens with free output ([TypeSafe launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev)). The vendor's own post says the service is based on the US West Coast and does not state a retention policy.

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

1. Run it in shadow only. It answers, the existing process acts, and disagreements are logged. The vendor's own integration guide recommends the same sequence ([Jev multi-agent guide](https://madewithjev.com/jev-multi-agent)).
2. Label a set of model-mesh decisions with the answer a person would give: situation routing, finding triage and severity. Use the seeded-defect protocol in [SEEDED-DEFECTS.md](SEEDED-DEFECTS.md) as the template and extend [score-review.py](../../../scripts/score-review.py) to score a decision arm.
3. Set pass conditions before the run. A reasonable starting condition, which is a judgement and not a measured threshold, is that no seeded blocker is suppressed or downgraded and that its calibration holds on model-mesh's own labels and not only the vendor's.
4. Check reachability from Hong Kong, retention terms, the early-access limits and the licence of any open weights, and record the results in this file.
5. Test an adversarial case: a finding whose evidence text tries to talk the decision model into a low score.

## What would change this assessment

Evidence from a run on model-mesh's own labels, a published retention and region policy, or a licensed open-weight model with a stated training method would each justify adding a decision seat and the validator rules that go with it. A vendor claim alone would not.
