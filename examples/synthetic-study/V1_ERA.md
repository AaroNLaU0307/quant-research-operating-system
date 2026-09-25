# This is a QROS 1.0 example

This study was produced under **QROS 1.0** and is kept unchanged as a worked
example. Records made under an earlier version are never re-judged under a later
one.

**Retired machinery.** `05-dispatch-r1.yaml`, `06-brief-r1.md`,
`07-attestation-r1.yaml`, `09-dispatch-r2.yaml`, `10-brief-r2.md` and
`11-attestation-r2.yaml` show the v1 review dispatch, brief and attestation, and
the verdict `PASS_WITH_BACKLOG`. All are retired. Their templates and schemas now
live in `../../retired/v1/`; the other artifacts' schema pointers and role names
are v1 too.

**Under QROS 2.0.0** the same study would instead:

- seal a mechanical verdict rule mapping the IC to a research status and a
  disposition, with a truncation-invariance validity check that must pass before
  the primary is read;
- be accepted by the `DELEGATE` reproduction-first
  (`QROS-ACCEPT-REPRODUCTION-FIRST`), not by dispatched reviewers.

**Still valid.** The research content, `verify.py` and `checks.py` still
illustrate sealing before exposure, the separation of builder claim, mechanical
evidence and independent recomputation, and change labels applied before a
repair.
