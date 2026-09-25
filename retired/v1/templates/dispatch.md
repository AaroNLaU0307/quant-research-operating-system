# Review Dispatch — `<REVIEW_ID>`

> This template operationalizes the following QROS rules:
> `QROS-REVIEW-MANDATORY-TRIGGERS` · `QROS-REVIEW-ROUND-BUDGET` ·
> `QROS-REVIEW-ROUND-SCOPE` · `QROS-BLIND-LEVELS` · `QROS-BLIND-IS-TRANSPORT` ·
> `QROS-BLIND-PRE-FREEZE-SET` · `QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE` ·
> `QROS-INDEP-STATE-PER-DIMENSION` · `QROS-ROLE-SELF-CERTIFICATION` ·
> `QROS-ROLE-SUBAGENT-NOT-INDEPENDENT`.
>
> `../SPEC.md` is the sole normative source. This file records a dispatch; it
> does not define a rule. Where a field is unclear, the cited rule governs.

This record is completed **before** review begins and is not edited after
`status: DISPATCHED`, except to set `status`, `returned_at`, and
`round_consumed`.

---

## 1. Identity

```yaml
review_id:        <REVIEW_ID>          # unique; reused by the matching attestation
project_id:       <PROJECT_ID>
work_item:        <WORK_ITEM_ID>       # the unit of work under review
issue_lineage:    <LINEAGE_ID | NONE>  # NONE for a first review of new work;
                                       # otherwise the lineage this round belongs to
round:            <N>                  # round number within issue_lineage
round_budget:     <N>                  # configured budget; QROS-REVIEW-ROUND-BUDGET
prepared_at:      <ISO8601_UTC>
prepared_by:      <ROLE_BINDING>       # the party preparing the dispatch
```

## 2. Trigger

```yaml
trigger_source:   BASELINE | CONFIGURED | OWNER_REQUEST
trigger_ref:      <BASELINE_ITEM_N | CONFIGURED_TRIGGER_ID | OWNER_DECISION_ID>
```

`trigger_source` records why review is required at all. A dispatch with no
valid trigger under `QROS-REVIEW-MANDATORY-TRIGGERS` should not exist.

## 3. Subject

```yaml
artifact_id:      <ARTIFACT_ID>
artifact_digest:  <DIGEST>
claim_under_review: <ONE SENTENCE — what is to be established, not what the
                     producer concluded>
producer_id:      <ROLE_BINDING>       # the party that produced the artifact
producer_role:    MAIN_AGENT | <OTHER>
```

### 3.1 Round scope (round > 1 only)

`QROS-REVIEW-ROUND-SCOPE`. Left empty on a first round.

```yaml
repair_ref:            <CHANGE_ID | NONE>
declared_impact_scope: <what the producer asserts the repair could affect>
scope_contestable:     YES              # the reviewer may reject this scope as
                                        # too narrow; that rejection is a finding
```

## 4. Reviewer requirement

```yaml
required_role:        INDEPENDENT_REVIEWER | ARCHITECTURE_REVIEWER
required_independence:                   # QROS-INDEP-STATE-PER-DIMENSION
  CONTEXT_INDEPENDENCE:     REQUIRED | NOT_REQUIRED
  AUTHORSHIP_INDEPENDENCE:  REQUIRED | NOT_REQUIRED
  MODEL_DIVERSITY:          REQUIRED | NOT_REQUIRED
  EMPIRICAL_INDEPENDENCE:   REQUIRED | NOT_APPLICABLE
independence_targets: <what each required dimension must hold with respect to>
must_not_be:          <parties this reviewer must not be: the producer; a
                       subagent of the producer; a prior reviewer in this
                       lineage — state which apply>
reviewer_id:          <ROLE_BINDING | UNASSIGNED>   # set at dispatch, not before
```

## 5. Blindness and isolation

`QROS-BLIND-LEVELS`, `QROS-BLIND-IS-TRANSPORT`. Blindness is established by
control of what is technically reachable, not by instruction.

```yaml
blindness_required:   CLAIM_BLIND | OUTCOME_BLIND | NONE
isolation_mechanism:  SEPARATE_EVIDENCE_SURFACE         # the mechanism; no alternatives
```

| Field | What to record |
|---|---|
| `reachable_from_environment` | what the reviewer can technically reach |
| `inaccessible_by_boundary` | what the boundary makes unreachable |
| `boundary_established_by` | the mechanism that enforces it |
| `boundary_verified_by` | how its effectiveness is checked, and by whom |

The evidence surface is built outside the environment holding the material the
reviewer must not reach, and its contents are enumerated in advance (§7). A
review conducted inside that environment is not blind, however the environment
is arranged.

## 6. Verification brief

```yaml
brief_id:        <BRIEF_ID>
brief_digest:    <DIGEST>              # fixed before dispatch
```

The brief carries the matching rules. `QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE`
requires every judgment-bearing rule to be fixed in the brief before the
reviewer is exposed to what it judges. Byte-identity comparisons need no such
fixing.

```yaml
matching_rules_fixed_at:  <ISO8601_UTC>
judgment_bearing_rules:   PRESENT | NONE   # if PRESENT, they are in the brief
```

## 7. Pre-freeze evidence manifest

`QROS-BLIND-PRE-FREEZE-SET`.

```yaml
manifest_id:       <MANIFEST_ID>
manifest_digest:   <DIGEST>
entry_count:       <N>
```

| # | Path or identifier | Digest | Why it is in the pre-freeze set |
|---|---|---|---|
| 1 | `<ITEM>` | `<DIGEST>` | `<REASON>` |

The manifest is exhaustive. The reviewer recomputes every digest before
substantive work; a mismatch is a stop condition.

## 8. Permitted and prohibited actions

| | |
|---|---|
| **Permitted commands / actions** | `<enumerate; a module executed is not a module inspected — record which>` |
| **Prohibited access / actions** | `<enumerate: material outside the manifest; discovery of authority; any write to the project>` |
| **On insufficient evidence** | Stop and report the surface as insufficient. Do not seek the missing material. |

## 9. Expected output

```yaml
expected_verdicts:        [PASS, PASS_WITH_BACKLOG, HOLD]
expected_evidence_classes: [REPRODUCED, REASONED, SELF_REPORTED]
attestation_template:     attestation.md
attestation_review_id:    <REVIEW_ID>    # must equal §1 review_id
```

## 10. Status and routing

```yaml
status:          PREPARED | DISPATCHED | RETURNED | TRANSPORT_FAILED | WITHDRAWN
dispatched_at:   <ISO8601_UTC | NONE>
returned_at:     <ISO8601_UTC | NONE>
round_consumed:  YES | NO
attestation_ref: <ATTESTATION_ID | NONE>
```

**`round_consumed` is `YES` only when a dispatched review returned a substantive
verdict.** It is `NO` for `PREPARED`, `WITHDRAWN`, and `TRANSPORT_FAILED`.

| Status | Meaning | Round consumed |
|---|---|---|
| `PREPARED` | assembled, not yet handed over | NO |
| `DISPATCHED` | handed to the reviewer | pending |
| `RETURNED` | a verdict came back | YES |
| `TRANSPORT_FAILED` | manifest mismatch, insufficient surface, exposure before freeze, or ineligible reviewer | **NO** |
| `WITHDRAWN` | never dispatched | NO |

`TRANSPORT_FAILED` records a `TRANSPORT_OR_PACKAGING_FAILURE` or a
`REVIEWER_ELIGIBILITY_OR_PROCEDURAL_FAILURE`. Per
`QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION` it leaves the gate unsatisfied,
establishes nothing about the work, and consumes no round. Repair the delivery
and dispatch again under a new `review_id`, keeping `issue_lineage` and `round`
unchanged.

### Post-review routing

| Verdict | Next action |
|---|---|
| `PASS` | proceed; record the verdict in `decision-log.md` |
| `PASS_WITH_BACKLOG` | proceed; findings become rows in `backlog.md` §2 |
| `HOLD` | do not proceed on the affected path; repair, then one further round if budget remains |
| budget exhausted, unresolved | escalate to `OWNER` — `QROS-REVIEW-ESCALATION-ON-EXHAUSTION` |
