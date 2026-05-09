# Operational coding plan template

## Task restatement

Implement [specific behavior] while preserving [specific existing behavior or API].

## Current understanding

- Relevant code appears to be in [files, modules, or search target].
- Desired behavior is [behavior].
- Existing behavior that must not change is [behavior].
- Main uncertainty is [uncertainty, or none identified yet].

## Assumptions

- [Assumption 1]
- [Assumption 2]

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1. Inspect [file or function] to confirm [specific condition].
2. Change [function, class, or module] so that [precise behavior].
3. Add or update focused tests for [case 1] and [case 2].
4. Run [specific test or check command].
5. Summarize the diff and any remaining risks.

## Files and functions likely to change

- `path/to/file.ext`: [specific intended change]
- `path/to/test_file.ext`: [specific intended test]

Avoid editing files outside this list unless the plan is found to be incomplete. If that happens, stop and explain why.

## Tests and checks

Run [command].

Expected result:

- [Expected result]

If tests fail:

1. Fix failures directly related to this change.
2. Do not fix unrelated failures unless required to unblock validation.
3. Report unrelated failures separately.

## Acceptance criteria

- [Observable criterion 1]
- [Observable criterion 2]
- [Observable criterion 3]

## Non-goals

- Do not [out-of-scope change].
- Do not [refactor, rename, or reformat].
- Do not change public APIs unless explicitly required.
- Do not perform opportunistic cleanup.

## Stop conditions

Stop and ask for review if:

- The required change affects public API compatibility.
- More than [N] production files need edits.
- The implementation requires a broader refactor than planned.
- Tests reveal behavior not covered by the task.
- The plan conflicts with existing code structure.

## Review checklist

Before finalizing, verify:

- The diff implements only the requested behavior.
- The change is covered by focused tests.
- Existing behavior is preserved.
- No unrelated formatting, renaming, or cleanup was introduced.
- Error handling and edge cases are explicit.
- The final summary lists files changed and tests run.

## Risk label

Risk: [low, medium, or high]

Reason: [one sentence]
