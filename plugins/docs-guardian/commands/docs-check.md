---
name: docs-check
description: Detect documentation likely made stale by recent code changes and suggest updates.
args: "[git-range] (optional, e.g. HEAD~5..HEAD or main..HEAD; defaults to uncommitted changes)"
---

Find documentation that recent code changes have probably made stale, and
propose concrete edits.

Steps:

1. Determine the changed source files:
   - If a git range is given, use `git diff --name-status <range>`.
   - Otherwise use `git status --porcelain` and `git diff` for uncommitted work.

2. Run the drift scanner for a fast first pass:
   ```sh
   sh "${CLAUDE_PLUGIN_ROOT}/scripts/docs-scan.sh"
   ```
   It lists changed source files, locates doc files (README*, docs/**, *.md,
   CHANGELOG*, mkdocs/docusaurus/sphinx configs), and heuristically flags likely
   drift (public API/signature/flag/env-var/config changes). It never fails
   (exit 0); treat its output as leads, not verdicts.

3. For each changed source file, reason about what documentation it touches.
   Load the skill `docs-drift` for the signal catalog. High-signal triggers:
   - Public function/class/endpoint signature changed -> API docs, examples.
   - CLI flags or subcommands changed -> README usage, `--help` snippets.
   - Env vars / config keys added, removed, renamed -> config docs, `.env.example`.
   - Dependency or min version bump -> install/requirements docs.
   - Default value or behavior changed -> docs describing that behavior.
   - New feature/module -> README feature list, CHANGELOG.

4. Cross-check the docs: search the doc files for references to the changed
   symbols, flags, or values and see whether they still match the code.

5. Report:
   - A short list of docs that are probably stale, each with the reason and the
     specific line/section to update.
   - Proposed edits (or a diff) where you are confident.
   - Explicitly note docs you checked that are still accurate, so the user knows
     the scan was thorough.

Only flag real mismatches. Do not rewrite prose style or invent doc conventions
the project does not use. If nothing looks stale, say so.
