# Doc-type checklist

Per documentation surface, what to verify after a code change.

## README

- Feature list still matches shipped capabilities.
- Install/quickstart commands run as written (deps, versions, entrypoints).
- Usage examples compile/run and show current flags and output.
- Badges (build, coverage, version) point at live sources.
- Links resolve (no moved/renamed files).

## API reference (OpenAPI, docstrings, generated docs)

- Every public symbol documented; removed ones deleted.
- Parameter names, types, required-ness, defaults match the code.
- Return/response shapes match.
- Examples use current field names and produce valid payloads.
- If generated (Sphinx autodoc, TypeDoc, godoc), confirm regeneration is wired
  and re-run it rather than hand-editing.

## CHANGELOG

- Add an entry for every user-facing change under the right heading
  (Added / Changed / Deprecated / Removed / Fixed / Security — Keep a Changelog).
- Note breaking changes prominently; link migration guidance.
- Keep an `Unreleased` section; move it under a version+date on release.
- Follow SemVer: breaking -> major, additive -> minor, fix -> patch.

## Configuration docs

- Every env var / config key: name, type, default, required-ness, description.
- `.env.example` and sample configs list all keys with safe placeholder values
  (never real secrets).
- Removed keys deleted; renamed keys noted with the old name for migration.

## Tutorials / guides

- Step-by-step flows still work end to end.
- Screenshots/output blocks reflect current UI/CLI.
- Version-pinned snippets updated after dependency bumps.

## Architecture / design docs

- Diagrams and module descriptions match the current structure.
- New components added; removed ones deleted.
- ADRs: record consequential, hard-to-reverse decisions; do not rewrite past
  ADRs — supersede them with a new one.

## What NOT to touch

- Prose style, tone, or formatting the project already uses consistently.
- Auto-generated files by hand (fix the generator/source instead).
- Historical CHANGELOG/ADR entries (they are a record, not living docs).
