# Why QROS looks like this

Explanatory. [SPEC.md](../SPEC.md) (v2.0.0) is the only normative source; where
this document and the specification differ, the specification governs.
Identifiers like `QROS-BLIND-ON-DEMAND` are pointers into it, not restatements.

Every rule below exists because of a failure mode, not because it seemed
principled. The failure modes are described generically; the illustrations are
synthetic.

---

## The two failures the whole system is shaped around

**Self-certification.** A party that produced a result and then attests to it
will confirm itself. This is not a claim about honesty — a producer that has
authored a fix acquires an interest in that fix being judged adequate, and a
model asked to check its own reasoning has no independent vantage from which to
disagree. Hence `QROS-ROLE-SELF-CERTIFICATION`, and hence
`QROS-ROLE-SUBAGENT-NOT-INDEPENDENT`: an agent invoked by the producer inherits
the producer's framing, its inputs, and the questions it was told to ask. A
different process is not a different perspective.

**Leakage.** Information about an outcome reaching a party whose judgement is
supposed to be independent of it. The obvious form is a party being told the
answer. The subtle form is a party that could reach the answer and was merely
asked not to. `QROS-BLIND-REPO-NOT-BLIND` treats blindness as a property of what
is technically reachable — a party that must stay blind receives a
digest-pinned bundle, not repository access — because an instruction constrains
conduct and not information flow.

Everything else is downstream of those two.

---

## Failure modes, and what answers them

### Look-ahead leakage

A feature computed from a window that includes the period it is supposed to
predict. The pipeline runs and the result improves. Shape-level
checks pass identically on a leaked and a correct implementation, and so does
reproduction: a leaked signal reproduces perfectly, because reproducing a number
shows only that it follows from the bytes.

**Answer:** the window rule is enforced in the runner's code, not stated in
prose (`QROS-PREREG-ENFORCED-DATA-RULES`); each instrument carries a validity
check that must pass before the primary result is read
(`QROS-PREREG-VALIDITY-CHECKS`); and where the construction itself is in doubt,
an independent recomputation from the sealed definition, isolated in a bundle
that excludes the producer's implementation (`QROS-BLIND-ON-DEMAND`). The worked
example shows the last: four green checks, a confident number, and a different
answer once someone computed it independently.

Also `QROS-CHECK-NON-VACUOUS`: check the property, not a correlated proxy.

### Silent overfitting

Searching until something works, then reporting the winner as though it had been
the only candidate.

**Answer:** the preregistration fixes planned comparisons and the project's
trial-accounting method before anything is computed (`QROS-PREREG-CONTENT`,
`QROS-AXIS-TRIAL-ACCOUNTING`); QROS prescribes no counting formula, because the
right adjustment depends on the design. Discovery has no candidate-count target
(`QROS-S0-DISCOVERY`), and once the question is answered, investigation stops
(`QROS-COMPLETION-STOP-RULE`).

### Moving the threshold

The result comes in at 0.12, the threshold was 0.15, and the threshold becomes
0.10 — usually with a plausible reason.

**Answer:** `QROS-PREREG-SEAL-BEFORE-EXPOSURE` fixes and digests the contract
before the outcome exists, so a later change is detectable rather than deniable.
The contract includes the verdict rule itself (`QROS-PREREG-VERDICT-RULE`), so
S4 computes rather than debates; nobody departs from it after an outcome is seen
(`QROS-VERDICT-NO-DEPARTURE`). Post-seal changes are labelled
(`QROS-CHANGE-LABELS`); a repair that alters the question, rule, threshold,
sample or metric is not a fix (`QROS-CHANGE-FIX-NOT-METHODOLOGY`).

### Unreachable safeguards and unanswerable designs

A kill condition no attainable measurement can reach looks like protection and
provides none (`QROS-PREREG-KILL-REACHABILITY`). A design whose sample cannot
resolve the smallest effect of interest can only return `unresolved`, and
spends a one-shot trial to learn nothing (`QROS-PREREG-RESOLVABILITY`). For a
return-stream claim, precision is set by calendar span — t is the annualized
Sharpe ratio times the square root of the years — so finer bars or more
instruments do not help; a true Sharpe of 0.5 needs about sixteen years to reach
t = 2. Both checks rerun after every amendment
(`QROS-PREREG-RECHECK-AFTER-AMENDMENT`).

### Silent sample reuse

A sample already searched or evaluated is reused as though fresh.

**Answer:** `QROS-REUSE-DECLARE-BEFORE-USE`. `QROS-REUSE-NEW-SEAL-NO-REFRESH`: a
new seal fixes what happens next; it does not undo what a sample has absorbed.
`QROS-REUSE-NEGATIVE-CONSUMES`: a negative result consumes selection freedom
exactly as a favourable one does. And `QROS-EXPOSURE-MONOTONIC`: exposure never
regresses, and a missing record means `UNKNOWN`, never `NONE` — the tempting
default is to assume nothing was seen, which is the assumption leakage exploits.

### Claim mistaken for evidence

"The tests pass" and "I verified it" describing one act.

**Answer:** `QROS-EVIDENCE-SEPARATION` — builder claim, mechanical evidence and
independent verification are not interchangeable, and model-written text is not
evidence for what it states (`QROS-PURPOSE-MODEL-OUTPUT-NOT-EVIDENCE`). Every
acceptance statement carries `REPRODUCED`, `REASONED` or `SELF-REPORTED`
(`QROS-REVIEW-EVIDENCE-CLASSES`), and a PASS that reproduced nothing is not
acceptance (`QROS-ACCEPT-REPRODUCTION-FIRST`).

### Governance that outgrows the research

Every incident produces a guard; every guard needs a test; reviews open reviews.
The process becomes the work. This is what systems of this kind usually die of:

- `QROS-COST-BUDGET` — a control must reduce a concrete risk by more than it
  costs, and is not added because another control failed.
- `QROS-BLOCKER-ADMISSION` — a blocker needs a named threat and a concrete
  failure path on the current or next stage; `QROS-COMPLETION-PROGRESSION` —
  proceed with backlog outstanding.
- `QROS-REVIEW-NOT-ROUTINE`, `QROS-COMPLETION-NO-AUTOMATIC-LOOPS` — no review as
  reassurance, no repair-review-repair cycle.
- `QROS-REVIEW-ROUND-BUDGET` — two substantive rounds per gate per lineage; a
  further HOLD goes to the `OWNER`.

### Transport failure, reopening, and stale state

A review that never validly happened — digests that do not recompute, a crashed
tool — establishes nothing about the work and consumes no review round
(`QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION`). A closed issue restated more
forcefully stays closed; reopening needs new evidence
(`QROS-BLOCKER-CLOSED-STAYS-CLOSED`).

The quieter failure is a record that drifts: a status copied into three places,
one updated. Current state is one screen, rewritten at checkpoints
(`QROS-STATE-CURRENT-ARTIFACT`); history is an append-only log
(`QROS-RECORD-DECISION-LOG-APPEND-ONLY`); derived facts point to their source
(`QROS-RECORD-DERIVED-NOT-COPIED`). Version 1 also asked the current-state page
to be outcome-clean so a blind party could read it. That promise could not be
kept — commit subjects and logs carry outcomes too — so version 2 withdraws it
(`QROS-STATE-NOT-BLIND`) and gives blind parties a bundle instead.

---

## Design choices worth explaining

**Why the Owner is human, and only some gates are retained.** Spending,
live capital, credentials, public release and destructive mutation
(`QROS-GATE-OWNER-RETAINED`) carry costs borne outside the system that no later
record can undo; accountability for them cannot rest with a party that cannot
hold it. Research-internal decisions — seal, run, reveal, verdict, methodology
change — are delegable (`QROS-GATE-DELEGATED`) because seals, sealed rules and
write-ahead grants protect them mechanically; the `OWNER` may take any back.
`QROS-GATE-NO-RELAY`: a relayed message never grants a retained gate, because a
relay is exactly where authority gets forged. And a recommendation does not
authorise acting on it (`QROS-OWNER-AUDIT-NOT-EXECUTION`).

**Why the Delegate may be an AI but never builds.** A `DELEGATE` that built
would certify itself, and a second writer corrupts records. It sends decisions,
which the `BUILDER` records verbatim, and reproduces from the repository at a
revision, never from a message (`QROS-RECORD-CHECKPOINT`).

**Why acceptance starts with reproduction.** Version 1 certified through
reviewer dispatch. Judgement is the expensive, fallible part, and ceremony can
mimic it; reproduction either happens or does not. When `DELEGATE` and
`BUILDER` share a model family, separate sessions separate context and
authorship, not perspective (`QROS-ROLE-SAME-FAMILY-LIMIT`); reproduction and a
sealed, computed verdict rule (`QROS-VERDICT-RULE-COMPUTED`) shrink the surface
where shared blind spots act. They do not remove it.

**Why one verdict vocabulary.** A research status plus a disposition
(`QROS-VERDICT-VOCABULARY`), nothing else: a second scale invites a result to be
described in whichever scale flatters it.

**Why a grant names what it covers.** A grant is recorded before the run, names
the code and data identities it covers, and says whether it is one-shot or
standing (`QROS-RUN-SEAL-NOT-AUTHORIZATION`). A standing grant lets the
`BUILDER` work autonomously without drifting silently: the mechanical run gate
checks those identities and fails closed (`QROS-RUN-GATE-MECHANICAL`,
`QROS-RUN-FAIL-CLOSED`). A one-shot grant is consumed write-ahead
(`QROS-RUN-ONE-SHOT-WRITE-AHEAD`), or crash-and-retry becomes a way to peek.

---

## What this reasoning does not claim

None of it makes a conforming project's conclusions correct. A wrong prior,
defective input data, an error no check was designed to catch, or a threat
outside the vocabulary will pass through all of it. The claim is narrower: a
specific, enumerated set of process failures becomes more expensive to commit
and harder to commit silently.

See [threat-model.md](threat-model.md) for where the boundary sits.
