# Retired QROS 1.0 artifacts

Everything in this directory is a QROS 1.0 artifact **retired by QROS 2.0.0**.
It is kept only so that records made under version 1 — including
`examples/synthetic-study/` — can still be read and checked as they were
written. **Never use these files for new work.**

| Path | What it was |
|---|---|
| `templates/dispatch.md` | review dispatch |
| `templates/review-brief.md` | review brief |
| `templates/attestation.md` | review attestation |
| `schemas/review-dispatch.schema.json` | dispatch schema |
| `schemas/review-attestation.schema.json` | attestation schema |
| `schemas/common.schema.json` | frozen v1 shared definitions, so the two schemas above resolve their references |

Version 2 has no dispatch, brief or attestation, and no `PASS_WITH_BACKLOG`.
Acceptance is now `QROS-ACCEPT-REPRODUCTION-FIRST`. `../../SPEC.md`, Appendix B,
maps every retired identifier to its successor.
