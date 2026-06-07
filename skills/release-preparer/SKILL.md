---
name: release-preparer
description: Use when preparing a private development repository for a clean public release repository, legacy-code isolation, repeatable release automation, and package publication readiness across Python/PyPI, Rust/Cargo, and Mojo/Pixi ecosystems.
---

# Release Preparer

## When to Use

Use this skill when a repository needs cleanup and release preparation that turns a
private development repo into a clean public release repo, then publishes a package
through the project's ecosystem.

This skill is for implementing a repeatable release workflow, not for one-off manual
publishing.

## Operating Rules

- Inspect first. Do not assume paths, package manager, version source, public repo
  name, CI layout, or release scripts.
- If the current project version is greater than `1.0.0`, preserve it. Otherwise use
  `1.0.0` as the stable-release default when the user asked for a stable first release.
- Keep development-only release tooling in the development repo unless the curation
  spec intentionally includes it in the public repo.
- Do not publish to GitHub or any package registry without explicit user approval.
- Do not delete legacy code unless explicitly asked; isolate and document it instead.
- Treat secrets found in tracked files as a stop condition.
- Load only the relevant reference files for the repository under work. For a normal
  single-ecosystem repo, load `references/public-repo.md` plus one package reference.

## Discovery

Before editing, inspect the repository for:

- Package metadata and version sources: `pyproject.toml`, `Cargo.toml`, `pixi.toml`,
  Mojo packaging recipes, setup files, dynamic version tooling, lockfiles, and release
  notes.
- Repository identity: current directory name, Git remotes, default branch, and whether
  the repo follows `<project>-dev` or `<project>_dev`.
- Existing release automation: scripts, Makefiles, CI workflows, deploy docs, package
  indexes, and GitHub Actions.
- Public-facing docs: `README`, install docs, quickstarts, API docs, contributing docs,
  changelog, examples, and notebooks.
- Development-only or non-public material: agent harnesses, internal docs, experiments,
  scratch work, intermediate artifacts, private configs, generated caches, and legacy
  code.
- Test and build commands already used by the project.

If multiple incompatible package managers, version sources, public repo names, or
release workflows exist, stop and ask for a decision before implementing.

## Reference Selection

- Always load `references/public-repo.md` when public repo generation, docs curation,
  or legacy isolation is in scope.
- For Python packages, load `references/python.md`.
- For Rust crates, load `references/rust.md`.
- For Mojo packages managed with Pixi or modular-community, load
  `references/mojo-pixi.md`.
- For multi-language repositories, load every applicable ecosystem reference and make
  the curation spec explicit about which package artifacts are public.

## Workflow

1. Discover the repo shape, package ecosystem, current version, release automation, and
   public/private boundary.
2. Load the matching reference files.
3. Plan the public release surface and package publication path.
4. Isolate legacy or non-public code only when safe and in scope.
5. Add or update curation config, public docs, and release scripts.
6. Validate locally without publishing.
7. Ask for explicit approval before GitHub creation/push or package publication.
8. Summarize changed files, validation output, and remaining approval-gated steps.

## Approval-Gated Actions

- GitHub repository creation or visibility changes.
- Commits, tags, pushes, or force updates to public repositories.
- Publishing to PyPI, TestPyPI, crates.io, prefix.dev, Anaconda.org, Cloudsmith, S3,
  Quetz, Artifactory, or modular-community.
- Deleting or permanently removing files from the development repository.

## Non-Goals

- Do not hard-code this skill's example paths into a project when the repo already has
  a release convention.
- Do not rewrite unrelated architecture or formatting.
- Do not replace existing release automation if a small extension can satisfy the goal.
- Do not move private/internal workflows into the generated public repository by
  default.
- Do not create a public repo, push commits, or publish packages without explicit
  approval.
- Do not guess ecosystem-specific syntax for fast-moving tools; consult current
  official docs when packaging behavior matters.

## Stop Conditions

Stop and report before continuing if:

- secrets, credentials, or private tokens are found in tracked files
- the public repository name cannot be derived safely
- multiple incompatible version sources or package managers exist
- existing release automation conflicts with the requested workflow
- moving legacy code would break imports or tests beyond the approved scope
- publishing would overwrite an existing GitHub repository or package version
- required tools such as `uv` or `gh` are unavailable and no acceptable fallback is
  approved
