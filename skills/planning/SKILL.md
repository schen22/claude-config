---
name: planning
description: Use this skill whenever the user wants to plan a new project, feature, or app before building it — including requests like "let's plan out X", "help me spec this", "I want to build a...", "let's figure out requirements for...", or any time meaningful implementation work is about to start without an aligned spec. Also use it to create or update a CLAUDE.md (or AGENTS.md / project instructions file) so that a coding agent can execute the plan correctly. Trigger even if the user jumps straight to "just build it" — pause and run this skill first unless the user explicitly says to skip planning or the ask is trivial (a one-file script, a small bugfix, a copy tweak). Do NOT use this skill for pure research questions, debugging existing code, or small isolated tasks that don't warrant a written spec.
---

# Planning

A skill for turning a rough idea into an aligned, written spec — then encoding that spec into a `CLAUDE.md` (or equivalent project-instructions file) so any LLM executing the work later builds the *right* thing, not just *a* thing.

The core failure mode this skill prevents: an agent starts coding based on assumptions, builds something technically correct but misaligned with what the user actually wanted, and the user only discovers the mismatch after a lot of wasted work. Planning up front is cheap. Rework is not.

## Philosophy

- **Interview, don't interrogate.** This is a conversation, not a form. Ask a few sharp questions, listen, follow up, then move on. Never fire off 20 questions at once.
- **Ask non-obvious questions.** Surface-level questions get surface-level answers that don't actually reduce risk. Prefer questions that expose assumptions, failure modes, and hidden scope.
- **Default to asking, but don't stall.** If the user is vague or says "you decide," make a reasonable default explicit, flag it as an assumption, and move on — don't block on every unanswered question.
- **Match effort to stakes.** A weekend hobby script doesn't need the full five-phase treatment. A multi-user product, anything touching money/auth/user data, or anything the user calls "production" does. Ask the user (or infer from context) how deep to go — see "Calibrating depth" below.
- **The output is a living document.** The point isn't a one-time interview — it's a `CLAUDE.md` that stays accurate as understanding evolves. Update it when plans change, don't let it rot.

## Calibrating depth

Before diving in, form a quick judgment (and optionally confirm with the user) on scope:

- **Quick** (a script, a prototype, a single feature on an existing well-understood codebase): compress phases 0–4 into a short conversation, skip the blind-spot checklist except where obviously relevant, produce a short `CLAUDE.md`.
- **Standard** (a new app, a nontrivial feature, anything shared with other people): go through all five phases below, use the blind-spot checklist, produce a full `CLAUDE.md`.
- **High-stakes** (handles money, auth, PII, health data, is customer-facing, or the user signals this is "the real thing"): go through all five phases with extra rigor on phase 1 (security, data model, compliance) and phase 3 (risk/dependencies), and explicitly call out open risks in the `CLAUDE.md` rather than silently picking defaults.

If unsure, ask once, briefly — don't build an elaborate calibration ritual.

## The five phases

Work through these roughly in order, but loop back when new information changes earlier answers (e.g., a tradeoff surfaced in phase 3 might reopen a requirement from phase 0). Don't present all five as a rigid checklist to the user — weave them into natural conversation.

### Phase 0 — Requirements: what and why

Get alignment on the problem before any solution talk.

- Who is the audience? (Be specific: not "users" but "solo freelancers doing their own taxes" vs "enterprise finance teams.")
- What problem does this solve, concretely? What do people do today without this?
- What does success look like — for the user, and in 6 months from now?
- Must-haves vs. nice-to-haves. Push for a real cut line, not "everything is important."
- What's explicitly out of scope?

Good follow-ups:
- "What's the most annoying thing about current solutions?"
- "Which user would get the MOST value from this, and which would get the LEAST?"
- "What's the smallest version of this that would still be useful?"
- "How will you know if this is successful in 6 months?"
- "What would make you delete this / stop using this after a week?"

### Phase 1 — Implementation: architecture alignment

Once the *what* is clear, align on the *how*, applying expert judgment rather than just capturing preferences at face value.

- Architecture shape: monolith vs. services, client-server split, batch vs. real-time.
- Security: authn/authz model, secrets handling, data sensitivity, threat surface.
- Performance & cost: expected load, latency budget, infra cost ceiling, what happens at 10x scale.
- State management: where state lives, source of truth, caching, consistency requirements.
- Data model: core entities, relationships, expected data volume/growth.
- API contracts & integrations: what talks to what, third-party dependencies, versioning/stability of those contracts.
- Scalability expectations: is this for 10 users or 10 million? Does that change between launch and year one?

Good follow-ups:
- "What happens when the network goes down mid-operation?"
- "If this fails, what's the most likely reason?"
- "What's the one part of this that's hardest to change later if we get it wrong?"

### Phase 2 — User experience: design alignment

Apply design expertise to pin down the experience, not just the feature list.

- Component library / design system to use (or build from scratch?).
- Visual language: font, color scheme, tone, existing brand constraints.
- Accessibility requirements (WCAG level, keyboard nav, screen reader support, contrast).
- Core user flows — walk through the primary path start to finish, and at least one secondary path.
- Platform considerations: mobile vs. web vs. both, responsive behavior, native vs. web wrappers.
- Error states and recovery paths — what does the user see and do when something breaks?
- Loading states and perceived performance — skeletons, spinners, optimistic UI, what feels "fast enough."

Good follow-ups:
- "Walk me through what someone sees the very first time they open this."
- "What should happen if [key action] fails halfway through?"
- "Is there an existing design system or brand guide this needs to match?"

### Phase 3 — Tradeoffs: risks, dependencies, constraints

Surface what could go wrong or get in the way before committing to a plan.

- Key risks and their likelihood/impact.
- Dependencies: external services, teams, approvals, data availability.
- Constraints: budget, timeline, team skill set, existing tech debt, legal/regulatory limits.
- What assumptions is the plan resting on, and what breaks if they're wrong?

Good follow-ups:
- "If this fails, what's the most likely reason?"
- "What are we depending on that we don't control?"
- "What's the assumption that, if wrong, blows up the whole plan?"

### Phase 4 — Priorities: making the tradeoff calls explicit

Turn tradeoffs into decisions, and write the decisions down (not just the topics).

- Speed vs. quality — where on that spectrum, and does it shift after launch?
- Build vs. buy — for each major component, was this considered, and why?
- Simplicity vs. flexibility — how much future-proofing is worth the complexity now?
- MVP scope vs. full vision — what's cut for v1, and what's the trigger to revisit?
- Technical debt tolerance — what shortcuts are acceptable now, and what's the plan to pay them off?

Good follow-ups:
- "If you had to ship half of this, which half survives?"
- "What's the shortcut we're comfortable taking now, and when do we have to stop being comfortable with it?"

## Blind spots to proactively cover

Users forget these more often than not — raise them even if unasked, briefly, and skip only if clearly irrelevant to scope:

- Offline / degraded-mode behavior
- Data migration from any existing system
- Internationalization / localization
- Audit logging and compliance requirements
- Backup and disaster recovery
- Admin/operator experience, not just end-user experience
- Onboarding and first-run experience
- Sunset plan and data deletion / retention

## Digging deeper on answers

When the user answers a question:
- If the answer seems shallow or you can't yet act on it, ask "why?" or for a concrete example.
- Ask about exceptions: "does that hold true for [edge case] too?"
- If an answer conflicts with an earlier one, surface the conflict — don't quietly pick one.
- Respectfully challenge assumptions that seem load-bearing but unexamined ("what if that's not true?").
- Explore implications: if they say "must-have," ask what happens if it slips.

## Producing and updating CLAUDE.md

Once phases 0–4 have enough signal (doesn't have to be exhaustive — "enough to build correctly" is the bar), write or update the project's `CLAUDE.md` (check for `AGENTS.md` or similar if that's the convention in use; ask if unsure which file the user wants).

**Before writing:**
- Check whether a `CLAUDE.md` already exists in the project. If it does, read it fully first — update it in place, preserving anything still accurate, rather than overwriting wholesale.
- Summarize back to the user what you've gathered, organized by the five phases, and explicitly flag: (a) any assumptions you made where they didn't answer, (b) any open questions still unresolved. Get a quick confirmation or correction before finalizing — this is the alignment checkpoint.

**Structure the CLAUDE.md so an executing LLM can act on it without re-deriving context.** Suggested shape (trim sections that don't apply, especially for "Quick" depth projects):

```markdown
# Project: <name>

## What this is
<1-3 sentences: the problem, the audience, the solution>

## Success criteria
<what "done" and "working" look like, concretely and ideally measurably>

## Requirements
### Must-have
- ...
### Nice-to-have (not v1)
- ...
### Explicitly out of scope
- ...

## Architecture
<stack, services, state management, data model summary, API contracts,
integrations, scale/perf targets, security model>

## Design / UX
<component library, visual language, key user flows, accessibility bar,
platform targets, error/loading state conventions>

## Known risks & dependencies
- ...

## Decisions & tradeoffs
<the explicit calls made in phase 4, and why — this section is what
prevents an executing agent from re-litigating settled decisions>

## Open questions
<anything still unresolved — an executing agent should ask before
guessing on these, not silently decide>

## Conventions for whoever (human or LLM) implements this
<coding style, testing expectations, commit/PR conventions, anything
that keeps output consistent with how this project wants to be built>
```

**After writing:** tell the user what changed (new file vs. diff-style summary of edits to an existing one) and point out anything in "Open questions" that will block a clean implementation start.

## When plans change mid-project

If the user comes back with new information, a pivot, or a correction to something already decided: update the relevant section of `CLAUDE.md` directly rather than appending contradictory notes. Treat this the same as the initial alignment checkpoint — confirm the change with the user before locking it in, especially if it invalidates decisions downstream (e.g., changing the data model after the API contract was already agreed).
