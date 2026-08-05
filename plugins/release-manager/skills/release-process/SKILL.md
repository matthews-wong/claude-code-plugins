---
name: release-process
description: A repeatable, honest release checklist. Use when cutting a release to decide the semver bump, promote the changelog, tag, and draft release notes without skipping governance steps.
---

# Release Process

A release turns an `Unreleased` changelog into a tagged, documented version.
This skill guides the steps; a human or agent executes them and confirms the
irreversible ones (tag, push, publish).

## Semver bump decision

Given the current version `X.Y.Z`, choose the bump from the pending changes:

- **MAJOR** — any breaking change (`!` or `BREAKING CHANGE`), or a removal that
  breaks consumers.
- **MINOR** — new backward-compatible features (`feat`).
- **PATCH** — backward-compatible bug fixes only (`fix`, `perf`).

Pre-1.0.0 projects may treat `minor` as the breaking lane; note this when it
applies. See `reference/semver.md` for edge cases (pre-releases, 0.x, build
metadata).

## Pre-flight checklist

```
Release pre-flight
- [ ] Working tree is clean (git status)
- [ ] On the intended release branch
- [ ] Tests pass / lint clean (or the exception is documented)
- [ ] CHANGELOG.md [Unreleased] has real entries
- [ ] Version decided and agreed
- [ ] No secrets or debug artifacts staged
```

Do not check a box you have not verified.

## Steps

1. Run the pre-flight checklist; stop on blockers.
2. Decide `X.Y.Z`.
3. Promote `## [Unreleased]` to `## [X.Y.Z] - <today>` and open a fresh
   Unreleased section (see the changelog format).
4. Update version in the manifest(s) (`package.json`, `pyproject.toml`,
   `Cargo.toml`, etc.).
5. Draft release notes from the promoted section.
6. Propose the commit + annotated tag `vX.Y.Z` + push commands for approval.

## Honesty

This process **does not** publish to a registry, push tags, or create a hosted
release on its own. It prepares the artifacts and surfaces the exact commands so
the person releasing stays in control of irreversible actions. See
`reference/release-notes.md` for the notes template.
