# Layout recipes

Copy-paste patterns. All mobile-first and breakpoint-light.

## Responsive card grid (no media query)

Fills available space, wraps automatically, never smaller than 16rem.

```css
.card-grid {
  display: grid;
  gap: var(--space-md);
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr));
}
```

`min(100%, 16rem)` prevents overflow on very narrow screens where 16rem exceeds the viewport.

## Flexible toolbar / nav (one-dimensional)

```css
.toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-sm);
}
.toolbar__spacer { margin-inline-start: auto; } /* pushes trailing items right */
```

## Holy-grail page shell (two-dimensional → grid)

```css
.app {
  display: grid;
  min-block-size: 100dvh;
  grid-template-rows: auto 1fr auto;      /* header / main / footer */
  grid-template-columns: 1fr;
}

@media (min-width: 48rem) {
  .app {
    grid-template-columns: minmax(12rem, 16rem) 1fr;
    grid-template-areas:
      "header header"
      "sidebar main"
      "footer footer";
  }
  .app__header { grid-area: header; }
  .app__sidebar { grid-area: sidebar; }
  .app__main   { grid-area: main; }
  .app__footer { grid-area: footer; }
}
```

## Fluid type with clamp (no breakpoints)

```css
:root {
  /* min 1rem, scales with viewport, max 1.5rem */
  --step-0: clamp(1rem, 0.9rem + 0.5vw, 1.5rem);
}
h1 { font-size: clamp(1.75rem, 1.2rem + 2.5vw, 3rem); }
```

## Container query — component adapts to its slot

```css
.card { container-type: inline-size; container-name: card; }

.card__body { display: grid; gap: var(--space-sm); }

@container card (min-width: 24rem) {
  .card__body { grid-template-columns: 8rem 1fr; } /* media beside text once wide */
}
```

Use this over a media query whenever the same component appears in slots of different widths (main column vs narrow sidebar).

## Constrained readable measure

```css
.prose { max-inline-size: 65ch; margin-inline: auto; }
```

## Aspect-ratio media box (no padding hack)

```css
.media { aspect-ratio: 16 / 9; inline-size: 100%; object-fit: cover; }
```

## Reduced motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important; /* justified: hard override of decorative motion */
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
