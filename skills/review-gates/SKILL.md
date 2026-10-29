---
name: review-gates
description: >-
  Default review gates for any of Sarah's projects — which review runs when, on which
  model, at what context cost. Use before every commit, when integrating a helper's
  lane, and when a batch of PLAN.md items is done. If the project has its own
  review-workflow skill, follow that too; it wins on conflict.
---

# Review gates

Goal: quality at the lowest token cost. Reviews read diffs, not the codebase, and heavy
output stays out of the orchestrator's context.

## Gate 0 — self-check before every commit (whoever commits)

1. While iterating: the project's fast gate (`npm run gate:fast` or equivalent).
2. Before the commit: the full gate (`npm run gate`). Only known failures allowed
   (listed in `PLAN.md`).
3. The project's constraints from its `CLAUDE.md`.
4. No raw logs, no screenshots. Helpers report in ≤ 15 lines (see `delegate`).

## Gate 1 — diff review, per lane or per own commit (orchestrator)

1. Read only `git diff <main>...lane/<name>` (or the staged diff) plus the helper's report.
2. Lens: does each commit do what its item says; stays in owned files; project
   constraints hold; each new test would fail before the change; no duplicate tests.
3. Verdict `SHIP` / `BLOCKED` + ≤ 5 one-line findings.
4. Blockers go back to the same helper via `SendMessage`. Should-fix → follow-up commit
   or a line in `PLAN.md` Next.
5. Fresh eyes, one pass per lane or own commit, before integrating: one Haiku subagent, read-only, briefed
   with the diff and the rules it touches only (no history). Blockers only, ≤ 10 lines. Not per edit.

## Gate 2 — whole batch, once (Sonnet subagent)

1. One Sonnet helper runs the `review` skill over the batch diff. Blockers only, ≤ 10 lines.
2. Fix blockers only. No iterate-to-a-score loop; no expert panel unless Sarah asks.
3. Visual sign-off is Sarah's: point at the pages to open.
4. Update `PLAN.md` and Lessons.

## Models

- Helpers and reviewers: Sonnet, passed explicitly. Orchestrator: briefs, Gate 1,
  merges, docs — judgment only. No Haiku for implementation or review, except the one
  fresh-eyes pass in Gate 1.
