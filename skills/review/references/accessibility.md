---
name: accessibility-review-lens
description: A standing code review lens for inspecting HTML, CSS, and interactive components for accessibility compliance.
---

# Lens: Accessibility

> **Core Question:** Can everyone—regardless of interaction method, sight, or motion sensitivity—navigate and use this component?  
> **Rule:** Check markup semantics first, measure contrast/focus explicitly, and verify runtime keyboard flow.

---

## Static Checks (Diff Review)

- **Semantics & ARIA:** Prefer native HTML (`<button>`, `<a href>`) over ARIA re-implementations (`<div role="button">`). Ensure `aria-label` includes any visible label text, update `aria-*` state dynamically, and never place `aria-hidden` on a focusable element.
- **Labels & Names:** Every input needs a `<label>` (or `aria-labelledby`). Icon-only controls require accessible names. Placeholders do not count as labels.
- **Focus & Order:** Maintain logical DOM order (avoid positive `tabindex`). Ensure hidden elements or closed overlays are removed or marked `inert`.
- **Contrast & Sensory:** Verify text contrast (4.5:1 standard, 3:1 for large text/UI components). Never rely solely on color, shape, or location to convey meaning. Honor `prefers-reduced-motion`.
- **Content:** Link text must be meaningful out of context (avoid "click here").

---

## Runtime Checks

- **Keyboard Navigation:** Tab through the interface to ensure full reachability, visible focus rings, logical visual order, and no keyboard traps.
- **Control Operation:** Test Space/Enter for buttons, Escape for modals/overlays, and Arrow keys for composite controls.
- **Zoom & Layout:** Verify reflow at 200% zoom without horizontal scrolling or clipped text.
- **Dynamic Updates:** Ensure state or content changes are announced via live regions or focus placement.
- **Scripts Disabled:** Every essential path still works with JS off. A control that only functions with JS must not render without it — a dead control is worse than no control. OS-level preferences (dark mode, reduced motion) must resolve in CSS, not JS.

---

## Severity Criteria

- **Blocker:** Keyboard traps, unreachable/dead controls, missing accessible names, failing contrast, or `aria-hidden` on focusable elements.
- **Major:** Degraded experience like awkward tab order, low-contrast focus indicators, or vague labels.
