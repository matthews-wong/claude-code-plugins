# auto-mode-setup

Enable Claude Code's auto permission mode the honest way: fewer prompts for routine work,
with an explicit allow set and a deny floor keeping the guardrails.

## What it does

- Sets `permissions.defaultMode` to `"auto"` in `~/.claude/settings.json`.
- Explains auto mode truthfully: a safety classifier approves routine actions and falls
  back to default (prompting) mode if the classifier is unavailable.
- Pre-approves a vetted set of safe bash/MCP commands via exact-match `permissions.allow`.
- Keeps a `permissions.deny` floor so a classifier miss can't cause the worst outcomes.

## Components

- **Command:** `/setup-auto-mode` — guided, confirm-before-write configuration.
- **Skill:** `auto-mode-setup` — how auto mode works and the recommended settings shape.

## Usage

Run `/setup-auto-mode`, review the explanation and the proposed merged JSON, then approve
the change. Revert anytime by setting `defaultMode` back to `"default"` or `"plan"`.

## Honesty note

Auto mode reduces friction; it is not a guarantee of safety. The classifier is a
heuristic, it fails safe (falls back to prompting) when unavailable, and your explicit
`allow`/`deny` rules always apply.

Author: Matthews Wong · License: MIT
