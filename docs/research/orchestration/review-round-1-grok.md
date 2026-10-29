# Independent orchestration review

Verdict: DO NOT SHIP

Commit `7e6972b` on `orchestration/multi-agent-matrix`. The shipped matrix happens to be label-clean. The validator that CI treats as the enforcement of the independence rule, the Hong Kong rule, and the cap does not enforce those rules. A violating cell stays green. That is the product this commit adds.

Mutations were run in `/tmp/review-copy` by importing `scripts/validate-orchestration.py` and calling `validate(..., check_files=False)`. The shipped tree passes: `python scripts/validate-orchestration.py` prints `all orchestration checks passed`.

## Blocker

### B1. Independence, Hong Kong, proxy, and hephaestus are label checks

File: `scripts/validate-orchestration.py:75-77`, `173-197`, `192-207`. `families()` returns the hand-written `family` string. Nothing derives family from the model ID prefix. No script in this commit does. O6 and O8 trust the same field, plus `hk_policy_eligible`.

Evidence. On a copy of the valid matrix, these mutations produced zero errors:

- Reviewer placeholder `id` set to the author's `deepseek/deepseek-v4-pro`, `family` set to `alibaba`. O5 did not fire.
- Reviewer `id` `deepseek/deepseek-v4-flash`, `family` `alibaba`. O5 did not fire.
- Ultimate author rung `id` `openai/gpt-6.1-sol`, `family` `deepseek`, `hk_policy_eligible` true. O6 did not fire.
- Ultimate author fallback `id` `apiyi/gpt-5.6-sol`, `family` `minimax`, `hk_policy_eligible` true. O6 did not fire. Rule 2's "no proxy" is not a check at all.
- Hephaestus first rung `id` `deepseek/deepseek-v4-pro`, `family` `openai`. O8 did not fire.

Controls that did fail, so the loop is not dead: a helper seat whose chain reused the reviewer's real family (`O5: reviewer family ['alibaba'] overlaps authors`); a category route that did the same; a differently named OpenAI model (`flagship-lite`) against an OpenAI author; orchestrator harness equal to reviewer harness.

Fix. Build family from a checked prefix map (`deepseek/` -> deepseek, `moonshotai/` and `kimi` -> moonshot, `qwen` -> alibaba, `glm` or `zai-coding-plan/` -> zai, `gpt` or `openai/` -> openai, `claude` or `anthropic/` -> anthropic, `grok` or `xai/` -> xai, `gemini` -> google, `apiyi/` -> proxy). Reject a chain if the stored family disagrees. Compare reviewer and author sets on model ID as well as family. For `ultimate`, reject any ID whose vendor is OpenAI, Anthropic, Google, xAI, Gemini, or `apiyi`, whatever the family field says.

### B2. `absolute_exception` is a free pass

File: `scripts/validate-orchestration.py:174-185`. Any non-empty `reason` turns reviewer/author harness overlap and family overlap into notes. It does not check that no alternative exists. `docs/ORCHESTRATION.md:57` says an exception is only when no alternative exists, and that none is granted in this package. The self-test at line 415 treats a reason of `synthetic fixture` as success.

Evidence. On `A01/ultimate/alternate` (authors on `dsh`, orchestrator on `opencode-omo`), setting the reviewer harness and chain equal to the author and `absolute_exception.reason` to `x` produced no errors. Notes only: `ABSOLUTE-EXCEPTION on harness: x` and `ABSOLUTE-EXCEPTION on family ['deepseek', 'moonshot']: x`. The earlier primary-cell attempt looked caught only because that cell's author harness is also the orchestrator harness, and the orchestrator check is not excused.

Fix. Delete the escape, or fail closed unless the reason names every other harness and every other legal family and why each is impossible. A one-character string must not suppress O5. Do not count a note as enforcement.

### B3. No reviewer means no independence check

File: `scripts/validate-orchestration.py:173`. O5, including orchestrator-versus-author overlap at lines 186-191, sits inside `for r in o["reviewers"]`. An empty list never enters. An empty reviewer chain makes `families()` return an empty set, so overlap is vacuous.

Evidence. `reviewers = []` on `A01/ultimate/primary` passed. The same cell with an empty reviewer list and the orchestrator chain copied from the author also passed. A reviewer with `"chain": []` and a different harness passed.

Fix. Require one or more reviewers, each with a non-empty chain. Run the orchestrator overlap check even when the reviewer list is empty. Reject reviewer role `momus` or `oracle`: those names are defined as in-harness gates (`docs/ORCHESTRATION.md:55`) and every shipped reviewer seat is role `momus` (108 of 108). The harness field currently differs, so this is not a shipped same-harness review, but the role name is how an implementer will wire omo's own momus.

## Major

### M1. Cap policy is not what the prose says, and hybrid cells follow the hole

File: `scripts/validate-orchestration.py:208-214`; `.github/checks.py:301-307` and `334`. O7 flags a placeholder only if the role suffix is in `OVER_CAP` and not in `METERED_EXEMPT`. `coder-xl` is exempt in every slot. The `"*"` value is never read. A placeholder renamed to `gen-pro` whose `id` is `opencode/qwen3.8-max` ($6, over the $4.65 cap in `docs/EXAMPLE-MAPPING.md:104`) passed O7 on `b4b`.

The written exemption table (`docs/EXAMPLE-MAPPING.md:122`) allows `coder-xl` in hybrid only on prometheus/atlas primaries, `deep` index 1, `ultrabrain` index 2, and `hephaestus.ultrawork`, and in b4b only on `deep` index 1. The matrix does not match that table. Hybrid `coder-xl` seat counts from a full scan of `matrix.example.json`: explore fallback 8, metis fallback 8, hephaestus fallback 6 (not ultrawork), atlas fallback 6 (not primary), prometheus fallback 5, oracle 5, `quick` route 5, `ultrabrain` route index 1 not 2 (5), `writing` 3, `unspecified-high` 2, librarian 2, sisyphus-junior 2. Those are generalist, utility, or orchestration rungs at the documented $15 output price. `flagship-open`, `div-flagship`, and `reasoner-xl` do not appear in hybrid or b4b cells. That is the only cap fact the gate actually checks.

Fix. Enforce the slot table, not a role-wide exemption. Check mapped output price, or at least the model ID, not the placeholder suffix. Put `coder-xl` on hybrid only in the slots the table names.

### M2. Seats contradict the harness evidence, and O2 ignores a cloned third option

Pi as an author has no container or isolation constraint in 24 cells. `docs/research/orchestration/HARNESSES.md:14` says Pi has no permission system and must run in a container. `examples/orchestration/harnesses/pi.example.json` says the same. `docs/research/orchestration/EXAMPLES.md:35` claims a container for A05 only, and that sentence is not in the cell data. The validator has no such rule.

Aider as orchestrator is accepted. Mutation: set `A01/ultimate/primary` orchestrator harness to `aider`. Zero errors. Shipped cells do not do this. The docs say never (`HARNESSES.md:16`). The gate does not.

Hephaestus is missing from every ultimate and b4b option of A01 and A03, while `agent_sequence` still lists it. O8 forbids the Hong Kong remap the profile docs already use (DeepSeek in the hephaestus seat), so the matrix substitutes `atlas` and the rationale does not say so. The validator never checks that `agent_sequence` roles are seated.

`A09` `rpc-worker` is identical to `alternate` in all four profiles once the name is ignored. O2 (`validate-orchestration.py:128-131`) compares only `options[0]` and `options[1]`. A mutation that pointed `rpc-worker` authors at the primary harness also passed.

Fix. Require a container constraint on every Pi author seat. Reject `aider` as orchestrator. Either seat hephaestus on the documented HK reasoner and drop the OpenAI-only O8 rule for `ultimate`, or remove hephaestus from the situation sequence and say why. Compare every option's author harness set with every other option, and reject a byte-identical clone.

### M3. The open-source alternate does not let you drop omo

`docs/ORCHESTRATION.md:73` and `docs/research/orchestration/SYNTHESIS.md:43` say every cell has an open-source-only alternate so the omo exception can be withdrawn without redesign. 44 of 48 alternates still set the orchestrator harness to `opencode-omo`. Only A12 has no orchestrator. Withdrawing the Sustainable Use License exception still leaves the orchestrator seat on omo.

Fix. Give each alternate an orchestrator that is not omo, or stop claiming the alternate is open-source-only.

### M4. Synthesis ticks are not in the reports

`docs/research/orchestration/SYNTHESIS.md:15` ticks all four models for "Pi must run in a container, Aider is never an orchestrator". `council/gpt-6-1-sol.md` has no "container" and does not state the Aider rule. Only `council/glm-5-3.md:156` states "Aider is a worker alternate and a reviewer, never an orchestrator." Opus states the container rule (`council/claude-opus-5-5.md:225`). Kimi's container hits are Goose Docker, not a Pi requirement.

`SYNTHESIS.md:34` attributes the author-provenance manifest to GPT 6.1 Sol. `council/gpt-6-1-sol.md` has no "provenance" and no "manifest". The closest line (185) says that if a reviewer authors a repair, allocate a new reviewer. That is not A06's constraint. The citation on line 15 points at the Pi settings page and the Kimi Codex guide, neither of which states those two rules. Fetched 2026-10-11: [Pi settings](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/settings.md) documents `defaultProvider` and `defaultThinkingLevel`, not a container mandate; [Kimi's Codex guide](https://platform.kimi.ai/docs/guide/codex-kimi) documents the TOML block, not Aider.

Kimi's ultimate A02 exception is real (`council/kimi-k3.md:150`). Do not treat that one match as cover for the false ticks.

Fix. Retick from the raw reports. Move the provenance rule to whoever actually wrote it, or label it as this package's rule. Drop the four-way checkmarks that only one report supports.

### M5. `HARNESS_ALLOW` hides model-like IDs

File: `.github/checks.py:38-45`. The regex has no word boundary. `HARNESS_ALLOW.sub` runs before `DENY`. Replicated `deny_hit` results:

| String | Result | After strip |
|---|---|---|
| `@openai/codex-mini` | pass | `-mini` |
| `@openai/codex-mini-latest` | pass | `-mini-latest` |
| `qwen-coder` | pass | `r` |
| `qwen-code-plus` | pass | `-plus` |
| `qwen-coder-plus` | pass | `r-plus` |
| `@qwen-code/qwen-coder-plus` | pass | `r-plus` |
| `codex clipboard` | pass | `pboard` |
| `codex executive summary` | pass | `utive summary` |
| `the model is qwen-code-flash` | pass | `the model is -flash` |

`use codex-mini` and `Qwen Code with qwen as the vendor` still block, so the self-test fixtures pass while the prefix hole stays open. The comment on line 44 says a model ID still fails. These strings show that is false.

Fix. Anchor each alternative with word boundaries, or reject a match that is a prefix of a longer token. Add the strings above to `_must_fail`.

## Minor

### m1. "24 failure cases" is the wrong count

`CHANGELOG.md:8`. `python scripts/validate-orchestration.py --self-test` prints 23 `expect()` hits plus `documented exception is reported, not silent`. That last case is a non-failure. The self-test also does not include B1, B2's clean alternate, B3, the third-option clone, or Aider-as-orchestrator. Saying the self-test proves the rules is how the holes shipped.

Fix. Say 23, and add the mutations above as cases that must fail.

### m2. DSH path claim is stronger than the SDK page

`examples/orchestration/harnesses/dsh.example.json` says "No config file." The fetched [SDK README](https://github.com/deepseek-ai/deepseek-harness/blob/master/python/sdk/README.md) documents `$DSH_HOME/profiles/sdk/cordis.patch.yml` as the persistent user patch, and constructor args `dsh_home`, `cwd`, `provider`, `model`, `reasoning_effort`, `max_tokens`, with example model `deepseek-v4-flash` only. The example's use of `deepseek-v4-pro` is already hedged. The "no config file" sentence is not.

Fix. Name the patch file, or say the example uses constructor args and ignores the patch file.

### m3. Global index figures are rounded and unlabelled

`docs/research/orchestration/GLOBAL-PROFILE.md:13-17`. Output prices that match vendor pages: GPT-6.1 Sol $10, GPT-6 Astra $50, GPT-6 Luna $0.50 ([OpenAI models](https://developers.openai.com/api/docs/models)); Grok 4.7 $6 / 1M output on the global standard rate below 200k ([xAI pricing](https://docs.x.ai/developers/pricing)), index 46 at xhigh ([Artificial Analysis](https://artificialanalysis.ai/models/grok-4-7)). Sonnet 5.5 at 56 and $10, and Opus 5.5 at 58, match the Artificial Analysis write-up. The Sol/Astra integers do not: Artificial Analysis puts Sol one point under Astra, and a 2026-09-30 comparison gives Sol 51.8 and Astra 52.7 at max effort, not 52 and 53. The table does not say max effort. `gpt-6.1-luna` is absent from the OpenAI models page; `gpt-6-luna` is listed. That "does not exist" claim holds. Gemini 4 Argon still has no Google-published model ID ([DataCamp](https://www.datacamp.com/blog/gemini-4-argon)); a third-party gateway inventing `gemini-4-argon` does not make it a public API ID. Gemini is absent from `profiles/global.json`, `profiles/global.example.json`, and every matrix chain.

Fix. Cite the effort setting and print the index to one decimal, or say the integers are rounded.

### m4. Two narrower gate gaps

`scripts/validate-orchestration.py:236` flags claim words only when the path ends in `rationale` or `status`. Putting `verified` in `constraints` passed. O13 checks that harness examples parse and carry the envelope. It does not check keys against the cited URLs, so an invented key would pass. `.github/checks.py:83` exempts the whole validator, which is why the self-test can embed `xai/grok-4.7` and `opencode/qwen3.8-max` (lines 394-396) in a scanned tree.

Fix. Scan every string for claim words. Spot-check native keys in CI or drop the "docs-checked" status to "keys copied, values unverified" where the limitation already says that. Build the self-test IDs from fragments, as `checks.py` does, and drop the exemption.

## Checks that found nothing wrong

- Shipped ultimate chains use only these IDs: `deepseek/deepseek-v4-pro`, `moonshotai/kimi-k3`, `opencode/qwen3.8-max`, `opencode/qwen3.7-plus`, `zai-coding-plan/glm-5.3`, `zai-coding-plan/glm-5.3-flash`, `minimax/MiniMax-M3`. No OpenAI, Anthropic, Google, xAI, Gemini, or `apiyi` ID in an ultimate cell. Codex in ultimate is only `A05` alternate, status `conditional-custom-provider-features-deferred`.
- No shipped reviewer shares an author model ID or a correctly labelled family. Helper chains that differ from the first author seat are included in the author union; a correctly labelled overlap is caught. Category routes are included. Orchestrator equals reviewer is caught when a reviewer exists and the exception is not set.
- Primary and alternate author harness sets differ in every cell. Hephaestus, where seated, has a first model labelled `openai` (`apiyi/gpt-5.6-terra` or `openai/gpt-6.1-sol`). It is not seated on a non-OpenAI label in the shipped file.
- No Gemini model is routed. Research notes mention Gemini only as a retired family or as another product's plugin ecosystem.
- `MATRIX.md` matches `--render` (O14 passed). New `docs/ORCHESTRATION.md` and the 1.2.0 changelog block have no em dashes. New README section has no em dashes and no curly quotes.
- Harness keys that match the fetched pages: Aider `model`, `architect`, `editor-model`, `auto-commits`, `auto-test`, `test-cmd`, `map-tokens`, `read` on [aider.chat](https://aider.chat/docs/config/aider_conf.html). Codex/Kimi `model`, `model_provider`, `model_context_window`, `base_url` `https://api.moonshot.ai/v1`, `env_key`, `wire_api` `responses` on the Kimi guide; reserved provider IDs `openai`, `ollama`, `lmstudio` on the [Codex config reference](https://www.codex-docs.com/en/docs/config-file/config-reference). Pi `providers` / `baseUrl` / `api` `openai-completions` / `apiKey` / `models` / `id`, and settings `defaultProvider`, `defaultModel`, `defaultThinkingLevel`, `enableAnalytics`, `enableInstallTelemetry`. Qwen `modelProviders` nested under `openai` with `id`, `name`, `envKey`, `baseUrl`; `mcpServers` `command`, `args`, `timeout`, `trust`. OpenCode `$schema`, `plugin`, `permission.edit`, `permission.bash`. Goose recipe fields including `goose_provider`, `goose_model`, `retry.checks`, `on_failure`. The Goose example's `openai` provider plus `qwen3.8-max` is not in the recipe page; the file's limitations already say so. The Qwen example's DashScope URL and `@playwright/mcp` package are labelled unfetched. Those hedges are accurate. They are not a substitute for B1.
