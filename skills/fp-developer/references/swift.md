# Swift

- Use structs and enums for value semantics and domain states. A value type that holds a mutable reference can still share state. Use optionals for absence and `throws` or `Result` for failures according to the caller's contract.
- At async boundaries, respect existing actor isolation and Sendable requirements. Use structured child tasks. Keep UI isolation where state is owned and justify any unchecked Sendable conformance with the actual synchronization invariant.
- Follow the project's SwiftPM or Xcode commands. Use Swift Testing or XCTest as supported by its toolchain. Avoid shared mutable fixtures in parallel tests. With the toolchain formatter, `swift format lint --strict` makes style violations fail the check when files or directories are supplied, using `--recursive` for directories.
