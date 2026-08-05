---
name: loop-task
description: Turn a repeatable task into a recurring routine using Claude Code's /loop, choosing interval vs. self-paced and setting a clear stop condition.
args: "[interval like 5m (optional)] [the task or /slash-command to repeat]"
---

Set up a recurring routine for: **$ARGUMENTS**

Claude Code has a built-in `/loop` that re-runs a prompt or slash command on a
schedule. Your job is to configure it correctly — the right cadence and, above
all, a stop condition — so it does useful work without running away. Follow the
`loop-routines` skill for the taxonomy and safeguards.

Steps:

1. **Confirm the task is genuinely repeatable.** Loops fit polling, watching,
   and periodic checks ("re-run tests until green", "check the deploy every 5
   minutes", "keep triaging new PRs"). A one-off task should not be a loop —
   just do it once.

2. **Pick the loop mode:**
   - **Interval loop** — a fixed cadence like `5m`, `30s`, `1h`. Best when the
     thing you are watching changes on the clock (deploy status, a queue, an
     external job). Form: `/loop 5m <prompt or /command>`.
   - **Self-paced loop** — omit the interval and the model decides when to run
     the next iteration, continuing as soon as it is ready. Best for iterate-
     until-done work (fix failures, refine output) where wall-clock spacing adds
     nothing. Form: `/loop <prompt or /command>`.

3. **Define the stop condition explicitly.** Every loop needs an exit: a success
   state ("stop when the test suite passes"), a bound ("at most 10 iterations"),
   or a time limit. State it in the prompt you hand to `/loop` so each iteration
   can decide whether to stop. A loop with no stop condition is a bug.

4. **Emit the exact command** for the user to run, for example:
   ```
   /loop 5m check the CI status of the current branch; stop and summarize once it succeeds or fails
   ```
   or a self-paced form:
   ```
   /loop run the test suite; fix the first failure each pass; stop when all tests pass or after 8 passes
   ```

5. **Add safeguards.** Recommend a max-iteration or time cap, note that the user
   can stop the loop at any time, and warn against loops that take irreversible
   or costly actions each pass without a guard.

Report the chosen mode, the cadence (or why self-paced), the stop condition, and
the exact `/loop` command.
