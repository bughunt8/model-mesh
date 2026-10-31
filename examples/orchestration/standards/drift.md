# Drift standard

Applies after authors finish and before acceptance. The reviewer receives the spec and the delivered change. It reports only differences. If there are none it answers exactly: No drift detected.

Check, in this order:

1. Each done criterion in the spec has matching code, configuration or test in the change. Report the ones that do not.
2. Each behavior in the change appears in the spec. Report the ones that do not. These are additions nobody approved.
3. Names, paths, limits and defaults agree between the spec and the change.
4. Anything the spec said to defer or exclude has not been built.

Each difference is one finding. Cite the spec line and the change line, quote both, and use the category spec-gap, consistency or correctness. Do not suggest redesigns. A difference is a blocker if a done criterion is unmet, major if behavior was added without approval, and a nit for naming.
