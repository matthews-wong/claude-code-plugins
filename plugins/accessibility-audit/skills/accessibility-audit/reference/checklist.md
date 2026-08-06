# WCAG 2.2 AA Checklist (organized by POUR)

Mark each PASS / FAIL / NEEDS-MANUAL-CHECK. SC = Success Criterion.

## Perceivable

- [ ] **1.1.1 Non-text Content (A)** — informative images have meaningful `alt`; decorative images `alt=""`; icon buttons have an accessible name; complex images (charts) have a long description.
- [ ] **1.2.x Media (A/AA)** — captions for video, transcript/audio description as applicable.
- [ ] **1.3.1 Info & Relationships (A)** — structure conveyed programmatically: headings as `<h1-6>`, lists as `<ul>/<ol>`, data in `<table>` with `<th scope>`, labels tied to inputs.
- [ ] **1.3.2 Meaningful Sequence (A)** — DOM order gives a sensible reading order (don't rely on CSS to reorder meaning).
- [ ] **1.3.5 Identify Input Purpose (AA)** — use appropriate `autocomplete` on personal-data fields.
- [ ] **1.4.1 Use of Color (A)** — color is not the sole means of conveying info (errors, links, states also have text/shape/icon).
- [ ] **1.4.3 Contrast Minimum (AA)** — text ≥ 4.5:1; large text (≥ 24px, or ≥ 18.66px bold) ≥ 3:1. Compute only from real color values.
- [ ] **1.4.4 Resize Text (AA)** — usable at 200% zoom without loss of content/function.
- [ ] **1.4.10 Reflow (AA)** — no horizontal scroll at 320px-equivalent width; content reflows.
- [ ] **1.4.11 Non-text Contrast (AA)** — UI components, focus indicators, and meaningful graphics ≥ 3:1 against adjacent colors.
- [ ] **1.4.12 Text Spacing (AA)** — no clipping when line-height/letter/word spacing is increased.

## Operable

- [ ] **2.1.1 Keyboard (A)** — all functionality operable by keyboard.
- [ ] **2.1.2 No Keyboard Trap (A)** — focus can move away from every component.
- [ ] **2.1.4 Character Key Shortcuts (A)** — single-key shortcuts can be remapped/disabled.
- [ ] **2.4.1 Bypass Blocks (A)** — skip link and/or landmarks to bypass repeated nav.
- [ ] **2.4.2 Page Titled (A)** — descriptive `<title>`.
- [ ] **2.4.3 Focus Order (A)** — focus order preserves meaning and operability.
- [ ] **2.4.4 Link Purpose (A)** — link text (with context) describes its destination; no bare "click here".
- [ ] **2.4.6 Headings & Labels (AA)** — descriptive headings and labels; logical heading hierarchy (no skipped levels without reason).
- [ ] **2.4.7 Focus Visible (AA)** — visible focus indicator on all interactive elements (don't remove `outline` without a replacement).
- [ ] **2.4.11 Focus Not Obscured (Minimum) (AA — new 2.2)** — focused element not entirely hidden by sticky/overlay content.
- [ ] **2.5.3 Label in Name (A)** — visible label text is included in the accessible name.
- [ ] **2.5.7 Dragging Movements (AA — new 2.2)** — any drag action has a single-pointer (click/tap) alternative.
- [ ] **2.5.8 Target Size (Minimum) (AA — new 2.2)** — pointer targets ≥ 24x24 CSS px (or adequate spacing/exceptions).

## Understandable

- [ ] **3.1.1 Language of Page (A)** — `<html lang="...">` set correctly.
- [ ] **3.2.1 On Focus (A)** / **3.2.2 On Input (A)** — no unexpected context change on focus or input.
- [ ] **3.2.6 Consistent Help (A — new 2.2)** — help mechanisms appear in a consistent order across pages.
- [ ] **3.3.1 Error Identification (A)** — errors described in text and programmatically associated.
- [ ] **3.3.2 Labels or Instructions (A)** — inputs have labels/instructions; required fields indicated in text.
- [ ] **3.3.3 Error Suggestion (AA)** — suggest a correction when known.
- [ ] **3.3.7 Redundant Entry (A — new 2.2)** — don't force re-entering info already provided in the same process.
- [ ] **3.3.8 Accessible Authentication (Minimum) (AA — new 2.2)** — no cognitive function test (puzzles, transcription) required; allow password managers/paste.

## Robust

- [ ] **4.1.2 Name, Role, Value (A)** — all UI components expose correct name, role, and state; custom widgets follow ARIA Authoring Practices; states kept in sync.
- [ ] **4.1.3 Status Messages (AA)** — status/toast/validation messages announced via `role="status"`/`aria-live` without moving focus.
- [ ] Valid, well-formed markup; no duplicate `id`s; ARIA only where native semantics fall short.

## Severity guidance
- **Blocker**: keyboard trap, control with no accessible name, image conveying essential info with no alt, form field with no label, focus lost/unmanaged in a modal.
- **Serious**: contrast failure on body text, missing focus indicator, wrong ARIA role, heading structure broken.
- **Moderate/Minor**: redundant ARIA, sub-optimal link text, minor spacing/reflow issues.

## Tooling (recommend, don't fake results)
axe-core / axe DevTools, Lighthouse, WAVE, Pa11y, IBM Equal Access. Automated tools catch ~30-50% of issues — always pair with keyboard-only testing and a screen reader (NVDA, JAWS, VoiceOver).
