---
name: schedule-routine
description: Design and set up a scheduled routine (a cron-style cloud agent) that runs a Claude Code task on a recurring cadence, such as nightly PR triage or a weekly dependency-update check.
args: "<what the routine should do, and how often>"
---

You are helping the user set up a scheduled routine. The request is:

$ARGUMENTS

A routine is a cron-style cloud agent: Claude Code runs a defined task
automatically on a schedule, without the user starting a session. Work through
these steps with the user.

1. Clarify the routine's contract. Restate in one sentence: what task runs, on
   what cadence, and what a successful run produces (a comment, a PR, a report,
   a notification). If the cadence or the definition of "done" is ambiguous, ask
   one focused question before proceeding — a scheduled task that runs
   unattended must have an unambiguous goal.

2. Confirm the cadence. Translate the user's phrasing ("every night,"
   "weekday mornings," "weekly") into a concrete schedule (a cron expression and
   timezone). State it back plainly, e.g. "0 6 * * 1-5 in Asia/Jakarta = 06:00
   on weekdays." Pick a low-traffic time for heavy routines.

3. Scope the work for unattended execution. A good routine is idempotent, has a
   bounded amount of work per run, reads more than it writes, and fails safely.
   Spell out guardrails: what it must NOT do autonomously (e.g. never merge or
   force-push without a human), and how it should surface results (open a draft
   PR, post a summary comment, write a report file) rather than taking
   irreversible action.

4. Create the routine. Claude Code manages scheduled cloud agents through its
   built-in scheduling capability. Use the `schedule` skill / routines interface
   to register the routine with the task prompt, the cron schedule, and the
   target repository. Do not invent CLI flags — drive it through the native
   scheduling tool. If that capability is not available in this environment, say
   so honestly and give the user the exact task prompt and cron schedule so they
   can register it from the Claude Code UI.

5. Write the routine's task prompt to be fully self-contained: the routine runs
   in a fresh session with no memory of this conversation. It must state its own
   goal, the repo/paths it operates on, the steps to take, the guardrails, and
   the exact output/notification expected.

6. Confirm and summarize: the routine name, schedule (human-readable + cron),
   what it does each run, its guardrails, and how the user will see results and
   later edit or disable it.

Consult the `routine-scheduler` skill for cadence patterns, guardrails, and
worked examples like nightly PR triage and dependency-update checks.
