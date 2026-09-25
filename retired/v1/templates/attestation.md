# Attestation — review `<REVIEW_ID>`

> This template operationalizes the following QROS rules:
> `QROS-REVIEW-VERDICTS` · `QROS-REVIEW-BLOCKING-REQUIREMENTS` ·
> `QROS-REVIEW-EVIDENCE-CLASSES` · `QROS-REVIEW-SELF-REPORTED-NOT-BLOCKING` ·
> `QROS-REVIEW-CLASSIFICATION-AUTHORITY` · `QROS-BLIND-FREEZE-POINT` ·
> `QROS-BLIND-POST-FREEZE-COMPARANDS` · `QROS-BLIND-EXPOSURE-RESPONSE` ·
> `QROS-BLIND-IS-TRANSPORT` · `QROS-INDEP-STATE-PER-DIMENSION` ·
> `QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION`.
>
> `../SPEC.md` is the sole normative source. This file records a returned
> result; it does not define a rule.

Written by the reviewer. The digest of this file is recorded by the dispatcher —
a file cannot contain its own digest.

---

## 1. Identity — must match the dispatch

```yaml
review_id:       <REVIEW_ID>          # equals dispatch.md §1 review_id
project_id:      <PROJECT_ID>
issue_lineage:   <LINEAGE_ID | NONE>  # equals dispatch.md §1 issue_lineage
round:           <N>                  # equals dispatch.md §1 round
brief_id:        <BRIEF_ID>           # equals dispatch.md §6 brief_id
brief_digest:    <DIGEST>             # recomputed by the reviewer
reviewer_id:     <ROLE_BINDING>
reviewer_role:   INDEPENDENT_REVIEWER | ARCHITECTURE_REVIEWER
returned_at:     <ISO8601_UTC>
```

## 2. Review validity — complete this before §6

A review is valid only if it was conducted under the conditions the dispatch
required. Where it was not, §7 applies and **no substantive verdict is issued**.

```yaml
manifest_id:           <MANIFEST_ID>        # equals dispatch.md §7 manifest_id
manifest_verified:     MATCH | MISMATCH
mismatched_entries:    <list | NONE>
not_the_producer:              YES | NO
not_a_subagent_of_producer:    YES | NO
not_a_prior_reviewer_in_lineage: YES | NO | NOT_APPLICABLE
surface_sufficient:    YES | NO            # NO ⇒ stop; see §7
```

### 2.1 Independence actually satisfied

`QROS-INDEP-STATE-PER-DIMENSION` — state per dimension **and per target**. Do
not assert independence as a global property.

| Dimension | Required | Satisfied | With respect to what |
|---|---|---|---|
| `CONTEXT_INDEPENDENCE` | `<from dispatch>` | YES / NO | `<target>` |
| `AUTHORSHIP_INDEPENDENCE` | `<from dispatch>` | YES / NO | `<target>` |
| `MODEL_DIVERSITY` | `<from dispatch>` | YES / NO | `<target>` |
| `EMPIRICAL_INDEPENDENCE` | `<from dispatch>` | YES / NO / NOT_APPLICABLE | `<target>` |

```yaml
independence_shortfalls: <any dimension required but not satisfied, and its
                          consequence for what this attestation certifies | NONE>
```

### 2.2 Blindness achieved

```yaml
blindness_required:  CLAIM_BLIND | OUTCOME_BLIND | NONE   # from dispatch.md §5
blindness_achieved:  CLAIM_BLIND | OUTCOME_BLIND | NONE
isolation_mechanism: SEPARATE_EVIDENCE_SURFACE          # the mechanism; no alternatives
```

`QROS-BLIND-IS-TRANSPORT` — record what was technically the case, not what was
instructed:

| Field | Reviewer's record |
|---|---|
| `reachable_from_environment` | what you could technically reach |
| `inaccessible_by_boundary` | what the boundary made unreachable |
| `boundary_established_by` | the mechanism |
| `boundary_verified_by` | how you confirmed it held, or `UNVERIFIED` |

`blindness_achieved` below `blindness_required` means the review did not meet
its blindness condition. Report it here; do not describe the review as blind.

### 2.3 Exposure events

`QROS-BLIND-EXPOSURE-RESPONSE`.

```yaml
exposure_before_freeze:  NONE | <what was reached, when, and how>
commands_run:            <list | NONE>
modules_executed_not_inspected: <list | NONE>
```

Exposure to material outside the pre-freeze set **before** the freeze point is a
stop condition: results after it are discarded and §7 applies.

### 2.4 Validity determination — decides which branch you complete

```yaml
review_validity: VALID | INVALID
```

`INVALID` where any of the following holds: `manifest_verified: MISMATCH`;
`surface_sufficient: NO`; any of the three eligibility fields is `NO`;
`exposure_before_freeze` is not `NONE`; or §4 records
`frozen_result_unmodified_after_comparands: NO`. Otherwise `VALID`.

| `review_validity` | Complete | Omit entirely |
|---|---|---|
| `VALID` | §3–§6 | §7 |
| `INVALID` | §7 | §3–§6, including the `verdict` field |

A review that never became valid produced **no verdict**. The `verdict` field is
absent from an `INVALID` attestation — absence is the representation, and no
sentinel value stands in for it.

## 3. Freeze

`QROS-BLIND-FREEZE-POINT`.

```yaml
frozen_result_path:  <RELATIVE_PATH>
frozen_result_digest: <DIGEST>
frozen_at:           <ISO8601_UTC>
freeze_marker_written: YES | NO
```

## 4. Post-freeze comparison

`QROS-BLIND-POST-FREEZE-COMPARANDS`. Completed only after §3.

```yaml
comparands_received_at:  <ISO8601_UTC | NOT_APPLICABLE>
comparands:              <list of the producer's claims / recorded values received>
```

| # | Compared | Matching rule (brief §4) | Result |
|---|---|---|---|
| 1 | `<ITEM>` | `<RULE_REF>` | MATCH / DISCREPANCY |

```yaml
discrepancies: <description of each, or NONE>
```

### Reviewer statement — required

> I confirm that the frozen result recorded in §3 was **not modified** after the
> comparands in §4 were delivered.

```yaml
frozen_result_unmodified_after_comparands: YES | NO
```

`NO` invalidates the independence of the result. Record it truthfully; §7 then
applies.

## 5. Findings

| id | blocking | threat class | evidence class | evidence | concrete failure path | smallest scope | minimal fix | minimal test |
|---|---|---|---|---|---|---|---|---|
| F1 | YES / NO | `<THREAT>` | `<CLASS>` | `<what was observed>` | `<how it produces a wrong, irreproducible, or unsafe outcome on the current or next stage>` | `<narrowest affected artifact or claim>` | `<smallest change>` | `<test that settles it>` |

```
threat classes    RESEARCH_CORRECTNESS · REPRODUCIBILITY ·
                  DATA_IDENTITY_OR_PROVENANCE · INDEPENDENCE_OR_BLINDNESS ·
                  CONSEQUENTIAL_EXECUTION_SAFETY · METHODOLOGY_OR_SCOPE_INTEGRITY
evidence classes  REPRODUCED · REASONED · SELF_REPORTED
```

A blocking finding needs all four of: exactly one threat class, a concrete
failure path, an evidence class, and the smallest affected scope. A
`SELF_REPORTED` finding is not blocking on its own.

Classification is the reviewer's (`QROS-REVIEW-CLASSIFICATION-AUTHORITY`). The
producing party does not reclassify these rows.

```yaml
out_of_scope_observations: <list | NONE>   # become backlog, never blocking here
```

## 6. Verdict — `review_validity: VALID` only

Complete this section only where §2.4 records `VALID`. Where it records
`INVALID`, omit this section in full and complete §7 instead: the `verdict`
field must not appear anywhere in the attestation.

```yaml
verdict: PASS | PASS_WITH_BACKLOG | HOLD
```

These are the only three values this field may take
(`QROS-REVIEW-VERDICTS`).

| Verdict | Condition |
|---|---|
| `PASS` | no finding requires action before proceeding |
| `PASS_WITH_BACKLOG` | findings exist; none is blocking |
| `HOLD` | at least one blocking finding — list its ids |

```yaml
blocking_finding_ids: <list | NONE>
```

A review unable to substantiate a blocking finding returns `PASS_WITH_BACKLOG`.

## 7. Invalid review — `review_validity: INVALID` only

Complete this section **instead of** §3–§6, where §2.4 records `INVALID`. This
attestation carries no `verdict` field.

```yaml
invalidity_class:       TRANSPORT_OR_PACKAGING_FAILURE | REVIEWER_ELIGIBILITY_OR_PROCEDURAL_FAILURE
invalidity_reason:      <the specific defect in the delivery or the seating>
supporting_evidence:    <mismatched digests, the material reached, the missing
                         item, or the eligibility fact — as applicable>
established_about_work: NOTHING
round_consumed:         NO
```

Per `QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION` this leaves the required gate
unsatisfied, establishes nothing about the work under review, and consumes no
round.

It is **not** a verdict of any kind. It MUST NOT be recorded as `PASS`,
`PASS_WITH_BACKLOG`, or `HOLD`, and no fourth value is introduced to stand for
it — a review that never became valid simply returned no verdict. It is also not
a finding against the work: do not open a blocker row for it
(`QROS-COMPLETION-NO-SPECULATIVE-BLOCKER`). Record the unsatisfied gate in
`backlog.md` §1.2, repair the delivery, and dispatch again.

## 8. Routing

```yaml
dispatch_ref:        <REVIEW_ID>
backlog_rows_opened: <list | NONE>
```

**If `VALID`:**

```yaml
decision_log_entry:  <ENTRY_ID | PENDING>   # the verdict is recorded there
```

**If `INVALID`:** no `decision-log.md` entry is created. The failure is durably
recorded here, in the dispatch (`status: TRANSPORT_FAILED`), and as an
unsatisfied-gate row in `backlog.md` §1.2. Should the `OWNER` later decide
something because of this failure, that decision is recorded as an
`OWNER_DECISION` on its own terms.
