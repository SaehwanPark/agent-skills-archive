---
name: fp-developer
description: Apply and enforce a functional-first development workflow with explicit state, pure core logic, typed boundaries, tests-as-specs, and Python, Rust, Swift, and Kotlin tooling.
---

# fp-developer

## Purpose

Use this skill when writing, reviewing, refactoring, or porting code toward a functional-first style.

Primary goals:

- Make state explicit.
- Keep core logic pure.
- Isolate side effects.
- Use types and tests as contracts.
- Prefer composable functions over hidden orchestration.
- Make code easier for agents and humans to reason about.
- Make cross-language porting safer.

---

# Part 1: General Principles

## Core Architecture

Organize code into:

```text
impure edge -> pure core -> impure edge
```

The pure core should contain domain logic, validation, transformations, scoring, modeling, and decision rules.

The impure edge should contain IO, filesystem access, database calls, logging, randomness, network calls, CLI parsing, environment reads, and framework adapters.

## State

Prefer explicit state passing.

Do:

```text
(new_state, output) = step(old_state, input)
```

Avoid:

```text
object.step(input) mutates hidden internal state
```

State should be:

* Passed as an argument
* Returned when changed
* Represented by typed domain structures
* Kept immutable unless mutation is locally justified

## Functions

Prefer small pure functions.

A good function:

* Has typed inputs and outputs
* Does one thing
* Avoids hidden dependencies
* Does not mutate inputs
* Does not perform IO
* Has deterministic behavior

## Failure and Absence

Represent absence and failure explicitly.

Prefer:

* `Option` / `Maybe` for absence
* `Result` / `Either` for recoverable failure
* Domain-specific error types

Avoid:

* Silent `None`
* Unstructured exceptions as normal control flow
* Boolean success flags without error context
* Stringly typed error states

## Types as Contracts

Use types to encode domain concepts.

Avoid primitive obsession:

```text
user_id: str
```

Prefer domain types where useful:

```text
UserId
```

Use types to make invalid states harder to represent.

## Tests as Specifications

Tests should describe expected behavior, not implementation details.

Treat unit tests as executable contracts. For new core behavior, write or update the focused unit tests before implementing the function. For refactors, first identify the existing contract tests or add them before changing internals.

Every core function should have tests for:

* Happy path
* Invalid input
* Boundary cases
* Absence/failure cases
* State transition behavior, if applicable

For agent work, tests act as executable specs. Do not make broad refactors or introduce new pure-core functions without first understanding or adding tests that lock the intended behavior.

## Portability

Write logic so that porting is translation, not redesign.

Prefer:

```text
config + state + input -> state + output
```

This structure maps well across Python, Rust, ML frameworks, and agent workflows.

---

# Part 2: Lint-Style Checklist

Use this checklist before finalizing any implementation, review, or refactor.

## A. State Checklist

* [ ] Is all required state visible in function signatures?
* [ ] Are state transitions represented as returned values?
* [ ] Are hidden mutable fields avoided?
* [ ] Are globals avoided?
* [ ] Is mutation either eliminated or tightly scoped?
* [ ] Could another agent understand the current state flow from signatures alone?

Red flags:

* Hidden caches
* Implicit lifecycle requirements
* Order-dependent method calls
* Mutable default arguments
* Shared mutable objects
* “Call `init()` before `run()`” protocols

## B. Purity Checklist

* [ ] Is domain logic free of IO?
* [ ] Is randomness injected rather than generated inside core logic?
* [ ] Is time injected rather than read inside core logic?
* [ ] Are logs/metrics emitted at the edge instead of inside core functions?
* [ ] Can the function be tested without mocks?

Red flags:

* Core function reads files
* Core function calls APIs
* Core function accesses environment variables
* Core function mutates external objects
* Core function depends on wall-clock time

## C. Type Checklist

* [ ] Are all public functions typed?
* [ ] Are domain concepts modeled explicitly?
* [ ] Are raw dicts avoided across stable boundaries?
* [ ] Are `None`/null cases reflected in the type?
* [ ] Are recoverable errors reflected in the return type?
* [ ] Are invalid states difficult or impossible to construct?

Red flags:

* `Any`
* Loose dictionaries
* Tuple blobs
* Stringly typed states
* Boolean flags with unclear meaning
* Unvalidated external input

## D. Error Handling Checklist

* [ ] Is absence represented explicitly?
* [ ] Is failure represented explicitly?
* [ ] Are errors typed or structured?
* [ ] Are exceptions reserved for exceptional or boundary failures?
* [ ] Are error cases tested?
* [ ] Does the caller have enough information to recover or report?

Red flags:

* `return None` without explanation
* `except Exception: pass`
* Raising generic exceptions from domain logic
* Encoding errors as strings only
* Losing original error context

## E. Composition Checklist

* [ ] Is the code organized as transformations?
* [ ] Are functions easy to compose?
* [ ] Are intermediate values named clearly?
* [ ] Is branching localized and explicit?
* [ ] Are pipelines readable without hidden side effects?

Red flags:

* Large orchestration methods
* Deeply nested conditionals
* Mixed validation/transformation/IO
* Functions that both compute and persist
* Objects that accumulate unrelated responsibilities

## F. Testing Checklist

* [ ] Do tests define expected behavior?
* [ ] Are pure functions tested directly?
* [ ] Are edge adapters tested separately?
* [ ] Are failure/absence paths tested?
* [ ] Are property-style tests considered for transformations?
* [ ] Can tests serve as porting specs?

Red flags:

* Only integration tests
* Tests require external services
* Tests depend on execution order
* Tests assert implementation details
* No tests for invalid inputs

## G. Agent-Friendliness Checklist

* [ ] Can the agent infer behavior from types, tests, and function names?
* [ ] Is the design documented in markdown-friendly rules?
* [ ] Are invariants explicit?
* [ ] Are side effects isolated?
* [ ] Are functions small enough for targeted edits?
* [ ] Is there a clear boundary between “change this logic” and “do not touch this adapter”?

Red flags:

* Hidden framework magic
* Implicit conventions
* Large classes with many responsibilities
* Scattered state mutation
* Behavior only explained in comments, not types/tests

---

# Part 3: Python Setup

## Recommended Tooling

Use:

* `pyright` for static type checking
* `pydantic` for validated boundary models
* `comp-builders` for explicit absence, recoverable failure, validation, async failure flows, and computational expressions
* `pytest` for tests

Prefer installing `comp-builders` directly from GitHub with `uv`:

```bash
uv add git+https://github.com/SaehwanPark/comp-builders.git
```

Prefer `comp-builders` when adding a dependency is acceptable. Use lightweight local `Option` / `Result` helpers only for tiny projects, dependency-sensitive code, or repositories that already have a local convention.

Prefer project-local Pyright configuration in `pyproject.toml` or `pyrightconfig.json`. Use strict checking where practical, and avoid weakening type guarantees to silence errors. If a repository cannot be fully strict yet, scope ignores narrowly and document why they are temporary.

## Python Rules

### Type Everything Public

All public functions must have full type annotations.

Avoid:

```python
def process(x):
  ...
```

Prefer:

```python
def process(input: Input) -> Output:
  ...
```

### Use Pydantic at Boundaries

Use Pydantic models for external inputs, configs, and serialized data.

```python
from pydantic import BaseModel

class TrainConfig(BaseModel):
  learning_rate: float
  batch_size: int
  seed: int
```

Do not pass raw external dictionaries deep into core logic.

### Prefer Frozen Domain Models

Prefer immutable models where practical.

```python
from pydantic import BaseModel, ConfigDict

class ModelState(BaseModel):
  model_config = ConfigDict(frozen=True)

  step: int
  loss: float
```

### Avoid Hidden Mutation

Avoid mutating inputs.

Bad:

```python
def add_item(items: list[str], item: str) -> None:
  items.append(item)
```

Good:

```python
def add_item(items: tuple[str, ...], item: str) -> tuple[str, ...]:
  return (*items, item)
```

### Represent Failure Explicitly

Use `Optional` only for true absence.

Prefer `comp-builders` values for absence, recoverable failure, validation, and composable pipelines when they clarify the data flow.

Prefer:

* `Option` for expected absence
* `Result` for recoverable failure where the workflow should stop on the first error
* `Validation` for independent checks where accumulated errors are more useful than fail-fast behavior
* `AsyncResult` for async workflows that should return explicit success or failure values
* `map`, bind/then-style composition, computational expression blocks, and pure transformation pipelines

Avoid deeply nested conditionals or exception-driven control flow for expected domain failures.

Keep these values in the pure/domain layer where they clarify composition. Convert at impure edges when frameworks, serializers, or external APIs expect plain Python values.

When using `comp-builders`, keep generator blocks short and readable. Use the block to express orchestration, but keep individual steps as normal typed functions that return `Result`, `Option`, `Validation`, or `AsyncResult`.

```python
from comp_builders import Err, Ok, Result, result

def parse_user_id(raw: str) -> Result[int, str]:
  try:
    return Ok(int(raw))
  except ValueError:
    return Err("user_id must be an integer")

def require_positive(user_id: int) -> Result[int, str]:
  if user_id <= 0:
    return Err("user_id must be positive")
  return Ok(user_id)

@result.block
def load_user_input(raw: str) -> Result[int, str]:
  user_id = yield parse_user_id(raw)
  return yield require_positive(user_id)
```

Use `Option` when absence is expected and not itself an error.

```python
from comp_builders import Nothing, Option, Some, option

def first_item(items: tuple[str, ...]) -> Option[str]:
  if not items:
    return Nothing
  return Some(items[0])

@option.block
def normalized_first_item(items: tuple[str, ...]) -> Option[str]:
  item = yield first_item(items)
  cleaned = item.strip()
  if not cleaned:
    return Nothing
  return cleaned
```

Use `Validation` when several checks can run independently and the caller benefits from all errors at once.

```python
from comp_builders import Invalid, Validation, Valid, validation

def validate_name(name: str) -> Validation[str, str]:
  if not name.strip():
    return Invalid("name is required")
  return Valid(name.strip())

def validate_age(age: int) -> Validation[int, str]:
  if age < 0:
    return Invalid("age must be non-negative")
  return Valid(age)

@validation.block
def validate_profile(name: str, age: int) -> Validation[tuple[str, int], str]:
  valid_name = yield validate_name(name)
  valid_age = yield validate_age(age)
  return (valid_name, valid_age)
```

Do not use computational expression builders to hide IO inside the pure core. For example, read files, call APIs, emit logs, and access environment variables at the edge; then pass plain inputs into pure functions that return explicit values.

Pyright may need generator return annotations, local `typing.cast` calls, or small helper functions around yielded values in larger workflows. Keep those annotations local to the block rather than weakening the public function type or introducing `Any`.

If `comp-builders` is not appropriate for a project, define only the minimal local dataclasses or classes needed for that codebase instead of building a general-purpose monad library.

### Keep Core Logic Mock-Free

If a function requires mocks to test, it probably contains effects. Move those effects outward.

Preferred shape:

```python
def compute_metrics(predictions: Predictions, labels: Labels) -> Metrics:
  ...

def load_predictions(path: Path) -> Predictions:
  ...
```

### Python Commands

Run before finalizing:

```bash
uvx pyright
uvx pytest
```
(parameters might vary depending on codebase directory structures)

When available, also run the project’s formatter/linter.

---

# Part 4: Rust Setup

## Recommended Tooling

Use:

* `cargo test`
* `cargo clippy`
* `cargo fmt`
* `Option`
* `Result`
* Domain `struct` and `enum` types

## Rust Rules

### Prefer Immutable Bindings

Default to:

```rust
let value = compute(input);
```

Use `mut` only when it materially improves clarity or performance.

### Model Domains Explicitly

Avoid primitive obsession.

Bad:

```rust
fn train(model_type: String, status: String) {}
```

Good:

```rust
enum ModelType {
  Transformer,
  Linear,
}

enum TrainingStatus {
  Pending,
  Running,
  Finished,
  Failed,
}
```

### Use `Option` for Absence

```rust
fn find_user(id: UserId, users: &[User]) -> Option<User> {
  users.iter().find(|user| user.id == id).cloned()
}
```

### Use `Result` for Recoverable Failure

```rust
fn parse_config(raw: &str) -> Result<Config, ConfigError> {
  ...
}
```

Prefer domain-specific error enums.

### Compose with `map` and `and_then`

```rust
fn process(raw: &str) -> Result<Output, Error> {
  parse(raw)
    .and_then(validate)
    .map(transform)
}
```

### Keep IO at the Edge

Bad:

```rust
fn compute_score(path: &Path) -> Result<Score, Error> {
  let raw = std::fs::read_to_string(path)?;
  ...
}
```

Good:

```rust
fn compute_score(input: &Input) -> Score {
  ...
}

fn load_input(path: &Path) -> Result<Input, Error> {
  ...
}
```

### Avoid Fighting the Borrow Checker

If lifetimes become complex, revisit the data flow.

Prefer:

* Clear ownership
* Small structs
* Explicit state passing
* Owned domain values where appropriate

Do not introduce unsafe code to preserve an unnecessarily stateful design.

### Rust Commands

Run before finalizing:

```bash
cargo fmt
cargo clippy -- -D warnings
cargo test
```


---

# Part 5: Swift Setup

## Recommended Tooling

Use:

* Swift Package Manager for package build, test, run, and dependency workflows
* Swift Testing for new tests where the supported platform and toolchain allow it
* XCTest for existing projects, Apple-platform integration tests, or compatibility needs
* `swift-format` for formatting and linting when adopted by the repository
* Swift 6 language mode and strict concurrency checking where practical
* `Optional`, `Result`, domain `struct`, `enum`, `actor`, and protocol types

Prefer the repository's existing Xcode or SwiftPM layout. Do not add third-party functional libraries unless the project already uses them or the gain is clear.

## Swift Rules

### Prefer Value Types and Immutability

Default to `let`, `struct`, and pure transformations.

Bad:

```swift
final class Accumulator {
  var total: Int = 0

  func add(_ value: Int) {
    total += value
  }
}
```

Good:

```swift
struct Accumulator: Sendable, Equatable {
  let total: Int
}

func add(_ value: Int, to accumulator: Accumulator) -> Accumulator {
  Accumulator(total: accumulator.total + value)
}
```

Use `var` only for local, tightly scoped mutation that improves clarity or performance.

### Model Domains Explicitly

Avoid primitive obsession.

Bad:

```swift
func train(modelType: String, status: String) {}
```

Good:

```swift
enum ModelType: Sendable {
  case transformer
  case linear
}

enum TrainingStatus: Sendable {
  case pending
  case running
  case finished
  case failed(TrainingError)
}
```

Prefer `struct` and `enum` domain models that conform to `Sendable`, `Equatable`, `Hashable`, `Codable`, or `Identifiable` only when those contracts are meaningful.

### Use Optional for Absence

Use `Optional` only when absence is expected and not itself an error.

```swift
func findUser(id: UserID, users: [User]) -> User? {
  users.first { $0.id == id }
}
```

Do not use `nil` to hide validation failures, authorization failures, or parse errors that the caller needs to distinguish.

### Use Result or Typed Throws for Recoverable Failure

For synchronous pure core logic, prefer explicit domain errors.

```swift
enum ConfigError: Error, Equatable, Sendable {
  case missingField(String)
  case invalidPort(Int)
}

func parseConfig(_ raw: RawConfig) -> Result<Config, ConfigError> {
  ...
}
```

Use `throws` where it matches Swift API conventions or integrates better with existing call sites. Keep thrown errors domain-specific and tested.

### Keep Effects at the Edge

Bad:

```swift
func computeScore(path: URL) throws -> Score {
  let data = try Data(contentsOf: path)
  ...
}
```

Good:

```swift
func computeScore(input: Input) -> Score {
  ...
}

func loadInput(from path: URL) throws -> Input {
  ...
}
```

Read files, call services, access environment values, and emit logs at the edge. Pass plain values into the core.

### Treat Concurrency as an Explicit Boundary

Prefer structured concurrency with `async`/`await`, `TaskGroup`, and actors at effect boundaries.

* Do not create detached tasks from pure core logic.
* Do not hide mutable shared state behind classes when an `actor` or explicit state transition would be clearer.
* Mark cross-concurrency domain values as `Sendable` where appropriate.
* Keep `@MainActor` and UI isolation at the adapter edge.
* Avoid `@unchecked Sendable` unless there is a documented invariant and a focused test or review reason.

### Swift Tests

Use Swift Testing for new pure-core tests when available.

```swift
import Testing

@Test func addReturnsUpdatedAccumulator() {
  let oldState = Accumulator(total: 1)
  let newState = add(2, to: oldState)

  #expect(newState == Accumulator(total: 3))
}
```

Use XCTest when required by the project or platform constraints.

Keep tests deterministic. Avoid global state because Swift Testing may run tests concurrently unless configured otherwise.

### Swift Commands

Run before finalizing:

```bash
swift format --in-place --recursive Sources Tests
swift format lint --recursive Sources Tests
swift build
swift test
```

For Xcode projects, use the repository's configured `xcodebuild test` command. If Swift 6 migration is in progress, run the configured build with strict concurrency diagnostics enabled and report remaining warnings clearly.

---

# Part 6: Kotlin Setup

## Recommended Tooling

Use:

* Gradle with the Kotlin Gradle plugin for build, compiler options, tests, and multiplatform targets
* Kotlin compiler warnings and explicit compiler options in the Gradle DSL
* `detekt` for static analysis and complexity checks when adopted by the repository
* `ktlint` for Kotlin formatting and style checks when adopted by the repository
* JUnit, Kotest, or the project-standard test framework
* `Result`, nullable types, sealed interfaces/classes, data classes, value classes, and immutable collections where appropriate
* `kotlinx.coroutines` structured concurrency for async workflows

Prefer the repository's existing Gradle conventions. Do not add detekt, ktlint, Kotest, Arrow, or other dependencies unless the project already uses them or the benefit is explicit.

## Kotlin Rules

### Prefer Immutable Values

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

### Model Domains Explicitly

Avoid primitive obsession.

Bad:

```kotlin
fun train(modelType: String, status: String) {}
```

Good:

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

### Use Nullable Types for Absence

Use nullable types only when absence is expected and not itself an error.

```kotlin
fun findUser(id: UserId, users: List<User>): User? =
  users.firstOrNull { it.id == id }
```

Do not return `null` for validation failures, authorization failures, or parse errors that the caller needs to distinguish.

### Use Result or Sealed Errors for Recoverable Failure

Prefer explicit domain failures.

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

### Keep Effects at the Edge

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

### Treat Coroutines as an Explicit Boundary

Prefer structured concurrency.

* Use `suspend` functions for async effects instead of blocking hidden work inside core functions.
* Keep `CoroutineScope` ownership at adapters, services, or application boundaries.
* Avoid `GlobalScope` and unstructured launched work.
* Let cancellation propagate; do not swallow `CancellationException`.
* Inject dispatchers for effectful adapters when tests need control.
* Keep pure core functions non-`suspend` unless the computation itself depends on suspendable inputs.

### Kotlin Tests

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

### Kotlin Commands

Run before finalizing:

```bash
./gradlew ktlintCheck detekt test
```

For Android projects, also run the relevant unit and instrumentation tasks configured by the repository. For multiplatform projects, run the relevant target test tasks or `allTests` when configured.

When the repository does not use ktlint or detekt, run the closest configured equivalents, usually:

```bash
./gradlew check
```

---

# Part 7: Review Protocol for Agents

When reviewing or modifying code:

1. Identify the pure core and impure edge.
2. Check whether state is explicit.
3. Check whether errors and absence are typed.
4. Check whether tests describe behavior.
5. Add or update unit tests as contracts before implementing new core behavior or refactoring internals.
6. Refactor toward small pure functions.
7. Keep adapters thin.
8. Run relevant unit tests, then type checks and broader tests where configured.
9. Report remaining violations clearly.

When proposing changes, prefer small diffs that improve one of:

* Explicit state
* Purity
* Type contracts
* Error modeling
* Testability
* Portability

Do not introduce clever abstractions unless they reduce hidden context.

---

# Part 8: Final Response Expectations

When using this skill, summarize:

* What functional-first changes were made
* What state/effects were made explicit
* What tests/type checks were run
* Any remaining non-FP compromises
* Any follow-up refactors worth considering
