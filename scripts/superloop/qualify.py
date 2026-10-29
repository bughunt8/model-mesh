"""Qualify a decision threshold on labelled local data before it may act.

A point threshold such as 0.8 is a label, not a promise. This module turns labelled shadow
decisions into a qualification record with a fixed-sequence Learn-then-Test procedure:

  For thresholds ordered from strictest to most lenient, test the null hypothesis
  "the error rate among accepted decisions is above alpha" with an exact binomial tail.
  Stop at the first threshold whose p-value exceeds delta. The last rejected threshold is
  qualified. Fixed-sequence testing keeps the family-wise error at delta without a
  multiple-testing correction.

The promise holds only for traffic like the labelled set. A new backend, model version,
question revision, state format or locale needs a new record. Labels must come from people or
from deterministic ground truth, never from the decision model itself.

Labelled decision: {"score": p, "correct": bool, "label_source": "human" | "ground_truth"},
where score is the quantity the gate reads (noul probability, or the chosen option's
probability for a choice).

A controller never states a threshold itself. It points at a record file written by
make_record, and the driver calls verify_record at admission: the dataset must still hash to
the recorded value, every label must name a human or ground-truth source, and re-running the
procedure on the dataset must give the recorded threshold.

  python scripts/superloop/qualify.py --dataset LABELS.jsonl --alpha 0.05 --delta 0.05 \
      --grid 0.99,0.95,0.9 --model M --question Q --revision 1 --locale en --out RECORD.json
"""
import argparse, hashlib, json, math, os, sys

MIN_LABELLED = 100
LABEL_SOURCES = ("human", "ground_truth")


def binom_cdf(k, n, p):
    """P(X <= k) for X ~ Binomial(n, p), computed in log space."""
    if k >= n:
        return 1.0
    total = 0.0
    lp, lq = math.log(p), math.log1p(-p)
    for i in range(k + 1):
        total += math.exp(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * lp + (n - i) * lq)
    return min(1.0, total)


def qualify(labelled, alpha, delta, grid, min_accepted=30):
    """Return a record: {"threshold", "accepted", "errors", "p_value", "tested": [...]}.
    threshold is None when no grid value qualifies."""
    tested, best = [], None
    for t in sorted(set(grid), reverse=True):
        acc = [d for d in labelled if d["score"] >= t]
        n = len(acc)
        k = sum(1 for d in acc if not d["correct"])
        if n < min_accepted:
            tested.append({"threshold": t, "accepted": n, "errors": k, "p_value": None, "rejected": False,
                           "note": "too few accepted decisions"})
            continue
        pv = binom_cdf(k, n, alpha)
        rej = pv <= delta
        tested.append({"threshold": t, "accepted": n, "errors": k, "p_value": round(pv, 6), "rejected": rej})
        if not rej:
            break
        best = {"threshold": t, "accepted": n, "errors": k, "p_value": round(pv, 6)}
    out = dict(best or {"threshold": None, "accepted": 0, "errors": 0, "p_value": None})
    out.update({"alpha": alpha, "delta": delta, "method": "learn-then-test-fixed-sequence", "tested": tested,
                "labelled": len(labelled)})
    return out


def _sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def load_dataset(path):
    text = open(path, encoding="utf-8").read()
    try:
        rows = json.loads(text)
    except ValueError:
        rows = [json.loads(l) for l in text.splitlines() if l.strip()]
    return rows


def make_record(dataset, alpha, delta, grid, model, question_id, revision, locale):
    rows = load_dataset(dataset)
    bad = [i for i, r in enumerate(rows) if r.get("label_source") not in LABEL_SOURCES]
    if bad:
        raise ValueError(f"rows {bad[:5]} have no human or ground_truth label_source")
    rec = qualify(rows, alpha, delta, grid)
    rec.update({"grid": sorted(set(grid), reverse=True), "dataset": os.path.abspath(dataset),
                "dataset_sha256": _sha(dataset), "model": model, "question_id": question_id,
                "revision": revision, "locale": locale})
    return rec


def verify_record(path, model, question_id, revision, locale):
    """Return (threshold, error). threshold is None when the record cannot act."""
    try:
        rec = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as ex:
        return None, f"qualification record unreadable: {ex}"
    if (rec.get("model"), rec.get("question_id"), rec.get("revision"), rec.get("locale")) != \
            (model, question_id, revision, locale):
        return None, "qualification record is for another model, question, revision or locale"
    if rec.get("method") != "learn-then-test-fixed-sequence":
        return None, "qualification method must be learn-then-test-fixed-sequence"
    for k in ("alpha", "delta"):
        if not isinstance(rec.get(k), (int, float)) or not 0 < rec[k] <= 0.1:
            return None, f"qualification {k} must be in (0, 0.1]"
    ds = rec.get("dataset")
    if not isinstance(ds, str) or not os.path.isfile(ds) or _sha(ds) != rec.get("dataset_sha256"):
        return None, "the labelled dataset is missing or no longer matches its recorded hash"
    rows = load_dataset(ds)
    if len(rows) < MIN_LABELLED:
        return None, f"qualification needs at least {MIN_LABELLED} labelled decisions"
    if any(r.get("label_source") not in LABEL_SOURCES for r in rows):
        return None, "every label must come from a person or deterministic ground truth"
    again = qualify(rows, rec["alpha"], rec["delta"], rec.get("grid", []))
    if again["threshold"] is None or again["threshold"] != rec.get("threshold"):
        return None, "re-running learn-then-test on the dataset does not give the recorded threshold"
    return again["threshold"], None


def main(argv):
    ap = argparse.ArgumentParser()
    for k in ("dataset", "model", "question", "locale", "out", "grid"):
        ap.add_argument("--" + k, required=True)
    ap.add_argument("--alpha", type=float, required=True)
    ap.add_argument("--delta", type=float, required=True)
    ap.add_argument("--revision", type=int, required=True)
    a = ap.parse_args(argv)
    rec = make_record(a.dataset, a.alpha, a.delta, [float(x) for x in a.grid.split(",")], a.model, a.question,
                      a.revision, a.locale)
    json.dump(rec, open(a.out, "w", encoding="utf-8"), indent=2)
    print(json.dumps({k: rec[k] for k in ("threshold", "accepted", "errors", "labelled")}))
    return 0 if rec["threshold"] is not None else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
