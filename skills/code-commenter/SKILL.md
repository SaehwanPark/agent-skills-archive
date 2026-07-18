---
name: code-commenter
description: Use when adding, revising, or reviewing code comments and documentation so maintainers understand non-obvious rationale, domain rules, invariants, constraints, and public contracts without restating code mechanics.
---

# Code Commenter

Make comments preserve information that clear code cannot express on its own.

## Required context

Inspect the relevant implementation, callers, tests, public contracts, repository
conventions, and existing comments. Pair this skill with the active implementation or
review workflow; do not use comments to compensate for unnecessarily obscure code.

## Decision workflow

1. Simplify confusing code first when that can make the behavior obvious without changing
   its contract.
2. Identify knowledge that would otherwise be lost: rationale, domain meaning, invariant,
   ordering requirement, compatibility constraint, safety condition, or deliberate
   tradeoff.
3. Put durable public behavior in the appropriate docstring or API documentation.
4. Add the smallest comment that explains the non-obvious fact.
5. Remove or revise comments that restate mechanics, preserve dead code, speculate, or no
   longer match the implementation.
6. Validate every changed comment against code and tests.

Read [comment patterns and examples](references/patterns.md) when deciding whether a
comment is warranted. Read [language guidance](references/languages.md) only for the
language being changed.

## Commenting rules

- Explain why a choice exists, what invariant it protects, or which external rule governs
  it; do not narrate syntax or control flow.
- Keep comments adjacent to the smallest stable unit they describe.
- Describe current truth. Put chronology in version control or a design record.
- Reference an ADR, issue, standard, or specification when it is the durable source of
  truth.
- Document inputs, outputs, errors, side effects, ownership, or safety for public or
  non-obvious interfaces; skip boilerplate for self-evident private helpers.
- Use `TODO` or `FIXME` only for concrete, actionable work. Include an issue identifier
  when the project uses one.
- Delete commented-out code; version control already preserves it.
- Follow the project's documentation tooling and style.

## Stop conditions

Stop and report when:

- The intended behavior is unclear enough that a truthful comment cannot be written.
- A comment would conceal a correctness issue or substitute for a necessary refactor.
- The requested wording conflicts with the implementation or public contract.
- A domain or safety claim lacks a reliable source.

## Validation

Before finalizing, verify:

- Each new comment adds rationale, context, or a contract not obvious from the code.
- Comments still hold for failure paths and edge cases.
- Public documentation matches the actual signature and behavior.
- No stale, redundant, speculative, or commented-out code remains in the touched scope.

Report which comments or docs changed and any uncertainty that prevented a safe update.
