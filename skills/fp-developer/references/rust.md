# Rust

- Use enums and exhaustive matches for closed states and newtypes for values the compiler should distinguish. Use `Option` for absence and `Result` with actionable error variants for failure. Pick `?`, a match, or combinators based on clarity and any error context callers need.
- Make ownership and borrowing match the data flow. Investigate a complicated lifetime before cloning, adding shared mutability, or using unsafe code. Keep local mutation for efficient transformations when the caller's state is unaffected.
- Use the project's Cargo workspace, feature, and toolchain settings for tests, Clippy, and formatting checks.
