# Swift functional-first guidance

## Contents

- Recommended tooling
- Rules: value types, domains, absence, failure, effects, concurrency, and tests
- Commands

## Recommended tooling

Use:

- Swift Package Manager for build, test, run, and dependency workflows.
- Swift Testing for new tests where the supported platform and toolchain allow it.
- XCTest for existing projects, Apple-platform integration tests, or compatibility needs.
- `swift-format` for formatting and linting when adopted by the repository.
- Swift 6 language mode and strict concurrency checking where practical.
- `Optional`, `Result`, domain `struct`, `enum`, `actor`, and protocol types.

Prefer the repository's existing Xcode or SwiftPM layout. Do not add third-party functional libraries unless the project already uses them or the gain is clear.

## Rules

### Prefer value types and immutability

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

### Model domains explicitly

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

### Use Optional for absence

Use `Optional` only when absence is expected and not itself an error.

```swift
func findUser(id: UserID, users: [User]) -> User? {
  users.first { $0.id == id }
}
```

Do not use `nil` to hide validation failures, authorization failures, or parse errors that the caller needs to distinguish.

### Use Result or typed throws for recoverable failure

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

### Keep effects at the edge

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

### Treat concurrency as an explicit boundary

Prefer structured concurrency with `async`/`await`, `TaskGroup`, and actors at effect boundaries.

- Do not create detached tasks from pure core logic.
- Do not hide mutable shared state behind classes when an `actor` or explicit state transition would be clearer.
- Mark cross-concurrency domain values as `Sendable` where appropriate.
- Keep `@MainActor` and UI isolation at the adapter edge.
- Avoid `@unchecked Sendable` unless there is a documented invariant and a focused test or review reason.

### Tests

Use Swift Testing for new pure-core tests when available.

```swift
import Testing

@Test func addReturnsUpdatedAccumulator() {
  let oldState = Accumulator(total: 1)
  let newState = add(2, to: oldState)

  #expect(newState == Accumulator(total: 3))
}
```

Use XCTest when required by the project or platform constraints. Keep tests deterministic. Avoid global state because Swift Testing may run tests concurrently unless configured otherwise.

## Commands

Run before finalizing when configured:

```bash
swift format --in-place --recursive Sources Tests
swift format lint --recursive Sources Tests
swift build
swift test
```

For Xcode projects, use the repository's configured `xcodebuild test` command. If Swift 6 migration is in progress, run the configured build with strict concurrency diagnostics enabled and report remaining warnings clearly.
