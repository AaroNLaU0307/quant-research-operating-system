# Blockers and Backlog — `<PROJECT_ID>`

> This template operationalizes `QROS-BLOCKER-SINGLE-SET` ·
> `QROS-BLOCKER-ADMISSION` · `QROS-BLOCKER-CLASSES` ·
> `QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION` ·
> `QROS-BLOCKER-CLOSED-STAYS-CLOSED` · `QROS-BLOCKER-EXPIRY` ·
> `QROS-COMPLETION-NO-SPECULATIVE-BLOCKER`.
>
> `../SPEC.md` is the sole normative source.

**This file is the project's only blocker authority** (`QROS-BLOCKER-SINGLE-SET`).
Other lists may exist for planning; none of them blocks.

Rows are **closed, never deleted**. A closed row keeps the evidence that closed
it (§3).

```yaml
updated_at:  <ISO8601_UTC>
updated_by:  <ROLE_BINDING>
open_blockers: <count>
open_backlog:  <count>
```

---

## 1. Current blockers

A row enters this section only if it states **exactly one** threat class **and**
a concrete failure path on the current or next stage (`QROS-BLOCKER-ADMISSION`).

| id | class | threat | concrete failure path | stage affected | evidence for the row | evidence required to clear | opened by | opened at | expires | status |
|---|---|---|---|---|---|---|---|---|---|---|
| `B-<N>` | `<CLASS>` | `<THREAT>` | `<how it produces a wrong, irreproducible, or unsafe outcome>` | `CURRENT` / `NEXT` | `REPRODUCED` / `REASONED` + reference | `<what would close it>` | `<ROLE_BINDING>` | `<ISO8601_UTC>` | `<ISO8601_UTC>` / `NONE` | `OPEN` |

```
class    CURRENT_PATH_BLOCKER · ARCHITECTURE_LEVEL_BLOCKER
threat   RESEARCH_CORRECTNESS · REPRODUCIBILITY · DATA_IDENTITY_OR_PROVENANCE ·
         INDEPENDENCE_OR_BLINDNESS · CONSEQUENTIAL_EXECUTION_SAFETY ·
         METHODOLOGY_OR_SCOPE_INTEGRITY
```

Only these two classes hold a project. `ARCHITECTURE_LEVEL_BLOCKER` is the only
class that may escalate to `ARCHITECTURE_REVIEWER`
(`QROS-ROLE-ARCHITECTURE-ESCALATION-BOUNDED`).

Every row needs a defined exit: an empty *evidence required to clear* column
means the row cannot be closed and is not admissible.

### 1.1 Candidates examined and not admitted

Recording rejections demonstrates the admission test is exercised rather than
assumed. Recommended, not required.

| candidate | why not admitted | where it went |
|---|---|---|
| `<ITEM>` | `<no current-path failure path / no single threat / speculative>` | §2 row `<ID>` / dropped |

Not admissible: a cleaner design is imaginable; a stronger general safeguard
could exist; further review would add confidence; a document is inconsistent; a
defect on a path this project will not take; a guard protecting a guard
(`QROS-COMPLETION-NO-SPECULATIVE-BLOCKER`).

### 1.2 Gates left unsatisfied by a transport or seating failure

These are **not** blockers and record **nothing** about the work
(`QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION`). They are tracked here only so an
unsatisfied gate is not mistaken for a satisfied one.

| id | class | gate left unsatisfied | what failed in the delivery or seating | round consumed | remedy |
|---|---|---|---|---|---|
| `T-<N>` | `<CLASS>` | `<review or gate ref>` | `<manifest mismatch / insufficient surface / ineligible reviewer / exposure before freeze>` | `NO` | re-dispatch under a new `review_id` |

```
class  TRANSPORT_OR_PACKAGING_FAILURE · REVIEWER_ELIGIBILITY_OR_PROCEDURAL_FAILURE
```

`round consumed` is always `NO` here.

## 2. Non-blocking backlog

A different row shape. These rows do **not** carry a threat class or a failure
path, and MUST NOT be given fabricated ones to fit §1.

| id | item | kind | source | disposition | notes |
|---|---|---|---|---|---|
| `N-<N>` | `<what it is>` | `<engineering / documentation / ergonomics / hardening / deferred-decision>` | `<review REVIEW_ID / observation / OWNER request>` | `<when it will be picked up, or "unscheduled">` | `<free text>` |

`kind` is free vocabulary local to the project. It carries no QROS semantics and
is not the threat vocabulary.

Work proceeds with these outstanding (`QROS-COMPLETION-PROGRESSION`).

## 3. Closed rows

Closed rows stay here with the evidence that closed them. Reopening requires
new, concrete evidence of a failure on the current path in exactly one threat
class (`QROS-BLOCKER-CLOSED-STAYS-CLOSED`).

| id | original section | summary | closed at | closed by | closing evidence | reopened? |
|---|---|---|---|---|---|---|
| `<ID>` | §1 / §1.2 / §2 | `<one line>` | `<ISO8601_UTC>` | `<ROLE_BINDING>` | `<reference>` | `NO` / `YES — <new id>` |

## 4. Expiry handling

`QROS-BLOCKER-EXPIRY`. At expiry the only permitted outcomes are:

| Outcome | Condition |
|---|---|
| Cleared | the required evidence now exists |
| Extended once | with a written reason, recorded below |
| `OWNER` decision | the row goes to the `OWNER` |

| id | expired at | outcome | reason | recorded by |
|---|---|---|---|---|
| `<ID>` | `<ISO8601_UTC>` | `CLEARED` / `EXTENDED` / `OWNER_DECISION` | `<reason>` | `<ROLE_BINDING>` |

A party may downgrade to §2 only a row **it opened itself** whose failure path
was never `REPRODUCED`. Reviewer-opened rows, and rows whose failure path was
reproduced, leave §1 only by clearing evidence or by `OWNER` decision.
