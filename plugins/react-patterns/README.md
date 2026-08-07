# react-patterns

A skill-first Claude Code plugin for modern React component and hook patterns.

## What it does

The `react-patterns` skill auto-invokes when you build or review React
components and hooks in `.jsx`/`.tsx` files, or mention "component",
`useState`, `useEffect`, custom hooks, re-renders, keys, context, controlled
inputs, or memoization. It applies:

- rules of hooks (top-level only, no conditional hooks)
- state colocation, lifting only when shared, deriving over duplicating
- stable, meaningful keys (never array index for dynamic lists)
- controlled inputs
- effects with correct dependencies and cleanup
- memoization only when measured
- accessibility basics (semantic elements, labels, focus)
- avoiding prop drilling; using Context sparingly

## Structure

- `skills/react-patterns/SKILL.md` — lean core rules + do/don't table
- `skills/react-patterns/reference/` — component composition examples and hook
  patterns (effects, custom hooks, memoization decision guide)

## Install

Place this directory under your Claude Code `plugins/` folder. The skill loads
automatically when a matching task is detected.

## License

MIT © Matthews Wong
