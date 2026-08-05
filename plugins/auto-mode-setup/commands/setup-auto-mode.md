---
name: setup-auto-mode
description: Guide the user through enabling permissions.defaultMode "auto" in ~/.claude/settings.json and pre-approving a vetted set of safe bash/MCP commands.
---

Walk the user through enabling auto mode safely and honestly.

First, explain what auto mode actually does, without overselling:

- Setting `permissions.defaultMode` to `"auto"` lets Claude Code auto-approve routine,
  low-risk actions instead of prompting for every one.
- Approval is decided by a safety classifier that judges whether an action is routine and
  low-risk. It is a heuristic, not a guarantee.
- If the classifier is unavailable, auto mode falls back to normal (default) permission
  behavior and prompts as usual — it fails safe, not open.
- Explicit `permissions.allow` entries still take effect and `permissions.deny` entries
  still block. Auto mode complements an allowlist; it does not replace `deny` guardrails.

Then guide the configuration:

1. **Confirm scope.** Auto mode as a personal default belongs in the user-level file
   `~/.claude/settings.json`. Confirm the user wants it global before editing.

2. **Set the mode.** Add or update `permissions.defaultMode` to `"auto"`, merging with
   existing settings rather than overwriting the file.

3. **Pre-approve a vetted safe set.** Offer to add exact-match `permissions.allow` rules
   for the routine commands the user relies on — read-only VCS/inspection (`git status`,
   `git diff`, `git log`, `rg`, `ls`) and any low-risk build/test commands they trust
   (e.g. `Bash(npm test:*)`). Keep matchers specific.

4. **Keep a deny floor.** Suggest `permissions.deny` entries for anything that should
   never auto-run regardless of mode (e.g. `Bash(rm -rf:*)`, `Bash(git push:*)`, secret
   files via `Read(./.env)`), so a classifier miss cannot cause the worst outcomes.

5. **Show the merged JSON and confirm.** Present the exact settings diff, explain each
   change, and only write after the user approves. Remind them they can revert by setting
   `defaultMode` back to `"default"` or `"plan"`.

Do not claim auto mode is fully safe or that it never makes mistakes. Frame it as reduced
friction with a safety classifier and a fail-safe fallback, backed by explicit allow/deny
guardrails the user controls.
