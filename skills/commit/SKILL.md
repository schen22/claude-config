---
name: commit
description: >-
  Default commit rules for any of Sarah's projects — branches, one-thing-per-commit,
  message shape. Use whenever about to commit. If the project has its own
  commit-workflow skill, follow that too; it wins on conflict.
---

# Commit

## Branches

- Orchestrator (the session Sarah talks to) commits on the project's working branch.
  Never push; pushing is Sarah's call.
- Helpers commit only on `lane/<name>` in their own worktree. Never touch the working
  branch, never merge, never push.
- Integrate a lane: `git rebase <main> lane/<name>` then `git merge --ff-only lane/<name>`.
- After the full gate passes on the working branch, clean up the lane in the same step:
  `git worktree remove <path>` and `git branch -d lane/<name>` (plus any
  `worktree-agent-*` branch). A leftover lane is easy to mistake for unfinished work.
- `git log --oneline -5` before the first commit — never assume repo state.
- Before staging: `git status` and `ListAgents`. If a peer session is busy in the same
  working tree (files change under you), stop and ask Sarah: wait for it to commit, or
  move it to its own worktree. Never commit around its half-done edits.

## One commit does one thing

- One commit per `PLAN.md` item (or one clearly named part of one).
- A test ships in the same commit as the change it proves.
- Shared docs (`PLAN.md`, `CLAUDE.md`, `README.md`, `docs/`) are orchestrator-only.
  Helpers list doc-worthy facts in their report instead.
- Docs go in their own commit, after the code they describe.
- Each commit passes the full gate on its own. After committing a partial working tree,
  run `~/.claude/skills/commit/gate-head.sh` (gate on a clean checkout of HEAD). A check
  tightened in one commit can fail data that only lands in a later one — order commits so
  each passes.
- Plan the commit stack before the first commit. > ~6 commits → split across helpers or
  sessions (see `delegate`).

## Message shape

Match the repo's existing style. Default: imperative subject, sentence case, ≤ 60 chars,
no "and" (two things → two commits).

```text
<Imperative subject>

<Why: PLAN item / review IDs and any non-obvious reasoning. Don't restate the diff.>

Verified: <full gate result>; <build/inspection done>. New test <name> fails before,
passes after.
Review: <SHIP|BLOCKED> — <one clause per finding and how it was handled>.

<Co-Authored-By trailer from the session's attribution instructions>
```

## Checklist

```text
[ ] right branch; nothing pushed; no peer session busy in this tree
[ ] partial tree committed → gate-head.sh passed
[ ] one item per commit; its test in the same commit
[ ] helpers: no shared-doc edits
[ ] subject imperative, <= 60 chars, no "and"
[ ] Verified + Review lines; full gate passed
```
