# Research State — `PROJECT_SYNTHETIC_001`

**Outcome-clean.** This page is readable by a party under `OUTCOME_BLIND`
obligations. It records where the work stands, never what the work found.
Rewritten in place as the study advanced; this is its final revision.

```yaml
updated_at:   "2000-01-06T16:00:00Z"
updated_by:   ROLE_BINDING_MAIN_AGENT
```

---

## 0. Who is reading this

- **A party required to stay blind:** safe to read in full. Take every artifact
  you need from the dispatcher's evidence surface, not from this directory.
- **Everyone else:** blockers are in `12-backlog.yaml`; decisions and verdicts
  are in `13-decision-log.yaml`.

## 1. Where the work stands

| | |
|---|---|
| Work item | `STUDY_SYNTHETIC_001` |
| Lane | `FULL` |
| Current stage | `RECORD` |
| Preregistration | `SEALED` — `PREREG_SYNTHETIC_001`, digest `bb8f114e…` |
| Last completed unit | round 2 independent verification, returned |
| Next unit | none — the preregistered question has been answered and the study is closed |

## 2. What question is being worked on

Stated as a question. No answer, paraphrased or hinted, appears on this page.

> See `01-preregistration.yaml` §`research_question`.

## 3. Authority to continue

| | |
|---|---|
| Who may advance this work | nobody — the study is closed under the stop rule |
| Awaiting an `OWNER` act? | `NO` |
| Open review dispatches | `NONE` |

## 4. Execution authorization

Status only. Any authorising entry lives in `13-decision-log.yaml`.

| | |
|---|---|
| Real-data execution | `NOT_AUTHORIZED` — not applicable; this study reads only deterministically generated synthetic data and touches no real data |
| Authorizing entry | `NONE` |
| Reveal status | `REVEALED — see E-3` |

`REVEALED` records only that a reveal occurred. The revealed content stays in
its own durable record and is never restated here.

## 5. Blockers and deferred work

| | |
|---|---|
| Open blockers | `0` — rows in `12-backlog.yaml` §1 |
| Non-blocking backlog | `2` — rows in `12-backlog.yaml` §2 |
| Closed blockers | `1` — retained with closing evidence |

The study proceeded to completion with both backlog rows open
(`QROS-COMPLETION-PROGRESSION`).

## 6. Evidence required to finish this stage

| # | Required evidence | Status |
|---|---|---|
| 1 | Sealed preregistration | `PRODUCED` |
| 2 | Deterministic mechanical checks run before review | `PRODUCED` |
| 3 | Independent recomputation of the sealed statistic | `VERIFIED` |
| 4 | Blocking findings closed with clearing evidence | `VERIFIED` |
| 5 | Sealed decision table applied to the revealed statistic | `PRODUCED` |
| 6 | Disposition recorded by the `OWNER` | `PRODUCED` |

Status tokens describe whether the evidence exists, never what it shows.

## 7. Stage exit condition

> The sealed decision table has been applied to an independently verified
> statistic in the preregistered order, the disposition is a row in the
> decision log, and no blocker is open.

Met.

## 8. Next legal action

> None under this preregistration. `QROS-COMPLETION-STOP-RULE` applies: the
> preregistered question has been answered, so no further parameters, windows,
> horizons or variants may be examined under this contract. A new question
> would require its own preregistration, with any sample reuse declared in
> advance.

## 9. Sample reuse

Not applicable to this study. `SAMPLE_SYNTHETIC_DEVELOPMENT` was generated for
this preregistration and carried no prior use; `SAMPLE_SYNTHETIC_RESERVED` was
never opened. No reuse occurred, so no declaration was made — the template is
not exercised here rather than exercised with invented content.

---

### Do not record on this page

Verdicts · statistical results · effect sizes · target-metric values · revealed
conclusions · exposure counts · decision-rule outcomes.
