# Verification Brief — `<BRIEF_ID>` (review `<REVIEW_ID>`)

> This template operationalizes the following QROS rules:
> `QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE` · `QROS-BLIND-PRE-FREEZE-SET` ·
> `QROS-BLIND-FREEZE-POINT` · `QROS-BLIND-BYTE-IDENTITY-NO-JUDGMENT` ·
> `QROS-REVIEW-BLOCKING-REQUIREMENTS` · `QROS-REVIEW-EVIDENCE-CLASSES` ·
> `QROS-REVIEW-VERDICTS` · `QROS-THREAT-VOCABULARY`.
>
> `../SPEC.md` is the sole normative source. This brief states a task; it does
> not define a rule.

This brief is fixed and digested **before** dispatch. Its digest is recorded in
`dispatch.md` §6. It is not edited afterwards.

---

## 0. Blindness self-check — complete before this brief is released

```yaml
blindness_required: CLAIM_BLIND | OUTCOME_BLIND | NONE   # from dispatch.md §5
```

| Check | Answer |
|---|---|
| Does this brief state the producer's conclusion, verdict, or claimed values? | YES / NO |
| Does it state the target metric, an effect size, or any revealed result? | YES / NO |
| Does any example, tolerance, or expected value here disclose the answer? | YES / NO |

Under `CLAIM_BLIND` the first must be **NO**. Under `OUTCOME_BLIND` all three
must be **NO**. A `YES` where the level prohibits it means the brief is not
releasable at that level: revise the brief, not the level, unless the `OWNER`
changes the level.

```yaml
self_check_passed: YES | NO
checked_by:        <ROLE_BINDING>
checked_at:        <ISO8601_UTC>
```

## 1. The review question

State in one or two sentences exactly what must be established.

```
<REVIEW_QUESTION>
```

```yaml
smallest_scope:   <the narrowest artifact, component, or property that answers it>
out_of_scope:     <what this review is explicitly not asked to judge>
```

Naming what is out of scope is not a gag. A finding outside scope is still
reportable — record it under §6 `OUT_OF_SCOPE_OBSERVATIONS`, where it becomes
backlog rather than a blocking finding on this review.

## 2. Properties to establish

| # | Property | How it is to be established | Settles what |
|---|---|---|---|
| 1 | `<PROPERTY>` | `<recompute / inspect / execute>` | `<what follows if it holds>` |

For each property, state what a **failure** would look like. A property whose
failure cannot be described is not checkable.

## 3. Allowed evidence and actions

```yaml
pre_freeze_manifest_id:  <MANIFEST_ID>     # matches dispatch.md §7
manifest_digest:         <DIGEST>
```

| | |
|---|---|
| **Allowed material** | everything in the manifest, and nothing else |
| **Allowed commands** | `<enumerate>` |
| **Execution note** | executing an allowed module may load its dependencies; that is execution, not inspection — record it |
| **Prohibited** | `<material outside the manifest; searching for governing authority; any write to the project>` |
| **If a required check cannot be completed** | stop, report the surface as insufficient, and do not seek the missing material |

**First action:** recompute every digest in the manifest. A mismatch is a stop
condition and is reported as a transport failure, not as a finding against the
work.

## 4. Matching rules — fixed here, before exposure

`QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE`. Any rule with judgment space
that is not written here is not blind.

### 4.1 Byte-identity comparisons (no judgment)

May be performed at any time — `QROS-BLIND-BYTE-IDENTITY-NO-JUDGMENT`.

| # | What is compared | Comparison |
|---|---|---|
| 1 | `<ITEM>` | digest equality / exact content equality |

### 4.2 Judgment-bearing rules (must be fixed here)

| # | Rule | Exact criterion | Tolerance |
|---|---|---|---|
| 1 | `<RULE>` | `<fully determined criterion>` | `<value or NONE>` |

A tolerance of `NONE` means exact. An empty §4.2 means the review contains no
judgment-bearing comparison.

## 5. Freeze

`QROS-BLIND-FREEZE-POINT`. Before any comparand is delivered:

1. Write your result to `<FROZEN_RESULT_PATH>`.
2. Record its digest.
3. Write the freeze marker.

```yaml
freeze_marker:
  frozen_result:  <RELATIVE_PATH>
  digest:         <DIGEST>
  frozen_at:      <ISO8601_UTC>
```

Then notify the dispatcher. Post-freeze material is delivered only after the
marker exists. **The frozen result does not change afterwards** — where the
comparison reveals a discrepancy, the discrepancy is the finding.

## 6. Output

Return an attestation using `attestation.md` with `review_id: <REVIEW_ID>`.

**Verdict** — exactly one of `PASS`, `PASS_WITH_BACKLOG`, `HOLD`.

**Findings table** — one row per finding:

| id | blocking | threat class | evidence class | evidence | smallest scope | minimal fix | minimal test that settles it |
|---|---|---|---|---|---|---|---|

A **blocking** finding requires all four of: exactly one threat class; a
concrete failure path; an evidence class; the smallest affected scope
(`QROS-REVIEW-BLOCKING-REQUIREMENTS`). A finding missing any of them is
non-blocking.

```
threat classes    RESEARCH_CORRECTNESS · REPRODUCIBILITY ·
                  DATA_IDENTITY_OR_PROVENANCE · INDEPENDENCE_OR_BLINDNESS ·
                  CONSEQUENTIAL_EXECUTION_SAFETY · METHODOLOGY_OR_SCOPE_INTEGRITY
evidence classes  REPRODUCED · REASONED · SELF_REPORTED
```

A `SELF_REPORTED` finding is never blocking on its own
(`QROS-REVIEW-SELF-REPORTED-NOT-BLOCKING`). A `REASONED` finding may be
blocking where it names a threat and a concrete failure path.

A review that cannot substantiate a blocking finding returns
`PASS_WITH_BACKLOG`, not `HOLD`.

**Also required:**

```yaml
OUT_OF_SCOPE_OBSERVATIONS:  <list | NONE>
INDEPENDENCE_STATEMENT:     <per dimension and per target — QROS-INDEP-STATE-PER-DIMENSION>
```
