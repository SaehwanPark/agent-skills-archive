# Rust functional-first guidance

## Contents

- Recommended tooling
- Rules: bindings, domain types, absence, failure, composition, I/O, and borrowing
- Commands

## Recommended tooling

Use:

- `cargo test`
- `cargo clippy`
- `cargo fmt`
- `Option`
- `Result`
- Domain `struct` and `enum` types

## Rules

### Prefer immutable bindings

Default to immutable bindings.

```rust
let value = compute(input);
```

Use `mut` only when it materially improves clarity or performance.

### Model domains explicitly

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

### Use `Option` for absence

```rust
fn find_user(id: UserId, users: &[User]) -> Option<User> {
  users.iter().find(|user| user.id == id).cloned()
}
```

### Use `Result` for recoverable failure

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

### Keep IO at the edge

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

### Avoid fighting the borrow checker

If lifetimes become complex, revisit the data flow. Prefer clear ownership, small structs, explicit state passing, and owned domain values where appropriate. Do not introduce `unsafe` code to preserve an unnecessarily stateful design.

## Commands

Run before finalizing:

```bash
cargo fmt
cargo clippy -- -D warnings
cargo test
```
