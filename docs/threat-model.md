# Threat model

What QROS defends against, how, and where the boundary sits.

Explanatory. [SPEC.md](../SPEC.md) (v2.0.0) is the only normative source.
Identifiers are pointers into it.

---

## The threat vocabulary

`QROS-THREAT-VOCABULARY` names fourteen failure modes and is **closed at each
version**. Each maps to the rules that address it:

| Threat | Addressed by |
|---|---|
| self-certification | `QROS-ROLE-SELF-CERTIFICATION`, `QROS-ROLE-SUBAGENT-NOT-INDEPENDENT`, `QROS-GATE-NO-SELF-AUTHORIZATION`, `QROS-ACCEPT-REPRODUCTION-FIRST` |
| outcome leakage | `QROS-PREREG-SEAL-BEFORE-EXPOSURE`, `QROS-BLIND-ON-DEMAND`, `QROS-BLIND-REPO-NOT-BLIND`, `QROS-STATE-NOT-BLIND`, `QROS-BLIND-EXPOSURE-RESPONSE` |
| hindsight selection | `QROS-PREREG-VERDICT-RULE`, `QROS-VERDICT-NO-DEPARTURE`, `QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE` |
| same-sample retuning | `QROS-VERDICT-NO-RESCUE`, `QROS-COMPLETION-STOP-RULE`, `QROS-CHANGE-FIX-NOT-METHODOLOGY`, `QROS-REUSE-NEW-SEAL-NO-REFRESH` |
| silent revival | `QROS-S0-ANTI-REVIVAL`, `QROS-LIFECYCLE-TERMINATES`, `QROS-BLOCKER-CLOSED-STAYS-CLOSED` |
| one-shot reuse | `QROS-REUSE-LOCKBOX`, `QROS-RUN-ONE-SHOT-WRITE-AHEAD`, `QROS-RUN-FAIL-CLOSED` |
| stale current state | `QROS-STATE-CURRENT-ARTIFACT`, `QROS-RECORD-CHECKPOINT`, `QROS-RECORD-CURRENT-VS-HISTORICAL` |
| derived-fact drift | `QROS-RECORD-DERIVED-NOT-COPIED`, `QROS-RECORD-REPRODUCE-COMMAND` |
| presence-only validation | `QROS-RECORD-PRESENT-AND-ABSENT`, `QROS-CHECK-NON-VACUOUS` |
| unpersisted review | `QROS-REVIEW-PERSISTED`, `QROS-RECORD-DURABLE-NOT-TRANSCRIPT` |
| prose-only data rules | `QROS-PREREG-ENFORCED-DATA-RULES` |
| invalid measurement | `QROS-PREREG-VALIDITY-CHECKS`, `QROS-S0-POINT-IN-TIME-FIRST` |
| unresolvable design | `QROS-PREREG-RESOLVABILITY`, `QROS-PREREG-KILL-REACHABILITY`, `QROS-PREREG-METRIC-SCALE-CONSISTENCY` |
| governance cost exceeding risk | `QROS-COST-BUDGET`, `QROS-REVIEW-NOT-ROUTINE`, `QROS-REVIEW-ROUND-BUDGET`, `QROS-COMPLETION-PROGRESSION` |

Across all of them, exposure is monotonic (`QROS-EXPOSURE-MONOTONIC`): a
missing record means `UNKNOWN`, never `NONE`.

### Why the vocabulary stays closed

An extensible vocabulary defeats the filter it belongs to: every project has a
local reason to add an entry, and after a few of those everything qualifies. A
new version may change the list; a project may not (`QROS-CONFIG-TIGHTEN-ONLY`).
The same reasoning closes the retained-gate list (`QROS-GATE-OWNER-RETAINED`): a
configurable safeguard gets configured away when it becomes inconvenient.

---

## Blocker admission

**A concern is not automatically a blocker.** `QROS-BLOCKER-ADMISSION` admits
an item only with a **named threat** and a **concrete failure path** on the
**current or next** stage. Each row carries exactly one class
(`QROS-BLOCKER-CLASSES`) and should state the evidence that would clear it.

A statement that something is undesirable is not a failure path. Neither is a
statement that something is wrong — a failure path says *what breaks next*.

**Not admissible** (`QROS-COMPLETION-NO-SPECULATIVE-BLOCKER`): a cleaner design
is imaginable; further review would add confidence; a defect exists on a path
this project will not take.

A finding also carries an evidence class (`QROS-REVIEW-EVIDENCE-CLASSES`).
`SELF-REPORTED` never passes and never blocks on its own
(`QROS-REVIEW-SELF-REPORTED-NOT-BLOCKING`): it adds no independent information.
`REPRODUCED` and `REASONED` may both block; requiring execution before a design
defect could be raised would exclude precisely the defects execution cannot
reveal.

### Worked illustration (synthetic)

From the worked example, a finding that **was** admitted:

> **Threat:** outcome leakage (look-ahead).
> **Failure path:** the signal dated *t* contains the return of *t+1*; the
> leaked value feeds the sealed decision table; rule 2 fires; the candidate is
> recorded as supported; the reserved sample is spent on an artefact.
> **Class:** real current-path blocker. **Evidence class:** `REPRODUCED`.

And an observation that was **not** admitted and went to backlog:

> The mechanical check set covers shape, nullity, alignment and determinism
> only; none could distinguish a leaked signal from a correct one.

True, useful, and not a blocker: it names no failure path on the current or next
stage. It was recorded, and the study proceeded. Under v2 the gap is closed
before seal (`QROS-PREREG-VALIDITY-CHECKS`, `QROS-PREREG-ENFORCED-DATA-RULES`).

---

## Transport failure is not implementation failure

`QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION`. Acceptance can fail to happen
validly: a bundle's digests do not recompute (the receiver must stop,
`QROS-BLIND-ON-DEMAND`), a tool crashes, the reproduce command cannot run.

Such a failure **leaves the gate unsatisfied**, **establishes nothing about the
work**, and **consumes no review round**. Repair the delivery and try again.
Recording it as a defect enters an undemonstrated defect into the record and
spends budget on something no code change addresses.

An acceptance that never became valid returned **no outcome** — neither `PASS`
nor `HOLD` (`QROS-REVIEW-VERDICTS`). Research verdicts are one separate
vocabulary (`QROS-VERDICT-VOCABULARY`); a rule that cannot be applied yields
`unresolved`, never a new term.

---

## Closed stays closed

`QROS-BLOCKER-CLOSED-STAYS-CLOSED`. Reopening **requires** new, concrete
evidence of a failure on the current path — not a better approach, another
reviewer's reassurance, or the concern restated more forcefully.

Without this rule a project cannot finish. Any settled question can be reopened
by conviction alone, and the cost is borne by those answering the research
question rather than by the person reopening it.

---

## What QROS does not defend against

Stated plainly, because a threat model that lists only successes is marketing.

- **A wrong prior.** If the hypothesis is misconceived, every rule will be
  followed and the conclusion will still be worthless.
- **Defective input data.** Identity checks detect undisclosed change, not a
  vendor's error, a corrupted source, or a wrong upstream construction.
- **A threat outside the vocabulary.** The closed list has a real cost: a novel
  failure mode has no rule written for it.
- **A determined adversary.** A party willing to falsify a decision entry,
  fabricate a digest or misreport its exposure defeats all of it. QROS raises
  the cost of error and self-deception, not of fraud.
- **Errors no check was designed to catch.** In the worked example only
  independent recomputation surfaced the defect; had nobody recomputed, nothing
  would have noticed.
- **Overfitting as such.** Moving a threshold, reusing a burned sample, and
  searching after the answer become visible. The general problem is not solved.
- **Human judgement.** The smallest effect of interest, whether a hypothesis is
  genuinely distinct, how decisive a negative result is: resolvability makes
  these explicit, but none is mechanisable.

`QROS-PURPOSE-NO-CORRECTNESS-GUARANTEE` states the limit normatively. QROS
confers no certification and claims no regulatory or fiduciary suitability.

---

## Residual risks worth naming

**Reproduction is the load-bearing element.** A `DELEGATE` that reads and
agrees rather than reproduces keeps the paperwork and loses the protection.
Requiring a PASS to list what it reproduced makes that visible, not impossible.
And reproduction shows only that numbers follow from bytes: a leaked or invalid
construction reproduces perfectly, which is why validity checks run before the
primary result is read.

**A same-family `DELEGATE` and `BUILDER` share blind spots.** Separate
sessions of one model family give CONTEXT and AUTHORSHIP independence, not
MODEL_DIVERSITY (`QROS-ROLE-SAME-FAMILY-LIMIT`, `QROS-INDEP-FOUR-KINDS`). A
misread method, a plausible but wrong construction, or a shared reasoning habit
can pass both, since the `DELEGATE`'s `REASONED` judgement comes from the same
distribution as the `BUILDER`'s. Reproduction and a sealed, computed verdict
rule (`QROS-VERDICT-RULE-COMPUTED`) push most of that risk into the design —
estimand, rule, validity checks — exactly where a same-family `DELEGATE` is
least independent, above all where it contributed the design
(`QROS-ROLE-SELF-CERTIFICATION`). QROS does not close this gap; the `OWNER` may
bring in an external reviewer for a consequential verdict.

**Messages carry authority imperfectly.** `QROS-GATE-NO-RELAY` keeps retained
gates out of reach of relayed messages. Delegated decisions do travel as
messages; recording them verbatim with their sender
(`QROS-RECORD-DECISION-LOG-APPEND-ONLY`) makes a forged one auditable, not
impossible.

**Blindness depends on how the bundle is built.** A bundle assembled carelessly,
or a "bundle" that is a directory holding more than intended, is not blind. The
digests make that checkable only if the receiver actually recomputes them.

**Self-declared conformance is self-declared.** Nothing verifies that a project
claiming QROS follows it (`QROS-CONFORMANCE-SELF-DECLARED`).
`QROS-CONFORMANCE-PUBLICATION-ASSURANCE` is the one place a claim must be
checkable rather than asserted, and it covers disclosure, not research quality.
