---
name: standards-enforcer
description: Check a diff against an editable org coding-standards profile — naming, file organization, error handling, no secrets or debug prints, docstrings on public APIs. Use when reviewing a diff or PR for convention compliance, before committing, or when the user asks to enforce coding standards or style rules. Triggers on "enforce standards", "check conventions", "style review", "does this follow our standards", "lint my diff".
---

# Standards Enforcer

Check changed code against the team's coding-standards profile. Review only the diff, cite the exact rule, and grade by severity.

## The profile is the source of truth

The enforceable rules live in `reference/standards-profile.md`, which the team edits. Always read it before enforcing — do not enforce rules that are not in the profile. If a repo linter/formatter config conflicts, prefer the repo config and note the conflict.

## Rule categories (default profile summary)

1. **Naming** — files kebab-case (except ecosystem norms like PascalCase React components); types PascalCase; functions/vars camelCase; constants UPPER_SNAKE_CASE. Names state intent; avoid abbreviations and single letters except loop indices.
2. **File organization** — one clear responsibility per module; group by feature/domain; colocate tests/styles with their unit.
3. **Error handling** — validate inputs at boundaries; never swallow errors silently; fail loudly in dev, degrade gracefully in prod; no empty catch blocks.
4. **No secrets / no debug output** — no hardcoded credentials, keys, or tokens; no leftover `print`, `console.log`, `dump`, `dbg!`, debugger statements in shipped code.
5. **Docstrings on public APIs** — exported functions, classes, and module entry points get a one-line purpose statement; document the *why*, not the *what*.

## Severity

- **Blocker** — secrets/keys in code; swallowed errors on critical paths; obvious data-loss risks.
- **Warning** — naming violations, missing public-API docstring, misplaced files.
- **Nit** — cosmetic style the formatter should own.

Fail the check if any Blocker is present.

## Output

Table: File:Line | Severity | Rule | Finding | Suggested fix. Then counts per severity and a pass/fail verdict. Offer to apply mechanical fixes.

## Going deeper

Full rule text, per-language specifics, allowed exceptions, and examples are in `reference/standards-profile.md`. Load it every run (it is the authority) and edit it to tune the org's standards.
