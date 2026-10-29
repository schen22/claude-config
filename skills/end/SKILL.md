---
name: end
description: End a session — sort its lessons and save a one-line note for the retro.
disable-model-invocation: true
---

# End

On exit the `session-log` hook records the facts (commits, tokens, helpers, hook denies).
This adds the judgement.

1. What went wrong or cost too much: retractions, rework, blocked actions, Sarah's
   corrections. Helper costs: `python3 ~/.claude/hooks/session-log.py --helpers`.
2. Lessons: sort each with the ladder (`~/.claude/CLAUDE.md` § Where a lesson goes) and
   propose where it goes. Apply after Sarah agrees. Update the project `PLAN.md`.
3. Save the note, one short line each ("none" is fine):
   `python3 ~/.claude/hooks/session-log.py --note --goal "…" --wrong "…" --lessons "…"`
