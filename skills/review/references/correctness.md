---
name: correctness-review-lens
description: A code review lens focused strictly on detecting functional correctness bugs, edge cases, and runtime failures.
---

# Lens: Correctness

> **Core Question:** Will this produce a wrong result or crash under realistic conditions?  
> **Rule:** Name the concrete inputs and the wrong output, or drop the issue.

---

## Procedure

1. **Trace Paths:** Trace one typical input, then trace edge cases: empty, zero, single/many, null/missing, duplicates, out-of-order, or very large inputs.
2. **Check References:** Verify callers match changed signatures and inspect time/timezone/DST boundaries.

---

## Core Red Flags

- **Flow & Data:** Off-by-one errors, unreachable branches, unhandled `switch` cases, unintended mutation, float/identity equality (`==`), or skipped cleanup on early returns.
- **Absence & Falsiness:** Unchecked `null`/`undefined` (e.g., `querySelector`), treating `0`/`""`/`false` as absent, or missing map keys silently evaluating to empty strings.
- **Timing & State:** Non-idempotent event handlers, un-cancelled async tasks, `setTimeout` used as a sync hack, or out-of-sync state updates.
- **External Calls:** Unhandled failures for fetches, file reads, or storage access (e.g., `localStorage` throwing in private mode).
- **Scope:** Changed shared utilities missing a global search/grep for affected call sites.

---

## Validation & Output

Before flagging an issue, verify it by tracing to a real caller, running a quick test, or proving no guards exist upstream.

**Required Finding Format:**  
`[Inputs / Conditions]` → `[What actually happens]` → `[What should happen]`
