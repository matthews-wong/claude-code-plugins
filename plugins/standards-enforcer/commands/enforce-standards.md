---
name: enforce-standards
description: Check the current diff against the org coding-standards profile and report violations with fixes.
args: "[diff range] — optional git ref/range (default: unstaged + staged changes vs HEAD)"
---

Review the change set against the organization's coding-standards profile. Diff scope: `$ARGUMENTS` (default: current uncommitted changes; otherwise the given git range).

Procedure:

1. **Get the diff.** Use git to obtain the changed hunks for the scope above. Review only changed lines and their immediate context — do not re-audit the whole repo.

2. **Load the standards profile.** Load the `standards-enforcer` skill and read its `reference/standards-profile.md`, which the team edits. Treat that file as the source of truth; if the repo has its own linter/style config that conflicts, note the conflict and prefer the repo's config.

3. **Check each rule category** against the diff: naming conventions, file organization, error handling (no swallowed errors, boundary validation), no secrets or leftover debug prints/console logs, and docstrings on new/changed public APIs. Only report issues introduced or touched by this diff.

4. **Grade findings** by severity: Blocker (secrets, swallowed critical errors), Warning (naming, missing docstring), Nit (style). Cite the exact profile rule for each finding.

5. **Output** a table (File:Line | Severity | Rule | Finding | Suggested fix). Summarize with counts per severity and a pass/fail verdict (fail if any Blocker). Offer to apply the mechanical fixes.

Be precise and cite line numbers from the diff. Do not invent rules that are not in the profile; if you believe a rule is missing, suggest it as a profile addition rather than enforcing it silently.
