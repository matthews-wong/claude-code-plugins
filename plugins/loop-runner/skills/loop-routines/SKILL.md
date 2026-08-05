---
name: loop-routines
description: Use when a task should repeat on a schedule or until a condition is met. Explains Claude Code's /loop taxonomy — interval loops (fixed cadence) vs. self-paced loops (model decides when to continue) — and how to set stop conditions and avoid runaway loops. Triggers on "loop", "run this every N minutes", "keep running until", "recurring task", "poll for status".
---

# Loop Routines

Claude Code's `/loop` re-runs a prompt or a slash command repeatedly instead of
once. It turns a one-shot instruction into a routine. The whole art is choosing
the cadence and giving the loop a way to stop.

## The two modes

### Interval loop — fixed cadence
```
/loop 5m <prompt or /command>
```
Runs on a wall-clock interval (`30s`, `5m`, `1h`, ...). Use when what you're
watching changes on the clock and there's no point checking faster:
- Poll a deploy or CI job every few minutes.
- Watch a queue, an inbox, or an external service periodically.
- Any "check on X every N" routine.

### Self-paced loop — model decides
```
/loop <prompt or /command>
```
Omit the interval and the model starts the next iteration as soon as it's ready,
with no forced wait. Use for iterate-until-done work where spacing adds nothing:
- Run tests, fix the first failure, repeat until green.
- Refine a draft or a data extraction across passes.
- Any converging task measured by progress, not by the clock.

Rule of thumb: **time-driven → interval; progress-driven → self-paced.**

## Stop conditions are mandatory

A loop without an exit is a runaway. Give every loop at least one:

- **Success state** — "stop once the suite passes" / "stop when status is done".
- **Iteration bound** — "at most 10 passes".
- **Time limit** — "for up to 30 minutes".

State the stop condition inside the prompt handed to `/loop` so each iteration
can evaluate it and end the loop when met. Prefer combining a success state with
a hard bound so a stuck loop still terminates.

## Avoiding runaway loops

- **Always bound it.** Even a success-state loop should carry a max-iteration or
  time cap as a backstop.
- **Watch irreversible/costly actions.** Don't loop something that spends money,
  sends messages, or mutates production each pass without a guard and a tight cap.
- **Make progress observable.** Each iteration should report what changed so a
  no-progress loop is obvious and can be stopped.
- **You can stop it anytime.** The loop is interruptible; end it manually if it
  stops making progress.
- **Don't loop the un-loopable.** One-off tasks and anything needing human
  judgment each pass are a poor fit — run them once.

## Related

For heavier, unattended scheduling (cron-style cloud routines) consider a
scheduled agent instead of an in-session `/loop`. `/loop` is for routines you
run and watch within a session.
