# Third-Party Notices

## fable-method (MIT)

The loop skills in `skills/` (`mm-method`, `mm-loop`, `mm-verify`, `mm-domain`) and the
`install.sh` / `install.ps1` scripts are **adapted from and integrated with**:

- Project: fable-method
- Author: Sahir619
- Source: https://github.com/Sahir619/fable-method
- License: MIT

Changes made in model-mesh:
- Skills renamed from the upstream fable-method naming to `mm-*`, and command names updated.
- All real model/provider names removed and replaced with behavioral descriptions.
- The bundled `eval/` trap-suite and its data were **not** included in this repo.
- Documentation rewritten for model-mesh.

The upstream MIT copyright is retained in `LICENSE`. This notice fulfills the MIT
attribution condition for the copied portions.

## oh-my-openagent

The routing configs target the oh-my-openagent / opencode framework
(https://github.com/code-yeongyu/oh-my-openagent). The strings `oh-my-openagent`,
`opencode`, the `[opencode]` config key, and the schema URL are that framework's
real identifiers, intentionally retained so the config loads. They are not vendor
model names.
