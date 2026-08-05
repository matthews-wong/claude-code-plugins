# Session failure patterns — detail

## 1. Kitchen-sink session

**Symptoms:** the conversation has fixed a bug, then answered a config question, then started a new feature — all in one session. Earlier topics no longer relate to the current one. Responses start referencing things that are no longer relevant.

**Why it hurts:** every token of stale history competes for attention and context budget. The model may re-apply assumptions from a finished task to the new one.

**Action:** `/clear` when moving to an unrelated task. Rule of thumb: new task, new context.

## 2. Correcting over and over

**Symptoms:** you've said "no, not like that" about twice on the same point and it's still wrong. Each turn adds another correction, and the model now has several contradictory attempts in view.

**Why it hurts:** the accumulated failed attempts and corrections become the dominant context, anchoring the model on the very approach that isn't working. More corrections deepen the loop.

**Trigger:** ~2 failed corrections on the same issue.

**Action:** stop patching. Extract learnings, `/clear`, and re-prompt.

### Before / after re-prompt

**Before (doom loop):**
> "No, that's still wrong. The date is off by one again. No — timezone. Still wrong..."

**After (fresh prompt built from learnings):**
> "Format a UTC timestamp as a local date string in `src/date.ts`.
> Learned: naive `toISOString().slice(0,10)` is off-by-one for users west of UTC because it renders in UTC, not local time. The bug is timezone handling, not the format.
> Approach: use the Intl.DateTimeFormat API with the user's timezone. Add a unit test covering a UTC-evening timestamp for a US-Pacific user."

The after version front-loads the exact insight the loop paid for, in a clean context.

## 3. Infinite exploration

**Symptoms:** many searches/reads, growing context, no decision or edit. "Let me also check…" with no convergence.

**Why it hurts:** raw exploration output crowds out room for the actual work, and the thread loses the thread.

**Action:**
- **Delegate to a subagent** — have it do the searching and return only the conclusion, keeping this session's context clean.
- Or, if it's one coherent long task low on room, **`/compact`** to condense and continue.

## Quick decision guide

| Situation | Do |
|-----------|-----|
| Switching to an unrelated task | `/clear` |
| ~2+ failed corrections, same issue | `/clear` + re-prompt with learnings |
| Long coherent task, low on context, going well | `/compact` |
| Investigation ballooning context | scope it to a subagent |
| Healthy and on-task | keep going — don't clear for its own sake |
