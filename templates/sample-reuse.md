# Sample Reuse Declaration — `<DECLARATION_ID>`

> This template operationalizes `QROS-REUSE-EXPOSURE-VS-TRIALS` ·
> `QROS-REUSE-DECLARE-BEFORE-USE` · `QROS-REUSE-NEW-SEAL-NO-REFRESH` ·
> `QROS-REUSE-NEGATIVE-CONSUMES` · `QROS-AXIS-OUTCOME-EXPOSURE` ·
> `QROS-AXIS-TRIAL-ACCOUNTING`.
>
> `../SPEC.md` is the sole normative source. Validated by
> `../schemas/sample-reuse-declaration.schema.json`.

**Completed before the reuse happens**, not after. A declaration written after
the fact records what occurred; it does not discharge the obligation, and the
`declared_before_use` field says which of the two this is.

One declaration per reuse. This is not a sample registry — the durable record of
what a sample has absorbed lives in the project's trial accounting, and this
document cites it rather than restating it.

---

## Declaration

```yaml
declaration_id: REUSE_SYNTHETIC_001
project_id: PROJECT_SYNTHETIC_001
work_item: WORKITEM_SYNTHETIC_002
declared_by: ROLE_BINDING_BUILDER
declared_at: "2000-01-01T00:00:00Z"
declared_before_use: true          # false ⇒ this is a retrospective record, and
                                   # the obligation was not met; say so plainly

# --- which sample -------------------------------------------------------
sample:
  identity: SAMPLE_SYNTHETIC_A
  class: synthetic-panel           # a class, never a vendor or product name
  definition: >
    What this sample is, in terms sufficient to tell it apart from a
    neighbouring one: coverage, period, inclusion rules.
  reuse_class: reused-dependent    # the project's declared class, or UNKNOWN
  evidence_ceiling: supported      # highest status any claim on this sample may reach
                                   # (QROS-REUSE-DECLARE-BEFORE-USE)

# --- what it has already absorbed ---------------------------------------
# QROS-REUSE-EXPOSURE-VS-TRIALS: these two records answer different questions
# and neither is derived from the other.
prior_uses:
  - use_ref: WORKITEM_SYNTHETIC_001
    what_was_done: >
      What that earlier work did with this sample.
    outcome_recorded: true         # whether a result was recorded, NOT what it was
    negative_result: false         # a negative result consumes freedom too
                                   # (QROS-REUSE-NEGATIVE-CONSUMES)

prior_exposure:
  - party: ROLE_BINDING_BUILDER
    target: SYNTH_METRIC_A
    level: TARGET_METRIC           # NONE | AGGREGATE | TARGET_METRIC | UNKNOWN
    as_of: "2000-01-01T00:00:00Z"

prior_trial_accounting:
  accounting_reference: ACCOUNTING_SYNTHETIC_001
  prior_effective_attempts: 1
  constraints_carried:
    - must_not_be_retested_for: SYNTH_METRIC_A
      basis: >
        Where this constraint came from.

# --- what is now proposed -----------------------------------------------
proposed_use:
  summary: >
    What this work will do with the sample.
  lane: MEASUREMENT                # EXPLORATORY | MEASUREMENT | FULL
  claim_intended: >
    The claim this reuse is meant to support. The justification below must be
    good enough for THIS claim, not in general.

# --- the boundary: what will and will not be computed --------------------
# The scope of an examination determines how much selection freedom it
# consumes. Both lists are required; an empty `will_not_compute` is a claim
# that nothing was withheld, which is rarely true and should be checked.
will_compute:
  - Statistic or comparison that this work WILL compute.
will_not_compute:
  - Statistic or comparison that this work WILL NOT compute.
  - A further withheld comparison.

# --- why this reuse is acceptable ---------------------------------------
justification: >
  Why the proposed use is valid for the intended claim given what the sample
  has already absorbed. A new preregistration does not restore freshness
  (QROS-REUSE-NEW-SEAL-NO-REFRESH), so "we sealed a new contract" is not a
  justification on its own.

# --- consequences, recorded in advance -----------------------------------
resulting_exposure:
  - party: ROLE_BINDING_BUILDER
    target: SYNTH_METRIC_A
    level: TARGET_METRIC
    note: >
      What this party will know afterwards that it does not know now.

resulting_trial_accounting:
  effective_attempts_added: 0
  basis: >
    Why the project's declared accounting method yields this number. QROS
    prescribes no counting formula; cite the method, do not invent one.
  accounting_reference: ACCOUNTING_SYNTHETIC_001

# --- authority ------------------------------------------------------------
# Required where the reuse is itself gated — e.g. it needs data access beyond
# a grant or a run authorization (QROS-GATE-DELEGATED), or touches a retained
# gate (QROS-GATE-OWNER-RETAINED).
authority:
  required: false
  # decision_ref: <decision-log entry authorising this, when required:true>
```

---

## Notes on completing this

| Field | What acceptance will check |
|---|---|
| `declared_before_use` | `true`, with `declared_at` preceding the work |
| `prior_uses` | every prior use, including those that produced nothing publishable |
| `prior_exposure` | one row per party and target — exposure is not a global property |
| `will_not_compute` | genuine withholding, not a formality |
| `justification` | an argument about *this* claim, not a general appeal to good practice |
| `resulting_trial_accounting.basis` | the project's declared method applied, not a new rule invented here |

Recording `outcome_recorded: true` states that a result exists. It never states
what the result was — that belongs in the durable record the accounting
reference points to.
