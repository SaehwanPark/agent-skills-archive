---
name: preferred-workflow
description: Use when resuming development, implementing a feature, or refactoring in a git repository that needs disciplined context recovery, branch setup, bounded implementation, verification, optional PR review, and push/PR handoff.
---

# Preferred Workflow

Move a coherent development slice from repository truth to a verifiable handoff without
broadening scope.

## Core workflow

1. Read repository instructions and inspect the working tree, current branch, relevant
   source, tests, docs, checkpoints, and open PR context.
2. Classify the task as continuation, feature, bug fix, or behavior-preserving refactor.
3. Define the smallest useful slice and its observable acceptance criteria.
4. Confirm or create a working branch from the repository's base branch.
5. Protect behavior with focused tests or characterization coverage when appropriate.
6. Implement the complete slice without placeholders or unrelated cleanup.
7. Run proportional tests and checks; update existing project-state documentation when
   the change affects it.
8. Commit, push, and open a PR only when the user or task authorizes that handoff.
9. Run the review loop when required by the user, repository, or default below.
10. Report branch, changes, validation, handoff, review disposition, and remaining risks.

Read [task-specific guidance](references/task-types.md) for continuations, features, bug
fixes, and refactors.

## Branch safety

- Record the base branch, normally the remote default.
- Reuse a non-default branch only when it matches the active task or PR.
- Otherwise update the clean base branch and create a short-lived branch with an
  appropriate `feat/`, `fix/`, or `refactor/` prefix.
- Do not switch branches over unrelated work or implement on the base branch unless the
  user explicitly requests it.
- Stop when a dirty tree, checkpoint, or open PR indicates the work belongs elsewhere.

## Approval gates and handoff

Treat commits, pushes, PR creation, merges, external comments, and deployments as separate
actions governed by user and repository authorization.

When PR handoff is authorized and implementation checks pass:

1. Commit coherent changes using the repository's message style.
2. Push the branch with `git push -u origin HEAD`.
3. Open a PR against the recorded base branch with a concise summary and test plan.
4. Return the PR URL.

If remote or PR tooling is unavailable, check the expected CLI path, report the exact
blocker, and provide the push command and prepared PR body. Do not claim that a PR exists.

## Review policy

Use the repository's review policy when one exists. Otherwise, after opening a PR, default
to the independent review procedure in [the review loop](references/review-loop.md).

Skip that procedure when the user explicitly says review is unnecessary or requests only
local implementation. Record the opt-out in the final handoff; still run implementation
tests and a basic author verification of scope and diff integrity.

## Documentation

Update existing specifications, architecture notes, changelogs, checkpoint files, or task
trackers only when the slice changes the state they describe. Do not create a heavyweight
documentation system solely to satisfy this workflow.

## Stop conditions

Stop and report before claiming completion when:

- Branch identity conflicts with a checkpoint or open PR.
- The required change exceeds the agreed slice or changes a public contract unexpectedly.
- Relevant tests cannot be run or expose unrelated failures that block validation.
- An authorized PR handoff has no PR URL and tooling was not genuinely unavailable.
- A required review has unresolved blocking findings.

## Completion report

Include:

- Task type, selected slice, base branch, and working branch.
- Files or behaviors changed and relevant project-state updates.
- Tests and checks, including failures.
- Commit/push/PR status and URL when applicable.
- Review pass count or the explicit reason review was skipped.
- Deviations, deferred work, and unresolved risks.
