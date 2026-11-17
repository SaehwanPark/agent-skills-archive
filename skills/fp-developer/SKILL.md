---
name: fp-developer
description: Use when designing, implementing, or reviewing Python, Rust, Swift, Kotlin, or Mojo code that benefits from a testable functional core and explicit state, effects, or failure.
---

# Functional-First Developer

- Identify the existing contract, state transitions, effects, and failure modes. Extract deterministic domain logic from I/O, time, randomness, and concurrency when the boundary makes behavior easier to verify.
- Pass the state and inputs a computation needs explicitly. Return meaningful outputs or state transitions. Use native types for domain invariants, absence, and recoverable failures where callers benefit.
- Prefer clear local mutation when it improves readability or performance without leaking state. Add dependencies, wrappers, and composition abstractions only when they solve a current problem.
- Test core behavior directly and exercise adapters at the boundaries that can fail. Preserve existing contracts unless the task changes them.

For language-specific tradeoffs, load the relevant guide only: [Python](references/python.md), [Rust](references/rust.md), [Swift](references/swift.md), [Kotlin](references/kotlin.md), or [Mojo](references/mojo.md).
