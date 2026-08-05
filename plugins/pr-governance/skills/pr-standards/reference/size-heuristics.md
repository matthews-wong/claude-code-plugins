# PR Size Heuristics

Size is a proxy for review quality, not a hard gate. Weigh net lines changed,
file count, and conceptual surface area together.

| Band | Net lines changed | Guidance |
|------|-------------------|----------|
| Small | < 200 | Ideal. Easy to review thoroughly. |
| Medium | 200–500 | Acceptable. Ensure the description maps the change. |
| Large | 500–1000 | Flag. Ask whether it can be split into stacked PRs. |
| Very large | > 1000 | Fail size unless it is generated code, a vendored move, or a lockfile. |

## Adjustments

- Exclude generated files, lockfiles, snapshots, and pure file moves from the
  count when judging reviewability — but call them out separately.
- A change touching many files with a single mechanical edit (a rename, a
  signature change) can be large yet reviewable; note that in the reason.
- Splitting advice: separate refactor from behavior change, separate schema
  migration from feature code, and land enabling scaffolding first.
