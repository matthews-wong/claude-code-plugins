# Verdict Rubric

Map the five criteria to an overall verdict.

- **REQUEST CHANGES** — Any of these fail: clear description, tests included, or
  no unrelated changes. These affect correctness, safety, or reviewability and
  must be resolved before merge.
- **APPROVE WITH COMMENTS** — All blocking criteria pass, but size is flagged or
  the linked issue/ticket is missing on a non-trivial change. Mergeable once the
  author acknowledges or addresses the comments.
- **APPROVE** — All five criteria pass.

## Principles

- Be specific: every fail names the file, line, or missing artifact and the
  exact action to fix it.
- Never fail a PR on subjective style the linter or formatter already owns.
- When PR metadata could not be fetched, say so explicitly and grade only what
  the local diff and commit messages reveal.
