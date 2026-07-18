# Specification workflow

Use the project's existing format when one exists. For a lightweight `SPEC.md`, organize
work as completed, active, and planned (commonly `Past`, `Present`, and `Future`). Keep the
active section intentionally small.

## Before implementation

1. Find the existing item or add one concise active item.
2. State the intended observable behavior.
3. Add verification criteria that can be demonstrated by tests or inspection.
4. Name important exclusions.
5. Preserve unrelated entries.

An active item may include a status, start date, branch, short summary, verification, and
out-of-scope list. Do not turn it into a second issue tracker.

## During and after implementation

- Update the item when scope or verification changes materially.
- After implementation, replace intent with the behavior actually delivered.
- Move the item to completed only after its criteria are verified.
- Leave unfinished follow-up work active or planned.
- Record known limitations and deliberate deferrals.

Verification may include unit or integration tests, manual checks, performance evidence,
migration validation, or compatibility checks. Never claim completion without evidence.

## Concurrent or reverted work

- Preserve other active items and their metadata.
- Prefer targeted additions over restructuring shared sections.
- When work is partially reverted, move it back to active, state why, and retain accurate
  history.
