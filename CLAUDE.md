# Every project — Sarah's defaults

A project's own `CLAUDE.md` wins where it is more specific.

## How we work

- **Plan, then wait.** Before changing files: a plan table
  (`| Step | Files | Technique | Notes |`) plus open questions, and what you think and why.
  Execute after Sarah confirms.
- **Verify, then argue.** Check current behaviour (build, run, read) before describing it. Before
  proposing a claim or a number, state what would refute it and what its arithmetic assumes.
- **Terse.** Tables, diffs, short bullets.
- **Hyperlink doc references.** Every mention of another doc, in files and in replies, is a
  Markdown link (to the section anchor when there is one). Never a bare ID: write the name first,
  the ID in parentheses, linked to its definition, e.g. [Repeated context (C2)](…#context).
- **YAGNI.** Build only what the project's size and stakes (`working-model`) and a named current
  need justify. Suggest scope changes; never make them unasked.

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

Project-specific → that project's Lessons; applies anywhere → this file or a skill. `/end` sorts them.

## Subagents

- Default is inline. Load the `delegate` skill before any Agent call that starts an
  implementation or review helper.
- Never two sessions editing one working tree: helpers work in their own worktree, and while Sarah
  has uncommitted edits so do you (`git worktree add --detach <scratch> HEAD`, then cherry-pick).

## Gates

- Every project exposes a fast check for iterating and a full check before commit, each
  printing ~5 lines. Convention: `npm run gate:fast` / `npm run gate` (or the stack's
  equivalent). If a project lacks them, propose adding them before delegating.

## Sharing and privacy

- A force-push leaves old commits reachable on GitHub by SHA. To purge personal data from a
  new repo, delete and recreate it (`gh auth refresh -s delete_repo`), then check the old SHA 404s.
