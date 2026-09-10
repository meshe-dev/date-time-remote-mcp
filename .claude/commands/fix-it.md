---
description: Triage and fix ONE issue red-first through this repo's swarm; deploy is always HELD
---

You are fixing ONE issue end-to-end. Argument: an issue number on
`meshe-dev/date-time-remote-mcp`, or a described bug. Canon: `docs/swarm-core.md` (core P-C)
and `docs/swarm.md`. Read both now.

## 0 — There is ALWAYS an issue
A described bug with no number → `gh issue create` first with symptom, repro, expected;
then work against it. Add `swarm-working` on entry; remove it on every exit path.

## 1 — Triage BEFORE any code
- **Clear defect** → proceed.
- **Judgment** (format, wording, scope, anything altering D-001/D-002 choices) → STOP.
  Comment options + recommendation, label `needs-meshe`, end with the cost footer.
- **Can't repro** → comment asking for the missing detail; do not guess.

## 2 — Fix RED-first
1. Pin a contract for the fix (core §4; a Rejections row if an input is involved).
2. `swarm-test-writer` writes the failing regression test in the right tier; confirm it
   fails for the right reason.
3. `datetime-engineer` makes the minimal change; scoped test run only; docs in-dispatch.

## 3 — Gate
`swarm-verifier` with contract + affected paths; `swarm-qa` if the tool surface changed.
FAIL → back to the engineer with the numbered findings; stuck-detector applies.

## 4 — Deploy: HELD
Commit on green on a `fix/<n>` branch. Comment on the issue: root cause, files, the
regression test, the commit SHA, the verifier's docker proof, and the exact commands for
meshe to deploy on awarm. Label `needs-meshe-deploy`. Never run the deploy.

**Unsatisfiable requirement = blocker (core C-9, meshe's ruling):** a contract row the environment contradicts is parked as `BLOCKED:` with evidence, options and a recommendation; everything that depends on it waits, everything else continues; the run finishes and reports the blocker first. Never amend the row, never choose, never write a D-entry (an O-row at most), never stop and wait for meshe.

## 5 — Escalate, don't loop
Three identical failures with zero progress → `blocked` label, comment with attempts and
hypotheses.

## 6 — Cost footer
Every terminal comment ends with the cost footer per `docs/swarm.md`.
