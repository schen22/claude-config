---
name: structure-review-lens
description: A core code review lens for scope discipline and code shape — whether the change earns its place, and whether what survives is modular, named well, and free of duplication.
---

# Lens: Structure & Scope

> **Core Question:** Does every line here need to exist, and is what survives shaped so the next person can change it?
> **Rule:** Rule of three — duplicate twice, extract on the third. It governs both halves: abstractions extracted too early and duplication left too long are the same mistake at different ends.

---

## Part 1 — Does it earn its place?

Classify **every hunk** as **required** (the ask fails without it), **enabling** (justified in one line), or **unrequested** (the finding). State the ask in one sentence from the task or spec, never from the diff.

**Hard stops — Blocker, report rather than merge:**

- A file touched outside declared ownership, or any frozen file edited.
- A new runtime dependency, config file, env var, or build step.
- A change contradicting the spec — escalate, never reverse quietly.

**The catalogue** — name the pattern in the finding:

- **Speculative generality** — a parameter, option, or hook with no current caller.
- **Premature abstraction** — extracted at the second occurrence, so its shape fits one example and breaks on the third.
- **Single-caller indirection** — a wrapper used exactly once. Inline it; it is a layer, not a design.
- **Drive-by refactor** — unrelated renames or reformatting. Hides the real diff, blocks a clean revert.
- **Defensive code for impossible states** — a guard against a caller that does not exist.
- **Speculative error handling** — `catch` that logs and continues, hiding a failure nobody has seen.
- **Config for a value with one setting** · leftover TODOs, commented code, `console.log` · a new export nothing imports.

---

## Part 2 — Is it shaped right?

**Budgets** (defaults; bindings override, but state the number): function 40 lines · parameters 3 · nesting depth 3 · file 300 lines · module exports 7 · branches per function 10.

**Duplication.** Before flagging, ask **do these change for the same reason?** Identical blocks answering to different specs or different owners must stay separate — merging them creates a shared file two people must edit. Real duplication, in order of cost: a repeated literal (hex, URL, magic number) → a repeated derivation → parallel structure → a re-implemented platform function. Search the repo before flagging; the helper may exist.

**One function, one thing** — every line at the same level of abstraction, one reason to change. Smells: the name needs "and" · it decides *and* does · a boolean parameter · I/O mixed with logic · a comment introducing a block, which names the function you should have extracted.

**Naming.** Says what, not how (`activeUsers`, not `loopUsersAndFilter`) · length scales with scope · no type in the name · no repeating the container (`User.name()`, not `User.getUserName()`) · no vague verbs (`handle`, `process`, `manage`) · booleans read as predicates · symmetric pairs (`open`/`close`) · no `utils.js` dumping grounds. A name needing a comment is the finding; a very long name means the function does too much.

**Cohesion.** If a type's fields split into two groups used by two disjoint sets of methods, it is two types. Group by feature, not by kind — that is also what makes single-writer ownership possible. A class with one method and no state is a function. Compose; inherit only for genuine substitutability.

**Contracts** — write one only when two or more implementations exist now, when a boundary crosses owners, or when a consumer must not depend on the implementation. Otherwise the concrete type is the contract. A JSDoc typedef or a table in the spec counts. Test: can a consumer be written against it without knowing who implements it?

---

## Not a finding

Work the spec requires that the task sentence omitted · duplication between things that change for different reasons · a long but flat function · a name that is unusual but accurate and consistent with the codebase · tests for the code actually written.
