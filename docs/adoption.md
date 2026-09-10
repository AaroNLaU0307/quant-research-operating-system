# Adopting QROS

How to run a project under QROS without any infrastructure beyond a filesystem,
version control, and whatever agents or people already do the work.

Explanatory. [SPEC.md](../SPEC.md) is the only normative source; where this
document and the specification differ, the specification governs.

There are **no conformance levels, tiers, profiles, editions, or maturity
stages**. The rules apply as written. Where a rule is conditional it says so at
its own site — `QROS-LIFECYCLE-PROPORTIONALITY` scales governance to
consequence, and `QROS-CHECK-MACHINE-BEFORE-MODEL` applies wherever a
deterministic check exists that could reject the artifact.

---

## What you need

Nothing beyond: somewhere to keep text files under version control, at least two
parties that can work independently of one another, and one accountable human.
The reference implementation of the worked example uses the Python standard
library and nothing else.

---

## 1. Name the roles

Four capability roles. Bind each to a concrete party and **record the binding**
(`QROS-ROLE-VENDOR-BINDING-IS-CONFIG`).

| Role | What it does | Constraint |
|---|---|---|
| `OWNER` | authorises the reserved actions; decides when review is exhausted | **must be human**; cannot be delegated to an agent by any means |
| `MAIN_AGENT` | designs, implements, tests, produces evidence, maintains records | the default working role; at most one active per write scope |
| `INDEPENDENT_REVIEWER` | certifies work it did not produce | must not repair what it reviews |
| `ARCHITECTURE_REVIEWER` | adjudicates design-level questions | exception path only, never routine |

Two rules do most of the work here, and both are easy to breach by accident:

- **The producer is never the sole certifier** of a consequential artifact
  (`QROS-ROLE-SELF-CERTIFICATION`). This attaches to the artifact, not the
  calendar — a later session of the same producing party inherits the same
  disqualification.
- **A spawned agent is not independent of its spawner**
  (`QROS-ROLE-SUBAGENT-NOT-INDEPENDENT`). Delegating the check to a subprocess of
  the party being checked produces no independence, however separate the
  execution context. Spawned agents are fine for gathering evidence; their
  conclusions are not independent verification.

Which model, vendor, or person fills a role is your configuration and forms no
part of QROS semantics. Different roles filled by different model families gives
you review diversity, which is worth something — but it is not replication, and
nothing in the specification treats it as such.

## 2. Decide where artifacts live

Plain files in the project repository is sufficient and is what the worked
example does. You need three durable artifacts and one per-review set:

| Artifact | Mutation rule | Template |
|---|---|---|
| Current state — one page, where the work stands | rewritten in place | [`research-state.md`](../templates/research-state.md) |
| Blockers and backlog — the single blocker authority | rows closed, never deleted | [`backlog.md`](../templates/backlog.md) |
| Decision log — Owner decisions and review verdicts | **append-only** | [`decision-log.md`](../templates/decision-log.md) |

Current state and historical record are different artifact classes with opposite
mutation rules and must not be merged
(`QROS-RECORD-CURRENT-VS-HISTORICAL`). An artifact attempting both loses the
first to clutter and the second to revision.

**Keep the current-state page outcome-clean** (`QROS-STATE-OUTCOME-CLEAN`): no
verdicts, no effect sizes, no target-metric values, no exposure counts. Its
whole purpose is that a party under blindness obligations can read it safely. A
page that cannot be read by such a party is unusable exactly when blindness
matters.

Conversational transcripts are not durable state
(`QROS-RECORD-DURABLE-NOT-TRANSCRIPT`). Where one stage's output is another
stage's input, name the file in advance and verify it exists before proceeding.

## 3. Instantiate the templates

[`templates/`](../templates) holds eight. Start with the three above, plus:

- [`preregistration.yaml`](../templates/preregistration.yaml) — the sealed
  contract for a `FULL`-lane study
- [`dispatch.md`](../templates/dispatch.md),
  [`review-brief.md`](../templates/review-brief.md),
  [`attestation.md`](../templates/attestation.md) — the review transport set
- [`sample-reuse.md`](../templates/sample-reuse.md) — one declaration per reuse

Templates cite specification identifiers rather than restating rules, so they
stay short and cannot drift into a second normative source. Adapt formatting
freely; keep the fields.

## 4. Wire up the schemas

[`schemas/`](../schemas) are JSON Schema 2020-12. YAML artifacts validate through
them directly, since YAML maps onto the JSON data model.

They enforce the closed vocabularies and the structural invariants that are
easiest to breach by hand — that a `VALID` review carries exactly one of three
verdicts and an `INVALID` one carries none, that a non-blocking backlog row
carries no invented threat class, that a blocking finding names a failure path,
that an authorised execution names the single execution it authorises.

Run them in whatever way suits you. The point is
`QROS-CHECK-MACHINE-BEFORE-MODEL`: if a deterministic check can reject the
artifact, run it before spending review capacity on it.

## 5. Preregister, then seal

For any study that will produce a durable confirmatory claim, fix the contract
before any party involved sees the target metric
(`QROS-PREREG-SEAL-BEFORE-EXPOSURE`): question, hypothesis, metric with its units
and scale and transformation, decision-relevant threshold where one applies,
sample definition and any reserved portion, decision rules in evaluation order,
kill conditions, trial-accounting plan, known reuse and exposure.

Three pre-seal checks are worth doing properly, because each catches a defect
that is invisible later:

- **Kill-branch reachability** — demonstrate from inputs available in advance
  that the branch can fire on realistic input. A branch nothing can reach looks
  like protection and is none.
- **Metric/scale consistency** — the threshold must be on the same metric and
  scale as the rule that reads it.
- **Rule-domain analysis** — evaluate each rule at the extremes of its input's
  attainable domain. Contradictory or degenerate rules are invisible at typical
  values.

Re-run all three after every amendment (`QROS-PREREG-RECHECK-AFTER-AMENDMENT`).

Sealing needs no special tooling: a digest over the contract fields, recorded
where it can be recomputed. The worked example's
[`02-seal.json`](../examples/synthetic-study/02-seal.json) shows a one-line
method.

## 6. Build the reviewer's evidence surface

This is the step most likely to be done badly, and the one that carries most of
the protective value.

A blind review requires a **separately constructed evidence surface**: an
evidence set built for the review, outside the working environment that holds the
material the reviewer must not reach, with its contents enumerated in advance and
each item digest-pinned. `SEPARATE_EVIDENCE_SURFACE` is **the** mechanism, not
one option among several — the specification recognises no alternative isolation
architecture, and a review conducted inside the environment that holds
outcome-bearing material is not blind however that environment is arranged.

In practice: create a directory, copy in exactly the enumerated items, and give
the reviewer that directory. The material outside it is then *absent* rather than
*forbidden*, which is the whole distinction (`QROS-BLIND-IS-TRANSPORT`).

What goes in depends on the obligation. For an independent recomputation of a
final statistic: the raw sample, the sealed preregistration, the brief, and the
recomputation instrument — but **not** the producer's implementation and **not**
the producer's claimed value. Those are post-freeze comparands, delivered only
after the reviewer has recorded and digested its own result.

Fix every judgement-bearing matching rule in the brief **before** the reviewer is
exposed to what it judges (`QROS-BLIND-MATCHING-RULE-FIXED-BEFORE-EXPOSURE`) —
tolerances, which cases apply, what counts as materially the same. A rule fixed
afterwards can be shaped by the values it will be applied to. Byte-identity
comparisons admit no judgement and need no such fixing.

[`05-dispatch-r1.yaml`](../examples/synthetic-study/05-dispatch-r1.yaml) is a
complete worked instance.

## 7. Define your deterministic checks

Whatever your domain makes checkable: invariants, leakage checks, timing checks,
accounting identities, deterministic reproduction.

Two rules about the checks themselves:

- **Every check must be demonstrably capable of failing**
  (`QROS-CHECK-NON-VACUOUS`). Be able to show, for each, a condition under which
  it fails. A check whose subject has moved passes forever while protecting
  nothing.
- **Assert the property, not a proxy.** Where the property is a runtime
  behaviour, a check over static structure does not establish it.

The worked example's [`checks.py`](../examples/synthetic-study/checks.py) has
five, one of which was added as the regression test for a real defect and still
fails against the retained defective implementation — which is what makes it
demonstrably non-vacuous.

## 8. Declare your trial-accounting method

QROS prescribes **no** counting formula (`QROS-AXIS-TRIAL-ACCOUNTING`). Record
the method your project declares: planned comparison count, what constitutes one
family, any adjustment procedure, and what the rule governs.

This is deliberate. The right adjustment depends on the design, and a
specification that hard-coded one would be wrong more often than helpful. What
the specification does require is that the method be declared in advance and
applied rather than reasoned about after the fact.

## 9. Record sample reuse before it happens

Before consequential use of a sample that has already been searched, selected on,
fitted, or evaluated: declare which sample, what prior use it absorbed, what this
use will do, why the reuse is acceptable **for this specific claim**, and — the
part usually skipped — what this use will **not** compute.

`QROS-REUSE-NEW-SEAL-NO-REFRESH` is the one people breach honestly: sealing a new
preregistration fixes what happens next, and does not undo what the sample has
already absorbed.

If no reuse occurs, do not file a declaration. The worked example does not — it
states that reuse was not applicable rather than exercising the template with
invented content.

## 10. Keep the Owner gates

Six reserved actions no agent may self-authorise
(`QROS-OWNER-GATE-LIST`). **The list is closed** — a project may not add, remove,
or rename a gate:

`QROS-OWNER-REAL-RUN` · `QROS-OWNER-REVEAL` · `QROS-OWNER-DISPOSITION` ·
`QROS-OWNER-METHODOLOGY-CHANGE` · `QROS-OWNER-PUBLIC-RELEASE` ·
`QROS-OWNER-DESTRUCTIVE-MUTATION`

Real-data execution is authorised **per execution**, bound to that execution's
identity — code and specification identity, data identity, purpose — and
re-verified immediately before it starts. One authorisation covers one
execution. There is no envelope, class, or standing authorisation covering future
runs, and an authorisation is current only until it is used, superseded, or
revoked.

And `QROS-OWNER-AUDIT-NOT-EXECUTION`: a party told to audit, review, analyse,
plan, or propose must not escalate into execution. Producing a recommendation,
however well supported, does not authorise acting on it. Where write permission
is ambiguous, the restrictive reading applies.

---

## What you may configure, and what you may not

**Configurable** (`QROS-CONFIG-CONFIGURABLE`): role bindings; stage aliases, if
the mapping is recorded; the review-round budget; exposure and data classes;
trial-accounting rules; the concrete file formats of your artifacts.

**Not configurable** (`QROS-CONFIG-NON-OVERRIDABLE`) — and specifically, three
things adopters most often want to make configurable and must not:

- **the six threat classes** — closed;
- **the six Owner gates** — closed;
- **the blindness mechanism** — the separately constructed evidence surface;
  no alternative isolation architecture is recognised.

A configuration may make the specification **stricter**: more mandatory review
triggers, a smaller review budget, narrower exposure classes. It may not relax a
requirement, and in particular may not define output of a producing party as
independent verification of that party's own work by any construction.

---

## Starting small, honestly

You do not have to adopt everything at once, and the specification does not
define a partial-adoption tier because a tier would invite treating the partial
state as complete. What it asks instead
(`QROS-CONFORMANCE-SELF-DECLARED`): if you claim conformance, state which
requirements you do not meet. A partial claim that names its gaps is more useful
than an unqualified one.

If you adopt exactly one thing, adopt independent recomputation of the statistic
that a decision rule reads, by a party that has not seen the producer's number.
That is where the worked example's defect was caught, and it is the mechanism
the rest of the system exists to protect.
