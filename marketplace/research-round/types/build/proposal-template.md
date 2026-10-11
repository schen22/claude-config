# Build proposal — template

The synthesizer writes this from the role reports. It is the one thing Sarah reads first.
Link each claim to the report it comes from (`../references/<file>.md#section`). Don't repeat what
a report already says: decide, score and order.

```markdown
# Proposal — <question>

<date> · Round: <slug> · Reports: [role](../references/<slug>-<role>.md), … · Status: **for review**

## TL;DR

- The recommendation in 3–5 bullets, and the one decision that most needs Sarah.

## Terms

| Term | Meaning here |
|---|---|

## Scorecard

| Option / plan | Goal 1 | Goal 2 | … | Cost | Maintenance |
|---|---|---|---|---|---|
(One cell per goal / success criterion: ✓ / partial / ✗ plus a few words of reason, with links.)

## Recommended build order

| # | Step | Serves | Depends on | Size (assumptions) |
|---|---|---|---|---|

## MVP vs later

- **MVP:** …
- **Later:** … (and the trigger that brings each one in)
- **Not building:** … (and why)

## Where the roles disagree

How each disagreement was settled, and why.

## Decisions for Sarah

| # | Decision | Default | Blocks | Source |
|---|---|---|---|---|

## Confidence

What rests on Low-confidence or unverified evidence, and how to check it cheaply.
```
