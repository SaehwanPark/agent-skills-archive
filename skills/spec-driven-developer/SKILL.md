---
name: spec-driven-developer
description: Use when implementing, reviewing, or planning changes in a small or mid-sized project that treats SPEC.md, ARCHITECTURE.md, and CHANGELOG.md as lightweight operational state and needs those documents kept aligned with the code.
---

# Spec-Driven Developer

Keep project intent, current design, and meaningful history synchronized with the work.
Use the repository's existing equivalents when it uses different filenames or conventions.

## Core rules

- Read applicable project instructions and existing state documents before editing.
- Keep documentation proportional to the change; do not introduce an enterprise process.
- Preserve unrelated entries and concurrent contributors' work.
- Treat implementation and tests as evidence, not as permission to claim undocumented behavior.
- Preserve documented constraints unless the user explicitly changes them.
- Mark uncertainty or partial completion instead of presenting stale material as verified.

## Select the documents

Update only documents affected by the task:

- `SPEC.md`: intended capabilities, active scope, verification, and deferred work. Read
  [the specification workflow](references/specification.md).
- `ARCHITECTURE.md`: system structure, ownership, data flow, dependencies, and important
  invariants. Read [the architecture workflow](references/architecture.md) only when the
  implementation changes one of those concerns.
- `CHANGELOG.md`: meaningful user- or contributor-visible history. Read
  [the changelog workflow](references/changelog.md) when the task warrants an entry.
- `TASKS.md` or an existing equivalent: short-lived execution details only when the task
  needs them.

If the project adopts this workflow but lacks the core files, use
[the bootstrap templates](assets/project-doc-templates.md) to create the smallest useful
versions. Do not create missing files merely because this skill was loaded.

## Workflow

1. Inspect the current documents, implementation, tests, branch, and requested outcome.
2. Identify the smallest documentation set affected by the change.
3. Before implementation, place active intent and observable verification in the
   project's specification or equivalent when that document exists or is being adopted.
4. During implementation, update active scope only when reality changes materially.
5. After implementation, reconcile the documents with actual behavior and test evidence.
6. Record unfinished or rolled-back work honestly; do not erase useful history.
7. Review the final diff for contradictions among specification, architecture, changelog,
   implementation, and tests.

## Concurrency and partial work

- Make additive, targeted edits; never overwrite unrelated active items.
- If two sources disagree, record the inconsistency and avoid guessing which is canonical.
- Keep incomplete work active or planned. Move it to completed history only after its
  verification criteria are satisfied.
- On rollback, restore the active state and explain what remains; retain historical
  changelog entries unless they are factually wrong.

## Stop conditions

Stop and ask before proceeding when:

- Existing documents prescribe incompatible architectures or scopes.
- The requested change would silently break a documented invariant.
- Bootstrapping project-wide state files was not requested and would materially expand
  the repository's process.
- Completion cannot be supported by implementation or verification evidence.

## Expected output

Report:

- Documents changed and why each was affected.
- Verification used to reconcile them with the implementation.
- Any conflicts, uncertainty, deferred work, or known stale sections.
