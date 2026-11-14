---
name: coupling-colocation-review-lens
description: A code review lens for inspecting module boundaries, dependency directions, shotgun surgery, and fragile hand-agreement pairs.
---

# Lens: Coupling & Colocation

> **Core Question:** Are related files and properties scattered, or do things that change together live together?  
> **Rule:** If changing X always requires changing Y, distance between them is a defect. Unchecked hand-agreement pairs are **Blockers**.

---

## Procedure

Build the dependency map for each changed file (`grep -rn "<basename>"`):

1. Identify all imports (fan-out) and callers (fan-in).
2. Trace cross-module property reads/writes.
3. Locate all "hand-agreement" dependencies.

---

## Red Flags & Fixes

- **Hand-Agreement Drift (Blocker):** Two places that must manually agree (e.g., CSS class in JS, route paths, mirrored constants).  
  _Fix:_ Enforce via (1) Single source generation, (2) Automated test assertion, or (3) Explicitly documented risk.
- **Shotgun Surgery & Scatter:** One conceptual change requiring edits across $N$ distant files, or a single property modified across $3+$ modules.  
  _Fix:_ Colocate by feature; encapsulate state behind a single owner.
- **Divergent Change:** One file modified for multiple unrelated functional reasons.  
  _Fix:_ Split into single-responsibility modules.
- **Inverted Dependency Direction:** Stable core code depending on volatile features, or underlying data logic depending on UI components.  
  _Fix:_ Invert direction (UI $\rightarrow$ Data, Volatile $\rightarrow$ Stable).
- **Cyclic & Extreme Coupling:** Circular imports ($A \rightarrow B \rightarrow A$), high fan-in (a de facto public contract), or high fan-out (a god module).  
  _Fix:_ Extract shared logic; freeze foundational contracts. Counts are a smell, not a threshold — a project that wants a number enforced writes a lint rule.

---

## Not a Finding

- High fan-in on foundational, stable contracts (e.g., global design tokens, core types).
- Superficially similar files with no actual code or logic dependencies.
- Architectural separation mandated by explicit repo/framework constraints.
