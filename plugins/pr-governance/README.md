# pr-governance

Enforces enterprise pull request standards and produces a checklist verdict.

## What it checks

1. Clear description (explains *why*)
2. Linked issue / ticket
3. Reasonable size
4. Tests included
5. No unrelated changes

## Usage

```
/pr-review              # review the current branch's PR
/pr-review 123          # review a specific PR number
```

The command gathers PR facts (via `gh` or the local diff), applies the
`pr-standards` skill, and returns a checklist ending in APPROVE,
APPROVE WITH COMMENTS, or REQUEST CHANGES. It never modifies files.

## Components

- `commands/pr-review.md` — the `/pr-review` command.
- `skills/pr-standards/` — the review criteria, size heuristics, and verdict
  rubric.

## License

MIT — Matthews Wong
