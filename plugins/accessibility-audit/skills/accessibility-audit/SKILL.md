---
name: accessibility-audit
description: Use when auditing or fixing UI for accessibility — triggers on "accessibility", "a11y", "WCAG", "screen reader", "keyboard navigation", "alt text", "color contrast", "ARIA", "focus order", "accessible form", or when HTML/JSX/Vue/component markup is shown and the user wants it usable by everyone. Reports issues mapped to WCAG 2.2 AA success criteria with concrete fixes.
---

# Accessibility Audit (WCAG 2.2 AA)

Audit UI markup or components against WCAG 2.2 Level AA basics and return actionable fixes. Work from the actual markup shown; distinguish what you can verify statically from what needs a browser, assistive tech, or a human.

## Method

1. **Inventory the UI.** Identify interactive elements (links, buttons, inputs, custom widgets), images/media, headings, landmarks, and any ARIA.
2. **Run the checklist** in `reference/checklist.md`, grouped by POUR (Perceivable, Operable, Understandable, Robust). Mark each PASS / FAIL / NEEDS-MANUAL-CHECK.
3. **Report findings**: table of Severity | Issue | WCAG SC | Element | Fix. Order by severity (blockers first).
4. **Show corrected markup** for each failing element.
5. **List manual checks** the audit cannot fully verify (contrast needs computed colors, keyboard/focus needs a live DOM, screen-reader output needs AT).

## Highest-impact checks (start here)

1. **Text alternatives (1.1.1).** Every informative `<img>` has meaningful `alt`; decorative images use `alt=""`. Icon-only buttons/links have an accessible name (`aria-label` or visually-hidden text). No "image of…" filler.
2. **Semantic HTML first.** Use native `<button>`, `<a href>`, `<nav>`, `<main>`, `<label>`, `<h1-6>`, lists, and tables before reaching for ARIA. A `<div onclick>` is not keyboard-accessible.
3. **Form labels (1.3.1, 3.3.2, 4.1.2).** Every control has a programmatic label (`<label for>` or wrapping `<label>`); grouped controls use `<fieldset>`/`<legend>`; errors are announced and associated (`aria-describedby`, `aria-invalid`).
4. **Color contrast (1.4.3, 1.4.11).** Text ≥ 4.5:1 (≥ 3:1 for large text ≥ 24px / 18.66px bold); UI components and graphical objects ≥ 3:1. Color is never the only way to convey meaning (1.4.1).
5. **Keyboard operability (2.1.1, 2.1.2).** All functionality works with keyboard alone; no keyboard traps. Custom widgets implement expected key handling (Enter/Space/arrows/Esc per the ARIA Authoring Practices).
6. **Focus visible & ordered (2.4.7, 2.4.3, 2.4.11).** A clearly visible focus indicator exists; DOM order matches reading/visual order; focus is not obscured by sticky headers (2.4.11 new in 2.2). Manage focus on route changes and dialog open/close.
7. **ARIA used correctly (4.1.2).** Correct `role`/state/property, kept in sync with JS. Prefer no ARIA over wrong ARIA. Don't set `aria-hidden` on focusable elements. `role` must match behavior.

## WCAG 2.2 additions to watch

- **2.4.11 Focus Not Obscured**, **2.5.7 Dragging Movements** (provide a single-pointer alternative), **2.5.8 Target Size (min 24x24 CSS px)**, **3.3.7 Redundant Entry**, **3.3.8 Accessible Authentication** (no cognitive-only test like solving a puzzle). See `reference/checklist.md`.

## Output

Findings table + corrected markup + manual-check list. Do NOT report a numeric contrast ratio unless you compute it from the actual hex/RGB values given; otherwise mark it NEEDS-MANUAL-CHECK. Recommend axe-core, Lighthouse, WAVE, Pa11y, and manual screen-reader testing (NVDA/JAWS/VoiceOver) rather than claiming an automated pass.

## References

- `reference/checklist.md` — full POUR checklist mapped to WCAG 2.2 AA success criteria.
- `reference/patterns.md` — accessible-vs-inaccessible markup snippets (icon buttons, forms, modals, custom widgets).
