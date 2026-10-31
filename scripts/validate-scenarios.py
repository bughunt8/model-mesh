#!/usr/bin/env python3
"""Offline checks on the installable skills.

For each skill under skills/:
  S1 SKILL.md has front matter with a name that equals the folder and a non-empty description.
  S2 SKILL.md stays under the size cap: 24,000 bytes, with a lower fixed ceiling for skills that were
     already larger when the cap was added. A grandfathered skill may shrink and may not grow.
  S3 tests/scenarios/<skill>.json exists with at least 3 scenarios and unique ids.
  S4 every required pattern matches SKILL.md and no forbidden pattern does.

These are static checks. They show a rule is still written in the skill. They do not show that an
agent follows it. Live runs are recorded by hand in TESTING.md.

Usage:
  python scripts/validate-scenarios.py
  python scripts/validate-scenarios.py --self-test
"""
import copy, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = 24000
GRANDFATHERED = {"mm-method": 40000}


def front_matter(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def check_skill(name, text, size, scen):
    errs = []
    fm = front_matter(text)
    if fm is None or fm.get("name") != name or not fm.get("description"):
        errs.append(f"S1 {name}: front matter needs name equal to the folder and a description")
    cap = GRANDFATHERED.get(name, CAP)
    if size > cap:
        errs.append(f"S2 {name}: {size} bytes exceeds the {cap} byte cap")
    if scen is None:
        return errs + [f"S3 {name}: tests/scenarios/{name}.json is missing"]
    items = scen.get("scenarios", [])
    ids = [s.get("id") for s in items]
    if scen.get("skill") != name:
        errs.append(f"S3 {name}: scenario file names skill {scen.get('skill')}")
    if len(items) < 3 or len(set(ids)) != len(ids) or not all(ids):
        errs.append(f"S3 {name}: needs at least 3 scenarios with unique ids")
    for s in items:
        for pat in s.get("required", []):
            if not re.search(pat, text):
                errs.append(f"S4 {name}/{s.get('id')}: required pattern not found: {pat}")
        for pat in s.get("forbidden", []):
            if re.search(pat, text):
                errs.append(f"S4 {name}/{s.get('id')}: forbidden pattern found: {pat}")
        if not s.get("required") and not s.get("forbidden"):
            errs.append(f"S4 {name}/{s.get('id')}: scenario asserts nothing")
    return errs


def run(root):
    errs = []
    base = os.path.join(root, "skills")
    for name in sorted(os.listdir(base)):
        p = os.path.join(base, name, "SKILL.md")
        if not os.path.isfile(p):
            continue
        raw = open(p, "rb").read()
        sp = os.path.join(root, "tests", "scenarios", name + ".json")
        scen = json.load(io.open(sp, encoding="utf-8")) if os.path.isfile(sp) else None
        errs += check_skill(name, raw.decode("utf-8"), len(raw), scen)
    return errs


def self_test():
    fails = 0

    def ok(label, cond):
        nonlocal fails
        print(("  ok   " if cond else "  FAIL ") + label)
        fails += 0 if cond else 1
    ok("repository skills pass", run(ROOT) == [])
    text = "---\nname: demo\ndescription: d\n---\n# Demo\nRule one.\n"
    scen = {"skill": "demo", "scenarios": [{"id": str(i), "required": ["Rule one"]} for i in range(3)]}
    ok("a good skill passes", check_skill("demo", text, len(text), scen) == [])
    ok("S1 wrong name", any(e.startswith("S1") for e in check_skill("other", text, 10, dict(scen, skill="other"))))
    ok("S1 no front matter", any(e.startswith("S1") for e in check_skill("demo", "# Demo\n", 10, scen)))
    ok("S2 over the cap", any(e.startswith("S2") for e in check_skill("demo", text, CAP + 1, scen)))
    ok("S2 grandfathered may not grow", any(e.startswith("S2") for e in check_skill("mm-method", text.replace("demo", "mm-method"), GRANDFATHERED["mm-method"] + 1, dict(scen, skill="mm-method"))))
    ok("S3 missing scenarios", any(e.startswith("S3") for e in check_skill("demo", text, 10, None)))
    few = dict(scen, scenarios=scen["scenarios"][:2])
    ok("S3 too few scenarios", any(e.startswith("S3") for e in check_skill("demo", text, 10, few)))
    dup = copy.deepcopy(scen); dup["scenarios"][1]["id"] = "0"
    ok("S3 duplicate ids", any(e.startswith("S3") for e in check_skill("demo", text, 10, dup)))
    miss = copy.deepcopy(scen); miss["scenarios"][0]["required"] = ["Rule two"]
    ok("S4 required pattern missing", any(e.startswith("S4") for e in check_skill("demo", text, 10, miss)))
    forb = copy.deepcopy(scen); forb["scenarios"][0]["forbidden"] = ["Rule one"]
    ok("S4 forbidden pattern present", any(e.startswith("S4") for e in check_skill("demo", text, 10, forb)))
    empty = copy.deepcopy(scen); empty["scenarios"][0] = {"id": "0"}
    ok("S4 empty scenario", any(e.startswith("S4") for e in check_skill("demo", text, 10, empty)))
    print("self-test " + ("passed" if not fails else f"FAILED ({fails})"))
    return 1 if fails else 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    errs = run(ROOT)
    for e in errs:
        print("  FAIL", e)
    print("skill checks " + ("passed" if not errs else f"FAILED ({len(errs)})"))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
