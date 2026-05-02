# Agent Skills Archive

Reusable skills for coding agents, with a small `uv`-native deploy command for choosing which skills to install.

## Quick Start

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

The launcher defaults to `/Users/saehwan/.local/bin/uv`. Override it with `UV_BIN`
if `uv` is installed elsewhere.

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
