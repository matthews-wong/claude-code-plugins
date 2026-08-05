---
name: release
description: Walk through a repeatable release: decide the semver bump, promote the changelog, tag, and draft release notes with a pre-flight checklist.
args: "[optional explicit version or bump level: major | minor | patch | X.Y.Z]"
---

Drive a release using the `release-process` skill. This command **guides** the
process and prepares artifacts; it performs git operations only with the user's
confirmation and never publishes or pushes without an explicit go-ahead.

Requested bump/version: $ARGUMENTS

Steps:

1. **Pre-flight.** Run the checklist in the skill: working tree clean, on the
   correct branch, tests/lint status known, and `## [Unreleased]` in
   `CHANGELOG.md` has content. Report any blockers and stop if the tree is dirty
   unless the user overrides.

2. **Decide the version.** Read the current version (latest tag and/or manifest
   such as `package.json`, `pyproject.toml`, `Cargo.toml`). If the user gave a
   version or level, use it; otherwise infer the bump from the Unreleased
   changelog / Conventional Commits (breaking -> major, feat -> minor, fix ->
   patch) and propose it with reasoning. Confirm before proceeding.

3. **Promote the changelog.** Rename `## [Unreleased]` to
   `## [X.Y.Z] - <today>`, add a fresh empty Unreleased section, and update the
   comparison links (see the changelog format).

4. **Draft release notes** for `vX.Y.Z` from that section.

5. **Prepare tag and manifest.** Update the version field in any manifest, and
   propose the commands to commit, tag (`vX.Y.Z`), and push. Show them for the
   user to approve; do not run push/publish yourself unless explicitly told to.

6. Summarize what was changed, what remains manual, and the exact next commands.
