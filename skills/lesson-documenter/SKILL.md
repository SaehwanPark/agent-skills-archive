---
name: lesson-documenter
description: Use when setup, implementation, testing, debugging, deployment, or tooling reveals a non-obvious recurring trap whose cause, verified resolution, and prevention should be preserved for future contributors.
---

# Lesson Documenter

Record durable, verified knowledge that would save future contributors meaningful time.
Do not document routine mistakes, blame, speculation, or facts already obvious from code,
tests, and standard tooling.

## Selection criteria

Document a lesson when it is likely to recur and involves an unexpected prerequisite,
version or environment mismatch, misleading failure, dead-end diagnosis, integration
constraint, generated/cache/migration behavior, or newly discovered domain assumption.

First search existing contributor docs, `LESSONS.md`, `docs/lessons.md`, development guides,
and nearby troubleshooting material. Update the established location. If none exists and
the lesson justifies a new file, prefer root `LESSONS.md` for a small project or the
existing docs hierarchy for a larger one.

## Workflow

1. Investigate until the cause and successful resolution are supported by evidence.
2. Check for an existing lesson and update it instead of duplicating it.
3. Add the smallest useful entry with context, symptom, cause, resolution, and prevention.
4. Include exact commands, versions, paths, or links only when they materially reduce
   ambiguity and do not expose secrets or machine-specific data.
5. Verify the prevention step from a clean or representative state when practical.
6. Link to the durable source of truth rather than copying large instructions.

Suggested form:

```markdown
## Short lesson title

- Context:
- Symptom:
- Cause:
- Resolution:
- Prevention:
```

Collapse small lessons into a paragraph when the fields would add noise.

## Stop conditions

Do not publish the lesson when the cause remains speculative, the content contains secrets
or personal paths, the guidance is temporary without a clear expiry/version, or an existing
canonical document should be fixed instead.

## Expected output

Report the lesson location, verified cause and prevention, evidence used, and any remaining
uncertainty.
