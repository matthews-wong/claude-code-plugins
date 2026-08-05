---
name: optimize-permissions
description: Analyze recently denied/repeated tool calls and propose a safe, read-only permissions.allow allowlist for .claude/settings.local.json.
---

Help the user cut down repeated permission prompts by proposing a safe allowlist.

Follow these steps:

1. **Collect the offenders.** Review the recent session and identify tool calls that were
   denied or that the user has approved repeatedly. If the signal is thin, ask the user:
   "Which commands keep asking you for permission?" List each candidate with an
   approximate frequency so the most disruptive ones surface first.

2. **Filter ruthlessly to read-only.** Keep only commands that read state and cause no
   side effects (e.g. `git status`, `git diff`, `git log`, `ls`, `cat`, `rg`, `grep`,
   `npm ls`, read-only MCP `list_*`/`get_*`/`search_*` tools). Discard anything that could
   write, move, delete, install, execute, push, or hit the network — even if it prompts
   often. When unsure whether a command mutates state, exclude it. State this rule to the
   user explicitly.

3. **Write exact-match rules.** Use precise matchers like `Bash(git status:*)` rather than
   broad ones like `Bash(git:*)` that would leak in mutating subcommands. Use fully
   qualified names for MCP tools.

4. **Present a mergeable snippet.** Show the exact JSON to add under `permissions.allow`
   in `.claude/settings.local.json`, merging with any existing entries rather than
   replacing them. Give a one-line read-only justification per rule, and list any
   frequently-prompted commands you intentionally left out because they mutate state.

5. **Confirm before writing.** Only edit the settings file after the user approves the
   proposed allowlist. If they decline, leave the file untouched.

Never propose write, execute, network, or destructive commands under any circumstance.
