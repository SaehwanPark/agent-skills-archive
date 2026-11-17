---
name: simple-code-writer
description: Use when implementing or refactoring code with the smallest correct change, existing capabilities, and focused verification.
---

# Simple Code Writer

- Establish the requested behavior and existing contracts from nearby code, callers, and tests.
- Use an existing boundary, platform feature, standard library, or dependency when it fits. Keep the diff focused and preserve public behavior outside the requested change.
- Add a helper or type when it names a stable concept, removes meaningful duplication, or enforces a real invariant. Keep control flow, state, ownership, and failure handling visible. Tie performance work to evidence or an explicit constraint.
- When refactoring, add characterization coverage if an important contract is otherwise unprotected. Run the checks that exercise the changed behavior and report any verification gaps.
