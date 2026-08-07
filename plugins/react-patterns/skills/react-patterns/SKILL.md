---
name: react-patterns
description: >-
  Apply modern React patterns when building or reviewing components and hooks in
  .jsx/.tsx files. Triggers on "component", "useState", "useEffect", "custom
  hook", "re-render", "props drilling", "context", "controlled input", "keys",
  "useMemo/useCallback", "effect cleanup", or React accessibility. Use whenever
  authoring React UI or debugging hook/render behavior.
---

# React Patterns

Opinionated, current React best practices (function components + hooks). Apply
while building; flag violations while reviewing.

## Core rules

1. **Rules of hooks.** Call hooks only at the top level of a component or custom
   hook — never inside conditions, loops, or nested functions, and never after
   an early `return`. Custom hooks start with `use`.
2. **Colocate state, then lift only when shared.** Keep state in the lowest
   component that needs it. Lift to the nearest common parent only when two
   siblings must share it. Derive values during render instead of storing
   duplicated state in another `useState`.
3. **Stable, meaningful keys.** Use a stable domain id (`item.id`) as `key`.
   Never use the array index for lists that reorder, insert, or delete — it
   corrupts state and identity.
4. **Controlled inputs.** Drive form fields with `value` + `onChange` bound to
   state. Don't mix controlled and uncontrolled (no `value` without `onChange`,
   no switching `undefined` ↔ a value).
5. **Effects: right deps + cleanup.** Include every reactive value the effect
   reads in the dependency array — don't lie to satisfy the linter. Return a
   cleanup for subscriptions, timers, and listeners; abort fetches. Most data
   fetching belongs in a library (React Query/RTK Query) or a framework loader,
   not a raw `useEffect`. Don't use effects to sync state you can derive.
6. **Memoize only when measured.** `useMemo`/`useCallback`/`React.memo` add
   complexity and aren't free. Reach for them for proven expensive computations
   or to stabilize props to a memoized child — not by default.
7. **Accessibility basics.** Use semantic elements (`button`, `nav`, `label`)
   over `div` with `onClick`. Associate labels with inputs, provide `alt`, keep
   focus order sane, and add `aria-*` only when semantics can't be expressed
   natively.
8. **Avoid prop drilling; use context sparingly.** For 2–3 levels, pass props or
   compose with `children`. Reach for Context for genuinely global, low-churn
   values (theme, auth, locale) — not high-frequency state, which re-renders all
   consumers.
9. **Pure render.** No side effects, mutations, or subscriptions during render.
   Don't mutate props or state — replace with new objects/arrays.

## Quick do / don't

| Don't | Do |
| --- | --- |
| `if (x) useEffect(...)` | call hooks unconditionally at top level |
| `key={index}` on a reorderable list | `key={item.id}` |
| `<input value={v} />` (no handler) | `<input value={v} onChange={...} />` |
| `useEffect(() => setFull(a+" "+b), [a,b])` | derive `const full = a+" "+b` in render |
| `useEffect(fetch, [])` with no cleanup | abort in cleanup, or use a data lib |
| `<div onClick=...>` | `<button onClick=...>` |
| `useCallback` everywhere | memoize only measured hot paths |

## Reference (load on demand)

- `reference/components.md` — component composition, lifting state, controlled
  forms, keys, context, and accessibility examples.
- `reference/hooks.md` — useEffect cleanup + deps, custom hooks, memoization
  decision guide, and common anti-patterns with fixes.
