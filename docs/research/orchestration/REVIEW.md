# Independent review record

Status: two review rounds finished. Round 1 returned DO NOT SHIP. Round 2 returned SHIP WITH FIXES, and every round 2 finding was then fixed. There was no third round, so those last fixes carry only the CI mutation tests as evidence.

## Who reviewed

Grok 4.7 reviewed as an independent subagent. The author of the package was Claude Sonnet 5.5, so the model family differs. The council that supplied design input was Claude Opus 5.5, GPT 6.1 Sol, Kimi K3 and GLM 5.3, so the reviewer was not on the council either. The reviewer ran inside the same Perplexity Computer harness as the author, so independence holds for the model family only, not for the harness. Nobody has run the work in a second harness.

Raw reports: [round 1](review-round-1-grok.md) on commit 7e6972b and [round 2](review-round-2-grok.md) on commit c96cb85.

## Round 1 findings and what changed

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| B1 | Blocker | Independence, Hong Kong and hephaestus rules trusted hand-written family labels | Fixed. Families come from the model name. A label that disagrees fails. Same ID under another family label fails. |
| B2 | Blocker | `absolute_exception` with any reason silenced the rule | Fixed. The key is rejected outright. |
| B3 | Blocker | An empty reviewer list or chain skipped the independence check | Fixed. A reviewer and a non-empty chain are required. |
| M1 | Major | Cap policy followed the placeholder suffix, and hybrid cells used the flagship coder in generalist slots | Fixed. The validator checks price references and exact slots. The matrix now uses cap-safe rungs. |
| M2 | Major | Pi without isolation, Aider as orchestrator, a missing hephaestus, a cloned third option | Fixed. Each is a validator rule with a mutation test. |
| M3 | Major | The open-source alternate still ran omo as orchestrator | Fixed. Non-primary options replace omo orchestration, and the validator enforces it. |
| M4 | Major | Council ticks and one attribution did not match the raw reports | Fixed. Every tick was rechecked and several were removed. |
| M5 | Major | The harness-name allowlist hid vendor words that followed it | Fixed for hyphen, slash, dot and punctuation continuations. |
| m1 to m4 | Minor | Wrong self-test count, an overstated DSH claim, unlabelled index figures, narrow claim and key checks | Fixed. |

## Round 2 findings and what changed

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| N1 | Major | The orchestrator seat could borrow the coding-tier cap exemption | Fixed. Only author seats get an exemption. Mutation test added. |
| N2 | Major | A situation-level role list contradicted the option role lists | Fixed. The situation field is removed and the validator rejects it. |
| N3 | Major | A model name that wrapped a blocked vendor name passed in ultimate | Fixed. Mixed or blocked name markers fail. Mutation test added. |
| N4 | Minor | The allowlist still hid a vendor word after a colon, comma or semicolon | Fixed. Only whitespace or punctuation followed by whitespace may follow a harness name. Four must-fail strings added. |
| N5 | Minor | Three synthesis statements did not match the council reports | Fixed. |
| N6 | Minor | The harness example check ignored nested keys | Fixed for the keys the cited pages list. It is a fixed list copied from the pages, not a live comparison. |

## What the review did not cover

- No harness was installed or run. Every harness example matches documentation only, and the reviewer fetched pages for a sample.
- Model availability and prices change. The reference prices in [PRICE-REFERENCE.md](PRICE-REFERENCE.md) are a 2026-10-11 snapshot.
- The scorer in `scripts/landscape` was not extended to `global`, so the new profile has an evidence sheet and no score.
- The base `hybrid` profile still maps its implementer seat to a model above the cap, and the base `ultimate` and `hybrid` profiles still give `momus` the same model as `hephaestus`. The matrix works around both. The base profiles are unchanged.
- omo licence terms are accepted by the owner for internal use only. Client or commercial use needs a separate check.
