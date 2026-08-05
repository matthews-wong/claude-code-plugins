# permission-optimizer

Reduce repeated permission prompts by turning frequently denied or repeatedly-approved
**read-only** tool calls into a tight, exact-match `permissions.allow` allowlist for
`.claude/settings.local.json`.

## What it does

- Reviews recent tool-call activity to find what keeps prompting.
- Filters strictly to read-only commands (never write/exec/network/destructive).
- Proposes precise `Bash(cmd:*)` / MCP matchers and merges them without clobbering
  existing entries.
- Always shows the final allowlist for confirmation before writing.

## Components

- **Command:** `/optimize-permissions` — analyze and propose an allowlist.
- **Skill:** `permission-optimizer` — the read-only safety rules and rule-format reference
  Claude applies whenever prompt-fatigue comes up.

## Usage

Run `/optimize-permissions` after a session where the same safe commands kept asking for
approval. Review the proposed JSON, then let Claude merge it into
`.claude/settings.local.json`.

## Safety

Only read-only commands are ever proposed. Anything that could mutate state, execute code,
or touch the network is excluded by design — it keeps prompting, on purpose.

Author: Matthews Wong · License: MIT
