# loop-runner

Turn a repeatable task into a recurring routine with Claude Code's built-in
`/loop`. This plugin helps you pick the right loop mode, set a stop condition,
and avoid runaway loops.

## Components
- `commands/loop-task.md` — `/loop-task` configures a routine and emits the exact
  `/loop` command to run.
- `skills/loop-routines/SKILL.md` — the `/loop` taxonomy and safeguards.

## The taxonomy
- **Interval loop** — `/loop 5m <task>` runs on a fixed cadence; best for
  time-driven watching (deploy/CI/queue polling).
- **Self-paced loop** — `/loop <task>` lets the model decide when to continue;
  best for progress-driven, iterate-until-done work.

Every loop needs a stop condition (success state, iteration bound, or time
limit) plus a backstop cap so it can never run away.

## Usage
```
/loop-task 5m check the deploy status; stop when it finishes
/loop-task run the tests; fix the first failure each pass; stop when green or after 8 passes
```

Author: Matthews Wong — MIT License.
