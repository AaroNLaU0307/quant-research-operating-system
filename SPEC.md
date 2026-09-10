# QROS — Quantitative Research Operating System

**Specification, version 1.0.0-draft**

QROS is a specification for conducting quantitative research with substantial
assistance from artificial-intelligence (AI) agents, in a way that keeps the
resulting claims reproducible, falsifiable, bounded in cost, and resistant to
two specific failure modes: **self-certification** (the party that produced a
result also attests to it) and **leakage** (information about an outcome
reaching a party whose judgement is supposed to be independent of it).

This document is the **sole normative source** for QROS. Every normative rule
appears here exactly once and carries a stable semantic identifier such as
`QROS-ROLE-SELF-CERTIFICATION`. Cross-references within this document use those
identifiers rather than section numbers, so sections may be reordered without
invalidating a reference.

**How to read the rules.** *MUST*, *MUST NOT*, *SHOULD*, *SHOULD NOT* and *MAY*
carry their ordinary specification meanings. A rule stated without one of those
words is a definition rather than an obligation. Section numbers are for
navigation only; identifiers are the stable reference.

---

## Contents

0. [Purpose and Non-Goals](#0-purpose-and-non-goals)
1. [Authority Model](#1-authority-model)
2. [Roles](#2-roles)
3. [Three Orthogonal Research Axes](#3-three-orthogonal-research-axes)
4. [Four Kinds of Independence](#4-four-kinds-of-independence)
5. [Research Lifecycle](#5-research-lifecycle)
6. [Preregistration and Sealing](#6-preregistration-and-sealing)
7. [Evidence Model](#7-evidence-model)
8. [Sample Reuse and Trial Accounting](#8-sample-reuse-and-trial-accounting)
9. [Threat Vocabulary](#9-threat-vocabulary)
10. [Reviewer Model](#10-reviewer-model)
11. [Blindness and Transport](#11-blindness-and-transport)
12. [Blocker Model](#12-blocker-model)
13. [Completion-First Progression](#13-completion-first-progression)
14. [Owner Gates](#14-owner-gates)
15. [State and Records](#15-state-and-records)
16. [Change Control](#16-change-control)
17. [Machine Checks Before Model Checks](#17-machine-checks-before-model-checks)
18. [Conformance](#18-conformance)
19. [Configuration](#19-configuration)

[Appendix A — Semantic Identifier Index](#appendix-a--semantic-identifier-index)

---

## 0. Purpose and Non-Goals

### `QROS-PURPOSE-SCOPE`

QROS governs the **process** by which a quantitative research claim is designed,
produced, checked, certified, decided, and recorded. It does not govern the
content of any hypothesis, the choice of any estimator, or the economics of any
market.

What a QROS project produces depends on the kind of work it is doing. QROS
recognises more than one legitimate terminal output:

- A `FULL`-lane preregistered study culminates in a **decided research
  question**: a question fixed in advance, answered by evidence, independently
  verified by a party that did not produce it, decided by the `OWNER`, and
  recorded with its provenance and its limitations.
- `EXPLORATORY` work, `MEASUREMENT` work, and defect repair terminate in the
  records their lane and work type permit (`QROS-AXIS-LANE`,
  `QROS-LIFECYCLE-PROPORTIONALITY`): hypotheses and leads; established facts
  about an implementation or a dataset; or a repaired defect with its regression
  test.

Each is a complete output in its own right, and reaching it is not a partial or
degraded result. Such work MUST NOT be presented as a decided confirmatory
research question, and it does not acquire independent verification merely by
being finished — independent review attaches to the cases in
`QROS-REVIEW-MANDATORY-TRIGGERS`, not to completion.

Whether an answer is favourable is not a measure of whether the process worked.

### `QROS-PURPOSE-NO-ALPHA-CLAIM`

QROS does not discover profitable strategies, and adopting QROS MUST NOT be
represented as evidence that any strategy is profitable. QROS constrains how a
claim may be made; it contributes nothing to whether the claim is true.

### `QROS-PURPOSE-MODEL-OUTPUT-NOT-EVIDENCE`

Output produced by an AI model is not evidence by virtue of having been produced
by a model. Specifically:

- **Model confidence is not evidence.** A statement's assertiveness, fluency, or
  stated probability carries no evidential weight.
- **Agreement between models is not empirical replication.** Concurrence is a
  review outcome; see `QROS-EVIDENCE-AGREEMENT-NOT-REPLICATION`.
- **A plausible narrative is not a result.** An economic rationale explains why
  an effect might exist. It is not evidence that it does.

### `QROS-PURPOSE-NEGATIVE-RESULTS-VALID`

A research question answered in the negative is a complete and legitimate
output. A project that preregisters a question, answers it, and records that the
effect was absent or too small to act on has succeeded.

A process that recognises only favourable outcomes as success creates pressure
to keep searching until one appears. That pressure is itself a research-integrity
failure, and several rules in this document exist to remove it — in particular
`QROS-COMPLETION-STOP-RULE` and `QROS-REUSE-NEGATIVE-CONSUMES`.

### `QROS-PURPOSE-NO-CORRECTNESS-GUARANTEE`

QROS does not guarantee that a conforming project's conclusions are correct. It
is designed to raise the cost of an enumerated set of process failures and to
make those failures explicit when they occur. A conforming project can still
reach a wrong conclusion through a mistaken prior, defective input data, an
error no check was designed to catch, or a threat outside
`QROS-THREAT-VOCABULARY`.

QROS makes no claim of suitability for any regulatory, fiduciary, or contractual
obligation.

---

## 1. Authority Model

### `QROS-AUTHORITY-PRECEDENCE`

Where instructions conflict, the following order applies, highest first:

| Rank | Layer | What it is |
|---|---|---|
| 1 | **This specification** | The normative rules in this document |
| 2 | **Project configuration** | A project's declared settings, bounded by `QROS-CONFIG-NON-OVERRIDABLE` |
| 3 | **Agent instructions** | Operating instructions given to an agent for a project or task |
| 4 | **Runtime defaults** | Any behaviour not fixed by the layers above |

A lower layer MAY make a higher layer stricter. A lower layer MUST NOT make a
higher layer more permissive (`QROS-CONFIG-TIGHTEN-ONLY`).

Two commitments rank above this specification, because a project has already
made them and cannot unilaterally revoke them:

- a **sealed preregistration**, as to the matters it fixes, for the study it
  seals (`QROS-PREREG-SEAL-BEFORE-EXPOSURE`);
- a **recorded `OWNER` decision**, as to the matter it decides
  (`QROS-OWNER-GATE-LIST`).

### `QROS-AUTHORITY-CROSS-SCOPE-CONFLICT`

When two instructions conflict and neither lies within the other's scope — so
that no most-specific-wins reading resolves them — an agent MUST NOT choose
between them. It MUST halt the affected work, state the conflict and both
sources, and refer the matter to the `OWNER`.

Most-specific-wins applies only within an already-authorised scope. It is not a
general tie-breaker and MUST NOT be used to resolve a conflict between
independent sources of authority.

---

## 2. Roles

QROS defines four **capability roles**. A role is a set of obligations and
permissions. It is not a person, a process, a session, or a product.

### `QROS-ROLE-OWNER`

The `OWNER` is the accountable human authority for a project: the only party
that may authorise the actions in `QROS-OWNER-GATE-LIST`, and the escalation
target when review is exhausted (`QROS-REVIEW-ESCALATION-ON-EXHAUSTION`) or
authority conflicts (`QROS-AUTHORITY-CROSS-SCOPE-CONFLICT`).

The `OWNER` MUST be human. No agent may hold this role, and no agent may assume
it by delegation, inference, silence, or claimed urgency.

### `QROS-ROLE-MAIN-AGENT`

The `MAIN_AGENT` designs, implements, tests, produces evidence, and maintains
project records. It is the default working role: most work in a QROS project is
`MAIN_AGENT` work, and invoking any other role requires a stated reason.

### `QROS-ROLE-INDEPENDENT-REVIEWER`

The `INDEPENDENT_REVIEWER` certifies work it did not produce. It challenges
designs before they are sealed, verifies outputs after they are produced, and
returns a verdict under `QROS-REVIEW-VERDICTS`.

An `INDEPENDENT_REVIEWER` MUST NOT repair the work it reviews. Identifying a
defect and fixing it are separate acts, because a party that has authored a fix
acquires an interest in that fix being judged adequate.

### `QROS-ROLE-ARCHITECTURE-REVIEWER`

The `ARCHITECTURE_REVIEWER` adjudicates design-level questions: cases where the
overall approach is itself unresolved, or where no bounded implementation path
can be derived under existing authority.

### `QROS-ROLE-ARCHITECTURE-ESCALATION-BOUNDED`

Escalation to `ARCHITECTURE_REVIEWER` is permitted **only** for an
`ARCHITECTURE_LEVEL_BLOCKER` as defined in `QROS-BLOCKER-CLASSES`. It MUST NOT
be used for ordinary debugging, routine code review, general adversarial review,
transport or packaging problems, normal implementation defects, reassurance, or
speculative improvement of an already-adequate design.

Architecture review is an exception path, not a lifecycle stage. A project in
which it occurs routinely has misclassified its blockers
(`QROS-BLOCKER-ADMISSION`).

### `QROS-ROLE-SELF-CERTIFICATION`

Producing a consequential artifact and independently certifying it are separate
capabilities and MUST be held by separate parties.

The party that produced a consequential artifact MUST NOT be its sole
independent certifier. This is a structural constraint, not a judgement about
competence, and it holds regardless of the producer's capability or diligence.
It attaches to the artifact rather than to the clock: a later working session of
the same producing party inherits the same disqualification with respect to that
artifact.

What counts as **consequential** is fixed by `QROS-REVIEW-MANDATORY-TRIGGERS`.
Work that is not consequential requires no independent certification at all.

### `QROS-ROLE-SUBAGENT-NOT-INDEPENDENT`

An agent invoked by a producing party — as a subprocess, subagent, delegated
task, or any other spawned unit — is **not** independent of that party, however
separate its execution context. Its task framing, its inputs, and the questions
it was told to ask all originate with the producer.

Spawned agents MAY be used for parallel evidence gathering. They SHOULD return
evidence — locations, quoted content, raw output — rather than conclusions,
because a summary is a compression and compressions conceal the errors they
compress. A spawned agent's conclusion MUST NOT be recorded as independent
verification.

### `QROS-ROLE-SINGLE-ACTIVE-BUILDER`

Where two parties acting as `MAIN_AGENT` could write the same artifacts, at most
one MUST be active at a time for that scope. Concurrent builders corrupt each
other's records, and the corruption is typically discovered later, in the
records themselves.

Where concurrent work is genuinely required, the project MUST partition write
scope in advance so that no artifact has two writers. Absent such a partition,
an agent that discovers another agent already writing the artifacts it was about
to write MUST halt and report rather than proceed.

### `QROS-ROLE-VENDOR-BINDING-IS-CONFIG`

The mapping from QROS roles to specific AI models, vendors, or products is
**project configuration** (`QROS-CONFIG-CONFIGURABLE`) and forms no part of QROS
semantics. This specification names no model and no vendor, and a conforming
project MUST NOT represent any particular product as normatively required by
QROS.

A project MUST record which concrete party actually filled a role for each
consequential act, because reproducibility concerns what happened rather than
what a policy preferred. Records already written MUST NOT be retroactively
re-attributed when a project later changes its role bindings.

---

## 3. Three Orthogonal Research Axes

### `QROS-AXES-THREE`

Every unit of research work carries three independent attributes:

| Axis | Values | Governs |
|---|---|---|
| `LANE` | `EXPLORATORY`, `MEASUREMENT`, `FULL` | which claims the work may emit |
| `TRIAL_ACCOUNTING` | project-defined counters and reuse constraints | how much selection freedom a sample has absorbed |
| `OUTCOME_EXPOSURE` | `NONE`, `AGGREGATE`, `TARGET_METRIC`, `UNKNOWN` | what a party has learned about the answer |

### `QROS-AXES-NO-INFERENCE`

The value of one axis MUST NOT be inferred from the value of another. Each is
declared, or determined by its own rules, independently.

The following inferences are specifically prohibited. Each is intuitive, and
each is false:

| Prohibited inference | Why it fails |
|---|---|
| exploratory work consumes no trials | Exploration that examines target performance consumes selection freedom regardless of lane. |
| measurement work leaves the sample clean | A measurement can expose the target metric on a sample reserved for later confirmation. |
| a full study equals exactly one trial | The number of effective attempts is set by the trial-accounting plan, not by the lane. |
| no counter increment means no contamination | Exposure and counting answer different questions (`QROS-REUSE-EXPOSURE-VS-TRIALS`). |
| undetermined exposure means no exposure | Absence of a determination is `UNKNOWN`, never `NONE`. |

### `QROS-AXIS-LANE`

`LANE` determines which claims the work may emit, and nothing else.

| Lane | Purpose | May emit | MUST NOT emit |
|---|---|---|---|
| `EXPLORATORY` | idea generation, prototyping, mechanism search | hypotheses, leads, candidate failure modes, exploratory observations | confirmatory performance claims; promotion; falsification |
| `MEASUREMENT` | establish implementation, data, or system facts | factual claims about implementation or data, including confirmed ones where reproducibly verified | a performance verdict; a selection among candidates on performance |
| `FULL` | answer a preregistered question | promotion, falsification, durable confirmatory claims | anything outside the sealed contract |

### `QROS-LANE-CLAIM-SCOPE`

Lane restricts **confirmatory performance and strategy claims only**. It does
not restrict factual claims of other kinds.

A `MEASUREMENT`-lane investigation that reproducibly demonstrates a
deterministic implementation defect MAY record that defect as a confirmed
factual claim. The same investigation MUST NOT record a performance result
arising from that work as confirmatory evidence about a strategy. Lane and claim
type are distinct attributes and do not map one-to-one.

### `QROS-AXIS-TRIAL-ACCOUNTING`

`TRIAL_ACCOUNTING` records how much selection freedom a sample has absorbed: the
number of effective attempts, which samples must not be retested, and any
multiple-comparison adjustment the project has committed to.

Trial accounting is governed solely by a project's declared plan
(`QROS-PREREG-CONTENT`) and its reuse declarations
(`QROS-REUSE-DECLARE-BEFORE-USE`). This specification adds no counting rule of
its own, and no other rule in this document may be read as adjusting a trial
count.

### `QROS-AXIS-OUTCOME-EXPOSURE`

`OUTCOME_EXPOSURE` records what a party has learned about the answer to a
question:

- `NONE` — nothing about the outcome has been observed.
- `AGGREGATE` — summary or distributional information has been observed, but not
  the decision-relevant quantity.
- `TARGET_METRIC` — the quantity a decision rule reads has been observed.
- `UNKNOWN` — exposure has not been determined.

`UNKNOWN` MUST be treated as potentially exposed wherever a rule keys on
exposure, and MUST NOT be simplified to `NONE`.

Exposure is a property of a **party** with respect to a **question**. The same
artifact may leave one party exposed and another unexposed, which is why
exposure is recorded per party rather than per artifact.

---

## 4. Four Kinds of Independence

### `QROS-INDEP-FOUR-KINDS`

"Independent" names four distinct properties. They MUST NOT be collapsed into a
single claim, because each is established differently and each supports
different conclusions.

| Kind | Carried by | Established by | Supports the claim that |
|---|---|---|---|
| `CONTEXT_INDEPENDENCE` | the working session | a fresh session that did not inherit the producer's context | the reviewer did not inherit the producer's framing |
| `AUTHORSHIP_INDEPENDENCE` | the artifact | a recorded contribution role on the artifact | this party did not shape this artifact |
| `MODEL_DIVERSITY` | the model or model family | a different family from the producer's | a second analytical style examined the work |
| `EMPIRICAL_INDEPENDENCE` | the sample | data not used in producing the result | the effect appears in data that did not produce it |

### `QROS-INDEP-CONTEXT`

`CONTEXT_INDEPENDENCE` requires a working session that did not carry the
producing session's context, framing, or intermediate reasoning. A spawned
agent never has it with respect to its spawner
(`QROS-ROLE-SUBAGENT-NOT-INDEPENDENT`).

### `QROS-INDEP-AUTHORSHIP`

`AUTHORSHIP_INDEPENDENCE` requires that the party did not materially shape the
artifact under review.

A reviewer that identifies ambiguity, an unreachable branch, a scale mismatch,
contradictory rules, or missing power analysis, and asks for justification,
remains authorship-independent. A reviewer becomes a **material contributor**
only by *supplying* an element that is then adopted: a hypothesis, a threshold,
a sample definition, a decision rule, a falsification rule, a promotion
criterion, or a statistical procedure. Useful criticism is not co-authorship.

Where a reviewer's contribution was adopted, the project MUST record that fact
on the artifact and disclose it at any later certification of that artifact
(`QROS-PRESEAL-CONTRIBUTION-RECORDED`).

### `QROS-INDEP-MODEL-DIVERSITY`

`MODEL_DIVERSITY` means a different model family examined the work. It supports
**review diversity only**. It MUST NOT be described as replication, corroboration
of an empirical result, or evidence about the world.

### `QROS-INDEP-EMPIRICAL`

`EMPIRICAL_INDEPENDENCE` requires data that played no part in producing the
result — not in parameter fitting, not in universe selection, not in window
selection, and not in exploration.

### `QROS-INDEP-REPLICATION-REQUIRES-EMPIRICAL`

Only `EMPIRICAL_INDEPENDENCE` supports the word **replication**. A claim that a
result was replicated MUST cite an independent sample. A fresh session, a
different model family, and a different author are each insufficient, alone or
in combination, to support a replication claim.

A related and common error: parameters were not refitted does **not** mean data
was held out. An evaluation that partitions the full sample without excluding
any window from exploration tests stability over time, not out-of-sample
behaviour, and MUST NOT be described as out-of-sample.

### `QROS-INDEP-STATE-PER-DIMENSION`

Independence MUST be stated per dimension and per target, never as a global
property of a reviewer.

A conforming statement names which of the four kinds hold, and with respect to
what: for example, independent of the implementation and of the post-seal
analysis, but not of one threshold in the design. A statement of the form "fully
independent reviewer" is not conforming, because it asserts four properties
without establishing any of them.

---

## 5. Research Lifecycle

### `QROS-LIFECYCLE-STAGES`

The full lifecycle for a preregistered study is:

| Stage | Held by | Produces |
|---|---|---|
| `DESIGN` | `MAIN_AGENT` | question, hypothesis, thresholds, decision rules, draft preregistration |
| `PRE_SEAL_CHALLENGE` | `INDEPENDENT_REVIEWER` | challenge findings against the design, before any outcome exposure |
| `SEAL` | project | the preregistration fixed and recorded (`QROS-PREREG-SEAL-BEFORE-EXPOSURE`) |
| `BUILD` | `MAIN_AGENT` | implementation, tests |
| `MECHANICAL_VERIFY` | deterministic checks | invariants, leakage checks, timing checks, accounting identities, deterministic reproduction |
| `EVIDENCE` | project | the preregistered study is executed |
| `ANALYSIS` | `MAIN_AGENT` | provisional interpretation — never certification |
| `RISK_GATED_AUDIT` | `ARCHITECTURE_REVIEWER` or `INDEPENDENT_REVIEWER` | adversarial examination, **only where risk warrants it** |
| `REPAIR_IF_REQUIRED` | `MAIN_AGENT` | fixes for confirmed defects, each with a regression test and a change label (`QROS-CHANGE-LABELS`) |
| `INDEPENDENT_VERIFICATION` | `INDEPENDENT_REVIEWER` | certification by a party that did not produce the work |
| `OWNER_DECISION` | `OWNER` | the decision the study was run to inform |
| `RECORD` | project | claim, evidence, provenance, limitations, reuse, scope |

### `QROS-LIFECYCLE-TERMINATES`

The lifecycle terminates. A study reaches `RECORD` and stops. Stages MUST NOT
be re-entered merely because further work is imaginable; re-entry requires
either an unresolved blocker (`QROS-BLOCKER-ADMISSION`) or a new question
(`QROS-COMPLETION-STOP-RULE`).

### `QROS-LIFECYCLE-PROPORTIONALITY`

The full lifecycle applies to preregistered studies. It MUST NOT be applied to
every task. Governance cost is justified by consequence: work that cannot
produce a durable claim, cannot expose a reserved sample, and cannot cause an
unsafe action requires no stage beyond ordinary engineering practice.

`RISK_GATED_AUDIT` is optional by default and is invoked only where the risk
warrants it. It is not a mandatory stage.

### `QROS-LIFECYCLE-REDUCED-EXPLORATORY`

`EXPLORATORY` work runs `DESIGN` (lightweight), `BUILD`, `MECHANICAL_VERIFY`,
`EVIDENCE`, `ANALYSIS`, `RECORD`. It omits `SEAL`, `PRE_SEAL_CHALLENGE`,
`RISK_GATED_AUDIT`, and `INDEPENDENT_VERIFICATION`, and correspondingly may emit
only the claims its lane permits (`QROS-AXIS-LANE`).

### `QROS-LIFECYCLE-REDUCED-MEASUREMENT`

`MEASUREMENT` work runs `BUILD`, `MECHANICAL_VERIFY`, `EVIDENCE`, `ANALYSIS`,
`RECORD`. It requires independent verification only where
`QROS-REVIEW-MANDATORY-TRIGGERS` applies. Measurement work MUST still record any
outcome exposure it causes (`QROS-AXIS-OUTCOME-EXPOSURE`).

### `QROS-LIFECYCLE-REDUCED-BUGFIX`

A defect repair runs `BUILD` and `MECHANICAL_VERIFY`, and MUST add a regression
test that fails without the fix. It MUST carry a change label
(`QROS-CHANGE-LABELS`) and MUST propagate to any other result that depends on
the corrected component.

---

## 6. Preregistration and Sealing

### `QROS-PREREG-CONTENT`

A preregistration MUST state, before any exposure to the outcome:

1. **Research question** — what is being asked, unambiguously.
2. **Hypothesis** — the claim under test and the mechanism proposed for it.
3. **Decision-relevant threshold** — where a decision depends on magnitude, the
   smallest effect that would change the decision, expressed on the **same
   metric and the same scale** as the rule that reads it
   (`QROS-PREREG-METRIC-SCALE-CONSISTENCY`).
4. **Metric and scale** — the quantity computed, its units, and its
   transformation.
5. **Sample definition** — what data is in scope, over what period, with what
   inclusion rules; and which portion, if any, is reserved.
6. **Decision rules** — how the result maps to a conclusion, evaluated in a
   stated order.
7. **Kill conditions** — what result would end the line of investigation
   (`QROS-PREREG-KILL-REACHABILITY`).
8. **Trial-accounting plan** — the number of planned comparisons and any
   multiple-comparison treatment (`QROS-AXIS-TRIAL-ACCOUNTING`).
9. **Known reuse and exposure** — any prior exposure of the sample, declared
   under `QROS-REUSE-DECLARE-BEFORE-USE`.
10. **Lineage and amendments** — the record required by `QROS-PREREG-LINEAGE`.

### `QROS-PREREG-SEAL-BEFORE-EXPOSURE`

The preregistration MUST be sealed before any party involved in the study is
exposed to the target metric. Sealing means the content is fixed and recorded
such that later modification is detectable and any modification is itself
recorded.

A preregistration written or amended after outcome exposure is not a
preregistration, and results obtained under it MUST NOT be recorded as
confirmatory.

### `QROS-PREREG-KILL-REACHABILITY`

Where a preregistration states a kill condition or any branch whose function is
to end or redirect the investigation, the project MUST demonstrate, from inputs
available in advance, that the branch is **reachable** — that some realistic
value of the measured quantity would trigger it.

A branch that no attainable measurement can reach provides no protection while
appearing to. Where a kill region is bounded on both sides, the condition MUST
be written as a bounded region rather than as a one-sided threshold.

### `QROS-PREREG-METRIC-SCALE-CONSISTENCY`

A threshold MUST be expressed on the same metric and the same scale as the rule
that evaluates it. Where a decision rule reads one quantity and the stated
threshold describes another — a different transformation, a different
normalisation, a different horizon — the design does not determine an outcome
and MUST NOT be sealed.

### `QROS-PREREG-RULE-DOMAIN-ANALYSIS`

Before sealing, the project MUST evaluate each decision rule at the extremes of
its input's attainable domain, and record the result. This analysis identifies
rules that are contradictory, jointly unsatisfiable, or degenerate at the
boundary — conditions that are invisible when a rule is inspected only at
typical values.

### `QROS-PREREG-RECHECK-AFTER-AMENDMENT`

`QROS-PREREG-KILL-REACHABILITY`, `QROS-PREREG-METRIC-SCALE-CONSISTENCY` and
`QROS-PREREG-RULE-DOMAIN-ANALYSIS` MUST be re-run after every amendment.
Repairing one rule defect can introduce another, and an amendment checked only
at the site it changed is not checked.

### `QROS-PREREG-LINEAGE`

A preregistration MUST carry a lineage record: its version, each amendment with
its date and rationale, the pre-amendment content or a digest of it, and — for
any element supplied by a reviewer and adopted — the attribution required by
`QROS-PRESEAL-CONTRIBUTION-RECORDED`.

Amendments made **before** sealing are design evolution and belong in this
record. Departures from an **already-sealed** contract are a different thing:
they are governed by `QROS-CHANGE-LABELS` and MUST NOT be recorded as
pre-seal amendments.

### `QROS-PRESEAL-CHALLENGE-SCOPE`

`PRE_SEAL_CHALLENGE` challenges a design; it does not author one. The reviewer
examines the design for: adequacy of the sample to detect the stated effect;
threshold and decision-rule scale consistency; kill-branch reachability; rule
behaviour at the domain's extremes; contradictory or jointly unsatisfiable
rules; ambiguous hypotheses; undeclared researcher degrees of freedom;
unaddressed multiple-comparison exposure; invalid sample assumptions; and
whether the design can answer the stated question at all.

The reviewer MUST NOT rewrite the preregistration.

### `QROS-PRESEAL-CONTRIBUTION-RECORDED`

Where a `PRE_SEAL_CHALLENGE` reviewer supplied a design element that was adopted
into the sealed artifact, the project MUST record the contribution on the
preregistration before sealing, and MUST disclose it at
`INDEPENDENT_VERIFICATION`.

The consequence is scoped, and MUST be stated as such under
`QROS-INDEP-STATE-PER-DIMENSION`: a later fresh reviewer retains
`CONTEXT_INDEPENDENCE` and `AUTHORSHIP_INDEPENDENCE` with respect to the
implementation and the analysis. What is absent is `MODEL_DIVERSITY` with
respect to **those specific adopted elements**, which therefore MUST NOT rest on
same-family review as their sole independent certification.

---

## 7. Evidence Model

### `QROS-EVIDENCE-SEPARATION`

Three kinds of support for a claim are distinct and MUST NOT be substituted for
one another:

| Kind | What it is | What it establishes |
|---|---|---|
| `BUILDER_CLAIM` | an assertion by the party that produced the work | what the producer believes or intends |
| `MECHANICAL_EVIDENCE` | the output of a deterministic check that could have failed | that a specific stated property holds |
| `INDEPENDENT_VERIFICATION` | certification by a party that did not produce the work | that a party without the producer's stake reached the same conclusion |

### `QROS-EVIDENCE-NOT-INTERCHANGEABLE`

A record MUST state which of the three kinds supports each claim. A
`BUILDER_CLAIM` MUST NOT be recorded as `MECHANICAL_EVIDENCE`, and neither MUST
be recorded as `INDEPENDENT_VERIFICATION`.

Passing tests are `MECHANICAL_EVIDENCE` for the properties those tests assert,
and for nothing else. A test suite's aggregate result is not evidence for a
property no test examines.

### `QROS-EVIDENCE-SELF-DESCRIPTION-NOT-PROOF`

A comment, docstring, commit message, variable name, or accompanying document
that agrees with a claim is not evidence for that claim. Self-description is
part of the artifact under examination, not a check on it.

### `QROS-EVIDENCE-SYNTHETIC-VS-REAL`

Evidence from synthetic or simulated data establishes that an implementation
behaves as specified. It does not establish anything about the world.

A result obtained on synthetic data MUST NOT be recorded as evidence for an
empirical claim, and a pipeline validated on synthetic data MUST NOT be
described as having produced a research result.

### `QROS-EVIDENCE-ACCESS-NOT-AUTHORITY`

Authorisation previously granted to access data does not authorise a future
execution, a further access, or a reveal. Data access and execution are separate
grants, and holding the first never implies the second.

Every consequential execution requires its own current authorisation under
`QROS-OWNER-REAL-RUN`, bound to that execution.

### `QROS-EVIDENCE-INFRASTRUCTURE-NOT-RESULT`

That a pipeline is built, tested, and ready to run is a fact about
infrastructure. It is not a research result, and MUST NOT be recorded, reported,
or presented as progress toward one.

### `QROS-EVIDENCE-CODE-QUALITY-NOT-AUTHORIZATION`

A favourable verdict on implementation quality does not authorise research
action. Code review and research authorisation are different judgements with
different criteria, and a `PASS` on the former MUST NOT be cited as satisfying a
gate that requires the latter.

### `QROS-EVIDENCE-AGREEMENT-NOT-REPLICATION`

Agreement between reviewers, sessions, or model families is a review outcome. It
MUST NOT be recorded as replication, as corroboration of an empirical result, or
as evidence about the world. Replication requires
`QROS-INDEP-REPLICATION-REQUIRES-EMPIRICAL`.

---

## 8. Sample Reuse and Trial Accounting

### `QROS-REUSE-EXPOSURE-VS-TRIALS`

Exposure and trial accounting are separate records answering separate questions:

- **Exposure** records what a party has observed about an outcome
  (`QROS-AXIS-OUTCOME-EXPOSURE`).
- **Trial accounting** records how much selection freedom a sample has absorbed
  (`QROS-AXIS-TRIAL-ACCOUNTING`).

Work can cause exposure without incrementing any trial counter, and can consume
selection freedom without any party observing a final outcome. A project MUST
maintain both records, and MUST NOT derive either from the other.

### `QROS-REUSE-DECLARE-BEFORE-USE`

Before consequential use of a sample that has already been used to search,
select, fit, or evaluate, the project MUST declare the reuse in advance,
stating: which sample, what prior use it has absorbed, what the current use will
do with it, and why the reuse is acceptable for the claim being made.

The declaration MUST also state what the current use will **not** do — which
statistics will not be computed, which comparisons will not be made — because
the scope of an examination determines how much freedom it consumes.

Silent reuse of a previously searched sample MUST NOT occur. Discovering
undeclared reuse after the fact is a `DATA_IDENTITY_OR_PROVENANCE` threat
(`QROS-THREAT-VOCABULARY`).

### `QROS-REUSE-NEW-SEAL-NO-REFRESH`

A new preregistration does not restore the freshness of a sample. Sealing a new
contract fixes what will be done next; it does not undo what a sample has
already absorbed. Prior exposure and prior trials carry forward across
preregistrations, projects, and personnel.

### `QROS-REUSE-NEGATIVE-CONSUMES`

Work that produces a negative result consumes selection freedom exactly as work
that produces a positive one does, and MUST be recorded in trial accounting on
the same terms.

Negative results are also research information: they disclose what was tested,
on which sample, under what design, and that the sample is correspondingly
depleted. A project MUST treat a negative finding as a recorded research output
subject to the same provenance, retention, and disclosure controls as a
favourable one.

---

## 9. Threat Vocabulary

### `QROS-THREAT-VOCABULARY`

QROS defines six threat classes. They are the closed vocabulary used by the
blocker model (`QROS-BLOCKER-ADMISSION`) and the reviewer model
(`QROS-REVIEW-BLOCKING-REQUIREMENTS`).

| Class | Covers |
|---|---|
| `RESEARCH_CORRECTNESS` | the result does not follow from the evidence: a defect in method, computation, inference, or interpretation |
| `REPRODUCIBILITY` | the result cannot be reproduced from recorded inputs, code, and procedure |
| `DATA_IDENTITY_OR_PROVENANCE` | the data is not what it is recorded to be: wrong source, wrong period, undisclosed transformation, undeclared reuse, unresolved lineage |
| `INDEPENDENCE_OR_BLINDNESS` | a certification is not independent, or a party judged information it should not have held |
| `CONSEQUENTIAL_EXECUTION_SAFETY` | an action with irreversible or external effect may occur without its authorisation, or outside its authorised bounds |
| `METHODOLOGY_OR_SCOPE_INTEGRITY` | the question, decision rule, or scope changed without the change being classified and recorded |

This vocabulary is **closed**. A project MUST NOT add, remove, merge, or rename
a class. Every blocking finding and every blocker row names exactly one of the
six.

A concern that does not fit one of them is not thereby unimportant — it is
non-blocking (`QROS-BLOCKER-ADMISSION`), and belongs in backlog.

---

## 10. Reviewer Model

### `QROS-REVIEW-MANDATORY-TRIGGERS`

Independent review is REQUIRED for work that is **consequential**. The following
list is the **baseline**: the minimum that every conforming project enforces.

1. a preregistration, before it is sealed;
2. the final result that a decision rule reads, before it is revealed to the
   decision-maker;
3. output of an execution against real data whose result will be recorded as
   evidence;
4. a change to a gate, authorisation path, or code on which a leakage or safety
   property depends;
5. a case where the producer's account and the mechanical evidence disagree;
6. an action listed in `QROS-OWNER-GATE-LIST`, where the `OWNER` requires review
   before deciding.

A project MAY declare additional mandatory triggers under
`QROS-CONFIG-TIGHTEN-ONLY`. It MUST NOT remove, narrow, or condition a baseline
trigger.

Independent review is required where, and only where, one of the following
applies: a baseline trigger above; an additional trigger validly configured by
the project; or an explicit request by the `OWNER`. Outside those cases it is
not required, and a project MUST NOT initiate it automatically
(`QROS-COMPLETION-NO-AUTOMATIC-LOOPS`).

### `QROS-REVIEW-NOT-ROUTINE`

Independent review is NOT required for ordinary maintenance, refactoring,
documentation edits, record appends, formatting, naming, vocabulary questions,
or the review of a review absent evidence of contamination.

Dispatching review for such work consumes the budget that
`QROS-REVIEW-ROUND-BUDGET` reserves for consequential disagreement, and a
project that does so routinely will exhaust its capacity for review where review
matters.

### `QROS-REVIEW-VERDICTS`

A review returns exactly one verdict:

| Verdict | Meaning | Effect |
|---|---|---|
| `PASS` | no finding that requires action before proceeding | work proceeds |
| `PASS_WITH_BACKLOG` | findings exist; none is blocking | work proceeds; findings become backlog rows (`QROS-BLOCKER-CLASSES`) |
| `HOLD` | at least one blocking finding | work does not proceed on the affected path |

A review that cannot substantiate a blocking finding under
`QROS-REVIEW-BLOCKING-REQUIREMENTS` MUST return `PASS_WITH_BACKLOG` rather than
`HOLD`.

### `QROS-REVIEW-BLOCKING-REQUIREMENTS`

A blocking finding MUST state all four of:

1. **Threat class** — exactly one class from `QROS-THREAT-VOCABULARY`.
2. **Concrete failure path** — the specific sequence by which the defect
   produces a wrong, irreproducible, or unsafe outcome on the current or next
   stage. A statement that a defect is undesirable is not a failure path.
3. **Evidence class** — one of `QROS-REVIEW-EVIDENCE-CLASSES`.
4. **Smallest relevant scope** — the narrowest artifact, component, or claim
   affected, and the smallest change or test that would settle it.

A finding that does not state all four is non-blocking by construction.

### `QROS-REVIEW-EVIDENCE-CLASSES`

| Class | Meaning |
|---|---|
| `REPRODUCED` | the reviewer independently produced the failure or the discrepancy |
| `REASONED` | the reviewer constructed a specific counterexample or derivation from the artifact, without executing it |
| `SELF_REPORTED` | the finding restates something the producer already reported |

### `QROS-REVIEW-SELF-REPORTED-NOT-BLOCKING`

A `SELF_REPORTED` finding MUST NOT be blocking on its own. Restating the
producer's account adds no independent information, and a review that blocks on
it has certified nothing.

`REPRODUCED` and `REASONED` findings MAY be blocking. A well-formed `REASONED`
finding — one naming a threat and a concrete failure path — is blocking on the
same terms as a reproduced one; requiring execution before a design defect may
be raised would exclude precisely the defects that execution cannot reveal.

### `QROS-REVIEW-CLASSIFICATION-AUTHORITY`

The reviewer classifies its own findings. The producing party MUST NOT
reclassify a reviewer's finding, downgrade it, or narrow its scope.

Where the producer disputes a classification, the dispute is settled by the
smallest test that decides it. Where no such test can be written, it is settled
by the `OWNER`.

### `QROS-REVIEW-ROUND-BUDGET`

Each issue lineage — one finding and its successive repairs — receives a finite
review budget, declared in project configuration
(`QROS-CONFIG-CONFIGURABLE`). The budget is counted continuously across
renames, restatements, stage changes, and reopenings of the same underlying
issue, so that an issue cannot acquire fresh budget by being relabelled.

A round is consumed only by a review that was actually dispatched and returned a
verdict. Preparing a review that is never dispatched, or one that fails in
transport (`QROS-BLOCKER-CLASSES`), consumes no round.

### `QROS-REVIEW-ROUND-SCOPE`

A review after a repair covers the repair **and** an impact scope declared by
the producing party. The reviewer MAY contest the declared scope; a scope the
reviewer rejects as too narrow is itself a finding.

Review after repair MUST NOT be limited to the changed lines, because the defect
being examined is whether the repair is adequate and complete, not whether the
edit was applied.

### `QROS-REVIEW-ESCALATION-ON-EXHAUSTION`

When an issue lineage exhausts its review budget with the disagreement
unresolved, the matter MUST escalate to the `OWNER`. It MUST NOT generate
further review rounds.

Escalation does not decide the question in either party's favour. It records
that the review mechanism has reached its limit and that a human decision is
required. Where the `OWNER` accepts work with residual findings outstanding, the
record MUST state that the findings remain open and were accepted, rather than
that they were resolved.

---

## 11. Blindness and Transport

### `QROS-BLIND-LEVELS`

Two blindness levels are defined:

| Level | The reviewer does not hold |
|---|---|
| `CLAIM_BLIND` | the producer's claims, conclusions, or reported values for the artifact under review |
| `OUTCOME_BLIND` | in addition, any information about the outcome of the research question |

`OUTCOME_BLIND` is required where the reviewer's task is to independently
produce a quantity that will then be compared with the producer's. `CLAIM_BLIND`
is sufficient where the task is to verify that a recorded artifact is what it is
recorded to be.

### `QROS-BLIND-IS-TRANSPORT`

Blindness is a property of **what information reaches a party, and when**. It is
not a property of a location, a directory, an instruction, or an intention.

A reviewer instructed not to read certain material, but able to reach it, is not
blind — the instruction constrains conduct, not information flow.

What defeats blindness is therefore **technical reachability**, not
co-location. A reviewer is not blind if outcome-bearing material is reachable
from the review environment without an enforced access boundary. That such
material exists somewhere in a larger system does not by itself defeat
blindness, provided an effective boundary stands between it and the review
environment.

Blindness MUST be established by a **separately constructed evidence surface**:
an evidence set built for the review, outside the working environment that holds
the material the reviewer must not reach, whose contents are enumerated in
advance and mechanically bounded (`QROS-BLIND-PRE-FREEZE-SET`).

This is the mechanism, not one option among several. A review conducted inside
the environment that holds outcome-bearing material is not blind, however that
environment is arranged.

An instruction, a convention, a filename, a directory name, or a voluntary
promise is never sufficient, alone or in combination, because none of them
constrains what is reachable.

### `QROS-BLIND-PRE-FREEZE-SET`

The **pre-freeze set** is the exhaustive collection of material a reviewer may
access before it commits to its result. It MUST be:

- **enumerated in advance** — a closed list, with a digest for each item;
- **verified on receipt** — the reviewer recomputes each digest before
  substantive work, and a mismatch is a stop condition
  (`QROS-BLIND-EXPOSURE-RESPONSE`);
- **sufficient** — containing everything a mandatory check requires.

For a verification of artifact identity, the pre-freeze set contains the
artifact, its sealed inputs, the code at the authorised identity, and the
**verification brief** — the document stating what is to be recomputed, from
which inputs, and under which matching rules
(`QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE`).
For an `OUTCOME_BLIND` verification it additionally contains the sealed
preregistration with its lineage and the pre-seal challenge record — both of
which precede any outcome and so do not compromise blindness.

Where a mandatory check cannot be completed from the pre-freeze set, the
reviewer MUST stop and report the evidence surface as insufficient, rather than
seek the missing material. Seeking it destroys the blindness the surface exists
to establish.

### `QROS-BLIND-FREEZE-POINT`

The **freeze point** is the moment the reviewer records its own result and fixes
it against later modification, before receiving any comparand.

The reviewer MUST record its result, produce a digest of it, and declare the
freeze before post-freeze material is delivered. A result produced after seeing
the producer's result is not an independent result, whatever the reviewer's
intent.

### `QROS-BLIND-POST-FREEZE-COMPARANDS`

**Post-freeze comparands** are the producer's claims, recorded values, and prior
certifications. They are delivered only after the freeze is declared, and are
compared against the frozen result.

The frozen result MUST NOT change after the freeze. Where comparison reveals a
discrepancy, the discrepancy is the finding; revising the frozen result to match
is prohibited.

From the moment comparands are delivered, the reviewer is outcome-exposed with
respect to that question, and the project MUST record that exposure
(`QROS-AXIS-OUTCOME-EXPOSURE`).

### `QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE`

Any matching or judgement rule used to assess an artifact MUST be fixed, in
writing, before the assessing party is exposed to the information that rule
judges. This is the central invariant of blind review.

A rule fixed afterwards can be shaped, consciously or not, by the values it will
be applied to. Where such a rule was not fixed in advance, the assessment MUST
NOT be described as blind, whatever process was otherwise followed.

### `QROS-BLIND-BYTE-IDENTITY-NO-JUDGMENT`

A comparison that admits no judgement — exact equality of content, or equality
of a cryptographic digest — may be performed at any time without affecting
blindness, because there is no discretion for exposure to influence.

Every comparison that does admit judgement — a tolerance, a subset selection, a
choice of which cases apply, a decision about what counts as materially the same
— MUST be fixed in advance under `QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE`.

### `QROS-BLIND-EXPOSURE-RESPONSE`

Where a reviewer is exposed, before its freeze point, to material outside the
pre-freeze set, it MUST stop immediately, report the exposure and its extent,
and MUST NOT continue the review.

The project MUST record the exposure, and MUST discard results produced after
it. A replacement review MUST use a newly constructed evidence surface and a
party not exposed. Repeated exposure on the same target is an
`INDEPENDENCE_OR_BLINDNESS` threat and MUST escalate to the `OWNER` rather than
prompting further attempts.

---

## 12. Blocker Model

### `QROS-BLOCKER-SINGLE-SET`

A project MUST maintain exactly one set of current blockers. Where more than one
list of outstanding work exists, no list is authoritative, and the project
cannot determine whether it is free to proceed.

Other lists MAY exist for planning, but MUST NOT be a source of blocking
authority.

### `QROS-BLOCKER-ADMISSION`

An item is admitted to the blocker set only if it states both:

1. exactly one threat class from `QROS-THREAT-VOCABULARY`; and
2. a concrete failure path on the **current or next** stage.

Everything else is `NON_BLOCKING_BACKLOG`. Specifically not admissible: a
cleaner design is imaginable; a stronger general safeguard could exist; further
review would add confidence; a document is inconsistent; a defect exists on a
path this project will not take; a guard protecting a guard is missing.

Each blocker row MUST also state the evidence that would clear it, so that the
row has a defined exit.

### `QROS-BLOCKER-CLASSES`

Five classes of impediment are distinguished. Only the first holds a project.

| Class | Definition | Holds the project |
|---|---|---|
| `CURRENT_PATH_BLOCKER` | satisfies `QROS-BLOCKER-ADMISSION` | **yes** |
| `NON_BLOCKING_BACKLOG` | a recorded item with no current-path failure path | no |
| `TRANSPORT_OR_PACKAGING_FAILURE` | the evidence surface, verification brief, digests, or delivery was defective | no — but leaves the gate unsatisfied |
| `REVIEWER_ELIGIBILITY_OR_PROCEDURAL_FAILURE` | the reviewing party was exposed, ineligible, or never dispatched | no — but leaves the gate unsatisfied |
| `ARCHITECTURE_LEVEL_BLOCKER` | the design approach itself is unresolved and no bounded implementation path can be derived | **yes**, and only this class may escalate under `QROS-ROLE-ARCHITECTURE-ESCALATION-BOUNDED` |

### `QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION`

A `TRANSPORT_OR_PACKAGING_FAILURE` or a
`REVIEWER_ELIGIBILITY_OR_PROCEDURAL_FAILURE` leaves a required gate
**unsatisfied** without establishing any defect in the work under review.

These MUST NOT be recorded as findings against the implementation, MUST NOT
consume a review round (`QROS-REVIEW-ROUND-BUDGET`), and MUST NOT be cited as
evidence that the work is defective. The correct response is to repair the
delivery and dispatch again; the gate remains unsatisfied until a valid review
occurs.

Conflating these with implementation defects produces two distinct errors: it
records defects that were never demonstrated, and it exhausts review budget on
failures that no repair to the work could fix.

### `QROS-BLOCKER-CLOSED-STAYS-CLOSED`

A closed item stays closed. Reopening REQUIRES new, concrete evidence of a
failure on the current path in exactly one threat class from
`QROS-THREAT-VOCABULARY`.

None of the following reopens anything: a better approach has become apparent;
a stronger safeguard is conceivable; another reviewer would add reassurance;
historical wording could be improved; the same concern is restated more
forcefully.

### `QROS-BLOCKER-EXPIRY`

A blocker row MAY carry an expiry. At expiry the only permitted outcomes are:
evidence that clears the row; one extension with a written reason; or an `OWNER`
decision.

A party MAY downgrade to `NON_BLOCKING_BACKLOG` only a row it opened itself and
whose failure path was never `REPRODUCED`. A row opened by a reviewer, or one
whose failure path was reproduced, leaves the blocker set only by clearing
evidence or by `OWNER` decision.

---

## 13. Completion-First Progression

### `QROS-COMPLETION-PROGRESSION`

If the current research question can be answered correctly and reproducibly, and
no unresolved `CURRENT_PATH_BLOCKER` threatens that answer, the project
proceeds to the next stage — **even when non-blocking backlog remains
outstanding**.

This rule does not waive any mandatory gate. `QROS-OWNER-GATE-LIST` and
`QROS-REVIEW-MANDATORY-TRIGGERS` apply unchanged.

### `QROS-COMPLETION-NO-AUTOMATIC-LOOPS`

A project MUST NOT run automatic cycles of repair, review, further repair, and
further review.

A review occurs because a rule requires it (`QROS-REVIEW-MANDATORY-TRIGGERS`) or
because the `OWNER` requests it. A review MUST NOT be initiated as reassurance
following ordinary validation, nor to achieve completeness for its own sake.

### `QROS-COMPLETION-NO-SPECULATIVE-BLOCKER`

A blocker MUST NOT be created on the grounds that an improvement is imaginable.
A cleaner architecture, a more general safeguard, or the observation that
additional review would increase confidence are not blockers, and admitting them
as such removes the distinction `QROS-BLOCKER-ADMISSION` exists to draw.

### `QROS-COMPLETION-STOP-RULE`

Once the preregistered question is answered, investigation of that question
stops. The project MUST NOT proceed to examine further parameters, universes,
thresholds, horizons, or variants.

Further investigation REQUIRES a new question, extension, or replication that is
scientifically justified and separately preregistered, with any sample reuse
declared in advance under `QROS-REUSE-DECLARE-BEFORE-USE`.

This rule exists because unbounded post-hoc search on an answered question is
indistinguishable, in its effect on the evidence, from selecting a favourable
result.

---

## 14. Owner Gates

### `QROS-OWNER-GATE-LIST`

The following actions are reserved to the `OWNER`. No agent may perform or
authorise them on its own initiative, under any instruction originating below
`QROS-AUTHORITY-PRECEDENCE` rank 1:

| Identifier | Reserved action |
|---|---|
| `QROS-OWNER-REAL-RUN` | execution against real data, or data access beyond an existing grant |
| `QROS-OWNER-REVEAL` | disclosure of a result to a party the project has deliberately kept unexposed |
| `QROS-OWNER-DISPOSITION` | promotion, falsification, or retirement of a research line, where consequential |
| `QROS-OWNER-METHODOLOGY-CHANGE` | a material change to methodology or scope: sample definition, labels, cost model, missing-data policy, primary metric, or decision rule |
| `QROS-OWNER-PUBLIC-RELEASE` | publication or external disclosure of any project material |
| `QROS-OWNER-DESTRUCTIVE-MUTATION` | irreversible or shared-history mutation, including deletion of records, rewriting shared history, and mutation of append-only records |

This list is **closed**. A project MUST NOT add, remove, or rename a gate.

**Scope of `QROS-OWNER-REAL-RUN` — authorisation is per execution.** Each
consequential execution against real data REQUIRES its own explicit and current
`OWNER` authorisation, bound to that execution's identity. One authorisation
covers one execution. A further execution REQUIRES a further authorisation, even
where nothing about the work has changed.

An authorisation MUST record what identifies the execution it authorises: the
code and specification identity it runs at, the identity of the data it reads,
and the purpose it serves. Before the execution begins, those identities MUST be
re-verified against the authorisation; a mismatch is a refusal, not a warning.

An authorisation is **current** only until it is used, superseded, or revoked.
The `OWNER` MAY revoke an unused authorisation at any time. An authorisation
that has been used, or whose recorded identities no longer match, authorises
nothing further.

An agent MUST NOT reuse an authorisation for a second execution, widen its
recorded scope, or infer coverage it does not state. Where coverage is unclear,
the restrictive reading applies and the matter goes to the `OWNER`.

### `QROS-OWNER-AUDIT-NOT-EXECUTION`

A party operating under an instruction to audit, review, analyse, plan, or
propose MUST NOT escalate into execution.

Producing a recommendation, however well supported, does not authorise acting on
it. Mutating governance records, specifications, schemas, validators,
preregistrations, seals, or verdicts REQUIRES a subsequent and explicit
authorisation naming what may be changed. Where write permission is ambiguous,
the restrictive reading applies and the party MUST stop and ask.

---

## 15. State and Records

### `QROS-STATE-CURRENT-ARTIFACT`

A project MUST maintain exactly one **current-state artifact** that answers, on
one page: what stage the work is in; what question is being answered; what is
blocking; what is deferred; what evidence remains outstanding; what would
terminate the stage; and who holds authority to continue.

It is rewritten in place as the project advances. Its history lives in version
control, not in the artifact.

### `QROS-STATE-OUTCOME-CLEAN`

The current-state artifact MUST be free of outcome information: it MUST NOT
restate a verdict, a decision-relevant value, an effect size, or an exposure
count.

This constraint exists so that a party under `OUTCOME_BLIND` obligations can
read the project's current state without becoming exposed. An artifact that
cannot be read by such a party is unusable at precisely the moments blindness
matters most.

### `QROS-STATE-BLOCKER-ARTIFACT`

A project MUST maintain exactly one artifact holding the current blocker set and
the non-blocking backlog, governed by `QROS-BLOCKER-SINGLE-SET` and
`QROS-BLOCKER-ADMISSION`.

Rows are closed rather than deleted, and a closed row retains the evidence that
closed it.

### `QROS-RECORD-DECISION-LOG-APPEND-ONLY`

A project MUST maintain one append-only decision record containing every `OWNER`
decision and every review verdict.

Entries MUST NOT be edited, reordered, or removed. A correction is a new entry
citing the entry it corrects. A verdict recorded as `HOLD` that was later
resolved MUST remain recorded as `HOLD`, with the resolution as a subsequent
entry — rewriting it as `PASS` destroys the record of what the review actually
found.

### `QROS-RECORD-CURRENT-VS-HISTORICAL`

Current state and historical record are distinct artifact classes with opposite
mutation rules, and MUST NOT be merged.

Current state is rewritten and answers "where are we now". The historical record
is appended and answers "what happened, and when was it decided". An artifact
that attempts both loses the first to clutter and the second to revision.

### `QROS-RECORD-DURABLE-NOT-TRANSCRIPT`

A conversational transcript is not durable state. Where the output of a stage is
required by a later stage, it MUST be written to a durable, named location, and
the later stage MUST verify that the content is present before proceeding.

A later stage MUST NOT accept a summary of a required artifact in place of the
artifact. Recording the location in advance — as part of dispatching the work —
is the mechanism that makes this checkable rather than aspirational.

---

## 16. Change Control

### `QROS-CHANGE-LABELS`

Every change made after a preregistration is sealed MUST carry exactly one
label:

| Label | Seal | Preregistration | Prior evidence | Lineage |
|---|---|---|---|---|
| `IMPLEMENTATION_FIX` | preserved | unchanged | affected results rerun; unaffected stand | unchanged |
| `DATA_FIX` | preserved | unchanged | everything touching the corrected path rerun | unchanged |
| `ANALYSIS_EXTENSION` | preserved | unchanged | stands; the extension is secondary and non-confirmatory | unchanged |
| `METHODOLOGY_CHANGE` | new version | amended, prior content preserved | prior primary results become historical | versioned |
| `HYPOTHESIS_CHANGE` | new seal | new preregistration | prior evidence does not transfer | new lineage, linked to the prior one |

`METHODOLOGY_CHANGE` and `HYPOTHESIS_CHANGE` are reserved to the `OWNER`
(`QROS-OWNER-METHODOLOGY-CHANGE`). A new seal never restores sample freshness
(`QROS-REUSE-NEW-SEAL-NO-REFRESH`).

### `QROS-CHANGE-CLASSIFY-BEFORE-APPLY`

The label MUST be assigned and recorded before the change is applied, and MUST
state the evidence for the classification.

An `IMPLEMENTATION_FIX` REQUIRES identifying the sealed requirement the code
failed to meet. Where the sealed rule is itself ambiguous, absent, or wrong, the
change is a `METHODOLOGY_CHANGE`, not a fix — the code was not violating a
requirement, because no unambiguous requirement existed.

### `QROS-CHANGE-FIX-NOT-METHODOLOGY`

A defect repair MUST NOT alter the research question, the decision rule, the
threshold, the sample definition, or the metric.

A change that does any of these is a `METHODOLOGY_CHANGE` or a
`HYPOTHESIS_CHANGE` regardless of how it is described, how small the edit is, or
whether it was discovered while fixing a genuine defect. Continuing under the
original preregistration after such a change misrepresents post-hoc choices as
preregistered ones.

---

## 17. Machine Checks Before Model Checks

### `QROS-CHECK-MACHINE-BEFORE-MODEL`

Where a deterministic check can reject an artifact, it MUST be run before
independent review of that artifact is dispatched.

Review capacity is finite and reserved by `QROS-REVIEW-ROUND-BUDGET` for
judgements that require judgement. Spending it on defects a validator would have
caught reduces the capacity available for defects only a reviewer can find.

### `QROS-CHECK-NON-VACUOUS`

Every governance check MUST be demonstrably capable of failing. A project MUST
be able to show, for each such check, a condition under which it fails — by a
deliberate fault, a fixture, or a recorded historical failure.

A check that cannot be shown to fail is not established as protection,
regardless of how long it has passed. This applies with particular force to
checks whose subject has moved: a check that examines a location nothing occupies
any more passes continuously while protecting nothing.

A check MUST assert the property of interest rather than a proxy that correlates
with it. Where the property is a runtime behaviour, a check over static structure
does not establish it, because the set of structures exhibiting the behaviour is
generally not enumerable.

---

## 18. Conformance

### `QROS-CONFORMANCE-SELF-DECLARED`

A project conforms when it follows the rules in this specification. There are no
conformance levels, tiers, profiles, or editions: the rules apply as written, and
a rule that is conditional says so at its own site — `QROS-LIFECYCLE-PROPORTIONALITY`
scales governance to consequence, and `QROS-CHECK-MACHINE-BEFORE-MODEL` applies
wherever a deterministic check exists that can reject the artifact.

Conformance is self-declared. QROS certifies nothing, issues no attestation, and
confers no assurance about any project's results.

A project claiming conformance SHOULD state which requirements it does not meet.
A partial claim that names its gaps is more useful than an unqualified one.

### `QROS-CONFORMANCE-PUBLICATION-ASSURANCE`

Where a project publishes material derived from work that also contains
non-public information, it MUST operate two separate checks, and MUST NOT
conflate them:

| Check | Contents | Where it lives |
|---|---|---|
| **Generic disclosure check** | patterns that are sensitive by shape rather than by identity: absolute filesystem paths, address-shaped strings, identifier-shaped strings, credential and key patterns, committed binary or data artifacts, dependencies resolving outside the published tree, digests committed where none belongs | published with the project |
| **Project-specific disclosure audit** | the project's own list of names, identifiers, and terms that must not appear | **retained privately and never published** |

The reason for the separation is that a published list of forbidden terms
discloses exactly the terms it protects. A project MUST NOT publish its
project-specific audit list, and MUST NOT embed its entries in any published
check, test fixture, or documentation.

A published artifact MUST additionally be free of ancestry that carries
non-public content: it MUST NOT be derived from a filtered copy of a
non-public history, MUST NOT retain non-public objects in its history, and MUST
NOT depend on a non-public source at build or run time. An ordinary development
history of multiple public-safe revisions is unaffected by this requirement.

---

## 19. Configuration

### `QROS-CONFIG-CONFIGURABLE`

A project MAY configure:

| Setting | Notes |
|---|---|
| Role bindings | which concrete party fills each role (`QROS-ROLE-VENDOR-BINDING-IS-CONFIG`) |
| Stage aliases | local names for lifecycle stages, provided the mapping is recorded |
| Review-round budget | the finite budget required by `QROS-REVIEW-ROUND-BUDGET` |
| Exposure and data classes | project-specific classifications of data sensitivity and exposure granularity |
| Trial-accounting rules | the counting and adjustment scheme (`QROS-AXIS-TRIAL-ACCOUNTING`) |
| Artifact formats | the concrete representation of the artifacts required by section 15 |

### `QROS-CONFIG-NON-OVERRIDABLE`

The following MUST NOT be weakened, redefined, or waived by any configuration,
instruction, or local convention:

1. `QROS-ROLE-SELF-CERTIFICATION` — the producer is never the sole certifier.
2. `QROS-ROLE-SUBAGENT-NOT-INDEPENDENT` — a spawned agent is not independent.
3. `QROS-ROLE-OWNER` — the `OWNER` is human, and gates are not self-authorised.
4. `QROS-AXES-NO-INFERENCE` — no axis is inferred from another.
5. `QROS-INDEP-REPLICATION-REQUIRES-EMPIRICAL` — replication requires an
   independent sample.
6. `QROS-EVIDENCE-SEPARATION` — the three kinds of support are not
   interchangeable.
7. `QROS-PREREG-SEAL-BEFORE-EXPOSURE` — sealing precedes exposure.
8. `QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE` — judgement rules are fixed
   before exposure.
9. `QROS-RECORD-DECISION-LOG-APPEND-ONLY` — recorded decisions are not rewritten.
10. `QROS-CHECK-NON-VACUOUS` — a check that cannot fail is not protection.

### `QROS-CONFIG-TIGHTEN-ONLY`

A configuration MAY impose requirements stricter than this specification: more
mandatory review triggers, a smaller review budget, or narrower exposure and
data classes. The threat vocabulary and the `OWNER` gate list are closed and are
not configuration surfaces.

A configuration MUST NOT relax a requirement. In particular, no configuration
may define output of a producing party as independent verification of that
party's own work, whether by redefining the role, by declaring a spawned agent
independent, by treating a `SELF_REPORTED` finding as certification, or by any
other construction that produces the same effect.

---

## Appendix A — Semantic Identifier Index

Identifiers are stable. Sections may be reordered; identifiers do not change.
Where an identifier is retired, it is not reused.

**Purpose** — `QROS-PURPOSE-SCOPE` · `QROS-PURPOSE-NO-ALPHA-CLAIM` ·
`QROS-PURPOSE-MODEL-OUTPUT-NOT-EVIDENCE` · `QROS-PURPOSE-NEGATIVE-RESULTS-VALID` ·
`QROS-PURPOSE-NO-CORRECTNESS-GUARANTEE`

**Authority** — `QROS-AUTHORITY-PRECEDENCE` · `QROS-AUTHORITY-CROSS-SCOPE-CONFLICT`

**Roles** — `QROS-ROLE-OWNER` · `QROS-ROLE-MAIN-AGENT` ·
`QROS-ROLE-INDEPENDENT-REVIEWER` · `QROS-ROLE-ARCHITECTURE-REVIEWER` ·
`QROS-ROLE-ARCHITECTURE-ESCALATION-BOUNDED` · `QROS-ROLE-SELF-CERTIFICATION` ·
`QROS-ROLE-SUBAGENT-NOT-INDEPENDENT` · `QROS-ROLE-SINGLE-ACTIVE-BUILDER` ·
`QROS-ROLE-VENDOR-BINDING-IS-CONFIG`

**Axes** — `QROS-AXES-THREE` · `QROS-AXES-NO-INFERENCE` · `QROS-AXIS-LANE` ·
`QROS-LANE-CLAIM-SCOPE` · `QROS-AXIS-TRIAL-ACCOUNTING` ·
`QROS-AXIS-OUTCOME-EXPOSURE`

**Independence** — `QROS-INDEP-FOUR-KINDS` · `QROS-INDEP-CONTEXT` ·
`QROS-INDEP-AUTHORSHIP` · `QROS-INDEP-MODEL-DIVERSITY` · `QROS-INDEP-EMPIRICAL` ·
`QROS-INDEP-REPLICATION-REQUIRES-EMPIRICAL` · `QROS-INDEP-STATE-PER-DIMENSION`

**Lifecycle** — `QROS-LIFECYCLE-STAGES` · `QROS-LIFECYCLE-TERMINATES` ·
`QROS-LIFECYCLE-PROPORTIONALITY` · `QROS-LIFECYCLE-REDUCED-EXPLORATORY` ·
`QROS-LIFECYCLE-REDUCED-MEASUREMENT` · `QROS-LIFECYCLE-REDUCED-BUGFIX`

**Preregistration** — `QROS-PREREG-CONTENT` · `QROS-PREREG-SEAL-BEFORE-EXPOSURE` ·
`QROS-PREREG-KILL-REACHABILITY` · `QROS-PREREG-METRIC-SCALE-CONSISTENCY` ·
`QROS-PREREG-RULE-DOMAIN-ANALYSIS` · `QROS-PREREG-RECHECK-AFTER-AMENDMENT` ·
`QROS-PREREG-LINEAGE` · `QROS-PRESEAL-CHALLENGE-SCOPE` ·
`QROS-PRESEAL-CONTRIBUTION-RECORDED`

**Evidence** — `QROS-EVIDENCE-SEPARATION` · `QROS-EVIDENCE-NOT-INTERCHANGEABLE` ·
`QROS-EVIDENCE-SELF-DESCRIPTION-NOT-PROOF` · `QROS-EVIDENCE-SYNTHETIC-VS-REAL` ·
`QROS-EVIDENCE-ACCESS-NOT-AUTHORITY` · `QROS-EVIDENCE-INFRASTRUCTURE-NOT-RESULT` ·
`QROS-EVIDENCE-CODE-QUALITY-NOT-AUTHORIZATION` ·
`QROS-EVIDENCE-AGREEMENT-NOT-REPLICATION`

**Reuse** — `QROS-REUSE-EXPOSURE-VS-TRIALS` · `QROS-REUSE-DECLARE-BEFORE-USE` ·
`QROS-REUSE-NEW-SEAL-NO-REFRESH` · `QROS-REUSE-NEGATIVE-CONSUMES`

**Threats** — `QROS-THREAT-VOCABULARY`

**Review** — `QROS-REVIEW-MANDATORY-TRIGGERS` · `QROS-REVIEW-NOT-ROUTINE` ·
`QROS-REVIEW-VERDICTS` · `QROS-REVIEW-BLOCKING-REQUIREMENTS` ·
`QROS-REVIEW-EVIDENCE-CLASSES` · `QROS-REVIEW-SELF-REPORTED-NOT-BLOCKING` ·
`QROS-REVIEW-CLASSIFICATION-AUTHORITY` · `QROS-REVIEW-ROUND-BUDGET` ·
`QROS-REVIEW-ROUND-SCOPE` · `QROS-REVIEW-ESCALATION-ON-EXHAUSTION`

**Blindness** — `QROS-BLIND-LEVELS` · `QROS-BLIND-IS-TRANSPORT` ·
`QROS-BLIND-PRE-FREEZE-SET` · `QROS-BLIND-FREEZE-POINT` ·
`QROS-BLIND-POST-FREEZE-COMPARANDS` ·
`QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE` ·
`QROS-BLIND-BYTE-IDENTITY-NO-JUDGMENT` · `QROS-BLIND-EXPOSURE-RESPONSE`

**Blockers** — `QROS-BLOCKER-SINGLE-SET` · `QROS-BLOCKER-ADMISSION` ·
`QROS-BLOCKER-CLASSES` · `QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION` ·
`QROS-BLOCKER-CLOSED-STAYS-CLOSED` · `QROS-BLOCKER-EXPIRY`

**Completion** — `QROS-COMPLETION-PROGRESSION` ·
`QROS-COMPLETION-NO-AUTOMATIC-LOOPS` · `QROS-COMPLETION-NO-SPECULATIVE-BLOCKER` ·
`QROS-COMPLETION-STOP-RULE`

**Owner gates** — `QROS-OWNER-GATE-LIST` · `QROS-OWNER-REAL-RUN` ·
`QROS-OWNER-REVEAL` · `QROS-OWNER-DISPOSITION` ·
`QROS-OWNER-METHODOLOGY-CHANGE` · `QROS-OWNER-PUBLIC-RELEASE` ·
`QROS-OWNER-DESTRUCTIVE-MUTATION` · `QROS-OWNER-AUDIT-NOT-EXECUTION`

**State and records** — `QROS-STATE-CURRENT-ARTIFACT` · `QROS-STATE-OUTCOME-CLEAN` ·
`QROS-STATE-BLOCKER-ARTIFACT` · `QROS-RECORD-DECISION-LOG-APPEND-ONLY` ·
`QROS-RECORD-CURRENT-VS-HISTORICAL` · `QROS-RECORD-DURABLE-NOT-TRANSCRIPT`

**Change control** — `QROS-CHANGE-LABELS` · `QROS-CHANGE-CLASSIFY-BEFORE-APPLY` ·
`QROS-CHANGE-FIX-NOT-METHODOLOGY`

**Checks** — `QROS-CHECK-MACHINE-BEFORE-MODEL` · `QROS-CHECK-NON-VACUOUS`

**Conformance** — `QROS-CONFORMANCE-SELF-DECLARED` ·
`QROS-CONFORMANCE-PUBLICATION-ASSURANCE`

**Configuration** — `QROS-CONFIG-CONFIGURABLE` · `QROS-CONFIG-NON-OVERRIDABLE` ·
`QROS-CONFIG-TIGHTEN-ONLY`

---

## Specification Change Policy

A change to this specification REQUIRES one of: an observed process failure that
the current rules permitted; a demonstrated defect in a rule as written; or a
material change in the capabilities the specification assumes.

That an additional rule is conceivable is not sufficient reason to add one. A
specification that grows whenever growth is imaginable becomes too expensive to
follow, and a rule that is not followed protects nothing.

Versioning is semantic. A change that makes a conforming project non-conforming
is a major version. A change that adds a requirement a conforming project would
already satisfy is a minor version. Editorial changes are patch versions.
