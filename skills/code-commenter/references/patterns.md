# Comment patterns

## Comment when knowledge would be lost

Useful subjects include:

- A business or regulatory rule that explains an otherwise surprising calculation.
- An ordering or algorithm choice required for determinism or correctness.
- A precondition not expressible in the type system.
- A deliberate tradeoff, such as avoiding a cache because invalidation costs dominate.
- Correctness-sensitive concurrency, numerical, serialization, or security behavior.

Prefer:

```python
# Group by billing provider because reimbursement is calculated at that boundary.
```

Avoid:

```python
# Group the records by provider.
```

## Prefer a design record for history

Use a short reference such as `See ADR-17 for evaluation-order rationale` when the full
decision belongs outside the code. Do not narrate who changed the code or when.

## Use annotations sparingly

- `TODO`: specific unfinished work.
- `FIXME`: a known defect with an actionable correction.
- `NOTE`: a durable, non-obvious fact that does not fit more naturally elsewhere.

Avoid vague notes such as “improve later.” Link to a tracked item when the repository uses
one.
