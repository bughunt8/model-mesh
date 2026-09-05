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
GATE_IDS = ("cap", "retired_vendor", "open_weight", "family_fit")
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
        return {"open_weights": False, "flagship_native_family": False, "known": False}
    row = matches[0]
    return {
        "open_weights": row.get("open_weights") is True,
        "flagship_native_family": row.get("flagship_native_family") is True,
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
                            else:
                                reasons.append(f"does not beat best under-cap incumbent {best['model']} ({best_role}): {detail}")
                    if verdict == "HOLD":
                        diff_ok, diff_detail = _valid_differentiator(scored_model["_raw"], inc, cfg)
                        if diff_ok:
                            verdict = "CONSIDER-NICHE"
                        reasons.append(diff_detail)
                    price = _durable_price(scored_model["_raw"]["metrics"].get("output_price"))
                    cap = float(cfg["policy"]["budget_cap_output_usd_per_1m"])
                    if verdict == "HOLD" and not _cap_scope(scored_model["_raw"], cfg) and price is not None and price > cap:
                        reasons.append("outside cap scope, but high durable cost is not justified by the measured capability")
            recs[role] = {"verdict": verdict, "why": reasons}
        scored_model["role_recommendations"] = recs
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
    lines += ["| Model | Decision | Policy | Score | Coverage | Role verdicts |",
              "|---|---|---|---:|---:|---|"]
    for model in result["models"]:
        score = "—" if model["total_score"] is None else f"{model['total_score']:.4f}"
        recs = "; ".join(f"{r}: **{v['verdict']}**" for r, v in model["role_recommendations"].items())
        lines.append(f"| {model['name']} | {model['decision']} | {model['policy_status']} | {score} | {model['weight_covered']:.2f} | {recs} |")
    lines.append("")
    for model in result["models"]:
        lines.append(f"### {model['name']}")
        for gate in model["gates"]:
            lines.append(f"- gate `{gate['id']}`: **{gate['status']}** — {gate['detail']}")
        for role, rec in model["role_recommendations"].items():
            lines.append(f"- `{role}`: **{rec['verdict']}** — {'; '.join(rec['why'])}")
        lines.append("")
    return "\n".join(lines) + "\n"


def render_csv(result):
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["model", "vendor", "profile", "decision", "policy_status", "total_score", "weight_covered", "blocked_by", "verdicts"])
    for model in result.get("models", []):
        writer.writerow([model["name"], model["vendor"], model["profile"], model["decision"], model["policy_status"],
                         model["total_score"], model["weight_covered"], "|".join(model["blocked_by"]),
                         "|".join(f"{r}:{v['verdict']}" for r, v in model["role_recommendations"].items())])
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
    check([g["id"] for g in vm["gates"]] == list(GATE_IDS), "all four explicit gate records required")
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
