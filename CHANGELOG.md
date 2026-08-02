# Changelog

## 1.0.0
- Initial release of model-mesh.
- Loop skills adapted from fable-method (MIT; see THIRD_PARTY_NOTICES.md): think (mm-method), act (mm-loop), prove (mm-verify), grow (mm-domain).
- Multi-model routing layer for oh-my-openagent with three profiles: ultimate, hybrid (default), b4b.
- All provider/model names genericized to placeholders (docs/PROVIDERS.md). Framework names (oh-my-openagent, opencode) intentionally kept and documented.
- Safe setup: setup-config.sh materializes any profile into a complete, schema-valid config with backup; profiles ship as fragments.
- CI enforces a vendor-name denylist, manifest/skill/profile validation, and link checks.
- Privacy note added: cross-provider fallback data-boundary caveat; 400 removed from transient retries.
- Schema pinned to a released framework tag for reproducibility.
