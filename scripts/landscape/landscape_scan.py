#!/usr/bin/env python3
"""Deterministic, fail-closed landscape recommendation framework.

Weekly scan JSON is untrusted. Gate attributes come only from the committed
configuration, every hard gate emits PASS/FAIL, and missing evidence cannot
produce a recommendation.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import io
import json
import math
import os
import re
import sys
from copy import deepcopy

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DEFAULT_CONFIG = os.path.join(HERE, "sources.yaml")
PROVENANCE_LEVELS = {"independent", "vendor", "vendor_partner"}
BOOL_FIELDS = ("open_weights", "flagship_native_family", "reversal")
GATE_IDS = ("cap", "retired_vendor", "open_weight", "family_fit", "region_availability")
SCHEMA_TEXT = r'''Scan dataset schema (weekly input is UNTRUSTED):
{
  "scan_date": "YYYY-MM-DD",
  "incumbents": {
    "role": {
      "model": "ProviderX/role", "role_dimension": "intelligence",
      "value": 60, "provenance": "independent", "source": "URL or citation",
      "under_cap": true,
      "metrics": {"speed": {"value": 100, "provenance": "independent", "source": "citation"}}
    }
  },
  "models": [{
    "name": "candidate-A", "vendor": "providerx", "profile": "hybrid",
    "candidate_for_roles": ["role"],
    "open_weights": false, "flagship_native_family": false, "reversal": false,
    "differentiator": {"metric": "speed", "value": 120,
                       "provenance": "independent", "source": "citation"},
    "metrics": {"output_price": {"value": 1, "durable_value": 1,
                    "provenance": "vendor", "source": "rate card"}}
  }]
}'''


class ConfigError(RuntimeError):
    pass


class Finding:
    def __init__(self, level, msg):
        self.level, self.msg = level, msg

    def __repr__(self):
        return f"[{self.level}] {self.msg}"


def _payload_hash(cfg):
    body = deepcopy(cfg)
    body.pop("config_payload_sha256", None)
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(encoded).hexdigest()


def _verify_stamp(cfg, label):
    if not isinstance(cfg, dict):
        raise ConfigError(f"{label}: configuration root must be an object")
    expected = cfg.get("config_payload_sha256")
    actual = _payload_hash(cfg)
    if not isinstance(expected, str) or expected != actual:
        raise ConfigError(f"{label}: configuration stamp mismatch; run --sync-config")
    return cfg


def load_config(path):
    """Prefer PyYAML; use the stamped JSON mirror only when yaml is unavailable."""
    mirror = os.path.splitext(path)[0] + ".json"
    try:
        import yaml  # type: ignore
    except ImportError:
        try:
            with io.open(mirror, encoding="utf-8") as handle:
                return _verify_stamp(json.load(handle), mirror)
        except (OSError, json.JSONDecodeError) as exc:
            raise ConfigError(f"cannot load JSON mirror {mirror}: {exc}") from exc
    try:
        with io.open(path, encoding="utf-8") as handle:
            return _verify_stamp(yaml.safe_load(handle), path)
    except OSError as exc:
        raise ConfigError(f"cannot read YAML config {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise ConfigError(f"invalid YAML config {path}: {exc}") from exc


def sync_config(path):
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise ConfigError("--sync-config requires PyYAML") from exc
    try:
        with io.open(path, encoding="utf-8") as handle:
            cfg = yaml.safe_load(handle)
    except OSError as exc:
        raise ConfigError(f"cannot read YAML config {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise ConfigError(f"invalid YAML config {path}: {exc}") from exc
    if not isinstance(cfg, dict):
        raise ConfigError("configuration root must be an object")
    cfg["config_payload_sha256"] = _payload_hash(cfg)
    text = yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True)
    with io.open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    mirror = os.path.splitext(path)[0] + ".json"
    with io.open(mirror, "w", encoding="utf-8") as handle:
        json.dump(cfg, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return mirror


def _number(value, allow_bool=False):
    if isinstance(value, bool) and not allow_bool:
        return None
    if not isinstance(value, (int, float)):
        return None
    value = float(value)
    return value if math.isfinite(value) else None


def _durable_price(cell):
    if not isinstance(cell, dict) or "durable_value" not in cell:
        return None
    return _number(cell.get("durable_value"))


def _roles(model):
    return {str(role).casefold() for role in model.get("candidate_for_roles", [])}


def _cap_scope(model, cfg):
    pol = cfg["policy"]
    profile = str(model.get("profile", "")).casefold()
    roles = _roles(model)
    metered = {x.casefold() for x in pol.get("metered_profiles", [])}
    exempt = {x.casefold() for x in pol.get("metered_exempt_roles", [])}
    if profile not in metered:
        return set()
    return roles - exempt


def resolve_attributes(name, cfg):
    """Resolve trusted attributes; unknown models get worst-case values."""
    matches = []
    for row in cfg.get("model_attributes", []):
        try:
            if re.search(row.get("pattern", r"(?!)"), name, re.I):
                matches.append(row)
        except re.error:
            continue
    if len(matches) != 1:
        return {"open_weights": False, "flagship_native_family": False, "owner": None, "known": False}
    row = matches[0]
    owner = row.get("owner")
    return {
        "open_weights": row.get("open_weights") is True,
        "flagship_native_family": row.get("flagship_native_family") is True,
        "owner": str(owner).casefold() if isinstance(owner, str) and owner else None,
        "known": True,
    }


def validate_scan(scan, cfg):
    findings = []
    if not isinstance(scan, dict):
        return [Finding("ERROR", "scan root is not an object")]
    models = scan.get("models")
    if not isinstance(models, list):
        return [Finding("ERROR", "scan.models missing or not a list")]
    if not models:
        findings.append(Finding("ERROR", "scan.models must contain at least one model"))
        return findings
    known_roles = {x.casefold() for x in cfg["policy"].get("known_roles", [])}
    known_vendors = {x.casefold() for x in cfg["policy"].get("known_vendors", [])}
    known_profiles = ({x.casefold() for x in cfg["policy"].get("metered_profiles", [])}
                      | {str(cfg["policy"].get("ultimate_profile", "ultimate")).casefold()})
    names = set()
    for index, model in enumerate(models):
        if not isinstance(model, dict):
            findings.append(Finding("ERROR", f"models[{index}] is not an object"))
            continue
        name = model.get("name")
        label = name if isinstance(name, str) and name else f"models[{index}]"
        for req in ("name", "vendor", "profile", "candidate_for_roles", "metrics"):
            if req not in model:
                findings.append(Finding("ERROR", f"{label}: missing '{req}'"))
        if not isinstance(name, str) or not name.strip():
            findings.append(Finding("ERROR", f"{label}: name must be a non-empty string"))
        elif name.casefold() in names:
            findings.append(Finding("ERROR", f"{label}: duplicate model name"))
        else:
            names.add(name.casefold())
        vendor = model.get("vendor")
        if not isinstance(vendor, str) or vendor.casefold() not in known_vendors:
            findings.append(Finding("ERROR", f"{label}: vendor is not in closed known-vendor enum"))
        profile = model.get("profile")
        if not isinstance(profile, str) or profile.casefold() not in known_profiles:
            findings.append(Finding("ERROR", f"{label}: unknown profile '{profile}'"))
        roles = model.get("candidate_for_roles")
        if not isinstance(roles, list) or not roles:
            findings.append(Finding("ERROR", f"{label}: candidate_for_roles must be a non-empty list"))
        else:
            for role in roles:
                if not isinstance(role, str) or role.casefold() not in known_roles:
                    findings.append(Finding("ERROR", f"{label}: unknown role '{role}'"))
        for field in BOOL_FIELDS:
            if field in model and not isinstance(model[field], bool):
                findings.append(Finding("ERROR", f"{label}.{field}: must be a real boolean"))
        metrics = model.get("metrics")
        if not isinstance(metrics, dict):
            findings.append(Finding("ERROR", f"{label}.metrics: must be an object"))
            continue
        for metric, cell in metrics.items():
            if not isinstance(cell, dict) or "value" not in cell:
                findings.append(Finding("ERROR", f"{label}.{metric}: metric must be an object with value"))
                continue
            if cell.get("provenance") not in PROVENANCE_LEVELS:
                findings.append(Finding("ERROR", f"{label}.{metric}: invalid provenance"))
            if not isinstance(cell.get("source"), str) or not cell.get("source", "").strip():
                findings.append(Finding("ERROR", f"{label}.{metric}: non-empty source required"))
            if metric == "output_price":
                if "durable_value" not in cell:
                    findings.append(Finding("ERROR", f"{label}.output_price: durable_value is required"))
                elif _number(cell.get("durable_value")) is None:
                    findings.append(Finding("ERROR", f"{label}.output_price: durable_value must be numeric"))
        if _cap_scope(model, cfg) and _durable_price(metrics.get("output_price")) is None:
            findings.append(Finding("ERROR", f"{label}: no numeric durable output price for non-exempt candidate role"))
        diff = model.get("differentiator")
        if diff is not None:
            if not isinstance(diff, dict):
                findings.append(Finding("ERROR", f"{label}.differentiator: must be a structured object"))
            else:
                for req in ("metric", "value", "provenance", "source"):
                    if req not in diff:
                        findings.append(Finding("ERROR", f"{label}.differentiator: missing '{req}'"))
                if diff.get("provenance") != "independent":
                    findings.append(Finding("WARN", f"{label}.differentiator: non-independent evidence cannot affect verdict"))
    incumbents = scan.get("incumbents")
    if not isinstance(incumbents, dict) or not incumbents:
        findings.append(Finding("ERROR", "scan.incumbents must be a non-empty object"))
        return findings
    dims = cfg["rubric"]["dimensions"]
    for role, inc in incumbents.items():
        label = f"incumbents.{role}"
        if str(role).casefold() not in known_roles:
            findings.append(Finding("ERROR", f"{label}: unknown role"))
        if not isinstance(inc, dict):
            findings.append(Finding("ERROR", f"{label}: must be an object")); continue
        for req in ("model", "role_dimension", "value", "provenance", "source", "under_cap"):
            if req not in inc:
                findings.append(Finding("ERROR", f"{label}: missing '{req}'"))
        if inc.get("provenance") != "independent":
            findings.append(Finding("ERROR", f"{label}: provenance must be independent"))
        if not isinstance(inc.get("source"), str) or not inc.get("source", "").strip():
            findings.append(Finding("ERROR", f"{label}: source required"))
        if not isinstance(inc.get("under_cap"), bool):
            findings.append(Finding("ERROR", f"{label}: under_cap must be a real boolean"))
        dim = inc.get("role_dimension")
        if dim not in dims:
            findings.append(Finding("ERROR", f"{label}: unknown role_dimension '{dim}'"))
        categorical = dims.get(dim, {}).get("scale") == "categorical"
        if categorical:
            if not isinstance(inc.get("value"), bool):
                findings.append(Finding("ERROR", f"{label}.value: categorical dimension requires boolean"))
        elif _number(inc.get("value")) is None:
            findings.append(Finding("ERROR", f"{label}.value: numeric independent value required"))
        imetrics = inc.get("metrics", {})
        if not isinstance(imetrics, dict):
            findings.append(Finding("ERROR", f"{label}.metrics: must be an object"))
        else:
            for metric, cell in imetrics.items():
                if not isinstance(cell, dict) or cell.get("provenance") != "independent" or "value" not in cell or not cell.get("source"):
                    findings.append(Finding("ERROR", f"{label}.metrics.{metric}: independent value and source required"))
    return findings


def _reversal_verified(model, retired_tokens):
    """Verify reversal against repo deny/retirement guards and the changelog."""
    guard_paths = [os.path.join(ROOT, "scripts", "validate-full-config.py"),
                   os.path.join(ROOT, ".github", "checks.py")]
    try:
        guards = "\n".join(io.open(p, encoding="utf-8").read().casefold() for p in guard_paths)
        changelog = io.open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8").read().casefold()
    except OSError:
        return False
    still_guarded = any(re.search(r"\b" + re.escape(token.casefold()) + r"\b", guards)
                        for token in retired_tokens)
    reversal_entry = ("reversal" in changelog and
                      any(token.casefold() in changelog for token in retired_tokens))
    return not still_guarded and reversal_entry


def apply_hard_gates(model, cfg):
    pol = cfg["policy"]
    attrs = resolve_attributes(str(model.get("name", "")), cfg)
    roles = _roles(model)
    metrics = model.get("metrics") if isinstance(model.get("metrics"), dict) else {}
    gates = []

    scoped = _cap_scope(model, cfg)
    price = _durable_price(metrics.get("output_price"))
    cap = float(pol["budget_cap_output_usd_per_1m"])
    if not scoped:
        gates.append(("cap", True, "PASS: profile/roles are outside the metered non-exempt cap scope"))
    elif price is None:
        gates.append(("cap", False, f"FAIL: no durable output price for non-exempt roles {sorted(scoped)}"))
    else:
        passed = price <= cap
        gates.append(("cap", passed, f"{'PASS' if passed else 'FAIL'}: durable output ${price:g}/1M vs cap ${cap:g} for {sorted(scoped)}"))

    vendor = str(model.get("vendor", "")).casefold()
    name = str(model.get("name", ""))
    retired_tokens = [v for v in pol.get("retired_vendors", []) if vendor == str(v).casefold()]
    for pattern in pol.get("retired_model_patterns", []):
        try:
            if re.search(pattern, name, re.I):
                retired_tokens.append(pattern.strip("^$"))
        except re.error:
            retired_tokens.append(pattern)
    if retired_tokens:
        if model.get("reversal") is True and _reversal_verified(model, retired_tokens):
            gates.append(("retired_vendor", True, "PASS: reversal verified in repository guards and CHANGELOG"))
        elif model.get("reversal") is True:
            gates.append(("retired_vendor", False, "FAIL: reversal claimed but not verified in repo state"))
        else:
            gates.append(("retired_vendor", False, "FAIL: candidate matches retired vendor/model policy"))
    else:
        gates.append(("retired_vendor", True, "PASS: candidate does not match retired vendor/model policy"))

    required = roles & {x.casefold() for x in pol.get("open_weight_required_roles", [])}
    if required and not attrs["open_weights"]:
        gates.append(("open_weight", False, f"FAIL: curated attributes are proprietary/unknown for {sorted(required)}"))
    else:
        gates.append(("open_weight", True, "PASS: no open-weight role conflict" if not required else "PASS: curated open-weight attribute"))

    native_role = str(pol.get("flagship_native_only_agent", "")).casefold()
    if native_role in roles and not attrs["flagship_native_family"]:
        gates.append(("family_fit", False, "FAIL: curated attributes are non-flagship or unknown"))
    else:
        gates.append(("family_fit", True, "PASS: family-fit requirement satisfied or not applicable"))

    # region_availability: FAIL-CLOSED, identity-bound region policy. For a
    # region-locked profile (e.g. the HK-native `ultimate`), a candidate is
    # region-available ONLY if its curated owner (resolved from the trusted
    # model_attributes table by name, never from the scan's self-reported vendor)
    # is on that profile's allowlist. Everything else fails: an unresolved or
    # unknown identity, an owner not on the allowlist, or a scan vendor that
    # disagrees with the curated owner. This is what stops a mislabeled or
    # adversarial weekly scan from routing a geo-locked flagship into HK.
    region_owners = pol.get("region_available_owners", {}) or {}
    profile = str(model.get("profile", "")).casefold()
    if profile not in {str(p).casefold() for p in region_owners}:
        # Profile is not region-locked (hybrid/b4b stay global): no-op PASS.
        gates.append(("region_availability", True,
                      f"PASS: profile '{profile}' is not region-locked"))
    else:
        allowed = {str(o).casefold() for o in region_owners.get(profile, [])}
        owner = attrs.get("owner")
        if not attrs.get("known") or not owner:
            gates.append(("region_availability", False,
                          f"FAIL: identity for '{name}' is unresolved/unowned; region-locked profile '{profile}' fails closed"))
        elif vendor and vendor != owner:
            gates.append(("region_availability", False,
                          f"FAIL: scan vendor '{vendor}' disagrees with curated owner '{owner}' for '{name}'"))
        elif owner not in allowed:
            gates.append(("region_availability", False,
                          f"FAIL: owner '{owner}' developer API is not region-available for profile '{profile}'"))
        else:
            gates.append(("region_availability", True,
                          f"PASS: owner '{owner}' is region-available for profile '{profile}'"))
    assert [g[0] for g in gates] == list(GATE_IDS)
    return gates, attrs


def score_model(model, cfg):
    contribs, skipped = {}, []
    metrics = model.get("metrics", {})
    for dim, spec in cfg["rubric"]["dimensions"].items():
        cell = metrics.get(spec["source"])
        if not isinstance(cell, dict):
            skipped.append((dim, "no metric")); continue
        if cell.get("provenance") != "independent":
            skipped.append((dim, f"non-independent ({cell.get('provenance')})")); continue
        if spec.get("scale") == "categorical":
            if not isinstance(cell.get("value"), bool):
                skipped.append((dim, "categorical value is not boolean")); continue
            value = 1.0 if cell["value"] else 0.0
        else:
            value = _number(cell.get("value"))
            if value is None:
                skipped.append((dim, "non-numeric")); continue
            if spec.get("scale") == "log10":
                if value <= 0:
                    skipped.append((dim, "log-scale value must be positive")); continue
                value = math.log10(value)
        contribs[dim] = {"value": value, "raw_value": cell.get("value"),
                         "weight": float(spec["weight"]),
                         "higher_is_better": spec.get("higher_is_better", True)}
    return {"contribs": contribs, "skipped": skipped, "normalization": {}}


def normalize_and_total(scored_models, cfg):
    dims = cfg["rubric"]["dimensions"]
    ranges = {}
    for dim in dims:
        values = [m["score"]["contribs"][dim]["value"] for m in scored_models
                  if dim in m["score"]["contribs"]]
        ranges[dim] = (min(values), max(values), len(set(values))) if values else None
    for model in scored_models:
        total = wsum = 0.0
        for dim, cell in model["score"]["contribs"].items():
            lo, hi, distinct = ranges[dim]
            if hi == lo:
                norm = 0.5
            else:
                norm = (cell["value"] - lo) / (hi - lo)
                if not cell["higher_is_better"]:
                    norm = 1.0 - norm
            ranked = distinct >= 2
            model["score"]["normalization"][dim] = {"norm": round(norm, 4), "ranked": ranked}
            if ranked:
                total += norm * cell["weight"]
                wsum += cell["weight"]
            else:
                model["score"]["skipped"].append((dim, "not_ranked: fewer than 2 distinct values"))
        model["weight_covered"] = round(wsum, 4)
        model["total_score"] = round(total / wsum, 4) if wsum else None
        model["ranking_status"] = ("RANKED" if wsum >= float(cfg["rubric"]["min_weight_covered"])
                                   else "LOW-COVERAGE")
    return scored_models


def _beats(candidate, incumbent, direction, noise):
    if isinstance(candidate, bool) or isinstance(incumbent, bool):
        return False, "categorical dimension requires a differentiator, not a margin"
    c, i = _number(candidate), _number(incumbent)
    if c is None or i is None:
        return False, "comparison value is non-numeric"
    improvement = (c - i) if direction else (i - c)
    kind = noise.get("type")
    if kind == "absolute":
        threshold = float(noise["value"])
        return improvement > threshold, f"improvement {improvement:g} must be > absolute noise {threshold:g}"
    if kind == "relative":
        threshold = abs(i) * float(noise["value"])
        return improvement > threshold, f"improvement {improvement:g} must be > relative noise {threshold:g}"
    return False, "categorical dimension requires a differentiator, not a margin"


def _best_incumbent(incumbents, dim, higher):
    candidates = [(role, inc) for role, inc in incumbents.items()
                  if inc.get("role_dimension") == dim and inc.get("under_cap") is True]
    if not candidates:
        return None, None
    key = lambda item: float(item[1]["value"])
    return (max(candidates, key=key) if higher else min(candidates, key=key))


def _valid_differentiator(model, incumbent, cfg):
    diff = model.get("differentiator")
    if not isinstance(diff, dict) or diff.get("provenance") != "independent":
        return False, "no independently proven structured differentiator"
    dim = diff.get("metric")
    spec = cfg["rubric"]["dimensions"].get(dim)
    inc_cell = incumbent.get("metrics", {}).get(dim) if isinstance(incumbent.get("metrics"), dict) else None
    if not spec or not isinstance(inc_cell, dict) or inc_cell.get("provenance") != "independent":
        return False, "differentiator is not a measured dimension the incumbent loses/lacks"
    if spec.get("scale") == "categorical":
        win = diff.get("value") is True and inc_cell.get("value") is False
        return win, "independent categorical differentiator win" if win else "no categorical differentiator win"
    win, detail = _beats(diff.get("value"), inc_cell.get("value"),
                         spec.get("higher_is_better", True), cfg["rubric"]["noise"].get(dim, {}))
    return win, f"independent differentiator: {detail}"


def _independent_observations(model, driving_source_dim, cfg):
    """List additional INDEPENDENT, NUMERIC metric cells (other than the driving
    dimension and price) present in the scan, so an actionable verdict surfaces
    the rest of its independent evidence base rather than silently dropping it
    (e.g. a Vals index that supports but did not itself trigger the swap).

    Deliberately named 'observations', not 'corroboration': these are additional
    independent data points shown alongside the verdict, NOT a claim that each one
    was benchmarked against the incumbent and found supportive. Non-numeric,
    price, and non-independent cells are excluded so no adverse or unrelated value
    is dressed up as support."""
    metrics = model.get("metrics") if isinstance(model.get("metrics"), dict) else {}
    dims = cfg["rubric"]["dimensions"]
    out = []
    driving_source = dims.get(driving_source_dim, {}).get("source") if driving_source_dim else None
    source_to_dim = {spec.get("source"): dim for dim, spec in dims.items() if spec.get("source")}
    for src, cell in metrics.items():
        if src in (driving_source, "output_price"):
            continue
        if not (isinstance(cell, dict) and cell.get("provenance") == "independent"):
            continue
        val = cell.get("value")
        # numeric only (bool is a numeric subtype in Python but is a categorical
        # signal, not a comparable observation, so exclude it explicitly)
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            continue
        out.append({"dimension": source_to_dim.get(src, src), "source": src,
                    "value": val, "reference": cell.get("source"),
                    "scored_dimension": src in source_to_dim})
    return out


REQUIRED_EVIDENCE_FIELDS = ("basis", "dimension", "candidate_value", "candidate_provenance")
VALID_EVIDENCE_BASES = ("independent-margin-vs-incumbent", "independent-differentiator")


def _evidence_is_well_formed(evidence):
    """An actionable verdict's evidence must be a dict with the required fields, a
    known basis, and an INDEPENDENT candidate provenance. Anything else is not a
    valid basis for a swap/niche recommendation."""
    if not isinstance(evidence, dict):
        return False
    if any(evidence.get(f) in (None, "") for f in REQUIRED_EVIDENCE_FIELDS):
        return False
    if evidence.get("basis") not in VALID_EVIDENCE_BASES:
        return False
    if evidence.get("candidate_provenance") != "independent":
        return False
    return True


def _enforce_actionable_evidence(recs):
    """Fail-closed guard over FINISHED recommendation objects: any CONSIDER* verdict
    whose evidence block is missing or malformed is downgraded to HOLD. Runs
    independently of how the verdict was produced, so a future path that forgets
    or corrupts evidence cannot ship an unsupported swap. Returns the count of
    downgrades (0 in normal operation)."""
    downgraded = 0
    for rec in recs.values():
        if rec["verdict"].startswith("CONSIDER") and not _evidence_is_well_formed(rec.get("evidence")):
            rec["verdict"] = "HOLD"
            rec.pop("evidence", None)
            rec.setdefault("why", []).append(
                "coherence guard: missing or malformed independent evidence; failed closed to HOLD")
            downgraded += 1
    return downgraded


def recommend(scan, cfg):
    findings = validate_scan(scan, cfg)
    errors = [f for f in findings if f.level == "ERROR"]
    result = {"scan_date": scan.get("scan_date") if isinstance(scan, dict) else None,
              "usable": not errors, "findings": [repr(f) for f in findings], "models": []}
    if errors:
        return result
    scored = []
    for model in scan["models"]:
        gates, attrs = apply_hard_gates(model, cfg)
        blocked = [gid for gid, passed, _ in gates if not passed]
        scored.append({"name": model["name"], "vendor": model["vendor"], "profile": model["profile"],
                       "trusted_attributes": attrs,
                       "candidate_for_roles": [r.casefold() for r in model["candidate_for_roles"]],
                       "gates": [{"id": gid, "passed": passed, "status": "PASS" if passed else "FAIL", "detail": detail}
                                 for gid, passed, detail in gates],
                       "blocked_by": blocked, "policy_status": "BLOCKED" if blocked else "ALLOWED",
                       "score": score_model(model, cfg), "_raw": model})
    normalize_and_total(scored, cfg)
    incumbents = scan["incumbents"]
    for scored_model in scored:
        recs = {}
        for role in scored_model["candidate_for_roles"]:
            reasons = []
            evidence = None
            if scored_model["blocked_by"]:
                verdict = "BLOCKED"
                reasons.append("hard gate(s): " + ", ".join(scored_model["blocked_by"]))
            else:
                inc = incumbents.get(role)
                verdict = "HOLD"
                if inc is None:
                    reasons.append("no provenanced incumbent comparison")
                else:
                    dim = inc["role_dimension"]
                    spec = cfg["rubric"]["dimensions"][dim]
                    if spec.get("scale") == "categorical":
                        reasons.append("categorical primary dimension requires a differentiator, not a margin")
                    else:
                        cell = scored_model["_raw"]["metrics"].get(spec["source"], {})
                        candidate = cell.get("value") if cell.get("provenance") == "independent" else None
                        best_role, best = _best_incumbent(incumbents, dim, spec.get("higher_is_better", True))
                        if candidate is None:
                            reasons.append(f"no independent {dim} value to justify a swap")
                        elif best is None:
                            reasons.append(f"no best under-cap incumbent for {dim}")
                        else:
                            win, detail = _beats(candidate, best["value"], spec.get("higher_is_better", True),
                                                 cfg["rubric"]["noise"].get(dim, {}))
                            if win:
                                verdict = "CONSIDER-SWAP"
                                reasons.append(f"beats best under-cap incumbent {best['model']} ({best_role}): {detail}")
                                evidence = {"basis": "independent-margin-vs-incumbent",
                                            "dimension": dim, "candidate_value": candidate,
                                            "candidate_provenance": "independent",
                                            "incumbent": best["model"], "incumbent_value": best["value"],
                                            "detail": detail,
                                            "observations": _independent_observations(scored_model["_raw"], dim, cfg)}
                            else:
                                reasons.append(f"does not beat best under-cap incumbent {best['model']} ({best_role}): {detail}")
                    if verdict == "HOLD":
                        diff_ok, diff_detail = _valid_differentiator(scored_model["_raw"], inc, cfg)
                        if diff_ok:
                            verdict = "CONSIDER-NICHE"
                            diff = scored_model["_raw"].get("differentiator", {})
                            diff_dim = diff.get("metric")
                            # the incumbent value on the SAME differentiator dimension it must lack/lose
                            inc_dim_cell = inc.get("metrics", {}).get(diff_dim) if isinstance(inc.get("metrics"), dict) else None
                            inc_dim_val = inc_dim_cell.get("value") if isinstance(inc_dim_cell, dict) else None
                            evidence = {"basis": "independent-differentiator",
                                        "dimension": diff_dim, "candidate_value": diff.get("value"),
                                        "candidate_provenance": "independent",
                                        "incumbent": inc.get("model"), "incumbent_value": inc_dim_val,
                                        "detail": diff_detail,
                                        "observations": _independent_observations(scored_model["_raw"], diff_dim, cfg)}
                        reasons.append(diff_detail)
                    price = _durable_price(scored_model["_raw"]["metrics"].get("output_price"))
                    cap = float(cfg["policy"]["budget_cap_output_usd_per_1m"])
                    if verdict == "HOLD" and not _cap_scope(scored_model["_raw"], cfg) and price is not None and price > cap:
                        reasons.append("outside cap scope, but high durable cost is not justified by the measured capability")
            # Coherence guard (fail-closed): an actionable CONSIDER verdict must
            # carry a well-formed independent evidence block. This is enforced by
            # _assert_actionable_evidence over the FINISHED recommendation objects
            # below, so a future code path that forgets evidence cannot silently
            # ship a swap with no basis (the 2026-09-14 defect: CONSIDER-SWAP next
            # to total_score=null / weight_covered=0.0).
            rec = {"verdict": verdict, "why": reasons}
            if evidence:
                rec["evidence"] = evidence
            recs[role] = rec
        # Fail-closed validation: downgrade any actionable verdict that lacks a
        # complete evidence block to HOLD, rather than emit an unsupported swap.
        _enforce_actionable_evidence(recs)
        scored_model["role_recommendations"] = recs
        # verdict_basis is derived from the ACTUAL role evidence, so it never
        # mislabels the reason a verdict stands. It surfaces why an actionable
        # verdict holds even when the candidate-vs-candidate scoring layer is
        # LOW-COVERAGE (e.g. a single candidate): the win is an independent margin
        # or differentiator vs the incumbent, not peer ranking.
        role_bases = [rec["evidence"]["basis"] for rec in recs.values()
                      if rec["verdict"].startswith("CONSIDER") and rec.get("evidence")]
        if scored_model["blocked_by"]:
            scored_model["verdict_basis"] = "blocked"
        elif role_bases:
            # one actionable basis -> report it; mixed -> generic actionable label
            scored_model["verdict_basis"] = role_bases[0] if len(set(role_bases)) == 1 else "independent-vs-incumbent"
        else:
            scored_model["verdict_basis"] = "no-comparative-win"
        any_consider = any(r["verdict"].startswith("CONSIDER") for r in recs.values())
        scored_model["decision"] = "CONSIDER" if any_consider and not scored_model["blocked_by"] else "HOLD"
        scored_model.pop("_raw")
        scored_model["score"].pop("contribs")
    def sort_key(item):
        ranked = item["ranking_status"] == "RANKED"
        score = item["total_score"] if item["total_score"] is not None else -1.0
        return ranked, score, item["weight_covered"]
    result["models"] = sorted(scored, key=sort_key, reverse=True)
    return result


def render_markdown(result, cfg):
    date = result.get("scan_date") or datetime.date.today().isoformat()
    pol, rubric = cfg["policy"], cfg["rubric"]
    lines = [f"## Landscape scan — {date} (auto-generated)", "",
             "Weekly input is untrusted. Scoring and comparisons use independent evidence only.", "",
             "### Applied policy", "",
             f"- Durable output cap: ${pol['budget_cap_output_usd_per_1m']}/1M",
             f"- Metered profiles: {', '.join(pol['metered_profiles'])}; ultimate is outside the cap",
             f"- Retired vendors: {', '.join(pol['retired_vendors'])}",
             "- Weights: " + ", ".join(f"{d}={s['weight']}" for d, s in rubric["dimensions"].items()), ""]
    if not result["usable"]:
        lines.append("> **DATASET REJECTED — not usable.**")
        lines.extend(f"> - {f}" for f in result["findings"] if f.startswith("[ERROR]"))
        return "\n".join(lines) + "\n"
    lines += ["| Model | Decision | Policy | Score | Coverage | Basis | Role verdicts |",
              "|---|---|---|---:|---:|---|---|"]
    for model in result["models"]:
        score = "—" if model["total_score"] is None else f"{model['total_score']:.4f}"
        recs = "; ".join(f"{r}: **{v['verdict']}**" for r, v in model["role_recommendations"].items())
        lines.append(f"| {model['name']} | {model['decision']} | {model['policy_status']} | {score} | {model['weight_covered']:.2f} | {model.get('verdict_basis','—')} | {recs} |")
    lines.append("")
    lines.append("When a candidate's peer-ranked score is `—` (a single candidate cannot be ranked against peers), an actionable verdict rests on its `verdict_basis`: an independent margin over the role incumbent (`independent-margin-vs-incumbent`) or an independent differentiator the incumbent lacks (`independent-differentiator`). The driving evidence and any additional independent observations are listed per model below.")
    lines.append("")
    for model in result["models"]:
        lines.append(f"### {model['name']}")
        lines.append(f"- verdict basis: **{model.get('verdict_basis','—')}** (peer-ranked score {'—' if model['total_score'] is None else f"{model['total_score']:.4f}"}, coverage {model['weight_covered']:.2f})")
        for gate in model["gates"]:
            lines.append(f"- gate `{gate['id']}`: **{gate['status']}** — {gate['detail']}")
        for role, rec in model["role_recommendations"].items():
            lines.append(f"- `{role}`: **{rec['verdict']}** — {'; '.join(rec['why'])}")
            ev = rec.get("evidence")
            if ev:
                inc = f" vs incumbent {ev.get('incumbent')} = {ev.get('incumbent_value')}" if ev.get('incumbent') is not None else ""
                lines.append(f"  - evidence ({ev['basis']}): {ev['dimension']} = {ev['candidate_value']} (independent){inc}")
                for c in ev.get("observations", []):
                    tag = "scored" if c.get("scored_dimension") else "independent (unscored)"
                    lines.append(f"  - additional independent observation [{tag}]: {c['dimension']} = {c['value']}")
        lines.append("")
    return "\n".join(lines) + "\n"


def render_csv(result):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["model", "vendor", "profile", "decision", "policy_status", "total_score",
                     "weight_covered", "verdict_basis", "blocked_by", "verdicts", "evidence_json"])
    for model in result.get("models", []):
        evidence = {r: v["evidence"] for r, v in model["role_recommendations"].items() if v.get("evidence")}
        writer.writerow([model["name"], model["vendor"], model["profile"], model["decision"], model["policy_status"],
                         model["total_score"], model["weight_covered"], model.get("verdict_basis", ""), "|".join(model["blocked_by"]),
                         "|".join(f"{r}:{v['verdict']}" for r, v in model["role_recommendations"].items()),
                         json.dumps(evidence, ensure_ascii=False) if evidence else ""])
    return buf.getvalue()


def _cell(value, provenance="independent", source="fixture"):
    return {"value": value, "provenance": provenance, "source": source}


def _inc(value, dim="intelligence", model="ProviderX/role", under_cap=True, metrics=None):
    return {"model": model, "role_dimension": dim, "value": value, "provenance": "independent",
            "source": "fixture", "under_cap": under_cap, "metrics": metrics or {}}


def _model(name="candidate-A", vendor="providerx", profile="hybrid", roles=None, metrics=None, **extra):
    data = {"name": name, "vendor": vendor, "profile": profile,
            "candidate_for_roles": roles or ["gen-pro"], "metrics": metrics if metrics is not None else {}}
    data.update(extra)
    return data


def self_test(cfg):
    failures = []
    checks = 0
    def check(condition, message):
        nonlocal checks
        checks += 1
        if not condition:
            failures.append(message)

    # Swap path, exact noise boundary, and just-beyond boundary.
    base_inc = {"gen-pro": _inc(60), "comm-xl": _inc(62)}
    for value, expected in ((65, "CONSIDER-SWAP"),):
        result = recommend({"incumbents": base_inc, "models": [_model(metrics={"intelligence_index": _cell(value),
                           "output_price": {**_cell(1, "vendor"), "durable_value": 1}})]}, cfg)
        check(result["models"][0]["role_recommendations"]["gen-pro"]["verdict"] == expected,
              "clear independent win beyond best under-cap incumbent must swap")
    boundary = recommend({"incumbents": {"gen-pro": _inc(60)}, "models": [_model(metrics={
        "intelligence_index": _cell(62), "output_price": {**_cell(1, "vendor"), "durable_value": 1}})]}, cfg)
    check(boundary["models"][0]["role_recommendations"]["gen-pro"]["verdict"] == "HOLD",
          "exact absolute noise boundary must HOLD")
    beyond = recommend({"incumbents": {"gen-pro": _inc(60)}, "models": [_model(metrics={
        "intelligence_index": _cell(62.0001), "output_price": {**_cell(1, "vendor"), "durable_value": 1}})]}, cfg)
    check(beyond["models"][0]["role_recommendations"]["gen-pro"]["verdict"] == "CONSIDER-SWAP",
          "just beyond absolute noise boundary must swap")

    # Vendor candidate evidence cannot drive a swap or niche verdict.
    vendor_only = recommend({"incumbents": {"gen-pro": _inc(10)}, "models": [_model(metrics={
        "intelligence_index": _cell(99, "vendor"), "output_price": {**_cell(1, "vendor"), "durable_value": 1}},
        differentiator={"metric": "speed", "value": 999, "provenance": "vendor", "source": "fixture"})]}, cfg)
    vm = vendor_only["models"][0]
    check(vm["role_recommendations"]["gen-pro"]["verdict"] == "HOLD", "vendor-only advantage must HOLD")
    check("intelligence" not in vm["score"]["normalization"], "vendor metric must be excluded before normalization")
    check(dict(vm["score"]["skipped"]).get("intelligence", "").startswith("non-independent"),
          "vendor metric must carry the explicit non-independent skip reason")

    # Curated family attribute: unknown candidate fails even if dataset self-attests true.
    family = recommend({"incumbents": {"hephaestus": _inc(60)}, "models": [_model(name="candidate-unknown",
        profile="ultimate", roles=["hephaestus"], flagship_native_family=True,
        metrics={"intelligence_index": _cell(70), "output_price": {**_cell(50, "vendor"), "durable_value": 50}})]}, cfg)
    fm = family["models"][0]
    check("family_fit" in fm["blocked_by"], "unknown non-flagship candidate must fail family_fit")
    check(not next(g for g in fm["gates"] if g["id"] == "family_fit")["passed"], "family_fit gate must explicitly FAIL")
    check(next(g for g in fm["gates"] if g["id"] == "cap")["passed"], "ultimate profile must be outside cap")

    # region_availability: FAIL-CLOSED, identity-bound. A region-locked owner
    # cannot enter the HK-native ultimate profile even when it passes family-fit.
    # This is the GPT-6-Astra-for-hephaestus case the 2026-09-07 scan raised, plus
    # the adversarial-relabel bypasses a skeptical review reproduced.
    def _region_case(name, vendor, profile, price=50, roles=("hephaestus",)):
        return recommend({"incumbents": {r: _inc(49) for r in roles}, "models": [_model(
            name=name, vendor=vendor, profile=profile, roles=list(roles),
            flagship_native_family=True, metrics={"intelligence_index": _cell(55),
            "output_price": {**_cell(price, "vendor"), "durable_value": price}})]}, cfg)["models"][0]

    # Honest region-locked owner in ultimate: HOLD, region_availability.
    region_blocked = _region_case("gpt-6-astra", "openai", "ultimate")
    check("region_availability" in region_blocked["blocked_by"],
          "region-locked owner (openai) must fail region_availability for ultimate")
    check(region_blocked["decision"] == "HOLD",
          "region-blocked candidate must HOLD despite a clear intelligence win")
    check(region_blocked["policy_status"] == "BLOCKED", "blocked candidate must report BLOCKED policy_status")
    check(region_blocked["role_recommendations"]["hephaestus"]["verdict"] == "BLOCKED",
          "blocked candidate role verdict must be BLOCKED not CONSIDER-SWAP")
    # Mixed case must behave identically (identity resolved case-insensitively).
    check("region_availability" in _region_case("GPT-6-Astra", "OpenAI", "Ultimate")["blocked_by"],
          "mixed-case region-locked owner must still FAIL region_availability")

    # CRITICAL bypass 1: scan relabels vendor to a region-available one but the
    # curated owner (resolved from name) still says openai. Identity mismatch FAILS.
    relabel_vendor = _region_case("gpt-6-astra", "providerx", "ultimate")
    check("region_availability" in relabel_vendor["blocked_by"],
          "scan vendor disagreeing with curated owner must FAIL region_availability")
    # Bypass 2: scan claims a global profile for a region-locked owner. It must not
    # become an actionable CONSIDER for the region-locked seat (cap catches the
    # over-cap flagship here; region policy stays global for genuine hybrid use).
    relabel_profile = _region_case("gpt-6-astra", "openai", "hybrid")
    check(relabel_profile["decision"] != "CONSIDER",
          "region-locked owner relabeled to a global profile must not be actionable")

    # Unknown identity (no curated owner) fails closed in a region-locked profile.
    unknown_region = _region_case("candidate-unmapped", "providerx", "ultimate")
    check("region_availability" in unknown_region["blocked_by"],
          "unresolved identity must FAIL region_availability closed for a locked profile")
    # Owner not on the allowlist (default-allow guard) fails: meta has no HK dev API.
    meta_gates = apply_hard_gates(_model(name="candidate-A", vendor="meta", profile="ultimate",
        roles=["gen-pro"], metrics={"intelligence_index": _cell(55)}), cfg)[0]
    check(not next(g for g in meta_gates if g[0] == "region_availability")[1],
          "an owner absent from the ultimate allowlist must FAIL (fail-closed, not default-allow)")

    # Legit HK-native flagship in ultimate passes and can CONSIDER.
    region_ok = _region_case("candidate-flagship", "providerx", "ultimate", price=3)
    check(next(g for g in region_ok["gates"] if g["id"] == "region_availability")["passed"],
          "region-available owner must pass region_availability for ultimate")
    check(region_ok["decision"] == "CONSIDER", "region-available flagship win must remain actionable")
    # No-op for genuinely global profiles: both hybrid and b4b.
    for prof in ("hybrid", "b4b"):
        g = apply_hard_gates(_model(name="candidate-A", vendor="providerx", profile=prof,
            roles=["gen-pro"], metrics={"intelligence_index": _cell(55)}), cfg)[0]
        check(next(x for x in g if x[0] == "region_availability")[1],
              f"region gate must be a no-op for non-region-locked profile ({prof})")

    # verdict coherence (the 2026-09-14 defect): a single-candidate scan cannot be
    # peer-ranked (total_score null, coverage 0), but a swap driven by an
    # independent margin over the incumbent must still be coherent: it carries an
    # evidence block and verdict_basis explains why it stands.
    single = recommend({"incumbents": {"gen-pro": {"model": "inc", "role_dimension": "intelligence",
        "value": 36, "provenance": "independent", "source": "fixture", "under_cap": True}},
        "models": [_model(metrics={"intelligence_index": _cell(40),
            "output_price": {**_cell(1, "vendor"), "durable_value": 1},
            "vals_index": _cell(57.86)})]}, cfg)["models"][0]
    check(single["total_score"] is None and single["weight_covered"] == 0.0,
          "single candidate cannot be peer-ranked (null score, zero coverage)")
    srec = single["role_recommendations"]["gen-pro"]
    check(srec["verdict"] == "CONSIDER-SWAP", "independent margin over incumbent must still swap on a lone candidate")
    check("evidence" in srec and srec["evidence"]["basis"] == "independent-margin-vs-incumbent",
          "an actionable swap must carry an explicit independent evidence block")
    check(single["verdict_basis"] == "independent-margin-vs-incumbent",
          "verdict_basis must explain an actionable-but-unranked swap")
    check(any(c["source"] == "vals_index" and not c["scored_dimension"] for c in srec["evidence"]["observations"]),
          "independent unscored evidence (vals_index) must appear as an observation, not be dropped")
    # Coherence invariant: no CONSIDER verdict anywhere may lack an evidence block.
    check(all("evidence" in rec for m in [single, region_ok]
              for rec in m["role_recommendations"].values() if rec["verdict"].startswith("CONSIDER")),
          "every CONSIDER verdict must carry an evidence basis (coherence guard)")

    # CONSIDER-NICHE: an independent differentiator the incumbent lacks. Evidence
    # must name the incumbent and the differentiator dimension, and verdict_basis
    # must reflect the differentiator basis (not the margin basis).
    niche = recommend({"incumbents": {"gen-pro": {"model": "inc", "role_dimension": "intelligence",
        "value": 40, "provenance": "independent", "source": "fixture", "under_cap": True,
        "metrics": {"speed": _cell(100)}}},
        "models": [_model(metrics={"intelligence_index": _cell(40), "output_speed": _cell(140),
            "output_price": {**_cell(1, "vendor"), "durable_value": 1}},
            differentiator={"metric": "speed", "value": 140, "provenance": "independent", "source": "fixture"})]}, cfg)["models"][0]
    nrec = niche["role_recommendations"]["gen-pro"]
    check(nrec["verdict"] == "CONSIDER-NICHE", "independent differentiator must grant niche")
    check(nrec["evidence"]["basis"] == "independent-differentiator", "niche evidence basis must be the differentiator basis")
    check(nrec["evidence"].get("incumbent") == "inc" and nrec["evidence"].get("incumbent_value") == 100,
          "niche evidence must name the incumbent and its value on the differentiator dimension")
    check(niche["verdict_basis"] == "independent-differentiator",
          "verdict_basis must reflect the actual niche basis, not hard-coded margin")

    # _independent_observations must exclude non-numeric, boolean, price, and
    # non-independent cells so no adverse/unrelated value is dressed up as support.
    obs = _independent_observations({"metrics": {
        "intelligence_index": _cell(40), "output_speed": _cell(200),
        "vals_index": _cell(58), "native_vision": _cell(True),
        "bogus_text": {"value": "great", "provenance": "independent", "source": "x"},
        "vendor_metric": {"value": 999, "provenance": "vendor", "source": "x"},
        "output_price": {**_cell(1, "vendor"), "durable_value": 1}}}, "intelligence", cfg)
    obs_sources = {o["source"] for o in obs}
    check("output_speed" in obs_sources and "vals_index" in obs_sources, "numeric independent metrics must appear as observations")
    check("intelligence_index" not in obs_sources, "the driving dimension must not be echoed as its own observation")
    check("bogus_text" not in obs_sources, "non-numeric independent values must be excluded from observations")
    check("native_vision" not in obs_sources, "boolean (categorical) values must be excluded from observations")
    check("vendor_metric" not in obs_sources, "vendor-provenance values must be excluded from observations")
    check("output_price" not in obs_sources, "price must be excluded from observations (handled by the cap gate)")

    # The fail-closed guard is a REAL validator: feed it a malformed CONSIDER and
    # confirm it downgrades to HOLD (not dead code).
    check(_evidence_is_well_formed({"basis": "independent-margin-vs-incumbent", "dimension": "intelligence",
          "candidate_value": 40, "candidate_provenance": "independent"}), "a complete evidence block is well-formed")
    check(not _evidence_is_well_formed({"basis": "made-up", "dimension": "x", "candidate_value": 1,
          "candidate_provenance": "independent"}), "an unknown basis must be rejected")
    check(not _evidence_is_well_formed({"basis": "independent-margin-vs-incumbent", "dimension": "x",
          "candidate_value": 1, "candidate_provenance": "vendor"}), "vendor-provenance evidence must be rejected")
    check(not _evidence_is_well_formed(None), "missing evidence must be rejected")
    bad_recs = {"gen-pro": {"verdict": "CONSIDER-SWAP", "why": [], "evidence": None},
                "oracle": {"verdict": "CONSIDER-NICHE", "why": []},
                "deep": {"verdict": "HOLD", "why": []}}
    downgraded = _enforce_actionable_evidence(bad_recs)
    check(downgraded == 2, "the guard must downgrade every malformed CONSIDER (both here)")
    check(bad_recs["gen-pro"]["verdict"] == "HOLD" and bad_recs["oracle"]["verdict"] == "HOLD",
          "malformed CONSIDER verdicts must be downgraded to HOLD")
    check(bad_recs["deep"]["verdict"] == "HOLD", "an existing HOLD is untouched by the guard")

    # A HOLD (no independent win) must NOT fabricate an evidence block or basis.
    hold_case = recommend({"incumbents": {"gen-pro": {"model": "inc", "role_dimension": "intelligence",
        "value": 40, "provenance": "independent", "source": "fixture", "under_cap": True}},
        "models": [_model(metrics={"intelligence_index": _cell(40),
            "output_price": {**_cell(1, "vendor"), "durable_value": 1}})]}, cfg)["models"][0]
    check(hold_case["role_recommendations"]["gen-pro"]["verdict"] == "HOLD", "a tie within noise must HOLD")
    check("evidence" not in hold_case["role_recommendations"]["gen-pro"], "a HOLD must not carry an evidence block")
    check(hold_case["verdict_basis"] == "no-comparative-win",
          "a non-actionable lone candidate reports no-comparative-win")

    # Cap must fail closed even when validation is bypassed/direct gate call.
    missing_price = _model(metrics={"intelligence_index": _cell(70)})
    gates, _ = apply_hard_gates(missing_price, cfg)
    check(not next(g for g in gates if g[0] == "cap")[1], "missing durable price must fail cap")
    invalid = recommend({"incumbents": {"gen-pro": _inc(60)}, "models": [missing_price]}, cfg)
    check(not invalid["usable"], "missing durable price must reject dataset")
    intro_price = _model(metrics={"intelligence_index": _cell(70),
        "output_price": {**_cell(1, "vendor"), "durable_value": 10, "introductory": True}})
    intro_gates, _ = apply_hard_gates(intro_price, cfg)
    check(not next(g for g in intro_gates if g[0] == "cap")[1],
          "introductory price must never replace over-cap durable price")

    # Pin weights, direction, log-cost normalization and normalized totals.
    scored_scan = {"incumbents": {"gen-pro": _inc(50)}, "models": [
        _model(name="candidate-A", metrics={"intelligence_index": _cell(80), "blended_price": _cell(10),
                                           "output_price": {**_cell(1, "vendor"), "durable_value": 1}}),
        _model(name="candidate-open", metrics={"intelligence_index": _cell(60), "blended_price": _cell(1),
                                              "output_price": {**_cell(1, "vendor"), "durable_value": 1}})]}
    scores = {m["name"]: m for m in recommend(scored_scan, cfg)["models"]}
    check(scores["candidate-A"]["total_score"] == 0.5455, "pinned capability/cost total for candidate-A")
    check(scores["candidate-open"]["total_score"] == 0.4545, "pinned capability/cost total for candidate-open")
    check(scores["candidate-A"]["weight_covered"] == 0.55, "pinned ranked weight coverage")
    check(scores["candidate-A"]["score"]["normalization"]["cost_efficiency"]["norm"] == 0.0,
          "higher cost must normalize worse")

    # Sole-holder/tie normalization is neutral 0.5 but not ranked or covered.
    tie_scan = {"incumbents": {"gen-pro": _inc(50)}, "models": [
        _model(name="candidate-A", metrics={"intelligence_index": _cell(70),
                                           "output_price": {**_cell(1, "vendor"), "durable_value": 1}}),
        _model(name="candidate-open", metrics={"intelligence_index": _cell(70), "output_speed": _cell(100),
                                              "output_price": {**_cell(1, "vendor"), "durable_value": 1}})]}
    ties = {m["name"]: m for m in recommend(tie_scan, cfg)["models"]}
    for name in ties:
        norm = ties[name]["score"]["normalization"]["intelligence"]
        check(norm == {"norm": 0.5, "ranked": False}, "tied normalization must be neutral and not ranked")
    check(ties["candidate-open"]["score"]["normalization"]["speed"] == {"norm": 0.5, "ranked": False},
          "sole-holder normalization must be neutral and not ranked")
    check(ties["candidate-open"]["weight_covered"] == 0.0, "unranked dimensions must not count toward coverage")

    # Valid independent differentiator can grant niche; absent one cannot.
    inc_metric = {"speed": _cell(100)}
    niche_scan = {"incumbents": {"gen-pro": _inc(70, metrics=inc_metric)}, "models": [
        _model(metrics={"intelligence_index": _cell(60), "output_speed": _cell(111),
                        "output_price": {**_cell(1, "vendor"), "durable_value": 1}},
               differentiator={"metric": "speed", "value": 111, "provenance": "independent", "source": "fixture"})]}
    niche = recommend(niche_scan, cfg)["models"][0]
    check(niche["role_recommendations"]["gen-pro"]["verdict"] == "CONSIDER-NICHE",
          "measured independent differentiator beyond relative noise must grant niche")
    no_diff = deepcopy(niche_scan); no_diff["models"][0].pop("differentiator")
    check(recommend(no_diff, cfg)["models"][0]["role_recommendations"]["gen-pro"]["verdict"] == "HOLD",
          "no differentiator must remain HOLD")

    # Every model always emits each gate exactly once; unknown attrs fail closed.
    check([g["id"] for g in vm["gates"]] == list(GATE_IDS), "all five explicit gate records required")
    unknown_open = recommend({"incumbents": {"open-coder": _inc(50)}, "models": [_model(name="candidate-unknown",
        roles=["open-coder"], metrics={"intelligence_index": _cell(70),
        "output_price": {**_cell(1, "vendor"), "durable_value": 1}}, open_weights=True)]}, cfg)["models"][0]
    check("open_weight" in unknown_open["blocked_by"], "dataset self-attestation must not bypass open-weight gate")

    # Validation robustness pins malformed shapes, strict booleans, duplicates, enums, incumbents.
    malformed = recommend({"incumbents": {"gen-pro": _inc(1)}, "models": [_model(metrics=[])]}, cfg)
    check(not malformed["usable"], "metrics-not-dict must reject rather than crash")
    dup = recommend({"incumbents": {"gen-pro": _inc(1)}, "models": [_model(), _model()]}, cfg)
    check(not dup["usable"], "duplicate names must reject")
    bad_bool = recommend({"incumbents": {"gen-pro": _inc(1)}, "models": [_model(open_weights="false")]}, cfg)
    check(not bad_bool["usable"], "truthy strings are not booleans")
    bad_vendor = recommend({"incumbents": {"gen-pro": _inc(1)}, "models": [_model(vendor="unknown-vendor")]}, cfg)
    check(not bad_vendor["usable"], "unknown vendor must reject")

    if failures:
        print(f"SELF-TEST FAILED ({len(failures)}/{checks} assertions):")
        for failure in failures:
            print("  -", failure)
        return 1
    print(f"self-test passed ({checks} assertions across gate, scoring, provenance, noise, and validation fixtures)")
    return 0


def _rejected_path(path):
    base, _ = os.path.splitext(path)
    return base + ".rejected.json"


def main(argv=None):
    parser = argparse.ArgumentParser(description="fail-closed landscape-scan framework")
    parser.add_argument("--scan")
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--out-json")
    parser.add_argument("--out-csv")
    parser.add_argument("--out-md")
    parser.add_argument("--golden", help="compare result JSON to this expected file")
    parser.add_argument("--write-golden", help="write result JSON to this expected file")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--strict", action="store_true", help="warnings also produce a nonzero exit")
    parser.add_argument("--print-schema", action="store_true")
    parser.add_argument("--sync-config", action="store_true")
    args = parser.parse_args(argv)
    if args.print_schema:
        print(SCHEMA_TEXT)
        return 0
    try:
        if args.sync_config:
            print(f"synced {sync_config(args.config)}")
            return 0
        cfg = load_config(args.config)
    except ConfigError as exc:
        print(f"CONFIG ERROR: {exc}", file=sys.stderr)
        return 2
    if args.self_test:
        return self_test(cfg)
    if not args.scan:
        parser.error("--scan is required")
    try:
        with io.open(args.scan, encoding="utf-8") as handle:
            scan = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"SCAN ERROR: {exc}", file=sys.stderr)
        return 2
    result = recommend(scan, cfg)
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if not result["usable"]:
        if args.out_json:
            rejected = _rejected_path(args.out_json)
            with io.open(rejected, "w", encoding="utf-8") as handle:
                handle.write(text)
            print(f"dataset rejected; details written to {rejected}", file=sys.stderr)
        else:
            print(render_markdown(result, cfg))
        return 2
    if args.golden:
        try:
            with io.open(args.golden, encoding="utf-8") as handle:
                expected = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"GOLDEN ERROR: {exc}", file=sys.stderr); return 1
        if json.loads(text) != expected:
            print("golden mismatch", file=sys.stderr)
            return 1
        print(f"golden match: {args.golden}")
    if args.write_golden:
        os.makedirs(os.path.dirname(os.path.abspath(args.write_golden)), exist_ok=True)
        with io.open(args.write_golden, "w", encoding="utf-8") as handle:
            handle.write(text)
    if args.out_json:
        with io.open(args.out_json, "w", encoding="utf-8") as handle:
            handle.write(text)
    if args.out_csv:
        with io.open(args.out_csv, "w", encoding="utf-8") as handle:
            handle.write(render_csv(result))
    markdown = render_markdown(result, cfg)
    if args.out_md:
        with io.open(args.out_md, "w", encoding="utf-8") as handle:
            handle.write(markdown)
    elif not args.golden:
        print(markdown)
    has_warn = any(f.startswith("[WARN]") for f in result["findings"])
    return 1 if args.strict and has_warn else 0


if __name__ == "__main__":
    sys.exit(main())
