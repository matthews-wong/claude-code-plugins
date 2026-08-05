# Contributing to claude-code-plugins

Thanks for your interest! This is an open-source marketplace of Claude Code plugins
for agentic workflows. Contributions — new plugins, fixes, and docs — are welcome.

## Adding or changing a plugin

1. Each plugin lives in `plugins/<name>/` with a `.claude-plugin/plugin.json` manifest
   and its components (`commands/`, `skills/`, `agents/`, `hooks/`).
2. Register the plugin in `.claude-plugin/marketplace.json` (name + `source`).
3. Validate locally before opening a PR:
   ```bash
   /plugin validate .
   ```
4. Keep plugins **small and focused** — one clear job each. Prefer real, accurate
   Claude Code behavior over inventing features.

## Pull requests

- One logical change per PR; describe what and why.
- Update the plugin's `README.md` and this repo's README table if you add a plugin.
- Be honest in docs — no fabricated metrics or claims.

## Conduct

Be respectful and constructive.
