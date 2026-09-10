# Verification Brief — `BRIEF_SYNTHETIC_R1` (review `REVIEW_SYNTHETIC_001`)

```
BRIEF_VERSION      = 1
VERIFICATION_SCOPE = the sealed statistic of STUDY_SYNTHETIC_001 on
                     SAMPLE_SYNTHETIC_DEVELOPMENT
OBLIGATION         = independent recomputation of the final statistic
BLINDNESS          = OUTCOME_BLIND
DISPATCHED_BY      = ROLE_BINDING_OWNER
DISPATCHED_AT_UTC  = 2000-01-05T09:00:00Z
```

Fixed and digested before dispatch. Not edited afterwards.

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
checked_at:        "2000-01-05T09:00:00Z"
```

The preregistered threshold is deliberately **not** repeated in this brief. You
are asked to produce a number, not to judge it against a bar.

## 1. The review question

> Computing only from the raw development sample and the sealed metric
> definition, what is the information coefficient of the sealed signal against
> the next period's return?

```yaml
smallest_scope: the single statistic named in the sealed metric definition
out_of_scope:   whether the value clears any threshold; whether the study
                should proceed; whether the generating process is realistic
```

An observation outside that scope is still reportable — record it under
`OUT_OF_SCOPE_OBSERVATIONS` in your attestation, where it becomes backlog
rather than a blocking finding on this review.

## 2. Properties to establish

| # | Property | How | A failure would look like |
|---|---|---|---|
| 1 | The signal as sealed is computable from the raw sample alone | implement the definition in §4 of the preregistration directly | the definition is ambiguous or under-determined |
| 2 | The information coefficient of that signal | recompute from the raw sample | — |
| 3 | The signal at each period uses no information dated after that period | inspect your own construction, then confirm the window bounds | the window includes the target period |

## 3. Allowed evidence and actions

```yaml
pre_freeze_manifest_id: MANIFEST_SYNTHETIC_R1
```

| | |
|---|---|
| **Allowed material** | exactly the four items enumerated in the dispatch manifest, and nothing else |
| **Allowed commands** | `python verify.py --data data/sample_development.csv --freeze frozen_result.json` |
| **Prohibited before freeze** | the builder's implementation (`analyze.py`), the builder's evidence record, the research-state page, any file not in the manifest, and the reserved sample `SAMPLE_SYNTHETIC_RESERVED` |
| **If a required check cannot be completed** | stop, report the surface as insufficient, do not go looking for the missing material |

**First action:** recompute every digest in the manifest. A mismatch is a stop
condition and is reported as a transport failure, not as a finding against the
work.

**Implement the definition yourself.** Do not reconstruct the builder's code
from memory or inference. The point of this step is a second, independent
route to the same number.

## 4. Matching rules — fixed here, before exposure

### 4.1 Byte-identity comparisons (no judgement)

| # | What | Comparison |
|---|---|---|
| 1 | every manifest item | sha256 equality against the dispatch |

### 4.2 Judgement-bearing rules

| # | Rule | Exact criterion | Tolerance |
|---|---|---|---|
| 1 | agreement between your recomputed value and the producer's, once delivered | absolute difference of the two information coefficients | `0.001` |

A difference above `0.001` is a discrepancy and must be reported. The tolerance
is fixed here, before you have seen either number.

## 5. Freeze

Write your result to `frozen_result.json`, record its sha256, and declare the
freeze. Only then are the post-freeze comparands delivered. **The frozen result
does not change afterwards** — if the comparison reveals a difference, the
difference is the finding.

## 6. Output

An attestation using `templates/attestation.md`, `review_id:
REVIEW_SYNTHETIC_001`.

Verdict: exactly one of `PASS`, `PASS_WITH_BACKLOG`, `HOLD`.

A blocking finding requires all four of: exactly one threat class from the six;
a concrete failure path on the current or next stage; an evidence class from
`REPRODUCED` / `REASONED` / `SELF_REPORTED`; and the smallest affected scope. A
`SELF_REPORTED` finding is never blocking on its own.

State independence per dimension and per target.
