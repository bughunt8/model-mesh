<!-- example-mapping: contains real provider/model IDs by design; exempt from the vendor denylist like profiles/*.example.json -->
# Example Mapping (placeholder → real ID)

This is the concrete reference mapping used by the `profiles/*.example.json` files. It shows one real-world way to fill in the placeholders. **Your mapping will differ** — use this only as a worked example, and keep your own mapping in a git-ignored `provider-map.local` (see [`PROVIDERS.md`](PROVIDERS.md)).

> These are illustrative IDs for a specific stack (including a proxy provider for geo-locked flagship models). They are not recommendations, and availability/pricing change frequently.

## Provider placeholders

| Placeholder | Real provider |
|---|---|
| `ProviderA` | `apiyi` (proxy for geo-locked flagship / premium models) |
| `ProviderB` | `opencode` (general gateway) |
| `ProviderC` | `deepseek` (open-weight reasoning) |
| `ProviderD` | `zai-coding-plan` (communicator-class subscription) |
| `ProviderE` | `moonshotai` (coding-specialist family) |
| `ProviderF` | `minimax` (multimodal / long-context) |
| `ProviderG` | `xai` (independent 5th-vendor diversification) |

## Model placeholders

| Placeholder | Real model ID | Role |
|---|---|---|
| `ProviderA/flagship-xl` | `apiyi/gpt-5.6-sol` | Top flagship reasoner |
| `ProviderA/flagship-mid` | `apiyi/gpt-5.6-terra` | Value flagship workhorse |
| `ProviderA/flagship-lite` | `apiyi/gpt-5.6-luna` | Cheap flagship tier |
| `ProviderA/flagship-prev` | `apiyi/gpt-5.5` | Previous-gen safety rung |
| `ProviderA/reasoner-xl` | `apiyi/claude-opus-5` | Cross-family deep reasoner |
| `ProviderE/coder-xl` | `moonshotai/kimi-k3` | Flagship coding model |
| `ProviderE/coder-mid` | `moonshotai/kimi-k2.7-code` | Coding workhorse |
| `ProviderE/coder-swarm` | `moonshotai/kimi-k2.6` | Long-context / swarm coding |
| `ProviderB/coder-swarm` | `opencode/kimi-k2.6` | Same model via the general gateway (alt route) |
| `ProviderD/comm-xl` | `zai-coding-plan/glm-5.3` | Communicator-class orchestrator |
| `ProviderD/comm-lite` | `zai-coding-plan/glm-5.3-flash` | Cheap communicator (GLM-5.3-Flash) |
| `ProviderD/vision-lite` | `zai-coding-plan/glm-5.3-flash` | Cheap multimodal fallback (GLM-5.3-Flash, native vision) |
| `ProviderC/open-reason-xl` | `deepseek/deepseek-v4-pro` | Open-weight reasoning lifeline (GA 0813 build; ID unchanged) |
| `ProviderC/open-reason-lite` | `deepseek/deepseek-v4-flash` | Open-weight fast reasoner |
| `ProviderB/gen-pro` | `opencode/qwen3.7-plus` | Concise planning/writing generalist (replaces retired gemini-3.1-pro) |
| `ProviderB/gen-flash` | `opencode/qwen3.5-plus` | Fast utility loop steps (distinct from `open-reason-lite`; replaces retired gemini-3-flash) |
| `ProviderB/util-misc` | `opencode/big-pickle` | Misc utility backup (Zen-exclusive experimental model) |
| `ProviderB/open-coder` | `opencode/mimo-v2.5-free` | Token-efficient open-weight coder (MiMo) — coding/open fallback rung |
| `ProviderB/retrieval-mid` | `opencode/qwen3.6-plus` | Retrieval / librarian |
| `ProviderB/creative-mid` | `opencode/muse-spark-1.2` | Creative generalist (distinct from `gen-pro` and `retrieval-mid`) |
| `ProviderB/budget-low` | `opencode/deepseek-v4-flash-free` | Cheapest general |
| `ProviderB/flagship-open` | `opencode/qwen3.8-max` | GA frontier-class open flagship — ultimate only (cost > cap) |
| `ProviderF/vision-xl` | `minimax/MiniMax-M3` | Native multimodal + long context |
| `ProviderG/div-flagship` | `xai/grok-4.6` | Diversification fallback — ultimate only (cost > cap) |

## Notes

- `coder-swarm` appears under two providers because the same model is reachable via both a specialist provider and the general gateway; the profiles use whichever route fits the fallback slot.
- `flagship-prev` (`gpt-5.5`) is retained only as a compatibility/safety fallback rung.
- `flagship-open` (`qwen3.8-max`) is the **GA production** release (ID `qwen3.8-max`, replacing the former `qwen3.8-max-preview` last-resort rung). It is [frontier-class on agentic work](https://rits.shanghai.nyu.edu/ai/qwen3-8-max-draws-level-with-the-frontier-on-agentic-benchmarks/) but priced at [$2 in / $6 out per 1M](https://aireiter.com/blog/qwen3-8-max-api-pricing); the $6 output rate exceeds the **policy budget cap** ($4.65/1M output — see the cap note below), so it is used in `ultimate` only. `hybrid`/`b4b` now use `gen-pro` (`qwen3.7-plus`) in the slots the preview previously occupied.
- `comm-xl` (`glm-5.3`) — GLM-5.3 is a [post-training upgrade on the same base as GLM-5.2](https://www.marktechpost.com/2026/08/14/z-ai-ships-glm-5-3-without-retraining-the-base-model-better-at-complex-coding-and-long-horizon-tasks/) with large agentic-coding gains ([DeepSWE 46.2 → 66.9, Terminal-Bench 3.0 4.6 → 28.3](https://www.eigent.ai/blog/glm-5-3-coding-cyber-model)). **Per-token pricing is now published on Z.ai's rate card** at [$1.40 in / $0.26 cached / $4.40 out per 1M](https://docs.z.ai/guides/overview/pricing). Note this is the **same unit price as GLM-5.2** ([$1.40 / $4.40](https://docs.z.ai/guides/overview/pricing)); only the *publication* is new — 5.3 did not get cheaper or more expensive per token than 5.2. Its **$4.40 output is under the $4.65/1M policy budget cap** (see the cap note below), so `comm-xl` maps into `hybrid`/`b4b` on a metered per-token basis. **Cost caveat:** GLM-5.3 is measurably more verbose than 5.2 — roughly [+55% output tokens per task](https://venturebeat.com/ai/glm-5-3-hits-the-api-at-1-4-4-4-per-million-tokens) — so real cost-per-solved-task can rise even at an unchanged unit price. No GLM version newer than 5.3 exists as of 2026-08-30.
- `comm-lite` / `vision-lite` (`glm-5.3-flash`) — [GLM-5.3-Flash](https://docs.z.ai/release-notes/new-released) (released 2026-08-26) replaces the stale `glm-5-turbo` (no longer on Z.ai's current rate card) as the cheap communicator, and is added as a cheap **multimodal fallback** on `multimodal-looker` (it has [native vision](https://docs.z.ai/release-notes/new-released); 320B/18B MoE, hybrid attention; vision numbers are vendor-stated — [OfficeQA 62.4 / MVBench 77.8 / MMVU 80.5 per Together AI's model card](https://www.together.ai/models/glm-5-3-flash) — not independently benchmarked here, so its placement ahead of a flagship-lite vision rung in `b4b` is a **cost-first** ordering, not a capability claim). Priced [$0.15 in / $0.50 out per 1M list](https://docs.z.ai/guides/overview/pricing) (promo $0.075/$0.25 until 2026-09-09). Both placeholders intentionally resolve to the same model — a dual-role mapping (like `coder-swarm`'s two-provider entries), not a duplicate.
- `open-reason-xl` (`deepseek/deepseek-v4-pro`) now resolves to the [GA **0813** build](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) — the [API ID is unchanged](https://openllmstack.com/models/deepseek-v4-pro-0813/), so no edit was needed. Note DeepSeek [moved the V4 family to peak/off-peak billing on 2026-08-16](https://ofox.ai/blog/deepseek-v4-pro-0813-price-weights-benchmarks-api-access-2026/) (peak $1.32/$3.96, off-peak $0.66/$1.98 per 1M) — still under the cap.
- **All Gemini models were retired** (both `gemini-3.1-pro` and `gemini-3-flash`). Role-aware replacements: the planning/writing/visual/artistry role (`gen-pro`) → `qwen3.7-plus`; the fast utility-loop role (`gen-flash`) → `qwen3.5-plus` (remapped in v1.1.5 from `deepseek-v4-flash`, which was `open-reason-lite`'s target, so the two no longer collapse when they share a chain; `qwen3.5-plus` keeps `gen-flash` on the `opencode` gateway matching its `ProviderB` placeholder). In the high-stakes fallback slots on `oracle`/`momus`/`prometheus` where the retired model was a *capability safety rung*, it was promoted to the strongest model not already in that chain (`deepseek-v4-pro`, else `glm-5.3`, else `gpt-5.6-terra`) rather than a flat generalist swap.
- `grok-flagship` (`xai/grok-4.6`) is an **ultimate-only** diversification fallback on `atlas` and `prometheus` — **not** `hephaestus`, which carries **no diversification-vendor rung**: its chain is a flagship-native primary tier plus the single documented open-weight lifeline (`open-reason-xl`) and, where set, a flagship-coder `ultrawork` escape hatch. Grok trails the stack's primaries on role-relevant benchmarks ([Terminal-Bench 2.1 83.3 vs kimi-k3 88.3 / deepseek-0813 87.9 / glm-5.3 88.2](https://www.tldevtech.com/grok-45-benchmarked-where-it-actually-wins)) but adds an independent 5th vendor (xAI) and is very token-efficient ([~16k output tok/task vs Opus 4.8's ~67k](https://hokai.io/hub/models/grok-4.5)). Priced [$2/$6 per 1M](https://benchlm.ai/xai/api-pricing) — the $6 output exceeds the $4.65/1M policy budget cap (see the cap note below), hence ultimate only.
- `open-coder` (`opencode/mimo-v2.5-free`) is Xiaomi's MiMo, a [1T-param open-weight MoE coder that matches frontier coding benchmarks at 40-60% fewer tokens](https://codersera.com/blog/xiaomi-mimo-v2-5-coding-model-2026/) (MIT). It is wired as a coding/open fallback rung in `deep` (all profiles), on `atlas`/`sisyphus-junior` open backups, and in `b4b`'s cost-preferenced `unspecified-low` — chosen for token efficiency, exactly what a resilience rung should optimize for. The full deployable example (`examples/omo.full.example.json`) uses `mimo-v2.5-pro` via the tokeness relay instead of the Zen `-free` tier.
- `creative-mid` was remapped in v1.1.5 from `qwen3.7-plus` to `muse-spark-1.2` so it stays distinct from **both** `gen-pro` (`qwen3.7-plus`) and `retrieval-mid` (`qwen3.6-plus`) — an intermediate fix to `qwen3.6-plus` would have merely traded the `gen-pro` collision for a `retrieval-mid` one, so a genuinely distinct creative model was chosen.
- Provider `apiyi` is a proxy used here because some flagship models are geo-locked; substitute your own gateway.

### The $4.65/1M policy budget cap

The cost-capped profiles (`hybrid`, `b4b`) hold their **generalist / utility / orchestration** rungs to an **output price at or below $4.65 per 1M tokens** (named exempt slots — the flagship coding tier, the architect, and `ultrawork` — may exceed it; see the exemption table below). This is a **policy budget number chosen for this repo — not any single vendor's list price.** In particular it is **not** the price of `coder-xl` (kimi-k3): Moonshot lists [kimi-k3 at $3 in / **$15 out** per 1M](https://www.usagepricing.com/blueprint/moonshot-ai), far above the cap. `coder-xl` is an **explicitly exempt** flagship-coding rung (see the exemption table below), not a capped generalist rung; the $4.65 ceiling is what keeps the *non-exempt* metered rungs anchored near the mid-coder tier (kimi-k2.7-code ≈ [$0.95 / $4.00](https://costgoat.com/pricing/kimi-api)). Treat $4.65 as an editable budget knob: raise or lower it and re-audit each rung's published output price against the new value. All "under cap" / "exceeds cap" statements in this file are measured against this $4.65 policy number, using each model's **published unit output price** (not blended or per-task cost).

**The cap is a preference for the cheap tiers, not a hard per-slot ceiling.** It governs generalist / utility / orchestration rungs. Deliberately **exempt** slots may carry an over-cap model:

| Over-cap model (output $/1M) | Where it appears in the metered profiles | Why exempt |
|---|---|---|
| `coder-xl` = kimi-k3 ($15) | `hybrid`: `prometheus`/`atlas` primaries, `deep`[1], `ultrabrain`[2], `hephaestus.ultrawork`. `b4b`: `deep`[1] only | Flagship coding tier on the hardest implementation work; `b4b` keeps it only as a deep-category fallback |
| `reasoner-xl` = claude-opus-5 (uncapped tier) | `ultimate` only | Not used in metered profiles |
| `flagship-open` = qwen3.8-max ($6) | `ultimate` only | Adds no capability the exempt coder lacks — kept out of metered profiles |
| `div-flagship` = grok-4.6 ($6) | `ultimate` only | Diversification vendor — kept out of metered profiles |

Every **other** metered-profile rung resolves to a model at or under $4.65 output. `.github/checks.py` enforces this: a placeholder tagged over-cap in this table's exemption list may appear in `hybrid.json`/`b4b.json` only in its listed exempt slots; any over-cap placeholder **not** on the exempt list fails the build if it lands in a metered profile.
