---
name: log-lesson
description: Use right after Claude makes a mistake, gets corrected, or repeats an error you've seen before, to preserve the lesson so it persists into future sessions. Triggers on "log this lesson", "remember this", "don't do that again", "capture what went wrong", "write this to CLAUDE.md", "make a skill for this".
---

Something just went wrong (or was corrected). Capture the lesson so it durably shapes future sessions instead of being forgotten.

Follow the `mistake-capture` skill to decide the right home for the lesson and to keep it lean.

Steps:

1. **Reconstruct the mistake.** In one or two sentences, state what actually went wrong, why it happened, and what the correct behavior is. Focus on the general rule, not the one-time specifics. If it is unclear, ask the user to confirm the takeaway before writing.

2. **Choose the destination** (see the skill for the decision rule):
   - A **one-off fact or constraint** ("this repo uses pnpm, not npm") → append a single concise line to the most appropriate `CLAUDE.md` (project-level `./CLAUDE.md` by default; user-level `~/.claude/CLAUDE.md` only if it is genuinely universal). Keep CLAUDE.md lean — no paragraphs, no duplication of an existing rule.
   - A **repeatable procedure or multi-step workflow** ("how to add a migration here") → scaffold a skill under `.claude/skills/<name>/SKILL.md` with a precise `description:` trigger and a lean body, pushing depth to `reference/` if needed.

3. **Write it.** Before appending to CLAUDE.md, read the file and check the rule is not already present or contradicted; if a related rule exists, tighten it rather than adding a duplicate. Phrase rules as imperative instructions ("Always…", "Never…", "Prefer…").

4. **Confirm.** Report what you wrote, where, and why that destination — and show the exact line or skill created.
