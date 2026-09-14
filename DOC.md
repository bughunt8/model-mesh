# model-mesh: plain-language explainer

**model-mesh** is two things in one repo:

1. **A method** any model can follow to do work carefully: figure out what's really being asked, decide what "done" looks like, gather real evidence, make the smallest correct change, verify by actually running/observing it, and report the outcome first with honest caveats. This is the "loop", shipped as four skills: think (`mm-method`), act (`mm-loop`), prove (`mm-verify`), grow (`mm-domain`).

2. **A way to route work across many models.** Instead of using one model for everything, each agent role (implementer, architect, reviewer, orchestrator, coder, utility) is matched to the *kind* of model that fits it. Three ready profiles express different cost/quality preferences: `ultimate` (max capability), `hybrid` (the default), and `b4b` (leans cheaper).

## Why route at all?

Modern models are close enough that "use the best one" is no longer obviously right. A very capable model can still be the wrong default for a given role once you weigh cost, verbosity, latency, and behavior. Routing encodes those trade-offs so the choice is deliberate, not accidental. These are **design heuristics**, not benchmark guarantees. The repo ships no eval data and makes no fixed quality/cost promise (your results depend on which real models you map in).

## Model-agnostic by design

Every model and provider name is a placeholder (`ProviderA`, `flagship-xl`, …). You map them to whatever you run. The method is also **harness-agnostic**. It works on any coding-agent harness, and the repo ships concrete configuration examples for two: **OpenCode** (via oh-my-openagent) and the **DeepSeek Harness**. The only real product names kept are the harness examples' own required identifiers: `oh-my-openagent` and `opencode` for the OpenCode example (its config must contain them to load), and the DeepSeek Harness keeps its own `settings.yaml` keys. These are framework identifiers, not model names.

## Getting started

See the README Quickstart (human and LLM versions). Short path: `./setup-config.sh hybrid`, map placeholders in `~/.omo/omo.jsonc`, run `bunx oh-my-openagent doctor`.

This package is version 1.0.0.
