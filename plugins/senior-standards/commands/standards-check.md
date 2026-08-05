---
name: standards-check
description: Use to review the current diff against senior engineering standards before committing or opening a PR. Flags band-aid fixes, non-minimal changes, and out-of-scope side effects. Triggers on "standards check", "review my diff", "check for band-aids", "is this minimal", "did I break anything", "senior review".
---

Review the working diff against the three senior engineering principles from Boris Cherny's documented CLAUDE.md. Follow the `senior-standards` skill for the full definitions.

1. Gather the diff. Run `git diff` and `git diff --staged`. If nothing is uncommitted, review the most recently changed files in this session. Read enough surrounding context to judge each change fairly.

2. Evaluate against each principle and collect concrete violations:

   - **1. Minimal change (prefer deleting to adding).** Flag added indirection, dead or unused code, speculative generality (YAGNI), and places where removing code would be simpler than what was added.

   - **2. Root cause, no band-aids.** Flag swallowed errors, symptom-only patches, `TODO`/`HACK`/`temporary`/`workaround` markers, and sleeps/retries/special-cases that mask an underlying defect instead of fixing it. For each, name the likely root cause the change avoided.

   - **3. Only what's necessary, no side effects.** Flag files or lines changed that the task didn't require, drive-by reformatting or renames, and behavior changes outside the stated intent. Check callers of anything touched for regressions.

3. Report as a short list. For each finding give: the principle violated, file and location, why it violates the principle, and the minimal correction. If a principle is clean, say so in one line.

4. End with a verdict: does the diff meet senior-developer standards, or what must change first? Do not make edits — this is a review.
