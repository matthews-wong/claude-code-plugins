# claude-md-manager

Create and maintain a lean, high-signal project `CLAUDE.md` — the persistent memory Claude
Code loads every session. Capture the build/test commands, conventions, gotchas, and
safety rules that matter; leave out everything Claude can already derive from the repo.

## What it does

- Scaffolds a strong, skimmable `CLAUDE.md` from the actual project.
- Lints an existing `CLAUDE.md`, flagging derivable, generic, stale, bloated, or vague
  content to trim.
- Keeps project memory focused on non-derivable, high-value context.

## Components

- **Command:** `/claude-md-init` — scaffold a new project `CLAUDE.md`.
- **Command:** `/claude-md-lint` — review an existing one and propose cuts.
- **Skill:** `claude-md-standards` — what belongs in project memory versus bloat, applied
  whenever you write or edit a CLAUDE.md.

## Usage

Run `/claude-md-init` in a new repo to bootstrap project memory, then `/claude-md-lint`
periodically to keep it from drifting or bloating. Both confirm before writing.

## Principle

Value is inversely related to length. If Claude can read it from the code, it doesn't
belong in `CLAUDE.md`.

Author: Matthews Wong · License: MIT
