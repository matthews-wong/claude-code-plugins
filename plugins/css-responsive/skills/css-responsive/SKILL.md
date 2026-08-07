---
name: css-responsive
description: Use when writing or reviewing CSS/SCSS styling and layout — in .css, .scss, .sass, .less, styled-components, or Tailwind/@apply files — especially for "responsive" design, "mobile-first", "flexbox" vs "grid", "media query", breakpoints, "dark mode", theming with CSS variables / design tokens, "container queries", relative units (rem/em/%/vw/ch/clamp), or fixing layouts that break on small screens. Provides opinionated best practices for adaptive, token-driven, accessible styling.
---

# Responsive CSS

Opinionated defaults for layouts that adapt cleanly across viewports, themes, and devices.

## Core principles

1. **Mobile-first.** Write base styles for the smallest screen, then layer complexity with `min-width` media/container queries. Never start desktop-first and claw back with `max-width` overrides.
2. **Relative units over pixels.** Use `rem` for type and spacing, `%`/`fr`/`minmax()` for layout, `ch` for measure, `clamp()` for fluid scaling. Reserve `px` for borders/hairlines. Set `:root { font-size: 100% }` — never override the root px so user zoom keeps working.
3. **Design tokens.** Define color, spacing, radius, and type as CSS custom properties on `:root`. Reference tokens everywhere; never hardcode a hex or a magic number twice. See `reference/design-tokens.md`.
4. **Theme via tokens, not duplication.** Support dark mode by re-declaring token *values* under `@media (prefers-color-scheme: dark)` (and an optional `[data-theme]` override for a manual toggle). Component rules stay unchanged.
5. **No magic numbers.** A raw `37px` with no comment is a smell. Derive from a token or a scale, or leave a `/* why */` note.
6. **Avoid `!important`.** It signals a specificity problem. Fix the selector or cascade layer instead. Justify in a comment on the rare legitimate use (e.g. overriding a third-party inline style).

## Flexbox vs Grid — choose deliberately

- **Flexbox** for one-dimensional flow where content sizes itself: nav bars, toolbars, tag lists, button rows. Content-out.
- **Grid** for two-dimensional structure you define up front: page shells, card galleries, form layouts, anything with aligned rows *and* columns. Layout-in.
- Rule of thumb: aligning along a single axis with wrapping → flex. Placing items into a defined matrix → grid. They compose — a grid cell can be a flex container.

## Modern responsiveness

- Prefer **intrinsic** patterns that need no breakpoints: `grid-template-columns: repeat(auto-fit, minmax(min(100%, 16rem), 1fr))` and `flex-wrap: wrap` with `flex: 1 1 <basis>`.
- Use **container queries** (`container-type: inline-size` + `@container`) when a component must adapt to *its own* width, not the viewport — reusable cards in varying slots. See `reference/layout-recipes.md`.
- Add media queries only when intrinsic sizing cannot express the change. Name breakpoints by content need, not device.

## Accessibility & robustness

- Respect `prefers-reduced-motion`; gate non-essential animation behind it.
- Keep tap targets ≥ 44×44px and maintain WCAG contrast in *both* themes.
- Never disable focus outlines without a visible replacement.
- Test at 320px width and at 200% zoom.

## References

- `reference/layout-recipes.md` — copy-paste flex/grid/container-query patterns.
- `reference/design-tokens.md` — a full token + dark-mode example.
