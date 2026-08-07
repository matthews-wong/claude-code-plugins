# JavaScript Do / Don't (expanded)

| Topic | Don't | Do | Why |
| --- | --- | --- | --- |
| Modules | `const x = require('x')` | `import x from 'x'` | ESM is the standard; enables static analysis, tree-shaking, top-level await. |
| Exports | one giant `export default {}` | named exports | Named exports rename-safely, tree-shake, and autocomplete. |
| Binding | `var count` | `const`/`let count` | `var` hoists and is function-scoped, leaking across blocks. |
| Reassign | `let name = getName()` never reassigned | `const name = getName()` | `const` signals intent and prevents accidental reassignment. |
| Equality | `if (id == '5')` | `if (id === '5')` | `==` coerces (`'' == 0`, `null == undefined`) — surprising bugs. |
| Nullish | `value || fallback` | `value ?? fallback` | `||` also replaces `0`, `''`, `false`; `??` only replaces null/undefined. |
| Chaining | `a && a.b && a.b.c` | `a?.b?.c` | Concise, and short-circuits on null/undefined only. |
| Async | `.then().then().catch()` | `await` in `try/catch` | Flat control flow, real stack traces, easier branching. |
| Parallel | sequential `await` in a loop | `await Promise.all(items.map(...))` | Independent work should run concurrently. |
| Errors | `catch (e) {}` | handle, rethrow, or add `cause` | Silent catches hide failures and corrupt state. |
| Error type | `throw 'bad'` | `throw new Error('bad')` | Only `Error` carries a stack and works with `instanceof`. |
| Mutation | `params.list.push(x)` | `return [...list, x]` | Mutating inputs creates spooky action at a distance. |
| Sort | `arr.sort()` on shared arr | `[...arr].sort()` | `sort`/`reverse` mutate in place. |
| Loops | `for` with index to transform | `map`/`filter`/`reduce` | Expresses intent; avoids off-by-one and mutation. |
| Copies | `Object.assign({}, deep)` | `structuredClone(deep)` | Real deep clone for nested data. |
| Equality of NaN | `x === NaN` | `Number.isNaN(x)` | `NaN === NaN` is false. |
| Numbers | `parseInt(s)` | `parseInt(s, 10)` or `Number(s)` | Always pass a radix. |
| Dead code | leave `// old impl` blocks | delete it | Git remembers; comments rot. |

## Notes

- Prefer `for...of` over `for...in` for arrays; `for...in` walks the prototype
  chain and yields string keys.
- Use `Array.isArray(x)` rather than `x instanceof Array` (works across realms).
- Prefer template literals over string concatenation.
- Guard boundaries: validate/parse external input (network, files, user) before
  trusting its shape.
