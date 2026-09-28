---
name: ux-review-lens
description: A deep-review judgment lens for whether an interface change serves the user's task, read against runtime screenshots.
---

# Lens: UX Judgment

> **Core Question:** Does this change serve the task the user came to do, or merely add to the screen?
> **Rule:** `deep` only, and after phase 3 — this lens reads the screenshots. You cannot judge what you have not seen.

This lens produces **Questions** more often than findings, and that is correct. An automated verdict on taste is noise, and noise is what teaches people to skip a review.

---

## The Questions

- **Task:** name in one sentence what the user came to do. Does this change make it longer, less obvious, or conditional on something new?
- **Duplicate affordances:** is there now a second way to do the same thing — an old path nobody removed plus a new one? One must go.
- **Hierarchy:** one primary action per view. If two things now compete for the same attention, one of them stopped working. Judge from the screenshot, not the markup.
- **Consistency:** a new pattern where an existing one would have done means every future contributor must choose between two. If the new one is genuinely better, the finding is *migrate the old*, not *keep both*.
- **Self-consistency:** motion timing, spacing rhythm, corner language, voice of the copy. A component disagreeing with its neighbours reads as broken even when nothing is wrong.
- **Visible state:** can the user tell what is selected, loading, disabled, or failed without being told? A disabled control must say why, or it reads as broken.
- **Real content:** longest realistic string, empty value, missing image, unusual characters. Design that only works with the demo data is not finished.
- **Copy:** labels naming the action, not the topic. Errors saying what to do next, not what went wrong.
- **Unearned attention:** animation on something incidental, a colour reserved for meaning used decoratively, an interruption for something that could have been passive.
- **Reversal:** can the user undo, go back, or get out — without the back button being the only answer?

---

## Output

- **Question** for a judgment call: what you observed, why it reads oddly, the one thing you would change. The human decides.
- **Finding** only when it is objectively broken against the project's own stated design principles — cite the principle.
- **Never** rewrite copy, restyle a component, or reverse a documented decision on this lens's authority alone.

**Not a finding:** taste that differs from yours · a deliberate rough edge the spec names · anything supported only by "users might prefer".
