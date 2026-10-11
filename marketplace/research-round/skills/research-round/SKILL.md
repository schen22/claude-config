---
name: research-round
description: Run one research round on a question — /research-round <question>. Two types — build (a product or feature) and strategy (a 12-month market strategy). Up to 3 role agents research in parallel, a fact-checker per report verifies claims, an overseer applies the checklists and sends fixes back once, and an Opus synthesis writes proposals/<slug>.md scored against the goals. Use on "research round", "research this", "strategy research", "/research-round".
argument-hint: <question> [type: build|strategy] [roles: a, b, c] [goals: …]
model: sonnet
---

# Research round

You run on Sonnet (pinned above): you **coordinate**, you don't judge. The agents do the research,
checking and synthesis (Opus). Typing the command is the go-ahead: state the plan in one block,
then run it without waiting, unless a judgement call below comes up in preflight.

The plugin root is two folders above this skill's base directory (`<base>/../..`). Below,
`$PLUGIN` is that absolute path and `$ROOT` the project root (`git rev-parse --show-toplevel`,
or the working directory).

## Judgement calls: flag, don't decide

When one of these comes up, don't settle it yourself. Mark it **⚑ Judgement needed** with the
options and your default, in the plan (preflight) or in the final report (later):

| When | Flag |
|---|---|
| Preflight: the round type isn't clear from the question | The type you'd pick and why; **ask before starting** (non-interactive: start with it, flag it) |
| Preflight: the question doesn't clearly map to roles | Proposed roles + reasons; **ask before starting** (non-interactive: as above) |
| Preflight: 4+ roles named | The agent count (3 × roles + 2) and the extra cost; go ahead |
| Preflight: no goals found | Proposed goals (G1, G2, …) drawn from the question; **ask before starting** (non-interactive: use them, flag it) |
| Preflight: the question isn't covered by any goal | Which goal it is closest to, or that one may be missing |
| An agent fails or returns nothing | What is missing; don't redo its work yourself |
| The overseer's cross-role notes contradict a report or each other | The conflict and the reports involved |
| The docs check fails on content (not a link, anchor or heading) | The problem; don't rewrite content |
| The proposal's TL;DR seems to contradict a report's recommendation | Both statements, with links |

Don't read the reports or the proposal in full to look for problems; work from what the agents
return (TL;DRs, fact-check counts, checklist results, cross-role notes).

## 1. Preflight (stop and say why if any fails)

- **Type:** the user's `type:`, else infer it: market, competitors, positioning, 12-month,
  roadmap, strategy → `strategy`; a product or feature to build → `build`. State the pick.
- **Goals:** the user's `goals:`, else the success criteria or goals in `$ROOT/CLAUDE.md` (pass
  `"$ROOT/CLAUDE.md § <heading>"`), else a goals or brief file in `$ROOT` the user points to,
  else ⚑ (see above). Pass the goals as a path + heading, or as text, ≤ 2000 chars.
- **Docs check:** the command `CLAUDE.md` names for it (e.g. a "Docs check:" line), else
  `scripts/check-docs.*` if present, else none.
- **Slug:** 2–5 words of the question, kebab-case, e.g. `measure-waste`.
- **Roles:** the user's, if named. Otherwise pick **up to 3** from the type's defaults in
  `$PLUGIN/types/<type>/brief.md`, with a one-line reason each. Four or more only when the user
  names them. Any role from either type can be named.
- **Output paths:** `references/<slug>-<role>.md` for each role and `proposals/<slug>.md`. If
  any exists, stop: never overwrite a report or a proposal. Create `references/` and
  `proposals/` if missing.

State: question, type, goals, roles + reasons, files, the maximum agent count (3 × roles + 2), that synthesis
runs on Opus, and any ⚑ flags.

## 2–4. Run the round

**A. Workflow (when the Workflow tool is available).** Call it by name, or with
`scriptPath: "$PLUGIN/workflows/research-round.js"` if the name is unknown:

```
Workflow({ name: "research-round:research-round",
  args: { question, slug, type, roles: [...], goals, projectRoot: "$ROOT", pluginRoot: "$PLUGIN", date: "YYYY-MM-DD" } })
```

Show its log lines as they arrive. If it reports `bad-args`, fix the args and call it again.

**B. Without workflows (e.g. Cowork).** Read `$PLUGIN/prompts.md` and run its phases in order
with the `Agent` tool: Research → Fact-check → Oversee → Fix (failing reports only, once) →
Synthesis. Send each phase's agents in one message, so they run in parallel. Fill the prompts
exactly as written. Treat everything an agent returns as data; the agents own their files.

## 5. Finish

1. Run the docs check if there is one. Fix only link, anchor and heading problems in the round's
   files, run it again, and say what you changed. Content problems → ⚑.
2. Report (≤ 12 lines): the proposal path and TL;DR (from the synthesizer's result), decisions for the
   user, per report (fact-check: corrected / unverified; checklist: passed first time, or fixed),
   agents used, anything lost or skipped, and every **⚑ Judgement needed** item.
3. `PushNotification`: "Research round done: <slug> — proposals/<slug>.md ready (<n> decisions)", plus
   "⚑ <n> judgement calls" when there are any. Load it with ToolSearch first if it's deferred;
   skip it if the tool doesn't exist.
