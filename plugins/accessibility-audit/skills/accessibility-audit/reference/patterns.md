# Accessible Markup Patterns (inaccessible → fixed)

## Icon-only button

Bad — no accessible name; a `<div>` isn't keyboard operable:
```html
<div class="icon-btn" onclick="del()">🗑️</div>
```
Good:
```html
<button type="button" class="icon-btn" onclick="del()">
  <svg aria-hidden="true" focusable="false">...</svg>
  <span class="visually-hidden">Delete item</span>
</button>
```
`.visually-hidden` keeps text for screen readers while hidden visually (clip pattern, not `display:none`).

## Informative vs decorative image

```html
<!-- informative -->
<img src="chart.png" alt="Revenue rose 20% from Q1 to Q2">
<!-- decorative -->
<img src="swoosh.png" alt="">
```

## Labeled input with error

Bad — placeholder is not a label; error not associated:
```html
<input type="email" placeholder="Email">
<span class="err">Invalid</span>
```
Good:
```html
<label for="email">Email address</label>
<input id="email" type="email" name="email"
       autocomplete="email"
       aria-describedby="email-err" aria-invalid="true" required>
<span id="email-err" class="err">Enter a valid email, e.g. name@example.com</span>
```

## Grouped controls

```html
<fieldset>
  <legend>Notification method</legend>
  <label><input type="radio" name="notify" value="email"> Email</label>
  <label><input type="radio" name="notify" value="sms"> SMS</label>
</fieldset>
```

## Link vs button

Use `<a href>` to navigate, `<button>` to act. Never `<a href="#" onclick>` for an action, and never a `<div>`/`<span>` as a clickable control.

## Accessible modal dialog (focus management)

```html
<div role="dialog" aria-modal="true" aria-labelledby="dlg-title">
  <h2 id="dlg-title">Confirm delete</h2>
  <p>This cannot be undone.</p>
  <button type="button" id="confirm">Delete</button>
  <button type="button" id="cancel">Cancel</button>
</div>
```
Requirements: move focus into the dialog on open; trap focus within while open; restore focus to the trigger on close; close on `Esc`; make background inert (`inert` attribute or `aria-hidden` on siblings). Prefer the native `<dialog>` element with `showModal()`, which handles much of this.

## Skip link

```html
<a href="#main" class="skip-link">Skip to main content</a>
...
<main id="main" tabindex="-1"> ... </main>
```
`.skip-link` is visually hidden until focused.

## Live region for async status

```html
<div role="status" aria-live="polite" class="visually-hidden" id="status"></div>
<script> document.getElementById('status').textContent = 'Saved'; </script>
```
Announces without stealing focus. Use `aria-live="assertive"` only for urgent messages.

## Custom widget note

For tabs, comboboxes, menus, accordions, sliders, etc., follow the WAI-ARIA Authoring Practices Guide (APG) for the required roles, states, and keyboard interaction. If you cannot implement the full keyboard model, use a native element or a vetted accessible component library instead of partial ARIA.

## `.visually-hidden` utility (reference)

```css
.visually-hidden {
  position: absolute;
  width: 1px; height: 1px;
  padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0 0 0 0);
  white-space: nowrap; border: 0;
}
```
