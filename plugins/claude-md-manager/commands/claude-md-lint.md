---
name: claude-md-lint
description: Review an existing CLAUDE.md and flag derivable, bloated, stale, or generic content to trim, keeping only high-value non-derivable context.
---

Review the project's `CLAUDE.md` and recommend what to trim so it stays lean and useful.

## Step 1 — Read it against the repo

Read the current `CLAUDE.md`, then cross-check it against the actual codebase (manifests,
scripts, config, layout). You need both to tell high-value context from noise.

## Step 2 — Flag problems

Go section by section and flag lines that should be cut or tightened:

- **Derivable** — restates what Claude can read directly (dependency lists, full file
  trees, language/tool versions the tooling already reports, obvious directory names).
- **Generic** — best practices that apply to any project and carry no project-specific
  signal ("write clean code", "add tests").
- **Stale** — commands, paths, or conventions that no longer match the repo. Verify
  against the actual scripts/config and call out mismatches.
- **Bloated** — long prose where a bullet would do; duplicated guidance; walls of text.
- **Vague** — rules too fuzzy to act on ("be careful with the database") that should be
  made concrete or dropped.

## Step 3 — Report and propose

Present findings as a checklist: each flagged line, why it's flagged, and the suggested
action (cut / tighten / fix / make concrete). Then note anything **missing** that a strong
CLAUDE.md should have — real build/test commands, gotchas, safety rules (see
`/claude-md-init` for the target shape).

## Step 4 — Offer to apply

Offer to produce the trimmed version. Only rewrite the file after the user approves the
proposed cuts. Preserve genuinely high-value, non-derivable content.
