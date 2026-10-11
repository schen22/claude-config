# research-round

`/research-round:research-round <question> [type: build|strategy] [roles: …] [goals: …] [inputs: …]`

Up to 3 role agents research in parallel → a fact-checker per report → an overseer (checklists,
cross-role conflicts, coverage per goal) → one fix pass for failing reports → an Opus synthesis
writes `proposals/<slug>.md`. Reports land in `references/<slug>-<role>.md`.

| Type | Use for | Phasing |
|---|---|---|
| `build` | What to build next and how: a product, a feature, an MVP | MVP / later / not building |
| `strategy` | Where to play and how to win over 12 months: an external market or an internal platform | Q1–Q4 / not doing this year |

## Which roles for which question

Pick up to 3. Name a 4th only when the question really needs it (3 × roles + 2 agents).

| Role | Pick it when the question is about… | Not for |
|---|---|---|
| product-designer | Flows, screens or surfaces, states, accessibility | Market or metrics questions |
| ux-researcher | Who the users are, what they need, why they struggle; developer experience | Building the solution |
| competitive-analyst | The market, competitors, benchmarks, buy / build alternatives | Internal design detail |
| data-scientist | How success is measured; north star, KPIs, experiments, tracking | Picking the product direction |
| staff-software-engineer | Feasibility, architecture and platform boundaries, reliability, security, build vs buy vs extend | User needs |
| ml-engineer | Ranking, recommendations, AI: model / agent / tool selection, evals, context and memory, quality–latency–cost | Non-AI features |

## When a role is stretched (split it, or make it more specific)

The overseer rates every goal **deep / partial / none** each round. Split a role, or add a more
specific one, when **any** of these holds:

1. The same role leaves the same goal `partial` in **two rounds** in a row.
2. One report carries **3 or more goals** and at least one is `partial`.
3. Fix passes keep failing on the same lens (e.g. eval design, security).
4. You find yourself writing the missing lens into the question every time.

Otherwise, make the question narrower or add background (`inputs`) first: that's cheaper than a
new agent. Each role added costs ~70 tokens in every session and up to 3 agents per round.

## Updating

Edit in `~/.claude/marketplace/research-round/`, then run:

```sh
python3 tests/test_write_scope.py && node tests/test_prompts.mjs && claude plugin validate .
```

Bump `version` in `.claude-plugin/plugin.json`, commit, push `schen22/claude-config`, then
**Check for updates** on the marketplace in Customize → Plugins (Cowork, claude.ai, Claude Code).
