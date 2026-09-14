# Contributing to model-mesh

Thanks for helping. Two ground rules keep this repo shippable:

1. **No real model/provider names.** CI (`.github/checks.py`) fails the build if any real vendor/model name appears in file contents or paths. The messaging is **harness-agnostic**. The method targets any coding-agent harness, and the repo ships examples for two (**OpenCode** via oh-my-openagent, and the **DeepSeek Harness**). The names `oh-my-openagent` and `opencode` are allowed because they are the OpenCode example's required framework identifiers (not model names); the DeepSeek Harness example keeps its own required identifiers too. Use placeholders (`ProviderA`, `flagship-xl`, …) for everything else. (Real model IDs are permitted only in `docs/EXAMPLE-MAPPING.md` and `docs/research/`, which are denylist-exempt.)
2. **Configs must validate.** Agents use `model` + `fallback_models` (never `models`); `ultrawork` uses a singular `model`; categories use `models[]`; use `reasoning` not `variant`. Run the checks below before opening a PR.

## Before you open a PR

```bash
python .github/checks.py         # denylist + manifest + skill + profile-shape + link checks
./setup-config.sh hybrid         # materialize succeeds for each profile
bunx oh-my-openagent doctor      # if you changed configs and have the framework installed
```

Run the loop's own reviewer on your change: `/mm-verify`.

## What lives where

- `skills/`: the loop (adapted from fable-method, MIT; see `THIRD_PARTY_NOTICES.md`). Keep changes here in sync with the loop's intent.
- `profiles/`: routing fragments. If you change a profile, update the README "Profile at a glance" table to match (CI checks profile validity; keep the prose honest).
- `docs/`: methodology and mapping guides.

## License

By contributing you agree your contributions are MIT licensed. New original work is © bughunt8; upstream portions remain © Sahir619.
