---
name: design-review
description: >-
  Read-only design and brand review of one of Sarah's websites — typography, hierarchy,
  layout at phone/tablet/desktop widths, spacing, navigation, states, motion, contrast,
  design-token discipline, and brand (mark, voice, share metadata). Produces a findings
  table with file:line evidence and a top 3. Use on "design review", "brand review",
  "review the look", "does this feel right", or at the end of a visual milestone.
---

# Design review

Findings only. Which ones to act on is Sarah's call, recorded in the project's
`PLAN.md`. Run it as one **Sonnet** helper (see `delegate`); it reports ≤ 30 lines.

## Read first (and only)

1. The project's design-system doc (e.g. `docs/design-system.md`). Where it disagrees with
   the tokens file, the tokens file wins — report the mismatch as a finding.
2. The tokens file, the layout/base/components CSS, and the page templates.
3. Earlier reviews (e.g. `docs/archive/*-review.md`) — don't re-raise what was decided.

## Measure, don't eyeball

Build to a scratch dir and use the project's browser test helpers (Puppeteer) to read
**computed values** at 375, 768 and 1280px: header height, overflow, font sizes, spacing
between blocks, target sizes, contrast of each text/background pair. No screenshots or
image reads (`helper-guard` blocks them): report computed values, and name the pages and
widths for Sarah to look at.

## Lenses

| Lens | Check |
|---|---|
| Type | Every weight/style used ships a real font file (no faux bold/italic); one clear hierarchy per page (h1 > h2 > body); sizes match the doc's tokens |
| Layout | No horizontal overflow; mobile header doesn't push content below the fold; one left edge unless an exception is declared |
| Space | Space between groups > space within a group; tokens, not raw values |
| Navigation | One visual treatment for nav links; current page marked; targets ≥ 24px (project may set 48) |
| States | Visible `:focus-visible`; hover/pressed/current states present (e.g. `[aria-pressed="true"]`) |
| Motion | `prefers-reduced-motion` respected; nothing loops forever (WCAG 2.2.2) |
| Contrast | Text ≥ 4.5:1, large text/UI ≥ 3:1, links vs body text distinguishable, in light **and** dark |
| System | Rules in the right file/layer; component-local values declared as such; doc matches code |
| Brand | Mark legible at header and favicon size in both themes; one voice and metaphor; title, description, `og:*` correct and absolute; emoji/glyphs widely supported |

## Report

```text
**Verdict.** <two sentences: what's strong, what undercuts it>

| # | Finding | Evidence | Sev | Suggested action |
|---|---|---|---|---|
| 1 | ... | `file.css:12-20` or measured value | high/med/low | ... |

Checked and fine: <one line of what passed>.
Top 3: <numbers and why>.
```

Evidence is a file:line or a measured number, never "looks off". Sarah makes the visual
call; the review makes it easy to make.
