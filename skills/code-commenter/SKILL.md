---
name: code-commenter
description: Apply code commenting guidelines to help future maintainers understand intent, rationale, assumptions, constraints, and domain context without cluttering code with mechanics.
---

# Code Commenter

Use this skill when writing new code, revising existing code, or reviewing code changes to ensure all comments and docstrings are meaningful, accurate, and aligned with standard software engineering best practices.

The core goal is to guide future maintainers (including engineers who are new to the codebase or problem domain) through the intent, rationale, assumptions, and constraints behind the code, without cluttering it with explanations of mechanics.

---

## When to Use

- Use this skill when implementing new features or refactoring modules to ensure appropriate comment density and clarity.
- Use this skill when reviewing a pull request or code diff to evaluate if the comments are accurate and explain the "why" rather than the "what".
- Use this skill to clean up obsolete inline comments, commented-out code blocks, and redundant code explanations.
- Use this skill to write high-quality public API docstrings, module-level documentation, and safety notes.

## Do Not Use This Skill When

- The task is purely configuration-based (e.g., updating CI/CD YAML files, package dependencies, or build scripts) where code commenting guidelines do not apply.
- You are strictly running static analysis/linter tools without editing or reviewing code.

## Required Inputs

- The source code files being written, modified, or reviewed.
- Context on the domain requirements, business logic constraints, and architectural decisions.
- Git diffs or pull request descriptions detailing proposed changes.

---

## Workflow

1. **Evaluate Code Quality First**: Prioritize self-explanatory code. Clean up naming, split large functions, and design clean abstractions before adding comments.
2. **Determine if a Comment is Needed**: Ask if a competent engineer new to the codebase would understand the implementation immediately, or if they would ask:
   - "Why is it implemented this way?"
   - "What assumption is being made?"
   - "What constraint drove this decision?"
3. **Write Comments for Rationale**: Draft comments focusing on the "why," domain rules, assumptions, invariants, and constraints. Do not explain mechanical code operations.
4. **Choose the Right Documentation Level**:
   - Short/simple functions: Use concise docstrings.
   - Public APIs: Document purpose, inputs, outputs, side effects, exceptions, and constraints.
   - Complex modules: Write module-level overviews describing architecture and interactions.
5. **Apply Annotations**: Use `TODO`, `FIXME`, or `NOTE` with issue numbers or ticket references where applicable.
6. **Apply Language-Specific Conventions**: Use specific syntaxes and focus areas for Python, Rust, and Mojo.
7. **Clean Up Obsolete Comments**: Remove any commented-out code blocks or outdated comments that conflict with the new behavior.

---

## Core Commenting Principles

### 1. Prefer Self-Explanatory Code
Always use clear naming, appropriate abstractions, and small focused functions first. Good code should explain **what** it does; comments should explain **why** it exists, **why** it is implemented this way, and any constraints or assumptions.

Avoid comments that merely restate what the code already expresses clearly.

### 2. Comment Rationale, Not Mechanics
Prefer:
```python
# Preserve stable ordering so downstream ranking remains deterministic.
```
Over:
```python
# Sort the list.
```

### 3. Keep Comments Accurate
Outdated comments are worse than missing comments. When code behavior changes, review nearby comments and update or delete them.

---

## What Should Be Commented

Identify and document the following areas in the implementation:

### Domain or Business Logic
Explain complex business requirements, regulatory policies, or external domain rules:
```python
# CMS reimbursement rules require grouping by billing provider,
# not rendering provider.
```

### Non-Obvious Implementation Decisions
Explain why a specific structure, traversal, or algorithm was selected:
```python
# Use breadth-first traversal to preserve dependency evaluation order.
```

### Assumptions and Invariants
Highlight preconditions or assumptions that must remain true for code safety/correctness:
```python
# Invariant:
# All timestamps have already been normalized to UTC.
```

### Tradeoffs and Constraints
Document chosen compromises, such as performance vs. memory, or intentional lack of caching:
```python
# Intentionally avoid caching here because inputs change frequently
# and cache invalidation is more expensive than recomputation.
```

### Complex Algorithms
Provide a high-level overview of the approach directly before the algorithm implementation.

### Safety-Critical or Correctness-Sensitive Code
Document safety assumptions and invariants that must be preserved to prevent bugs, crashes, or security risks.

---

## Function and Module Documentation

### Docstrings for Straightforward Functions
For short or simple functions, use a concise, single-line docstring instead of inline comments.

### Public APIs
Public-facing functions, methods, and classes must document:
- Purpose and high-level responsibility
- Inputs (types, expectations, allowed ranges)
- Outputs (returned values, types)
- Side effects (state modifications, I/O operations)
- Exceptions thrown
- Important constraints

### Complex Modules
Provide module-level documentation at the top of the file describing:
- Overall responsibilities of the module
- Architecture and design pattern overview
- Important component interactions
- Known limitations or future directions

---

## Annotations, TODOs, and Future Work

Use explicit, standard annotations for unfinished or future tasks:
- `TODO`: Unfinished implementation or future feature.
- `FIXME`: Existing bug or issue that needs correcting.
- `NOTE`: Useful context or refactoring suggestion.

Whenever possible, include references to issue trackers, design docs, ADRs, or ticket IDs.

Examples:
```python
# TODO: Support incremental refreshes.
# FIXME: This fails when duplicate IDs exist.
# NOTE: Consider moving this to the shared scheduling framework.
# TODO(#482): Replace polling with event-driven updates.
```

---

## Historical Decisions & Chronology

### No Commented-Out Code
Do not preserve deleted code through commented-out blocks. Version control handles history.

### Reference Design Records
When historical context is necessary to understand the current behavior, reference design resources:
```python
# See ADR-17 for evaluation-order rationale.
```
Avoid vague inline comparisons unless directly relevant:
```python
# We used to do X but removed it.
```

### Avoid Dates in Comments
Chronology belongs in version control. Avoid adding dates to comments unless time itself is critical to the context:
- **Temporary workarounds**:
  ```python
  # TEMP (2026-06):
  # Workaround for vendor issue #1234.
  ```
- **Migrations**:
  ```python
  # 2026-06 migration note:
  # Writes go to v2; reads support both v1 and v2.
  ```
- **Time-sensitive rules**:
  ```python
  # 2026 reimbursement policy update:
  # Apply the new coding standard.
  ```

---

## Comment Density
Optimize the volume and placement of comments. One meaningful comment before a complex block is far better than line-by-line comments describing obvious operations.

If a competent engineer can understand the code after a single careful reading, no comment is needed.

---

## Language-Specific Guidance

### Python
- Use docstrings (`"""..."""`) for modules, classes, public functions, and public methods.
- Use inline comments (`# ...`) primarily for rationale, assumptions, domain logic, and tradeoffs.
- Do not use comments as a substitute for clear naming or code decomposition.

### Rust
- Use `///` for public API documentation.
- Use `//!` for module-level or crate-level documentation.
- Use ordinary comments (`// ...`) for implementation rationale and details.
- Every non-trivial `unsafe` block **must** include a `// SAFETY:` comment describing the invariant that makes the operation sound:
  ```rust
  // SAFETY:
  // ptr is non-null and points to initialized memory for len elements.
  unsafe { ... }
  ```
- Document ownership, lifetime, concurrency, and performance assumptions when not obvious.

### Mojo
- Use docstrings for API documentation.
- Use inline comments (`# ...`) for Mojo-specific attributes:
  - Ownership assumptions and transfer semantics
  - Mutability expectations
  - Performance considerations and memory layouts
  - SIMD/GPU compilation assumptions
  - Python interoperability constraints
- Example:
  ```mojo
  # Keep this as fn rather than def to preserve ownership semantics.
  ```

---

## Validation Checklist

Before finishing the implementation or review, verify that:
1. All newly added comments explain **why** (rationale) rather than **what** (mechanics).
2. Code layout, naming, and structure are clean enough to minimize the need for comments.
3. No commented-out code blocks exist.
4. Public APIs are properly documented with their expectations, inputs, and outputs.
5. All dates in comments are restricted to allowed exceptions (migrations, temp workarounds, time-sensitive rules) and design records are referenced instead.
6. Language-specific guidelines (e.g., Rust's `// SAFETY:` comments or Mojo's ownership comments) are strictly adhered to.
