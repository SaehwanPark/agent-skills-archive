---
name: preferred-workflow
description: Use when resuming from checkpoints, handling feature requests, or refactoring safely across projects. Guides feature-branch setup, push and PR handoff, and a three-pass code-reviewer loop with fix-and-reply cycles before merge-ready delivery.
---

# preferred-workflow

## When to use this skill

Use this skill when the task is a development continuation, a new feature request, or a refactor that should be carried out in a disciplined, repeatable way across different projects.

Use it when you need to:

- recover context from the latest checkpoint or branch tip
- decide what is already complete and what remains
- turn a feature request into a concrete implementation slice
- refactor without changing behavior beyond the agreed scope
- hand work off for review with a clear, verifiable diff on a temporary branch and open PR

## Core workflow

1. Inspect the current project state first.
2. Identify the latest checkpoint, branch, spec, notes, or equivalent source of truth.
3. Classify the task as one of:
   - development continuation
   - feature request
   - refactor
4. Select the smallest useful target slice.
5. **Branch setup** — create or confirm the working branch (see below).
6. Write or update failing tests before implementation when behavior is changing.
7. Implement the slice completely, without stubs or placeholders.
8. Run the project's tests and checks for the slice.
9. Update relevant docs or lightweight project state files when they exist.
10. **PR handoff** — commit, push, and open a PR when approval allows (see below).
11. **Review loop** — run three `code-reviewer` passes, fix findings, reply on the PR, and re-review until merge-ready (see below).
12. Report completion only after the **Completion checklist** passes.

## Branch setup

Required when the project uses git and the slice changes tracked files.

1. Record `base_branch` (repo default, usually `main` or `master`).
2. If already on a non-default branch for this slice, confirm it matches the checkpoint or open PR before editing.
3. Otherwise create a temporary branch from `base_branch`:
   - `git fetch origin <base_branch>` when a remote exists
   - `git checkout <base_branch>` then `git pull` when safe
   - `git checkout -b <prefix>/<short-slice-name>`
   - Prefix: `feat/` for feature request, `fix/` for bugfix continuation, `refactor/` for refactor
4. Do not implement the slice on `base_branch` unless the user explicitly asked to work there.

Stop and ask if the working tree is dirty on the wrong branch, or if the slice clearly belongs on an existing open branch or PR.

## Development continuation

When resuming from the latest checkpoint:

- inspect the latest branch, commit, checkpoint note, or project-specific progress record
- confirm the current branch matches the checkpoint branch before editing
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

- use the project's equivalent notes, checkpoint files, or task tracker
- do not invent a heavy documentation system just to satisfy the workflow

## Approval gates

Respect project and user git rules:

- **Commit, push, and open a PR** only when the user requested that handoff or the task explicitly includes opening a PR.
- If implementation and tests are done but approval is missing, stop with: branch name, diff summary, test results, and the exact commands you would run next. Do not claim the slice is fully delivered.
- If the user asked only for local implementation with no PR, skip PR handoff and the review loop; still use a temporary branch unless they asked to work on `base_branch`.

## PR handoff

Required after the slice is implemented and tests pass, unless the user opted out or git remote / PR tooling is unavailable after fallbacks.

1. Commit slice changes on the working branch (meaningful commits; follow the project's message style).
2. Push the branch: `git push -u origin HEAD`
3. Open a PR against `base_branch`:
   - GitHub: `gh pr create` with summary and test plan
   - Other hosts: use the closest equivalent (`glab`, web UI, or patch series)
4. Return the PR URL in the final report.

If `gh` or the remote is missing, run `which gh` (or the platform CLI), report the blocker, and provide the push command and draft PR body. Do not skip PR handoff without documenting why.

## Review loop

Required after a PR is open. Do not mark the work done until this loop completes or a stop condition applies.

### A. Spawn reviewers

- Read and follow `code-reviewer` for every pass.
- Run **exactly 3 independent passes** on the PR diff plus canonical spec or checkpoint docs and test output.
- Use parallel subagent/Task calls when available; otherwise run 3 sequential passes with a fresh diff read each time (`git diff <base_branch>...HEAD`).
- Keep findings from each pass labeled separately (Pass 1, Pass 2, Pass 3).
- Do not substitute one self-review for three passes.

### B. Triage

- Merge findings across passes; dedupe; rank by severity.
- Fix all `Critical` and `High` findings before merge readiness.
- For `Medium` and `Low`, fix or record an explicit deferral with rationale.

### C. Fix and verify

- Apply fixes on the same branch.
- Rerun the slice's tests and checks.
- Commit and push fixes to the PR branch.

### D. Reply on the PR

- Reply on the PR (or review thread) for each actionable finding: fixed, won't fix (with reason), or deferred.
- Resolve review threads when the platform supports it.

### E. Re-review gate

- After any `Critical` or `High` fix, run at least **1 follow-up `code-reviewer` pass** on the updated diff.
- Repeat C–E until no open `Critical` or `High` findings remain.

### F. Merge readiness

- Apply `babysit` when CI fails or bot/human comments appear after the review loop.
- Mark merge-ready only when: tests pass, PR URL is present, all `Critical`/`High` findings are addressed or explicitly accepted by the user, and review threads are triaged.

### Without PR support

When git exists but no PR host is available:

- run the same 3-pass `code-reviewer` loop on `git diff <base_branch>...HEAD`
- apply fixes, recommit, and document findings and resolutions in the final report
- note the limitation; do not pretend a PR was opened

## Integration with other skills

This skill composes well with:

- `plan-designer` for turning a request into a bounded implementation plan
- `spec-driven-developer` for keeping project state and documentation aligned
- `code-reviewer` for post-implementation review (required in the review loop)
- `babysit` for CI and comment triage after the review loop

Use the narrower skill when it is a better fit for the immediate task.

## Stop conditions

Stop and report before claiming completion if:

- the slice is implemented but still on `base_branch` with unmerged work and the user did not request direct-to-main delivery
- a PR was requested but no PR URL exists and tooling was not genuinely unavailable
- fewer than 3 `code-reviewer` passes ran without documenting the escape hatch
- open `Critical` or `High` review findings remain unaddressed and unaccepted
- branch identity does not match the checkpoint or open PR for a continuation task
- required tools (`git`, `gh`, tests) are missing and no acceptable fallback was approved

## Completion checklist

Do not report the slice as done until every applicable item is checked:

```
- [ ] Task type classified and slice named
- [ ] Working branch confirmed or created (not base_branch unless requested)
- [ ] Tests/checks run for the slice
- [ ] Docs or checkpoint notes updated when they exist
- [ ] Commits on working branch (if approval granted)
- [ ] Branch pushed (if PR handoff required)
- [ ] PR URL returned (if PR handoff required)
- [ ] 3 code-reviewer passes completed with separate findings
- [ ] Critical/High findings fixed or explicitly accepted
- [ ] PR replies posted for actionable review feedback (if PR exists)
- [ ] Follow-up review after Critical/High fixes
- [ ] CI/comments triaged (babysit when needed)
```

## Non-goals

- Do not assume every project uses `SPEC.md`.
- Do not require GitHub specifically when another PR or review platform exists.
- Do not turn the workflow into a project-management system.
- Do not broaden the task beyond the smallest useful slice without a clear reason.
- Do not skip tests when the change affects behavior.
- Do not skip the review loop because PR tooling is inconvenient when git diff review is still possible.

## Expected output

When using this skill, report:

- the chosen task type
- what was already complete
- what slice was selected
- `base_branch` and working branch name (created or reused)
- what tests or checks were run
- what docs or handoff notes were updated
- PR URL, or why PR handoff was skipped
- review summary: pass count, findings by severity, fix/defer disposition, merge-ready yes/no
- any deferred work or review caveats
