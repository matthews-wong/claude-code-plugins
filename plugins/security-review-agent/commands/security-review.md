---
name: security-review
description: Review the current working changes for security vulnerabilities and report severity-ranked, actionable findings.
args:
  - name: range
    description: Optional git ref or range to review (e.g. "main", "HEAD~3"). Defaults to the working diff (staged + unstaged).
---

Run a security review of the current changes before they are merged.

1. Delegate to the **security-reviewer** subagent so the audit runs in its own
   read-only context. If a `range` argument was given ("$1"), have it review that
   range; otherwise it reviews the working diff (`git diff` plus `git diff --staged`),
   falling back to the latest commit when the tree is clean.

2. Instruct the subagent to trace tainted data from source to sink — not just read
   the diff in isolation — and to evaluate the change against the standard threat
   categories: injection, XSS, authn/authz, secrets, unsafe deserialization, SSRF,
   path traversal, weak crypto, data exposure, and risky dependencies/config.

3. Present its findings **ranked by severity** (Critical → High → Medium → Low →
   Informational). Each finding should include a `file:line` location, the impact,
   a brief exploit sketch, and a concrete remediation, plus a one-line overall risk
   verdict.

Do not modify any files during the review. If I ask you to fix a finding afterward,
treat that as a separate step.
