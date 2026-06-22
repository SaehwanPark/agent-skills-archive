---
name: code-reviewer
description: Review working-branch code changes for bugs, security, performance, maintainability, and edge cases with severity-ranked findings.
---

# Code Reviewer

## When to Use

- Use this skill when reviewing a diff, a working branch, a PR, or any proposed code change that needs a senior-engineer critique.
- Use it when the user wants a blunt review focused on correctness and production risk.
- Do not use it as a substitute for implementation, tests, or static analysis.

## Required Inputs

- Current diff or changed files
- Relevant source files and nearby context
- Test output, if available
- Any stated scope or risk areas from the user

## Workflow

1. Read the diff first, then inspect the surrounding code paths that the diff depends on.
2. Review for bugs, security issues, performance regressions, maintainability problems, and edge cases.
3. Treat changed code as suspect until the surrounding invariants prove it safe.
4. Prefer concrete failures over style opinions; if a concern is hypothetical, state the condition that would trigger it.
5. Apply `simple-code-writer` when evaluating complexity. Report an abstraction,
   dependency, indirection, or generalization only when it creates a concrete correctness,
   maintenance, performance, or operational cost; do not report simplicity preferences as
   defects.
6. Recommend the smallest safe correction that addresses the demonstrated problem.
7. Assign one severity per finding: `Critical`, `High`, `Medium`, or `Low`.
8. For every finding, include the file and line number or the relevant section, what is wrong, and how to fix it.
9. Separate blocking correctness issues from lower-risk cleanup items.
10. If no actionable issues are found, say so explicitly and note any residual test or coverage gaps.

## Review Checklist

- Bugs: logic errors, off-by-one mistakes, null or `None` handling, race conditions, state desynchronization.
- Security: injection risks, authorization mistakes, data exposure, secret handling, unsafe deserialization.
- Performance: unnecessary loops, repeated work, N+1 patterns, unbounded memory growth, hot-path allocations.
- Maintainability: ambiguous naming, duplicated logic, excessive complexity, poor separation of concerns, brittle abstractions.
- Edge cases: empty input, large input, malformed input, concurrency, retries, partial failure, and backward compatibility.

## Output Format

- Start with findings ordered by severity, highest first.
- Use a compact, direct format for each finding:
  - `Severity`
  - `File:line` or section
  - `What is wrong`
  - `How to fix it`
- If there are no findings, state `No actionable issues found.`
- Keep summaries short. The findings are the deliverable.

## Validation

- Verify every reported issue is grounded in code or surrounding behavior, not guesswork.
- Verify line references or sections are specific enough to act on.
- Verify the review does not dilute severity by mixing major defects with cosmetic comments.
