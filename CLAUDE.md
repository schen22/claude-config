# Every project — Sarah's defaults

A project's own `CLAUDE.md` wins where it is more specific.

## How we work

- **Plan, then wait.** Before changing files: a plan table
  (`| Step | Files | Technique | Notes |`) plus open questions. Execute after Sarah confirms.
- Say what you're thinking and why. Don't assume — ask when a decision is Sarah's.
- **Verify before claiming.** Check current behaviour (build, run, read) before describing it.
- **Terse.** Tables, diffs, short bullets.
- **Hyperlink doc references.** Every mention of another doc, in files and in replies, is a
  Markdown link (to the section anchor when there is one).

## State

- One status file per project: `PLAN.md` — Now / Next / Later / Done, plus a dated,
  append-only Decisions log. Lessons live in the project `CLAUDE.md` under **Lessons**.
- New projects: scaffold this with the `working-model` skill. Existing projects keep
  their scheme unless Sarah asks to migrate.
- Local auto memory is keyed to one folder and never travels. Don't put workflow
  lessons there.
- The global setup (skills, hooks, plugins, decisions, who runs what) is tracked in
  `~/.claude/PLAN.md`. Read it before changing anything in `~/.claude`; update it after.

## Where a lesson goes (strongest first)

1. A committed script or test — works without anyone remembering.
2. A template that must be filled in (e.g. the `delegate` brief).
3. A step in a skill.
4. A line in a `CLAUDE.md`.

End of session: sort each new lesson. Project-specific → that project's Lessons.
Applies anywhere → this file or a skill in `~/.claude/skills/`. Prefer the highest rung
that fits.

## Subagents

- Default is inline. Load the `delegate` skill before any Agent call that starts an
  implementation or review helper — it decides inline vs helper, sizes the lane and
  gives the brief template.
- Cost ≈ context size × steps. Small briefs, few steps, filtered output.
- Models: `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` is the default. Pass `model` explicitly
  anyway; `haiku` only for mechanical edits with no judgment.
- Never two sessions editing one working tree. Helpers work in their own worktree.
- Sarah has uncommitted edits → make every edit in a separate worktree from the start
  (`git worktree add --detach <scratch> HEAD`), then cherry-pick. An edit left in her tree
  can end up in her next commit.

## Gates

- Every project exposes a fast check for iterating and a full check before commit, each
  printing ~5 lines. Convention: `npm run gate:fast` / `npm run gate` (or the stack's
  equivalent). If a project lacks them, propose adding them before delegating.
- No screenshots in helpers. Compare hashes or computed values; the visual call is Sarah's.

## Websites

- New site, header or theme toggle → the `web-kit` skill (`~/Documents/projects/web-kit`).
  Design or brand review → the `design-review` skill.

## Commits and reviews

- `commit` and `review-gates` skills hold the defaults. A project skill
  (`commit-workflow`, `review-workflow`) extends them with project checks and wins on conflict.

## Sharing and privacy

- A force-push leaves old commits reachable on GitHub by SHA. To purge personal data from a
  new repo, delete and recreate it (`gh auth refresh -s delete_repo`), then check the old SHA 404s.
- Build ffmpeg filter strings in Python, not zsh: `$5:c` in a zsh string is a modifier.
