#!/usr/bin/env python3
"""Report drift between the model-mesh method docs and the data and scripts they describe.

Prints only differences. If there are none it prints: No drift detected.

Checks:
  D1 every validator rule id in the validate-orchestration.py docstring is raised by a check in that file
  D2 counts stated in the docs (profiles, situations, patterns, harnesses, lenses) match the data
  D3 the situation table in docs/ORCHESTRATION.md matches the matrix ids and titles
  D4 the lens table in docs/REVIEW-PANEL.md matches examples/orchestration/lenses.json
  D5 relative links and repo paths in the orchestration docs exist
  D6 the CHANGELOG top version equals the plugin and marketplace versions
  D7 every script with a --self-test flag is run by a CI workflow

Usage:
  python scripts/check-drift.py
  python scripts/check-drift.py --self-test
"""
import glob, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
       "ten": 10, "eleven": 11, "twelve": 12}
DOCS = ["docs/ORCHESTRATION.md", "docs/REVIEW-PANEL.md"]


def read(root, rel):
    return io.open(os.path.join(root, rel), encoding="utf-8").read()


def jload(root, rel):
    return json.loads(read(root, rel))


def count_claims(text, noun):
    out = []
    for m in re.finditer(r"\b(" + "|".join(NUM) + r")\s+(?:\w+\s+)?" + noun + r"\b", text, re.I):
        out.append((NUM[m.group(1).lower()], m.group(0)))
    return out


def run(root):
    drift = []

    def add(rule, where, msg):
        drift.append((rule, where, msg))

    matrix = jload(root, "examples/orchestration/matrix.example.json")
    lenses = jload(root, "examples/orchestration/lenses.json")["lenses"]
    val = read(root, "scripts/validate-orchestration.py")
    # D1
    head = val.split('"""')[1]
    for rid in sorted(set(re.findall(r"^\s*(O\d+)\b", head, re.M)), key=lambda x: int(x[1:])):
        if not re.search(r"\b" + rid + r"\b", val.split('"""', 2)[2]):
            add("D1", "scripts/validate-orchestration.py", f"{rid} is documented but no check raises it")
    # D2
    facts = {"profiles": len(matrix["profiles"]), "situations": len(matrix["situations"]),
             "patterns": len(matrix.get("patterns", [])) or 5,
             "harnesses": len(matrix["harnesses"]), "lenses": len(lenses)}
    for doc in DOCS + ["README.md"]:
        text = read(root, doc)
        for noun, real in facts.items():
            for n, quoted in count_claims(text, noun):
                if n != real and not (noun == "profiles" and "ultimate" not in text):
                    add("D2", doc, f'says "{quoted}" but the data has {real}')
    # D3
    doc = read(root, "docs/ORCHESTRATION.md")
    rows = dict(re.findall(r"^\|\s*(A\d\d)\s*\|\s*([^|]+?)\s*\|", doc, re.M))
    want = {s["id"]: s["title"] for s in matrix["situations"]}
    for sid in sorted(set(rows) | set(want)):
        if sid not in rows:
            add("D3", "docs/ORCHESTRATION.md", f"{sid} is in the matrix but not in the situation table")
        elif sid not in want:
            add("D3", "docs/ORCHESTRATION.md", f"{sid} is in the table but not in the matrix")
        elif rows[sid] != want[sid]:
            add("D3", "docs/ORCHESTRATION.md", f'{sid} title is "{rows[sid]}" but the matrix says "{want[sid]}"')
    # D4
    panel = read(root, "docs/REVIEW-PANEL.md")
    in_doc = set(re.findall(r"^\|\s*`([a-z-]+)`\s*\|", panel.split("## Lenses", 1)[-1].split("## Tiers", 1)[0], re.M))
    in_lib = {x["id"] for x in lenses}
    for x in sorted(in_lib - in_doc):
        add("D4", "docs/REVIEW-PANEL.md", f"lens {x} is in the library but not in the lens table")
    for x in sorted(in_doc - in_lib):
        add("D4", "docs/REVIEW-PANEL.md", f"lens {x} is in the lens table but not in the library")
    used = {l for s in matrix["situations"] for l in s["lenses"]}
    for x in sorted(in_lib - used):
        add("D4", "examples/orchestration/lenses.json", f"lens {x} is in the library and no situation uses it")
    # D5
    for d in DOCS:
        base = os.path.dirname(os.path.join(root, d))
        for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", read(root, d)):
            if re.match(r"[a-z]+://", target) or target.startswith("mailto:"):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                add("D5", d, f"link target {target} does not exist")
        for target in re.findall(r"`((?:scripts|examples|docs|profiles|skills)/[A-Za-z0-9_./-]+\.[a-z]+)`", read(root, d)):
            if not os.path.exists(os.path.join(root, target)):
                add("D5", d, f"path {target} does not exist")
    # D6
    log = read(root, "CHANGELOG.md")
    top = re.search(r"^##\s*\[?v?(\d+\.\d+\.\d+)", log, re.M)
    for rel in (".plugin/plugin.json", ".plugin/marketplace.json"):
        txt = read(root, rel)
        vers = set(re.findall(r'"version"\s*:\s*"(\d+\.\d+\.\d+)"', txt))
        if top and vers and vers != {top.group(1)}:
            add("D6", rel, f"version {sorted(vers)} differs from the CHANGELOG top entry {top.group(1)}")
    # D7
    flows = "".join(read(root, os.path.relpath(p, root)) for p in glob.glob(os.path.join(root, ".github", "workflows", "*.yml")))
    for p in sorted(glob.glob(os.path.join(root, "scripts", "*.py"))):
        rel = os.path.relpath(p, root).replace(os.sep, "/")
        if "--self-test" in io.open(p, encoding="utf-8").read() and (rel + " --self-test") not in flows:
            add("D7", rel, "has a --self-test flag that no CI workflow runs")
    return drift


def report(drift):
    if not drift:
        return "No drift detected"
    out = []
    for rule, where, msg in drift:
        out.append(f"{rule} {where}: {msg}")
    return "\n".join(out)


def self_test():
    import shutil, tempfile
    fails = 0

    def ok(label, cond):
        nonlocal fails
        print(("  ok   " if cond else "  FAIL ") + label)
        fails += 0 if cond else 1

    def mutated(fn):
        tmp = tempfile.mkdtemp()
        try:
            for rel in ["docs", "examples", "scripts", ".github", ".plugin", "README.md", "CHANGELOG.md"]:
                src = os.path.join(ROOT, rel)
                if os.path.isdir(src):
                    shutil.copytree(src, os.path.join(tmp, rel), ignore=shutil.ignore_patterns("__pycache__", "landscape"))
                else:
                    shutil.copy(src, os.path.join(tmp, rel))
            fn(tmp)
            return {d[0] for d in run(tmp)}
        finally:
            shutil.rmtree(tmp)

    def edit(rel, a, b):
        def f(tmp):
            p = os.path.join(tmp, rel); s = io.open(p, encoding="utf-8").read()
            assert a in s, (rel, a)
            io.open(p, "w", encoding="utf-8").write(s.replace(a, b, 1))
        return f
    ok("the repository is clean", run(ROOT) == [])
    ok("clean output text", report([]) == "No drift detected")
    ok("D1 undocumented check", "D1" in mutated(edit("scripts/validate-orchestration.py", "  O18 gates:", "  O99 invented rule.\n  O18 gates:")))
    ok("D2 wrong count", "D2" in mutated(edit("docs/ORCHESTRATION.md", "## Twelve situations", "## Eleven situations")))
    ok("D3 renamed situation", "D3" in mutated(edit("docs/ORCHESTRATION.md", "Regression bug repair", "Bug repair")))
    ok("D4 lens missing from docs", "D4" in mutated(edit("docs/REVIEW-PANEL.md", "| `consistency` |", "| `consistent` |")))
    ok("D5 broken link", "D5" in mutated(edit("docs/REVIEW-PANEL.md", "(../scripts/score-review.py)", "(../scripts/missing.py)")))
    ok("D6 version skew", "D6" in mutated(edit(".plugin/plugin.json", '"version": "1.', '"version": "9.')))

    def drop_workflows(tmp):
        for f in glob.glob(os.path.join(tmp, ".github", "workflows", "*.yml")):
            os.remove(f)
    ok("D7 script not in CI", "D7" in mutated(drop_workflows))
    print("self-test " + ("passed" if not fails else f"FAILED ({fails})"))
    return 1 if fails else 0


def main(argv):
    if "--self-test" in argv:
        return self_test()
    drift = run(ROOT)
    print(report(drift))
    return 1 if drift else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
