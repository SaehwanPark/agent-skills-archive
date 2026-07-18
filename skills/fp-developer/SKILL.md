---
name: fp-developer
description: Use when designing, implementing, refactoring, or reviewing Python, Rust, Swift, Kotlin, or Mojo code that benefits from explicit state, a pure functional core, typed boundaries, controlled effects, and tests as behavioral specifications.
---

# Functional-First Developer

Use functional techniques where they reduce hidden state and make behavior easier to
reason about. Do not force immutability, monadic abstractions, or pipelines when direct
imperative code is clearer and equally safe.

## Core workflow

1. Identify inputs, outputs, state, effects, failure, absence, and important invariants.
2. Establish the existing public contract from types, callers, tests, and documentation.
3. Separate domain transformations from I/O, time, randomness, storage, UI, and network
   adapters where that creates a real testable boundary.
4. Make state transitions explicit in arguments and return values when practical.
5. Model meaningful domain states and failures with the language's native type system.
6. Keep pure functions small enough to test directly; test effectful adapters separately.
7. Verify behavior, types, failure paths, and the repository's standard checks.

Prefer this shape when it fits the domain:

```text
config + state + input -> state + output
```

## Design rules

- Keep effects at explicit boundaries; inject time, randomness, configuration, and clients
  when deterministic behavior matters.
- Prefer returned state over hidden mutation, but allow localized mutation when it is
  clearer or materially more efficient.
- Represent absence and recoverable failure explicitly using the language's established
  `Option`/`Optional`, `Result`, sealed type, exception, or equivalent convention.
- Use types to encode stable domain concepts and prevent invalid states when the added
  structure pays for itself.
- Prefer readable named transformations over dense chains or custom combinator libraries.
- Preserve public APIs during refactors unless change is explicitly requested.
- Add dependencies or abstractions only for a current, demonstrated requirement.

## Reference routing

Read only the language guide relevant to the changed code:

- [Python](references/python.md)
- [Rust](references/rust.md)
- [Swift](references/swift.md)
- [Kotlin](references/kotlin.md)
- [Mojo](references/mojo.md)

For Mojo, verify current syntax, ownership, package, test, and tool behavior against the
current official documentation before relying on memory.

Use [the implementation checklist](references/checklists.md) before finalizing substantial
work. Use [the review protocol](references/review-protocol.md) and
[review summary template](examples/review-summary-template.md) only for an explicit
functional-first review. Consult [source notes](references/source-notes.md) only when
maintaining the guidance itself.

## Stop conditions

Stop and report when:

- Functional restructuring would change a public contract or performance characteristic
  outside the agreed scope.
- The repository's established architecture uses a different sound state/effect boundary.
- A proposed type, abstraction, or dependency adds more complexity than the failure mode
  it prevents.
- Required language or tool behavior cannot be verified.

## Expected output

Report the state or effects made explicit, tests and checks run, public behavior preserved
or intentionally changed, and any remaining non-functional compromises.
