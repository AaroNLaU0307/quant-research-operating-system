"""Deterministic mechanical checks for STUDY_SYNTHETIC_001.

These run BEFORE any independent review is dispatched
(`QROS-CHECK-MACHINE-BEFORE-MODEL`). They are cheap, they either pass or fail,
and none of them requires judgement.

Check 5 (truncation invariance) was ADDED BY THE ROUND-1 REPAIR. It is the
regression test for the planted defect: it fails on the defective
implementation and passes on the repaired one. Checks 1-4 pass on both, which
is the honest lesson of this example -- shape-level checks are necessary and
were not sufficient.

Usage:
    python checks.py --data data/sample_development.csv
    python checks.py --data data/sample_development.csv --with-defect
"""

import argparse
import math

import analyze


def check_signal_length(returns, signal):
    """1. The signal series is the same length as the return series."""
    return len(signal) == len(returns), "len(signal)=%d len(returns)=%d" % (
        len(signal), len(returns))


def check_no_nulls_in_pairs(returns, signal):
    """2. Every paired observation is a finite number."""
    xs, ys = analyze.pairs(signal, returns)
    ok = all(isinstance(v, float) and math.isfinite(v) for v in xs + ys)
    return ok, "%d paired observations, all finite=%s" % (len(xs), ok)


def check_pairing_alignment(returns, signal):
    """3. Signals and targets are paired one-to-one."""
    xs, ys = analyze.pairs(signal, returns)
    return len(xs) == len(ys), "len(xs)=%d len(ys)=%d" % (len(xs), len(ys))


def check_determinism(returns, with_defect):
    """4. The statistic is reproducible: same input, same output."""
    a, _ = analyze.information_coefficient(returns, with_defect=with_defect)
    b, _ = analyze.information_coefficient(returns, with_defect=with_defect)
    return a == b, "two runs agree exactly: %s" % (a == b)


def check_truncation_invariance(returns, with_defect):
    """5. ADDED BY REPAIR. A signal at t must not change when data after t is
    withheld. If it does, the signal depends on the future.

    Recompute the signal on a prefix of the sample and compare, position by
    position, against the signal computed on the full sample.
    """
    build = analyze.defective_signal if with_defect else analyze.trailing_mean_signal
    full = build(returns)
    cut = 2000
    prefix = build(returns[:cut])
    for t in range(len(prefix)):
        if prefix[t] != full[t]:
            return False, ("signal at t=%d differs when data after t is "
                           "withheld (prefix=%r full=%r): the signal depends "
                           "on the future" % (t, prefix[t], full[t]))
    return True, "signal at every position is unchanged when later data is withheld"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/sample_development.csv")
    ap.add_argument("--with-defect", action="store_true")
    args = ap.parse_args()

    returns = analyze.read_returns(args.data)
    build = analyze.defective_signal if args.with_defect else analyze.trailing_mean_signal
    signal = build(returns)

    results = [
        ("1 signal length", check_signal_length(returns, signal)),
        ("2 no nulls in pairs", check_no_nulls_in_pairs(returns, signal)),
        ("3 pairing alignment", check_pairing_alignment(returns, signal)),
        ("4 determinism", check_determinism(returns, args.with_defect)),
        ("5 truncation invariance", check_truncation_invariance(returns, args.with_defect)),
    ]

    print("implementation = %s\n"
          % ("ROUND-1 DEFECT" if args.with_defect else "repaired (sealed definition)"))
    failed = 0
    for name, (ok, detail) in results:
        print("  %-26s %-6s %s" % (name, "PASS" if ok else "FAIL", detail))
        failed += 0 if ok else 1
    print("\n%d passed, %d failed" % (len(results) - failed, failed))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
