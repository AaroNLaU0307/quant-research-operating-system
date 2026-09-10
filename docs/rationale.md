# Why QROS looks like this

Explanatory. [SPEC.md](../SPEC.md) is the only normative source; where this
document and the specification differ, the specification governs. Identifiers
like `QROS-BLIND-IS-TRANSPORT` are pointers into it, not restatements of it.

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
supposed to be independent of it. The obvious form is a reviewer being told the
answer. The subtle form is a reviewer that could reach the answer and was merely
asked not to. `QROS-BLIND-IS-TRANSPORT` treats blindness as a property of what
is technically reachable, because an instruction constrains conduct and not
information flow.

Everything else is downstream of those two.

---

## Failure modes, and what answers them

### Look-ahead leakage

A feature computed from a window that includes the period it is supposed to
predict. It is not a syntax error; the pipeline runs, the shapes match, the
result improves. Shape-level checks — length, nullity, alignment, determinism —
pass identically on a leaked and a correct implementation, because a leaked
signal has the same shape as a correct one.

**Answer:** independent recomputation from the sealed definition
(`QROS-REVIEW-MANDATORY-TRIGGERS`), by a party that has not seen the producer's
implementation. The worked example demonstrates exactly this: four green checks
and a confident number, and a different answer the moment someone computed it
independently.

Also `QROS-CHECK-NON-VACUOUS`: a check that observes the property of interest,
rather than a proxy that correlates with it. Where the property is a runtime
behaviour, a check over static structure does not establish it.

### Silent overfitting

Searching until something works, then reporting the winner as though it had been
the only candidate.

**Answer:** the preregistration fixes the number of planned comparisons and the
project's trial-accounting method before anything is computed
(`QROS-PREREG-CONTENT`, `QROS-AXIS-TRIAL-ACCOUNTING`). QROS deliberately
prescribes no counting formula — it records the method the project declares,
because the right adjustment depends on the design and a specification that
hard-coded one would be wrong more often than helpful.

And `QROS-COMPLETION-STOP-RULE`: once the preregistered question is answered,
investigation of that question stops. Unbounded post-hoc search on an answered
question is indistinguishable, in its effect on the evidence, from selecting a
favourable result.

### Moving the threshold

The result comes in at 0.12, the threshold was 0.15, and the threshold becomes
0.10 — usually with a plausible reason.

**Answer:** `QROS-PREREG-SEAL-BEFORE-EXPOSURE`. The contract is fixed and
digested before any party involved sees the target metric, so a later change is
detectable rather than deniable. Post-seal changes are classified
(`QROS-CHANGE-LABELS`), and `QROS-CHANGE-FIX-NOT-METHODOLOGY` closes the gap a
bug fix would otherwise open: a repair that alters the question, the rule, the
threshold, the sample or the metric is a methodology change however small the
edit and however genuine the defect that prompted it.

### Unreachable safeguards

A kill condition whose branch no attainable measurement can reach. It looks like
protection and provides none.

**Answer:** `QROS-PREREG-KILL-REACHABILITY` requires demonstrating, from inputs
available in advance, that the branch can fire on realistic input — and
`QROS-PREREG-RECHECK-AFTER-AMENDMENT` requires re-running that check after every
amendment, because repairing one rule defect can introduce another and an
amendment checked only where it was applied is not checked.

### Silent sample reuse

A sample that has already been searched, fitted, or evaluated is used again as
though fresh. Each reuse consumes selection freedom; nothing records it.

**Answer:** `QROS-REUSE-DECLARE-BEFORE-USE` requires the declaration in advance,
including what the work will **not** compute — because the scope of an
examination determines how much freedom it consumes, and an unbounded
examination is indistinguishable from an unlimited one.

Two related rules exist because both are counter-intuitive.
`QROS-REUSE-NEW-SEAL-NO-REFRESH`: sealing a new contract fixes what happens
next; it does not undo what a sample has absorbed.
`QROS-REUSE-NEGATIVE-CONSUMES`: work that produces a negative result consumes
selection freedom exactly as favourable work does, and discloses what was
tested, on which sample, under what design.

### Claim mistaken for evidence

"The tests pass" and "I verified it" describing the same act.

**Answer:** `QROS-EVIDENCE-SEPARATION` names three distinct kinds of support —
builder claim, mechanical evidence, independent verification — and forbids
substituting one for another. A record must say which supports each claim.
Related traps get their own rules because each is individually tempting:
passing tests are evidence for the properties those tests assert and nothing
else; a docstring agreeing with a claim is part of the artifact under
examination, not a check on it; agreement between reviewers or model families is
a review outcome and not replication; and a favourable verdict on code quality
does not authorise research action.

### Governance that outgrows the research

Every incident produces a guard. Every guard needs a test. Every test needs an
index. Reviews open reviews. The process becomes the work.

This is the failure mode most systems of this kind actually die of, and several
rules exist solely against it:

- `QROS-BLOCKER-ADMISSION` — a concern is a blocker only with one threat class
  and a concrete failure path on the current or next stage. "A cleaner design is
  imaginable" is explicitly not admissible.
- `QROS-COMPLETION-PROGRESSION` — if the question can be answered and no blocker
  threatens the answer, proceed with backlog outstanding.
- `QROS-COMPLETION-NO-AUTOMATIC-LOOPS` — review happens because a rule requires
  it or the Owner asks, never as reassurance after ordinary validation.
- `QROS-REVIEW-ROUND-BUDGET` and `QROS-REVIEW-ESCALATION-ON-EXHAUSTION` — a
  finite budget per issue lineage, counted continuously across renames so an
  issue cannot acquire fresh budget by being relabelled; then a human decides.
- `QROS-REVIEW-NOT-ROUTINE` — review dispatched for maintenance and formatting
  consumes the capacity reserved for consequential disagreement.
- `QROS-LIFECYCLE-PROPORTIONALITY` — the full lifecycle is for preregistered
  studies. Work that cannot produce a durable claim, expose a reserved sample,
  or cause an unsafe action needs no stage beyond ordinary engineering.

### Transport failure read as implementation failure

A review that never validly happened — a mismatched digest, an insufficient
evidence surface, an ineligible reviewer — recorded as a finding against the
work.

**Answer:** `QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION`. Such a failure leaves
the gate unsatisfied and establishes nothing about the work. It consumes no
review round, and it is not a defect to be repaired in the code. Conflating the
two produces two errors at once: it records defects that were never
demonstrated, and it burns review budget on failures no repair to the work could
fix.

### Reopening settled questions

A closed issue returns because someone restates it more forcefully.

**Answer:** `QROS-BLOCKER-CLOSED-STAYS-CLOSED`. Reopening requires new, concrete
evidence of a failure on the current path in one threat class. Not: a better
approach has become apparent, a stronger safeguard is conceivable, another
reviewer would add reassurance.

---

## Two design choices worth explaining

**Why the Owner must be human.** `QROS-ROLE-OWNER` reserves a closed list of
consequential actions — real-data execution, reveal, disposition, methodology
change, public release, destructive mutation — and requires a human to authorise
each. Not because agents are untrustworthy, but because these are the decisions
whose cost is borne outside the system, and accountability for them cannot be
delegated to a party that cannot hold it. `QROS-OWNER-AUDIT-NOT-EXECUTION`
closes the obvious route around it: producing a recommendation, however well
supported, does not authorise acting on it.

**Why one authorisation covers one execution.** Consequential execution against
real data is authorised per execution, bound to that execution's identity, and
re-verified immediately before it starts. This is more Owner effort than a
standing permission would be. It is deliberate: a standing authorisation drifts
from what was actually approved as code and data move underneath it, and the
drift is invisible precisely when it matters.

---

## What this reasoning does not claim

None of it makes a conforming project's conclusions correct. A wrong prior,
defective input data, an error no check was designed to catch, or a threat
outside the vocabulary will pass through all of it. The claim is narrower and
worth stating plainly: a specific, enumerated set of process failures becomes
more expensive to commit and harder to commit silently.

See [threat-model.md](threat-model.md) for where the boundary sits.
