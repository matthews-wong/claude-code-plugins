# conventional-commits

Formats and enforces [Conventional Commits](https://www.conventionalcommits.org)
v1.0.0.

## Components

- **`/commit`** — inspects staged changes and composes a compliant commit
  message (`type(scope): description`, body, breaking-change footer), then
  creates the commit. Never pushes, never uses `--no-verify`.
- **`conventional-commits` skill** — the grammar, type-selection guide, and
  validation regex, used whenever a commit message is written or checked.
- **Validation hook** — a `PostToolUse` hook on `Bash` runs
  `scripts/check-commit-msg.sh` after commands. When a `git commit` ran, it
  checks the latest commit subject and prints advisory warnings.

## Non-blocking guarantee

`scripts/check-commit-msg.sh` always exits `0`. It emits warnings to stderr but
never fails a command or blocks the workflow. Run it standalone too:

```sh
sh scripts/check-commit-msg.sh .git/COMMIT_EDITMSG
echo "feat(auth): add SSO login" | sh scripts/check-commit-msg.sh
```

## License

MIT — Matthews Wong
