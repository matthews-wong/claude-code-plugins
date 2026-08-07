---
name: javascript-standards
description: >-
  Apply modern JavaScript/TypeScript standards when writing, reviewing, or
  refactoring .js/.jsx/.ts/.tsx/.mjs code. Triggers on "modern JS", "ESM",
  "import/export", "async/await", "callback hell", "var vs let", "==",
  Promises, error handling, immutability, optional chaining, or nullish
  coalescing. Use whenever authoring or cleaning up JavaScript modules.
---

# JavaScript Standards

Opinionated, current best practices for writing modern JavaScript and
TypeScript. Apply these while authoring; flag violations while reviewing.

## Core rules

1. **Modules: ESM only.** Use `import`/`export`. No `require`/`module.exports`
   in new code. Prefer named exports; reserve `default` for a module's single
   obvious entry point. No wildcard side-effect re-exports.
2. **Declarations: `const` by default, `let` when reassigned. Never `var`.**
   `var` is function-scoped and hoisted — a bug source. Declare at first use.
3. **Equality: always `===` / `!==`.** `==` triggers coercion. The only
   acceptable loose check is `x == null` to catch both `null` and `undefined`
   (and even then, prefer being explicit).
4. **Async: `async`/`await` over `.then()` chains and callbacks.** Wrap awaited
   calls that can fail in `try/catch`. Use `Promise.all` for independent work,
   never `await` in a sequential loop when the iterations are independent.
5. **Error handling: never swallow.** No empty `catch {}`. Either handle
   meaningfully, rethrow, or attach context (`throw new Error("...", { cause })`).
   Throw `Error` instances, never strings. Validate inputs at boundaries.
6. **Immutability by default.** Do not mutate function parameters or shared
   state. Prefer `map`/`filter`/`reduce` and spread/`structuredClone` over
   in-place `push`/`splice`/`sort` on inputs. `sort`/`reverse` mutate — copy
   first (`[...arr].sort()`).
7. **Optional chaining + nullish coalescing.** Use `a?.b?.c` and `x ?? fallback`.
   Do **not** use `||` for defaults when `0`, `""`, or `false` are valid values.
8. **Small pure functions.** One responsibility; return values instead of
   mutating; isolate side effects (I/O, logging, DOM) at the edges.
9. **No dead code.** Delete commented-out blocks and unused symbols.

## Quick do / don't

| Don't | Do |
| --- | --- |
| `var x = 1` | `const x = 1` |
| `if (a == b)` | `if (a === b)` |
| `p.then(f).catch(e)` chains | `try { await p } catch (e) {}` |
| `catch (e) {}` | `catch (e) { throw new Error("context", { cause: e }) }` |
| `opts.timeout || 300` | `opts.timeout ?? 300` |
| `arr.push(x)` on a param | `return [...arr, x]` |
| `user && user.name` | `user?.name` |

## Reference (load on demand)

- `reference/do-dont.md` — expanded do/don't table with rationale.
- `reference/examples.md` — before/after code for each rule, plus async
  patterns, error-handling recipes, and immutability helpers.
- `reference/tooling.md` — ESLint/Prettier config and package.json `"type"`.
