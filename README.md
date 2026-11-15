# claude-config

My Claude Code setup: the rules, skills, hooks and one plugin I use on every project I build
with AI. It's published so others can copy what works. The projects built with it are listed on
[my GitHub profile](https://github.com/schen22).

## The loop

1. **Start.** `/start` shows the last session here, this session's goal, and what's due.
2. **Plan, then wait.** Claude proposes a plan table (step, files, lane, technique) and open
   questions. Nothing changes until I confirm.
3. **Delegate or not.** [`delegate`](skills/delegate/SKILL.md) decides whether to work inline or
   start a helper, and gives each helper a fixed brief (goal, files owned, gate, report).
   A hook keeps helpers within budget.
4. **Before each commit.** [`review-gates`](skills/review-gates/SKILL.md) picks the review,
   the project gate runs (`npm run gate`), then [`commit`](skills/commit/SKILL.md) sets the
   branch and message rules.
5. **End.** `/end` sorts the session's lessons onto a ladder (strongest first: script or test ›
   template › skill step › `CLAUDE.md` line) and saves a note.
6. **Monthly.** [`retro`](skills/retro/SKILL.md) reads the session and helper logs and proposes
   fixes to the setup itself.

The rules behind it are in [`CLAUDE.md`](CLAUDE.md).

## What's here

| Path | What |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Global rules: plan then wait, verify then argue, YAGNI, gates, privacy |
| [`skills/`](skills/) | `start`, `end`, `delegate`, `review-gates`, `review`, `commit`, `retro`, `working-model`, `design-review`, `web-kit` |
| [`hooks/`](hooks/) | `helper-guard` (helper budget, no raw test runs), `usage-ledger` (cost per helper), `session-log` (one row per session), `due` (reminds when a retro is due). Tests: `python3 hooks/test_hooks.py` |
| [`marketplace/research-round/`](marketplace/research-round/README.md) | Plugin: `/research-round <question>` runs up to 3 role agents in parallel, then fact-checkers, an overseer and a synthesis |
| [`git-hooks/`](git-hooks/) | Global git hooks for every repo (`core.hooksPath`): `pre-commit` blocks secrets (gitleaks); `pre-push` blocks private terms and secrets (diffs and commit messages) in pushes to **public** repos, and publishes this repo when `~/.claude` is pushed. Tests: `python3 git-hooks/test_git_hooks.py` |
| [`settings.json`](settings.json) | Hook wiring and subagent model |

## Use it

- **Plugin:** `/plugin marketplace add schen22/claude-config`, then
  `/plugin install research-round@sarah-config`.
- **Git hooks:** `git config --global core.hooksPath ~/.claude/git-hooks` (needs `gitleaks`;
  `pre-push` reads its terms from `~/.claude/scripts/private-terms.txt`, one regex per line).
- **Skills and hooks:** copy the folders you want into `~/.claude/` and merge the `hooks` block
  from `settings.json`. The skills mention me ("Sarah") by name; change that to your own name.

## How this repo is made

`~/.claude` is a private repo. Its runtime state (transcripts, history, logs) is never committed.
[`scripts/export_public.py`](scripts/export_public.py) copies the committed setup here, without
`PLAN.md` (my private decision log) and without local-only settings. It refuses to export if it
finds private terms, or if this README misses a skill, hook or plugin.

Pushing `~/.claude` publishes this repo automatically: the global `pre-push` runs the export,
commits any change here (the message lists files only) and pushes it. If the export or that push
fails, the private push is blocked too, so the two never drift. To change anything, edit
`~/.claude`; edits made directly in this repo are overwritten by the next export.
