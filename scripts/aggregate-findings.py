#!/usr/bin/env python3
"""Merge review findings deterministically, before any model touches them.

Findings from every reviewer seat follow examples/orchestration/finding.schema.json. This script
validates them, clusters findings that point at the same place with the same category, keeps the
highest severity, and records which lenses, harnesses and model families reported each cluster.
A cluster reported by two or more model families is marked corroborated. A cluster from one family is
not discarded: it is marked single-family so a person or the aggregator seat can look at it.

A finding joins a cluster only when its range lies within 3 lines of the range of the cluster's first
finding, so a chain of nearby findings cannot grow into one corroborated cluster. Paths and family names
are normalized, and ids are prefixed with the input file name so two reviewers may both number from 1.

Possible duplicates that the deterministic rules cannot settle are listed in related_clusters and
needs_model_merge: the same place under a different category, a finding with no line range on a path that
has ranged findings of the same category, and several rangeless findings on one path and category. The
model merge may combine them. It must keep every cluster's families, severity and corroboration flag, and
a blocker reported by only one family must stay a blocker.

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
GAP = 3  # a finding joins a cluster if it is within this many lines of the cluster's first finding


def lens_ids():
    return {x["id"] for x in json.load(io.open(LENSES, encoding="utf-8"))["lenses"]}


def norm_path(p):
    p = p.strip().replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p


def norm(findings):
    out = []
    for f in findings:
        g = dict(f)
        if isinstance(g.get("path"), str):
            g["path"] = norm_path(g["path"])
        for k in ("family", "harness"):
            if isinstance(g.get(k), str):
                g[k] = g[k].strip().lower()
        out.append(g)
    return out


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
    findings = norm(findings)
    ranged = sorted((f for f in findings if "line_start" in f),
                    key=lambda f: (f["path"], f["category"], f["line_start"], f["id"]))
    loose = sorted((f for f in findings if "line_start" not in f), key=lambda f: (f["path"], f["category"], f["id"]))
    groups = []
    for f in ranged:
        end = f.get("line_end", f["line_start"])
        g = groups[-1] if groups else None
        if g and g["path"] == f["path"] and g["category"] == f["category"] and f["line_start"] <= g["a_end"] + GAP and end >= g["a_start"] - GAP:
            g["items"].append(f); g["end"] = max(g["end"], end)
        else:
            groups.append({"path": f["path"], "category": f["category"], "start": f["line_start"], "end": end,
                           "a_start": f["line_start"], "a_end": end, "items": [f]})
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
            "claims": [x["claim"] for x in items], "evidence": [x["evidence"] for x in items],
            "needs_model_merge": g["start"] is None and len(items) > 1, "related_clusters": [],
            "_a": (g.get("a_start"), g.get("a_end")),
        })
    out.sort(key=lambda c: (-SEVERITY[c["severity"]], not c["corroborated"], c["path"], c["line_start"] or 0, c["category"], c["finding_ids"]))
    for n, c in enumerate(out, 1):
        c["cluster"] = f"C{n:03d}"
    # possible duplicates the deterministic rules did not merge
    for a in out:
        for b in out:
            if a is b or a["path"] != b["path"]:
                continue
            rel = False
            if a["line_start"] is not None and b["line_start"] is not None and a["category"] != b["category"]:
                rel = a["line_start"] <= b["line_end"] + GAP and a["line_end"] >= b["line_start"] - GAP
            elif a["category"] == b["category"] and (a["line_start"] is None) != (b["line_start"] is None):
                rel = True
            if rel:
                a["related_clusters"].append(b["cluster"])
                a["needs_model_merge"] = True
    for c in out:
        c["related_clusters"] = sorted(set(c["related_clusters"]))
        del c["_a"]
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
        lines += [f"## {c['cluster']} {c['severity']}", ""]
        lines += [f"- {t} Evidence: {v}" for t, v in zip(c["claims"], c["evidence"])]
        if c["related_clusters"]:
            lines += ["", "Possible duplicate of: " + ", ".join(c["related_clusters"])]
        lines += [""]
    return "\n".join(lines)


def load(paths):
    out = []
    for p in paths:
        d = json.load(io.open(p, encoding="utf-8"))
        items = d["findings"] if isinstance(d, dict) and "findings" in d else d
        stem = os.path.splitext(os.path.basename(p))[0]
        for f in items:
            if isinstance(f, dict) and "id" in f:
                f = dict(f, id=f"{stem}:{f['id']}")
            out.append(f)
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
    chain = [fx("a", "f1", s=1, e=2), fx("b", "f2", s=5, e=6), fx("c", "f1", s=9, e=10)]
    cc = cluster(chain)
    ok("a chain of nearby findings does not grow into one cluster", len(cc) == 2 and not all(x["corroborated"] for x in cc))
    ok("anchor range still merges neighbours", any(x["finding_ids"] == ["a", "b"] and x["corroborated"] for x in cc))
    diffcat = cluster([fx("a", "f1", cat="security"), fx("b", "f2", cat="correctness")])
    ok("same place, other category is flagged as a possible duplicate",
       all(x["needs_model_merge"] and x["related_clusters"] for x in diffcat) and len(diffcat) == 2)
    mixed = cluster([fx("a", "f1"), fx("b", "f2", s=None, e=None)])
    ok("rangeless finding next to a ranged one is flagged", all(x["needs_model_merge"] for x in mixed) and len(mixed) == 2)
    ok("paths and families are normalized", len(cluster([fx("a", "OpenAI", path="./src/a.py"), fx("b", "openai", path="src/a.py ")])) == 1
       and cluster([fx("a", "OpenAI", path="./src/a.py"), fx("b", "openai", path="src/a.py ")])[0]["corroborated"] is False)
    ok("cluster output carries evidence", cluster([fx("a", "f1")])[0]["evidence"] == ["e a"])
    import tempfile
    tmp = tempfile.mkdtemp()
    fa, fb = os.path.join(tmp, "rev-a.json"), os.path.join(tmp, "rev-b.json")
    json.dump([fx("1", "f1")], open(fa, "w")); json.dump([fx("1", "f2", s=11, e=11)], open(fb, "w"))
    merged = load([fa, fb])
    ok("two files may both use id 1", check(merged) == [] and len(cluster(merged)) == 1 and cluster(merged)[0]["corroborated"])
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
