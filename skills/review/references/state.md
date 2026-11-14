---
name: state-review-lens
description: A code review lens for inspecting state management, single sources of truth, persistence, and cleanup.
---

# Lens: State

> **Core Question:** Who owns this state, where does it live, and what happens when it is missing, stale, corrupt, or re-initialized?  
> **Rule:** Every piece of state must have one clear writer and a single source of truth.

---

## Procedure

For every state location touched (in-memory, DOM, URL, `localStorage`, cache, server):

1. **Identify the Writer:** Uncoordinated multiple writers = **Blocker**.
2. **Check Derivations:** Compute derived values instead of storing duplicates.
3. **Verify Edge Cases & Re-entry:** Trace missing, stale, string-coerced, or corrupted values, and verify re-running initialization/handlers is safe.

---

## Core Red Flags

- **Non-Idempotent Operations:** Setup or state mutations running twice (e.g., repeated navigation, hot reload, re-renders, rapid toggles) causing double-bound listeners, duplicate API calls, or compounded mutations.
- **Duplicate Truths:** Same fact stored in multiple locations (e.g., JS variable + DOM attribute, state + URL). Pick one authority; derive the rest.
- **Fragile Persistence:** Unguarded `localStorage` access (throws in private mode), treating stored string `"false"` as boolean, or storing private data in storage/cookies.
- **Init & Timing:** Reading before writing, pre-paint reads racing CSS (causing flash of unstyled content), or non-idempotent re-initialization (double-binding events).
- **Missing Cleanup:** Event listeners, timers, or observers remaining active after a component/element is destroyed.
- **Unmanaged Transitions:** Complex multi-state flows missing an explicit state model, or allowing illegal state transitions.

---

## Not a Finding

- Local variables scoped strictly within a single function.
- Explicitly documented caches with clear invalidation rules.
- Single-writer, multi-reader state patterns.
