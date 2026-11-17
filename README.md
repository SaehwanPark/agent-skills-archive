# Agent Skills Archive

This repository collects reusable skills for coding agents and the tooling used to
validate and deploy them.

Each skill provides a short workflow for a specific task. The entry point carries the
decisions that matter on routine runs. Linked guides, examples, and tools are available
when the task needs them.

## Skills in this archive

| Skill | When to use it |
| --- | --- |
| [`simple-code-writer`](skills/simple-code-writer/SKILL.md) | Make the smallest correct implementation or refactor and verify the affected behavior. |
| [`code-commenter`](skills/code-commenter/SKILL.md) | Document rationale, invariants, and public contracts close to the code. |
| [`code-reviewer`](skills/code-reviewer/SKILL.md) | Report actionable defects in a diff with concrete triggers and impact. |
| [`fp-developer`](skills/fp-developer/SKILL.md) | Make state and effects explicit in Python, Rust, Swift, Kotlin, or Mojo. |
| [`plan-designer`](skills/plan-designer/SKILL.md) | Write a bounded implementation plan with observable acceptance criteria. |
| [`preferred-workflow`](skills/preferred-workflow/SKILL.md) | Take a change from repository context through verification and the requested Git handoff. |
| [`spec-driven-developer`](skills/spec-driven-developer/SKILL.md) | Keep a project's specification, architecture, and changelog aligned with the work. |
| [`release-preparer`](skills/release-preparer/SKILL.md) | Curate public source and validate Python, Rust, or Mojo release artifacts. |
| [`end-user-xp-improver`](skills/end-user-xp-improver/SKILL.md) | Improve defaults, errors, recovery, and accessibility on the common user path. |
| [`lesson-documenter`](skills/lesson-documenter/SKILL.md) | Record a verified cause and prevention for a recurring development trap. |
| [`wayback-link-fallback`](skills/wayback-link-fallback/SKILL.md) | Find and cite a relevant historical web capture. |
| [`call-r-lib-in-python`](skills/call-r-lib-in-python/SKILL.md) | Use rpy2 to call R and preserve data and model semantics at the boundary. |
| [`scientific-prose-editor`](skills/scientific-prose-editor/SKILL.md) | Edit scientific prose and verify meaning claim by claim. Local token and style diagnostics are available for longer or higher-risk edits. |

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

Give the frontmatter description enough detail for an agent to recognize when to use
the skill. Keep the normal workflow in `SKILL.md` and link each bundled Markdown
resource directly with a cue for when to open it. Keep verification proportional to the
task. For version-sensitive commands, prefer the project's toolchain and link the
official documentation for the version-specific behavior.

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
