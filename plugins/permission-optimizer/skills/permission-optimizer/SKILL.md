---
name: permission-optimizer
description: Use when a user is repeatedly prompted to approve the same safe, read-only tool calls and wants to reduce friction — phrasings like "stop asking me to approve git status / ls / rg" or "add these commands to the allowlist". Analyzes recently denied or repeatedly-prompted tool calls, isolates the read-only ones, and proposes exact-match permissions.allow rules for .claude/settings.local.json. Never allowlists write, execute, network, or destructive commands.
---

# Permission Optimizer

Turn repeated permission prompts into a small, safe, exact-match allowlist so routine
read-only work stops interrupting the user, while every mutating action still requires
explicit approval.

## The one hard safety rule

Only ever propose read-only commands for the allowlist. If a command reads state and
produces no side effects, it is a candidate. If there is any chance it writes, deletes,
moves, installs, sends over the network, changes config, or executes arbitrary code, it
is NOT a candidate — even if the user is annoyed by the prompts. When in doubt, leave it
out and let it keep prompting.

### Read-only (safe to propose)

- `git status`, `git log`, `git diff`, `git show`, `git branch`, `git remote -v`
- `ls`, `cat`, `head`, `tail`, `wc`, `pwd`, `find` (without `-delete`/`-exec`)
- `grep`, `rg`, `fd` (search only)
- `npm ls`, `npm outdated`, `pip show`, `pip list`, `cargo tree`
- `node --version`, `python --version`, tool `--help` / `--version` invocations
- Read-only MCP tools: `list_*`, `get_*`, `search_*`, `query_*` (verify they do not mutate)

### Never propose (mutating / side-effecting)

- Writes/moves/deletes: `rm`, `mv`, `cp`, `mkdir`, `touch`, `sed -i`, `>` / `>>` redirects
- Package/build side effects: `npm install`, `pip install`, `cargo build`, `make`
- Execution: `node script.js`, `python script.py`, `bash`, `eval`, `npx`
- Network: `curl`, `wget`, `git push`, `git pull`, `git fetch`, `gh` mutations
- VCS state changes: `git commit`, `git add`, `git checkout`, `git reset`, `git rebase`
- Any MCP tool whose name implies mutation: `create_*`, `update_*`, `delete_*`, `send_*`

## Workflow

1. **Gather signal.** Ask the user which commands keep prompting, or review the recent
   session for tool calls that were denied or repeatedly approved. Count frequency —
   prioritize the ones that interrupt most often.
2. **Filter to read-only.** Drop everything mutating using the rules above. This is the
   step you must not shortcut.
3. **Write exact-match rules.** Prefer precise `Bash(<cmd>:*)` prefixes over broad
   wildcards. `Bash(git status:*)` is good; `Bash(git:*)` is too broad because it would
   also allow `git push`. For MCP, use the fully qualified tool name.
4. **Choose scope.** Propose additions to the project-local `.claude/settings.local.json`
   (gitignored, personal) unless the user asks for shared `.claude/settings.json`.
5. **Show the diff and confirm.** Present the exact JSON to be merged and the reasoning
   per rule. Never write the file without the user seeing the final allowlist.

## Rule format reference

Permissions live under `permissions.allow` as an array of matcher strings:

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(rg:*)",
      "Read(./**)"
    ]
  }
}
```

Rules of thumb:

- `Bash(cmd:*)` matches that command with any arguments — keep the command specific.
- Merge into any existing `allow` array; never clobber the user's current entries.
- Keep the list short. A tight allowlist of the top offenders beats a sprawling one.

## What to hand back

A ready-to-merge JSON snippet, a one-line justification per rule stating why it is
read-only, and an explicit note of any prompted commands you deliberately excluded
because they mutate state.
