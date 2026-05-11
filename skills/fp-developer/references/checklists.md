# Functional-first checklists

## State checklist

- [ ] Is all required state visible in function signatures?
- [ ] Are state transitions represented as returned values?
- [ ] Are hidden mutable fields avoided?
- [ ] Are globals avoided?
- [ ] Is mutation either eliminated or tightly scoped?
- [ ] Could another agent understand the current state flow from signatures alone?

Red flags: hidden caches, implicit lifecycle requirements, order-dependent method calls, mutable default arguments, shared mutable objects, and `init()`-before-`run()` protocols.

## Purity checklist

- [ ] Is domain logic free of IO?
- [ ] Is randomness injected rather than generated inside core logic?
- [ ] Is time injected rather than read inside core logic?
- [ ] Are logs and metrics emitted at the edge instead of inside core functions?
- [ ] Can the function be tested without mocks?

Red flags: core functions reading files, calling APIs, accessing environment variables, mutating external objects, or depending on wall-clock time.

## Type checklist

- [ ] Are public functions typed?
- [ ] Are domain concepts modeled explicitly?
- [ ] Are raw dictionaries or map blobs avoided across stable boundaries?
- [ ] Are absence cases reflected in the type?
- [ ] Are recoverable errors reflected in the return type or throws contract?
- [ ] Are invalid states difficult or impossible to construct?

Red flags: `Any`, loose dictionaries, tuple blobs, stringly typed states, unclear boolean flags, and unvalidated external input.

## Error-handling checklist

- [ ] Is absence represented explicitly?
- [ ] Is failure represented explicitly?
- [ ] Are errors typed or structured?
- [ ] Are exceptions reserved for exceptional or boundary failures?
- [ ] Are error cases tested?
- [ ] Does the caller have enough information to recover or report?

Red flags: unexplained `None`/`nil`/`null`, catch-all swallowing, generic exceptions from domain logic, string-only stable errors, and lost original context.

## Composition checklist

- [ ] Is the code organized as transformations?
- [ ] Are functions easy to compose?
- [ ] Are intermediate values named clearly?
- [ ] Is branching localized and explicit?
- [ ] Are pipelines readable without hidden side effects?

Red flags: large orchestration methods, deeply nested conditionals, mixed validation/transformation/IO, functions that both compute and persist, and objects accumulating unrelated responsibilities.

## Testing checklist

- [ ] Do tests define expected behavior?
- [ ] Are pure functions tested directly?
- [ ] Are edge adapters tested separately?
- [ ] Are failure and absence paths tested?
- [ ] Are property-style tests considered for transformations?
- [ ] Can tests serve as porting specs?

Red flags: only integration tests, tests requiring external services, order-dependent tests, implementation-detail assertions, and no invalid-input coverage.

## Agent-friendliness checklist

- [ ] Can an agent infer behavior from types, tests, and function names?
- [ ] Is the design documented in markdown-friendly rules?
- [ ] Are invariants explicit?
- [ ] Are side effects isolated?
- [ ] Are functions small enough for targeted edits?
- [ ] Is there a clear boundary between domain logic and adapters?

Red flags: hidden framework magic, implicit conventions, large classes with many responsibilities, scattered mutation, and behavior explained only in comments rather than types and tests.
