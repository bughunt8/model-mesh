#!/usr/bin/env python3
"""Wrap a profile fragment (agents+categories) into a complete deployable omo.jsonc.
Usage: materialize.py <fragment.json> <profile-name>  ->  prints full config to stdout.
Framework note: the "[opencode]" key and schema URL are the REAL oh-my-openagent
framework identifiers, intentionally kept so the file loads. Model/provider names
are placeholders you must map (see docs/PROVIDERS.md)."""
import json, sys
from collections import OrderedDict

frag_path, profile = sys.argv[1], sys.argv[2]
frag = json.load(open(frag_path), object_pairs_hook=OrderedDict)

deploy = OrderedDict()
# Pinned schema tag for reproducibility (see docs/PROVIDERS.md "Framework compatibility").
deploy["$schema"] = "https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/v4.19.4/assets/omo.schema.json"
oc = OrderedDict()
oc["team_mode"] = OrderedDict([("enabled", True), ("tmux_visualization", False)])
oc["agents"] = frag["agents"]
oc["categories"] = frag["categories"]
oc["background_task"] = OrderedDict([
    ("defaultConcurrency", 3), ("staleTimeoutMs", 60000),
    ("providerConcurrency", OrderedDict([("ProviderB", 10), ("ProviderD", 10)])),
])
oc["runtime_fallback"] = OrderedDict([
    ("enabled", True),
    ("retry_on_errors", [429, 503, 529]),   # 400 removed: not a transient error
    ("max_fallback_attempts", 3), ("cooldown_seconds", 60),
    ("timeout_seconds", 30), ("notify_on_fallback", True),
])
deploy["[opencode]"] = oc

header = f"// model-mesh deployable config — {profile} profile\n" \
         f"// Placeholder model/provider names must be mapped (see docs/PROVIDERS.md).\n" \
         f"// '[opencode]' and the schema URL are the real oh-my-openagent framework identifiers.\n"
sys.stdout.write(header + json.dumps(deploy, indent=2) + "\n")
