---
name: security-review-guidance
description: Use when the user asks to review changes for security vulnerabilities — injection, XSS, auth flaws, secrets, SSRF, unsafe deserialization, path traversal. Delegates to the security-reviewer subagent via /security-review. Triggers on "security review", "check for vulnerabilities", "is this safe", "audit this diff for security", "OWASP".
---

# Security review guidance

When the user wants their changes audited for security vulnerabilities — before committing or merging security-relevant code — route it through this plugin.

## When this applies

- The user asks to check a diff or PR for exploitable flaws.
- Changes touch auth, input handling, deserialization, network calls, or secrets.

## What to do

Run `/security-review` (optionally with a git ref or range; defaults to the working diff). It dispatches the read-only `security-reviewer` subagent, which reports severity-ranked, actionable findings (injection, authn/authz, secrets, SSRF, unsafe deserialization, path traversal, and more). Relay the findings.
