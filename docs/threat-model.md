# Threat model

What QROS defends against, how, and where the boundary sits.

Explanatory. [SPEC.md](../SPEC.md) is the only normative source. Identifiers are
pointers into it.

---

## The six threat classes

`QROS-THREAT-VOCABULARY` fixes exactly six classes. **The vocabulary is closed**:
a project may not add, remove, merge, or rename one. A concern that fits none of
them is not thereby unimportant — it is non-blocking, and belongs in backlog.

| Class | Covers |
|---|---|
| `RESEARCH_CORRECTNESS` | the result does not follow from the evidence: a defect in method, computation, inference, or interpretation |
| `REPRODUCIBILITY` | the result cannot be reproduced from recorded inputs, code, and procedure |
| `DATA_IDENTITY_OR_PROVENANCE` | the data is not what it is recorded to be: wrong source, wrong period, undisclosed transformation, undeclared reuse, unresolved lineage |
| `INDEPENDENCE_OR_BLINDNESS` | a certification is not independent, or a party judged information it should not have held |
| `CONSEQUENTIAL_EXECUTION_SAFETY` | an action with irreversible or external effect may occur without its authorisation, or outside its authorised bounds |
| `METHODOLOGY_OR_SCOPE_INTEGRITY` | the question, decision rule, or scope changed without the change being classified and recorded |

Six is a deliberate number. A vocabulary large enough to classify every concern
would classify every concern as blocking, which is the same as having no filter.
A closed vocabulary forces the question *which of these six is this?* — and
"none of them" is a legitimate and common answer.

### Why the classes must stay closed

An extensible vocabulary defeats the filter it belongs to. Every project that
finds a concern it cannot classify has a local reason to add a seventh class,
and after a few of those the admission test admits everything. The pressure to
extend is exactly the pressure the closed list exists to resist.

The same reasoning closes the `OWNER` gate list (`QROS-OWNER-GATE-LIST`) and the
blindness mechanism: a configurable safeguard is a safeguard that will be
configured away at the moment it becomes inconvenient.

---

## Blocker admission

**A concern is not automatically a blocker.** `QROS-BLOCKER-ADMISSION` admits an
item to the blocker set only if it states both:

1. **exactly one** of the six threat classes; and
2. a **concrete failure path** on the **current or next** stage — the specific
   sequence by which the defect produces a wrong, irreproducible, or unsafe
   outcome.

Plus, so the row has a defined exit: the evidence that would clear it. A row that
cannot be closed is not admissible.

A statement that something is undesirable is not a failure path. Neither is a
statement that something is wrong — a failure path says *what breaks next*.

**Specifically not admissible:** a cleaner design is imaginable; a stronger
general safeguard could exist; further review would add confidence; a document is
inconsistent; a defect exists on a path this project will not take; a guard
protecting a guard is missing.

A blocking finding also carries an evidence class
(`QROS-REVIEW-EVIDENCE-CLASSES`). `SELF_REPORTED` — restating what the producer
already said — is never blocking on its own, because it adds no independent
information. `REPRODUCED` and `REASONED` may both block; a well-formed reasoned
finding blocks on the same terms as a reproduced one, since requiring execution
before a design defect could be raised would exclude precisely the defects
execution cannot reveal.

### Worked illustration (synthetic)

From the worked example, a finding that **was** admitted:

> **Threat:** `RESEARCH_CORRECTNESS`.
> **Failure path:** the signal dated at period *t* contains the return of period
> *t+1*; the leaked value is the input to the sealed decision table; rule 2
> fires; the candidate is recorded as supported; the reserved sample is spent on
> an artefact.
> **Evidence class:** `REPRODUCED`.
> **Smallest scope:** the window bounds of one expression.

And, from the same review, an observation that was **not** admitted and went to
backlog instead:

> The mechanical check set covers shape, nullity, alignment and determinism
> only, and none of those could distinguish a leaked signal from a correct one.

True, useful, and not a blocker: it names no failure path on the current or next
stage. It was recorded, and the study proceeded.

---

## Transport failure is not implementation failure

`QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION`.

A review can fail to happen validly: a manifest digest mismatches, the evidence
surface turns out insufficient for a mandatory check, the reviewer was
ineligible, or the reviewer was exposed to withheld material before freezing its
own result.

Such a failure:

- **leaves the required gate unsatisfied** — the work is not certified;
- **establishes nothing about the work** — no defect was demonstrated;
- **consumes no review round** — the budget is for disagreement, not delivery;
- **is not a finding against the implementation** — no repair to the code could
  fix it.

The correct response is to repair the delivery and dispatch again. Recording it
as an implementation defect produces two errors at once: a defect that was never
demonstrated enters the record, and review budget is spent on something no code
change addresses.

A review that never became valid returned **no verdict**. There is no fourth
verdict value for it — the verdict vocabulary is exactly `PASS`,
`PASS_WITH_BACKLOG`, `HOLD`, and an invalid review simply carries none.

---

## Closed stays closed

`QROS-BLOCKER-CLOSED-STAYS-CLOSED`. A closed item stays closed. Reopening
**requires** new, concrete evidence of a failure on the current path, in exactly
one of the six threat classes.

None of the following reopens anything: a better approach has become apparent; a
stronger safeguard is conceivable; another reviewer would add reassurance;
historical wording could be improved; the same concern is restated more
forcefully.

Without this rule a project has no way to finish. Any settled question can be
reopened by conviction alone, and the cost of reopening is borne by the people
trying to answer the research question rather than by the person reopening it.

---

## What QROS does not defend against

Stated plainly, because a threat model that lists only successes is marketing.

- **A wrong prior.** If the hypothesis is misconceived, every rule here will be
  followed and the conclusion will still be worthless.
- **Defective input data.** Provenance controls record what the data is claimed
  to be and detect undisclosed change. They do not detect a vendor's error, a
  corrupted source, or a subtly wrong construction upstream of the project.
- **A threat outside the six classes.** The vocabulary is closed by design, and
  the cost of that choice is real: a novel failure mode will be classified as
  non-blocking and recorded as backlog.
- **A determined adversary.** Every mechanism assumes parties are trying to get
  the right answer. A party willing to falsify an attestation, fabricate a
  digest, or misreport its own exposure defeats all of it. QROS raises the cost
  of error and self-deception, not of fraud.
- **Errors no check was designed to catch.** The worked example makes this
  concrete: four green checks, a confident result, and a defect that only
  independent recomputation surfaced. Had nobody recomputed, nothing in the
  system would have noticed.
- **Overfitting as such.** Specific overfitting-adjacent behaviours become
  visible and recorded — moving a threshold, reusing a burned sample, searching
  after the question is answered. The general problem is not solved.
- **Human judgement.** SESOI choice, whether a hypothesis is genuinely distinct,
  how decisive a negative result is, whether a design can answer its claim: none
  of these is mechanisable, and QROS does not pretend otherwise.

`QROS-PURPOSE-NO-CORRECTNESS-GUARANTEE` states the limit normatively. QROS makes
no claim of suitability for any regulatory, fiduciary, or contractual obligation,
and confers no certification: conformance is self-declared.

---

## Residual risks worth naming

**The reviewer is the load-bearing element.** Most of the system's protective
value comes from independent recomputation. A project that dispatches review as
ceremony — a reviewer who reads and agrees rather than recomputes — keeps the
paperwork and loses the protection, and no rule here can detect the difference
from outside.

**Blindness depends on how the evidence surface is built.** The specification
requires a separately constructed surface with enumerated contents. A surface
assembled carelessly, or one whose "enumeration" is a directory that happens to
contain more than intended, is not blind. The digest discipline exists to make
that checkable, and it only works if the digests are actually recomputed.

**Self-declared conformance is self-declared.** Nothing verifies that a project
claiming to follow QROS does. The publication-assurance rule
(`QROS-CONFORMANCE-PUBLICATION-ASSURANCE`) is the one place the specification
insists a claim be checkable rather than asserted, and it applies to disclosure,
not to research quality.
