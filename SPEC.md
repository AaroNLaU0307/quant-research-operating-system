# QROS — Quantitative Research Operating System

**Specification, version 2.0.0**

QROS is a specification for conducting quantitative research with substantial
assistance from artificial-intelligence (AI) agents. Its aim is that the resulting
claims stay reproducible, falsifiable and bounded in cost. It is built to resist two
failure modes:

- **self-certification** — the party that produced a result also attests to it;
- **leakage** — information about an outcome reaches a party whose judgement is
  supposed to be independent of it.

Version 2 replaces version 1's reviewer-dispatch model with three roles (Owner,
Delegate, Builder), acceptance by reproduction, and verdicts computed by a rule sealed
in advance. Retired v1 identifiers are listed in Appendix B.

This document is the **sole normative source** for QROS. Every normative rule appears
here exactly once and carries a stable semantic identifier. *MUST*, *MUST NOT*,
*SHOULD*, *SHOULD NOT* and *MAY* carry their ordinary specification meanings. A rule
without one of those words is a definition. Section numbers are for navigation only.

---

## 0. Purpose and non-goals

### `QROS-PURPOSE-SCOPE`
QROS governs research whose output is a claim about data: a strategy, a factor, a
mechanism or a measurement. It governs how claims are designed, sealed, tested,
accepted and recorded. It does not govern ordinary engineering, which needs only good
practice.

### `QROS-PURPOSE-NO-ALPHA-CLAIM`
Following QROS makes no result profitable, true or publishable. It makes results
**honest about what they are**.

### `QROS-PURPOSE-MODEL-OUTPUT-NOT-EVIDENCE`
Text produced by a model — a summary, a rationale, a docstring, a commit message — is
not evidence for the claim it states.

### `QROS-PURPOSE-NEGATIVE-RESULTS-VALID`
A negative or unresolved result is a legitimate completion, for a single line of work or
for a whole project. Zero candidates worth sealing is a legitimate result of discovery.
No party may treat a negative result as a reason to keep searching the same sample.

### `QROS-PURPOSE-NO-CORRECTNESS-GUARANTEE`
QROS reduces specific, named failure modes (`QROS-THREAT-VOCABULARY`). It does not
guarantee correctness.

### `QROS-PURPOSE-PRIORITIES`
Where rules compete, the order is: correct research, then reproducibility, then
essential safety, then finishing the research, then framework perfection. Governance
exists to protect research; research does not exist to feed governance.

---

## 1. Authority

### `QROS-AUTHORITY-PRECEDENCE`
Highest first:

1. a decision of the `OWNER`, or a decision of the `DELEGATE` within its delegated
   scope (`QROS-GATE-DELEGATED`), or a hard research invariant — a lockbox or one-shot
   holdout, immutable sealed artifacts, run outputs and decision records, declared
   outcome blindness. An `OWNER` decision overrides a `DELEGATE` decision. A
   `DELEGATE` decision never overrides a hard invariant.
2. an active sealed preregistration for the research in hand. It MAY be stricter than
   this specification.
3. this specification.
4. project-local workflow or convenience instructions.
5. tool and model defaults.

### `QROS-AUTHORITY-CROSS-SCOPE-CONFLICT`
A conflict this ordering does not settle MUST be halted and reported to the party
holding the relevant gate. The session that meets it MUST NOT reconcile it.

### `QROS-AUTHORITY-STALE-LOCAL-DOCS`
A project document at rank 4 or 5 cannot revive machinery this specification retires
(Appendix B).

### `QROS-AUTHORITY-STATE-NOT-AUTHORITY`
The current-state artifact (`QROS-STATE-CURRENT-ARTIFACT`) records state, never
authority. A claim in it that contradicts this specification is a defect in the
artifact.

---

## 2. Roles

### `QROS-ROLE-OWNER`
The `OWNER` is a human. The `OWNER` holds the retained gates (`QROS-GATE-OWNER-RETAINED`),
MAY override any delegated decision at any time, and adopts changes to the project's
operating model.

### `QROS-ROLE-DELEGATE`
The `DELEGATE` is a party appointed by the `OWNER`. It MAY be an AI agent running in its
own session. It:

- decides the delegated gates (`QROS-GATE-DELEGATED`), informed by the `BUILDER`;
- accepts work by reproduction (`QROS-ACCEPT-REPRODUCTION-FIRST`);
- routes work;
- designs on request.

It MUST NOT build, MUST NOT write to a project's records, and MUST NOT set a research
agenda. It sends decisions, grants and findings. The role is optional: where no
`DELEGATE` is appointed, the `OWNER` holds the delegated gates.

### `QROS-ROLE-BUILDER`
The `BUILDER` designs, implements, tests, executes authorized runs and keeps the
project's records. It is the only writer of those records. It MAY work autonomously
under a standing authorization (`QROS-ROLE-BUILDER-AUTONOMY`). It MUST NOT authorize
its own run, reveal or verdict, and MUST NOT widen its own grant.

### `QROS-ROLE-BUILDER-AUTONOMY`
Under a standing authorization, the parts of the work are held as follows:

| part of the work | status |
|---|---|
| the research goal and sealed objects | fixed |
| the method | the `BUILDER`'s |
| current hypotheses | open to challenge |
| historical evidence | immutable |
| external and irreversible actions | the `OWNER`'s |

Before seal, the `BUILDER` MAY redesign the method, open or stop branches, and close a
candidate pre-outcome, recording why. After seal, the method moves only through
`QROS-CHANGE-LABELS`. The `BUILDER` returns to the `DELEGATE` when a gate is needed or a
result materially changes understanding — not to report progress.

### `QROS-ROLE-SINGLE-ACTIVE-BUILDER`
Each project has exactly one active `BUILDER`. Two parties building in one repository
corrupt each other's records; a second builder MUST declare a lease or not start.

### `QROS-ROLE-SELF-CERTIFICATION`
No party certifies its own material contribution. Where the `DELEGATE` designed an
element, its acceptance of that element is `REASONED` (`QROS-REVIEW-EVIDENCE-CLASSES`),
never independent.

### `QROS-ROLE-SUBAGENT-NOT-INDEPENDENT`
An agent spawned by a party is never independent of that party. A subagent's output is
its spawner's claim until reproduced.

### `QROS-ROLE-SAME-FAMILY-LIMIT`
Separate sessions of one model family separate context and authorship. That is not
model diversity, and it is never empirical replication. Where `DELEGATE` and `BUILDER`
share a family, the structural substitutes are reproduction-first acceptance and
verdicts computed by a sealed rule (`QROS-VERDICT-RULE-COMPUTED`). The `OWNER` MAY bring
in an external reviewer for a consequential verdict; none is a default role.

### `QROS-ROLE-VENDOR-BINDING-IS-CONFIG`
Which concrete person, model or session fills a role is configuration
(`QROS-CONFIG-CONFIGURABLE`). A record of what actually happened MUST name the concrete
party.

---

## 3. Three orthogonal axes

### `QROS-AXES-THREE`
Every piece of research work carries three independent attributes:

- `LANE` — which claims it may emit;
- `TRIAL_ACCOUNTING` — how it counts against multiple-testing budgets;
- `OUTCOME_EXPOSURE` — which outcomes it has revealed, and to whom.

### `QROS-AXES-NO-INFERENCE`
No axis is inferred from another. For example, a measurement can expose target
performance without moving the trial count; that exposure is recorded anyway.

### `QROS-AXIS-LANE`
`EXPLORATORY | MEASUREMENT | FULL`.

### `QROS-LANE-CLAIM-SCOPE`
Only `FULL` work may emit a confirmatory performance or strategy claim. Lane restricts
performance claims only, not implementation facts.

### `QROS-AXIS-TRIAL-ACCOUNTING`
The project's declared counting scheme — trials, variants, deflation. The count lives
in one declared place. A count that is unknown is recorded as unknown. No adjusted
statistic may be computed against an invented count.

### `QROS-AXIS-OUTCOME-EXPOSURE`
Exposure is recorded per object and per party.

### `QROS-EXPOSURE-MONOTONIC`
Exposure is monotonic:

- once revealed, never regressed;
- a missing record means `UNKNOWN`, never `NONE`;
- failing to record an exposure is itself a defect.

---

## 4. Independence

### `QROS-INDEP-FOUR-KINDS`
Independence has four dimensions, and each MUST be stated separately:

- **CONTEXT** — the party did not see the producer's reasoning;
- **AUTHORSHIP** — the party did not contribute the material;
- **MODEL_DIVERSITY** — a different model family;
- **EMPIRICAL** — a different sample.

### `QROS-INDEP-REPLICATION-REQUIRES-EMPIRICAL`
Only EMPIRICAL independence supports "replication". Agreement between models is review
diversity, never replication.

### `QROS-INDEP-STATE-PER-DIMENSION`
A claim of independence names which dimensions hold. Silence about a dimension means
`UNKNOWN`.

---

## 5. Lifecycle

### `QROS-LIFECYCLE-STAGES`
`S0 FRAME → S1 DESIGN+SEAL → S2 BUILD → S3 RUN → S4 VERDICT → STOP`.

### `QROS-LIFECYCLE-TERMINATES`
`STOP` is terminal. A stage MUST NOT be re-entered because further work is imaginable.
Re-research requires a genuinely untested subspace or a demonstrably invalid prior
design (`QROS-VERDICT-NO-RESCUE`).

### `QROS-LIFECYCLE-PROPORTIONALITY`
The full lifecycle applies to preregistered `FULL` work. `EXPLORATORY` and `MEASUREMENT`
work runs build, check and record, and emits only what its lane permits. Work that
cannot produce a durable claim, cannot expose a reserved sample and cannot cause an
unsafe action needs nothing beyond ordinary engineering practice.

### `QROS-S0-DISCOVERY`
Discovery belongs to S0; it is not a separate stage.

- Work from mechanism, to family, to candidate object.
- Never commission "N strategies".
- There is no candidate-count target.
- At S0 the `BUILDER` states the mechanism, rival explanations and kill criteria, and
  the `DELEGATE` decides `RESEARCH | PARK | REJECT`.

### `QROS-S0-ANTI-REVIVAL`
Changing the instrument, lookback, threshold, wrapper, holding period, scaling or
announcement family does not, by itself alone, make a candidate new. Equivalence is
judged on mechanical overlap evidence.

### `QROS-S0-POINT-IN-TIME-FIRST`
Before design effort, confirm that every load-bearing input can be reconstructed as it
was known at the decision timestamp. If it cannot, the candidate is
`PARKED_PRE_OUTCOME`.

For price-only or trivially reconstructible inputs, this check is a one-line statement.
A full retrieval freeze applies only where retrieval feasibility materially shapes the
design.

### `QROS-S2-LIGHT-LOOP`
S2 is implement, test, repair, replay. Mechanical validators take precedence over model
review. Ordinary changes need no review seat and no standalone evidence document.

---

## 6. Preregistration and seal

### `QROS-PREREG-CONTENT`
A preregistration states:

- the question and hypothesis;
- the estimand and metric, on one declared scale (`QROS-PREREG-METRIC-SCALE-CONSISTENCY`);
- the sample, the data rules and the missing-data policy;
- the cost model;
- the primary definition and the secondaries;
- the verdict rule (`QROS-PREREG-VERDICT-RULE`);
- the resolvability evidence (`QROS-PREREG-RESOLVABILITY`);
- the validity checks (`QROS-PREREG-VALIDITY-CHECKS`);
- sample-reuse and trial accounting;
- disclosed design contributions (`QROS-PRESEAL-CONTRIBUTION-RECORDED`).

### `QROS-PREREG-SEAL-BEFORE-EXPOSURE`
The seal precedes any exposure of the outcome it governs. The seal is a digest manifest
over the preregistration and the code and data identities that define the object under
test.

### `QROS-PREREG-RESOLVABILITY`
Before a one-shot trial is spent, show the admissible sample size and the minimum
detectable effect, set against the smallest effect of interest.

For a return-stream claim, precision is governed by calendar span:
- the t-statistic equals the annualized Sharpe ratio times the square root of the span
  in years;
- sampling at a higher frequency, or pooling across instruments, does not change that
  relation.

A design that can only return `unresolved` is redesigned or stopped. It is not run.

### `QROS-PREREG-KILL-REACHABILITY`
Every kill criterion MUST be reachable, on the declared scale, by a plausible outcome.

### `QROS-PREREG-METRIC-SCALE-CONSISTENCY`
Thresholds, estimates and intervals are stated on one scale. Where a transformation
maps between scales, it is declared.

### `QROS-PREREG-VERDICT-RULE`
The preregistration maps primary results mechanically to a verdict
(`QROS-VERDICT-VOCABULARY`), so that S4 computes rather than debates.

### `QROS-PREREG-ENFORCED-DATA-RULES`
Every window, terminal-period, universe and missing-data rule that the runner can check
MUST be checked in the runner's code. A rule stated only in prose does not control the
run.

### `QROS-PREREG-VALIDITY-CHECKS`
Each measurement instrument has a check that runs, and MUST pass, before the primary
result is read. Reproducing a number shows only that it follows from the bytes, not that
the measurement is valid.

### `QROS-PREREG-RECHECK-AFTER-AMENDMENT`
After any amendment, the preregistration validators are rerun and resolvability is
rechecked.

### `QROS-PREREG-LINEAGE`
Every seal records its parent seal, or records that it has none. Superseded seals are
kept and never erased.

### `QROS-PRESEAL-CONTRIBUTION-RECORDED`
Design contributions by any party are recorded before seal. A party's later acceptance
of its own contribution is governed by `QROS-ROLE-SELF-CERTIFICATION`.

---

## 7. Runs

### `QROS-RUN-GATE-MECHANICAL`
The run gate is mechanical. It checks only what is material:

- code identity, data identity and preregistration binding;
- environment identity, where relevant;
- runner safety;
- replay, where relevant;
- outcome-access state;
- a live grant.

A green gate lets the `DELEGATE` authorize the run. No model review re-checks anything
a machine decides.

### `QROS-RUN-SEAL-NOT-AUTHORIZATION`
A seal is not authorization to run. A grant is recorded before the run, names the
identities it covers, and states whether it is one-shot or standing.

### `QROS-RUN-ONE-SHOT-WRITE-AHEAD`
The runner records consumption of a one-shot grant **before** touching outcomes. A
grant with any evidence of use is consumed; that includes a partial, crashed or
indeterminate run. Nothing reverses consumption.

### `QROS-RUN-FAIL-CLOSED`
Run guards fail closed when a grant record is missing, ambiguous or indeterminate.

### `QROS-RUN-NO-GRANT-FOR-DEV`
Development, synthetic and replay runs that touch no sealed outcome need no grant.

---

## 8. Verdicts and stopping

### `QROS-VERDICT-RULE-COMPUTED`
Tooling recomputes the primary results and applies the sealed verdict rule. For a
consequential claim, the `BUILDER` first attacks its own claim adversarially and fixes
or discloses what it finds. The `DELEGATE` then reproduces the result and decides the
verdict and the wording of the claim.

### `QROS-VERDICT-NO-DEPARTURE`
No party departs from the sealed verdict rule after an outcome is seen. Where the rule
cannot be applied, the verdict is `unresolved`, and the reason is recorded.

### `QROS-VERDICT-VOCABULARY`
A verdict has two parts:

- a research status: `confirmed | supported | not_promoted | falsified | active |
  archived | experimental | unresolved`;
- a disposition: `RUN_TO_VERDICT | CLOSED_PRE_OUTCOME | PARKED_PRE_OUTCOME |
  NOT_STANDALONE`.

No other verdict vocabulary is used. When in doubt, `not_promoted`.

### `QROS-VERDICT-RECORD`
Each verdict entry in the decision record names:

- the decider;
- what was reproduced;
- whether an external review was called.

### `QROS-VERDICT-NO-RESCUE`
An `unresolved` result licenses no rescue, no threshold change, no same-sample retuning
and no relabelling. No observed-power argument is admitted. A failure-mode record may
explain why later research is eligible; it never constitutes a new verdict.

---

## 9. Evidence model

### `QROS-EVIDENCE-SEPARATION`
Builder claim ≠ mechanical evidence ≠ independent verification. The three are not
interchangeable.

### `QROS-EVIDENCE-SELF-DESCRIPTION-NOT-PROOF`
An artifact's description of itself is not evidence about it.

### `QROS-EVIDENCE-SYNTHETIC-VS-REAL`
Synthetic evidence ≠ real governed evidence.

### `QROS-EVIDENCE-ACCESS-NOT-AUTHORITY`
Having had access to data before ≠ authority to execute on it, or to reveal from it, in
the future.

### `QROS-EVIDENCE-INFRASTRUCTURE-NOT-RESULT`
Infrastructure readiness ≠ a result.

### `QROS-EVIDENCE-CODE-QUALITY-NOT-AUTHORIZATION`
A PASS on code quality ≠ research authorization.

### `QROS-EVIDENCE-AGREEMENT-NOT-REPLICATION`
Agreement between reviewers ≠ replication (`QROS-INDEP-REPLICATION-REQUIRES-EMPIRICAL`).

---

## 10. Sample reuse and trial accounting

### `QROS-REUSE-EXPOSURE-VS-TRIALS`
Exposure and trial count are separate ledgers (`QROS-AXES-NO-INFERENCE`).

### `QROS-REUSE-DECLARE-BEFORE-USE`
Every use of a sample is declared before outcomes are touched, together with the
sample's reuse class and evidence ceiling.

### `QROS-REUSE-NEW-SEAL-NO-REFRESH`
A new seal never restores a sample's freshness.

### `QROS-REUSE-NEGATIVE-CONSUMES`
A negative or unresolved result consumes its trial exactly as a positive one does.

### `QROS-REUSE-LOCKBOX`
A lockbox or one-shot holdout is used once, for the pre-committed test, under an
explicit grant. Build a sealed holdout arm only when a planned test will consume it.

---

## 11. Acceptance and review

### `QROS-ACCEPT-REPRODUCTION-FIRST`
Acceptance begins with reproduction:

1. run the project's reproduce command;
2. check commit order — preregistration, then predictions, then unseal, then scoring;
3. recompute the headline numbers from committed outputs;
4. confirm the sealed validity checks ran and passed before the primary result was
   read.

Judgement comes second. A PASS lists what it reproduced. A PASS that reproduced nothing
is not acceptance.

### `QROS-REVIEW-EVIDENCE-CLASSES`
Every acceptance or review statement carries one of `REPRODUCED | REASONED |
SELF-REPORTED`.

### `QROS-REVIEW-SELF-REPORTED-NOT-BLOCKING`
A `SELF-REPORTED` statement never passes and never blocks on its own.

### `QROS-REVIEW-VERDICTS`
The review outcomes are:

- `PASS` — move on; a PASS never widens scope;
- `HOLD` — requires a blocking finding, and buys one bounded repair.

For the delegated S2 loop, acceptance returns one of `ACCEPT | BOUNDED_REPAIR |
ESCALATE_TO_GATE`.

### `QROS-REVIEW-BLOCKING-REQUIREMENTS`
A blocking finding names a concrete threat and a concrete failure path on the current or
next stage. Anything else is `NON-BLOCKING`, `OPTIONAL` or `UNRELATED`, and becomes a
backlog row.

### `QROS-REVIEW-ROUND-BUDGET`
There are at most two substantive rounds per gate per lineage. A further HOLD goes to
the `OWNER`. No review creates another review. A finding becomes a row, a bounded
repair, or a decision.

### `QROS-REVIEW-NOT-ROUTINE`
Review happens because a rule requires it or a gate holder asks for it — never as
reassurance after ordinary validation.

### `QROS-REVIEW-PERSISTED`
A review or judgement that informs a decision is saved into the project when it is
received. An unpersisted review carries no evidential weight.

---

## 12. Blindness

### `QROS-BLIND-LEVELS`
A party is `OUTCOME_BLIND`, `OUTCOME_AWARE` or `UNKNOWN` with respect to a named
outcome.

### `QROS-BLIND-ON-DEMAND`
A sealed or blind bundle is an on-demand capability, never a stage. It is used only
for a concrete need:

- outcome blindness;
- isolation of an independent recomputation;
- a high-consequence evidence transfer.

A bundle carries recorded digests that the receiver recomputes before doing any work.
On absence, truncation or mismatch, the receiver MUST STOP.

### `QROS-BLIND-REPO-NOT-BLIND`
A project repository is not blind: commit subjects, logs and the current-state artifact
carry outcomes. A party that must stay blind receives a bundle, not repository access.

### `QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE`
Any rule that judges results — matching, thresholds, classification — is fixed before
exposure.

### `QROS-BLIND-EXPOSURE-RESPONSE`
When a party that was meant to be blind is exposed:

- the exposure is recorded (`QROS-EXPOSURE-MONOTONIC`);
- the party's subsequent judgement on that outcome is `REASONED` at most.

---

## 13. Blockers and progression

### `QROS-BLOCKER-SINGLE-SET`
There is one current blocker set, kept separate from the non-blocking backlog.

### `QROS-BLOCKER-ADMISSION`
A blocker is admitted only with a named threat and a concrete failure path on the
current or next stage.

### `QROS-BLOCKER-CLASSES`
Every blocker has exactly one class:

- real current-path blocker;
- non-blocking backlog;
- transport or packaging issue;
- review-seat or procedural failure;
- architecture-level blocker.

### `QROS-BLOCKER-TRANSPORT-NOT-IMPLEMENTATION`
A transport, tool or packaging failure is not evidence of an implementation defect, and
consumes no review round.

### `QROS-BLOCKER-CLOSED-STAYS-CLOSED`
A closed row stays closed and keeps the evidence that closed it. Reopening it needs new
evidence.

### `QROS-BLOCKER-EXPIRY`
A backlog row that no stage needs expires. It is never promoted to a blocker merely
because it has aged.

### `QROS-COMPLETION-PROGRESSION`
If the current question can be answered correctly and reproducibly, and no admitted
blocker threatens that answer, the work proceeds. Remaining non-blocking backlog does
not hold it.

### `QROS-COMPLETION-NO-AUTOMATIC-LOOPS`
No automatic cycle of repair then review then repair. No extra rounds for cosmetic
completeness.

### `QROS-COMPLETION-NO-SPECULATIVE-BLOCKER`
That a cleaner design is imaginable is not a blocker.

### `QROS-COMPLETION-STOP-RULE`
Stop once material risk is resolved. The same sample with tweaked parameters, or the
same strategy renamed, is not a new question.

### `QROS-COST-BUDGET`
Every control MUST reduce a concrete research risk by more than it costs in time,
tokens, complexity or maintenance; otherwise simplify it or remove it. Do not add a
control because another control failed.

Work inline by default. Parallel multi-agent fan-out earns its cost only where
adversarial coverage can change a decision:
- mechanism search at S0;
- a leakage hunt before S3;
- a red-team of a consequential claim at S4;
- a project exhaustion audit.

---

## 14. Gates

### `QROS-GATE-OWNER-RETAINED`
Only the `OWNER` performs or grants the following. This list is **closed**:

| Identifier | Reserved action |
|---|---|
| `QROS-OWNER-SPEND` | spending money |
| `QROS-OWNER-LIVE-CAPITAL` | live capital, broker connections, real orders |
| `QROS-OWNER-CREDENTIALS` | credentials and private data |
| `QROS-OWNER-PUBLIC-RELEASE` | pushing or publishing any project material beyond the local machine |
| `QROS-OWNER-DESTRUCTIVE-MUTATION` | permanent deletion; rewriting shared history; mutating append-only records |

### `QROS-GATE-DELEGATED`
The `DELEGATE` decides the following, informed by the `BUILDER`:

- the S0 decision;
- sealing;
- run authorization on a green gate;
- statistical reveal;
- the S4 verdict;
- promotion, falsification, retirement and closure;
- scope and methodology changes;
- data access beyond a grant, where it costs nothing and needs no credentials;
- local merges.

The `OWNER` MAY take back any delegated decision.

### `QROS-GATE-NO-RELAY`
A retained gate is exercised or granted by the `OWNER` directly. A relayed message
claiming to be the `OWNER`'s decision is not sufficient.

### `QROS-GATE-NO-SELF-AUTHORIZATION`
No party authorizes its own run, reveal or verdict, or widens its own grant.

### `QROS-OWNER-AUDIT-NOT-EXECUTION`
A party instructed to audit, review, plan or propose MUST NOT escalate into writing.
Where write permission is ambiguous, the restrictive reading applies: stop and ask.

---

## 15. Records

### `QROS-STATE-CURRENT-ARTIFACT`
A project keeps one current-state artifact, rewritten and never appended, at every
checkpoint. It fits on one screen. It holds, as relevant:

- the question and stage;
- active lines of work;
- live grants;
- dated live obligations;
- outcome exposure;
- open blockers;
- the next decision, and who holds it.

A closed line is reduced to one row and a pointer. Superseded facts are deleted, not
annotated. An inactive project needs no current-state artifact.

### `QROS-STATE-NOT-BLIND`
The current-state artifact is not presumed outcome-blind (`QROS-BLIND-REPO-NOT-BLIND`).

### `QROS-STATE-BLOCKER-ARTIFACT`
The blocker set and the backlog live in one artifact. Rows are closed, never deleted.

### `QROS-RECORD-DECISION-LOG-APPEND-ONLY`
One append-only decision record holds one entry for each:

- grant and consumption;
- seal and reveal;
- verdict and disposition;
- methodology change;
- `DELEGATE` or `OWNER` decision.

Each entry records `id · UTC · decider · decision · evidence pointer`. Entries are
written when the event happens, never reconstructed from a later state. An event that
cannot be established is `UNKNOWN`. A correction is a new entry that cites the old one.
A binding message is recorded verbatim, with its sender, before it is acted on. A grant
lives in exactly one place.

### `QROS-RECORD-CURRENT-VS-HISTORICAL`
Current state is rewritten; history is appended. The two are never merged.

### `QROS-RECORD-DURABLE-NOT-TRANSCRIPT`
A conversation or session memory is not durable state. Anything a later stage needs is
written to a named location, and the later stage verifies that it is present.

### `QROS-RECORD-DERIVED-NOT-COPIED`
A derived fact — a count, a status, a liveness flag — is generated from its source or
points to it. It is never hand-copied into a second document, and a derived fact never
overrides its source.

### `QROS-RECORD-PRESENT-AND-ABSENT`
Record validators check that expected current facts are present **and** that
incompatible live facts are absent.

### `QROS-RECORD-REPRODUCE-COMMAND`
Each active project keeps one command that re-derives its checkpoint evidence.

### `QROS-RECORD-CHECKPOINT`
At each research boundary — seal, run complete, verdict, stop — and whenever the
`BUILDER` chooses:

1. rewrite the current-state artifact;
2. regenerate derived facts, or point to their source;
3. run the reproduce command and a link check;
4. commit;
5. notify the `DELEGATE` with the checkpoint id and revision.

The `DELEGATE` reproduces from the repository at that revision, never from the message.
After a merge or publication, the same checks run once on the revision readers will
see. There is no completion token: the revision and the decision entry are the evidence.

---

## 16. Change control

### `QROS-CHANGE-LABELS`
Every change made after seal carries exactly one label:

| Label | Seal and lineage | Decided by |
|---|---|---|
| `IMPLEMENTATION_FIX` | preserved; same lineage only when the change restores the contract | `BUILDER` |
| `DATA_FIX` | preserved; same lineage only when the change restores a frozen input rule | `BUILDER`; a new source, sample or missing-data rule is a methodology change |
| `ANALYSIS_EXTENSION` | original seal and evidence unchanged; non-confirmatory; no rescue | `DELEGATE` |
| `METHODOLOGY_CHANGE` | amendment or new seal; same lineage only before exposure | `DELEGATE` |
| `HYPOTHESIS_CHANGE` | new preregistration, seal and lineage; no transfer as confirmation | `DELEGATE` |

No change reruns, amends or alters the trial count automatically.

### `QROS-CHANGE-CLASSIFY-BEFORE-APPLY`
The label is assigned and recorded, with its evidence, before the change is applied.
Where the sealed rule is ambiguous or absent, the change is a `METHODOLOGY_CHANGE`,
not a fix.

### `QROS-CHANGE-FIX-NOT-METHODOLOGY`
A repair MUST NOT alter the question, decision rule, threshold, sample or metric,
however small the edit.

### `QROS-CHANGE-DEFECT-IMPACT`
A confirmed defect that affects research gets one decision entry. The entry names:

- the defect;
- what is affected;
- what is demonstrably unaffected;
- what is unknown;
- whether recomputation is needed, and why;
- any restriction on how the evidence may be used;
- which runs were not recomputed.

---

## 17. Machine checks before model checks

### `QROS-CHECK-MACHINE-BEFORE-MODEL`
Where a deterministic check can reject an artifact, it runs before any model spends
effort on that artifact.

### `QROS-CHECK-NON-VACUOUS`
Every governance check MUST be demonstrably capable of failing, and MUST assert the
property of interest rather than a proxy for it. A check that examines a location
nothing occupies any more protects nothing.

---

## 18. Threat vocabulary

### `QROS-THREAT-VOCABULARY`
The failure modes QROS addresses:

- self-certification;
- outcome leakage;
- hindsight selection;
- same-sample retuning;
- silent revival;
- one-shot reuse;
- stale current state;
- derived-fact drift;
- presence-only validation;
- unpersisted review;
- prose-only data rules;
- invalid measurement;
- unresolvable design;
- governance cost exceeding risk.

The list is closed at each version.

---

## 19. Conformance and configuration

### `QROS-CONFORMANCE-SELF-DECLARED`
A project conforms by following these rules as written. There are no levels or
profiles. QROS certifies nothing. A project claiming conformance SHOULD name the rules
it does not meet.

### `QROS-CONFORMANCE-PUBLICATION-ASSURANCE`
A project publishing material derived from non-public work operates two checks:

- a **generic disclosure check**, published with the project: absolute paths, address-
  and identifier-shaped strings, credential patterns, committed data artifacts;
- a **project-specific disclosure audit**, kept private and never published, since
  publishing it would disclose what it protects.

A published artifact carries no non-public ancestry.

### `QROS-CONFIG-CONFIGURABLE`
A project MAY configure the following:

- role bindings;
- stage aliases, recorded;
- a review budget below the ceiling;
- exposure and data classes;
- the trial-accounting scheme;
- artifact formats.

### `QROS-CONFIG-NON-OVERRIDABLE`
No configuration weakens the following rules:

- `QROS-ROLE-OWNER`
- `QROS-ROLE-SELF-CERTIFICATION`
- `QROS-ROLE-SUBAGENT-NOT-INDEPENDENT`
- `QROS-GATE-NO-RELAY`
- `QROS-GATE-NO-SELF-AUTHORIZATION`
- `QROS-AXES-NO-INFERENCE`
- `QROS-INDEP-REPLICATION-REQUIRES-EMPIRICAL`
- `QROS-EVIDENCE-SEPARATION`
- `QROS-PREREG-SEAL-BEFORE-EXPOSURE`
- `QROS-VERDICT-NO-DEPARTURE`
- `QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE`
- `QROS-EXPOSURE-MONOTONIC`
- `QROS-RECORD-DECISION-LOG-APPEND-ONLY`
- `QROS-CHECK-NON-VACUOUS`

### `QROS-CONFIG-TIGHTEN-ONLY`
A configuration MAY be stricter than this specification; it MUST NOT relax it. The
threat vocabulary and the retained-gate list are not configuration surfaces.

---

## Appendix A — Identifier index

- **Purpose:** `PURPOSE-SCOPE` · `PURPOSE-NO-ALPHA-CLAIM` ·
  `PURPOSE-MODEL-OUTPUT-NOT-EVIDENCE` · `PURPOSE-NEGATIVE-RESULTS-VALID` ·
  `PURPOSE-NO-CORRECTNESS-GUARANTEE` · `PURPOSE-PRIORITIES`
- **Authority:** `AUTHORITY-PRECEDENCE` · `AUTHORITY-CROSS-SCOPE-CONFLICT` ·
  `AUTHORITY-STALE-LOCAL-DOCS` · `AUTHORITY-STATE-NOT-AUTHORITY`
- **Roles:** `ROLE-OWNER` · `ROLE-DELEGATE` · `ROLE-BUILDER` · `ROLE-BUILDER-AUTONOMY` ·
  `ROLE-SINGLE-ACTIVE-BUILDER` · `ROLE-SELF-CERTIFICATION` ·
  `ROLE-SUBAGENT-NOT-INDEPENDENT` · `ROLE-SAME-FAMILY-LIMIT` ·
  `ROLE-VENDOR-BINDING-IS-CONFIG`
- **Axes:** `AXES-THREE` · `AXES-NO-INFERENCE` · `AXIS-LANE` · `LANE-CLAIM-SCOPE` ·
  `AXIS-TRIAL-ACCOUNTING` · `AXIS-OUTCOME-EXPOSURE` · `EXPOSURE-MONOTONIC`
- **Independence:** `INDEP-FOUR-KINDS` · `INDEP-REPLICATION-REQUIRES-EMPIRICAL` ·
  `INDEP-STATE-PER-DIMENSION`
- **Lifecycle:** `LIFECYCLE-STAGES` · `LIFECYCLE-TERMINATES` ·
  `LIFECYCLE-PROPORTIONALITY` · `S0-DISCOVERY` · `S0-ANTI-REVIVAL` ·
  `S0-POINT-IN-TIME-FIRST` · `S2-LIGHT-LOOP`
- **Preregistration:** `PREREG-CONTENT` · `PREREG-SEAL-BEFORE-EXPOSURE` ·
  `PREREG-RESOLVABILITY` · `PREREG-KILL-REACHABILITY` ·
  `PREREG-METRIC-SCALE-CONSISTENCY` · `PREREG-VERDICT-RULE` ·
  `PREREG-ENFORCED-DATA-RULES` · `PREREG-VALIDITY-CHECKS` ·
  `PREREG-RECHECK-AFTER-AMENDMENT` · `PREREG-LINEAGE` ·
  `PRESEAL-CONTRIBUTION-RECORDED`
- **Runs:** `RUN-GATE-MECHANICAL` · `RUN-SEAL-NOT-AUTHORIZATION` ·
  `RUN-ONE-SHOT-WRITE-AHEAD` · `RUN-FAIL-CLOSED` · `RUN-NO-GRANT-FOR-DEV`
- **Verdicts:** `VERDICT-RULE-COMPUTED` · `VERDICT-NO-DEPARTURE` · `VERDICT-VOCABULARY` ·
  `VERDICT-RECORD` · `VERDICT-NO-RESCUE`
- **Evidence:** `EVIDENCE-SEPARATION` · `EVIDENCE-SELF-DESCRIPTION-NOT-PROOF` ·
  `EVIDENCE-SYNTHETIC-VS-REAL` · `EVIDENCE-ACCESS-NOT-AUTHORITY` ·
  `EVIDENCE-INFRASTRUCTURE-NOT-RESULT` · `EVIDENCE-CODE-QUALITY-NOT-AUTHORIZATION` ·
  `EVIDENCE-AGREEMENT-NOT-REPLICATION`
- **Reuse:** `REUSE-EXPOSURE-VS-TRIALS` · `REUSE-DECLARE-BEFORE-USE` ·
  `REUSE-NEW-SEAL-NO-REFRESH` · `REUSE-NEGATIVE-CONSUMES` · `REUSE-LOCKBOX`
- **Acceptance and review:** `ACCEPT-REPRODUCTION-FIRST` · `REVIEW-EVIDENCE-CLASSES` ·
  `REVIEW-SELF-REPORTED-NOT-BLOCKING` · `REVIEW-VERDICTS` ·
  `REVIEW-BLOCKING-REQUIREMENTS` · `REVIEW-ROUND-BUDGET` · `REVIEW-NOT-ROUTINE` ·
  `REVIEW-PERSISTED`
- **Blindness:** `BLIND-LEVELS` · `BLIND-ON-DEMAND` · `BLIND-REPO-NOT-BLIND` ·
  `BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE` · `BLIND-EXPOSURE-RESPONSE`
- **Blockers and progression:** `BLOCKER-SINGLE-SET` · `BLOCKER-ADMISSION` ·
  `BLOCKER-CLASSES` · `BLOCKER-TRANSPORT-NOT-IMPLEMENTATION` ·
  `BLOCKER-CLOSED-STAYS-CLOSED` · `BLOCKER-EXPIRY` · `COMPLETION-PROGRESSION` ·
  `COMPLETION-NO-AUTOMATIC-LOOPS` · `COMPLETION-NO-SPECULATIVE-BLOCKER` ·
  `COMPLETION-STOP-RULE` · `COST-BUDGET`
- **Gates:** `GATE-OWNER-RETAINED` (`OWNER-SPEND`, `OWNER-LIVE-CAPITAL`,
  `OWNER-CREDENTIALS`, `OWNER-PUBLIC-RELEASE`, `OWNER-DESTRUCTIVE-MUTATION`) ·
  `GATE-DELEGATED` · `GATE-NO-RELAY` · `GATE-NO-SELF-AUTHORIZATION` ·
  `OWNER-AUDIT-NOT-EXECUTION`
- **Records:** `STATE-CURRENT-ARTIFACT` · `STATE-NOT-BLIND` · `STATE-BLOCKER-ARTIFACT` ·
  `RECORD-DECISION-LOG-APPEND-ONLY` · `RECORD-CURRENT-VS-HISTORICAL` ·
  `RECORD-DURABLE-NOT-TRANSCRIPT` · `RECORD-DERIVED-NOT-COPIED` ·
  `RECORD-PRESENT-AND-ABSENT` · `RECORD-REPRODUCE-COMMAND` · `RECORD-CHECKPOINT`
- **Change control:** `CHANGE-LABELS` · `CHANGE-CLASSIFY-BEFORE-APPLY` ·
  `CHANGE-FIX-NOT-METHODOLOGY` · `CHANGE-DEFECT-IMPACT`
- **Checks:** `CHECK-MACHINE-BEFORE-MODEL` · `CHECK-NON-VACUOUS`
- **Threats:** `THREAT-VOCABULARY`
- **Conformance and configuration:** `CONFORMANCE-SELF-DECLARED` ·
  `CONFORMANCE-PUBLICATION-ASSURANCE` · `CONFIG-CONFIGURABLE` ·
  `CONFIG-NON-OVERRIDABLE` · `CONFIG-TIGHTEN-ONLY`

All identifiers carry the `QROS-` prefix.

## Appendix B — Retired identifiers (v1)

Retired identifiers are never reused.

| v1 identifier | v2 successor |
|---|---|
| `QROS-ROLE-MAIN-AGENT` | `QROS-ROLE-BUILDER` |
| `QROS-ROLE-INDEPENDENT-REVIEWER` | `QROS-ROLE-DELEGATE` (acceptance) and `QROS-ROLE-SAME-FAMILY-LIMIT` (external review on request) |
| `QROS-ROLE-ARCHITECTURE-REVIEWER`, `QROS-ROLE-ARCHITECTURE-ESCALATION-BOUNDED` | `QROS-ROLE-DELEGATE` (design on request) |
| `QROS-INDEP-CONTEXT`, `-AUTHORSHIP`, `-MODEL-DIVERSITY`, `-EMPIRICAL` | `QROS-INDEP-FOUR-KINDS` |
| `QROS-LIFECYCLE-REDUCED-EXPLORATORY`, `-MEASUREMENT`, `-BUGFIX` | `QROS-LIFECYCLE-PROPORTIONALITY`, `QROS-CHANGE-LABELS` |
| `QROS-PREREG-RULE-DOMAIN-ANALYSIS` | `QROS-PREREG-KILL-REACHABILITY`, `QROS-PREREG-RESOLVABILITY` |
| `QROS-PRESEAL-CHALLENGE-SCOPE` | `QROS-S0-DISCOVERY` (challenge on request) |
| `QROS-REVIEW-MANDATORY-TRIGGERS` | `QROS-REVIEW-NOT-ROUTINE` |
| `QROS-REVIEW-CLASSIFICATION-AUTHORITY`, `QROS-REVIEW-ROUND-SCOPE`, `QROS-REVIEW-ESCALATION-ON-EXHAUSTION` | `QROS-REVIEW-ROUND-BUDGET`, `QROS-REVIEW-BLOCKING-REQUIREMENTS` |
| `QROS-BLIND-IS-TRANSPORT`, `QROS-BLIND-PRE-FREEZE-SET`, `QROS-BLIND-FREEZE-POINT`, `QROS-BLIND-POST-FREEZE-COMPARANDS`, `QROS-BLIND-BYTE-IDENTITY-NO-JUDGMENT` | `QROS-BLIND-ON-DEMAND`, `QROS-BLIND-REPO-NOT-BLIND` |
| `QROS-STATE-OUTCOME-CLEAN` | `QROS-STATE-NOT-BLIND` |
| `QROS-OWNER-GATE-LIST` | `QROS-GATE-OWNER-RETAINED`, `QROS-GATE-DELEGATED` |
| `QROS-OWNER-REAL-RUN`, `QROS-OWNER-REVEAL`, `QROS-OWNER-DISPOSITION`, `QROS-OWNER-METHODOLOGY-CHANGE` | `QROS-GATE-DELEGATED` |
| review dispatch, review brief, review attestation, `PASS_WITH_BACKLOG` | retired; acceptance is `QROS-ACCEPT-REPRODUCTION-FIRST` |

## Specification change policy

A new version states its changes against the previous one, retires identifiers
instead of reusing them, and applies prospectively. Records made under an earlier
version are never re-judged under a later one.
