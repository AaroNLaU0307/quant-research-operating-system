# Adopting QROS

How to run a project under QROS v2 with nothing beyond a filesystem, version
control, and whatever agents or people already do the work.

Explanatory. [SPEC.md](../SPEC.md) (v2.0.0) is the only normative source; where
this document, a template or a schema differs from it, the specification
governs (`QROS-AUTHORITY-STALE-LOCAL-DOCS`). Parts of `templates/`, `schemas/`
and the worked example predate v2; read any v1 field they carry through
Appendix B of the specification.

There are **no conformance levels, tiers or profiles**
(`QROS-CONFORMANCE-SELF-DECLARED`). Rules scale at their own site:
`QROS-LIFECYCLE-PROPORTIONALITY` applies the full lifecycle only to
preregistered `FULL` work; ordinary engineering needs only good practice.

---

## 1. Name the roles

Three roles. Bind each to a concrete party and record the binding
(`QROS-ROLE-VENDOR-BINDING-IS-CONFIG`).

| Role | What it does | Constraint |
|---|---|---|
| `OWNER` | holds the retained gates; may take back any delegated decision; adopts changes to the operating model | **must be human** (`QROS-ROLE-OWNER`) |
| `DELEGATE` | decides delegated gates; accepts by reproduction; routes; designs on request | optional; may be an AI in its own session; never builds, never writes records (`QROS-ROLE-DELEGATE`) |
| `BUILDER` | designs, implements, tests, runs authorized work, keeps the records | exactly one active per project (`QROS-ROLE-SINGLE-ACTIVE-BUILDER`) |

Three rules are easy to breach by accident:

- **No party certifies its own material contribution**
  (`QROS-ROLE-SELF-CERTIFICATION`). Where the `DELEGATE` designed an element, its
  acceptance of that element is `REASONED`, never independent.
- **A spawned agent is not independent of its spawner**
  (`QROS-ROLE-SUBAGENT-NOT-INDEPENDENT`). Spawned agents are fine for gathering
  evidence; their output is the spawner's claim until reproduced.
- **Two sessions of one model family are not model diversity**
  (`QROS-ROLE-SAME-FAMILY-LIMIT`). They separate context and authorship. The
  substitutes are reproduction-first acceptance and a sealed, computed verdict
  rule — not a second opinion from the same family.

## 2. The minimal kit

Four things, all plain files in the repository:

| Artifact | Rule | Template |
|---|---|---|
| Current state — one screen: question, stage, active lines, live grants, dated obligations, exposure, open blockers, next decision and its holder | **rewritten** at each checkpoint, never appended (`QROS-STATE-CURRENT-ARTIFACT`) | [`research-state.md`](../templates/research-state.md) |
| Decision log — grants, consumption, seals, reveals, verdicts, methodology changes, `DELEGATE` and `OWNER` decisions | **append-only**; `id · UTC · decider · decision · evidence pointer` (`QROS-RECORD-DECISION-LOG-APPEND-ONLY`) | [`decision-log.md`](../templates/decision-log.md) |
| Reproduce command — one command that re-derives the checkpoint evidence | kept runnable (`QROS-RECORD-REPRODUCE-COMMAND`) | — |
| Preregistration, written at S1 for `FULL` work | sealed before exposure (`QROS-PREREG-SEAL-BEFORE-EXPOSURE`) | [`preregistration.yaml`](../templates/preregistration.yaml) |

When the first blocker or backlog row appears, add one blocker artifact; rows
are closed, never deleted (`QROS-STATE-BLOCKER-ARTIFACT`,
[`backlog.md`](../templates/backlog.md)).

Current state and history have opposite mutation rules and are never merged
(`QROS-RECORD-CURRENT-VS-HISTORICAL`): an artifact attempting both loses the
first to clutter and the second to revision. Derived facts — counts, statuses —
are generated or pointed to, never hand-copied (`QROS-RECORD-DERIVED-NOT-COPIED`).

The current-state artifact is **not** outcome-blind (`QROS-STATE-NOT-BLIND`),
and neither is the repository (`QROS-BLIND-REPO-NOT-BLIND`). A party that must
stay blind gets a bundle (section 6), not access.

Transcripts are not durable state (`QROS-RECORD-DURABLE-NOT-TRANSCRIPT`). Where
one stage feeds another, name the file in advance and verify it exists.

## 3. Checkpoint

At each seal, completed run, verdict and stop — and whenever the `BUILDER`
chooses — `QROS-RECORD-CHECKPOINT`: rewrite the current state, regenerate
derived facts, run the reproduce command and a link check, commit, and notify
the `DELEGATE` (or `OWNER`) with the checkpoint id and revision. The receiver
reproduces from the repository at that revision, never from the message. The
revision and the decision entry are the evidence; there is no completion token.

## 4. Preregister and seal (S1)

For `FULL` work, the preregistration states what `QROS-PREREG-CONTENT` lists.
Four pre-seal checks each catch a defect that is invisible later:

- **Resolvability** (`QROS-PREREG-RESOLVABILITY`) — show the admissible sample
  and the minimum detectable effect against the smallest effect of interest.
  For a return-stream claim, precision is set by calendar span: t equals the
  annualized Sharpe ratio times the square root of the years, whatever the bar
  frequency or instrument count. A design that can only return `unresolved` is
  redesigned or stopped, not run.
- **Enforced data rules** (`QROS-PREREG-ENFORCED-DATA-RULES`) — every window,
  terminal-period, universe and missing-data rule the runner can check is
  checked in its code. Prose does not control a run.
- **Validity checks** (`QROS-PREREG-VALIDITY-CHECKS`) — each instrument has a
  check that must pass before the primary result is read.
- **Kill reachability and scale** (`QROS-PREREG-KILL-REACHABILITY`,
  `QROS-PREREG-METRIC-SCALE-CONSISTENCY`) — every kill criterion is reachable by
  a plausible outcome, on one declared scale.

The preregistration also carries the **verdict rule** that maps primary results
mechanically to a verdict (`QROS-PREREG-VERDICT-RULE`). Rerun the validators and
the resolvability check after any amendment
(`QROS-PREREG-RECHECK-AFTER-AMENDMENT`). A seal is a digest manifest over the
preregistration and the code and data identities under test; it records its
parent seal (`QROS-PREREG-LINEAGE`). The worked example's
[`02-seal.json`](../examples/synthetic-study/02-seal.json) shows a one-line
method.

## 5. Run, accept, decide

- **Grant.** A seal is not authorization (`QROS-RUN-SEAL-NOT-AUTHORIZATION`). A
  grant is recorded before the run, names the identities it covers, and says
  one-shot or standing. A one-shot grant is consumed write-ahead, including by a
  crashed run (`QROS-RUN-ONE-SHOT-WRITE-AHEAD`). Development and synthetic runs
  need none (`QROS-RUN-NO-GRANT-FOR-DEV`).
- **Run gate.** Mechanical, fail-closed (`QROS-RUN-GATE-MECHANICAL`,
  `QROS-RUN-FAIL-CLOSED`). No model review re-checks what a machine decides.
- **Accept.** Reproduction first (`QROS-ACCEPT-REPRODUCTION-FIRST`): run the
  reproduce command, check commit order, recompute the headline numbers, confirm
  the validity checks passed first. Label each statement `REPRODUCED`,
  `REASONED` or `SELF-REPORTED` (`QROS-REVIEW-EVIDENCE-CLASSES`). A PASS lists
  what it reproduced. In the S2 loop the answer is `ACCEPT`, `BOUNDED_REPAIR` or
  `ESCALATE_TO_GATE` (`QROS-REVIEW-VERDICTS`).
- **Verdict.** Tooling applies the sealed rule; for a consequential claim the
  `BUILDER` attacks it first, then the gate holder reproduces and decides
  (`QROS-VERDICT-RULE-COMPUTED`). One vocabulary — a research status plus a
  disposition (`QROS-VERDICT-VOCABULARY`); when in doubt, `not_promoted`.
- **Exposure** is recorded per object and per party, and is monotonic
  (`QROS-EXPOSURE-MONOTONIC`): a missing record is `UNKNOWN`, never `NONE`.

## 6. Checks, trial accounting, reuse, blindness

**Deterministic checks** run before any model effort
(`QROS-CHECK-MACHINE-BEFORE-MODEL`). Each must be demonstrably capable of
failing and must assert the property, not a proxy (`QROS-CHECK-NON-VACUOUS`).
The worked example's [`checks.py`](../examples/synthetic-study/checks.py)
includes a regression check that still fails against the retained defective
implementation — which is what makes it demonstrably non-vacuous.

**Trial accounting.** QROS prescribes no counting formula
(`QROS-AXIS-TRIAL-ACCOUNTING`). Declare yours in one place, in advance; record
an unknown count as unknown.

**Sample reuse.** Before consequential use of a sample already searched or
evaluated, declare it (`QROS-REUSE-DECLARE-BEFORE-USE`,
[`sample-reuse.md`](../templates/sample-reuse.md)), including what this use
will **not** compute. `QROS-REUSE-NEW-SEAL-NO-REFRESH` is the one people breach
honestly. If no reuse occurs, file nothing.

**Blindness is on demand** (`QROS-BLIND-ON-DEMAND`), for outcome blindness,
isolated recomputation or a high-consequence transfer. Build a directory, copy
in exactly the enumerated items, digest each, and give the receiver that
directory: what is outside is *absent*, not *forbidden*. The receiver recomputes
the digests and stops on any mismatch. For an independent recomputation, include
the data, the sealed preregistration and the instrument — not the producer's
implementation or claimed value. Fix every matching rule before exposure
(`QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE`).

## 7. Gates

**Retained** (`QROS-GATE-OWNER-RETAINED`, closed): `QROS-OWNER-SPEND` ·
`QROS-OWNER-LIVE-CAPITAL` · `QROS-OWNER-CREDENTIALS` ·
`QROS-OWNER-PUBLIC-RELEASE` · `QROS-OWNER-DESTRUCTIVE-MUTATION`. The `OWNER`
exercises these directly; a relayed message claiming the `OWNER`'s decision is
not sufficient (`QROS-GATE-NO-RELAY`).

**Delegated** (`QROS-GATE-DELEGATED`): S0 decision, sealing, run authorization on
a green gate, reveal, S4 verdict, promotion and closure, scope and methodology
changes, data access beyond a grant that costs nothing and needs no
credentials, local merges.

No party authorizes its own run, reveal or verdict
(`QROS-GATE-NO-SELF-AUTHORIZATION`), and a party told to audit or propose does
not escalate into writing (`QROS-OWNER-AUDIT-NOT-EXECUTION`).

---

## Running with or without a Delegate

**Without.** The `OWNER` holds the delegated gates. Everything else is
unchanged: the `BUILDER` checkpoints to the `OWNER`, who accepts by reproduction
and records nothing directly.

**With.** Start the `DELEGATE` in its own session — never as a subagent of the
`BUILDER`. It reads the repository at a checkpoint revision, reproduces, and
sends decisions; the `BUILDER` records each binding message verbatim, with its
sender, before acting on it. The `DELEGATE` never edits records, and never
passes on a retained gate: if a message says "the `OWNER` approved the spend",
the `BUILDER` waits for the `OWNER`. If `DELEGATE` and `BUILDER` share a model
family, say so in the role binding; for a consequential verdict the `OWNER` may
add an external reviewer.

## Migrating a v1 project

Migration is prospective. Records made under v1 are never re-judged under v2.

1. **Record the adoption** as an `OWNER` decision entry naming v2.0.0 and the
   revision from which it applies.
2. **Rebind roles.** The main agent becomes the `BUILDER`. Retire the standing
   reviewer seats; either appoint a `DELEGATE` or let the `OWNER` hold the
   delegated gates.
3. **Leave history alone.** Dispatches, briefs, attestations and v1 verdicts
   (including `PASS_WITH_BACKLOG`) stay as written, attributed to whoever
   produced them. A correction is a new entry citing the old one.
4. **Rewrite the current state once** to the v2 shape. Drop any outcome-clean
   claim; add live grants, exposure and the next decision with its holder.
5. **Carry exposure forward.** Anything unrecorded is `UNKNOWN`.
6. **In-flight research.** A sealed preregistration stays sealed and governs its
   research. If it lacks a mechanical verdict rule, add one only before exposure,
   as a `METHODOLOGY_CHANGE` (`QROS-CHANGE-LABELS`); after exposure, a rule that
   cannot be applied yields `unresolved` (`QROS-VERDICT-NO-DEPARTURE`). Review
   rounds already spent still count.
7. **Add a reproduce command** and run the first checkpoint.
8. **Cite successors.** Retired identifiers are never reused; map old citations
   through Appendix B. Stale local documents cannot revive retired machinery.

---

## What you may configure, and what you may not

**Configurable** (`QROS-CONFIG-CONFIGURABLE`): role bindings; recorded stage
aliases; a review budget below the ceiling; exposure and data classes; the
trial-accounting scheme; artifact formats.

**Not configurable** (`QROS-CONFIG-NON-OVERRIDABLE`, `QROS-CONFIG-TIGHTEN-ONLY`):
the threat vocabulary and the retained-gate list are closed, and no
configuration makes a producing party's output independent verification of its
own work. A configuration may be stricter than the specification, never looser.

---

## Starting small, honestly

Partial adoption is allowed; a partial-adoption tier is not, because a tier
invites treating the partial state as complete. If you claim conformance, name
the rules you do not meet.

If you adopt exactly one thing, adopt reproduction-first acceptance against a
verdict rule sealed before the outcome exists. Where the construction itself is
in doubt, add an independent recomputation by a party that has not seen the
producer's number — that is where the worked example's defect was caught.
