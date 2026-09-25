# Blockers and Backlog — `<PROJECT_ID>`

> This template operationalizes `QROS-STATE-BLOCKER-ARTIFACT` ·
> `QROS-BLOCKER-SINGLE-SET` · `QROS-BLOCKER-ADMISSION` · `QROS-BLOCKER-CLASSES` ·
> `QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION` ·
> `QROS-BLOCKER-CLOSED-STAYS-CLOSED` · `QROS-BLOCKER-EXPIRY` ·
> `QROS-COMPLETION-NO-SPECULATIVE-BLOCKER`.
>
> `../SPEC.md` is the sole normative source. Each row validates against
> `../schemas/backlog-row.schema.json`.

**This file is the project's only blocker authority** (`QROS-BLOCKER-SINGLE-SET`).
Other lists may exist for planning; none of them blocks.

Rows are **closed, never deleted**. A closed row keeps the evidence that closed
it (§3).

```yaml
updated_at:  <ISO8601_UTC>
updated_by:  <ROLE_BINDING>
open_blockers: <count>          # generated from the rows below, never
open_backlog:  <count>          # hand-copied (QROS-RECORD-DERIVED-NOT-COPIED)
```

---

## 1. Current blockers

A row enters this section only if it names a threat **and** a concrete failure
path on the current or next stage (`QROS-BLOCKER-ADMISSION`). A `SELF-REPORTED`
statement never blocks on its own (`QROS-REVIEW-SELF-REPORTED-NOT-BLOCKING`).

| id | class | threat | threat class | concrete failure path | stage affected | evidence for the row | evidence required to clear | opened by | opened at | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `B-<N>` | `<CLASS>` | `<the named threat>` | `<THREAT_CLASS>` / — | `<how it produces a wrong, irreproducible, or unsafe outcome>` | `CURRENT` / `NEXT` | `REPRODUCED` / `REASONED` + reference | `<what would close it>` | `<ROLE> / <party>` | `<ISO8601_UTC>` | `OPEN` |

```
class         CURRENT_PATH_BLOCKER · ARCHITECTURE_LEVEL_BLOCKER
threat class  optional tag from QROS-THREAT-VOCABULARY:
              SELF_CERTIFICATION · OUTCOME_LEAKAGE · HINDSIGHT_SELECTION ·
              SAME_SAMPLE_RETUNING · SILENT_REVIVAL · ONE_SHOT_REUSE ·
              STALE_CURRENT_STATE · DERIVED_FACT_DRIFT ·
              PRESENCE_ONLY_VALIDATION · UNPERSISTED_REVIEW ·
              PROSE_ONLY_DATA_RULES · INVALID_MEASUREMENT ·
              UNRESOLVABLE_DESIGN · GOVERNANCE_COST_EXCEEDING_RISK
```

Only these two classes hold a project. An `ARCHITECTURE_LEVEL_BLOCKER` goes to
the `DELEGATE`, which designs on request (`QROS-ROLE-DELEGATE`).

Every row needs a defined exit: an empty *evidence required to clear* column
means the row cannot be closed and is not admissible.

### 1.1 Candidates examined and not admitted

Recording rejections demonstrates the admission test is exercised rather than
assumed. Recommended, not required.

| candidate | why not admitted | where it went |
|---|---|---|
| `<ITEM>` | `<no current-path failure path / no named threat / speculative>` | §2 row `<ID>` / dropped |

Not admissible: a cleaner design is imaginable; a stronger general safeguard
could exist; further review would add confidence; a document is inconsistent; a
defect on a path this project will not take; a guard protecting a guard
(`QROS-COMPLETION-NO-SPECULATIVE-BLOCKER`).

### 1.2 Gates left unsatisfied by a transport or procedural failure

These are **not** blockers and record **nothing** about the work
(`QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION`). They are tracked here only so an
unsatisfied gate is not mistaken for a satisfied one.

| id | class | gate left unsatisfied | what failed | round consumed | remedy |
|---|---|---|---|---|---|
| `T-<N>` | `<CLASS>` | `<gate or acceptance ref>` | `<bundle digest mismatch / truncated transfer / tool failure / blind party exposed / wrong party accepted>` | `NO` | `<repeat the step correctly>` |

```
class  TRANSPORT_OR_PACKAGING_ISSUE · REVIEW_SEAT_OR_PROCEDURAL_FAILURE
```

`round consumed` is always `NO` here.

## 2. Non-blocking backlog

A different row shape. These rows do **not** carry a threat or a failure path,
and MUST NOT be given fabricated ones to fit §1. Findings classed `NON-BLOCKING`,
`OPTIONAL` or `UNRELATED` land here (`QROS-REVIEW-BLOCKING-REQUIREMENTS`).

| id | item | kind | source | disposition | notes |
|---|---|---|---|---|---|
| `N-<N>` | `<what it is>` | `<engineering / documentation / ergonomics / hardening / deferred-decision>` | `<acceptance finding E-<N> / observation / OWNER or DELEGATE request>` | `<the stage that needs it, or "unscheduled">` | `<free text>` |

`kind` is free vocabulary local to the project. It carries no QROS semantics and
is not the threat vocabulary.

Work proceeds with these outstanding (`QROS-COMPLETION-PROGRESSION`).

## 3. Closed rows

Closed rows stay here with the evidence that closed them. Reopening requires
new evidence of a named threat with a failure path on the current or next stage
(`QROS-BLOCKER-CLOSED-STAYS-CLOSED`).

| id | original section | summary | closed at | closed by | closing evidence | reopened? |
|---|---|---|---|---|---|---|
| `<ID>` | §1 / §1.2 / §2 | `<one line>` | `<ISO8601_UTC>` | `<ROLE_BINDING>` | `<reference>` | `NO` / `YES — <new id>` |

## 4. Expiry

`QROS-BLOCKER-EXPIRY`. A §2 row that no stage needs expires: it moves to §3 with
closing evidence `expired — no stage needs it`. A row is never promoted to §1
merely because it has aged.

A party may downgrade to §2 only a row **it opened itself** whose failure path
was never `REPRODUCED`. Rows opened by another party, and rows whose failure
path was reproduced, leave §1 only by clearing evidence or by decision of the
gate holder (`DELEGATE`, or `OWNER`), recorded in the decision log.
