# Decision Log — `<PROJECT_ID>`

> This template operationalizes `QROS-RECORD-DECISION-LOG-APPEND-ONLY` ·
> `QROS-RECORD-CURRENT-VS-HISTORICAL` · `QROS-VERDICT-RECORD` ·
> `QROS-VERDICT-VOCABULARY` · `QROS-GATE-OWNER-RETAINED` ·
> `QROS-GATE-DELEGATED` · `QROS-GATE-NO-RELAY` ·
> `QROS-GATE-NO-SELF-AUTHORIZATION` · `QROS-RUN-SEAL-NOT-AUTHORIZATION` ·
> `QROS-RUN-ONE-SHOT-WRITE-AHEAD` · `QROS-CHANGE-CLASSIFY-BEFORE-APPLY` ·
> `QROS-CHANGE-DEFECT-IMPACT`.
>
> `../SPEC.md` is the sole normative source. Each entry validates against
> `../schemas/decision-log-entry.schema.json`.

**Append-only.** Entries are never edited, reordered or removed. Each is written
when the event happens, never reconstructed from a later state; an event that
cannot be established is recorded as `UNKNOWN`. A correction is a **new** entry
that cites the entry it corrects. The `BUILDER` is the only writer; the `OWNER`
and the `DELEGATE` send decisions, which are recorded verbatim with their sender
**before** they are acted on.

A grant lives in exactly one place: its `grant` entry. The current-state
artifact points here; it never restates a grant.

---

## Every entry

```yaml
id:        E-<N>
utc:       <ISO8601_UTC>                  # when the event happened
decider:
  role:    OWNER | DELEGATE | BUILDER
  party:   <concrete party that decided>  # QROS-ROLE-VENDOR-BINDING-IS-CONFIG
type:      grant | consumption | seal | reveal | verdict | disposition |
           methodology_change | delegate_decision | owner_decision | correction
decision:  <what was decided, one or two sentences>
evidence:  <path | commit | persisted message | UNKNOWN>
gate:      <a retained gate: QROS-OWNER-SPEND | QROS-OWNER-LIVE-CAPITAL |
            QROS-OWNER-CREDENTIALS | QROS-OWNER-PUBLIC-RELEASE |
            QROS-OWNER-DESTRUCTIVE-MUTATION;
            or a delegated gate: S0_DECISION | SEAL | RUN_AUTHORIZATION | STATISTICAL_REVEAL |
            S4_VERDICT | PROMOTION_FALSIFICATION_RETIREMENT_CLOSURE |
            SCOPE_OR_METHODOLOGY_CHANGE | DATA_ACCESS_BEYOND_GRANT | LOCAL_MERGE>
verbatim:                                 # required when the decision arrived
  text:         <the message, exactly>    # as a message; always for OWNER
  sender:       { role: <ROLE>, party: <PARTY> }
  received_utc: <ISO8601_UTC>
  channel:      DIRECT | RELAYED          # RELAYED never suffices for a
                                          # retained gate (QROS-GATE-NO-RELAY)
```

Who may decide what:

| type | decider |
|---|---|
| `grant`, `seal`, `reveal`, `verdict` | `DELEGATE`, or `OWNER`; never the `BUILDER` (`QROS-GATE-NO-SELF-AUTHORIZATION`) |
| any entry naming a retained gate (`QROS-GATE-OWNER-RETAINED`) | `OWNER` only, received `DIRECT` |
| `consumption` | whoever runs; written by the runner |
| `methodology_change` labelled `IMPLEMENTATION_FIX` / `DATA_FIX` | `BUILDER` |
| `methodology_change` labelled `ANALYSIS_EXTENSION` / `METHODOLOGY_CHANGE` / `HYPOTHESIS_CHANGE` | `DELEGATE`, or `OWNER` |
| `delegate_decision` / `owner_decision` | that role |

Add the block that matches the `type`. Omit the others.

## `grant`

```yaml
grant:
  mode:   ONE_SHOT | STANDING
  scope:  <what is authorized, and what is not>
  covers:
    preregistration: <PREREG_ID and version>
    seal:            <seal manifest digest>
    code:            <commit or digest>
    data:            <digest>
    environment:     <lockfile digest, where relevant>
  grantee:           { role: BUILDER, party: <PARTY> }
  run_gate_evidence: <the green mechanical run gate (QROS-RUN-GATE-MECHANICAL)>
  # revokes_entry:   E-<M>                # only when this entry revokes a grant
```

A seal is not a grant. Unclear coverage takes the restrictive reading: the run
guard fails closed (`QROS-RUN-FAIL-CLOSED`).

## `consumption`

Written by the runner **before** it touches outcomes. A grant with any evidence
of use is consumed — including a partial, crashed or indeterminate run — and
nothing reverses consumption.

```yaml
consumption:
  grant_entry: E-<M>
  run_ref:     <RUN_ID>
  written_before_outcome_access: true
  run_state:   STARTED | COMPLETED | CRASHED | INDETERMINATE
```

## `seal`

```yaml
seal:
  prereg_ref:        <PREREG_ID and version>
  manifest_ref:      <path of the digest manifest>
  manifest_digest:   <DIGEST>
  parent_seal:       <prior seal | NONE>
  resolvability_ref: <where resolvability was shown>
```

## `reveal`

```yaml
reveal:
  reveal_to:     [<party>, …]             # exposure is recorded per party
  reveal_scope:  <what is disclosed>
  result_record: <where the revealed content lives>
  validity_checks_passed_ref: <evidence the sealed validity checks passed first>
```

The revealed content is never written into this log.

## `verdict`

`QROS-VERDICT-RECORD`: the decider (the entry's `decider`), what was reproduced,
and whether an external review was called.

```yaml
verdict:
  subject_ref:      <research line or claim>
  research_status:  confirmed | supported | not_promoted | falsified | active |
                    archived | experimental | unresolved
  disposition:      RUN_TO_VERDICT | CLOSED_PRE_OUTCOME | PARKED_PRE_OUTCOME |
                    NOT_STANDALONE
  verdict_rule_ref: <PREREG_ID §verdict_rule>
  rule_applied:     <order of the sealed rule row that fired | NOT_APPLICABLE>
  # unresolved_reason: <required when rule_applied is NOT_APPLICABLE>
  reproduced:                             # at least one REPRODUCED item
    - what:           <reproduce command run at revision <REV>>
      evidence_class: REPRODUCED | REASONED | SELF-REPORTED
      evidence_ref:   <path or commit>
    - what:           <headline number recomputed from committed outputs>
      evidence_class: REPRODUCED
    - what:           <sealed validity checks ran and passed before the primary was read>
      evidence_class: REPRODUCED
  external_review:
    called:     true | false
    # reviewer:   <concrete party>        # required when called
    # outcome:    PASS | HOLD
    # record_ref: <where the review was persisted on receipt>
```

No departure from the sealed rule after an outcome is seen. Where the rule cannot
be applied the status is `unresolved` and the reason is recorded
(`QROS-VERDICT-NO-DEPARTURE`). A PASS that reproduced nothing is not acceptance
(`QROS-ACCEPT-REPRODUCTION-FIRST`).

## `disposition`

For a line closed or parked before any outcome, or declared not standalone.

```yaml
disposition:
  subject_ref:     <line or candidate>
  disposition:     CLOSED_PRE_OUTCOME | PARKED_PRE_OUTCOME | NOT_STANDALONE | RUN_TO_VERDICT
  research_status: <optional; one of the eight>
  reason:          <why>
```

## `methodology_change`

Every change made after seal carries exactly one label, recorded with its
evidence **before** the change is applied. Where the sealed rule is ambiguous or
absent, the change is a `METHODOLOGY_CHANGE`, not a fix.

```yaml
change:
  change_label:      IMPLEMENTATION_FIX | DATA_FIX | ANALYSIS_EXTENSION |
                     METHODOLOGY_CHANGE | HYPOTHESIS_CHANGE
  what_changed:      <the change>
  sealed_clause_ref: <the sealed clause a fix restores>
  recorded_before_apply: true
  prior_seal_ref:    <for METHODOLOGY_CHANGE / HYPOTHESIS_CHANGE>
  new_seal_ref:      <for METHODOLOGY_CHANGE / HYPOTHESIS_CHANGE>
  prior_evidence_disposition: <stays historical | does not transfer>
  defect_impact:                          # QROS-CHANGE-DEFECT-IMPACT, when a
    defect:               <the defect>    # confirmed defect affects research
    affected:             <what>
    unaffected:           <what is demonstrably unaffected>
    unknown:              <what is unknown>
    recomputation:        <needed or not, and why>
    evidence_restriction: <any restriction on use of the evidence>
    not_recomputed:       <runs not recomputed>
```

No change reruns, amends or alters the trial count automatically. A new seal
never restores a sample's freshness (`QROS-REUSE-NEW-SEAL-NO-REFRESH`).

## `delegate_decision` / `owner_decision`

Any other decision by that role: an S0 `RESEARCH | PARK | REJECT`, a local merge,
a scope change, a delegated decision the `OWNER` takes back. Name the `gate`
where one applies. An `OWNER` decision overrides a `DELEGATE` decision.

## `correction`

Corrects the record, never the history. The corrected entry stays exactly as
written.

```yaml
corrects_entry: E-<M>
what_was_wrong: <the specific error in E-<M> as recorded>
correct_record: <what the record should be understood to say>
```

A correction does not reverse a decision or change a verdict. Reversing a
decision is a new decision entry that cites the one it reverses.

---

## Index

Generated from the entries above, never hand-maintained
(`QROS-RECORD-DERIVED-NOT-COPIED`).

| id | utc | type | decider | decision |
|---|---|---|---|---|
| `E-<N>` | `<ISO8601_UTC>` | `<type>` | `<ROLE> / <PARTY>` | `<one line>` |
