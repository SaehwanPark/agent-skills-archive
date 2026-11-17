# Python

- Use annotations for public boundaries. Use dataclasses for named domain values and enums for closed state sets. A frozen dataclass prevents field reassignment but does not freeze mutable field values. Use a schema validator such as Pydantic at input boundaries when the project already uses it or needs its features.
- Return `None` for expected absence when unambiguous. Preserve exception conventions and chain causes when translating boundary errors. Use a union or the project's existing result type when callers need to branch on domain failures.
- Use project-pinned type checking and test commands. For a uv project, prefer its `uv run` checks over standalone tool installs that can select different versions or miss project dependencies.
