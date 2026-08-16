# Implementation Plan — model-mesh on the DeepSeek Harness (Path D)

Status: **proposal.** Only **Phase 0 (a spike)** is approved to run as written; Phases 1–4 are re-planned *after* Phase 0 reports, because they depend on facts Phase 0 must first establish. This plan was hardened after an independent adversarial review (6 critical / 10 major findings); the review is summarized in [§11](#11-review-response).

Target: the **DeepSeek Harness** (`dsh`), a Cordis-powered "everything is a plugin" TypeScript runtime, currently **developer preview — its README warns of compatibility-breaking changes** ([repo](https://github.com/deepseek-ai/deepseek-harness)).

---

## 1. Goal

Run model-mesh's two assets on `dsh` **without** maintaining a second copy of the config by hand and **without** hand-writing throwaway code against a preview API:

1. the **routing** (which model/role handles what), today expressed as `profiles/*.json`;
2. the **method loop** (think / act / prove / grow with its gates), today four `SKILL.md` files.

## 2. Approach: harness-neutral core + a per-harness adapter

Factor the repo so model-mesh content is a single source of truth, and each harness gets a small **adapter** that compiles that source into the harness's format. DSH becomes one adapter. This mirrors OmO's own stated refactor (pure-TS core + per-harness shims; [OmO](https://github.com/code-yeongyu/oh-my-openagent)).

### Honest comparison (rescored after review)

The earlier draft's table was rigged: it credited "core + adapter" with "survives breaking changes" while ignoring that the adapter itself is DSH-coupled. Corrected:

| Property | MCP-only | Native plugin | Profile-only + skills | **Core + adapter (this plan)** |
|---|---|---|---|---|
| DSH-coupled artifacts that break on schema/event churn | MCP mount row | whole plugin | patch rows | **patch rows + (later) runtime plugin** |
| Harness-neutral part that never changes | n/a | `core/`¹ | `core/`¹ | **`core/`** |
| Single source of truth across OmO + DSH | no | possible¹ | possible¹ | **yes (enforced by generator)** |
| Routing on DSH now | no | yes | yes | **yes (generated patch)** |
| Method loop on DSH now | retrievable text | full | as skills | **retrievable text + skills** |
| Effort | low | high | low | **medium** |

¹ A native plugin or a hand-kept profile *could* also read `core/`; the honest differentiator of this plan is that the generator **enforces** single-source and gives drift-protection, not that only it can be neutral.

Truthful summary: this plan ≈ **profile-only + skills + an MCP for retrievable loop text**, plus an `adapters/` boundary that makes a future native plugin incremental instead of a rewrite. It does **not**, in the near-term scope, deliver runtime fallback behavior or gate *enforcement* inside DSH (see §5, §6).

## 3. Confirmed facts (with sources)

- A dsh/Cordis plugin is a TS module exporting `name` / `inject` / `apply(ctx)` (+ optional Schemastery `Config`); services (`ctx.llm`, `ctx.tools`, `ctx.agents`) are consumed via `inject` ([services](https://deepseek-harness.github.io/deepseek-harness/en/develop/framework/service)).
- Distribution: a **bundle** (npm package whose `package.json` carries a `dsh.bundle` manifest → a `cordis.patch.yml`) composed into a **profile** (`dsh.profile`, ordered `bundles`). Layer precedence: **bundle patches (lowest) → profile patch → home patch → `--patch` (highest)** ([publish](https://deepseek-harness.github.io/deepseek-harness/en/develop/basic/publish)).
- Install is profile-scoped and forwards to pnpm: `dsh plugin --profile web add …` ([plugins](https://deepseekdocs.com/en/docs/user-guide/plugins)).
- Registrations are effects, reversible on unload; a plugin waits (PENDING, no error) until injected services exist ([lifecycle](https://deepseek-harness.github.io/deepseek-harness/en/develop/cordis-tutorial/)).
- **Loader footgun:** namespace exports only; **no `export default`** (incl. `export { apply as default }` and bundler CJS-interop defaults), or the loader discards the namespace and `apply` runs with no injected services.
- **Cordis is vendored** as `@deepseek-ai/cordis`; a bundle depending on upstream `cordis` gets a *second kernel*, and its services silently never inject.
- **Config authority for a preview is the generated catalog**, `reference/config-catalog` (produced by the repo's own `gen-config-catalog` and verified in its CI) — trust it over prose docs.

### Open unknowns — MUST be answered by Phase 0, not assumed

U1. Does DSH have a **named-agent registry with a dispatcher**, or are agents created per-session by an `AgentFactory`/`AgentLoop`? (Determines whether 11 role rows are dispatchable or inert.)
U2. Is there any **router / provider-failover / fallback** plugin in the catalog, or is agent config a **singular** `provider`+`model` only?
U3. Is **reasoning effort** a config field anywhere?
U4. Can a **bundle-layer** patch mount an MCP, or must the MCP row live in the **home** patch (the only documented example puts it there)?
U5. Do **pre-action events** (something like `agent/pre-step`) exist that could enforce a gate? (Hook names must be read from the pinned source, not assumed.)
U6. **`prompt_append` / persona** mapping target (e.g. a system-prompt/persona plugin, `toolOrder`).

## 4. Kill-criteria (decide BEFORE coding Phases 2–4)

Phase 0 is a real gate only if each "no" has a pre-agreed consequence. Gate on a **signed decision against this table**, not on a file existing.

| Unknown | If the answer is "no / absent" | Consequence |
|---|---|---|
| U1 named-agent registry | agents are factory-created | Phase 2 ships a **single** model-mesh agent + a documented gap; the 11-role mapping moves to Phase 4 |
| U2 fallback/router plugin | singular provider+model only | **Fallback parity is Phase 4.** Phase 2 emits **primaries only** + `LIMITATIONS.md` |
| U3 reasoning field | absent | drop `reasoning`/effort from generated output; record in `LIMITATIONS.md` |
| U4 bundle can mount MCP | only home patch can | the MCP ships as a **documented user-patch snippet**, not a bundle row |
| U5 pre-action event | absent | **drop `adapters/dsh/runtime` from scope**; the loop stays advisory (retrievable text) |
| U6 persona target | absent | `prompt_append` is dropped or inlined into skill text; record in `LIMITATIONS.md` |

If U1="factory" **and** U2="none", Path D's Phase 2 collapses into Phase 4 work — **re-plan before coding**, do not patch.

## 5. Target structure & distribution

```
core/                       # single source of truth (a real neutralization — see Phase 1)
  ir/profiles/              # ultimate/hybrid/b4b in the NEUTRAL IR (not opencode's schema)
  ir/schema.json            # the one JSON Schema = single source of shape truth
  skills/  references/      # method loop content (harness-neutral prose)
adapters/
  opencode/generate.py      # existing OmO output, refactored to read core/ir (byte-parity gate)
  dsh/
    generate.py             # PYTHON: core/ir -> cordis.patch.yml + package.json(dsh.bundle)
    overlay.yml             # tracked, generator-merged: legit DSH-only settings (timeouts, sandbox)
    golden/                 # checked-in expected cordis.patch.yml per profile (regen-and-diff in CI)
    verify.sh               # dsh --profile web --dump-config; assert each mm-* row present & un-overridden
    runtime/                # ONLY if U5=yes: thin Cordis plugin (namespace exports; no default)
mcp/mm-loop-server/         # harness-neutral MCP: loop text retrievable as mcp__mm-loop__* tools
docs/dsh/
  PLAN.md                   # this file
  PHASE0-FINDINGS.md        # signed answers to U1..U6 + pinned dsh revision (Phase 0 deliverable)
  LIMITATIONS.md            # every unmapped field, per the kill-criteria outcomes
```

**Distribution (resolves the "git-ignored dist can't install" contradiction).** Chosen mechanism, to be proven in Phase 2 with a pasted install transcript: **CI regenerates the bundle and pushes it to a dedicated `bughunt8/model-mesh-dsh` repo whose bundle files are committed** (so `dsh plugin add github:bughunt8/model-mesh-dsh` resolves real files), while this repo keeps only the *generator* and *golden* files. Drift is caught by a regenerate-and-diff CI step in both repos. (Alternatives considered and rejected for now: npm publish — adds registry ownership; local-path only — not shareable.) `dist/` in *this* repo stays git-ignored and is never the install source.

## 6. Phases

### Phase 0 — De-risk the preview (spike; ~0.5–1 day; produces a decision, not product)
Pin a `dsh` commit. Clone, `pnpm install`, `pnpm run build`, `pnpm dsh web`; confirm boot. Build the tutorial `hello` plugin via `--patch` to confirm the loader contract on this revision. Read the **generated** `reference/config-catalog` at the pinned hash and answer **U1–U6 in writing**. Verify cordis identity (peer-dep on `@deepseek-ai/cordis`; no duplicate kernel).
Deliverable: `docs/dsh/PHASE0-FINDINGS.md` — the U1–U6 answers, the pinned revision, the catalog file hash — **and a signed go/no-go decision against §4**. Gate: no Phase 2–4 work until that decision is recorded.

### Phase 1 — Real neutralization (refactor; no behavior change)
- Define a **neutral IR** with named semantics: `role`, `persona/prompt-family`, ordered `model-preference` list, `effort`, `orchestration-slot` (root/sub/ultrawork), `category→capability-class`. This is *not* opencode's object with names blanked.
- Write the **impedance table** `IR ↔ opencode` and `IR ↔ DSH`, each with an `unmappable` column. **If the `IR ↔ DSH` column can't be filled from Phase 0, Path D is not yet shown to exist — stop.**
- Port the OmO generator to read `core/ir` and emit byte-identical `[opencode]` output (CI byte-parity step, exact command, covering the three `*.example.json` variants too).
- Rewrite `.github/checks.py` to be **path-agnostic** (globs, not hardcoded `profiles/<x>.json`), validate profiles against the **one** `core/ir/schema.json` (retire the imperative shape rules so there's no second schema), drive `is_example()` by suffix/config, and add **negative fixtures** (a knowingly-bad IR that must fail) so the gate is proven live after the move.
- Back-compat: use **forwarding stub files or a copy step, not symlinks** (Windows `install.ps1`, marketplace `source: "./"`, and `os.walk` not following links make symlinks unsafe); CI asserts both old and new paths resolve on a symlink-less checkout.
Deliverable: green CI, OmO output byte-unchanged, impedance table published.

### Phase 2 — DSH config adapter (Python generator → the routing)
- `adapters/dsh/generate.py` maps IR → DSH rows **per the Phase 0 answers and kill-criteria** (single agent vs roster per U1; **primaries only** unless U2 says otherwise). Emits `cordis.patch.yml` + `package.json` (`dsh.bundle`), merging tracked `overlay.yml`. All op `id`s namespaced `mm-*`.
- Placeholders only in committed files (`ProviderA/…`); real IDs via local `provider-map.local` at generate time, never committed — consistent with the repo rule and the denylist gate.
- Distribution per §5; **pasted install transcript** is part of the deliverable.
- `verify.sh` runs `dsh --profile web --dump-config` and asserts each `mm-*` row is present **and un-overridden** (bundle layer is lowest precedence — collisions must fail, not eyeball).
Deliverable: on the pinned revision, a **stub/fake-provider** profile boots and `--dump-config` shows the intended `mm-*` rows; golden files diff-clean in CI.

### Phase 3 — The loop as an MCP (retrievable text, not enforcement)
- `mcp/mm-loop-server` exposes loop entrypoints as MCP tools returning the SKILL text. Harness-neutral (OmO and other editions reuse it).
- The generated patch (or documented home-patch snippet per U4) mounts it; set `toolCallTimeoutMs` **explicitly** (default 60s is too low for a VERIFY run) and do a **tool-name-agnostic** pass of the skill text (DSH bridges tools namespaced as `mcp__server__*`).
Deliverable (falsifiable): in a `dsh` session, `mm-method` / `mm-verify` / plan/audit/report text is retrievable via `mcp__mm-loop__*`, and a transcript shows the checklist applied. **Explicitly NOT delivered here:** pre-action gate enforcement, subagent fan-out, or diff-as-ground-truth — an MCP returns text and cannot preempt the next step. Those are Phase 4.

### Phase 4 — Native depth (deferred until DSH leaves preview)
Native `ctx.agents`/`ctx.llm` registration for live behavior: the 11-role roster (if U1 needed it), **runtime fallback** (error-class retry + cooldown + notify — this is real work, not "thin"), reasoning effort, persona mapping, and true gate enforcement against `AgentLoop`/`AgentFactory`/pre-step events. Gated on API stability. **Fallback and enforcement live here — they are not claimed earlier.**

## 7. Effort (honest)

Phase 0: 0.5–1d. Phase 1 (IR + impedance + CI rewrite + parity + negative fixtures): 3–5d. Phase 2 (generator + distribution repo + golden + verify): 3–5d. Phase 3 (MCP + wiring): 2–3d. Plus docs/version bumps and applying model-mesh's own gates to this work. Realistic total to the §8 criteria: **~2–3 person-weeks**, single-maintainer. The earlier "~1 week" was not credible. If ~1 week is required, cut scope to: Phase 0 + skills/MCP reachable in dsh + primaries-only patch + documented gaps.

## 8. Success criteria (measurable)

1. One edit to `core/ir/profiles/hybrid.*` regenerates **both** the OmO config (byte-parity CI) **and** the DSH golden bundle (regenerate-and-diff CI) with no hand editing.
2. On the pinned revision, a **stub-provider** profile boots and `dsh --dump-config` snapshot shows the expected `mm-*` rows (runs without secrets). *(Real-provider boot is a separate manual gate with a named signer and a recorded transcript, because placeholders can't resolve a real adapter.)*
3. Loop text is retrievable via `mcp__mm-loop__*` in a `dsh` session; a saved transcript shows the checklist applied. *(Enforcement is explicitly Phase 4.)*
4. Denylist CI is green across `core/`, `adapters/`, `mcp/`, including the new self-test; no real provider/model IDs in any committed file.
5. `PHASE0-FINDINGS.md` (signed decision + pinned revision + catalog hash) and `LIMITATIONS.md` exist and match what's shipped.

## 9. Risks & mitigations

- **DSH breaking changes (high).** Adapter is generated + thin; `core/` never changes. Pin the revision + catalog hash; re-run Phase 0 checks on upgrade before regenerating.
- **`export default` footgun (high impact).** Runtime plugin (if any) uses namespace exports; CI asserts on the **built** artifact (load it, fail if a `default` key exists), backed by an injection smoke test inside `apply()`.
- **Duplicate cordis kernel (silent PENDING).** Peer-dep on `@deepseek-ai/cordis`; pnpm resolution check for duplicate kernels; `apply()` smoke-test asserts each injected service is defined.
- **Config schema differs from assumption (medium).** Phase 0 kill-criteria; no Phase 2 code before the signed decision.
- **Lowest-precedence bundle silently overridden (medium).** `mm-*` id namespacing + `verify.sh` un-overridden assertion.
- **Placeholder/real-ID leak (medium).** Generator keeps placeholders; local-only substitution; denylist self-test in CI.
- **Two-source drift (medium).** Golden files regenerated-and-diffed in CI; hand edits fail; legit DSH-only settings go through tracked `overlay.yml`, not hand edits.
- **New Node/TS toolchain vs the repo's Python+bash + "never add a dependency" rule (medium).** Config generator is **Python**; TS confined to the runtime plugin *if it survives Phase 0*; any dep needs explicit authorization + `THIRD_PARTY_NOTICES.md` entries + a CI job.

## 10. Out of scope (now)

Runtime fallback behavior, gate enforcement inside DSH, the full 11-role native roster, publishing to a public registry, and any change to the model-mesh method itself. All either Phase 4 or non-goals.

## 11. Review response

An independent adversarial model (run separately from the author) raised 6 critical + 10 major findings against the first draft. Resolutions folded into this version: the release-gate collision (narrow allowlist + build-dir exclusion + negative self-test landed in `.github/checks.py`; plan moved out of the harness-named dotfolder to `docs/dsh/`); the un-installable "git-ignored dist" (dedicated bundle repo, §5); Phase 0 made a signed kill-criteria decision (§4) instead of a file-existence gate; dropped the false claims of fallback parity and MCP gate-enforcement (moved to Phase 4; Phase 3 is retrievable text only); replaced the "rename" core with a real neutral IR + impedance table (Phase 1); path-agnostic CI with one schema + negative fixtures; Python generator instead of TS; vendored-cordis peer-dep + injection smoke test; built-artifact `default`-export check; and a corrected, non-rigged comparison table (§2) with a realistic 2–3 person-week estimate (§7).
