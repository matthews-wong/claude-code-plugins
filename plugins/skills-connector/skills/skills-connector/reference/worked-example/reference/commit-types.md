# Conventional Commit types

The `type` is the first token of the subject and signals the nature of the change. Pick the
most specific one that fits.

| Type       | Use when the change…                                              | SemVer bump |
|------------|-------------------------------------------------------------------|-------------|
| `feat`     | adds a user-visible feature or capability                         | minor       |
| `fix`      | fixes a bug in behavior                                           | patch       |
| `docs`     | touches documentation only                                       | none        |
| `style`    | changes formatting/whitespace, no code meaning change            | none        |
| `refactor` | restructures code without changing behavior or public API         | none        |
| `perf`     | improves performance without changing behavior                    | patch       |
| `test`     | adds or fixes tests only                                          | none        |
| `build`    | changes the build system or dependencies                          | none        |
| `ci`       | changes CI configuration or scripts                              | none        |
| `chore`    | maintenance that fits nowhere above (e.g. bumping a tool version) | none        |
| `revert`   | reverts a previous commit                                        | varies      |

## Breaking changes

Any type can be breaking. Signal it either way:

- Append `!` after the type/scope: `feat(api)!: drop v1 endpoints`, and/or
- Add a `BREAKING CHANGE:` footer describing what broke and how to migrate.

A breaking change forces a **major** version bump regardless of the base type.

## Choosing between close calls

- **`feat` vs `fix`** — did the change add something users can now do (`feat`), or restore
  intended behavior that was broken (`fix`)?
- **`refactor` vs `perf`** — `perf` only when the goal and result is measurable speed/
  resource improvement; otherwise `refactor`.
- **`chore` vs `build`/`ci`** — prefer the specific `build` or `ci` when the change is to
  those systems; reserve `chore` for genuine catch-all maintenance.
