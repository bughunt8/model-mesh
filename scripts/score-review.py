#!/usr/bin/env python3
"""Score review runs against seeded defects, and show what each lens and model family added.

This is the measurement harness for the claim that more lenses or more model families catch more.
It measures nothing by itself: the committed fixture is invented. A real corpus needs defects
planted in realistic artifacts by someone who is not a reviewer.

A defect is found when a finding has the same path and category and its line range overlaps the
defect's range, widened by 3 lines on each side. Precision counts clusters from
scripts/aggregate-findings.py, so several reviewers pointing at one place count once.

Reported per run: recall, cluster precision, recall for each lens and family on its own,
and the recall lost when one lens or one family is removed (what only it caught).

Usage:
  python scripts/score-review.py cases.json     print the report as JSON
  python scripts/score-review.py --self-test
"""
import importlib.util, io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("agg", os.path.join(ROOT, "scripts", "aggregate-findings.py"))
agg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agg)
SLACK = 3


def hits(defect, finding):
    if defect["path"] != finding["path"] or defect["category"] != finding["category"] or "line_start" not in finding:
        return False
    return finding["line_start"] <= defect["line_end"] + SLACK and finding["line_end"] >= defect["line_start"] - SLACK


def found(defects, findings):
    return {d["id"] for d in defects if any(hits(d, f) for f in findings)}


def score_run(defects, findings):
    all_found = found(defects, findings)
    clusters = agg.cluster(findings)
    useful = [c for c in clusters if any(
        d["path"] == c["path"] and d["category"] == c["category"] and c["line_start"] is not None
        and c["line_start"] <= d["line_end"] + SLACK and c["line_end"] >= d["line_start"] - SLACK for d in defects)]
    n = len(defects) or 1
    out = {"defects": len(defects), "found": sorted(all_found), "recall": round(len(all_found) / n, 3),
           "clusters": len(clusters), "precision": round(len(useful) / len(clusters), 3) if clusters else None,
           "by_lens": {}, "by_family": {}}
    for key, field in (("by_lens", "lens"), ("by_family", "family")):
        for v in sorted({f[field] for f in findings}):
            own = found(defects, [f for f in findings if f[field] == v])
            without = found(defects, [f for f in findings if f[field] != v])
            out[key][v] = {"recall_alone": round(len(own) / n, 3), "only_this_caught": sorted(all_found - without)}
    return out


def score(doc):
    errs = []
    for c in doc["cases"]:
        for r in c["runs"]:
            errs += agg.check(r["findings"])
    if errs:
        return None, errs
    return {c["case"]: {r["run"]: score_run(c["defects"], r["findings"]) for r in c["runs"]} for c in doc["cases"]}, []


def self_test():
    fails = 0

    def ok(label, cond):
        nonlocal fails
        print(("  ok   " if cond else "  FAIL ") + label)
        fails += 0 if cond else 1
    doc = json.load(io.open(os.path.join(ROOT, "examples", "orchestration", "seeded", "cases.example.json"), encoding="utf-8"))
    res, errs = score(doc)
    ok("fixture findings are valid", not errs)
    r = res["synthetic-001"]["two-families-three-lenses"]
    ok("recall is 3 of 4", r["recall"] == 0.75 and r["found"] == ["D1", "D2", "D4"])
    ok("one defect is missed", "D3" not in r["found"])
    ok("two reports on one place count as one cluster", r["clusters"] == 4)
    ok("precision counts the unmatched cluster", r["precision"] == 0.75)
    ok("family b alone finds the token gap and the caller break", r["by_family"]["fam-b"]["recall_alone"] == 0.5)
    ok("family a overlap means family b is not the only catcher of D2", "D2" not in r["by_family"]["fam-b"]["only_this_caught"])
    ok("only family b caught D4", r["by_family"]["fam-b"]["only_this_caught"] == ["D4"])
    ok("only the regression lens caught D4", r["by_lens"]["regression-risk"]["only_this_caught"] == ["D4"])
    bad = json.loads(json.dumps(doc)); bad["cases"][0]["runs"][0]["findings"][0]["lens"] = "vibes"
    ok("invalid findings are rejected", score(bad)[0] is None)
    ok("category must match", not hits({"path": "p", "category": "security", "line_start": 1, "line_end": 2},
                                       {"path": "p", "category": "clarity", "line_start": 1, "line_end": 2}))
    ok("slack is 3 lines", hits({"path": "p", "category": "c", "line_start": 10, "line_end": 10},
                                {"path": "p", "category": "c", "line_start": 13, "line_end": 13})
       and not hits({"path": "p", "category": "c", "line_start": 10, "line_end": 10},
                    {"path": "p", "category": "c", "line_start": 14, "line_end": 14}))
    print("self-test " + ("passed" if not fails else f"FAILED ({fails})"))
    return 1 if fails else 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__); return 2
    res, errs = score(json.load(io.open(paths[0], encoding="utf-8")))
    if errs:
        for e in errs:
            print("  FAIL", e)
        return 1
    print(json.dumps(res, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
