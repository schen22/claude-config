---
name: review
description: End-to-end product engineering review of a change — correctness, scope, structure, coupling, state, accessibility, UX, security and privacy — routed by what actually changed, verified against build and tests, ending in a SHIP/BLOCKED verdict. Use on "review this", "review my changes", "code review", "is this ready to ship", "review before merge", "check this diff", "deep review", "review and fix". Self-contained: runs on local tools only.
---

# Review

> **Core Question:** Does this change do what was asked, without breaking anything, and can every finding be proven?
> **Rule:** Evidence, not inference. Cheapest signal first. Anything a machine can decide belongs in CI, not here.

**Two rules govern everything below.**

1. **Evidence, not inference.** Report a finding only once confirmed — code re-read in context, the call site traced, or the behaviour observed. A self-report is not evidence; "looks fine" is not evidence.
2. **Mechanical checks belong to CI.** Regex scanning, file-extension rules, EXIF validation, lint, and conformance assertions run in the pre-commit hook or the pipeline, triggered on the diff. This skill reads their exit code and never re-runs them by hand. A mechanical defect that slipped through is fixed with **a new check in CI**, not a new rule here.

## Modes

| Invocation | Behaviour |
| :--- | :--- |
| `/review` | Routed, scoped to changed files. The default. |
| `/review deep` | Every lens, whole-feature scope, ignores routing. Adds `ux` and screenshots. |
| `/review --fix` | Review, apply findings, re-run phase 3, discharge regression obligations. |
| `/review --since=<ref>` | Review `<ref>...HEAD` instead of the working tree. |
| `/review --lens=coupling,state` | Force specific lenses regardless of routing. |

---

## Phase 1 — Route

1. **Get the diff.** Working tree by default (`git diff HEAD` plus untracked); `<ref>...HEAD` with `--since`. Clean tree and no ref → review the last commit and say so.
2. **State the ask in one sentence**, from the task or spec, never from the diff. If it can't be stated, say so — the scope was never defined, and `structure` part 1 becomes the primary lens.
3. **Load bindings** (below). They outrank every default in these lenses.
4. **Select lenses and announce the route**, e.g. `Route: core + coupling, state · runtime: build + tests`.

**Work up the cost ladder, and stop as soon as the answer is decided.** A Blocker in the first two steps short-circuits the review — spending a full pass on code that cannot ship is how a review wastes its budget.

| # | Step | Always? |
| :--- | :--- | :--- |
| 1 | Build + test suite + CI gate — exit codes | yes |
| 2 | `security-privacy` Gate 2 — diff fast-scan | yes |
| 3 | Core: `correctness` · `structure` | yes — `correctness` skipped on docs-only |
| 4 | Routed extras, from the table below | by file kind |
| 5 | `ux` + screenshots | `deep` only |

`structure` part 1 is the scope check — does this earn its place, is it inside its ownership, does it add new surface. Part 2 is the shape check. Together they make step 3 the whole of what most reviews need.

| What changed | Adds | Phase 3 |
| :--- | :--- | :--- |
| Docs, comments, README | — *(`structure` part 1 only)* | no |
| Config, build files, lockfiles | — *(new surface and new deps are `structure` part 1 hard stops)* | build |
| Logic / data-layer code | coupling · state | build + tests |
| CSS / styles | accessibility *(contrast, focus)* | build + tests |
| Client-side JS | state | build + tests + console |
| Markup, templates, components | accessibility | build + tests + console |
| Data, schema, content | coupling *(hand-agreement pairs)* | build + tests |
| Data rendering, embeds, redirects, headers | security-privacy **Gate 3** | build + tests |

**Gate 3 is diff-triggered, not mode-triggered** — it runs whenever the diff touches those surfaces, in `/review` as much as in `deep`, and stays unloaded otherwise. If a project has no CI gate at all, say `no Gate 1 configured` once in the report rather than substituting greps for it.

Load only the selected files from `references/`. They are lazy by design — the library growing must never make a single review heavier.

---

## Phase 2 — Read

Each selected lens produces **candidates**, not findings. Every candidate carries, or it is dropped in phase 4:

- `file:line` · **what** is wrong in one sentence · **the rule** it breaks, named from the lens · **the concrete failure** — inputs or conditions producing a wrong result · **the fix**, specific enough to apply.

If you cannot describe the failure, you have a preference. Search before concluding: a "duplicate" with an existing shared helper, or a "missing" guard that lives one layer up, costs more trust than the finding was worth.

---

## Phase 3 — Run

Skip only if routing says no. Protocol is `references/runtime.md`: run the build and suite, read exit codes, load only what the diff can reach and check the console, take the built-size delta, enumerate edge cases. Screenshots are `deep`-only.

The runtime half of `accessibility` runs here, on the artifacts, as does `ux` in `deep`.

**If the project cannot be built**, report `RUNTIME: NOT RUNNABLE — <reason>` and mark every runtime claim unverified. An absent build never reads as a pass.

---

## Phase 4 — Confirm and report

**Confirm.** Try to disprove each candidate — re-read the surrounding code, trace callers, check for a guard elsewhere, run the case.

- Confirmed → report.
- Unconfirmed and cheap to check → say what to check, as a Question.
- Unconfirmed and expensive to check → **drop it.** Never downgrade to "possible issue"; a review that is half noise gets read once.
- Confirmed but spec-mandated → not a finding. Escalate as a Question.
- **One defect, one finding.** Where two lenses catch the same thing, report it once under the more specific rule.

**Severity.**

| Sev | Meaning | Examples |
| :--- | :--- | :--- |
| **Blocker** | Do not ship | Broken build, test, or CI gate · a route or error state that fails · secret, key, or PII published · injection surface · a duplicated source of truth that can drift · ownership or frozen-file violation · accessibility failure that locks someone out |
| **Major** | Fix before merge | Budget exceeded · function doing two jobs · scattered concept needing colocation · unrequested new surface · state with two sources |
| **Minor** | Fix or file | Naming, nesting, local duplication, ordering |
| **Question** | Needs a human | Spec conflict, UX judgment, an unconfirmed candidate worth checking |

**Verdict.** One line: `SHIP` or `BLOCKED — N blockers`. No hedging, and no verdict at all if phase 3 was required but not runnable.

**Regression obligation.** Every Blocker and every newly found edge case owes a test that **fails before the fix and passes after**. In `--fix` mode, write it and watch it fail before fixing. Reviewing someone else's worktree, record it as owed by the file's owner. If it genuinely cannot be automated, name it on a manual checklist with the reason — never silently dropped. A defect found twice means the first review failed.

**Output.**

```
Route: <lenses> · runtime: <what ran>
Ask: <one sentence>

| Sev | File:line | Finding | Rule | Fix |

Runtime: <exit codes, console, or NOT RUNNABLE>
Perf delta: +N KB built   (vs <base>)
Obligations: <n> — <list>

SHIP | BLOCKED — N blockers
```

**`--fix`:** apply in severity order, write owed tests first, re-run phase 3, re-report. Never fix outside the change's ownership — report it instead.

---

## What is not a finding

Anything the spec requires (disagreement is a Question, never an edit) · a preference with no failure case · duplication between things that change for different reasons · style the codebase already committed to · a missing feature nobody asked for.

---

## Project bindings

Per-project rules live **in the project**, so this skill stays portable. At phase 1, load the first that exists: `.claude/review-bindings.md` → `AGENTS.md` / `CLAUDE.md` / `CONTRIBUTING.md` → none, in which case say `bindings: none — using defaults`.

**Bindings outrank every default here.** If a binding and a lens disagree, the binding wins and no finding is raised. If a binding and the project's spec disagree, report the contradiction rather than picking one.

| Binding | Used by |
| :--- | :--- |
| Spec file and precedence | phase 1, "what is not a finding" |
| Ownership and frozen files | `structure` part 1 — violations are Blockers |
| Build, test, serve commands · where the CI gate lives | phase 3 |
| Single-source-of-truth locations | coupling, structure |
| Hand-agreement pairs | coupling |
| Publish surface — dirs copied verbatim to production | security-privacy |
| Budget overrides | structure part 2 |
| Branch and push policy | `--fix` |

**Absent bindings, assume:** never push, never edit a file the change didn't already touch without saying so, treat any directory served verbatim as published, and report missing dependencies rather than installing them.
