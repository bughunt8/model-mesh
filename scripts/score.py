#!/usr/bin/env python3
"""Recompute OMO-Benchmark chain scores from data/*.csv.

Usage:
    python3 scripts/score.py --all
    python3 scripts/score.py --profile oracle --verbose
    python3 scripts/score.py --category quick
"""
from __future__ import annotations

import argparse
import csv
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

SLOT_WEIGHTS = [0.50, 0.25, 0.12, 0.08, 0.05]

GRADE_BANDS = [
    (85, "A"), (80, "A-"), (75, "B+"), (70, "B"), (65, "B-"),
    (60, "C+"), (55, "C"), (45, "D"),
]


def grade(score: float) -> str:
    for threshold, label in GRADE_BANDS:
        if score >= threshold:
            return label
    return "F"


def load_scores() -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    with open(DATA / "model-scores.csv", newline="") as fh:
        for row in csv.DictReader(fh):
            out[row["model"]] = {
                k: float(row[k]) for k in ("AE", "TO", "IP", "R", "CR", "VD", "LC", "REL")
            }
    return out


def load_fits() -> list[dict[str, str]]:
    with open(DATA / "profile-fits.csv", newline="") as fh:
        return list(csv.DictReader(fh))


def compute(profile: str, rows: list[dict[str, str]], verbose: bool) -> float:
    total = 0.0
    cxr_total = 0.0
    for row in rows:
        if row["profile"] != profile:
            continue
        fit = float(row["fit"])
        weighted = float(row["weighted"])
        cxr = float(row["cxr"])
        total += weighted
        cxr_total += cxr
        if verbose:
            print(f"  {row['slot']:>10}  {row['model']:<40} fit={fit:5.1f}  w={weighted:5.1f}  cxr={cxr:+.1f}")
    final = total + cxr_total
    if verbose:
        print(f"  {'':>10}  {'TOTAL':<40} {total:5.1f} {cxr_total:+.1f} -> {final:.1f} ({grade(final)})")
    return final


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile")
    ap.add_argument("--category")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    fits = load_fits()
    profiles = sorted({r["profile"] for r in fits})

    if args.all or (not args.profile and not args.category):
        print(f"{'profile':<24} {'score':>6}  grade")
        print("-" * 40)
        for p in profiles:
            s = compute(p, fits, verbose=False)
            print(f"{p:<24} {s:6.1f}  {grade(s)}")
        return 0

    target = args.profile or args.category
    if target not in profiles:
        print(f"unknown profile/category: {target}", file=sys.stderr)
        print("known:", ", ".join(profiles), file=sys.stderr)
        return 1

    print(f"{target}:")
    s = compute(target, fits, verbose=args.verbose)
    print(f"\nChain score: {s:.1f}  Grade: {grade(s)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
