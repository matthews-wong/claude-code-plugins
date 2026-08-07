# React Component Patterns

## Colocate state, lift only when shared

```tsx
// Colocated: only the input owns its draft
function SearchBox({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('');
  return (
    <input
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      onKeyDown={(e) => e.key === 'Enter' && onSearch(query)}
    />
  );
}
```

Lift state to the nearest common parent only when two siblings must read/write
the same value. Don't hoist higher than necessary — it forces needless
re-renders and prop plumbing.

## Derive, don't duplicate, state

```tsx
// Don't — fullName is redundant state that can drift
const [first, setFirst] = useState('');
const [last, setLast] = useState('');
const [fullName, setFullName] = useState('');

// Do — derive during render
const fullName = `${first} ${last}`.trim();
```

## Stable keys

```tsx
// Don't — index breaks when the list reorders/filters
{todos.map((todo, i) => <Row key={i} todo={todo} />)}

// Do — stable domain id
{todos.map((todo) => <Row key={todo.id} todo={todo} />)}
```

## Controlled inputs

```tsx
function Field() {
  const [value, setValue] = useState('');
  return (
    <>
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        value={value}
        onChange={(e) => setValue(e.target.value)}
      />
    </>
  );
}
```

Pick controlled *or* uncontrolled and stay there. Never pass `value` without
`onChange`, and never flip a field between `undefined` and a string.

## Composition over prop drilling

```tsx
// Don't — threading `user` through layers that don't use it
<Page user={user}><Sidebar user={user}><Profile user={user} /></Sidebar></Page>

// Do — pass children / slots so intermediate layers stay agnostic
<Page>
  <Sidebar>
    <Profile user={user} />
  </Sidebar>
</Page>
```

## Context — sparingly, for low-churn globals

```tsx
const ThemeContext = createContext<'light' | 'dark'>('light');

function useTheme() {
  return useContext(ThemeContext);
}

// Good fits: theme, current user, locale, feature flags.
// Bad fits: fast-changing values (mouse position, form drafts) — every
// consumer re-renders on each change. Split contexts or use a store instead.
```

## Accessibility basics

```tsx
// Don't
<div className="btn" onClick={submit}>Save</div>

// Do — real button: keyboard, focus, and screen-reader support for free
<button type="button" onClick={submit}>Save</button>

// Images: meaningful alt, or alt="" for decorative
<img src={avatar} alt={`${name}'s avatar`} />

// Icon-only control needs an accessible name
<button type="button" aria-label="Close dialog" onClick={close}>
  <XIcon aria-hidden="true" />
</button>
```

Prefer semantic elements (`nav`, `main`, `ul`, `label`, `button`) before
reaching for `role`/`aria-*`. Keep a logical heading order and visible focus.
