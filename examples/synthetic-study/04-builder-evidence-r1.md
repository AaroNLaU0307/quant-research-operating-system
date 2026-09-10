# Builder evidence — round 1 — `STUDY_SYNTHETIC_001`

```
RECORD_TYPE = BUILDER_EVIDENCE
ROUND       = 1
PRODUCED_BY = ROLE_BINDING_MAIN_AGENT
PRODUCED_AT = 2000-01-04T14:00:00Z
ARTIFACT    = ARTIFACT_SYNTHETIC_ANALYSIS_R1
```

This record is a **`BUILDER_CLAIM`** together with the **`MECHANICAL_EVIDENCE`**
that supports parts of it. Neither is independent verification
(`QROS-EVIDENCE-SEPARATION`). It is written before any review is dispatched.

---

## 1. What was built

`analyze.py` computes the sealed statistic on `SAMPLE_SYNTHETIC_DEVELOPMENT`:
the trailing ten-period mean of returns, paired with the following period's
return, correlated.

## 2. Builder claim

```
BUILDER_CLAIM: information_coefficient = 0.331216 on 2990 paired observations.
```

Under the sealed decision rules this would fire rule 2 (`>= 0.15`) and the
candidate would be `supported`.

**Reproduce:**

```
python analyze.py --data data/sample_development.csv --with-defect
```

## 3. Mechanical evidence

`QROS-CHECK-MACHINE-BEFORE-MODEL` — deterministic checks were run before any
review was dispatched. Four existed at this point; all passed.

| # | Check | Result | What it established |
|---|---|---|---|
| 1 | signal length | PASS | `len(signal) == len(returns) == 3000` |
| 2 | no nulls in pairs | PASS | 2990 paired observations, every value finite |
| 3 | pairing alignment | PASS | signals and targets pair one-to-one |
| 4 | determinism | PASS | two runs of the statistic agree exactly |

**Reproduce:** the four checks above are checks 1–4 in `checks.py`.

## 4. What the mechanical evidence does NOT establish

Stated by the builder, before review, because a check's silence is not a result:

- Nothing about whether the signal is computed from information available at
  the time it is dated. Every one of the four checks is a **shape** check; each
  would pass identically on a signal that had been handed the answer.
- Nothing about whether the statistic answers the sealed question.
- Nothing about the magnitude being real rather than an artefact.

There is no check here for **look-ahead**. That gap is the reason this
statistic is not a verified result, and it is why an independent recomputation
is being dispatched rather than treated as ceremony.

## 5. Exposure caused by producing this

`QROS-AXIS-OUTCOME-EXPOSURE`.

| Party | Target | Level |
|---|---|---|
| `ROLE_BINDING_MAIN_AGENT` | `information_coefficient` | `TARGET_METRIC` |
| `ROLE_BINDING_OWNER` | `information_coefficient` | `NONE` |
| `ROLE_BINDING_INDEPENDENT_REVIEWER` | `information_coefficient` | `NONE` |

The `OWNER` remains unexposed: no reveal has been authorised
(`QROS-OWNER-REVEAL`). The reviewer must remain unexposed until it has frozen
its own recomputation, which is why the number above is **not** in the
pre-freeze evidence surface.

## 6. Requested next step

Dispatch an outcome-blind independent recomputation of the sealed statistic
from the raw sample. Trigger: baseline item 2 — the final result that a
decision rule reads, before it is revealed to the decision-maker.
