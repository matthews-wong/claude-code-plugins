# typescript-typing

A skill-first Claude Code plugin for precise, safe TypeScript typing.

## What it does

The `typescript-typing` skill auto-invokes when you write or fix types in
`.ts`/`.tsx` files, or mention "type error", `any`, `unknown`, generics,
interfaces, discriminated unions, `readonly`, `satisfies`, or strict tsconfig.
It applies:

- ban `any` — prefer `unknown` plus narrowing/guards
- discriminated unions to make illegal states unrepresentable
- `readonly` and `as const` by default
- precise, explicit return types on public functions
- generics constrained with `extends` (no bare `<T>` used as `any`)
- `satisfies` to validate config without widening
- derive types (`Pick`/`Omit`/`Record`/`keyof`) instead of duplicating
- no force-fit `as` casts; narrow instead
- strict `tsconfig` baseline

## Structure

- `skills/typescript-typing/SKILL.md` — lean core rules + do/don't table
- `skills/typescript-typing/reference/` — worked type examples and a
  recommended strict `tsconfig` with rationale

## Install

Place this directory under your Claude Code `plugins/` folder. The skill loads
automatically when a matching task is detected.

## License

MIT © Matthews Wong
