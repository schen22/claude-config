---
name: runtime-protocol
description: The phase 3 protocol (not a lens) — how to run the build and suite, what evidence counts, and how to enumerate edge cases.
---

# Protocol: Runtime Evidence

> **Core Question:** Does it actually build, run, and hold up — proven by exit codes rather than by reading?
> **Rule:** A claim without an exit code is not a pass. An agent's own report is never evidence.

Almost none of this is the reviewer's job to check by hand. The build, the suite, and the CI gate decide it, on every build, for every agent. This protocol runs them and reads the result.

---

## 1. Run It

```
<build command>   → must exit 0
<test command>    → must exit 0
<CI / pre-commit gate>  → must exit 0
```

Capture exit codes, plus any warning **new** since the base commit — a new warning is a finding.

If the project cannot be built, report `RUNTIME: NOT RUNNABLE — <reason>` and mark every runtime claim unverified. An absent build never reads as a pass. If no CI gate exists, say `no Gate 1 configured` once — do not substitute manual greps for it.

---

## 2. Load What Changed

Only the pages or entry points this diff can reach. For each: **console shows zero errors** (an error is a Blocker), **network shows zero 4xx/5xx** and zero requests to an origin the project does not permit, and the thing renders at all.

That is the whole default runtime pass — no screenshot matrix, no width sweep.

---

## 3. Performance — One Number

```
Perf delta: +N KB built   (vs <base>)
```

Build at base, build at HEAD, diff the output size. Size budgets are the suite's job; this line is for the human reading the report. Add build seconds only when the change touches build tooling.

---

## 4. Screenshots — `deep` Only

Capture an image when a human asked to see it, when `ux` is running, or when a failure needs a picture to explain. Never as a routine sweep: images are the most expensive thing this skill can do, and anything they would catch mechanically — overflow, overlap, clipped text — is measurable in a test.

---

## 5. Edge Cases

Cheap, text-only, and the highest-value part of this phase. Walk the axes for the changed behaviour and record which cases hold:

| Axis | Cases |
| :--- | :--- |
| Cardinality | zero · one · many · far too many |
| Data | missing · empty string · wrong type · very long · unicode |
| Time | first visit · repeat visit · stale state · timezone ≠ author's |
| Input | double click · rapid toggle · keyboard only · back button |
| Environment | offline · storage off · scripts off · reduced motion · dark mode |
| External | resource 404 · blocked by a content blocker |

**Every new case found here becomes a test** (phase 4's regression obligation). Enumerating an edge case and fixing it without a test means the next agent reintroduces it.

---

## What Belongs in the Suite, Not Here

If this protocol ever finds itself grepping for a rule, that rule is a missing check. Say so in the report — *"no check covers X — add one to `<suite>`"*. A check in the suite runs on every build by every agent; the same check in a review runs only when someone remembers to review.
