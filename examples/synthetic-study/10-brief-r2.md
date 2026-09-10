# Verification Brief — `BRIEF_SYNTHETIC_R2` (review `REVIEW_SYNTHETIC_002`)

```
BRIEF_VERSION      = 1
VERIFICATION_SCOPE = the repair closing F1, plus the producer-declared impact
                     scope, plus the sealed statistic recomputed after it
OBLIGATION         = independent recomputation of the final statistic
BLINDNESS          = OUTCOME_BLIND
LINEAGE            = LINEAGE_SYNTHETIC_IC, round 2 of 2
DISPATCHED_BY      = ROLE_BINDING_OWNER
DISPATCHED_AT_UTC  = 2000-01-06T09:00:00Z
```

Round 2 of the same issue lineage. Budget after this round is exhausted; an
unresolved disagreement escalates to the `OWNER` rather than opening a round 3
(`QROS-REVIEW-ESCALATION-ON-EXHAUSTION`).

---

## 0. Blindness self-check — completed before release

```yaml
blindness_required: OUTCOME_BLIND
```

| Check | Answer |
|---|---|
| Does this brief state the producer's conclusion, verdict, or claimed values? | NO |
| Does it state the target metric, an effect size, or any revealed result? | NO |
| Does any example, tolerance, or expected value here disclose the answer? | NO |

```yaml
self_check_passed: YES
checked_by:        ROLE_BINDING_OWNER
checked_at:        "2000-01-06T09:00:00Z"
```

You are a fresh seat. You did not perform round 1 and you have not been given
its frozen value or its verdict. Produce your own number.

## 1. The review question

> Does the repaired implementation now compute the signal as the sealed
> definition states, and what is the information coefficient of that signal
> against the next period's return?

```yaml
smallest_scope: the signal construction, and the statistic that follows from it
out_of_scope:   whether the value clears any threshold; what should be done
                about the result
```

## 2. Properties to establish

| # | Property | How | A failure would look like |
|---|---|---|---|
| 1 | The information coefficient, recomputed independently | implement the sealed definition directly from the raw sample | — |
| 2 | The signal uses no information dated after the period it is dated at | run the truncation-invariance check on the repaired implementation | a signal value changes when later data is withheld |
| 3 | The producer's declared impact scope is not too narrow | check the paired-observation count and the sample identity are unchanged, and that nothing outside the signal construction moved | the change touched the pairing, the sample, or the arithmetic |

Property 3 exists because a repair's declared scope is contestable. If you
judge the scope too narrow, that is a finding.

## 3. Allowed evidence and actions

```yaml
pre_freeze_manifest_id: MANIFEST_SYNTHETIC_R2
```

| | |
|---|---|
| **Allowed material** | the items enumerated in the dispatch manifest, and nothing else |
| **Allowed commands** | `python verify.py --data data/sample_development.csv --freeze frozen_result.json`; `python checks.py --data data/sample_development.csv` |
| **Prohibited before freeze** | the round-1 attestation and its frozen value, the builder evidence records, the research-state page, the decision log, the reserved sample |
| **If a required check cannot be completed** | stop and report the surface as insufficient |

The repaired implementation **is** in this manifest, because property 2 and
property 3 require inspecting it. Your own recomputation must still be written
from the sealed definition, not adapted from it.

**First action:** recompute every manifest digest. A mismatch is a stop
condition.

## 4. Matching rules — fixed here, before exposure

### 4.1 Byte-identity comparisons (no judgement)

| # | What | Comparison |
|---|---|---|
| 1 | every manifest item | sha256 equality against the dispatch |

### 4.2 Judgement-bearing rules

| # | Rule | Exact criterion | Tolerance |
|---|---|---|---|
| 1 | agreement between your recomputed value and the producer's, once delivered | absolute difference of the two information coefficients | `0.001` |
| 2 | declared impact scope adequate | paired-observation count and sample identity unchanged from round 1 as recorded in the dispatch | exact |

## 5. Freeze

Write your result, record its sha256, declare the freeze. Comparands follow.
The frozen result does not change afterwards.

## 6. Output

An attestation using `templates/attestation.md`, `review_id:
REVIEW_SYNTHETIC_002`. Verdict: exactly one of `PASS`, `PASS_WITH_BACKLOG`,
`HOLD`. Blocking findings need all four elements. State independence per
dimension and per target.
