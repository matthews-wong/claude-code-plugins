---
description: Use when a user wants to enable or understand Claude Code's auto permission mode. Explains permissions.defaultMode "auto" honestly (a safety classifier approves routine actions and falls back to default mode if unavailable), and helps configure ~/.claude/settings.json with a vetted allow set and a deny floor.
---

# Auto Mode Setup

Help users trade some permission prompts for flow, without pretending the trade-off is
free. Auto mode reduces friction; explicit allow/deny rules keep the guardrails.

## How auto mode actually works

- `permissions.defaultMode: "auto"` tells Claude Code to auto-approve actions it judges
  routine and low-risk, instead of prompting on each one.
- The judgment comes from a **safety classifier**. It is a heuristic and can be wrong in
  either direction.
- If the classifier is **unavailable**, auto mode **falls back to default mode** and
  prompts normally. It fails safe.
- `permissions.allow` still pre-approves listed matchers; `permissions.deny` still hard-
  blocks listed matchers. Auto mode sits between them — it does not override `deny`.

Be honest about all four points. Never tell a user auto mode is "safe" in absolute terms.

## The permission modes, briefly

- `default` — prompt for actions not already allowed.
- `plan` — read/plan only; no edits or command execution until the user approves.
- `acceptEdits` — auto-accept file edits, still prompt for other actions.
- `auto` — classifier-gated auto-approval of routine actions, with the fallback above.

## Recommended configuration shape

Put personal defaults in `~/.claude/settings.json`:

```json
{
  "permissions": {
    "defaultMode": "auto",
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(npm test:*)",
      "Bash(rg:*)"
    ],
    "deny": [
      "Bash(rm -rf:*)",
      "Bash(git push:*)",
      "Read(./.env)",
      "Read(./**/*.pem)"
    ]
  }
}
```

## Guidance when helping

1. Confirm the user wants a global default before editing `~/.claude/settings.json`.
2. Merge into existing settings; never overwrite the whole file.
3. Curate the `allow` set from commands the user genuinely trusts — favor read-only and
   idempotent test/build commands. Keep matchers specific.
4. Always keep a `deny` floor for destructive, network-mutating, and secret-reading
   actions so a classifier miss cannot cause the worst outcomes.
5. Show the merged JSON, explain each change, confirm before writing.
6. Note the easy revert: set `defaultMode` back to `"default"` (or `"plan"`).
