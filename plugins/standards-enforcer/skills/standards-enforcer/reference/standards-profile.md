# Org Coding-Standards Profile (editable)

This file is the source of truth for `/enforce-standards` and the `standards-enforcer` skill. **Edit it to match your organization's standards** — add, remove, or retune rules. Each rule has an ID so findings can cite it.

## 1. Naming (`NAME-*`)

- **NAME-1** Files: kebab-case by default. Exceptions by ecosystem: React components PascalCase; language-idiomatic names (e.g. Go, Python modules) as the ecosystem dictates.
- **NAME-2** Types / classes / interfaces: PascalCase.
- **NAME-3** Functions and variables: camelCase (or snake_case in Python/Ruby per language norm — pick one per language and keep it consistent).
- **NAME-4** Constants: UPPER_SNAKE_CASE.
- **NAME-5** Names describe intent. No abbreviations or single letters except conventional loop indices (`i`, `j`) and idiomatic short names (`err`, `ctx`, `id`).
- **NAME-6** Booleans read as predicates (`isReady`, `hasAccess`, `canRetry`).

## 2. File organization (`ORG-*`)

- **ORG-1** One clear responsibility per module; if describing it needs "and", consider splitting.
- **ORG-2** Group by feature/domain first, technical layer second.
- **ORG-3** Colocate closely-coupled artifacts (component + its test + its styles).
- **ORG-4** Keep dependency direction inward — domain core independent of framework/IO.

## 3. Error handling (`ERR-*`)

- **ERR-1** Validate inputs at boundaries (API handlers, CLI entry, deserialization).
- **ERR-2** Never swallow errors silently. No empty `catch {}` / bare `except: pass` without a logged reason and a deliberate decision.
- **ERR-3** Fail loudly in dev, degrade gracefully in prod.
- **ERR-4** Do not catch broadly then continue as if nothing happened; re-throw, wrap with context, or handle explicitly.
- **ERR-5** No control flow that hides partial failures (e.g. ignoring a rejected promise / unchecked error return).

## 4. No secrets / no debug output (`SEC-*`)

- **SEC-1** No hardcoded credentials, API keys, tokens, private keys, or connection strings. Use env/secret manager.
- **SEC-2** No leftover debug output in shipped code: `print`, `console.log`/`console.debug`, `debugger`, `System.out.println`, `dump`, `var_dump`, `dbg!`, `fmt.Println` used as debugging.
- **SEC-3** No committed `.env` files or secret fixtures with real values.
- **SEC-4** No PII or secrets written to logs (see data-classification for detail).

## 5. Docstrings on public APIs (`DOC-*`)

- **DOC-1** Exported/public functions, classes, and module entry points have a one-line purpose statement.
- **DOC-2** Comments explain the *why* (intent, trade-offs, constraints), not the *what*.
- **DOC-3** Comment density matches the surrounding file; don't over-document trivial private helpers.
- **DOC-4** Keep docs true or delete them — a stale doc is worse than none.

## Severity mapping

- Blocker: SEC-1, SEC-3, ERR-2/ERR-4 on critical paths.
- Warning: NAME-*, ORG-*, DOC-1, SEC-2, remaining ERR-*.
- Nit: purely cosmetic items the formatter should own.

## Enforcement notes

- Enforce only rules listed here. Missing rule? Propose adding it, don't enforce silently.
- Prefer the repo's own linter/formatter config where it conflicts; report the conflict.
- Review only lines in the diff, plus the minimum surrounding context needed to judge them.
