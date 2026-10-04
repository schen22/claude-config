---
name: delegate
description: >-
  Use before EVERY Agent-tool call that starts an implementation or review helper
  (not Explore, claude-code-guide, Plan or a fork). Decides inline vs helper, sizes and
  splits lanes, and gives the brief template (Goal, Owns, Snippets, Gate, Report) so a
  helper doesn't start from zero or burn tokens on logs and screenshots.
---

# Delegate

Cost ≈ context size × steps. Everything a helper reads at startup rides along on every
later step, so a 60-step lane that read 20k of docs pays for it 60 times.

## Decide

One fresh helper per task keeps every context small; one helper doing many tasks carries
all of them on every step (lane H: 5 items, 202k peak, 15.4M tokens).

| Situation | Do |
|---|---|
| Small item (≤ ~2 commits), or the orchestrator already has the files loaded | Inline — a helper's startup (~25–35k) costs more |
| A task that owns files no one else touches | **One fresh helper per task (1–2 items).** Never more than 2 items per helper |
| Several such tasks | Run them one after another; each brief pastes the previous report. Parallel only when they share no files |
| Follow-up on a finished helper's work (a blocker, a small fix) | `SendMessage` the same helper (keeps its context) |
| Review after each task | Orchestrator reads the diff inline (Gate 1 in `review-gates`) |
| Review by a separate helper | Only for risky tasks (JS behaviour, accessibility, security) and once per batch. Sonnet, diff only, blockers only, ≤ 10 lines |

## Brief template

Paste, don't point. The helper reads nothing beyond this brief and the files it owns.

```text
## Goal
<one sentence; PLAN.md item ids>

## Owns
<files / regions it may change; nothing else>

## Snippets
<pasted excerpts it needs — tokens, rules from CLAUDE.md / design docs, the current
code to change. Aim ≤ ~3k tokens. No "read CLAUDE.md" / "read docs/…".>

## Gate
- While iterating: <fast gate, e.g. npm run gate:fast>
- Before each commit: <full gate, e.g. npm run gate>
- Never run raw test commands or paste logs; the gate scripts filter output.
- Prove "fails before" with the single test (name filter), never the full suite.
- Never `git stash`: every worktree shares one stash list. For "fails before":
  `git diff <file> > <scratch>.patch`, `git checkout <file>`, test, `git apply` it back.
- Cap any other output (`| head -c 4000`). Never print generated files (builds, lockfiles).
- No screenshots. Verify visuals by hash or computed values; the visual call is Sarah's.
- Commit on lane/<name> in your worktree. Never push, never merge.

## Report (≤ 15 lines)
Commits (hash + subject), git diff --stat, gate result, what's left, anything Sarah
must look at. No logs.
```

Pass `model: "sonnet"` (or `"haiku"` for purely mechanical edits).

## While it runs

- No `git stash` in your own tree either while a helper's worktree exists — a pop can
  take the helper's entry.
- A helper past ~150k tokens: `SendMessage` it to commit what's green, report, and stop.
  Re-brief the rest as a new, smaller lane — a fresh brief is cheaper than every further
  step at 150k+.

## After

- The completion notice shows the helper's tokens. Over ~60k → add a Lessons line with
  the cause (see `~/.claude/CLAUDE.md` § Where a lesson goes).
