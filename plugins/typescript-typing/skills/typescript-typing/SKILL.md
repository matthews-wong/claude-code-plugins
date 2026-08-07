---
name: typescript-typing
description: >-
  Apply precise TypeScript typing when writing or fixing types in .ts/.tsx
  files. Triggers on "type error", "any", "unknown", generics, interfaces,
  discriminated unions, "readonly", "satisfies", type narrowing, type guards,
  tsconfig strict, or TS compiler complaints. Use whenever modeling data,
  designing type signatures, or resolving type-checker errors.
---

# TypeScript Typing

Model data so illegal states are unrepresentable, and let the compiler catch
mistakes. Apply while writing types; flag looseness while reviewing.

## Core rules

1. **Ban `any`. Reach for `unknown` + narrowing.** `any` disables checking and
   spreads silently. For untrusted/external data type as `unknown`, then narrow
   with type guards (`typeof`, `in`, `Array.isArray`, or a validator like Zod).
2. **Discriminated unions over optional-field grab-bags.** Give each variant a
   literal tag (`kind`/`type`) so `switch` narrows exactly and impossible
   combinations can't be constructed.
3. **`readonly` by default.** Mark fields, arrays (`readonly T[]` /
   `ReadonlyArray<T>`), and tuples immutable unless mutation is the point. Use
   `as const` for literal config to get the narrowest types.
4. **Precise, explicit return types on exported/public functions.** They act as
   a contract and stop inference from leaking `any` outward. Prefer narrow input
   types (`ReadonlyArray`, unions) over broad ones.
5. **Constrained generics — never bare `<T>` used as `any`.** Constrain with
   `extends` (`<T extends object>`, `<K extends keyof T>`). Let call sites infer;
   don't over-annotate. Avoid a generic that appears only once (it's not generic).
6. **`satisfies` to validate without widening.** `const cfg = {...} satisfies
   Config` keeps the precise literal type *and* checks the shape — better than
   `const cfg: Config = {...}`, which widens and hides excess keys.
7. **Prefer `interface` for object/public shapes, `type` for unions,
   intersections, tuples, and mapped/conditional types.** Both work; be
   consistent.
8. **Derive, don't duplicate.** Use `Pick`, `Omit`, `Partial`, `Required`,
   `Record`, `ReturnType`, `Parameters`, and `keyof`/indexed access to keep one
   source of truth. Avoid re-declaring shapes that already exist.
9. **No `as` casts to force-fit.** A cast silences the checker without proving
   anything. Narrow instead; reserve `as` for genuinely unprovable truths and
   `as const`. Never `as any`. Avoid non-null `!` unless truly guaranteed.

## Quick do / don't

| Don't | Do |
| --- | --- |
| `function f(x: any)` | `function f(x: unknown)` + narrow |
| `data as User` | validate/guard, then use as `User` |
| `{ ok: boolean; error?: string; data?: T }` | `\| { ok: true; data: T } \| { ok: false; error: string }` |
| `const c: Config = {...}` | `const c = {...} satisfies Config` |
| `items: string[]` (never mutated) | `items: readonly string[]` |
| `<T>(x: T): T` used as any | `<T extends Item>(x: T): T` |

## tsconfig baseline

Enable `"strict": true` plus `noUncheckedIndexedAccess`,
`exactOptionalPropertyTypes`, and `noImplicitOverride`. See reference.

## Reference (load on demand)

- `reference/examples.md` — worked type examples: unknown-narrowing,
  discriminated unions, generics with constraints, `satisfies`, utility types.
- `reference/tsconfig.md` — recommended strict `compilerOptions` with rationale.
