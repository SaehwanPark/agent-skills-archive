# Mojo functional-first guidance

## Documentation freshness rule

Mojo is evolving quickly. Before writing or reviewing Mojo code, consult the current docs at `https://mojolang.org/docs/` whenever syntax, ownership, lifetimes, testing, packaging, Python interop, or error behavior matters.

Do not rely only on memory for Mojo-specific syntax. Prefer the Mojo Manual, Language Reference, standard library docs, and official Mojo AI skills when available.

## Recommended tooling

Use the repository's existing Mojo or Modular setup. When starting or validating a Mojo project, prefer the current official workflow, currently centered on `pixi` and the `mojo` package.

Typical commands to discover or run in an existing project:

```bash
pixi run mojo --version
pixi run mojo format .
pixi run mojo test
pixi run mojo package .
```

Command names and package layout may change; check the current docs before adding workflow instructions.

## Rules

### Model domains with structs and traits

Use `struct` for nominal domain types and traits for shared behavior. Avoid passing loosely related primitive values through stable APIs.

Prefer small data-first structs whose methods are thin and whose core logic can also be tested as pure functions.

```mojo
@fieldwise_init
struct Accumulator(Copyable, Movable):
  var total: Int

fn add(value: Int, accumulator: Accumulator) -> Accumulator:
  return Accumulator(accumulator.total + value)
```

Use traits to express required behavior when generic code needs a contract. Avoid using traits as a place to hide side effects.

### Make ownership and mutation explicit

Mojo has an ownership system. Treat ownership annotations and argument conventions as part of the functional contract.

Prefer function signatures that show whether values are read, mutated, copied, moved, or returned as updated state.

Guidelines:

- Prefer read-only argument passing for pure transformations.
- Return updated values instead of mutating shared state.
- Use local mutation only when it improves clarity or performance and does not escape the function.
- Avoid global mutable state.
- Avoid pointer-based designs unless the domain genuinely requires them.
- Document any destructor/resource invariants for types that manage external resources.

### Use explicit state transitions

Prefer pure transition functions:

```mojo
fn step(state: ModelState, input: Input) -> ModelStep:
  ...
```

When multiple values must be returned, use a named result struct rather than a tuple blob if the values are part of a stable boundary.

```mojo
@fieldwise_init
struct ModelStep(Copyable, Movable):
  var state: ModelState
  var output: Output
```

### Represent absence and failure deliberately

Use optional or result-like patterns when absence and recoverable failure are expected. For public domain contracts, prefer structured error or result values over string-only errors when callers need to branch or recover.

Mojo also supports error raising and handling. Keep raised errors at effect boundaries or in APIs where that is the idiomatic project convention. For pure core workflows, prefer values that make failure cases visible to tests and callers.

When using Mojo typed errors, model domain errors as structs, enumerated error types, variants, or project-standard result types. Keep error paths covered by tests.

### Keep effects at the edge

Bad:

```mojo
fn compute_score(path: String) raises -> Score:
  let raw = read_file(path)
  ...
```

Good:

```mojo
fn compute_score(input: Input) -> Score:
  ...

fn load_input(path: String) raises -> Input:
  ...
```

Read files, call Python, allocate external resources, log, access environment values, and launch device/parallel work at the adapter edge. Pass plain values into the core.

### Be careful with Python interop

Python interop is an effect boundary. Treat Python calls as impure unless proven otherwise.

- Convert Python values into typed Mojo domain values before core logic.
- Keep Python exceptions and dynamic types out of stable pure-core APIs.
- Do not let Python objects become hidden global state.

### Treat GPU and parallel execution as explicit boundaries

For GPU kernels, layout tensors, or parallel execution:

- Keep scheduling, memory transfer, device selection, and synchronization at the edge.
- Keep scalar domain calculations and validation pure when possible.
- Make shapes, layouts, and compile-time parameters explicit in types or function parameters.
- Test CPU-equivalent pure transformations when practical.

### Prefer current syntax over guessed syntax

When a Mojo example is more than trivial, verify:

- Declaration keywords and function signatures.
- Struct initialization syntax.
- Trait conformance syntax.
- Argument conventions, references, origins, and lifetimes.
- Error syntax and typed errors.
- Testing commands and package layout.

If unsure, state that the code is a pattern sketch and point to the docs requirement rather than pretending it is guaranteed to compile.

## Commands

Use the project's configured commands. When no project convention exists, check the current Mojo docs and then run the closest available commands for:

```bash
pixi run mojo format .
pixi run mojo test
pixi run mojo package .
```
