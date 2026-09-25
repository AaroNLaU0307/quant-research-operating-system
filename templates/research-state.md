# Research State — `<PROJECT_ID>`

> Operationalizes `QROS-STATE-CURRENT-ARTIFACT` · `QROS-STATE-NOT-BLIND` ·
> `QROS-AUTHORITY-STATE-NOT-AUTHORITY` · `QROS-RECORD-CURRENT-VS-HISTORICAL` ·
> `QROS-RECORD-DERIVED-NOT-COPIED`. `../SPEC.md` is the sole normative source.

**Not outcome-blind.** This page may carry outcomes; a party that must stay blind
receives a bundle, never this page (`QROS-STATE-NOT-BLIND`). It records state,
never authority. Rewritten at every checkpoint, never appended; superseded facts
are deleted, not annotated. One screen.

| | |
|---|---|
| Updated | `<ISO8601_UTC>` · revision `<REV>` · by `<BUILDER party>` |
| Question | `<one line>` — sealed text in `<PREREG_ID>` |
| Stage | `S0_FRAME` / `S1_DESIGN_SEAL` / `S2_BUILD` / `S3_RUN` / `S4_VERDICT` / `STOP` |
| Reproduce | `<the one reproduce command>` (`QROS-RECORD-REPRODUCE-COMMAND`) |

## Active lines

| line | lane | stage | seal | status |
|---|---|---|---|---|
| `<LINE_ID>` | `EXPLORATORY` / `MEASUREMENT` / `FULL` | `<stage>` | `<seal ref>` / `DRAFT` / `NONE` | `<one line>` |

## Live grants

Pointers only; each grant lives in its decision-log entry.

| grant | mode | covers | state |
|---|---|---|---|
| `E-<N>` | `ONE_SHOT` / `STANDING` | `<line or run>` | `LIVE` / `CONSUMED — E-<M>` |

## Live obligations

| due | obligation | owed by | source |
|---|---|---|---|
| `<YYYY-MM-DD>` | `<what must happen>` | `<ROLE / party>` | `E-<N>` / `<path>` |

## Outcome exposure

| party | target | level | since |
|---|---|---|---|
| `<party>` | `<outcome>` | `NONE` / `AGGREGATE` / `TARGET_METRIC` / `UNKNOWN` | `E-<N>` |

Monotonic; no row means `UNKNOWN`, never `NONE` (`QROS-EXPOSURE-MONOTONIC`).

## Open blockers

`B-<N>`: `<one line>` / `NONE`. Rows live in `backlog.md`; this is a pointer.

## Next decision

| decision | holder | needs |
|---|---|---|
| `<what must be decided>` | `OWNER` / `DELEGATE` / `BUILDER` — `<party>` | `<evidence or checkpoint ref>` |

## Closed lines

One row and a pointer each.

| line | outcome | record |
|---|---|---|
| `<LINE_ID>` | `<research_status>` · `<disposition>` | `E-<N>` |

---

Counts, statuses and liveness flags above are generated from, or point to, their
source; they are never hand-copied, and never override it
(`QROS-RECORD-DERIVED-NOT-COPIED`). An inactive project needs no current-state
artifact.
