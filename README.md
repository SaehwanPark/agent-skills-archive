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
| `simple-code-writer` | Chooses the smallest correct implementation or refactor. | Preserves contracts while avoiding speculative abstractions and dependencies. |
| `code-commenter` | Adds or reviews comments that preserve rationale, invariants, and public contracts. | Gives maintainers non-obvious context without narrating code mechanics. |
| `code-reviewer` | Reviews diffs and PRs for concrete production risks. | Produces evidence-based, severity-ranked findings and minimizes false positives. |
| `fp-developer` | Applies functional-first design to Python, Rust, Swift, Kotlin, and Mojo. | Makes state, effects, failures, types, and testable domain logic explicit. |
| `plan-designer` | Turns coding requests into bounded, decision-complete implementation plans. | Removes design guesswork while defining tests, non-goals, and stop conditions. |
| `preferred-workflow` | Guides continuations, features, fixes, and refactors through branch and PR handoff. | Provides a safe default workflow with review that can be explicitly opted out of. |
| `spec-driven-developer` | Keeps lightweight project state aligned with implementation. | Reconciles specifications, architecture, and changelog history with evidence. |
| `release-preparer` | Prepares private repositories and packages for public release. | Separates curation, validation, approval-gated publication, and ecosystem details. |
| `end-user-xp-improver` | Improves user-facing workflows, defaults, errors, recovery, and accessibility. | Grounds interface decisions in a target audience and representative journeys. |
| `lesson-documenter` | Captures verified, recurring development and operations traps. | Preserves causes and prevention without accumulating debugging diaries. |
| `wayback-link-fallback` | Recovers version-appropriate archived web evidence. | Handles dead or changed sources while preserving provenance and current-truth checks. |
| `call-r-lib-in-python` | Integrates R packages and models into Python through `rpy2`. | Makes runtime discovery, dependencies, conversion, fitting, and extraction explicit. |

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

All trigger conditions belong in the frontmatter description because it is available
before the skill loads. Keep `SKILL.md` to the core workflow and directly link every
bundled Markdown resource so agents can load optional detail only when it applies.

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

By default, the deploy command installs for Codex at the standard personal skill
location. You can also target a project or request compatibility links for another
agent with the flags described below.

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

The test suite validates canonical frontmatter, portable skill names, a 200-line budget
for each `SKILL.md`, local Markdown links, and direct discoverability of bundled Markdown
resources. It uses only the project's existing standard-library tooling.

## Deploy Targets

Every deployment copies each selected skill once to a standard directory:

| Scope | Canonical destination |
| --- | --- |
| Personal | `~/.agents/skills/<skill-name>` |
| Project | `<project>/.agents/skills/<skill-name>` |

Agent-specific locations contain relative links to those canonical copies only when
the agent does not discover the standard directory natively:

| Agent | Personal compatibility location | Project compatibility location |
| --- | --- | --- |
| Codex | None; uses the canonical location | None; uses the canonical location |
| Claude Code | `~/.claude/skills` | `.claude/skills` |
| ForgeCode | None; discovers `~/.agents/skills` | `.forge/skills` |
| Droid | `~/.factory/skills` | `.factory/skills` |
| OpenCode | None; discovers the canonical location | None; discovers the canonical location |
| AntiGravity CLI | `~/.gemini/skills` | None; uses the canonical location |

The compatibility aliases `codex-legacy` and `droid-compat` link from
`$CODEX_HOME/skills` and project `.agent/skills`, respectively. A link is created for
each selected skill rather than for the entire skills root, so unrelated agent-specific
skills remain untouched.

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

This copies each selected skill to `~/.agents/skills` and links the corresponding
entry under `~/.claude/skills` back to that canonical copy.

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

Target output labels the canonical `copy` destination and any agent-specific `link`
destinations.

## Safety

The deploy command preflights all selected destinations before writing. It fails if a
canonical destination or conflicting compatibility entry already exists unless you
explicitly replace it:

```bash
uv run deploy-skills --force
```

Use `--force` to migrate old agent-specific copied directories to links. Correct links
are left unchanged. Replacement removes the link itself, never the canonical directory
to which it points.

Use `--dry-run` before writing:

```bash
uv run deploy-skills --agent opencode --scope project --dry-run
```

When you run `uv run deploy-skills` without `--skill` or `--all`, it shows a numbered
chooser so you can pick one or more skills.
