# QROS — Quantitative Research Operating System

QROS is an operating model for quantitative strategy research done with substantial
help from AI agents. It keeps apart the parties who build, accept and authorize work,
and it records which outcomes each party has seen. The aim is research that stays
reproducible and resistant to leakage, silent overfitting and self-certification.

The repository holds:

- a **specification**;
- **artifact templates**;
- **schemas** that enforce the templates;
- one **fully synthetic worked example**.

It is not a trading system.

**Version 2.0.0.** Version 2 replaces v1's review-dispatch machinery with:

- three roles;
- acceptance by reproduction;
- verdicts computed from a rule sealed in advance.

The v1 artifacts live under [`retired/v1/`](retired/v1/). The mapping from every v1
rule to its v2 successor is in [SPEC.md](SPEC.md), Appendix B.

---

## Why it exists

An AI agent that produces a result and then attests to it will confirm itself. A
pipeline that lets outcome information reach the party meant to check it cannot detect
its own errors. Both failures are quiet: the tests stay green, the write-up stays
confident, and the mistake propagates.

QROS targets failures that recur in quantitative research:

- look-ahead leakage;
- moving a threshold to meet a result;
- reusing an already-searched sample;
- treating a builder's claim as evidence;
- data rules that exist only in prose;
- designs that can only ever return "unresolved";
- governance that grows until it replaces the research.

Each rule exists to make one of these expensive rather than convenient. The reasoning
is in [docs/rationale.md](docs/rationale.md). What QROS does and does not defend against
is in [docs/threat-model.md](docs/threat-model.md).

## Roles

| role | who | does |
|---|---|---|
| `OWNER` | a human | holds the retained gates: spending, live capital, credentials, public release, destructive mutation; may override any delegated decision |
| `DELEGATE` | appointed by the Owner, optional; may be an AI agent in its own session | decides the delegated gates (seal, run authorization, reveal, verdict, scope and methodology changes); accepts work by reproduction; never builds |
| `BUILDER` | one per project | designs, implements, tests, runs authorized runs, keeps the records; autonomous under a standing authorization; never authorizes its own run, reveal or verdict |

A retained gate is never granted through a relayed message. Where a Delegate and a
Builder share a model family, that is not model diversity. QROS relies on structure
instead: reproduction-first acceptance and verdicts computed by a sealed rule.

## Lifecycle

```
S0 FRAME ──► S1 DESIGN+SEAL ──► S2 BUILD ──► S3 RUN ──► S4 VERDICT ──► STOP
   │               │                │            │             │
   │               │                │            │             └─ tooling applies the sealed verdict
   │               │                │            │                rule; the Delegate reproduces and
   │               │                │            │                decides; no departure after outcome
   │               │                │            └─ mechanical gate; a one-shot grant is recorded as
   │               │                │               consumed before outcomes are touched; fail closed
   │               │                └─ implement · test · repair · replay; machine checks, not reviewers
   │               └─ preregistration with a verdict rule, resolvability (MDE vs the smallest effect
   │                  of interest), data rules enforced in code, validity checks; sealed by digest
   └─ mechanism → family → candidate; anti-revival; point-in-time feasibility first
```

At every research boundary the Builder writes a **checkpoint**:

1. rewrite the one-screen current state;
2. regenerate derived facts, or point to their source;
3. run the reproduce command and a link check;
4. commit;
5. notify the Delegate with the revision.

The Delegate reproduces from the repository at that revision. Every statement is
labelled `REPRODUCED`, `REASONED` or `SELF-REPORTED`, and a PASS lists what it
reproduced.

Review is bounded:

- a PASS means move on;
- a HOLD needs a named threat and failure path, and buys one repair;
- there are at most two rounds per gate per lineage.

## What QROS separates

| Separation | Why it matters |
|---|---|
| Producing work / certifying it | No party certifies its own material contribution. A spawned agent is not independent of its spawner. |
| Builder claim / mechanical evidence / independent verification | Three kinds of support. None substitutes for another. |
| Numbers that reproduce / measurements that are valid | Reproduction shows a number follows from the bytes, not that the instrument measures what it claims. Validity checks are sealed and run first. |
| Seal / authorization | A seal fixes the design; it does not permit a run. |
| What a party knows / when it knows it | Exposure is recorded per party and object, and never regresses. A missing record is `UNKNOWN`, not `NONE`. |
| Current state / history | One page, rewritten, says where the work stands. One append-only log says what was decided, by whom, and on what evidence. |
| Retained / delegated authority | Irreversible, external and financial actions stay with the human Owner. |

## The worked example (v1-era)

[`examples/synthetic-study/`](examples/synthetic-study/STUDY.md) runs a whole study on
**entirely fabricated, deterministically generated data**. It was produced under
QROS 1.0, so its dispatch, brief and attestation files show retired machinery (see
[V1_ERA.md](examples/synthetic-study/V1_ERA.md)). Its lesson holds unchanged in v2.

| | |
|---|---|
| Builder's result | **0.331216** |
| Independent recomputation | **0.064635** |
| Preregistered threshold | **0.15** |
| Final disposition | **`not_promoted`** |

The builder's code had a one-line look-ahead defect: the signal dated *t* contained the
return of *t+1*. Four shape checks passed on it. A recomputation from the sealed
definition, without the builder's code or number, got a different answer; that
discrepancy was the finding. The repaired result fell below the preregistered threshold.
The threshold never moved.

In v2 terms:

- the recomputation is the Delegate's `QROS-ACCEPT-REPRODUCTION-FIRST`;
- the leak check that the shape checks lacked is a sealed validity check
  (`QROS-PREREG-VALIDITY-CHECKS`, `QROS-CHECK-NON-VACUOUS`).

**Nothing here is alpha.** The first number was an artefact of the defect, and the
second describes a synthetic process designed to sit below the threshold.

## Repository structure

```
SPEC.md                     the single normative source; every rule, stated once
templates/                  preregistration, research state, decision log, backlog,
                            sample-reuse declaration
schemas/                    JSON Schema (2020-12) enforcing the templates and the
                            closed vocabularies
examples/synthetic-study/   one worked study, end to end, fully synthetic (v1-era)
docs/                       rationale, threat model, adoption guide
retired/v1/                 v1 review dispatch, brief and attestation artifacts;
                            never used for new work
```

## Quick start

To reproduce the example (standard library only; no dependencies, no network, no
committed data):

```bash
cd examples/synthetic-study

python generate.py --out data                                        # deterministic data
python analyze.py  --data data/sample_development.csv --with-defect   # 0.331216
python checks.py   --data data/sample_development.csv --with-defect   # shape checks pass, leak check fails
python verify.py   --data data/sample_development.csv                 # 0.064635, independently
python analyze.py  --data data/sample_development.csv                 # 0.064635, repaired
python checks.py   --data data/sample_development.csv                 # all checks pass
```

Then read [SPEC.md](SPEC.md) for the rules and [docs/adoption.md](docs/adoption.md) to
adopt them.

**The minimal kit for a new project:**

- this specification;
- a one-screen current-state artifact;
- an append-only decision log;
- a reproduce command;
- a preregistration from S1.

## Design principles

- **Correct research first.** The priority order is correct research, then
  reproducibility, then essential safety, then finishing, then framework perfection.
  A control that costs more than the risk it removes is simplified or removed.
- **Rigor that terminates.** Review is budgeted, negative results are complete work,
  and `STOP` is terminal.
- **Resolvability before spending a trial.** For a return-stream claim, precision is set
  by calendar span. A design that can only return "unresolved" is redesigned or stopped
  before it consumes a sample.
- **Rules in code, not prose.** Data rules the runner can check are checked in the
  runner.
- **Machine checks before model checks.** A check that cannot fail is not protection.
- **Roles, not products.** Which model or person fills a role is configuration. The
  Owner is human.

## What QROS does not do

- It does not find profitable strategies, and adopting it is not evidence that any
  strategy is profitable.
- It does not guarantee correct conclusions. It raises the cost of named process
  failures and makes them explicit when they occur.
- It does not prevent overfitting. It makes threshold-moving, sample reuse and
  post-answer searching visible and recorded.
- It is not a backtesting engine, signal library, strategy collection or data
  pipeline.
- It makes no claim of fitness for any regulatory, fiduciary or contractual purpose,
  and it confers no certification.

## License

This project is licensed under the [MIT License](LICENSE).
