# React Hook Patterns

## Rules of hooks

```tsx
// Don't — conditional hook: order changes between renders
function Bad({ enabled }: { enabled: boolean }) {
  if (enabled) {
    const [n, setN] = useState(0); // ILLEGAL
  }
}

// Do — hook at top level, branch inside
function Good({ enabled }: { enabled: boolean }) {
  const [n, setN] = useState(0);
  if (!enabled) return null;
  return <span>{n}</span>;
}
```

## Effects: correct deps + cleanup

```tsx
useEffect(() => {
  const controller = new AbortController();
  fetch(`/api/items/${id}`, { signal: controller.signal })
    .then((r) => r.json())
    .then(setItem)
    .catch((e) => {
      if (e.name !== 'AbortError') setError(e);
    });
  return () => controller.abort(); // cleanup on unmount / id change
}, [id]); // every reactive value read inside must be listed
```

Rules:
- List **every** reactive value the effect reads. Don't disable the lint rule to
  hide a missing dep — fix the dependency instead (memoize it, move it in, or
  use a functional `setState`).
- Always clean up subscriptions, timers, listeners, and in-flight requests.
- Prefer a data-fetching library (React Query, SWR, RTK Query) or a framework
  loader over hand-rolled `useEffect` fetching.

## Effects you don't need

```tsx
// Don't — syncing derived state via an effect
const [items, setItems] = useState<Item[]>([]);
const [count, setCount] = useState(0);
useEffect(() => setCount(items.length), [items]); // unnecessary render

// Do — derive during render
const count = items.length;
```

Also avoid effects for: transforming data for render, handling user events
(do it in the handler), or resetting state on prop change (use a `key` instead).

## Functional updates avoid stale deps

```tsx
// Don't — closes over `count`, needs it in deps
const inc = useCallback(() => setCount(count + 1), [count]);

// Do — updater form; stable, no dep on count
const inc = useCallback(() => setCount((c) => c + 1), []);
```

## Custom hooks

```tsx
function useDebouncedValue<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delayMs);
    return () => clearTimeout(id);
  }, [value, delayMs]);
  return debounced;
}
```

Extract repeated stateful logic into a `use*` hook. It must obey the rules of
hooks itself and should return a stable, minimal API.

## Memoization decision guide

Reach for memoization only when one of these is true — otherwise skip it:

1. **`useMemo`** — a computation in render is measurably expensive (large sort,
   heavy parse) and its inputs rarely change.
2. **`useCallback`** — a function is passed to a `React.memo` child or used as an
   effect dependency, and you need referential stability to prevent re-renders.
3. **`React.memo`** — a pure child re-renders often with the same props and it
   shows up in a profile.

```tsx
// Justified: expensive derived data
const sorted = useMemo(
  () => [...rows].sort((a, b) => b.score - a.score),
  [rows],
);
```

Premature `useMemo`/`useCallback` adds allocation and cognitive cost for no
benefit. Measure with the React Profiler before optimizing. (React 19's compiler
can automate much of this — hand-memoize only proven hot paths.)
