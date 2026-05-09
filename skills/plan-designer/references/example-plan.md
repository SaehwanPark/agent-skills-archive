# Example operational plan

## Task restatement

Fix stale reads after `update_user_profile` by invalidating the per-user profile cache after a successful database update.

## Current understanding

- Profile updates appear to be handled by `update_user_profile`.
- Cached reads appear to use `profile_cache`.
- Cache invalidation should happen only after a successful write.

## Assumptions

- `update_user_profile` is the only write path for this profile object.
- Cache invalidation should not happen if the database update fails.
- Existing cache key format must be preserved.

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1. Inspect `update_user_profile` and the profile read path to confirm the cache key.
2. After the database update succeeds, invalidate the existing cache entry for that user.
3. Do not change cache key format or read-through behavior.
4. Add a regression test showing initial read, successful update, and next read returning updated data.
5. Run the focused profile tests.

## Files and functions likely to change

- `src/users/profile_service.py`: add post-success cache invalidation in `update_user_profile`.
- `tests/users/test_profile_service.py`: add regression coverage for stale cache after update.

## Tests and checks

Run `pytest tests/users/test_profile_service.py`.

## Acceptance criteria

- Updated profiles are visible on the next read after a successful update.
- Failed updates do not invalidate the cache.
- Existing cache key format is unchanged.
- No unrelated user-service behavior changes.

## Non-goals

- Do not replace the cache implementation.
- Do not change cache TTLs.
- Do not refactor profile reads.
- Do not modify unrelated user tests.

## Stop conditions

Stop if:

- There are multiple profile update paths.
- Cache keys are generated in more than one incompatible way.
- The fix requires changing public API behavior.

## Review checklist

- Diff is limited to profile update and cache behavior.
- Test fails before the fix and passes after.
- No unrelated formatting or cleanup was introduced.

## Risk label

Risk: medium

Reason: Cache behavior can affect multiple read paths.
