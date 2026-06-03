# Repository Agents Guide

## What

- This repo is an archive and development workspace for reusable coding-agent skills.
- Deployable skills live only under `skills/<skill-name>/`; each skill must include `SKILL.md` with `name` and `description` YAML frontmatter.
- The project harness lives under `.agents/`, `docs/harness/`, and `_workspace/`; it guides work on this repo and is not deployable archive content.

## Why

- Keeping archive skills separate from repo-local harness guidance prevents accidental deployment of project-only workflows.
- The deploy CLI depends on stable skill directory names and frontmatter metadata.

## How

- List skills: `uv run deploy-skills --list-skills`
- Preview deployment: `uv run deploy-skills --dry-run --skill <skill-name>`
- Run tests: `uv run python -m unittest discover -s tests`
- For skill creation or maintenance workflow, use `.agents/skills/agent-skills-archive-orchestrator/SKILL.md` and `docs/harness/agent-skills-archive/team-spec.md`.
