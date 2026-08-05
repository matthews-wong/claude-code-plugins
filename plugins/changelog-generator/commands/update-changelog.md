---
name: update-changelog
description: Update CHANGELOG.md from Conventional Commit history using the Keep a Changelog format.
args: "[optional git range, e.g. v1.2.0..HEAD; defaults to commits since the last tag]"
---

Update the project's `CHANGELOG.md`. Apply the `changelog-maintenance` skill for
the mapping rules and format.

Range: $ARGUMENTS

Steps:

1. Determine the commit range. If none was given, use commits since the most
   recent tag (`git describe --tags --abbrev=0`); if there are no tags, use the
   full history. Read messages with
   `git log <range> --pretty=format:%H%x09%s%x09%b`.

2. If `CHANGELOG.md` does not exist, create it with the Keep a Changelog header
   and an `## [Unreleased]` section.

3. Map each Conventional Commit to a Keep a Changelog category (feat -> Added,
   fix -> Fixed, breaking change -> Changed with a breaking note, etc.) per the
   skill. Skip noise like `chore`, `ci`, `test`, and `style` unless
   user-facing. De-duplicate and write human-readable bullet points, not raw
   subjects.

4. Place entries under `## [Unreleased]` in the correct subsections, preserving
   any existing released sections and links. Show a summary of what changed. Do
   not create a version heading or tag — that is the release step. Do not commit.
