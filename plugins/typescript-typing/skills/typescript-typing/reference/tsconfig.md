# Recommended strict tsconfig

`strict: true` is the floor, not the ceiling. The extra flags below catch real
classes of bugs the base `strict` preset leaves open.

```jsonc
{
  "compilerOptions": {
    // Type-safety floor
    "strict": true,                        // implies noImplicitAny, strictNullChecks,
                                           // strictFunctionTypes, strictBindCallApply,
                                           // strictPropertyInitialization, alwaysStrict,
                                           // useUnknownInCatchVariables, and more
    "noUncheckedIndexedAccess": true,      // arr[i] / obj[key] is T | undefined
    "exactOptionalPropertyTypes": true,    // `x?: T` ≠ `x: T | undefined`
    "noImplicitOverride": true,            // require `override` keyword
    "noImplicitReturns": true,             // every code path returns
    "noFallthroughCasesInSwitch": true,
    "noPropertyAccessFromIndexSignature": true,
    "forceConsistentCasingInFileNames": true,

    // Module / output
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",         // or "NodeNext" for Node without a bundler
    "verbatimModuleSyntax": true,          // explicit `import type`
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "isolatedModules": true
  }
}
```

## Why the extra flags matter

- **`noUncheckedIndexedAccess`** — the single highest-value flag beyond `strict`.
  Turns silent `undefined` from array/record access into a checked case.
- **`exactOptionalPropertyTypes`** — distinguishes "absent" from "present but
  `undefined`", which matters for `in` checks and API payloads.
- **`useUnknownInCatchVariables`** (on via `strict`) — `catch (e)` gives `unknown`,
  forcing you to narrow before using the error.
- **`verbatimModuleSyntax`** — forces `import type { X }` for type-only imports,
  preventing accidental runtime imports and easing bundler tree-shaking.

## catch narrowing

```ts
try {
  risky();
} catch (error) {
  // error is `unknown`
  const message = error instanceof Error ? error.message : String(error);
  logger.error(message);
}
```

Pair with `@typescript-eslint` rules `no-explicit-any`,
`no-unnecessary-condition`, and `consistent-type-imports`.
