---
name: simple-code-writer
description: Use when writing, editing, or refactoring code to choose the smallest correct implementation, prefer standard and platform capabilities, avoid speculative abstractions, and verify changes proportionally. Do not use for planning-only or review-only tasks.
---

# Simple Code Writer

Write the simplest code that correctly solves the agreed problem. Simplicity means the
lowest overall cost across readability, maintainability, correctness, performance,
operational risk, and future modification. It does not mean the fewest lines.

## When to use

Use this skill for implementation work that writes, edits, or refactors code. Apply it as
a baseline alongside narrower skills that add domain, language, testing, documentation,
or workflow constraints.

Do not use it by itself for planning-only, review-only, research-only, or documentation-
only tasks. Use the skill specific to those tasks instead.

## Required context

Before editing, inspect:

- The user's requested behavior and agreed scope.
- Applicable repository instructions and existing conventions.
- Relevant source, callers, public contracts, tests, and current changes.
- Available standard-library, platform, framework, and dependency capabilities.

Read [the simplicity checklist](references/checklist.md) before substantive implementation
or refactoring.

## The six-step pause

Apply these questions in order before writing code:

1. **Does this need to exist?** Consider eliminating, deferring, configuring, or solving
   the requirement at a more appropriate boundary. Explain a materially simpler
   alternative, but do not silently change agreed behavior or scope. Ask for confirmation
   when adopting the alternative would do so.
2. **Can the standard library solve it?** Prefer maintained, documented language
   facilities over custom code.
3. **Does the platform already provide it?** Prefer database constraints, operating-
   system facilities, framework behavior, and runtime features over parallel mechanisms.
4. **Can an existing dependency solve it naturally?** Use a dependency only when the
   problem belongs to its domain. Its presence alone is not justification.
5. **Can it be expressed simply?** Prefer obvious control flow, ownership, mutation,
   error handling, and data transformations. A one-line expression is not automatically
   clearer.
6. **Only then write code.** Implement only the behavior required now.

## Implementation rules

- Make the smallest coherent diff that satisfies the observable behavior.
- Preserve public interfaces and user-visible behavior during refactors unless a change
  is explicitly requested.
- Follow established local patterns when they are sound; do not introduce a competing
  architecture for a local change.
- Prefer direct code over indirection. Introduce a helper or abstraction when it names a
  stable concept, removes meaningful duplication, or enforces a real boundary.
- Keep state, mutation, effects, ownership, and failure paths visible at the level where
  they matter.
- Add a dependency only when simpler available options are inadequate and the lifecycle,
  security, operational, and maintenance costs are justified.
- Optimize for measured hot paths or explicit constraints. Do not obscure ordinary code
  for hypothetical performance gains.
- Avoid stubs, speculative extension points, premature generalization, drive-by cleanup,
  and architecture for unrequested future requirements.
- Use comments to explain non-obvious rationale or constraints, not mechanics that clear
  code already expresses.

## Refactoring rules

- Establish the behavior contract from tests, callers, and public interfaces before
  changing structure.
- Add characterization coverage when important behavior is not protected.
- Prefer local simplification over redesign.
- Remove obsolete indirection and duplication only inside the agreed scope.
- Stop when further simplification would change behavior, widen the diff materially, or
  require a separate architectural decision.

## Verification

Scale verification to the risk and scope of the change:

- Run the narrowest relevant existing tests, type checks, linters, or builds.
- Add focused tests for changed behavior and important contracts that lack coverage.
- For behavior-preserving refactors, rely on existing contract tests or add
  characterization tests before changing internals.
- Do not add tests that merely reproduce implementation details.
- Report unrelated failures separately rather than expanding scope to fix them.

## Composition

This skill supplies implementation defaults. A narrower skill may impose stronger rules
for its domain, but added types, layers, abstractions, dependencies, or process must still
solve a concrete problem. Follow explicit user and repository instructions when they
conflict with this baseline.

Common pairings include:

- `plan-designer` before implementation to bound the change.
- `preferred-workflow` around implementation for branch, handoff, and review discipline.
- `fp-developer` when explicit state and effect boundaries reduce actual complexity.
- `code-commenter` when comments or public documentation need focused attention.
- `code-reviewer` after implementation to identify correctness and production risks.

## Stop conditions

Stop and report before improvising if:

- The simpler solution changes agreed behavior, scope, data, or a public interface.
- Existing architecture offers multiple incompatible implementation paths.
- A new dependency, migration, security-sensitive change, or broad redesign appears
  necessary but was not part of the request.
- Relevant behavior cannot be verified without unavailable context or tooling.

## Expected output

Report:

- The behavior implemented and any simpler alternative considered.
- Files changed.
- Tests and checks run, including failures.
- Deviations from the request or plan.
- Remaining risks or deliberately deferred work.
