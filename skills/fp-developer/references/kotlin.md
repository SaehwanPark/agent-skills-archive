# Kotlin functional-first guidance

## Contents

- Recommended tooling
- Rules: values, domains, absence, failure, effects, coroutines, and tests
- Commands

## Recommended tooling

Use:

- Gradle with the Kotlin Gradle plugin for build, compiler options, tests, and multiplatform targets.
- Kotlin compiler warnings and explicit compiler options in the Gradle DSL.
- `detekt` for static analysis and complexity checks when adopted by the repository.
- `ktlint` for formatting and style checks when adopted by the repository.
- JUnit, Kotest, or the project-standard test framework.
- `Result`, nullable types, sealed interfaces/classes, data classes, value classes, and immutable collections where appropriate.
- `kotlinx.coroutines` structured concurrency for async workflows.

Prefer the repository's existing Gradle conventions. Do not add detekt, ktlint, Kotest, Arrow, or other dependencies unless the project already uses them or the benefit is explicit.

## Rules

### Prefer immutable values

Default to `val`, data classes, and pure transformations.

Bad:

```kotlin
class Accumulator {
  var total: Int = 0

  fun add(value: Int) {
    total += value
  }
}
```

Good:

```kotlin
data class Accumulator(
  val total: Int,
)

fun add(value: Int, accumulator: Accumulator): Accumulator =
  accumulator.copy(total = accumulator.total + value)
```

Use `var` only for local, tightly scoped mutation that improves clarity or performance.

### Model domains explicitly

```kotlin
enum class ModelType {
  Transformer,
  Linear,
}

sealed interface TrainingStatus {
  data object Pending : TrainingStatus
  data object Running : TrainingStatus
  data object Finished : TrainingStatus
  data class Failed(val error: TrainingError) : TrainingStatus
}
```

Use `@JvmInline value class` for lightweight domain wrappers when they improve type safety without adding runtime overhead on the JVM.

### Use nullable types for absence

Use nullable types only when absence is expected and not itself an error.

```kotlin
fun findUser(id: UserId, users: List<User>): User? =
  users.firstOrNull { it.id == id }
```

Do not return `null` for validation failures, authorization failures, or parse errors that the caller needs to distinguish.

### Use Result or sealed errors for recoverable failure

```kotlin
sealed interface ConfigError {
  data class MissingField(val name: String) : ConfigError
  data class InvalidPort(val value: Int) : ConfigError
}

sealed interface ConfigResult {
  data class Success(val config: Config) : ConfigResult
  data class Failure(val error: ConfigError) : ConfigResult
}
```

Use Kotlin's `Result<T>` when it fits project conventions and the error type does not need to be part of the public domain contract. Use sealed result types when callers need exhaustive, typed recovery.

### Keep effects at the edge

Bad:

```kotlin
fun computeScore(path: Path): Score {
  val raw = path.readText()
  ...
}
```

Good:

```kotlin
fun computeScore(input: Input): Score =
  ...

fun loadInput(path: Path): Input =
  ...
```

Read files, call services, access environment values, launch coroutines, and emit logs at the edge. Pass plain values into the core.

### Treat coroutines as an explicit boundary

Prefer structured concurrency.

- Use `suspend` functions for async effects instead of blocking hidden work inside core functions.
- Keep `CoroutineScope` ownership at adapters, services, or application boundaries.
- Avoid `GlobalScope` and unstructured launched work.
- Let cancellation propagate; do not swallow `CancellationException`.
- Inject dispatchers for effectful adapters when tests need control.
- Keep pure core functions non-`suspend` unless the computation itself depends on suspendable inputs.

### Tests

Test pure functions directly without mocks.

```kotlin
import kotlin.test.Test
import kotlin.test.assertEquals

class AccumulatorTest {
  @Test
  fun addReturnsUpdatedAccumulator() {
    val oldState = Accumulator(total = 1)
    val newState = add(2, oldState)

    assertEquals(Accumulator(total = 3), newState)
  }
}
```

Prefer property-style tests for transformations with invariants. Keep coroutine tests deterministic with the project-standard coroutine test utilities.

## Commands

Run before finalizing when configured:

```bash
./gradlew ktlintCheck detekt test
```

For Android projects, also run relevant unit and instrumentation tasks configured by the repository. For multiplatform projects, run relevant target test tasks or `allTests` when configured.

When the repository does not use ktlint or detekt, run the closest configured equivalents, usually:

```bash
./gradlew check
```
