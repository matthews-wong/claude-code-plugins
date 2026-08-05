---
name: docs-drift
description: >
  Use when code changes may have made documentation stale, or the user asks to
  check/update docs after editing source. Triggers: "docs out of date", "stale
  docs", "update the README", "docs drift", "did I miss a doc", "keep docs in
  sync", "changelog", "document this change". Not for writing new docs from
  scratch — for detecting and fixing drift caused by code changes.
---

# Docs Drift Detection

Find documentation that code changes have quietly invalidated, then propose the
minimal edits to make it true again. A stale doc is worse than no doc — it
misleads with authority.

## Workflow

1. Get the changed source files (git diff / status).
2. Run `sh "${CLAUDE_PLUGIN_ROOT}/scripts/docs-scan.sh"` for leads.
3. For each change, map it to the docs it affects (signals below).
4. Grep the docs for the changed symbols/flags/values; confirm real mismatches.
5. Report stale docs with reasons + concrete edits; note what you verified as
   still correct.

## Drift signal catalog

Map a code change to the docs it likely breaks:

- **Public signature change** (function/method/class/endpoint params, return
  type) -> API reference, usage examples, docstrings, type stubs.
- **CLI change** (added/removed/renamed flag or subcommand) -> README usage,
  quickstart, embedded `--help` output, man pages.
- **Config change** (env var, config key, default) -> configuration docs,
  `.env.example`, Helm/compose samples, settings reference.
- **Dependency/version change** -> install instructions, requirements,
  compatibility matrix, badges.
- **Behavior/default change** -> any prose describing that behavior; tutorials.
- **New feature/module** -> README feature list, docs nav/index, CHANGELOG,
  migration notes.
- **Removed/deprecated code** -> remove or mark deprecated in docs; add to
  CHANGELOG and migration guide.

The full checklist per doc type (README, API ref, CHANGELOG, tutorials,
architecture docs) is in `./reference/doc-map.md`.

## Judgment rules

- Flag only genuine mismatches you can point to. No speculative "you might want
  to mention this."
- Match the project's existing doc style and structure; do not impose new
  conventions.
- Prefer surgical edits over rewrites. Keep the author's voice.
- CHANGELOG entries follow the project's format (e.g. Keep a Changelog) — see
  the reference.
- If nothing is stale, say so; a clean bill is a valid, useful result.
