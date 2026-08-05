# release-manager

Guides a repeatable, governance-respecting release process.

## Usage

```
/release            # infer the bump from pending changes
/release minor      # force a bump level
/release 2.1.0      # set an explicit version
```

## What it does

1. Runs a pre-flight checklist (clean tree, right branch, tests, changelog).
2. Decides the semver bump (major/minor/patch) from the pending changes and
   confirms it.
3. Promotes `## [Unreleased]` in `CHANGELOG.md` to a dated version heading.
4. Updates manifest version fields.
5. Drafts release notes for `vX.Y.Z`.
6. Proposes the commit, annotated tag, and push commands for approval.

## Honest scope

This plugin **prepares** a release and surfaces the exact commands. It does not
push tags, publish to registries, or create hosted releases on its own — those
irreversible steps stay with the person running the release.

## Components

- `commands/release.md`
- `skills/release-process/` — checklist, semver rules, and release-notes
  template.

## License

MIT — Matthews Wong
