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

Labelled decision: {"score": p, "correct": bool}, where score is the quantity the gate reads
(noul probability, or the chosen option's probability for a choice).
"""
import math


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
