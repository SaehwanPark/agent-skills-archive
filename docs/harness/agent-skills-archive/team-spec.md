# Agent Skills Archive Harness Team Spec

## Domain Summary

This repository maintains reusable coding-agent skills and the deploy tooling that copies
those skills into agent-specific personal or project locations. The archive surface is
`skills/`. The repo-local harness surface is `.agents/`, `docs/harness/`, and
`_workspace/`.

## Architecture

Pattern: Pipeline.

Most work moves through a simple ordered flow: classify the request, inspect the target
surface, edit the skill or tooling, validate metadata and behavior, then summarize the
result. Parallel workers are unnecessary unless a future task asks for broad independent
review across many skills.

## Roles

### Orchestrator

Skill: `.agents/skills/agent-skills-archive-orchestrator/SKILL.md`

Responsibilities:

- Route work to the archive surface or the project-harness surface.
- Preserve the boundary between deployable skills and repo-local guidance.
- Choose validation commands based on the changed files.
- Keep intermediate handoffs deterministic when a task has multiple phases.

Inputs:

- User request.
- Affected files under `skills/`, `src/`, `tests/`, `README.md`, `AGENTS.md`, or `docs/harness/`.

Outputs:

- Edited repository files.
- Optional `_workspace/` handoff notes.
- Final validation summary.

## Handoff Files

Use `_workspace/` only when a task benefits from a durable intermediate artifact.

Suggested names:

- `_workspace/01_request_scope.md`
- `_workspace/02_skill_draft.md`
- `_workspace/03_validation_report.md`
- `_workspace/04_review_notes.md`

Small one-turn tasks do not need handoff files.

## Surface Rules

- `skills/<skill-name>/` is the only deployable archive location.
- `.agents/skills/` contains repo-local harness skills and should not be copied into `skills/`.
- `docs/harness/agent-skills-archive/` contains durable harness design and role contracts.
- `_workspace/` contains temporary or reviewable handoff artifacts.

## Quality Gates

- Every deployable skill has `SKILL.md` with YAML frontmatter containing `name` and `description`.
- The frontmatter `name` matches the skill directory.
- Deploy-tooling changes include focused tests or a clear explanation for why tests were not needed.
- Documentation changes keep the archive and harness surfaces distinct.

## Failure Policy

- If a skill lacks valid frontmatter, stop archive deployment work and fix metadata first.
- If a requested project-scope deployment would write into `.agents/skills/` in this repo, confirm whether the user intends to mix installed skills with the repo-local harness.
- If validation fails, preserve the failure output in the final summary or `_workspace/03_validation_report.md` for multi-phase tasks.
