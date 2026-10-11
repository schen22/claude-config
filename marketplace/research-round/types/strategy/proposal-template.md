# Strategy proposal — template

The synthesizer writes this from the role reports: the draft of a **12-month strategy**, built on
the strategy kernel (diagnosis → guiding policy → coherent actions). Link each claim to the report
it comes from (`../references/<file>.md#section`). Decide, score and order; don't repeat reports.

**If the goals or background name a brief with its own structure or length** (e.g. a case
study's questions, "max 6 pages"), use the brief's structure and limit for the main body, answer
each of its questions under its own heading, and move the remaining sections below to an appendix.

```markdown
# 12-month strategy — <question>

<date> · Round: <slug> · Mode: external market | internal platform · Reports: [role](../references/<slug>-<role>.md), … · Status: **for review**

## Executive summary

Page 1, one story (Pyramid Principle):
- **Governing thought** in one sentence: the answer.
- **The story**: one concrete user's experience that shows the problems, then SCQA
  (situation, complication, question, answer) in a short table or ≤ 5 lines.
- **The order is the story**: the bets in order, with the one-line reason each comes where it does.
- **How we'll know**: the north star credited honestly against a do-nothing baseline, commit /
  stretch, the guardrails.
- **Why it's worth it**: the value bridge. **The ask**: what Sarah or the panel approves.

## What we learned, by role

| Role | Finding (non-obvious) | So what | Source |
|---|---|---|---|

2–3 findings per role, taken from each report's Key findings. Include the reports' diagrams where
they make the argument clearer.

## Levers: what moves the north star and the cost

Decompose the north star and the main cost metric into a formula, then one row per lever:

| Lever | Term in the formula | Problem | Baseline → change | Effect on the metric (arithmetic) | Effect on quality and human time | Confidence · source |
|---|---|---|---|---|---|---|

Then **findings → so what**: 3–5 cross-role findings no single report states alone (e.g. the lever
that moves quality and cost together; the pure-cost lever that needs no bet; the lever that pays
on cost while quality falls, so it needs a guardrail; whether the levers combined make a target
too easy or too hard).

## Terms

| Term | Meaning here |
|---|---|

## Diagnosis

The few problems that matter most, ranked, with evidence. What makes them hard.

## North star and guiding policy

The north-star metric and why; the guiding policy (the approach that rules options in or out);
for an internal platform, the boundary: what the platform owns vs each product, and the contract.

## Market or demand · alternatives

Size or demand (with method), trends, and the comparison of competitors or benchmarks and
buy / build / extend options.

## Strategic bets and trade-offs

| Bet | Goals served | Why now | Cost / effort (assumptions) | Confidence |
|---|---|---|---|---|

How the bets trade off against each other (e.g. quality vs latency vs cost), and the rule used.

## 12-month roadmap

| Quarter | Milestones | Exit criteria |
|---|---|---|
| Q1 | | |
| Q2 | | |
| Q3 | | |
| Q4 | | |

**Not doing this year:** … (and why)

## Metrics and the learning loop

| Group (question it answers) | Metric (numerator ÷ denominator) | Problem | Baseline | Commit / stretch | Measurability (A/B/C) |
|---|---|---|---|---|---|

Projection: do-nothing vs commit vs stretch, low / base / high scenarios. Experiment cards per the
core checklist M7.

The experiments planned, and how results move the roadmap (review cadence, decision rules).

## Assumptions

| Assumption | Why we assume it | How it shapes the recommendation | How to check |
|---|---|---|---|

## Risks

| Risk | Leading indicator | Response |
|---|---|---|

## Where the roles disagree

How each disagreement was settled, and why.

## Decisions for Sarah

| # | Decision | Default | Blocks | Source |
|---|---|---|---|---|

## Confidence and coverage

What rests on Low-confidence or unverified evidence; every goal the overseer rated partial or none.
```
