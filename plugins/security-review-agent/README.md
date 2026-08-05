# security-review-agent

A dedicated security-review subagent plus a slash command to invoke it. It audits
your **working git diff** for vulnerabilities and reports severity-ranked,
actionable findings — a focused security pass to run alongside your normal review.

## What it installs

- **Subagent `security-reviewer`** (`agents/security-reviewer.md`) — a read-only
  auditor (tools: Read, Grep, Glob, Bash) that gathers the diff via `git`, traces
  tainted data from source to sink, and evaluates the change against a standard
  threat checklist (injection, XSS, authn/authz, secrets, unsafe deserialization,
  SSRF, path traversal, weak crypto, data exposure, dependencies/config).
- **Command `/security-review`** — delegates the audit to the subagent and presents
  severity-ranked findings. Accepts an optional git range argument.

## How to use

- Run `/security-review` to audit the current working changes (staged + unstaged),
  falling back to the last commit if the tree is clean.
- Run `/security-review main` (or any ref/range) to audit a specific range.

Findings are ordered Critical → High → Medium → Low → Informational, each with a
`file:line` location, impact, a brief exploit sketch, and a concrete remediation.

## Notes

- The subagent uses `git` via the Bash tool; run it inside a git repository.
- This is an assistive review, not a substitute for dedicated SAST/DAST tooling or a
  professional audit. It reports; it never modifies code.
