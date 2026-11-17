---
name: code-commenter
description: Use when adding or reviewing code comments and docstrings for non-obvious rationale, invariants, constraints, or public contracts.
---

# Code Commenter

- Read the surrounding implementation and callers. Explain why a decision exists, which invariant it protects, or which external rule governs it. Put the comment beside the code that depends on it.
- Document externally relevant inputs, outputs, errors, side effects, ownership, and safety in the project's API documentation format. Link to the canonical design record or standard where it supplies context.
- Remove stale comments, dead commented-out code, and descriptions that merely repeat mechanics. Use actionable TODOs and issue links where the project uses them.
- Check claims against the relevant success and failure paths. Flag behavior that cannot be established from available evidence.

See [comment examples](references/patterns.md) for placement and [language conventions](references/languages.md) for Python, Rust, and Mojo.
