# Independent review of the review panel change

Reviewer: Grok 4.7 as a separate subagent (a different model family from the author). Author model: Claude Sonnet 5.5. Both ran in the same Perplexity Computer harness, so this review is independent by model family only, not by harness. The reviewer's original report follows the disposition table. The fixes were not re-reviewed by that reviewer.

## Disposition

| Finding | Severity | Disposition |
|---|---|---|
| Call budget is not rule O17 | Major | Fixed. O17 now enforces the spread split: primary lens on both seats, every other lens on exactly one seat. Docs say what O17 covers for other tiers |
| Gap clustering false-corroborates | Major | Fixed. A finding joins a cluster only within 3 lines of the first finding's range. Self-test added |
| Category and range misses never reach the model merge | Major | Fixed. `related_clusters` and `needs_model_merge` cover other-category and rangeless-next-to-ranged cases. Docs require the model merge to keep families, severity and corroboration |
| Duplicate ids abort a multi-file merge | Major | Fixed. Ids are prefixed with the input file name. Self-test added |
| Drift check misses the drifts it is for | Major | Partly fixed. Added digit counts, tier and gate table checks (D8), test count and rule range checks (D9), research notes in the link check, nested scripts in the CI check, and D1 now requires a self-test mutation per rule. It still reads text with patterns. The descriptive text of a lens row is not compared |
| Ultimate spread seat has no fallback | Major | Documented under Known limits. No legal fallback exists in the model table |
| Spread aggregator is reviewer 0 where a third family was available | Major | Fixed outside ultimate. Rule O16 now requires the first rung to be a third family where one exists. A05 on hybrid and b4b and all ultimate options have none and are documented |
| Both spread seats are momus | Minor | Fixed. Seat ids added and validated |
| O15 is a string presence check | Minor | Improved. Reviewer seats may carry only the contract keys. Run-time behavior is still untested and the docs say so |
| Primary lens is whatever is first | Minor | Fixed. `primary_lens` is explicit and must equal the first lens |
| qwen-code example is stale | Minor | Fixed. Role binding states the second-seat use and that the pairing is unmeasured |
| EGM-ANALYSIS overstates two facts | Minor | Fixed. Reviewer counts per stage and the benchmark wording are corrected |
| Cluster markdown drops evidence, family case not normalized | Minor | Fixed |
| Also noted: O10, O13 and O14 had no self-test mutation | Found while fixing D1 | Fixed. File-based self-test cases added. O14 now reads the table under the root it is given |

## Original report


Independent review of `orchestration/egm-lenses-and-gates` at `c966d55`, diff `main...HEAD`, checkout `/home/user/workspace/open-model-method`. No repo file was edited. Mutations ran in memory. Drift probes used temp copies. `--render` rewrote `docs/research/orchestration/MATRIX.md` and `git diff` was empty.

Verdict: SHIP WITH FIXES.

The independence checks hold on the committed matrix. The new scripts' self-tests pass and do not cover the holes below. No catch rate is claimed, and that restraint is real. Do not treat the green drift check or the 7-call budget as enforced.

## Checks

Python for the full list was 3.14.3. TESTING.md asks for 3.12. The new self-tests and `check-drift.py` were repeated on 3.12.13 and passed. CI is 3.12.

| Command | Result |
|---|---|
| `python .github/checks.py` | exit 0, all checks passed, including the denylist self-test |
| `python scripts/validate-full-config.py` | exit 0, R1 to R14 passed |
| `python scripts/validate-orchestration.py` | exit 0, all orchestration checks passed |
| `python scripts/validate-orchestration.py --self-test` | exit 0, 63 ok, self-test passed |
| `python scripts/validate-scenarios.py` | exit 0, skill checks passed |
| `python scripts/validate-scenarios.py --self-test` | exit 0, self-test passed |
| `python scripts/aggregate-findings.py` | exit 2, usage text, no input file. CI runs `--self-test`, not the bare command |
| `python scripts/aggregate-findings.py --self-test` | exit 0, self-test passed |
| `python scripts/score-review.py` | exit 2, usage text |
| `python scripts/score-review.py --self-test` | exit 0, self-test passed |
| `python scripts/check-drift.py` | exit 0, `No drift detected` |
| `python scripts/check-drift.py --self-test` | exit 0, self-test passed |
| `python scripts/landscape/landscape_scan.py --self-test` | exit 0, 67 assertions |
| `python scripts/validate-orchestration.py --render` | exit 0, committed `MATRIX.md` unchanged |

Also run, present in `.github/workflows/checks.yml`, absent from the TESTING.md table: landscape YAML and JSON mirrors match under pyyaml 6.0.3, `review_gate.py --self-test` passed 15 cases, golden scan matched. Dropping the review-gate step from a temp copy of the workflow left `check-drift.py` clean.

The 63 self-test count matches TESTING.md. CHANGELOG 1.3.0 says 23 new cases. I counted 23 new labels in the self-test output, from the zero-context drop through the wrong-situation drift gate. Plugin and marketplace versions are 1.3.0, matching the changelog top entry. A scan of the diff found no new vendor model ids outside `*.example.json` and `docs/research/`.

## Mutations

Fourteen violations of independence, lens coverage, aggregator, gate, or cap rules were caught. Two further probes that should still fail, a waiver key plus a real family overlap, and a lens parked only on the aggregator, were also caught.

| Mutation | Caught as |
|---|---|
| A05 hybrid primary, second reviewer harness set to the author harness | O5 |
| A06 hybrid primary, second reviewer chain gains an author rung | O5, including author model id |
| A05 global alternate, second reviewer harness set to the orchestrator harness | O5 |
| A05 hybrid primary, second reviewer fallback gains the other reviewer's family | O17 |
| A06 b4b alternate, `comprehension` removed from both seats | O17 uncovered |
| A05 ultimate primary, aggregator chain gains the orchestrator rung | O16 |
| A06 global primary, aggregator harness set to an author harness | O16 |
| A03 gates swapped | O18 |
| A05 given spec-readiness and drift | O18 |
| `zero-context-review` removed from A06 global alternate only | O15 |
| A05 b4b primary, second reviewer chain set to `ProviderA/flagship-mid` then `ProviderF/vision-xl` | O7 only. Price reference 18, no family overlap, exemption did not leak |
| A02 hybrid primary, aggregator chain set to `ProviderE/coder-xl` | O7 and O16 |
| A01 hybrid primary, a category route gains the aggregator family | O16 and O5 |
| A06 ultimate primary, second reviewer chain replaced with an author placeholder | O5 |

Passed undetected:

| Probe | What it violates | Result |
|---|---|---|
| Both A06 seats list all 6 lenses. 12 reviewer calls | REVIEW-PANEL.md line 49 says rule O17 caps the cost. Line 55 says up to 7 calls. Line 59 says the remaining lenses split | no errors |
| A05 ultimate reviewer seats gain `tools: write` and `context: author-transcript` | zero-context contract, REVIEW-PANEL.md lines 18 to 23 | no errors. O15 only checks that two constraint strings exist |
| A05 hybrid primary, both reviewers on goose, families still disjoint | not a written rule. O5 is against authors and the orchestrator. O17 only demands disjoint families | no errors |
| A05 lens list reordered so `security-abuse` is second, and only one seat runs it | not a written pin. Primary means list position 0, validator lines 421 to 422 | no errors |
| A06 hybrid primary, aggregator harness set to aider, chain left legal | not forbidden. O16 blocks omo and author or orchestrator harnesses only | no errors |
| A05 ultimate primary, `evidence-provenance` added to both seats | the split in REVIEW-PANEL.md line 59 | no errors |

The 63 planted mutations do not include any of those passes.

## Design

### Aggregator reuses the reviewer chain

It is allowed, and the committed data always does it. 104 of 104 options copy a reviewer harness and chain. On every A05 and A06 option the copy is reviewer 0. Example, A05 ultimate primary: reviewer 0 is goose on `ProviderB/flagship-open` then `ProviderB/gen-pro` at matrix.example.json lines 4615 to 4618, and the aggregator is the same pair at lines 4676 to 4680.

For a one-seat tier this is a cost default, not an independence gain. There is no second family to protect. For spread it fights the reason the second seat exists. The merge model is one of the two families. The script can label a cluster single-family, and nothing checks that the later model merge keeps that label or keeps a single-family blocker.

Ultimate is forced. A05 ultimate already uses deepseek, moonshot, zai, alibaba, and minimax. Xiaomi is retiring. No third family is left. Hybrid, b4b, and global are not forced. On A06 hybrid, minimax is unused, priced at 1.2 in the validator table, and dsh is an unused harness. The same pattern is a blanket, not a last resort. REVIEW-PANEL.md line 63 is honest that reuse is allowed. The data never takes the other option, and the page does not say so.

### Spread cost arithmetic

The stated arithmetic is right. Max 6 lenses, primary on both seats, the other five once each, is 7 reviewer calls. REVIEW-PANEL.md line 55. Add the aggregator from line 57 and a full spread round is 8 model calls. The page states that total only for standard, 4 lens calls plus 1 aggregator equals 5. That sum is also right. A06 in the example is exactly 7 lens assignments. A05 has 5 lenses and 6 assignments. Both match the intended split.

What is wrong is the attribution. Line 49 says the tier caps the cost, rule O17. O17, validator lines 390 to 422, caps lens count and seat count. It does not count calls and does not forbid a non-primary lens on both seats. The example follows the budget. CI will not notice a later edit that breaks it.

### Overclaims

Catch-rate language is clean. REVIEW-PANEL.md line 5, TESTING.md lines 20 to 24, and CHANGELOG 1.3.0 say the fixture is invented and no panel has been run. I did not find a measured-affinity claim in the new docs.

The cost sentence at REVIEW-PANEL.md line 49 overclaims what O17 checks. finding.schema.json line 4 says family is derived by the runner and never typed by the reviewer. `aggregate-findings.py` trusts the string. `OpenAI` and `openai` on the same lines became one cluster marked corroborated, because the family set had two spellings.

EGM-ANALYSIS.md line 23 says model-mesh says little about context hygiene. That was the pre-proposal state. This PR's docs now say a lot. The runtime still enforces none of it. Line 31 says six to eight reviewers per stage. The review skill lists 1 or 3 reviewers per stage. The synthesizer may launch an optional second instance, which tops out at 6, not 8. `agents/synthesizer.md` line 39. Line 27 says no benchmark was found. `docs/designs/review.md` line 169 in the EGM clone labels `test_scenarios.yaml` as an evaluation benchmark for precision and recall. The file is regex `required_pattern` checks, not a rate. The "no rate" half is right. The "no benchmark" half is too strong for a skim.

### Dedupe

`aggregate-findings.py` line 73 merges when the next finding's start is within 3 of the growing cluster end, same path and category.

Demonstrated on temp input, not committed:

- Findings at lines 1 to 2, 5 to 6, and 9 to 10, two families, became one cluster spanning lines 1 to 10, `corroborated` true. The outer findings are 7 lines apart. A nearby unrelated hit mints corroboration.
- Same lines, categories `security` and `correctness`, stayed two clusters. Neither had `needs_model_merge`. REVIEW-PANEL.md line 70 sends only rangeless duplicates to the model merge, so a category disagreement is never merged and never handed to the model. Lenses do not map to one category, so two families on the primary lens can miss corroboration by picking `security` and `regression` for one defect.
- One ranged finding and one rangeless finding on the same path and category stayed split. The rangeless cluster was not flagged for model merge, because that flag requires two rangeless items, line 93.
- `src/a.py`, `./src/a.py`, and `src/a.py ` with a trailing space stayed three clusters. The emptiness check strips, the stored path does not.
- Two reviewer files both using id `1`: `aggregate-findings.py` exited 1 with `finding[2]: duplicate id 1`. The usage accepts multiple files. Reviewers will number from 1. One collision rejects the whole merge. Schema line 9 says unique within one run, and the script applies that across files.
- Cluster output has claims and no evidence. Keys are path, lines, category, severity, lenses, harnesses, families, corroborated, finding_ids, claims, needs_model_merge.

`score-review.py` uses the same 3-line slack and also requires category match, so a right-place wrong-category finding is a miss and a precision penalty. A snowballed cluster that overlaps one defect counts as one useful cluster, which hides the extra findings chained into it.

### Drift false negatives

A complete temp copy was clean. These edits stayed clean:

- `## Twelve situations` changed to `## 12 situations` in ORCHESTRATION.md. D2 only matches number words, `check-drift.py` lines 35 to 39.
- The `contract-fit` "looks for" cell replaced with other prose. D4 compares ids only, lines 77 to 84.
- The spread row changed from `A05, A06` to `A06 only`. No rule reads the tier table.
- A relative link in EGM-ANALYSIS.md pointed at a missing file. D5 scans only ORCHESTRATION.md and REVIEW-PANEL.md, line 24.
- TESTING.md changed from 63 mutations to 99. Not scanned.
- The O18 body set to `if False` while the string O18 remained in the file. D1 only checks that the docstring id appears later in the file, lines 51 to 55.
- The review-gate self-test removed from CI. D7 only looks at `scripts/*.py`, lines 107 to 112, so `scripts/landscape/review_gate.py` is invisible.

`patterns` is missing from the matrix. D2 takes the length of that list, and substitutes 5 when the list is missing, lines 57 to 58, so a missing list still counts as five and matches the doc. The qwen-code role binding is not compared to the matrix.

## EGM spot check

Local clone `/home/user/workspace/egm`. Six or more claims checked.

Faithful:

- Apache-2.0. LICENSE header.
- 9 commits, 2026-10-21 to 2026-10-23. `git log` dates match EGM-ANALYSIS.md line 5.
- Seven skill directories and nine agent files. Line 5.
- Review stages 5 to 9 stay sequential, and reviewers parallelize only inside the current stage. `docs/claude.md` lines 41 to 42. Matches line 13.
- `model: inherit` on `.claude-plugin/agents/zoom_out.md` line 6, and the same phrase in `docs/claude.md` line 72. Matches line 21.
- Context and tool isolation, not filesystem isolation. `docs/claude.md` lines 86 to 88.
- Skill body cap 24,000 bytes, message names Antigravity. `tests/unit/test_skill_load_limits.py` lines 18 to 19. Matches line 17. model-mesh copies that cap in `validate-scenarios.py` line 21, with mm-method grandfathered at 40,000, line 22.
- Claude Code nesting up to 3 levels, Cowork subagents cannot spawn. `docs/claude.md` lines 36 to 39. Matches line 37.
- Bootstrap removes a concurrency limit and spawns one sub-orchestrator per subtree after approval. `docs/designs/bootstrap.md` lines 64 to 67.
- Brainstorm table is Contrarian, Cost, UX, Migration, Observability and SRE, Tech debt. `skills/egm_brainstorm/SKILL.md` around lines 90 to 129. The paraphrase on line 15 is fair.
- Synthesizer takes unconstrained text, dedupes, and groups Blocker, Major, Nit. `agents/synthesizer.md` lines 12 and 40.
- The hallucination reduction sentence is asserted, not measured. `docs/index.md` line 56.
- 104 options. Counted. 12 situations, 4 profiles, 2 options, plus 8 `rpc-worker` options on A01 and A03. Line 57 is right. All 104 carry both review constraints. All 104 aggregators copy a reviewer chain.

Not faithful, already listed under overclaims: the six-to-eight count, and "no benchmark".

## A05 and A06 second reviewers

All 16 second seats are `qwen-code` and `momus`. First seat is goose on primary and pi on alternate. Families are disjoint from each other and from authors and the orchestrator on every committed option. Cap exemption is author-only, validator lines 125 to 131. A clean over-cap swap on the second seat fired O7. Committed second-seat rungs on hybrid and b4b are under the 4.65 reference: gpt-5.6-luna at 1.8, MiniMax-M3 at 1.2, kimi-k2.7-code at 4. Global and ultimate have no price cap in O7. Ultimate rungs are HK families.

| Cell | Second chain | Cap | Fallback |
|---|---|---|---|
| A05 and A06, ultimate, both options | `ProviderF/vision-xl` only, minimax, matrix.example.json lines 4630 to 4632 for A05 ultimate primary | no price cap, HK eligible | none. These four seats are the only 1-rung reviewer chains in the matrix. 116 other reviewer chains have 2 rungs |
| A05 hybrid and b4b | `ProviderA/flagship-lite` then `ProviderF/vision-xl`, lines 4868 to 4871 | both under 4.65 | yes, and it changes family from openai to minimax |
| A06 hybrid and b4b | flagship-lite then `ProviderE/coder-mid` | 1.8 and 4, under the cap | yes, openai to moonshot |
| A05 global | `ProviderB/flagship-open` then `ProviderE/coder-xl` | no cap, references 6 and 15 | yes, alibaba to moonshot |
| A06 global | flagship-lite then coder-xl | no cap, references 0.75 and 15 | yes, openai to moonshot |

Harness. qwen-code is a legal unused harness once authors, orchestrator, and reviewer 0 have taken pi, omo, goose, codex, or aider. The harness example still describes an author seat for A07, A08, and A10 to A12, with an alibaba chain, and says the reviewer is a different harness. `qwen-code.example.json` line 18. Twelve of the sixteen second-seat primary rungs are not Qwen models. A05 global is the one whose first rung is Qwen. The native config example is a DashScope Qwen provider. Routing MiniMax, GPT, or Kimi through it is an unbuilt adapter, and the option status says proposed-not-implemented. That is acceptable as a proposal. It is not a measured pairing, and the example text was not updated. On hybrid and b4b primary, codex is free and would match the GPT primary rung more closely. Uniform qwen-code is a choice, not a constraint.

Fallbacks. Hybrid, b4b, and global have one. It is a different family, so the seat that answers is not stable, though the chain as a whole stays disjoint and under the cap where a cap applies. Ultimate has none, and a legal one does not exist in the current table. A same-family spare would need a second minimax model. There is one minimax row. A cross-family spare would overlap authors, the orchestrator, or reviewer 0, or it would be the retiring xiaomi row, which O4 rejects. The security cross-check on ultimate is a single rung. That is not written down.

Role. Both seats are momus. `agent_sequence` records momus twice, lines 4673 to 4674. The rendered table can tell them apart by harness and chain. A runner that keys seats by role cannot. There is no seat id.

## Findings

**Major. Call budget is not rule O17.** REVIEW-PANEL.md line 49, validator lines 390 to 422. Both seats can run every lens. CI stays green. Fix the sentence or enforce the split and the 7-call max.

**Major. Gap clustering false-corroborates.** `scripts/aggregate-findings.py` line 73. Three findings spaced 3 lines apart became one corroborated cluster from line 1 to line 10. Corroboration is the signal the spread tier is for. A nearby unrelated hit should not create it.

**Major. Category and line-range misses never reach the model merge.** `aggregate-findings.py` lines 73 to 93, REVIEW-PANEL.md line 70. Same lines with different categories stay split. A rangeless duplicate of a ranged finding is not flagged. Two families can describe one defect and never count as corroborated.

**Major. Duplicate ids abort a multi-file merge.** `aggregate-findings.py` lines 47 to 49. Two reviewer files that both use id `1` exit 1. Namespace by file, or by harness and family, before this script is on a real panel.

**Major. Drift check misses the drifts it is for.** `scripts/check-drift.py` lines 24, 35 to 39, 51 to 55, 77 to 84, and 107 to 112. A temp copy with the spread tier retargeted, a digit count, a gutted O18 check, a broken EGM link, and a dropped CI step all printed no drift. The self-test only checks that a planted hit appears, so a noisy or narrow checker still passes.

**Major. Ultimate spread seat has no fallback, and none is legal.** matrix.example.json lines 4630 to 4632, and the same shape on the other three ultimate second seats. Say so, or free a family. A security cross-check with one rung is a thin design even when the validator cannot do better.

**Major. Spread aggregator is reviewer 0 wherever a third family was available.** matrix.example.json lines 4676 to 4680, and the same copy on all 104 options. REVIEW-PANEL.md line 63 allows it. On ultimate it is forced. On hybrid, b4b, and global it is not. Either use the free family on spread, or say the merge seat is intentionally one of the reviewers and that single-family blockers must survive the model merge.

**Minor. Both spread seats are momus.** matrix.example.json lines 4629 and 4673 to 4674. Add a seat id. The role name is doing too much.

**Minor. O15 is a string presence check.** Validator lines 402 to 404. A seat can declare write tools and the author transcript and still pass. Reject unknown seat keys, or stop calling the constraint a contract the validator checks.

**Minor. Primary lens is whatever is first.** Validator lines 421 to 422. Moving `security-abuse` off position 0 on A05, and covering it with one seat, passed. If security must be the A05 primary, name it.

**Minor. qwen-code example is stale for the new reviewer use.** `examples/orchestration/harnesses/qwen-code.example.json` line 18. Second-seat models are mostly not Qwen. Do not imply a native pairing. None is claimed in REVIEW-PANEL.md, which is correct.

**Minor. EGM-ANALYSIS.md overstates two repo facts.** Line 31, reviewer count per stage. Line 27, no benchmark, against `docs/designs/review.md` line 169 in the clone. The rest of the study I checked matches the clone. Line 23 is stale relative to this PR's own docs.

**Minor. Cluster markdown drops evidence, and family case is not normalized.** `aggregate-findings.py` lines 86 to 93. Small next to the false corroboration.

No blocker. The committed matrix does not sneak an author or orchestrator family into a reviewer or aggregator. Cap exemption does not leak onto the second seat. Gates fire when moved. I would not run a panel on `aggregate-findings.py` as it stands, and I would not cite the drift check as proof the tier table matches the data.

## Verdict

SHIP WITH FIXES.

Fix in this change, or stop claiming the check exists: the O17 cost sentence, transitive false corroboration, cross-file id failure, and the drift checker's blind spots on the tier table and disabled rules. Document or change, before anyone treats spread as two independent looks plus a neutral merge: the ultimate single-rung second seat, and the aggregator copying reviewer 0 on cells where a third family fits under the cap.
