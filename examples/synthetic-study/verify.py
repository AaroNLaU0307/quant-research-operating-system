"""Independent recomputation for STUDY_SYNTHETIC_001. Standard library only.

This is the REVIEWER's tool, not the builder's. It deliberately does not
import `analyze.py`: the whole value of the step is that the statistic is
produced a second time, from the raw sample and the sealed definition, by
something that has not seen the builder's implementation or the builder's
claimed number.

It implements the sealed feature definition directly:

    signal_t = mean(r[t-K+1 .. t])        K = 10, window ENDS at t
    IC       = pearson(signal_t, r[t+1])

Run inside the reviewer's evidence surface, whose contents are enumerated in
the dispatch. The builder's report is not part of that surface before the
freeze point, and this script never opens it.

Usage:
    python verify.py --data data/sample_development.csv --freeze frozen_result.json
"""

import argparse
import csv
import hashlib
import json
import math

K = 10  # from the sealed preregistration


def read_returns(path):
    with open(path, encoding="utf-8") as fh:
        return [float(row["return"]) for row in csv.DictReader(fh)]


def independent_ic(returns, k=K):
    """Recomputed from the sealed definition, without reference to the builder."""
    xs, ys = [], []
    for t in range(k - 1, len(returns) - 1):
        window = returns[t - k + 1:t + 1]          # ends at t, by definition
        assert len(window) == k
        xs.append(sum(window) / k)
        ys.append(returns[t + 1])                  # the target, never in the window

    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/sample_development.csv")
    ap.add_argument("--freeze", default="frozen_result.json")
    args = ap.parse_args()

    returns = read_returns(args.data)
    ic, n = independent_ic(returns)

    result = {
        "study_id": "STUDY_SYNTHETIC_001",
        "statistic": "information_coefficient",
        "recomputed_from": "sealed definition + raw development sample",
        "window_k": K,
        "paired_observations": n,
        "value": round(ic, 6),
    }
    body = json.dumps(result, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(body).hexdigest()

    with open(args.freeze, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print("independent information_coefficient = %.6f" % ic)
    print("paired observations                 = %d" % n)
    print("frozen result written to            = %s" % args.freeze)
    print("frozen result sha256                = %s" % digest)
    print()
    print("FREEZE this result before any comparand is delivered.")


if __name__ == "__main__":
    main()
