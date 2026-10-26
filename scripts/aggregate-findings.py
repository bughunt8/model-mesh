#!/usr/bin/env python3
"""Merge review findings deterministically, before any model touches them.

Findings from every reviewer seat follow examples/orchestration/finding.schema.json. This script
validates them, clusters findings that point at the same place with the same category, keeps the
highest severity, and records which lenses, harnesses and model families reported each cluster.
A cluster reported by two or more model families is marked corroborated. A cluster from one family is
not discarded: it is marked single-family so a person or the aggregator seat can look at it.

Only residual near-duplicates, such as findings with no line range, are left for the model merge.

Usage:
  python scripts/aggregate-findings.py findings.json [more.json ...]   print the merged report as JSON
  python scripts/aggregate-findings.py --markdown findings.json        print a Markdown report
  python scripts/aggregate-findings.py --self-test
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LENSES = os.path.join(ROOT, "examples", "orchestration", "lenses.json")
SEVERITY = {"nit": 1, "major": 2, "blocker": 3}
CATEGORIES = {"correctness", "regression", "security", "spec-gap", "simplicity", "operability",
              "compatibility", "cost", "clarity", "evidence", "numeric", "authorization", "consistency"}
REQUIRED = {"id", "lens", "harness", "family", "severity", "category", "path", "claim", "evidence"}
OPTIONAL = {"line_start", "line_end", "fix"}
GAP = 3  # findings within this many lines of each other, same path and category, are one cluster


def lens_ids():
    return {x["id"] for x in json.load(io.open(LENSES, encoding="utf-8"))["lenses"]}


def check(findings, lenses=None):
    lenses = lenses or lens_ids()
    errs, seen = [], set()
    if not isinstance(findings, list):
        return ["input must be a list of findings"]
    for i, f in enumerate(findings):
        w = f"finding[{i}]"
        if not isinstance(f, dict):
            errs.append(f"{w}: not an object"); continue
        if not REQUIRED <= set(f):
            errs.append(f"{w}: missing {sorted(REQUIRED - set(f))}")
            continue
        if set(f) - REQUIRED - OPTIONAL:
            errs.append(f"{w}: unknown keys {sorted(set(f) - REQUIRED - OPTIONAL)}")
        if f["id"] in seen:
            errs.append(f"{w}: duplicate id {f['id']}")
        seen.add(f["id"])
        if f["lens"] not in lenses:
            errs.append(f"{w}: unknown lens {f['lens']}")
        if f["severity"] not in SEVERITY:
            errs.append(f"{w}: severity must be one of {sorted(SEVERITY)}")
        if f["category"] not in CATEGORIES:
            errs.append(f"{w}: category must be one of {sorted(CATEGORIES)}")
        for k in ("claim", "evidence", "path", "family", "harness"):
            if not isinstance(f[k], str) or not f[k].strip():
                errs.append(f"{w}: {k} must be a non-empty string")
        s, t = f.get("line_start"), f.get("line_end", f.get("line_start"))
        if (s is None) != (t is None) or (s is not None and (not isinstance(s, int) or not isinstance(t, int) or s < 1 or t < s)):
            errs.append(f"{w}: line_start and line_end must be positive integers with end >= start, or both absent")
    return errs


def cluster(findings):
    ranged = sorted((f for f in findings if "line_start" in f),
                    key=lambda f: (f["path"], f["category"], f["line_start"], f["id"]))
    loose = sorted((f for f in findings if "line_start" not in f), key=lambda f: (f["path"], f["category"], f["id"]))
    groups = []
    for f in ranged:
        end = f.get("line_end", f["line_start"])
        g = groups[-1] if groups else None
        if g and g["path"] == f["path"] and g["category"] == f["category"] and f["line_start"] <= g["end"] + GAP:
            g["items"].append(f); g["end"] = max(g["end"], end)
        else:
            groups.append({"path": f["path"], "category": f["category"], "start": f["line_start"], "end": end, "items": [f]})
    for f in loose:
        g = next((x for x in groups if x["start"] is None and x["path"] == f["path"] and x["category"] == f["category"]), None)
        if g:
            g["items"].append(f)
        else:
            groups.append({"path": f["path"], "category": f["category"], "start": None, "end": None, "items": [f]})
    out = []
    for g in groups:
        items = g["items"]
        fams = sorted({x["family"] for x in items})
        out.append({
            "path": g["path"], "line_start": g["start"], "line_end": g["end"], "category": g["category"],
            "severity": max((x["severity"] for x in items), key=SEVERITY.get),
            "lenses": sorted({x["lens"] for x in items}), "harnesses": sorted({x["harness"] for x in items}),
            "families": fams, "corroborated": len(fams) >= 2, "finding_ids": sorted(x["id"] for x in items),
            "claims": [x["claim"] for x in items],
            "needs_model_merge": g["start"] is None and len(items) > 1,
        })
    out.sort(key=lambda c: (-SEVERITY[c["severity"]], not c["corroborated"], c["path"], c["line_start"] or 0, c["category"]))
    for n, c in enumerate(out, 1):
        c["cluster"] = f"C{n:03d}"
    return out


def markdown(clusters):
    lines = ["# Merged review findings", ""]
    if not clusters:
        return "# Merged review findings\n\nNo findings.\n"
    lines += ["| Cluster | Severity | Where | Category | Families | Corroborated | Lenses |", "|---|---|---|---|---|---|---|"]
    for c in clusters:
        where = c["path"] + (f":{c['line_start']}-{c['line_end']}" if c["line_start"] else "")
        lines.append(f"| {c['cluster']} | {c['severity']} | {where} | {c['category']} | {len(c['families'])} | "
                     f"{'yes' if c['corroborated'] else 'single family'} | {', '.join(c['lenses'])} |")
    lines += [""]
    for c in clusters:
        lines += [f"## {c['cluster']} {c['severity']}", ""] + [f"- {t}" for t in c["claims"]] + [""]
    return "\n".join(lines)


def load(paths):
    out = []
    for p in paths:
        d = json.load(io.open(p, encoding="utf-8"))
        out += d["findings"] if isinstance(d, dict) and "findings" in d else d
    return out


def fx(i, family, lens="regression-risk", path="a.py", s=10, e=12, cat="regression", sev="major"):
    f = {"id": i, "lens": lens, "harness": "h-" + family, "family": family, "severity": sev, "category": cat,
         "path": path, "claim": "c " + i, "evidence": "e " + i}
    if s is not None:
        f.update(line_start=s, line_end=e)
    return f


def self_test():
    fails = 0

    def ok(label, cond):
        nonlocal fails
        print(("  ok   " if cond else "  FAIL ") + label)
        fails += 0 if cond else 1
    base = [fx("1", "f1"), fx("2", "f2", s=13, e=14), fx("3", "f1", s=40, e=41, sev="nit"),
            fx("4", "f2", cat="security", lens="security-abuse", sev="blocker"), fx("5", "f1", path="b.py", s=None, e=None, cat="clarity"),
            fx("6", "f2", path="b.py", s=None, e=None, cat="clarity")]
    ok("valid input has no errors", check(base) == [])
    c = cluster(base)
    ok("same place, same category, two families merge and corroborate",
       any(x["finding_ids"] == ["1", "2"] and x["corroborated"] and x["line_end"] == 14 for x in c))
    ok("distant finding stays separate and single family",
       any(x["finding_ids"] == ["3"] and not x["corroborated"] for x in c))
    ok("same place, other category does not merge", any(x["finding_ids"] == ["4"] for x in c))
    ok("highest severity first", c[0]["severity"] == "blocker" and c[0]["cluster"] == "C001")
    ok("rangeless duplicates are flagged for model merge", any(x["finding_ids"] == ["5", "6"] and x["needs_model_merge"] for x in c))
    ok("output is deterministic", cluster(list(reversed(base))) == c)
    ok("severity keeps the maximum", next(x for x in cluster([fx("a", "f1", sev="nit"), fx("b", "f2", sev="blocker")]))["severity"] == "blocker")
    ok("unknown lens rejected", bool(check([fx("1", "f1", lens="vibes")])))
    ok("unknown category rejected", bool(check([fx("1", "f1", cat="mood")])))
    ok("duplicate id rejected", bool(check([fx("1", "f1"), fx("1", "f2")])))
    ok("end before start rejected", bool(check([fx("1", "f1", s=9, e=3)])))
    ok("missing evidence rejected", bool(check([{k: v for k, v in fx("1", "f1").items() if k != "evidence"}])))
    ok("unknown key rejected", bool(check([dict(fx("1", "f1"), mood="x")])))
    ok("empty input renders", "No findings" in markdown([]))
    print("self-test " + ("passed" if not fails else f"FAILED ({fails})"))
    return 1 if fails else 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    md = "--markdown" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__); return 2
    findings = load(paths)
    errs = check(findings)
    if errs:
        for x in errs:
            print("  FAIL", x)
        return 1
    clusters = cluster(findings)
    print(markdown(clusters) if md else json.dumps({"clusters": clusters}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
