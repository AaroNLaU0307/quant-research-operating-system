"""Deterministic synthetic data generator for STUDY_SYNTHETIC_001.

Standard library only. Same seed always produces the same series.

The data-generating process is FABRICATED. It represents no market, no
instrument, and no real research. Its parameters were chosen analytically
before any data was generated, so the expected behaviour of the study was
known by design rather than discovered by inspecting results.

    z_t ~ N(0, 1), independent
    r_t = z_t + GAMMA * z_{t-1}            (a moving-average process)

Two consequences follow analytically, and are the whole point of the example:

  * A trailing K-period mean of r carries a small genuine relationship with
    the NEXT period's r, because both contain z_t. With GAMMA = 0.25 and
    K = 10 the population information coefficient is about 0.062.

  * If that same window is shifted forward by one period so that it contains
    r_{t+1} itself, the information coefficient rises to about 0.327 -- not
    because the feature predicts anything, but because it has been told the
    answer.

The preregistered threshold sits between those two values.

Usage:
    python generate.py [--out DIR]

Writes:
    <out>/sample_development.csv   periods 0..2999      (may be read)
    <out>/sample_reserved.csv      periods 3000..3999   (reserved; not read
                                   by this study)
"""

import argparse
import os
import random

SEED = 20260910
GAMMA = 0.25
N_DEVELOPMENT = 3000
N_RESERVED = 1000


def generate(seed=SEED, n_total=N_DEVELOPMENT + N_RESERVED, gamma=GAMMA):
    """Return the synthetic return series, deterministically."""
    rng = random.Random(seed)
    z = [rng.gauss(0.0, 1.0) for _ in range(n_total + 1)]
    # r_t = z_t + gamma * z_{t-1}; z[0] is the pre-sample innovation.
    return [z[t + 1] + gamma * z[t] for t in range(n_total)]


def write_csv(path, start_period, values):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("period,return\n")
        for i, v in enumerate(values):
            fh.write("%d,%.10f\n" % (start_period + i, v))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    series = generate()
    write_csv(os.path.join(args.out, "sample_development.csv"), 0,
              series[:N_DEVELOPMENT])
    write_csv(os.path.join(args.out, "sample_reserved.csv"), N_DEVELOPMENT,
              series[N_DEVELOPMENT:])

    print("seed                = %d" % SEED)
    print("gamma               = %s" % GAMMA)
    print("development periods = %d  -> %s/sample_development.csv"
          % (N_DEVELOPMENT, args.out))
    print("reserved periods    = %d  -> %s/sample_reserved.csv  (NOT read by "
          "this study)" % (N_RESERVED, args.out))


if __name__ == "__main__":
    main()
