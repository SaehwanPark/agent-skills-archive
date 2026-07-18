# Task-specific guidance

## Development continuation

- Recover the latest branch, checkpoint, spec, or PR rather than reconstructing state from
  memory.
- Separate complete, partial, and remaining work.
- Select the next thin slice and preserve later work explicitly.

## Feature or bug fix

- Turn the request into observable acceptance criteria.
- Add focused failing tests first when they accurately express the new behavior.
- Keep the implementation bounded; do not convert a local feature or fix into a redesign.

## Behavior-preserving refactor

- Establish the contract from public interfaces, callers, and tests.
- Add characterization coverage when important behavior is unprotected.
- Prefer local simplification and stop if the work becomes a redesign.

For every type, implement a complete slice, use the narrowest useful validation, and
report unrelated failures without absorbing them into scope.
