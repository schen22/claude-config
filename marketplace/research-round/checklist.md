# Overseer checklist (core)

Every round answers these, plus its type's checklist (`types/<type>/checklist.md`). For each
report: **pass**, or **fail** with the exact fix (section, what to change). A fix says what to
write, not "improve X". Cross-report consistency is checked across all reports.

| # | Question |
|---|---|
| 1 | Does it open with a **TL;DR** that gives the answer, not the background? |
| 2 | Is there a **Terms** table, with every abbreviation and term of art defined? |
| 3 | Is every cross-reference to a project file, section or question a **relative link**? |
| 4 | Does every claim have a **source and a confidence level**? Are the fact-checker's "unverified" marks kept, not hidden? Were the numbers recomputed (see the fact-check notes)? |
| 5 | Are options compared on **advantages mapped to the goals (by ID), gaps, cost and maintenance**, with a stated reason for the pick? |
| 6 | Does every estimate **list its assumptions**? |
| 7 | Is every rate written as **numerator ÷ denominator**? |
| 8 | Is there a **happy-case** and a **complex-case** example? |
| 9 | Are **edge cases** listed? |
| 10 | Does every **open question** have a default and say what it blocks? |
| 11 | Does **Key findings and trends** hold 3–6 findings that are non-obvious (not a must-have anyone would list), each with evidence, trend where relevant, and the decision it changes? |
| 12 | Are the **role artifacts** listed in the agent's prompt present, and is the report mostly those (not a re-derivation of a decision every role was asked for)? |
| 13 | Is there at least one **Mermaid diagram** where structure or data clarifies, built only from the report's own numbers? |
| 14 | Is any research **invented** (quotes, participants, counts, survey results without a source)? Unrun studies must be labelled plans. |

## Metrics, projections and targets

Answer when a report sets metrics, targets, projections or experiments; otherwise `n/a`.

| # | Question |
|---|---|
| M1 | **Counterfactual:** does every projection show a do-nothing baseline next to the with-change line, and credit the change only with the gap (exogenous growth such as adoption is not counted as impact)? |
| M2 | **Scenarios:** do Low-confidence inputs get low / base / high cases, and does it name the input that moves the result most? |
| M3 | **Derived targets:** is each target baseline + named levers' expected lift (each lift sourced), stated as commit / stretch, relative to baseline while the baseline is assumed, with absolute targets committed only after the baseline is measured? |
| M4 | **Achievable:** is each target checked against plausible throughput (e.g. wins needed ÷ typical win rate × effect size) or a dated benchmark? |
| M5 | **Measurable:** is every metric tagged A (existing logs) / B (needs new instrumentation) / C (needs sampled labels), with committed targets only where a baseline exists or has a dated plan? |
| M6 | **Mix and gaming:** are blended rates mix-adjusted or shown per segment, and does each target name its gaming risk and counter-metric? |
| M7 | **Experiment cards:** hypothesis + where it comes from; control → treatment; unit of randomisation; one primary metric chosen in advance; MDE (sizes the test) kept separate from the ship rule (the decision); sample including clustering and outcome lag; guardrails with non-inferiority margins? |
| M8 | **Guardrails can veto:** does each guardrail have a threshold or margin? ("unknown" or "no rise" fails.) |
| M9 | **Coverage:** does every problem in the goals have at least one metric, grouped by the question it answers? |
| M10 | **Value:** does the north star connect to business value (e.g. hours saved × loaded cost, avoided spend) with sourced inputs, or say what is missing? |
| M11 | **Ranking follows the scoring:** if a ranking overrides its own scores, is the override an open question for the user rather than the recommendation? |
