# Research State — `<PROJECT_ID>`

> This template operationalizes `QROS-STATE-CURRENT-ARTIFACT` and
> `QROS-STATE-OUTCOME-CLEAN`. `../SPEC.md` is the sole normative source.

**Outcome-clean.** This page is readable by a party under `OUTCOME_BLIND`
obligations. It records *where the work stands*, never *what the work found*.
Rewritten in place; its history lives in version control
(`QROS-RECORD-CURRENT-VS-HISTORICAL`).

```yaml
updated_at:   <ISO8601_UTC>
updated_by:   <ROLE_BINDING>
```

---

## 0. Who is reading this

- **A party required to stay blind:** this page is safe to read in full. Take
  every artifact you need from the dispatcher's evidence surface, not from this
  repository.
- **Everyone else:** blockers are in `backlog.md` §1; decisions and verdicts are
  in `decision-log.md`.

## 1. Where the work stands

| | |
|---|---|
| Work item | `<WORK_ITEM_ID>` |
| Lane | `EXPLORATORY` / `MEASUREMENT` / `FULL` |
| Current stage | `<one of QROS-LIFECYCLE-STAGES>` |
| Preregistration | `NOT_APPLICABLE` / `DRAFT` / `SEALED` — ref `<PREREG_ID>` |
| Last completed unit | `<UNIT_ID>` |
| Next unit | `<UNIT_ID>` / `NOT_STARTED` / `BLOCKED` |

## 2. What question is being worked on

State the question **as a question**. Do not state, paraphrase, or hint at any
answer.

```
<QUESTION_REF or one-line neutral restatement>
```

Where the full text is sealed, cite `<PREREG_ID>` rather than reproducing it.

## 3. Authority to continue

| | |
|---|---|
| Who may advance this work | `<ROLE_BINDING>` |
| Awaiting an `OWNER` act? | `NO` / `YES — <gate identifier>` |
| Open review dispatches | `<REVIEW_ID list>` / `NONE` |

## 4. Execution authorization

Status only. The authorising entry lives in `decision-log.md`
(`QROS-OWNER-REAL-RUN`).

| | |
|---|---|
| Real-data execution | `NOT_AUTHORIZED` / `EXECUTION_AUTHORIZED` / `AUTHORIZATION_USED` / `AUTHORIZATION_REVOKED` |
| Authorizing entry | `<ENTRY_ID>` / `NONE` |
| Reveal status | `NOT_REVEALED` / `AWAITING_OWNER_ACTION` / `REVEALED — see <ENTRY_ID>` |

`REVEALED` records only that a reveal occurred. The revealed content stays in
its own durable record and is never restated here.

## 5. Blockers and deferred work

| | |
|---|---|
| Open blockers | `<count>` — rows in `backlog.md` §1 |
| Non-blocking backlog | `<count>` — rows in `backlog.md` §2 |

Counts and references only. A project proceeds with non-blocking backlog
outstanding (`QROS-COMPLETION-PROGRESSION`).

## 6. Evidence still required to finish this stage

| # | Required evidence | Status |
|---|---|---|
| 1 | `<what must exist>` | `NOT_STARTED` / `IN_PROGRESS` / `PRODUCED` / `VERIFIED` |

Status tokens describe *whether the evidence exists*, never what it shows.

## 7. Stage exit condition

```
<what must be true for this stage to terminate>
```

## 8. Next legal action

```
<the single next action, and who takes it>
```

---

### Do not record on this page

Verdicts · statistical results · effect sizes · target-metric values · revealed
conclusions · exposure counts · decision-rule outcomes · any value a decision
rule reads.

Each belongs in its own durable record; cite the record by identifier. A page
that carries any of them cannot be read by a blind party, which is the one
audience this page exists to serve.
