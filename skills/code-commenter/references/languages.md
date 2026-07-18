# Language-specific comment guidance

Read only the section for the language being changed and defer to repository conventions.

## Python

- Use docstrings for public modules, classes, functions, and non-obvious contracts.
- Follow the established docstring style rather than introducing a second one.
- Use inline comments for rationale or invariants local to an expression or block.

## Rust

- Use `///` for public items and `//!` for module or crate documentation.
- Document panics, safety contracts, ownership surprises, and externally visible errors.
- Every `unsafe` block needs a nearby explanation of the invariant that makes it sound.

## Mojo

- Follow the repository's current documentation convention and verify syntax against the
  current Mojo documentation when it may have changed.
- Explain ownership, transfer, aliasing, or accelerator constraints only when they are not
  evident from the types and API.
