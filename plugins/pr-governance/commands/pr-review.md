---
name: pr-review
description: Review the current pull request against enterprise PR standards and produce a checklist verdict.
args: "[PR number or branch (optional; defaults to the current branch's PR)]"
---

You are performing an enterprise pull request governance review. Apply the
`pr-standards` skill.

Target: $ARGUMENTS (if empty, review the PR associated with the current branch).

Steps:

1. Gather the facts about the PR without assuming any host (GitHub, GitLab,
   Bitbucket). Prefer whatever CLI is available (for example `gh pr view
   <target> --json title,body,files,additions,deletions,commits` when GitHub
   CLI is present). If no CLI is available, inspect the local diff against the
   base branch (`git diff <base>...HEAD --stat` and the full diff) and the
   commit messages, and note that the PR metadata could not be fetched.

2. Evaluate each standard defined in the `pr-standards` skill: description
   quality, linked issue/ticket, change size, tests included, and scope
   discipline (no unrelated changes).

3. Produce the checklist verdict exactly in the format the skill specifies,
   ending with an overall verdict of APPROVE, APPROVE WITH COMMENTS, or REQUEST
   CHANGES, plus concrete, actionable follow-ups.

Do not modify any files. This command only reviews and reports.
