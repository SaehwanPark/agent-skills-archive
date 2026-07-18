---
name: code-reviewer
description: Use when reviewing a diff, working branch, pull request, or proposed code change for concrete correctness, security, performance, maintainability, compatibility, and edge-case risks with severity-ranked findings.
---

# Code Reviewer

Treat actionable findings as the deliverable. Do not substitute review for tests, static
analysis, or implementation.

## Required inputs

Read the complete diff, relevant surrounding source and callers, public contracts, tests
and output, repository instructions, and the stated task scope. If essential context is
unavailable, narrow the review and disclose the limitation.

## Workflow

1. Establish the intended behavior and invariants before judging the change.
2. Trace changed values through success, failure, cleanup, and compatibility paths.
3. Check authorization, data exposure, injection, secret handling, concurrency, resource
   ownership, error propagation, boundary inputs, and performance where relevant.
4. Report only concerns grounded in code and a plausible triggering condition. Do not
   report style preferences or speculative abstractions as defects.
5. Recommend the smallest safe correction.
6. Assign one severity: `Critical`, `High`, `Medium`, or `Low`.
7. Recheck each finding against surrounding behavior to avoid false positives.

## Severity and output

Order findings by severity. For each finding include:

- Severity and concise title.
- Specific `file:line` or section.
- Triggering input or state and resulting impact.
- Smallest safe fix.

Use Critical or High only for demonstrated severe impact or a credible path to it. Keep
summaries secondary to findings. If none exist, state `No actionable issues found.` and
mention residual validation or coverage gaps.

## Validation

Verify that every finding is introduced or exposed by the reviewed change, has enough
evidence to reproduce or reason about, points to the correct location, and is not already
prevented by a nearby invariant. Separate blocking defects from optional cleanup.
