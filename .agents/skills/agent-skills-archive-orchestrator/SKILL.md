---
name: agent-skills-archive-orchestrator
description: Use when creating, revising, reviewing, or validating deployable skills in this repository while keeping project harness artifacts separate from the skill archive.
---

# Agent Skills Archive Orchestrator

## When to Use

Use this skill for repository tasks that create, modify, review, validate, or document
skills under `skills/`, or that change the deploy tooling used to install those skills.

Do not use this skill for ordinary downstream use of an installed skill. Do not treat
files under `.agents/skills/` as archive content.

## Required Inputs

- The user request and intended target skill, if any.
- Current contents of the affected `skills/<skill-name>/` directory.
- Any deploy-tooling files touched by the request, especially `src/agent_skills_archive/deploy.py` and `tests/`.
- Existing repo guidance from `AGENTS.md` and `docs/harness/agent-skills-archive/team-spec.md`.

## Workflow

1. Classify the task as one or more of: new skill, skill revision, skill review, deploy-tooling change, documentation update, or harness update.
2. Confirm the target surface:
   - deployable archive content belongs under `skills/`
   - repo-local agent workflow belongs under `.agents/`, `docs/harness/`, or `_workspace/`
3. Inspect existing files before editing. Preserve unrelated user changes.
4. For archive skills, keep `SKILL.md` discoverable:
   - include YAML frontmatter with `name` and `description`
   - match `name` to the skill directory
   - keep large optional detail in `references/` or `examples/`
5. Record intermediate handoffs in `_workspace/` when the task has multiple phases or review evidence worth preserving.
6. Validate with the narrowest useful checks:
   - `uv run deploy-skills --list-skills`
   - `uv run deploy-skills --dry-run --skill <skill-name>` for affected skills
   - `uv run python -m unittest discover -s tests` when deploy code or metadata behavior changed
7. Summarize changed surfaces and validation results.

## Expected Outputs

- Updated archive skill files, deploy code, docs, or harness files as requested.
- A short note distinguishing archive changes from project-harness changes.
- Test or validation output, including any command that could not be run.

## Validation Notes

- The deploy command discovers only the archive source at `skills/` by default.
- Project harness skills under `.agents/skills/` should have normal skill frontmatter for agent usability, but they are not part of the archive.
- If a task asks to install skills into this repo as a project target, call out that the target path may overlap with the repo-local harness and confirm the intended destination before copying.
