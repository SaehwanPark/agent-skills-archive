# Python functional-first guidance

## Recommended tooling

Use:

- `pyright` for static type checking.
- `pydantic` for validated boundary models.
- `comp-builders` for explicit absence, recoverable failure, validation, async failure flows, and computational expressions.
- `pytest` for tests.

Prefer installing `comp-builders` directly from GitHub with `uv` when adding a dependency is acceptable:

```bash
uv add git+https://github.com/SaehwanPark/comp-builders.git
```

Use lightweight local `Option` or `Result` helpers only for tiny projects, dependency-sensitive code, or repositories that already have a local convention.

Prefer project-local Pyright configuration in `pyproject.toml` or `pyrightconfig.json`. Use strict checking where practical, and scope ignores narrowly when full strictness is not yet feasible.

## Rules

### Type public APIs

All public functions must have complete type annotations.

```python
def process(input: Input) -> Output:
  ...
```

### Validate boundaries with Pydantic

Use Pydantic models for external inputs, configs, and serialized data. Do not pass raw external dictionaries deep into core logic.

```python
from pydantic import BaseModel

class TrainConfig(BaseModel):
  learning_rate: float
  batch_size: int
  seed: int
```

### Prefer frozen domain models

```python
from pydantic import BaseModel, ConfigDict

class ModelState(BaseModel):
  model_config = ConfigDict(frozen=True)

  step: int
  loss: float
```

### Avoid hidden mutation

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

### Represent failure explicitly

Use `Optional` only for true absence. Prefer `comp-builders` values when they clarify composition:

- `Option` for expected absence.
- `Result` for fail-fast recoverable failure.
- `Validation` for independent checks where accumulated errors are useful.
- `AsyncResult` for async workflows that should return explicit success or failure values.

Keep these values in the pure/domain layer where they clarify composition. Convert at impure edges when frameworks, serializers, or external APIs expect plain Python values.

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

Do not use computational expression builders to hide IO inside the pure core. Read files, call APIs, emit logs, and access environment variables at the edge; then pass plain inputs into pure functions that return explicit values.

Pyright may need generator return annotations, local `typing.cast` calls, or small helper functions around yielded values in larger workflows. Keep those annotations local rather than weakening public types or introducing `Any`.

### Keep core logic mock-free

If a function requires mocks to test, it probably contains effects. Move those effects outward.

```python
def compute_metrics(predictions: Predictions, labels: Labels) -> Metrics:
  ...

def load_predictions(path: Path) -> Predictions:
  ...
```

## Commands

Run before finalizing when available:

```bash
uvx pyright
uvx pytest
```

Also run the project formatter and linter if configured.
