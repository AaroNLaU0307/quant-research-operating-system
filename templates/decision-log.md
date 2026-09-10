# Decision Log — `<PROJECT_ID>`

> This template operationalizes `QROS-RECORD-DECISION-LOG-APPEND-ONLY` ·
> `QROS-RECORD-CURRENT-VS-HISTORICAL` · `QROS-OWNER-GATE-LIST` ·
> `QROS-OWNER-REAL-RUN` · `QROS-REVIEW-VERDICTS` ·
> `QROS-REVIEW-ESCALATION-ON-EXHAUSTION`.
>
> `../SPEC.md` is the sole normative source.

**Append-only.** Entries are never edited, reordered, or removed. A correction
is a **new** entry citing the entry it corrects. A verdict recorded as `HOLD`
stays `HOLD`; its later resolution is a subsequent entry.

Three entry kinds, and no others: `OWNER_DECISION`, `REVIEW_VERDICT`,
`CORRECTION`.

```yaml
project_id:   <PROJECT_ID>
entry_count:  <N>
```

---

## Index

| entry | date | kind | subject | outcome |
|---|---|---|---|---|
| `E-<N>` | `<ISO8601_UTC>` | `<KIND>` | `<one line>` | `<one line>` |

---

## `E-<N>` — OWNER_DECISION

```yaml
entry_id:    E-<N>
kind:        OWNER_DECISION
recorded_at: <ISO8601_UTC>
decided_by:  OWNER
gate:        QROS-OWNER-REAL-RUN | QROS-OWNER-REVEAL | QROS-OWNER-DISPOSITION |
             QROS-OWNER-METHODOLOGY-CHANGE | QROS-OWNER-PUBLIC-RELEASE |
             QROS-OWNER-DESTRUCTIVE-MUTATION          # closed list; no others
decision:    AUTHORIZED | DECLINED | DEFERRED | REVOKED
subject:     <what is being decided>
basis:       <what the OWNER relied on: reviews, evidence, escalations>
```

Add the block below that matches the gate. Omit the others.

### If `gate: QROS-OWNER-REAL-RUN`

**One authorisation covers one execution.** A further execution requires a
further `OWNER_DECISION` entry, even where nothing about the work has changed.

```yaml
execution:
  execution_ref:   <EXECUTION_ID>
  purpose:         <what this execution is for>
  data_identity:   <identity of the data it reads>
  code_identity:   <code and specification identity it runs at>
  identity_verified_before_start: true | false
```

The recorded identities are re-verified against this entry immediately before
the execution begins; a mismatch is a refusal, not a warning.

An authorisation is **current** only until it is used, superseded, or revoked.
Once used, it authorises nothing further. An agent never reuses an
authorisation for a second execution, widens its recorded scope, or infers
coverage it does not state; unclear coverage takes the restrictive reading and
returns to the `OWNER`.

**Revocation** of an unused authorisation is its own entry:
`decision: REVOKED`, citing `execution_ref` and the entry that created it.

### If `gate: QROS-OWNER-REVEAL`

```yaml
reveal_target:    <who becomes exposed>
reveal_scope:     <what is disclosed>
result_record:    <where the revealed content lives>
```

The revealed content itself is never written into this log.

### If `gate: QROS-OWNER-DISPOSITION`

```yaml
disposition:      PROMOTED | FALSIFIED | RETIRED | <PROJECT_TERM>
subject_ref:      <research line or claim>
evidence_refs:    <the records relied on>
```

### If `gate: QROS-OWNER-METHODOLOGY-CHANGE`

```yaml
change_label:     METHODOLOGY_CHANGE | HYPOTHESIS_CHANGE
what_changed:     <sample definition / labels / cost model / missing-data policy /
                   primary metric / decision rule / scope>
prior_seal_ref:   <PREREG_ID and version>
new_seal_ref:     <PREREG_ID and version>
prior_evidence_disposition: <becomes historical | does not transfer>
```

A new seal never restores sample freshness (`QROS-REUSE-NEW-SEAL-NO-REFRESH`).

### If `gate: QROS-OWNER-PUBLIC-RELEASE`

```yaml
release_scope:    <what material is released, and where>
assurance_ref:    <the disclosure checks run before release>
```

### If `gate: QROS-OWNER-DESTRUCTIVE-MUTATION`

```yaml
mutation_type:    <deletion / shared-history rewrite / append-only mutation>
target:           <what is affected>
irreversible:     YES | NO
recovery_path:    <how the prior state can be recovered, or NONE>
```

---

## `E-<N>` — REVIEW_VERDICT

```yaml
entry_id:        E-<N>
kind:            REVIEW_VERDICT
recorded_at:     <ISO8601_UTC>
review_id:       <REVIEW_ID>
issue_lineage:   <LINEAGE_ID | NONE>
round:           <N> of <ROUND_BUDGET>
reviewer_role:   INDEPENDENT_REVIEWER | ARCHITECTURE_REVIEWER
reviewer_id:     <ROLE_BINDING>
verdict:         PASS | PASS_WITH_BACKLOG | HOLD
attestation_ref: <ATTESTATION_ID>
attestation_digest: <DIGEST>
brief_digest:       <DIGEST>
blindness_required: CLAIM_BLIND | OUTCOME_BLIND | NONE
blindness_achieved: CLAIM_BLIND | OUTCOME_BLIND | NONE
blocking_finding_ids: <list | NONE>
backlog_rows_opened:  <list | NONE>
round_consumed:       YES | NO
```

A `REVIEW_VERDICT` entry exists **only** where a valid review returned one of
the three verdicts above. The `verdict` field takes no other value
(`QROS-REVIEW-VERDICTS`).

### A review that never became valid produces no entry here

Where an attestation records `review_validity: INVALID` — manifest mismatch,
insufficient evidence surface, an ineligible reviewer, or exposure before the
freeze point — **no `REVIEW_VERDICT` entry is written**. No verdict was
returned, so there is nothing for this log to record.

The failure is durably recorded elsewhere: in the dispatch
(`status: TRANSPORT_FAILED`, `round_consumed: NO`), in the attestation (§7), and
as an unsatisfied-gate row in `backlog.md` §1.2. It consumes no round and leaves
the required gate unsatisfied without establishing anything about the work
(`QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION`).

No entry kind is added for this case. Should the `OWNER` later decide something
because of the failure — to change the mechanism, to accept a delay, to stop
dispatching — that decision is recorded as an `OWNER_DECISION` on its own terms.

### Escalation on exhausted budget

Where a lineage exhausts its budget unresolved, record a `REVIEW_VERDICT` entry
for the final round, then an `OWNER_DECISION` entry for the escalation
(`QROS-REVIEW-ESCALATION-ON-EXHAUSTION`). Where the `OWNER` accepts work with
findings still open, the entry says the findings **remain open and were
accepted** — not that they were resolved.

---

## `E-<N>` — CORRECTION

Corrects the record, never the history. The corrected entry stays exactly as
written.

```yaml
entry_id:       E-<N>
kind:           CORRECTION
recorded_at:    <ISO8601_UTC>
corrects_entry: E-<M>
recorded_by:    <ROLE_BINDING>
what_was_wrong: <the specific error in E-<M> as recorded>
correct_record: <what the record should be understood to say>
```

A `CORRECTION` does not reverse a decision or change a verdict. Reversing a
decision is a new `OWNER_DECISION`; a changed judgement is a new
`REVIEW_VERDICT`.
