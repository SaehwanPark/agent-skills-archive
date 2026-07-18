---
name: simple-code-writer
description: Use when implementing, editing, or refactoring code and the solution should be the smallest correct change, prefer standard or platform capabilities, avoid speculative abstractions, and preserve existing contracts with proportional verification.
---

# Simple Code Writer

Choose the lowest total-cost solution across correctness, readability, maintenance,
performance, operations, and future change—not merely the fewest lines.

## Before editing

Inspect the request, repository instructions, current changes, relevant source and callers,
public contracts, tests, and established conventions. Read
[the simplicity checklist](references/checklist.md) before substantial implementation or
refactoring.

Apply these questions in order:

1. Can the requirement be eliminated, deferred, configured, or enforced at an existing
   boundary without changing agreed behavior?
2. Can the standard library or platform solve it directly?
3. Does an existing dependency solve a problem that belongs to its domain?
4. What is the clearest direct implementation that satisfies only the current requirement?

Ask before adopting a simpler alternative that changes agreed scope or behavior.

## Implementation rules

- Make the smallest coherent diff that satisfies observable behavior.
- Preserve public interfaces and user-visible behavior unless change is requested.
- Follow sound local patterns; do not introduce a competing architecture for a local edit.
- Introduce a helper or abstraction only when it names a stable concept, removes meaningful
  duplication, or enforces a real boundary.
- Keep state, effects, ownership, error handling, and data movement visible where they
  matter.
- Add a dependency only when simpler available options are inadequate and its lifecycle,
  security, and operational costs are justified.
- Optimize measured hot paths or explicit constraints, not hypothetical ones.
- Avoid stubs, speculative extension points, drive-by cleanup, and comments that narrate
  mechanics.

## Refactoring

Establish the behavior contract before changing structure. Add characterization coverage
when important behavior is unprotected. Prefer local simplification and stop when further
work would change behavior, widen scope materially, or require an architectural decision.

## Verification

Run the narrowest relevant tests, type checks, linters, or builds. Add focused tests for
changed behavior and important unprotected contracts, not implementation details. Report
unrelated failures separately.

## Composition and conflicts

Narrower domain skills may impose stronger requirements, but every added layer, type,
dependency, or process must solve a concrete problem. Follow explicit user and repository
instructions when they conflict with this baseline.

## Stop conditions

Stop when the simpler solution changes a public contract, multiple incompatible
architectures exist, a new dependency/migration/security change is unexpectedly required,
or relevant behavior cannot be verified.

## Expected output

Report behavior implemented, simpler alternatives materially considered, files changed,
tests and checks, deviations, and remaining risks or deferred work.
