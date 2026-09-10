"""Builder-side analysis for STUDY_SYNTHETIC_001. Standard library only.

Computes the preregistered statistic: the information coefficient (IC) of a
trailing K-period mean of returns against the NEXT period's return, on the
development sample.

The implementation below is the REPAIRED one. The single planted defect that
round 1 shipped is reproducible with --with-defect, which is kept so a reader
can verify the story rather than take it on trust. Do not use that flag for
anything but the demonstration.

Usage:
    python analyze.py --data data/sample_development.csv
    python analyze.py --data data/sample_development.csv --with-defect
"""

import argparse
import csv
import math

WINDOW = 10  # K, fixed by the sealed preregistration


def read_returns(path):
    with open(path, encoding="utf-8") as fh:
        return [float(row["return"]) for row in csv.DictReader(fh)]


def trailing_mean_signal(returns, k=WINDOW):
    """Sealed definition: signal_t = mean(r[t-k+1 .. t]).

    The window ENDS at t. It never contains r[t+1], which is the quantity the
    signal is asked to predict.
    """
    signal = [None] * len(returns)
    for t in range(k - 1, len(returns)):
        signal[t] = sum(returns[t - k + 1:t + 1]) / k
    return signal


def defective_signal(returns, k=WINDOW):
    """ROUND-1 DEFECT, retained for demonstration only.

    The window was written as r[t-k+2 .. t+1]: shifted forward by one period,
    so it CONTAINS r[t+1]. The signal is therefore partly a copy of the target.
    Shapes, lengths, dtypes and null counts are identical to the correct
    version, which is why the shape-level checks did not notice.
    """
    signal = [None] * len(returns)
    for t in range(k - 1, len(returns) - 1):
        signal[t] = sum(returns[t - k + 2:t + 2]) / k
    return signal


def pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    return sxy / math.sqrt(sxx * syy)


def pairs(signal, returns):
    """Pair signal_t with r[t+1]. Drop periods where the signal is undefined."""
    xs, ys = [], []
    for t in range(len(returns) - 1):
        if signal[t] is not None:
            xs.append(signal[t])
            ys.append(returns[t + 1])
    return xs, ys


def information_coefficient(returns, with_defect=False):
    signal = defective_signal(returns) if with_defect else trailing_mean_signal(returns)
    xs, ys = pairs(signal, returns)
    return pearson(xs, ys), len(xs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/sample_development.csv")
    ap.add_argument("--with-defect", action="store_true",
                    help="reproduce the round-1 defective computation")
    args = ap.parse_args()

    returns = read_returns(args.data)
    ic, n = information_coefficient(returns, with_defect=args.with_defect)

    print("implementation      = %s"
          % ("ROUND-1 DEFECT (window shifted forward by one)" if args.with_defect
             else "sealed definition (trailing window ending at t)"))
    print("window K            = %d" % WINDOW)
    print("paired observations = %d" % n)
    print("information_coefficient = %.6f" % ic)


if __name__ == "__main__":
    main()
