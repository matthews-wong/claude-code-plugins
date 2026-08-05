---
name: code-review
description: Review the current working changes (git diff) for bugs, edge cases, and quality, and report concise, actionable findings.
args:
  - name: range
    description: Optional git ref or range to review (e.g. "main", "HEAD~3"). Defaults to the working diff (staged + unstaged).
---

Review the current working changes for correctness and quality before a human
looks at them.

1. Delegate the review to the **code-reviewer** subagent so it runs in its own
   context with read-only tools. If a `range` argument was provided ("$1"), tell
   the subagent to review that range; otherwise it should review the working diff
   (`git diff` plus `git diff --staged`), falling back to the last commit if the
   working tree is clean.

2. Have the subagent examine not just the diff but the surrounding code — callers,
   related helpers, and tests — so context-dependent bugs are caught.

3. Present its findings to me, grouped by severity (Blocker / Should-fix / Nit),
   each with a `file:line` reference and a concrete suggested fix, plus a one-line
   overall verdict (approve / approve-with-nits / request-changes).

Do not modify any files during the review; this is a read-only pass. If I ask you
to address the findings afterward, that's a separate step.
