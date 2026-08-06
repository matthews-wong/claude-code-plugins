# accessibility-audit

A skill-first Claude Code plugin that audits UI markup against **WCAG 2.2 AA** basics.

## What it does
Auto-invokes on "accessibility", "a11y", "WCAG", "screen reader", "keyboard navigation", "alt text", "color contrast", or "ARIA", or when component markup is shown. It checks text alternatives, form labels, contrast, keyboard operability, focus order and visibility, ARIA correctness, and semantic HTML, then reports issues mapped to specific success criteria with corrected markup.

## Structure
- `skills/accessibility-audit/SKILL.md` — audit method + highest-impact checks + WCAG 2.2 additions.
- `skills/accessibility-audit/reference/checklist.md` — full POUR checklist mapped to WCAG 2.2 AA success criteria.
- `skills/accessibility-audit/reference/patterns.md` — accessible-vs-inaccessible markup snippets (icon buttons, forms, modals, live regions, skip links).

## Usage
Paste HTML/JSX/Vue/component markup and ask for an accessibility audit. The skill activates automatically.

## Note
Contrast ratios are only reported when computed from real color values; keyboard/focus/screen-reader behavior is flagged for manual testing. Recommends axe-core, Lighthouse, WAVE, Pa11y, and NVDA/JAWS/VoiceOver rather than claiming an automated pass.

## License
MIT © Matthews Wong
