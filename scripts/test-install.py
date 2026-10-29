#!/usr/bin/env python3
"""Test a standalone installer against every skill directory and existing backups.

Usage:
  python scripts/test-install.py --self-test --shell bash
  python scripts/test-install.py --self-test --shell powershell

--root selects a repository fixture for a regression test. No installed user skill is touched.
"""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def files(root):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob("*") if p.is_file()}


def self_test(root, shell):
    exe = shutil.which("bash" if shell == "bash" else "pwsh")
    if not exe:
        raise RuntimeError(f"{shell} is required for this installer test")
    script = root / ("install.sh" if shell == "bash" else "install.ps1")
    skills = sorted(p for p in (root / "skills").iterdir()
                    if p.is_dir() and p.name.startswith("mm-") and (p / "SKILL.md").is_file())
    if not skills:
        raise AssertionError("the repository fixture has no mm-* skills")
    argv = [exe, str(script)] if shell == "bash" else [exe, "-NoProfile", "-File", str(script)]
    with tempfile.TemporaryDirectory(prefix="mm-install-") as tmp:
        dest = Path(tmp) / "skills with spaces"
        env = dict(os.environ, MM_SKILLS_DIR=str(dest))

        def install():
            result = subprocess.run(argv, cwd=root, env=env, capture_output=True, text=True)
            if result.returncode:
                raise AssertionError(f"installer exited {result.returncode}: {result.stdout}\n{result.stderr}")

        install()
        for source in skills:
            target = dest / source.name
            if not target.is_dir() or files(target) != files(source):
                raise AssertionError(f"first install omitted or changed {source.name}")
        print(f"  ok   {shell}: all {len(skills)} skills copied in full")

        before = {}
        for source in skills:
            target = dest / source.name
            (target / "local-note.txt").write_text("preserve this file\n", encoding="utf-8")
            before[source.name] = files(target)
        unrelated = dest / "unrelated.txt"
        unrelated.write_text("leave this alone\n", encoding="utf-8")
        install()
        for source in skills:
            backups = list(dest.glob(source.name + ".bak-*"))
            if len(backups) != 1 or files(backups[0]) != before[source.name]:
                raise AssertionError(f"reinstall lost the existing contents of {source.name}")
            if files(dest / source.name) != files(source):
                raise AssertionError(f"reinstall did not replace {source.name} with its source")
        if unrelated.read_text(encoding="utf-8") != "leave this alone\n":
            raise AssertionError("installer changed an unrelated file")
        print(f"  ok   {shell}: all {len(skills)} prior skills backed up without losing local files")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", required=True)
    parser.add_argument("--shell", choices=("bash", "powershell"), required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        self_test(args.root.resolve(), args.shell)
    except (AssertionError, OSError, RuntimeError) as ex:
        print(f"self-test FAILED: {ex}", file=sys.stderr)
        return 1
    print("self-test passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
