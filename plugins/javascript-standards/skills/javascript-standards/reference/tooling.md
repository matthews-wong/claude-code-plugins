# Tooling baseline

Let the formatter and linter own whitespace/quotes/semicolons — never hand-fight
them. Run lint + format before committing.

## package.json

```jsonc
{
  "type": "module",          // opt into ESM for .js files
  "engines": { "node": ">=20" },
  "scripts": {
    "lint": "eslint .",
    "format": "prettier --write ."
  }
}
```

## ESLint (flat config, eslint.config.js)

```js
import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    languageOptions: { ecmaVersion: 'latest', sourceType: 'module' },
    rules: {
      'no-var': 'error',
      'prefer-const': 'error',
      eqeqeq: ['error', 'smart'],
      'no-eq-null': 'off',
      'no-empty': ['error', { allowEmptyCatch: false }],
      'no-unused-vars': 'warn',
      'prefer-arrow-callback': 'warn',
      'no-param-reassign': ['error', { props: true }],
    },
  },
];
```

## Prettier (.prettierrc)

```json
{ "singleQuote": true, "semi": true, "trailingComma": "all", "printWidth": 100 }
```

## Notes

- Prefer Node's built-in test runner (`node --test`) or Vitest for tests.
- Use `node:` protocol imports for built-ins (`import fs from 'node:fs'`).
- In TypeScript projects, pair these with `@typescript-eslint` and see the
  `typescript-typing` plugin for strict `tsconfig` settings.
