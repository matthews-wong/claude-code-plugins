# api-contract-guard

Catch breaking API changes before they ship. Diffs an OpenAPI or JSON Schema
against a baseline and classifies each change as breaking or non-breaking.

## Components

- **`/api-compat <baseline> <candidate>`** — diffs two spec versions (paths or
  git refs), classifies changes, and recommends a SemVer action. Prefers
  `oasdiff` when present, otherwise diffs structurally.
- **Skill: api-compatibility** — the request-vs-response direction rule, a fast
  classification list, and deprecation guidance. Full rule matrix in
  `skills/api-compatibility/reference/compat-rules.md`.

## Key idea

Required-ness inverts between request and response: adding a required *request*
field breaks callers; removing a *response* field breaks readers. The command
always checks direction before calling a change safe.

## Optional tooling

Install [`oasdiff`](https://github.com/oasdiff/oasdiff) for authoritative
OpenAPI breaking-change detection and CI gating. The plugin works without it.

Author: Matthews Wong · License: MIT
