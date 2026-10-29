# Config Changes — v1.0

Every change from the reviewed `omo.jsonc` to `configs/omo.recommended.jsonc`.
Severity: **B** = blocking (invalid or non-functional), **H** = high (wrong
behaviour), **M** = medium (suboptimal), **L** = low (cosmetic).

## Structural

| # | Sev | Change | Rationale |
|---|---|---|---|
| 1 | B | Added missing `}` closing `agents` before `categories` | The reviewed file had unbalanced braces; `categories` was nested inside `agents` and the JSON was invalid |
| 2 | B | Removed duplicate `prompt_append` in `sisyphus` | Two keys with the same name; the second (short) value won in JSON, discarding the entire operating contract |
| 3 | H | Moved `temperature` from per-entry to agent level where applicable | Per-entry temperature means every other rung runs at provider defaults (0.7–1.0), wrong for orchestrators and gates |
| 4 | H | Added `temperature: 0.1` to `momus` | Documented default for consistent, objective review; was absent |

## Dead or unverified model IDs

| # | Sev | Slot | Change | Rationale |
|---|---|---|---|---|
| 5 | B | `sisyphus-junior[2]` | `tokeness/deepseek-v4.1-flash` → `tokeness/deepseek-v4-flash` | No canonical `deepseek-v4.1-flash` ID exists; Tokeness lists `deepseek-v4-flash` |
| 6 | B | `sisyphus[1]` | `tokeness/MiniMax-M3` → `minimax/MiniMax-M3` | Tokeness catalog does not include MiniMax |
| 7 | B | `explore[4]` | `packyapi/gemini-3.7-flash` at `max` → `tokeness/gemini-3.7-flash` at `high` | PackyAPI's indexed Gemini listings show 3.5/3.6/preview, not 3.7; and `max` is not a valid Gemini 3.7 tier |
| 8 | B | `explore[5]` | `zai-coding-plan/glm-5.3-flashx` → `zai-coding-plan/glm-5.3-flash` | FlashX is not available on the Coding Plan; only `glm-5.3-flash` is |
| 9 | B | `prometheus[4]` | `packyapi/gemini-4-argon` → `tokeness/gemini-4-argon` | PackyAPI availability unverified; Tokeness listing confirmed |
| 10 | H | `librarian` | Swapped slots 1 and 2: `gemini-3-flash` first, `deepseek-flash` second | Gemini 3 Flash is the documented default and has the stronger CR score |

## Capability and diversity

| # | Sev | Slot | Change | Rationale |
|---|---|---|---|---|
| 11 | H | `atlas` | Promoted `claude-sonnet-5-5` to slot 1; Kimi K3 → slot 2; `glm-5.3-flash` → `claude-haiku-5-5` | K3's TB4 12.6 and tool-call repeat bug are wrong for a todo orchestrator; GLM-5.3-Flash has the lowest SkillsBench in the roster |
| 12 | H | `momus` | Replaced `packyapi/gpt-6.1-sol` duplicate with `tokeness/claude-opus-5-5` | PackyAPI historical function-calling 7–20%; Opus has the highest Toolathlon score |
| 13 | H | `prometheus` | Replaced `packyapi/claude-sonnet-5-5` duplicate with `tokeness/claude-opus-5-5` | Diversity instead of redundancy |
| 14 | H | `metis` | Replaced `packyapi/claude-sonnet-5-5` with `tokeness/gemini-4-argon` | Different family; Argon's AA 53 ties Astra at lower cost |
| 15 | M | `hephaestus[2]` | `gpt-6-astra` from `medium` → `low` | At medium, Astra scores TB4 49.5 vs Sol high's 54.0 at 3× the cost |
| 16 | M | `sisyphus-junior[5]` | `glm-5.3-flash` → `tokeness/gpt-6-luna-fast` at `low` | Removes the −15 CXR penalty; Luna-fast is the documented quick-tier floor |

## Categories

| # | Sev | Change | Rationale |
|---|---|---|---|
| 17 | B | Added `architect` | Missing key silently falls through to built-in defaults on first-party provider lanes |
| 18 | B | Split `deep` into `deep-low` and `deep-high` | `deep` is a deprecated alias on a removal clock |
| 19 | H | `ultrabrain` head → `gpt-6-astra` at `max`; added Opus 5.5 at `max` | Documented head; Sol high is a tier below the ceiling |
| 20 | H | `visual-engineering` head → `claude-opus-5-5` at `max`, `temperature: 0.7` | Category is frontend code taste, not image QA |
| 21 | H | `artistry` head → `claude-opus-5-5` at `xhigh`, `temperature: 0.7` | Same rationale; no creative-coding specialist in roster |
| 22 | H | `quick[1]` → `tokeness/gpt-6-luna-fast` at `low` | Qwen3.8-Max is a 66-second flagship in the trivial lane |
| 23 | H | `writing` head → `kimi-k3` at `low`; Qwen → slot 3 at `medium` | Qwen's instruction-following rank is #36; wrong for a prose contract |
| 24 | M | Added `description` to every category | Surfaced in the task prompt; improves routing |
| 25 | M | `unspecified-low` head → `claude-sonnet-5-5` at `medium` | Matches the v5.1.1 documented default |

## Runtime

| # | Sev | Change | Rationale |
|---|---|---|---|
| 26 | H | `timeout_seconds` 30 → 120 | Argon TTFT is 28.14s; Astra and Opus per-task times exceed 200s. At 30s, middle rungs never finish |
| 27 | M | `staleTimeoutMs` 60s → 180s | Matches the raised timeout |
| 28 | M | `max_fallback_attempts` → 6 | Six-rung chains need at least six attempts to be reachable |

## Not changed

- `allow_non_gpt_model: true` on Hephaestus — required for the Argon floor; keep.
- `_migrations` — retains the existing migration marker.
- `team_mode`, `claude_code.hooks`, `background_task.providerConcurrency` — untouched.
