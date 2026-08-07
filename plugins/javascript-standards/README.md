# javascript-standards

A skill-first Claude Code plugin that enforces modern JavaScript/TypeScript
authoring standards.

## What it does

The `javascript-standards` skill auto-invokes when you write, review, or
refactor `.js`, `.jsx`, `.ts`, `.tsx`, or `.mjs` code — or mention "modern JS",
"ESM", async/await, error handling, and similar. It applies:

- ESM imports/exports (no CommonJS in new code)
- `const`/`let` only, never `var`
- strict equality (`===` / `!==`)
- `async`/`await` over `.then()` chains and callbacks
- immutability by default (no mutating inputs/shared state)
- real error handling (no swallowed `catch`, `Error` with `cause`)
- optional chaining `?.` and nullish coalescing `??`
- small, pure functions with side effects at the edges

## Structure

- `skills/javascript-standards/SKILL.md` — lean core rules + do/don't table
- `skills/javascript-standards/reference/` — expanded do/don't, before/after
  examples, and ESLint/Prettier tooling baseline

## Install

Place this directory under your Claude Code `plugins/` folder. The skill loads
automatically when a matching task is detected.

## License

MIT © Matthews Wong
