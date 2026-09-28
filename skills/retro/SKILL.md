---
name: retro
description: >-
  Monthly or end-of-milestone review of Sarah's Claude setup across all projects —
  repeated prompts, lessons stuck in one folder's memory, what the hooks blocked, the
  costliest helpers — ending in proposals for where each fix belongs. Use on "retro",
  "what am I repeating", "review my setup", "why is this expensive", or when
  ~/.claude/PLAN.md says a retro is due.
---

# Retro

Plan, then wait: this skill proposes. Nothing changes until Sarah agrees.

## Steps

1. `python3 ~/.claude/skills/retro/scan.py` (add `--days N` to change the window).
2. For token usage by project, session and skill, run the `session-report` skill's analyzer
   in JSON mode and read only `overall`, `by_project` and `by_subagent_type`. Build the
   HTML report only if Sarah asks for it.
3. Read `~/.claude/PLAN.md` (inventory, Now/Next, Decisions) so proposals don't repeat
   something already decided.

## Report (≤ 30 lines)

| Finding | Evidence | Proposed fix | Rung |
|---|---|---|---|

Rungs, strongest first (from `~/.claude/CLAUDE.md`): 1 script/test/hook · 2 template ·
3 skill step · 4 CLAUDE.md line. Pick the strongest that fits.

- A repeated phrase across projects → a line in `~/.claude/CLAUDE.md` or a skill.
- A local memory holding a workflow lesson → move it up, then delete the memory.
- A hook's would-deny that was right → propose enforce. One that was wrong → fix the rule.
- A costly helper → name the cause (items per helper, pointer brief, unfiltered output).

## After Sarah agrees

Apply the changes, then update `~/.claude/PLAN.md`: inventory, status, a dated Decisions
line and a Lessons line where something was learned. Set the next retro date in Now.
