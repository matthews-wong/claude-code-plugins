---
name: senior-standards
description: Use while writing, changing, or reviewing code to hold to senior-developer standards. Applies three principles — make every change minimal (prefer deleting lines to adding), find and fix root causes (no band-aids or temporary hacks), and touch only what's necessary (no side effects, don't introduce new bugs). Triggers on "senior standards", "root cause", "minimal change", "no band-aid", "don't break other things", "keep it simple".
---

# Senior engineering standards

Three principles documented at the bottom of Boris Cherny's CLAUDE.md. Apply them to every change you make and every diff you review.

## 1. Make every change as simple as possible — minimal code

Prefer the smallest change that fully solves the problem. **Prefer deleting lines to adding them.** Every added line is future maintenance; every deleted line is a liability removed. Before adding code, ask whether existing code can be reused, or whether the goal can be met by removing something instead. Avoid speculative generality (YAGNI): don't build for requirements that don't exist yet.

Apply while coding:
- Reach for the simplest construct that works; don't add layers, options, or abstractions with a single caller.
- If a change grows large, stop and ask whether the approach is right.

## 2. Find the root cause — no band-aids

Fix the actual cause, not the symptom. **No temporary fixes, no hacks, no papering over.** A `try/catch` that swallows an error, a special-case branch that hides a bad state, a sleep that masks a race — these are band-aids that defer and compound the problem. Hold to what a senior developer would ship: understand *why* it's broken, then fix *that*.

Apply while coding:
- Before fixing, state the root cause in one sentence. If you can't, investigate more.
- If a true fix is out of scope, say so explicitly and flag it — don't quietly patch the symptom.

## 3. Touch only what's necessary — no side effects

Change only what the task requires. **Don't introduce new bugs while fixing old ones.** Unrelated refactors, drive-by renames, reformatting, and "while I'm here" changes expand the blast radius and hide the real change in review. Preserve existing behavior everywhere you're not deliberately changing it.

Apply while coding:
- Keep the diff scoped to the task; split unrelated improvements into their own change.
- Check callers and dependents of anything you touch — a local fix must not break a distant caller.

## Using these while reviewing

For each principle, scan the diff and flag concrete violations:
- **Simplicity:** added indirection, dead code, needless options, additions where a deletion would do.
- **Root cause:** swallowed errors, symptom-only patches, TODO/HACK/temporary comments, magic sleeps/retries hiding a real defect.
- **Scope:** files or lines changed that the task didn't require; behavior changes outside the stated intent.

Report violations with file, location, why it breaks the principle, and the minimal correction. Attribute the principles to Boris Cherny's documented CLAUDE.md.
