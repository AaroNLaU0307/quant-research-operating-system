# Bounded repair — `STUDY_SYNTHETIC_001` — closes finding `F1`

```
RECORD_TYPE   = REPAIR
LINEAGE       = LINEAGE_SYNTHETIC_IC        (unchanged; this is not a new issue)
CLOSES        = F1
CHANGE_LABEL  = IMPLEMENTATION_FIX
REPAIRED_BY   = ROLE_BINDING_MAIN_AGENT
REPAIRED_AT   = 2000-01-05T15:00:00Z
```

## 1. Classification, before the change was applied

`QROS-CHANGE-CLASSIFY-BEFORE-APPLY` requires the label and its evidence to be
recorded first, and `IMPLEMENTATION_FIX` requires naming the sealed requirement
the code failed to meet.

**Sealed requirement violated** — preregistration §`metric.definition`:

> signal_t is the arithmetic mean of the ten returns r_{t-9} through r_t
> inclusive. The window ENDS at t: it never contains r_{t+1} …

The implementation's window ended at `t+1`. The sealed rule was unambiguous and
the code did not meet it, so this is an `IMPLEMENTATION_FIX` and not a
`METHODOLOGY_CHANGE`. The seal is preserved and the preregistration is
unchanged.

## 2. Exactly what changed

One expression, in the signal construction:

```diff
-    signal[t] = sum(returns[t - k + 2:t + 2]) / k     # window ends at t+1
+    signal[t] = sum(returns[t - k + 1:t + 1]) / k     # window ends at t
```

The round-1 form is retained verbatim in `analyze.py` as `defective_signal`,
reachable only through `--with-defect`, so a reader can reproduce the original
number rather than take this record's word for it.

## 3. Regression test added

`QROS-LIFECYCLE-REDUCED-BUGFIX` requires a test that fails without the fix.
Check 5 in `checks.py`, truncation invariance:

> Recompute the signal on a prefix of the sample. If a signal value at a period
> inside the prefix changes when later data is withheld, the signal depends on
> the future.

| Implementation | Check 5 |
|---|---|
| round-1 defect | **FAIL** — signal at t=1999 differs when data after t is withheld |
| repaired | **PASS** — every position unchanged |

This is the reviewer's own `minimal_test` from finding `F1`, implemented as a
standing check rather than a one-off.

## 4. What was NOT changed

Stated explicitly, because a repair is the easiest place to smuggle in a rescue:

| | |
|---|---|
| Preregistration | unchanged; seal digest `bb8f114e…` still verifies |
| Threshold | unchanged at `0.15` |
| Decision rules | unchanged, same order |
| Window length K | unchanged at 10 |
| Metric definition | unchanged |
| Sample | unchanged; `SAMPLE_SYNTHETIC_RESERVED` still untouched |
| Hypothesis | unchanged |
| Parameters | none were tuned; there are no free parameters to tune |

No amendment was made to the sealed contract. The preregistration was already
exposed to an outcome at this point, and amending it to rescue the candidate is
exactly what sealing exists to prevent.

## 5. Declared impact scope for the re-review

`QROS-REVIEW-ROUND-SCOPE`. The reviewer may contest this scope; a scope
rejected as too narrow is itself a finding.

> The change affects the construction of `signal_t` and nothing else. It cannot
> affect the sample, the pairing of signal to target, the correlation
> arithmetic, or the count of paired observations — the paired-observation
> count is unchanged at 2990, which is itself checkable.

## 6. Builder claim after repair

```
BUILDER_CLAIM: information_coefficient = 0.064635 on 2990 paired observations.
```

Still a builder claim. It agrees with the value the reviewer froze in round 1,
but the builder is not the party that establishes that
(`QROS-EVIDENCE-SEPARATION`), which is why round 2 of the same lineage follows.
