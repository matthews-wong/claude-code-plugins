---
description: How to define scheduled routines in Claude Code — cron-style cloud agents that run a task on a recurring cadence. Covers cadence selection, guardrails for unattended execution, self-contained task prompts, and worked examples (nightly PR triage, dependency-update check). Use when setting up recurring automated agent work.
---

# Routine Scheduler

A routine is a scheduled cloud agent: Claude Code runs a task automatically on a
cron-style cadence, without a human starting the session. Routines are how you
move recurring, mechanical, or vigilance-style work off a person's plate —
nightly triage, periodic checks, weekly digests.

This skill describes routines conceptually and honestly. Claude Code exposes
scheduling through a native routines capability (a `schedule` skill / routines
interface and, in the product, a scheduled-agents UI). Register routines through
that native capability rather than hand-rolling cron plumbing. Where exact
options matter, consult the official Claude Code documentation — do not assume
flags that may vary by version.

## What makes a good routine

Routines run unattended, so the bar for reliability is higher than an
interactive session:

- **Unambiguous goal.** The task prompt must define "done" with no human in the
  loop to clarify.
- **Idempotent.** Running twice should not double-act. Check for its own prior
  output (an existing comment, an open PR) before creating a new one.
- **Bounded per run.** Cap the work — e.g. "triage up to 20 new PRs," not "all
  PRs ever." Predictable cost and runtime.
- **Reads more than it writes.** Prefer producing summaries, reports, draft PRs,
  and notifications over taking irreversible action.
- **Fails safe.** On uncertainty it should surface the issue to a human, not
  guess and act.

## Choosing a cadence

Match the cadence to how fast the underlying signal changes and how urgent a
response is:

- **Nightly** (`0 3 * * *`) — triage, digests, health checks. Run in off-hours
  so heavy work doesn't contend with the workday.
- **Weekday mornings** (`0 6 * * 1-5`) — anything a person acts on that day, so
  results are fresh when they log in.
- **Weekly** (`0 4 * * 1`) — dependency updates, slow-moving audits, trend
  reports.
- **Hourly / frequent** — only for genuinely time-sensitive signals; watch cost
  and rate limits.

Always pin a timezone so "morning" means the team's morning. State the schedule
back in both human and cron form, e.g. `0 6 * * 1-5` = 06:00 on weekdays.

## Writing the task prompt

The routine executes in a fresh session with no memory of the setup
conversation. The task prompt must be fully self-contained:

- The goal and the definition of a successful run.
- The repository and specific paths/labels/branches it operates on.
- The ordered steps to take.
- The guardrails — what it must never do autonomously (merge, force-push,
  delete, deploy, message customers).
- The exact output: where results go (draft PR, issue comment, report file,
  chat notification) and in what format.

## Worked example: nightly PR triage

> Cadence: `0 3 * * *`, timezone Asia/Jakarta.
> Task: For each PR opened or updated in the last 24h in `org/repo` that has no
> `triaged` label: read the diff and description, post a summary comment
> covering scope/risk/test coverage, apply size and area labels, and request
> the appropriate reviewers from CODEOWNERS. Add the `triaged` label so the next
> run skips it. Never approve, merge, or close a PR. If a PR looks risky or
> ambiguous, add the `needs-human` label and note why. Cap at 20 PRs per run.

Idempotent (the `triaged` label), bounded (20/run), read-biased (comments and
labels, never merges), fails safe (`needs-human`).

## Worked example: weekly dependency-update check

> Cadence: `0 4 * * 1`, timezone Asia/Jakarta.
> Task: In `org/repo`, check for outdated dependencies and known advisories. For
> low-risk patch/minor bumps with green expectations, open ONE draft PR grouping
> the updates, with a changelog summary and the reasoning per package. For major
> bumps or anything with breaking-change notes, open a tracking issue instead of
> a PR and summarize the migration effort. Never push to the default branch and
> never enable auto-merge. If a prior draft PR from this routine is still open,
> update it instead of opening a second.

## Managing routines

Keep routines discoverable and editable: give each a clear name, review their
output for the first few runs to confirm the prompt behaves, and disable or
narrow any routine that produces noise. Treat a routine's task prompt like code
— when the repo's conventions change, update the prompt.

## Anti-patterns

- Vague goals ("keep the repo healthy") with no concrete success criteria.
- Autonomous irreversible actions (merging, deploying, deleting) with no human
  gate.
- Non-idempotent routines that re-post or re-open on every run.
- Unbounded scope that makes cost and runtime unpredictable.
- Cadence mismatched to the signal (hourly for a weekly-moving concern).
