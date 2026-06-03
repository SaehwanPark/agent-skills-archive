# Agent Skills Archive

Reusable skills for coding agents, plus the repo-local tooling and harness used to create,
maintain, validate, and deploy them.

This repository has two separate surfaces:

| Surface | Path | Purpose |
| --- | --- | --- |
| Skill archive | `skills/` | Deployable reusable skills. Each child directory is a skill package. |
| Project harness | `.agents/`, `docs/harness/`, `_workspace/` | Guidance for agents working on this repository. This is not archive content. |

Keep those surfaces separate. Add or update deployable skills under `skills/`; add
repository-specific agent workflow guidance under `.agents/` and `docs/harness/`.

## Creating and Developing Skills

Each archive skill lives in its own directory:

```text
skills/<skill-name>/SKILL.md
```

`SKILL.md` must start with a YAML frontmatter header so the deploy tooling can discover
and validate it:

```markdown
---
name: <skill-name>
description: Use when ...
---
```

The `name` must match the directory name. Keep the top-level `SKILL.md` lean and move
large examples, checklists, or domain references into `references/` or `examples/`
inside that skill directory.

Useful development loop:

```bash
uv run deploy-skills --list-skills
uv run deploy-skills --dry-run --skill <skill-name>
uv run python -m unittest discover -s tests
```

When changing deploy behavior, update tests in `tests/`. When changing a skill, validate
that its frontmatter, directory name, and internal references still line up.

## Project Harness

The repo-local harness for maintaining this project lives outside the deployable archive:

```text
AGENTS.md
.agents/skills/agent-skills-archive-orchestrator/SKILL.md
docs/harness/agent-skills-archive/team-spec.md
_workspace/
```

Use the harness when a task is about creating, revising, reviewing, or validating skills
in this repository. Do not copy `.agents/skills/` into `skills/`; those files are
project workflow guidance, not reusable archive skills.

## Deploy Quick Start

```bash
uv run deploy-skills --list-skills
uv run deploy-skills --dry-run
uv run deploy-skills
uv run deploy-skills --all
```

For spawned or non-interactive environments where `uv` may not be on `PATH`, use the
repo-local launcher:

```bash
./bin/deploy-skills --list-skills
./bin/deploy-skills --all
```

The launcher resolves `uv` with `which uv`. Override it with `UV_BIN` if `uv` is
installed somewhere that is not on `PATH`.

By default, this opens a chooser and installs the selected skill(s) into the Codex personal location:

```text
~/.agents/skills
```

## Deploy Targets

| Agent | Personal | Project |
| --- | --- | --- |
| Codex | `~/.agents/skills` | `.agents/skills` |
| Claude Code | `~/.claude/skills` | `.claude/skills` |
| ForgeCode | `~/forge/skills` | `.forge/skills` |
| Droid | `~/.factory/skills` | `.factory/skills` |
| OpenCode | `~/.config/opencode/skills` | `.opencode/skills` |
| AntiGravity CLI | `~/.gemini/skills` | `.agents/skills` |

Copy everything explicitly:

```bash
uv run deploy-skills --all
```

## Examples

Choose a specific skill non-interactively:

```bash
uv run deploy-skills --skill fp-developer
```

Install for Claude Code:

```bash
uv run deploy-skills --agent claude --all
```

Install into the current repo for Codex:

```bash
uv run deploy-skills --scope project --skill fp-developer
```

In this repository, `.agents/skills` is reserved for the project harness. When deploying
archive skills into another repo, pass that repo explicitly:

```bash
uv run deploy-skills --scope project --project /path/to/target-repo --skill fp-developer
```

Compatibility aliases are available for older or alternate conventions:

```bash
uv run deploy-skills --agent codex-legacy
uv run deploy-skills --agent droid-compat --scope project
```

Preview destination paths:

```bash
uv run deploy-skills --list-targets --agent all --scope project
```

## Safety

The deploy command copies skill directories. It fails if a destination already exists, unless you explicitly replace it:

```bash
uv run deploy-skills --force
```

Use `--dry-run` before writing:

```bash
uv run deploy-skills --agent opencode --scope project --dry-run
```

When you run `uv run deploy-skills` without `--skill` or `--all`, it shows a numbered chooser so you can pick one or more skills.

## Development

Requirements:

- Python 3.12+
- `uv`

Run tests:

```bash
uv run python -m unittest discover -s tests
```
