# Mojo Pixi Release

Use this reference for Mojo projects managed with Pixi or published through
modular-community-style recipes.

## Current Docs Rule

Mojo and Pixi packaging are evolving quickly. Before implementing package metadata,
scripts, or command syntax, check the current official Mojo and Pixi docs. Do not rely
only on memory for Mojo package layout, Pixi build metadata, or publish behavior.

## Discovery

Inspect:

- `pixi.toml`, `pixi.lock`, recipes, build backends, and target platforms
- Mojo source layout, package entrypoints, examples, notebooks, and generated artifacts
- existing `pixi` tasks for format, test, package, build, and publish
- whether the release target is a direct Pixi channel or a modular-community recipe PR
- channel credentials, target channels, and local package output directories

If direct channel publishing and modular-community publication are both plausible, stop
and ask which release path is intended.

## Version and Metadata

Find the canonical version in the Pixi project metadata, recipe, or project-standard
source. Preserve an existing version higher than `1.0.0`; otherwise set the release
version to `1.0.0` when the user requested a stable release.

Review public package metadata:

- package name, version, description, license, repository, and maintainers
- dependencies, host/build requirements, platforms, and channels
- included source files and excluded development-only material
- package recipe compatibility with the intended channel
- lockfile expectations for reproducible development environments

## Build and Publish Script

Create a project-local build/publish script, usually under `deployment/`, that:

- verifies `pixi` and any required Mojo toolchain are installed
- runs project-defined format, test, build, and package tasks
- validates the package locally with `pixi publish --target-dir <path>` when suitable
- publishes to a channel with `pixi publish --target-channel <url>` only after approval
- supports the project's registry authentication method without printing secrets
- clearly separates local package validation from channel publication
- fails clearly when metadata, version, channel, or credential prerequisites are missing

For modular-community publication, the script or docs may prepare recipe changes and
validation output, but creating the pull request remains approval-gated.

## Validation

Use the project conventions first. Common checks:

```bash
pixi run mojo --version
pixi run mojo format .
pixi run mojo test
pixi publish --target-dir ./dist/pixi-local
```

Command names may differ by project. Prefer configured Pixi tasks when present, and
record any docs-derived command assumptions in the release handoff.
