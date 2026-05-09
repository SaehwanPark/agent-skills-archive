# Ambiguity rewrite guide

Use these rewrites to convert vague plans into operational plans.

## Validation

Vague:

Improve validation handling.

Operational:

Add validation for [specific invalid input] in [function]. Return the existing [error type] without changing the public response shape.

## Parser behavior

Vague:

Update the parser to handle malformed inputs better.

Operational:

Update [parser function] so that [specific malformed input] returns [specific error type or result] instead of [current bad behavior]. Preserve existing behavior for [valid input].

## Tests

Vague:

Add tests for the new behavior.

Operational:

Add focused tests for [case 1], [case 2], [case 3], and existing valid input [case 4].

## Refactoring

Vague:

Refactor authentication logic.

Operational:

Move [specific repeated check] into a private helper in [file]. Do not change middleware ordering, request context shape, or public auth interfaces.

## Robustness

Vague:

Make the cache more reliable.

Operational:

Invalidate [specific cache key] after [specific successful write]. Do not change cache key format, TTL, or read-through behavior.

## Performance

Vague:

Optimize the query path.

Operational:

Avoid repeated calls to [function] inside [loop] by computing [value] once before the loop. Do not change query results, ordering, pagination, or public API behavior.

## Error handling

Vague:

Handle errors better.

Operational:

When [specific dependency] returns [specific error], return [existing error type] with [existing message format]. Preserve current behavior for all other errors.

## Generated files

Vague:

Update generated output.

Operational:

Change the generator source in [file]. Regenerate [specific generated files] using [command]. Do not hand-edit generated files.
