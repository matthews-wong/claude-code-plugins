# e2e-verifier

A checklist-driven skill (plus a command) for **end-to-end verification** of a
change before it's handed to a human. Unit tests prove units; this proves the whole
change works through the real running system — the rigorous end of "Step 1: verify."

## What it installs

- **Skill `e2e-verification`** (`skills/e2e-verification/SKILL.md`) — a checklist
  Claude follows to: establish what "working" means, reproduce the happy path
  through the real entry point, verify at least one edge case, guard against
  regressions, capture concrete evidence, and only then give a ready/not-ready
  verdict.
- **Command `/e2e-check`** — invokes the skill against the current change (or a
  specified focus) and produces the checklist report.

## How to use

- Run `/e2e-check` to verify the current working changes end-to-end.
- Run `/e2e-check "the new /login endpoint"` to focus on a specific feature.

The skill also activates automatically when a task calls for end-to-end
verification, thanks to its `description`.

## Notes

- The skill explicitly requires **evidence** (real commands and output) and forbids
  claiming success that wasn't observed — if the system can't be run in the current
  environment, it hands off exact reproduction steps and marks those items
  "could-not-run."
- It complements `verify-before-review` (tests/lint/build) and the review agents:
  run e2e verification, then review.
