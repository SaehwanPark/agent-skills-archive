# Kotlin

- Use data classes for values and sealed interfaces for states callers must handle exhaustively. A `val` prevents reassignment and a read-only collection interface can still wrap a mutable collection. Avoid leaking aliases across domain boundaries.
- Use nullable types for expected absence and a sealed outcome for typed recovery. Keep coroutine scope ownership at service or application boundaries and propagate `CancellationException` when translating failures, including around `runCatching`.
- Use the repository's Gradle wrapper and configured target test tasks. When using `kotlinx.coroutines.test.runTest`, use test dispatchers that share its scheduler for virtual time and return the test result directly in multiplatform tests.
