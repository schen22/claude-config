---
name: working-model
description: Right-size the working model — the doc surface, oversight cadence, scope unit, and decision-capture style — to a project's current size, phase and stakes, and re-tune it as the project scales. Use when planning a new project or feature; before creating any new .md file; at a stage or milestone boundary to run the audit; and whenever the user says "restructure the docs", "too many files", "this is over-documented", "the codebase grew too fast", "this milestone feels big", "split this", "merge these docs", or asks how much to review versus let the agent execute. Guards against .md sprawl, sudden codebase growth, untracked decisions, and mis-sized scope.
---

# Working model

The **working model** is four dials, not one:

1. **Doc surface** — how many files, each file's single job, append vs. rewrite.
2. **Oversight cadence** — review per commit / per stage / per PR; inline vs. subagent.
3. **Scope unit** — how large a chunk the agent takes before checking in.
4. **Decision capture** — what gets recorded, where, how heavy.

The failure this skill prevents: the working model is set once at the start and
never re-tuned, so a small project accretes the doc apparatus of a large one, the
codebase grows past its milestone, and decisions scatter. Re-tune the dials to
the project's **size and phase** — re-check at every milestone boundary.

Vocabulary here is generic. "The state file" = whatever the project uses to track
where it is. "The decisions log" = the architecture-decision record, if the
project keeps one. "The commit-count estimate" = any running `[n of x]` or
similar gauge of how big the current chunk is.

## When to run

- **Session startup** — classify the archetype (below); state it in one line.
- **Before creating any new `.md` file** — check the doc budget first; a new file
  must clear the bar in "Doc budget".
- **At a stage / milestone boundary** — run the Audit, after the state file is updated.
- **On request** — "restructure the docs", "too many files", "over-documented",
  "this feels big", "split this", "merge these", "how much should I review".

## Archetype

Pick the row that matches the project **today**. Re-classify at each milestone.
Crossing a boundary is itself a trigger (see the trigger list).

| Dial | Small / short-cycle | Growing codebase | Large-scoped |
|---|---|---|---|
| **Docs** | One running plan file; a README if someone else runs it. No standalone architecture or decisions docs — architecture is a few bullets in the plan file. | "One job per file" set (state / architecture / decisions / readme), each capped ~150–300 lines, and no more. | Hierarchical: a top-level index → per-area docs → one file per decision record. |
| **Oversight** | Steer direction; review at the end or 1–2 checkpoints. Tests are the safety net. | Subagent review per meaningful change (staged diff only) + a heavier review at milestone boundaries. Not per-commit inline. | Agent executes inside a pre-fenced area; humans review at PR boundaries. |
| **Scope unit** | The whole task fits one context window. If it doesn't, it's not small — use the next column. | A named milestone, roughly 6 commits. Estimate drift is the alarm. | A bounded task, decomposed by a human before the agent starts. |
| **Decisions** | Inline comments + one-liners under a "Decisions" heading in the plan file. | Recorded only if the choice moves a boundary, semantics, persistence, concurrency, security, or extensibility. Everything else is not recorded. | Numbered decision-record process, each owned. |

Most projects are "growing". The common mistake is applying the growing (or
large) row's doc instincts to a small / short-cycle project.

## Stakes

Separate from size: how much rigour the plan gets. If unsure, ask once.

- **Quick** — a script, a prototype, one feature on a known codebase: plan in a short conversation.
- **Standard** — a new app, a nontrivial feature, anything shared with others: a full plan with
  blind spots checked.
- **High-stakes** — money, auth, PII, health data, customer-facing, or "the real thing": extra rigour
  on security, the data model and risks; name open risks in `CLAUDE.md` rather than picking
  silent defaults.

## Concision & simplicity — the default posture

Applies to every edit this skill makes or reviews:

- **Simplify the approach before documenting it.** If a design needs a paragraph
  to justify, first try to make the design smaller.
- **Every doc edit should remove at least as much as it adds** where the content
  allows. A net-additive edit needs a reason.
- **Redundancy across files is a defect, not thoroughness.** The same fact in two
  docs is one fact to keep and one to delete-and-link.
- **Prefer** deleting to adding, a section to a file, a link to a copy.
- **No new abstraction — code or doc — without a nameable current requirement.**
  "We'll need it later" is not one.

## Doc budget

The project's `CLAUDE.md` (or equivalent) states the number of root docs and each
one's one-line job. Before adding doc N+1: propose retiring or splitting an
existing one instead, and get agreement.

Ledgers append (the decisions log, a retro log). Everything else is rewritten in
place — never append a "update" section to a doc whose body is now stale.

## Audit

Run at each stage / milestone boundary, after the state file is updated. One line
of output per check — either `OK` or the fixed response to apply.

1. **Archetype** — still the right row? If it changed, adopt the new row's doc
   surface and oversight cadence.
2. **Doc size** — any file past its cap, or holding content outside its one-line job?
3. **Resume cost** — would a cold read of the docs exceed ~5k tokens? Any two
   docs stating the same thing?
4. **Triggers** — did any row in the trigger list fire this milestone?
5. **Abstractions** — anything added (code or doc) with no current consumer?

Anything beyond a one-line in-place fix opens a restructure proposal (below) —
the Audit does not itself edit.

## Triggers → fixed response

| Trigger | Fixed response |
|---|---|
| A doc's content has drifted from its one-line job | De-overlap the doc set (restructure proposal) |
| Cold resume reads > ~5k tokens of docs, or docs repeat each other | Prune / merge (restructure proposal) |
| The commit-count estimate drifts upward mid-milestone | Split into named sub-milestones; a fresh session for each; the state file carries the baton |
| You're reviewing every commit and it's slowing the work | Move oversight to milestone boundaries; per-change review becomes a subagent on the staged diff |
| A review was skipped and a real bug shipped | Oversight back up one level, or fix task sizing if the tasks were too big to review |
| More than one agent / instance is working the same tree | Each in its own worktree + branch; shared-doc edits deferred to scratchpad notes; one integrator applies them |
| An abstraction exists with no nameable current requirement | Revert it |
| The project crossed an archetype boundary | Adopt the next archetype's doc surface and oversight cadence |

## Restructuring `.md` files — proposal first, always

1. When the Audit flags anything beyond a trivial one-line fix, write a short
   **restructure proposal**: what merges into what (or is split, or deleted),
   why, which references get repointed, and the resulting doc budget. Touch no
   files yet.
2. Present it and get an explicit green light. If the user wants changes, revise
   the proposal — still no edits.
3. On approval, execute with **minimal edits**: move sections verbatim, don't
   rewrite prose that's already aligned; delete emptied files; repoint every
   reference in one pass; update the doc budget. One restructure = one docs-only
   commit.
4. Restructure at milestone boundaries only, never mid-stage.

## Do not

- Restructure docs autonomously — always propose first.
- Turn this skill into tooling: a doc-count linter, an archetype detector. It is
  a checklist a person runs.
- Rewrite aligned content to "improve" it.
