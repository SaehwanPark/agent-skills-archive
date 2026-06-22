---
name: fp-developer
description: Apply and enforce a functional-first development workflow with explicit state, pure core logic, typed boundaries, tests-as-specs, and language-specific guidance for Python, Rust, Swift, Kotlin, and Mojo.
---

# fp-developer

## When to use this skill

Use this skill when writing, reviewing, refactoring, or porting code toward a functional-first style.

Use it especially when the task involves:

- Separating domain logic from IO, frameworks, persistence, networking, randomness, or time.
- Making state transitions explicit and testable.
- Replacing hidden mutation with typed values and pure functions.
- Representing absence and recoverable failure with explicit types.
- Adding or updating tests as executable specifications.
- Porting logic between Python, Rust, Swift, Kotlin, Mojo, or adjacent languages.

## Core workflow

1. Identify the impure edge and pure core.
2. Read existing tests and type contracts before changing behavior.
3. Add or update focused tests before implementing new pure-core behavior.
4. Refactor toward small, typed, deterministic transformations.
5. Keep IO, randomness, time, logging, environment reads, framework calls, and concurrency orchestration at the edge.
6. Run the relevant language commands from the reference files.
7. Report what changed, what checks ran, and any remaining compromises.

## Architecture rule

Organize code as:

```text
impure edge -> pure core -> impure edge
```

The pure core contains domain logic, validation, transformations, scoring, modeling, decision rules, and state transitions.

The impure edge contains filesystem access, database calls, logging, randomness, network calls, CLI parsing, environment reads, framework adapters, UI adapters, clock access, and process orchestration.

Apply this architecture proportionally with `simple-code-writer`. Functional structure is
a means to make state, effects, and contracts clearer, not an unconditional target. Do
not introduce wrappers, domain types, pure-core boundaries, or transformation pipelines
when they add more ceremony and indirection than the concrete problem warrants. Preserve
direct, idiomatic code when its state and effects are already obvious and testable.

## Functional-first principles

### Explicit state

Prefer explicit state passing:

```text
(new_state, output) = step(old_state, input)
```

Avoid designs where method calls mutate hidden internal state or require implicit lifecycle ordering.

State should be:

- Passed as an argument.
- Returned when changed.
- Represented by typed domain structures.
- Immutable by default, with local mutation only when it is clearly justified.

### Small pure functions

A good core function:

- Has typed inputs and outputs.
- Does one thing.
- Avoids hidden dependencies.
- Does not mutate inputs.
- Does not perform IO.
- Has deterministic behavior.
- Can be tested without mocks.

### Explicit failure and absence

Represent absence and recoverable failure explicitly.

Prefer:

- `Option`, `Optional`, nullable, or `Maybe`-style values for expected absence.
- `Result`, `Either`, typed throws, sealed results, or domain error values for recoverable failure.
- Domain-specific error types when callers need recovery, reporting, or exhaustive handling.

Avoid:

- Silent `None`, `nil`, or `null` when the caller needs context.
- Unstructured exceptions as normal control flow.
- Boolean success flags without error context.
- Stringly typed error states as stable contracts.

### Types as contracts

Use types to encode domain concepts and make invalid states harder to represent.

Avoid primitive obsession at stable boundaries:

```text
user_id: str
```

Prefer domain types where useful:

```text
UserId
```

### Tests as specifications

Tests should describe expected behavior, not implementation details.

For new core behavior, write or update focused unit tests before implementation. For refactors, identify existing contract tests or add them before changing internals.

Every core function should have tests for:

- Happy path.
- Invalid input.
- Boundary cases.
- Absence or failure cases.
- State transition behavior, when applicable.

### Portability

Write logic so porting is translation, not redesign.

Prefer:

```text
config + state + input -> state + output
```

This shape maps well across Python, Rust, Swift, Kotlin, Mojo, ML workflows, and agent workflows.

## Required reference files

Before making language-specific recommendations, read the relevant reference file:

- Python: `references/python.md`
- Rust: `references/rust.md`
- Swift: `references/swift.md`
- Kotlin: `references/kotlin.md`
- Mojo: `references/mojo.md`
- Review checklist: `references/checklists.md`
- Agent review protocol: `references/review-protocol.md`
- Source notes: `references/source-notes.md`

For Mojo, check the current language docs at `https://mojolang.org/docs/` whenever syntax, ownership rules, tool commands, package layout, testing, or error semantics might have changed.

Also look at [YAML](./skill.yml) and [README](README.md) to better understand the structure.

## Final response expectations

When using this skill, summarize:

- What functional-first changes were made.
- What state or effects were made explicit.
- What tests, type checks, formatters, or linters were run.
- Any remaining non-functional compromises.
- Any follow-up refactors worth considering.
