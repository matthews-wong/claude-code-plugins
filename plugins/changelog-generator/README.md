# changelog-generator

Maintains a [Keep a Changelog](https://keepachangelog.com) `CHANGELOG.md` from
Conventional Commit history.

## Usage

```
/update-changelog                 # commits since the last tag
/update-changelog v1.2.0..HEAD    # an explicit range
```

The command reads commit messages, maps them into the six Keep a Changelog
categories (Added, Changed, Deprecated, Removed, Fixed, Security), and writes
human-readable bullets under `## [Unreleased]`. Noise commits (`chore`, `ci`,
`test`, `style`) are skipped unless user-facing.

It fills only the `Unreleased` section; cutting a version heading is left to the
release process. It does not commit.

## Components

- `commands/update-changelog.md`
- `skills/changelog-maintenance/` — mapping rules and file format.

## License

MIT — Matthews Wong
