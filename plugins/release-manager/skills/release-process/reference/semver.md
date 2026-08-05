# Semantic Versioning Notes

Format: `MAJOR.MINOR.PATCH`, optionally `-prerelease` and `+build`.

## Bump rules

- **MAJOR** — incompatible API changes. Reset MINOR and PATCH to 0.
- **MINOR** — backward-compatible functionality. Reset PATCH to 0.
- **PATCH** — backward-compatible bug fixes.

## Edge cases

- **0.x.y (initial development):** anything may change at any time. Common
  convention: bump MINOR for breaking changes, PATCH for everything else. Call
  this out explicitly so consumers understand the instability.
- **Pre-releases:** `1.4.0-rc.1`, `2.0.0-beta.2`. Pre-release versions have
  lower precedence than the associated normal version. Use them for release
  candidates before a MAJOR.
- **Build metadata:** `+20260805`, ignored for precedence; never use it to
  convey meaning consumers depend on.
- **Never re-tag a released version.** If a release is broken, ship a new PATCH.

## Deciding from Conventional Commits

Scan the pending commits/changelog:
- Any breaking marker -> MAJOR (or MINOR if 0.x).
- Else any `feat` -> MINOR.
- Else `fix`/`perf` only -> PATCH.
- Only docs/chore/ci -> question whether a release is warranted at all.
