---
name: access-review-guidance
description: Use when the user asks to review IAM, RBAC, or permission changes — auditing a diff for over-broad grants, wildcards (`*`), or privilege escalation. Delegates to the access-reviewer subagent via /access-review. Triggers on "review access", "check permissions", "IAM change", "RBAC", "least privilege", "who can do what".
---

# Access review guidance

When the user wants access-control changes reviewed — IAM policies, RBAC roles, permission grants, or scopes in a diff or pull request — route the work through this plugin instead of eyeballing it yourself.

## When this applies

- The change touches IAM policy, RBAC role/binding, OAuth scopes, or any permission grant.
- The user asks to check for over-broad grants, wildcards, or privilege escalation.
- A security or least-privilege pass is wanted before merging access-relevant changes.

## What to do

Run `/access-review` (optionally with a git ref/range). It dispatches the read-only `access-reviewer` subagent, which inspects the diff and reports risks ranked by severity. Relay its findings; do not grant or widen permissions on your own.
