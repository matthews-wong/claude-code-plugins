# Design tokens & dark mode

Tokens are named CSS custom properties that carry *intent*. Components reference tokens; only the token layer knows raw values. Theming = re-declaring token values, never rewriting components.

## Token layers

1. **Primitive** — raw scale values (`--blue-500`, `--size-4`). No semantics.
2. **Semantic** — role-based aliases that components use (`--color-surface`, `--color-text`, `--space-md`). Point at primitives.

Components use *semantic* tokens only. Swapping a theme rewires semantic → primitive; components never change.

## Example

```css
:root {
  /* --- primitives --- */
  --gray-0:   #ffffff;
  --gray-50:  #f7f8fa;
  --gray-900: #10131a;
  --blue-500: #2b6cff;
  --blue-300: #86abff;

  /* --- spacing scale (rem, base 16px) --- */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2.5rem;

  /* --- radius & type --- */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --font-sans: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;

  /* --- semantic (light defaults) --- */
  --color-bg:      var(--gray-50);
  --color-surface: var(--gray-0);
  --color-text:    var(--gray-900);
  --color-accent:  var(--blue-500);
  --color-border:  #e2e6ee;
}

/* Automatic dark mode: only semantic values change */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg:      var(--gray-900);
    --color-surface: #171b24;
    --color-text:    var(--gray-50);
    --color-accent:  var(--blue-300);
    --color-border:  #262c38;
  }
}

/* Manual override wins over OS preference (toggle sets data-theme on <html>) */
:root[data-theme="light"] {
  --color-bg: var(--gray-50);
  --color-surface: var(--gray-0);
  --color-text: var(--gray-900);
  --color-accent: var(--blue-500);
  --color-border: #e2e6ee;
}
:root[data-theme="dark"] {
  --color-bg: var(--gray-900);
  --color-surface: #171b24;
  --color-text: var(--gray-50);
  --color-accent: var(--blue-300);
  --color-border: #262c38;
}
```

## Consuming tokens

```css
body {
  margin: 0;
  background: var(--color-bg);
  color: var(--color-text);
  font-family: var(--font-sans);
}

.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-lg);
}
```

## Rules

- Never hardcode a hex or spacing literal in a component rule — reference a token.
- Verify contrast (WCAG AA: 4.5:1 body text) in *both* themes; dark mode is not just inverted light.
- Keep primitives theme-agnostic; only semantic tokens differ per theme.
- Prefer `color-scheme: light dark;` on `:root` so native form controls and scrollbars theme correctly.
