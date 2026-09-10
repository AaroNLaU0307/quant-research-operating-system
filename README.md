# QROS — Quantitative Research Operating System

QROS is an agent-assisted research operating system for quantitative strategy
development. It separates strategy construction, mechanical validation,
independent review, data exposure, and Owner authorization, so that
AI-assisted research stays reproducible and resistant to leakage, silent
overfitting, and self-certification.

It is a **specification**, a set of **artifact templates**, **schemas** that
enforce them, and one **fully synthetic worked example**. It is not a trading
system.

---

## Why it exists

An AI agent that produces a result and then attests to that result will confirm
itself. A research pipeline that lets outcome information reach the party
supposed to be checking it cannot detect its own errors. Both failures are
quiet: the tests stay green, the write-up stays confident, and the mistake
propagates.

QROS is built around a small number of failure modes that recur in quantitative
research — look-ahead leakage, silent overfitting, moving a threshold to meet a
result, reusing an already-searched sample, treating a builder's claim as
evidence, and governance that grows until it replaces the research. The rules
exist to make each of those expensive rather than convenient.

The full reasoning is in [docs/rationale.md](docs/rationale.md). The limits —
what QROS defends against and what it does not — are in
[docs/threat-model.md](docs/threat-model.md).

## Core workflow

```
        Research question
                |
          Preregistration          question, metric, scale, threshold,
                |                  decision rules, kill conditions -- fixed
                |                  and sealed before any outcome exists
               Seal
                |
            MAIN_AGENT             design, implementation, evidence
                |
         Mechanical checks         deterministic; run before review is
                |                  dispatched, because a validator that can
                |                  reject an artifact is cheaper than a reviewer
                |
       INDEPENDENT_REVIEWER        a party that did not produce the work,
                |                  working from a separately constructed
                |                  evidence surface, freezing its own result
                |                  before it sees the producer's
                |
        PASS / PASS_WITH_BACKLOG / HOLD
                |
        +-------+--------+
        |                |
   bounded repair    OWNER gate    the reserved decisions: reveal, disposition,
        |                |         real-data execution, methodology change,
        +------> re-review         public release, destructive mutation
                         |
                 Research disposition
```

Stages, roles and verdicts are defined normatively in [SPEC.md](SPEC.md). This
diagram is a map, not the rules.

## What QROS separates

| Separation | Why it matters |
|---|---|
| Producing work / certifying it | The producer of a consequential artifact is never its sole certifier. A spawned agent is not independent of the agent that spawned it. |
| Builder claim / mechanical evidence / independent verification | Three different kinds of support for a claim. None substitutes for another. |
| What a party knows / when it knows it | Outcome exposure is recorded per party and per target. A reviewer freezes its own result before receiving the producer's. |
| Blocking / non-blocking | A concern is a blocker only if it names one threat class and a concrete failure path on the current or next stage. Everything else is backlog, and work proceeds. |
| Transport failure / implementation failure | A broken delivery leaves a gate unsatisfied without establishing anything about the work under review. |
| Current state / historical record | One page says where the work stands and is rewritten. One log says what was decided and is append-only. |
| Agent authority / Owner authority | A closed list of consequential actions no agent may self-authorize. |

## The worked example

[`examples/synthetic-study/`](examples/synthetic-study/STUDY.md) runs the whole
lifecycle on **entirely fabricated, deterministically generated data**. It is
the shortest honest way to see what the rules do.

A signal was tested against the next period's synthetic return:

| | |
|---|---|
| Builder's result | **0.331216** |
| Independent recomputation | **0.064635** |
| Preregistered threshold | **0.15** |
| Final disposition | **`not_promoted`** |

The builder's implementation contained a one-line look-ahead defect: the signal
window was shifted forward by a period, so the signal dated at *t* contained the
return of *t+1* — the very quantity it was asked to predict. Four deterministic
checks passed on it, because all four were shape checks and a leaked signal has
the same shape as a correct one.

An independent reviewer, working from an evidence surface that did not contain
the builder's code or the builder's number, recomputed the statistic from the
sealed definition and got a different answer. That discrepancy was the finding.

The repair changed one expression and added the regression test the reviewer had
specified. The corrected result — independently recomputed again by a second
reviewer — fell below the preregistered threshold, and the candidate was **not
promoted**. The threshold never moved; the reserved sample was never opened.

**Nothing here is alpha.** The first number was an artefact of the defect, and
the second describes a synthetic process that was designed in advance to sit
below the threshold. It says nothing about any market. The point is that the
workflow prevented a false-looking result from being promoted, and produced a
recorded negative instead — which is a completed research result, not a failure.

## Repository structure

```
SPEC.md                     the single normative source; every rule, stated once
templates/                  the artifact set: preregistration, research state,
                            backlog, decision log, dispatch, review brief,
                            attestation, sample-reuse declaration
schemas/                    JSON Schema (2020-12) enforcing the templates and
                            the closed vocabularies
examples/synthetic-study/   one worked study, end to end, fully synthetic
docs/                       why the rules exist, what they defend against,
                            and how to adopt them
```

## Quick start

Read [`examples/synthetic-study/STUDY.md`](examples/synthetic-study/STUDY.md)
first — it answers eleven questions about the study in order, and takes about
five minutes.

To reproduce the example (standard library only, no dependencies, no network,
no committed data):

```bash
cd examples/synthetic-study

python generate.py --out data                                        # deterministic data
python analyze.py  --data data/sample_development.csv --with-defect   # 0.331216
python checks.py   --data data/sample_development.csv --with-defect   # shape checks pass, leak check fails
python verify.py   --data data/sample_development.csv                 # 0.064635, independently
python analyze.py  --data data/sample_development.csv                 # 0.064635, repaired
python checks.py   --data data/sample_development.csv                 # all checks pass
```

Then read [SPEC.md](SPEC.md) for the rules themselves, and
[docs/adoption.md](docs/adoption.md) to put them to work on a project of your
own.

## Design principles

- **Rigor that terminates.** Review rounds are budgeted; an exhausted budget
  escalates to a human rather than opening another round. If the question can be
  answered and nothing threatens the answer, the project proceeds with backlog
  outstanding.
- **Blindness is about reachability, not instruction.** Telling a reviewer not
  to look at something it can reach does not make it blind. The evidence surface
  is built so the material is absent.
- **Machine checks before model checks.** If a deterministic check can reject an
  artifact, run it first.
- **A check that cannot fail is not protection.** Every governance check must be
  demonstrably capable of failing.
- **Negative results are results.** A preregistered question answered in the
  negative is complete work. A process that only recognises favourable outcomes
  will eventually manufacture one.
- **Roles, not products.** `OWNER`, `MAIN_AGENT`, `INDEPENDENT_REVIEWER`,
  `ARCHITECTURE_REVIEWER` are capabilities. Which model or person fills a role is
  project configuration and forms no part of QROS semantics. The `OWNER` must be
  human.

## What QROS does not do

- It does not find profitable strategies, and adopting it is not evidence that
  any strategy is profitable.
- It does not guarantee that a conforming project's conclusions are correct. It
  raises the cost of an enumerated set of process failures and makes them
  explicit when they occur.
- It does not prevent overfitting. It makes specific overfitting-adjacent
  behaviours — moving a threshold, reusing a burned sample, searching after the
  question is answered — visible and recorded rather than silent.
- It is not a backtesting engine, a signal library, a strategy collection, or a
  data pipeline.
- It makes no claim of suitability for any regulatory, fiduciary, or contractual
  obligation.
- It confers no certification. Conformance is self-declared, and a claim that
  names its own gaps is more useful than one that does not.

## License

This project is licensed under the [MIT License](LICENSE).
