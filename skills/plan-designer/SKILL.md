---
name: plan-designer
description: Use when creating, revising, or reviewing a coding implementation plan that must become bounded, decision-complete, testable, and safe for another engineer or coding agent to execute without guessing.
---

# Plan Designer

Turn an ambiguous coding request into the smallest operational plan that preserves existing
behavior unless change is explicitly required.

## Planning workflow

1. Inspect repository instructions, current implementation, public contracts, tests, and
   relevant history before asking discoverable questions.
2. Restate the requested outcome as observable behavior and identify what must remain
   unchanged.
3. Resolve product preferences with the user; record technical assumptions that cannot be
   proven before implementation.
4. Choose the smallest approach using existing platform, standard-library, framework, and
   dependency capabilities before proposing new machinery.
5. Name likely edit targets, interfaces, data flow, concrete failure states, and migration
   or compatibility effects where applicable.
6. Define focused tests, acceptance criteria, non-goals, stop conditions, and one risk
   label.
7. Check that an implementer can identify the first three actions without making a design
   decision.

Use [the plan template](assets/plan-template.md) when a detailed operational handoff is
needed. Use [the quality checklist](references/quality-checklist.md) before returning a
non-trivial plan. Consult [ambiguity rewrites](references/ambiguity-rewrites.md) only when
the draft contains vague goals, and [the example plan](references/example-plan.md) only
when the expected level of detail is unclear.

## Required plan content

Adapt the presentation to task size, but include:

- Narrow task restatement and current repository understanding.
- Explicit assumptions and instructions to stop when they are false.
- Ordered implementation changes with likely files or bounded discovery targets.
- Public API, schema, I/O, compatibility, or migration effects—or an explicit statement
  that none are expected.
- Concrete test cases, commands, and observable acceptance criteria.
- Non-goals, stop conditions, handoff requirements, and exactly one risk label.

Do not pad a small refactor to satisfy a template. Do not hide uncertainty behind vague
verbs such as “improve,” “robustify,” or “clean up.” Convert edge cases into explicit inputs
or states.

## Boundaries

- Avoid new dependencies, public API changes, broad rewrites, generated-file edits, and
  opportunistic cleanup unless the request requires them.
- Require the implementer to stop instead of improvising when repository reality conflicts
  with the plan.
- Reserve review for semantic correctness, scope, and risk—not only test passing.
- Label low risk for local changes, medium risk for multiple consumers or compatibility
  concerns, and high risk for public contracts, persistence, concurrency, security,
  payments, privacy, production configuration, or data loss.

## Execution handoff

Include this instruction:

> Implement exactly this plan. Do not broaden scope. If the plan conflicts with the
> codebase, stop and report the conflict instead of improvising.

Require the implementer to report files changed, tests run, deviations, and unresolved
risks.
