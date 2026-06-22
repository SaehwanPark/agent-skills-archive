# Agent Skills Archive

This repository collects reusable skills for coding agents and the tooling used to
validate and deploy them.

If you are new here, the short version is:

- a **skill** is a small, reusable playbook for a specific kind of task
- skills live under `skills/<skill-name>/`
- each skill can be installed into an agent's personal or project skill directory
- the repo also contains a separate harness for maintaining this archive, but that
  harness is not itself deployable content

The benefit of using skills is consistency. Instead of re-explaining a workflow every
time, an agent can load a focused guide for a known task and apply the same pattern
reliably across projects.

## Skills in this archive

| Skill | What it does | Why it helps |
| --- | --- | --- |
| `simple-code-writer` | Applies simplicity-first defaults when writing, editing, or refactoring code. | Produces the smallest correct implementation while accounting for readability, maintenance, performance, and operational risk. |
| `code-reviewer` | Reviews code changes for bugs, security issues, performance risks, maintainability problems, and edge cases. | Gives a structured review with severity-ranked findings instead of vague feedback. |
| `fp-developer` | Applies a functional-first workflow with explicit state, pure core logic, typed boundaries, and tests-as-specs. | Helps keep complex code predictable and easier to test. |
| `plan-designer` | Turns an ambiguous implementation request into a bounded, decision-complete plan. | Reduces missed requirements before editing starts. |
| `preferred-workflow` | Guides checkpoint continuation, feature work, and refactors through a shared branch-test-review workflow. | Gives a reusable default for moving from context recovery to review-ready delivery. |
| `spec-driven-developer` | Keeps `SPEC.md`, `ARCHITECTURE.md`, and `CHANGELOG.md` aligned with implementation. | Preserves design intent and release history as code changes. |
| `release-preparer` | Prepares a private development repo for a clean public release. | Helps isolate legacy code and streamline release readiness. |
| `end-user-xp-improver` | Shapes product and interface decisions around user pain points and workflows. | Improves defaults and interactions from the end user's point of view. |
| `lesson-documenter` | Captures debugging lessons, setup traps, and project-specific gotchas. | Prevents the same operational mistakes from being rediscovered later. |
| `wayback-link-fallback` | Recovers archived copies of dead or unreliable web references. | Keeps research and documentation work moving when source links fail. |
| `call-r-lib-in-python` | Helps Python code call R packages through `rpy2` with reproducible packaging and safer data handling. | Makes mixed Python/R workflows less brittle. |

## What a skill looks like

Each deployable skill is a directory like this:

```text
skills/<skill-name>/SKILL.md
```

`SKILL.md` starts with YAML frontmatter so the deploy tool can discover it:

```markdown
---
name: <skill-name>
description: Use when ...
---
```

The `name` must match the directory name. Keep the top-level `SKILL.md` focused and move
long examples or reference material into `references/` or `examples/` inside the skill
directory.

## Using the archive

List the available skills:

```bash
uv run deploy-skills --list-skills
```

Preview a single skill before installing it:

```bash
uv run deploy-skills --dry-run --skill <skill-name>
```

Install a skill into the default personal target:

```bash
uv run deploy-skills --skill <skill-name>
```

If `uv` is not on `PATH`, use the repo-local launcher:

```bash
./bin/deploy-skills --list-skills
./bin/deploy-skills --all
```

By default, the deploy command installs into the current agent's personal skill
location. You can also target a project or a different agent with the deploy flags
described below.

## Archive And Harness

This repository has two separate surfaces:

| Surface | Path | Purpose |
| --- | --- | --- |
| Skill archive | `skills/` | Deployable reusable skills. Each child directory is one skill package. |
| Project harness | `.agents/`, `docs/harness/`, `_workspace/` | Repo-local guidance for creating, validating, and documenting skills in this repository. |

Keep those surfaces separate. Add or update deployable skills under `skills/`; add
repository-specific workflow guidance under `.agents/` and `docs/harness/`.

## Development

Requirements:

- Python 3.12+
- `uv`

Useful commands:

```bash
uv run deploy-skills --list-skills
uv run deploy-skills --dry-run --skill <skill-name>
uv run python -m unittest discover -s tests
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

The deploy command copies skill directories. It fails if a destination already exists,
unless you explicitly replace it:

```bash
uv run deploy-skills --force
```

Use `--dry-run` before writing:

```bash
uv run deploy-skills --agent opencode --scope project --dry-run
```

When you run `uv run deploy-skills` without `--skill` or `--all`, it shows a numbered
chooser so you can pick one or more skills.
