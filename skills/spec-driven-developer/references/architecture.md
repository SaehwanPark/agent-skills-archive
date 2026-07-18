# Architecture workflow

Update architecture documentation only when work changes system structure, module
ownership, control or data flow, storage, APIs, dependencies, deployment assumptions,
concurrency, or an important invariant.

Keep it high level enough that a new contributor can answer:

- What are the major components and entry points?
- What does each component own?
- How does data or control move through the system?
- Which boundaries and constraints must future changes preserve?

Prefer short explanations, ordered flows, small diagrams, and explicit constraints. Avoid
line-by-line code narration or duplicated API documentation.

When the project tracks freshness, use its convention. A lightweight convention is:

```markdown
Last Reviewed: YYYY-MM-DD
Status: Verified | Needs Review | Partially Stale
```

Mark uncertainty explicitly. Do not update a review date without checking the described
behavior against the current implementation.

Document only consequential invariants, such as forbidden dependencies, persistence or
compatibility guarantees, performance boundaries, concurrency assumptions, security
constraints, or directory ownership.
