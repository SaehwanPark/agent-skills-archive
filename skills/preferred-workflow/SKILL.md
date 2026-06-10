---
name: preferred-workflow
description: Use when you want a reusable workflow for resuming from checkpoints, handling feature requests, or refactoring safely across projects.
---

# preferred-workflow

## When to use this skill

Use this skill when the task is a development continuation, a new feature request, or a refactor that should be carried out in a disciplined, repeatable way across different projects.

Use it when you need to:

- recover context from the latest checkpoint or branch tip
- decide what is already complete and what remains
- turn a feature request into a concrete implementation slice
- refactor without changing behavior beyond the agreed scope
- hand work off for review with a clear, verifiable diff

## Core workflow

1. Inspect the current project state first.
2. Identify the latest checkpoint, branch, spec, notes, or equivalent source of truth.
3. Classify the task as one of:
   - development continuation
   - feature request
   - refactor
4. Select the smallest useful target slice.
5. Write or update failing tests before implementation when behavior is changing.
6. Implement the slice completely, without stubs or placeholders.
7. Commit at meaningful milestones when the project’s workflow supports it.
8. Update relevant docs or lightweight project state files when they exist.
9. Prepare a PR or the project’s closest equivalent handoff.
10. Run the appropriate review loop before marking the work done.

## Development continuation

When resuming from the latest checkpoint:

- inspect the latest branch, commit, checkpoint note, or project-specific progress record
- identify what is complete, what is partially complete, and what remains
- choose the next thin slice or split a coarse slice if that is safer
- preserve unfinished scope explicitly so it can be resumed later

Prefer to recover the actual working state rather than reconstructing it from memory.

## Feature request

When the task is a feature request:

- restate the requested outcome as observable behavior
- turn the request into acceptance criteria before editing
- add failing tests that describe the expected behavior
- keep the implementation bounded to the requested slice unless the codebase proves that a smaller change is unsafe

Avoid broadening a feature request into unrelated cleanup or architecture work.

## Refactor

When the task is a refactor:

- add characterization tests first if behavior is not already locked down
- preserve user-visible behavior unless the task explicitly calls for a change
- move toward simpler, clearer, or more maintainable code only within the agreed scope
- stop if the refactor turns into a redesign, unless that broader change is approved

Treat behavior preservation as the default unless the task says otherwise.

## Documentation and project state

If the project has `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, or similar workflow docs:

- update the relevant file(s) to match the implementation
- keep the documentation lightweight and current
- record deferred slices or follow-up work clearly

If the project does not have those files:

- use the project’s equivalent notes, checkpoint files, or task tracker
- do not invent a heavy documentation system just to satisfy the workflow

## Review loop

When the environment supports pull requests and independent reviewers:

1. Open a PR or equivalent reviewable change set.
2. Request review on the PR diff plus the project’s canonical spec or checkpoint docs.
3. Prefer exactly 3 independent `code-reviewer` passes when the platform and agent setup support it.
4. Keep reviewer feedback separate and trace each comment back to a concrete fix, explanation, or deferment.
5. Mark the change ready for merge only after the review comments are resolved.

When the environment does not support that setup:

- use the closest local review workflow available
- preserve the same review intent: independent critique, concrete findings, and explicit resolution
- note the limitation instead of pretending the full PR workflow was available

## Integration with other skills

This skill composes well with:

- `plan-designer` for turning a request into a bounded implementation plan
- `spec-driven-developer` for keeping project state and documentation aligned
- `code-reviewer` for post-implementation review

Use the narrower skill when it is a better fit for the immediate task.

## Non-goals

- Do not assume every project uses `SPEC.md`.
- Do not require GitHub specifically when another PR or review platform exists.
- Do not turn the workflow into a project-management system.
- Do not broaden the task beyond the smallest useful slice without a clear reason.
- Do not skip tests when the change affects behavior.

## Expected output

When using this skill, report:

- the chosen task type
- what was already complete
- what slice was selected
- what tests or checks were run
- what docs or handoff notes were updated
- any deferred work or review caveats
