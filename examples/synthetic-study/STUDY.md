# A worked QROS study, end to end

`STUDY_SYNTHETIC_001` · `PROJECT_SYNTHETIC_001`

Everything here is fabricated. The data is generated from a seed, the research
question is invented, and the "edge" under test was designed in advance to be
too small to act on. Nothing in this directory describes a market, an
instrument, or a real result.

The study reaches a **negative** conclusion. That is the point. A process that
only looks successful when the answer is favourable is a process that will
eventually manufacture a favourable answer.

---

## The eleven questions

### 1. What research question was asked?

Does a trailing ten-period mean of a generated return series carry information
about the *next* period's return, at a magnitude worth pursuing?

The statistic is the **information coefficient (IC)**: the Pearson correlation
between the signal at period *t* and the return at period *t+1*.

### 2. What was fixed before seeing the result?

All of it, in `01-preregistration.yaml`, sealed at digest `bb8f114e…` before a
single number was computed:

| Fixed in advance | Value |
|---|---|
| Metric | Pearson IC of signal against next-period return |
| Signal | mean of `r[t-9 … t]` — window **ends at t** |
| Scale | correlation coefficient, −1 to 1 |
| Threshold (SESOI) | **0.15** |
| Decision rule 1 | `IC < 0.15` → `not_promoted` |
| Decision rule 2 | `IC >= 0.15` → `supported` |
| Kill condition | `abs(IC) <= 0.02` → end the line |
| Sample | synthetic periods 0–2999, seed `20260910` |
| Reserved | periods 3000–3999, never opened |
| Planned comparisons | 1 |

The generating process was chosen **analytically**, before generating anything,
so the expected behaviour was known by design rather than discovered by
looking: returns follow a moving-average process where each return shares an
innovation with its predecessor, which puts the true IC near 0.06 — deliberately
below the 0.15 threshold.

### 3. What did the builder do?

Implemented the signal and the statistic in `analyze.py`, ran the deterministic
checks, and reported — in `04-builder-evidence-r1.md`:

```
BUILDER_CLAIM: information_coefficient = 0.331216
```

That clears 0.15 comfortably. Rule 2 would fire and the candidate would be
recorded as `supported`.

### 4. What did mechanical checks establish?

Four deterministic checks ran **before** any review was dispatched
(`QROS-CHECK-MACHINE-BEFORE-MODEL`). All four passed:

| Check | Established |
|---|---|
| signal length | the signal series matches the return series in length |
| no nulls in pairs | 2990 paired observations, every value finite |
| pairing alignment | signals and targets pair one-to-one |
| determinism | two runs of the statistic agree exactly |

These are not decorative. They would have caught a misaligned join, a silent
truncation, or a non-deterministic pipeline.

### 5. What did they NOT establish?

Anything about **when** the information in the signal became available.

Every one of those four checks is a shape check. Each passes *identically* on a
signal that has been handed the answer. The builder said so in writing before
review, rather than letting a wall of green imply more than it showed.

### 6. What did the independent reviewer discover?

A different number.

The reviewer worked inside a **separately constructed evidence surface** — a
directory containing exactly four enumerated, digest-pinned items: the raw
sample, the sealed preregistration, the recomputation script, and the brief.
The builder's implementation and the builder's claimed value were **not in it**.
Not forbidden: absent.

It implemented the sealed definition itself (`verify.py`), computed the IC,
froze the result and its digest, and only then received the builder's figure:

```
independent recomputation (frozen first) = 0.064635
builder claim (delivered after freeze)   = 0.331216
difference                               = 0.266581
tolerance, fixed in the brief in advance = 0.001
```

With the builder's code delivered after the freeze, the cause was one line:

```diff
-    signal[t] = sum(returns[t - k + 2:t + 2]) / k     # window ends at t+1
+    signal[t] = sum(returns[t - k + 1:t + 1]) / k     # window ends at t
```

The window had been shifted forward by one period, so the signal dated at *t*
**contained `r[t+1]`** — precisely the quantity it was supposed to predict.

### 7. Why was it a blocker?

It satisfied the admission test, and the reviewer had to show all four parts:

| Requirement | Satisfied by |
|---|---|
| Exactly one threat class | `RESEARCH_CORRECTNESS` |
| Concrete current-path failure path | the leaked value is the input to the sealed decision table; rule 2 fires, the candidate is recorded `supported`, and the reserved sample gets spent on an artefact |
| Evidence class | `REPRODUCED` — the reviewer produced the discrepancy, it was not argued |
| Smallest affected scope | the window bounds of one expression |

Note what is *not* the failure path: "the number looks wrong". A blocker has to
name what breaks next.

### 8. What was repaired?

One expression (`08-repair.md`), labelled `IMPLEMENTATION_FIX` **before** the
change was applied, citing the sealed clause the code violated. Plus the
reviewer's own `minimal_test`, added as a standing check — truncation
invariance: *recompute the signal on a prefix; if a value inside the prefix
changes when later data is withheld, the signal depends on the future.*

| Implementation | Check 5 |
|---|---|
| round-1 defect | **FAIL** |
| repaired | **PASS** |

The check is demonstrably not vacuous (`QROS-CHECK-NON-VACUOUS`), because the
defective form is retained and it still fails against it.

Not changed: the threshold, the decision rules, the window length, the metric,
the sample, the hypothesis. No amendment to the sealed contract. Amending a
preregistration after outcome exposure to rescue a candidate is the exact
failure sealing exists to prevent.

### 9. What happened after the repair?

Round 2 of the **same issue lineage** — a repair does not earn a fresh budget.
A second, fresh reviewer, again outcome-blind, again recomputing from the
sealed definition, again freezing before receiving comparands:

```
independent recomputation = 0.064635
builder claim             = 0.064635
difference                = 0.000000
verdict                   = PASS_WITH_BACKLOG
```

The round-1 reviewer's number had been right all along. What changed is that
the builder's code now agrees with it. One non-blocking finding went to
backlog; the blocker `B-1` was closed with clearing evidence and **retained** in
the record.

### 10. Why was the candidate not promoted?

```
PREREGISTERED_THRESHOLD = 0.15
VERIFIED_RESULT         = 0.064635
DECISION RULE 1 FIRES   → not_promoted
```

The threshold was fixed before anything was computed and was not touched. The
kill condition (`abs(IC) <= 0.02`) did **not** fire, so the line is not
falsified — the association is real but too small to be worth carrying forward.
The `OWNER` revealed the statistic (`E-3`) and recorded the disposition
(`E-4`). The reserved sample was never opened.

### 11. Why is that still a successful QROS research run?

Because every mechanism did its job:

- **Preregistration held.** The threshold could not move to meet the result,
  because it was sealed and digested before the result existed.
- **Independent review mattered.** A green check suite and a confident builder
  produced 0.331216. Independent recomputation produced 0.064635. Only one of
  those was a measurement.
- **Repair did not imply promotion.** Fixing the defect did not rescue the
  candidate — it revealed that there was nothing to rescue.
- **A negative result is a completed result.** The question was asked, answered,
  verified, and recorded with its provenance.
- **The work stopped.** No second window length, no alternate horizon, no
  post-hoc rescue. The stop rule closed the study.

Had the defect survived, the recorded outcome would have been `supported`, the
reserved sample would have been spent, and the error would have propagated into
whatever came next. That is the failure this whole apparatus is built to make
expensive.

---

## Evidence hierarchy, kept separate

The three never substitute for one another (`QROS-EVIDENCE-SEPARATION`):

| Kind | In this study | Established |
|---|---|---|
| `BUILDER_CLAIM` | `0.331216`, then `0.064635` | what the producer believed |
| `MECHANICAL_EVIDENCE` | 4 checks green (round 1); 5 green (round 2) | specific stated properties, and nothing else |
| `INDEPENDENT_VERIFICATION` | `0.064635`, frozen twice by two seats | that a party without the producer's stake reached the same number |

Note that the builder's *second* claim happens to be correct. It is still a
claim. The verification is what makes it a result.

---

## Reproducing this

Standard library only. No dependencies, no network, no committed data.

```bash
cd examples/synthetic-study

python generate.py --out data                                          # 1. data, seed 20260910
python analyze.py  --data data/sample_development.csv --with-defect     # 2. round-1 claim: 0.331216
python checks.py   --data data/sample_development.csv --with-defect     # 3. checks 1-4 pass, 5 fails
python verify.py   --data data/sample_development.csv                   # 4. independent: 0.064635
python analyze.py  --data data/sample_development.csv                   # 5. repaired:    0.064635
python checks.py   --data data/sample_development.csv                   # 6. all 5 pass
```

`data/` and `frozen_result.json` are regenerated by steps 1 and 4; they are not
committed. Their digests are pinned in the review manifests, so a reader can
confirm the regenerated sample is the one that was reviewed.

## Reading order

| File | What it is |
|---|---|
| `01-preregistration.yaml` | the sealed contract |
| `02-seal.json` | the seal, with the digest method |
| `03-research-state.md` | where the work stands — outcome-clean throughout |
| `04-builder-evidence-r1.md` | the builder's claim and its mechanical support |
| `05-dispatch-r1.yaml` · `06-brief-r1.md` | round-1 review, and the evidence surface |
| `07-attestation-r1.yaml` | round-1 verdict: `HOLD` |
| `08-repair.md` | the one-line bounded repair |
| `09-dispatch-r2.yaml` · `10-brief-r2.md` | round-2 review |
| `11-attestation-r2.yaml` | round-2 verdict: `PASS_WITH_BACKLOG` |
| `12-backlog.yaml` | the closed blocker and two open backlog rows |
| `13-decision-log.yaml` | append-only: two verdicts, reveal, disposition |

## Not exercised here, deliberately

**Sample reuse.** No reuse occurred — the sample was generated for this
preregistration and the reserved portion was never opened. The declaration
template is left unused rather than filled with invented content.

**Transport failure.** Both reviews were validly transported. An invalid-review
branch exists in the attestation template and is enforced by the schema, but
manufacturing a broken dispatch to exercise it would misrepresent what happened.
