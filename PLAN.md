# Global Claude setup — plan

What's installed in `~/.claude`, how the pieces fit, who runs what, and why. Not loaded
automatically (costs nothing per session). Read it before changing anything in
`~/.claude`; update it after. The `retro` skill reads and updates it too.

Status sections are rewritten in place. **Decisions** and **Lessons** are append-only.

## Workflow

1. **Session start.** Loaded: `~/.claude/CLAUDE.md`, the project `CLAUDE.md`, skill and
   plugin descriptions. The `hook-review` hook stays silent until a review is due.
2. **Plan, then wait.** Plan table and open questions → Sarah confirms → execute.
3. **Delegate?** Load `delegate` → inline, or one fresh helper per task → fill in the
   brief template. `brief-check` checks the brief. `helper-guard` watches the helper
   (context budget, raw test runs, images). `usage-ledger` logs its cost when it stops.
4. **Before each commit.** `review-gates` + the project's `review-workflow` →
   `npm run gate` → `commit` + the project's `commit-workflow`.
5. **End of session.** Update the project `PLAN.md`. Sort each lesson with the ladder:
   project-specific → project `CLAUDE.md`; every project → `~/.claude` (+ a line here).
   `/revise-claude-md` can suggest candidates.
6. **Monthly.** `retro` → proposals → Sarah agrees → apply → update this file.

## What's in context

**Always loaded — every session and every subagent** (~4.0k tokens of ours; the rest of
the ~24–35k starting context is Claude Code's own system prompt and tools):

| Item | ~Tokens |
|---|---|
| `~/.claude/CLAUDE.md` | 730 |
| Descriptions of 10 user skills | 1,150 |
| Descriptions of 12 synced skills (`anthropic-skills:*`, from claude.ai) | 2,220 |
| Plugins: `claude-md-management` 177, `session-report` 72 | 250 |
| `research-round` plugin, once installed (10 agent + 1 skill + 1 workflow descriptions) | ~480 |
| Project `CLAUDE.md` (per project) | 800–1,300 |

**Loaded only when used:**

| Skill | ~Tokens | Job |
|---|---|---|
| `delegate` | 750 | Inline vs helper, brief template |
| `review-gates` | 470 | Gates 0–2, models |
| `commit` | 700 | Branches, one thing per commit, message shape, peer-session + clean-HEAD gate |
| `retro` | 430 (+ scan output) | Monthly review of the setup |
| `design-review` | ~700 | Read-only design + brand review of a site, findings table |
| `web-kit` | ~600 | New site from the starter; add/update header + theme toggle |
| `review` | 2,270 | Full engineering review (Gate 2) |
| `expert-review-panel` | 1,690 | Only when Sarah asks |
| `planning` | 2,920 | New project or feature spec |
| `working-model` | 1,880 | Right-size docs and oversight |
| `claude-md-improver` / `revise-claude-md` | 2,200 / 500 | CLAUDE.md audit / session learnings |
| `session-report` | 1,100 | Token usage report |
| `research-round` | ~970 skill + ~1,300 templates (read by its agents) | `/research-round <question>` → role reports + `PROPOSAL.md` |

**Runs outside context** (0 tokens unless it blocks or reminds):

| Hook | Event | Mode | What |
|---|---|---|---|
| `brief-check.py` | PreToolUse `Agent` | enforce | Helper brief follows the `delegate` template; opus/fable needs a reason |
| `helper-guard.py` | PreToolUse Bash/Read/Edit/Write/NotebookEdit, subagents only | enforce | 150k budget → wrap up; raw test runs → gate; no images |
| `usage-ledger.py` | SubagentStop | always on | One row per helper in `logs/agents.jsonl` |
| `research-round` `write-scope.py` | PreToolUse Write/Edit, `research-round:*` agents only | enforce | Role → its `references/<slug>-<role>.md`; fact-checker → `references/*.md`; synthesizer → `PROPOSAL.md` |
| `hook-review.py` | SessionStart | always on | From the date in `hooks/REVIEW_DUE`, asks for the hook review each session until done |

Settings: `CLAUDE_CODE_SUBAGENT_MODEL=sonnet`. Tests: `python3 hooks/test_hooks.py`.
Logs: `logs/hooks.jsonl`, `logs/agents.jsonl`. Backups: `backups/`.

## Who does what

| Task | Sarah | Claude | When |
|---|---|---|---|
| Approve plans, commits, deletions, installs | Decides | Proposes | Always |
| Retro | Asks for it, approves | Runs `retro`, proposes, applies, updates this file | Monthly |
| End-of-session lessons | Approves | Sorts with the ladder | Every session |
| After editing a hook | — | Runs `test_hooks.py` | On change |
| Plugins | Decides | Checks cost with `claude plugin details` | As needed |
| Visual sign-off | Decides | Points at the pages | Every visual change |
| Push the `~/.claude` repo (once it exists) | Pushes | Commits | — |

## Now

- First retro **2026-10-28**. Known candidates from the first scan:
  - walmart `prioritization-working-style` (feedback memory) → `~/.claude/CLAUDE.md`?
  - walmart `working-model-changes` → already in `delegate` / `review-gates`; delete.
  - Weigh each rule added to `CLAUDE.md` / skills: cost (tokens, time, friction) vs. risk.
    Demote heavy, low-priority checks or drop them (e.g. the every-image check, removed 2026-09-30).

## Next

- **research-round: run the workflow path once.** The 2026-10-10 trial ran the skill
  fallback (no Workflow tool in `claude -p`). Run `/research-round` in an interactive session
  that has workflows, and check that `write-scope` and `usage-ledger` see workflow agents.
- **research-round cost:** the orchestrating session ran on Opus and used ~1.37M of the ~2.79M
  tokens processed. Decide: start rounds from a Sonnet session, or pin the skill's model.
- **Install research-round** (after committing `settings.json`):
  `claude plugin marketplace add ~/.claude` → `claude plugin install research-round@sarah-config`.

- **Adopt web-kit** — tasks written into each project's CLAUDE.md; Sarah starts a session
  there: shindig-thingamajig (required), schen22.github.io (required; confirm its purpose
  first), sarahs-corner (optional, later).


## Later

- **research-round in Cowork:** install the plugin from `schen22/claude-config` (private: needs
  GitHub access from Cowork), run one small round, confirm skills + agents load and whether
  the workflow runs, else the skill fallback.
- **hookify:** only if many simple text rules are wanted.

## Done

- 2026-10-10 · `research-round` plugin 0.1.0 (`marketplace/research-round/`; the repo root is
  the `sarah-config` marketplace): 7 role agents (product-designer, ux-researcher,
  market-researcher, ranking-engineer, architect, data-scientist, data-engineer), fact-checker,
  overseer, synthesizer (Opus); `report-template.md`, `checklist.md`, `proposal-template.md`;
  workflow `research-round.js`; skill `/research-round` (calls the workflow, else runs the same
  phases through the Agent tool); `write-scope` hook + 14 tests. Trial in food-planner
  ("How should SC4 be measured?", 3 roles, skill fallback): **11 agents, 535 s, ~$3.61 list**;
  subagents 856k tokens processed (synthesis 151k), main session ~1.37M (Opus); ~2.79M across all models; 3 reports
  fact-checked (14 corrected, ~10 unverified), all 3 failed the checklist once and were fixed;
  docs check passed; only the 4 round files written. PushNotification skipped (Remote Control off).
- 2026-09-30 · `commit` skill: peer-session check before staging; `gate-head.sh` runs
  the gate on a clean checkout of HEAD (`commit` ~480 → ~700 tokens, chars÷4).
- 2026-09-28 · `~/.claude` is a git repo (allowlist `.gitignore`: setup files only), pushed
  to `schen22/claude-config` (private). web-kit pushed to `schen22/web-kit` (private).
  Convert to a plugin only for a second machine, cloud sessions or sharing.
- 2026-09-28 · `design-review` skill, built from the sarahs-corner design and brand reviews.
- 2026-09-28 · web-kit 0.1.0 (`~/Documents/projects/web-kit`, local repo): header, theme
  toggle, `--wk-*` token contract, starter site, copy-in script, contract tests (8) and a
  browser check (10). `web-kit` skill covers new site / add / update.
- 2026-09-28 · shindig's broken project copy of `review` removed (backup kept); its
  `code-reviewer` now uses the user-level `review` + `.claude/review-bindings.md`.

## Decisions

- 2026-09-28 · Lesson ladder, strongest first: script/test/hook → template → skill step
  → CLAUDE.md line. Workflow lessons never go in local auto memory.
- 2026-09-28 · `~/.claude/CLAUDE.md` holds rules for every project; this file tracks
  the setup and is not auto-loaded.
- 2026-09-28 · Subagents default to Sonnet (env var); Haiku only for mechanical edits;
  Opus/Fable helpers need a stated reason.
- 2026-09-28 · One fresh helper per task (1–2 items), run in sequence. Orchestrator
  reviews each diff inline; a reviewer helper only for risky tasks and once per batch.
  From lane H (5 items → 202k peak, 15.4M tokens) and a comparison with superpowers.
- 2026-09-28 · Every project exposes `npm run gate` / `gate:fast` (~5 lines of output).
- 2026-09-28 · Generic `commit` / `review-gates` at user level; project skills extend them.
- 2026-09-28 · Hooks start log-only, fail open, log every decision; enforce after review.
- 2026-09-28 · Plugins installed: `claude-md-management`, `session-report`. Skipped:
  superpowers (reviewer per task, ~800 tokens injected every session), `code-review`
  (built-in `/code-review` exists), `skill-creator` (duplicate of the synced one),
  `github` (`gh` covers it), hookify (for now).
- 2026-09-28 · Removed 4 unused agents and the older `interview-prep` copy
  (`backups/removed-2026-09-28/`).
- 2026-09-28 · Git repo before plugin. New projects use `PLAN.md`; shindig keeps its scheme.
- 2026-09-28 · web-kit: neutral `--wk-*` tokens each site maps once (no renames); files
  copied in with a version stamp, never installed as a dependency; toggle uses a fixed
  label + `aria-pressed`; one `web-kit` skill instead of a separate `new-site` skill.
- 2026-09-30 · Dropped the every-image / GIF-frame / EXIF check from `~/.claude/CLAUDE.md`
  § Sharing and privacy: too heavy for routine sharing (Sarah). Force-push and ffmpeg bullets
  kept. The phone-number lesson below stays as history.

- 2026-10-07 · Hook trial reviewed (48 decisions, 2026-09-28 → 10-05): `brief-check` and
  `helper-guard` switched to enforce, unchanged. 24 image/screenshot and 19 incomplete-brief
  calls would have been denied.

- 2026-10-10 · research-round: up to 3 roles per round by default (≤ 3 × roles + 2 = 11 agents),
  4+ only when Sarah names them; every report always gets its own fact-checker; one fix pass,
  failing reports only. Opus only for synthesis (cross-role judgement). Agents may write only
  their own file, enforced by the plugin's `write-scope` hook. The plugin lives in claude-config
  so Cowork can install it; trial with `--plugin-dir` so `settings.json` isn't touched.
- 2026-10-10 · Hook visibility (trial): PreToolUse events from plugin subagents carry
  `agent_id` + `agent_type` (`research-round:<name>`), so `helper-guard` and `write-scope` act
  on them; `usage-ledger` logged all 11. `brief-check` skips named agent types by design.
  Workflow agents untested.

## Lessons

- Lessons saved in local memory or a session scratchpad never reach the next session
  (the walmart memory, `gate0.sh`).
- A rule in a skill only works if the skill is loaded when the decision is made. Rules
  that matter get a hook.
- `CLAUDE.md` loads at launch; running sessions must be told to re-read it. Skills,
  settings and hooks reload live.
- Helper cost ≈ context size × steps; a helper starts at ~25–35k before reading anything.
- WebFetch summaries can be wrong on specifics (it said `Agent` calls can't be matched by
  a hook). Check the raw doc.
- `git stash` in a repo with live-reloaded skills briefly swaps which skills are loaded.
- Keep process work and project work in separate sessions: the process session edits only
  `~/.claude`, the project session owns the repo. Global skill and hook edits reach running
  sessions immediately, so batch them and tell the project session when one lands.
- Static checks missed a real layout bug (header overflowed at 375px on a site without a
  `box-sizing` reset); the browser check caught it. Component work needs a browser check.
- The common reduced-motion reset (`transition-duration: 0.01ms !important` on `*`) makes
  every property transition for 0.01ms — measure layout a frame after a resize.
- A project skill with the same name as a user skill silently overrides it (shindig's
  stale `review`). Project skills extend under a different name.
- Two sessions edited one working tree (ai-deep-dive, 2026-09-30): files changed under a
  commit being planned. `commit` now checks `git status` + `ListAgents` before staging.
- A gate check tightened in one commit failed data that only landed in a later one.
  `commit` now gates each partial-tree commit on a clean checkout (`gate-head.sh`).
- An edit left in Sarah's dirty working tree got swept into her next commit (ai-deep-dive
  `d211c8f`, 2026-09-30). `~/.claude/CLAUDE.md` § Subagents: with her edits uncommitted, edit
  in a separate worktree from the start, then cherry-pick.
- A phone number sat in frames 30–47 of a GIF that Read previewed as frame 1 only (ai-deep-dive,
  2026-09-30). `~/.claude/CLAUDE.md` § Sharing and privacy: check every image and GIF frame plus
  metadata before sharing; delete + recreate a repo to purge history.
- `git stash` is one list for every worktree: the orchestrator's pop took a helper's stashed
  CSS edit (sarahs-corner, 2026-10-03). `delegate` brief Gate + "While it runs": no stash;
  use `git diff > patch` / `git checkout` / `git apply`.
- `claude -p` has no Workflow tool, so a workflow can't be trial-run headless. The skill
  fallback ran instead. Ship every workflow with a fallback path the skill can run.
