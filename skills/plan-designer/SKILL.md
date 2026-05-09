---
name: plan-designer
description: Use when Codex is asked to create, improve, or review a coding implementation plan before editing code. This skill turns ambiguous or ambitious plan-mode output into a bounded, operational plan with explicit assumptions, file targets, tests, acceptance criteria, non-goals, stop conditions, and review checks.
---

# Plan Designer

Use this skill when working in plan mode for a coding task, or when asked to make a coding plan clearer, less ambitious, less ambiguous, or easier for another agent to execute.

The goal is to reduce implementation reasoning burden. The plan should make the next step mostly mechanical: inspect specific code, make bounded edits, add focused tests, run checks, and stop when the plan no longer fits the codebase.

## Operating principle

Prefer a plan that is boring, bounded, and verifiable.

A strong plan narrows the task to concrete behavior, names likely files and functions, states what must not change, defines tests, and gives the implementation agent explicit stop conditions.

## Use this skill when

- The user asks for a coding plan or implementation plan.
- The user asks to improve a plan before implementation.
- The task is subtle, cross-file, under-specified, or likely to invite overengineering.
- A lower-effort or separate agent will execute the plan.
- The user wants the implementation to stay tightly scoped.

## Do not use this skill when

- The user asked for direct implementation and the change is trivial.
- The user asked for exploratory research rather than a concrete code change.
- The right next action is only to inspect the repository and no responsible files can yet be named.
- The task is already fully specified and operational.

## Required plan shape

Produce plans with these sections in this order:

1. Task restatement
2. Current understanding
3. Assumptions
4. Minimal implementation plan
5. Files and functions likely to change
6. Tests and checks
7. Acceptance criteria
8. Non-goals
9. Stop conditions
10. Review checklist
11. Risk label

Use the template in `assets/plan-template.md` when drafting a new plan.

Use the checklist in `references/quality-checklist.md` before returning the plan.

Use the rewrite guide in `references/ambiguity-rewrites.md` when a plan contains vague or overly broad language.

## Planning rules

### Restate the task narrowly

Convert broad goals into concrete behavior. Preserve existing APIs and behavior unless the user explicitly requests a change.

Avoid vague goals such as improve validation, refactor auth, make parsing robust, or clean up resolver logic.

Prefer concrete statements such as add validation for whitespace-only names in `create_user` while preserving the existing `ValidationError` response shape.

### Make assumptions explicit

List any facts the plan depends on. Include the instruction that implementation should stop and report a mismatch if an assumption is false.

Examples of assumptions:

- A named function is the only write path.
- Existing error formatting must be preserved.
- Generated files should not be edited manually.
- A behavior applies only to a specific API surface.

### Bias toward minimal diffs

Plans should choose the smallest change that satisfies the task.

Avoid introducing new dependencies, new abstractions, broad rewrites, public API changes, formatting-only edits, drive-by cleanup, and multi-module refactors unless explicitly requested.

### Name likely edit targets

Identify likely files, classes, functions, tests, and commands.

If exact files are unknown, make repository discovery the first implementation step. Do not tell the implementation agent to edit every plausible path. Tell it to stop if multiple incompatible paths are found.

### Turn edge cases into inputs or states

Do not say handle edge cases. List concrete cases, such as omitted field, explicit null, empty string, whitespace-only string, duplicate ID, expired token, failed write, missing config key, or existing valid input.

### Define observable acceptance criteria

Acceptance criteria must be checkable by reading the diff, running tests, or exercising the behavior.

Avoid criteria such as code is cleaner or validation is better.

Prefer criteria such as whitespace-only `name` returns HTTP 400, existing valid create-user test still passes, and no public response fields are renamed.

### Add non-goals

Every plan must say what not to do. Non-goals prevent implementation agents from broadening scope.

Common non-goals:

- Do not rename public interfaces.
- Do not change generated files.
- Do not alter unrelated error messages.
- Do not add a dependency.
- Do not reformat files outside touched blocks.
- Do not perform opportunistic cleanup.

### Add stop conditions

Stop conditions prevent improvisation when the plan no longer fits reality.

Use stop conditions for public API changes, security-sensitive logic, persistence or migration behavior, concurrency, multiple incompatible code paths, broader-than-expected refactors, or unrelated test failures.

### Separate execution from review

The plan should reserve review for semantic correctness, not just test passing.

The review checklist must verify that the diff matches the task, follows the non-goals, uses focused tests, avoids fixture overfitting, and does not introduce a broader abstraction than needed.

## Risk labels

Assign exactly one risk label.

Low risk: single-function or small local behavior change, focused tests, no public API change.

Medium risk: multiple call sites, behavior relied on by other modules, nontrivial test setup, or moderate compatibility concern.

High risk: public API behavior, persistence format, migration, concurrency, security, auth, payments, privacy, data loss, or production configuration may change.

For high-risk plans, require a review pass before implementation.

## Execution handoff

When handing the plan to an implementation agent, include this instruction:

Implement exactly this plan. Do not broaden scope. If the plan conflicts with the codebase, stop and report the conflict instead of improvising.

Also require the implementation agent to report:

- Files changed
- Tests run
- Deviations from the plan
- Unresolved risks

## Final quality gate

Before returning a plan, verify that a lower-effort coding agent could implement it without guessing.

The first three edits should be obvious. Non-goals should be explicit. Tests should be concrete. Stop conditions should be present. The plan should be smaller than the task initially seemed. A reviewer should understand why each file changed.
