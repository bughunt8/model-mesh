# Orchestration review, round 2

Verdict: SHIP WITH FIXES

HEAD `c96cb85`. Mutations ran in `/tmp/review-copy2` by importing `scripts/validate-orchestration.py` and calling `validate(..., check_files=False)`. The shipped matrix returns zero errors. `python scripts/validate-orchestration.py --self-test` prints `self-test passed` (37 `expect()` calls).

## Original findings

| ID | Status | Evidence |
|---|---|---|
| B1 | fixed | Same-ID alias with family `alibaba`, `deepseek/*` labelled `alibaba`, `openai/gpt-6.1-sol` labelled `deepseek`, and `apiyi/gpt-5.6-sol` labelled `minimax` all fail. O4, O5, and O6 fire. Hephaestus on a DeepSeek ID labelled `openai` fails O4 and O8. Same ID with a correct label fails O5 on family and on model ID. |
| B2 | fixed | `absolute_exception.reason = "x"` on `A01/ultimate/alternate`, with the reviewer copied onto the author harness and chain, fails O5 (`no owner-approved independence exception`) plus harness, family, and ID overlap. The key alone on A04 also fails O5. |
| B3 | fixed | `reviewers = []` fails O5 (`at least one reviewer is required`). Empty list plus an orchestrator chain copied from the author also fails O5 on family overlap. `chain: []` fails O4 (`every seat needs a non-empty string chain`). |
| M1 | fixed | Hybrid last-author `coder-xl` fails O7 at `explore[2]`. Rewriting b4b `gen-pro` to `opencode/qwen3.8-max` fails O7. Shipped hybrid `kimi-k3` sits only on atlas or prometheus index 0, or `deep` index 1. No `qwen3.8-max` or terra ID remains in hybrid or b4b cells. |
| M2 | partly fixed | Aider-as-orchestrator, removing `pi-external-container` from A05, and cloning the third option's harness set all fail. Shipped: 104 Pi seats, 0 missing the constraint; 0 non-primary orchestrators are `opencode-omo` (44 goose, 8 qwen-code, 4 none). Situation-level `agent_sequence` is still unchecked. See N2. |
| M3 | fixed | Non-primary orchestrator harnesses are goose, qwen-code, or none. The O9 check rejects a non-primary `opencode-omo` orchestrator; the shipped file passes it. |
| M4 | partly fixed | The four-way Pi-container and Aider ticks are gone. Sol's provenance manifest is no longer attributed to Sol; Sol line 185 is the repair-reviewer point, and that is what the unique table now says. Residual false sentences remain. See N5. |
| M5 | partly fixed | Round-1 strings now block: `@openai/codex-mini`, `qwen-coder`, `qwen-code-plus`, `codex clipboard`, `codex executive summary`. Lookahead `(?![\w/.-])` stops hyphen continuation. Separators outside that class still strip the token. See N4. |
| m1 | fixed | Changelog says 37 failure cases. The file has 37 `expect()` calls and the self-test passes. |
| m2 | fixed | `dsh.example.json` `native_path` now names `$DSH_HOME/profiles/sdk/cordis.patch.yml` and says the example does not use it. |
| m3 | fixed | `GLOBAL-PROFILE.md` labels effort (Sol 51 xhigh, Astra 53 max, Grok 46 xhigh) and shows both price tiers. Six Zen figures match the fetched page: terra $18 above 272K, Sol $15, Astra $75, Grok $12 above 200K, Qwen3.8-max $6, Kimi K3 $15 ([OpenCode Zen](https://opencode.ai/docs/zen/)). |
| m4 | partly fixed | `verified` inside `constraints` now fails O11. `check_native_keys` only compares the top-level key set with a fixture. A nested `invented_key` under Goose `settings` passed. `scripts/validate-orchestration.py` is still denylist-exempt (`.github/checks.py:83`). |

## New findings

### Major

N1. Cap exemption follows the role name, not the seat kind. `cap_exempt` (`scripts/validate-orchestration.py`, the function above O7) treats hybrid `atlas` or `prometheus` at index 0 as exempt, and `seats()` includes the orchestrator. Mutation: A01 hybrid authors and category routes set to `ProviderD/comm-xl`, orchestrator role set to `atlas`, chain `ProviderE/coder-xl` (`moonshotai/kimi-k3`, $15). `validate` returned no errors and no O7. That is an orchestration rung over the cap. Fix: exempt only author seats, and only the slots named in the table (`kind == "author"`). Add this mutation to the self-test.

N2. Situation `agent_sequence` is not the option sequence, and nothing compares them. A01's situation sequence is `explore, hephaestus, momus`. The ultimate option sequence is `atlas, explore, momus`. The same split holds for A01 and A03 on ultimate, hybrid, and b4b (hephaestus dropped). Global seats hephaestus but in a different order. That is 24 options. O3 checks `option.agent_sequence` against that option's seats only. Fix: require `situation.agent_sequence` to equal the union of seated roles, or delete the situation field and render from the option.

N3. `model_family` is a prefix test, and ultimate allows vendor `opencode`. Mutation: author chain `opencode/qwen-wrapped-gpt-6.1-sol`, family label `alibaba`, reviewer moved to `ProviderF/vision-xl`, other author and routes left on DeepSeek. Zero errors. The name starts with `qwen`, so it is classified Alibaba and the vendor is on the HK allowlist. Real IDs are caught: `openai/gpt-6.1-sol`, `apiyi/gpt-5.6-sol`, and `opencode/o3-mini` (unknown prefix) all fail. Fix: ultimate may use only IDs in a closed catalog, or reject a name that contains a blocked prefix (`gpt-`, `claude-`, `grok-`, `gemini-`) after the allowed prefix.

### Minor

N4. `HARNESS_ALLOW` still hides a vendor word when the next character is not in `[\w/.-]`. Replicated `deny_hit`: `qwen-code:qwen3.8-max`, `qwen-code@qwen3.8-max`, `@openai/codex:mini`, `@openai/codex mini`, and `@openai/codex@1.0` pass. `Codex CLI,gpt-5.4-codex` still blocks because `gpt-5` remains. Fix: after a match, require end of string or whitespace, and add these strings to `_must_fail`.

N5. Synthesis residuals. `SYNTHESIS.md` ticks Kimi for "Orca is worth its cost only for parallel isolated worktrees." Kimi line 160 says no scoped row needs Orca at all. The evidence cell even says Kimi uses no coordinator. The analysis says only Opus and Sol say momus cannot be the independent review. Kimi line 157 says the independent reviewer is never omo because momus and oracle share the worker harness. The closing paragraph says no report proposed the Pi container rule. Opus line 225 says "Pi runs in a container, read-only mount." Fix: untick Kimi on Orca, tick Kimi on the momus rule, and credit Opus for the container line.

N6. `check_native_keys` does not walk nested keys. Adding `invented_key: true` under Goose `settings` left the top-level set unchanged and passed. O13 still does not compare nested keys to the cited pages. Fix: check the nested names the fixture claims, or stop calling the check a source match.
