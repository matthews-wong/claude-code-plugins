# docs-guardian

Keep documentation honest. Flags when code changes likely make docs, README, or
API references stale and proposes the specific updates.

## Components

- **`/docs-check [git-range]`** — maps changed source files to the docs they
  affect, verifies real mismatches, and suggests concrete edits.
- **Skill: docs-drift** — a signal catalog (signatures, CLI, config, versions,
  behavior) and per-doc-type checklist in
  `skills/docs-drift/reference/doc-map.md`.
- **Hook (PostToolUse)** — a once-per-session nudge to run `/docs-check` after
  editing source (skips doc edits). Non-blocking.
- **`scripts/docs-scan.sh`** — POSIX sh; lists changed source files, locates doc
  surfaces, and heuristically flags drift. Always exits 0.

## Philosophy

A stale doc misleads with authority — worse than no doc. The plugin flags only
genuine mismatches, respects the project's existing doc style, and prefers
surgical edits over rewrites.

Author: Matthews Wong · License: MIT
