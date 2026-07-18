---
name: release-preparer
description: Use when converting a private development repository into a clean public release, isolating legacy code, adding repeatable release automation, or preparing Python/PyPI, Rust/Cargo, and Mojo/Pixi packages for publication.
---

# Release Preparer

Prepare a public release without rewriting the working project or publishing anything
without explicit authorization.

## Operating rules

- Inspect repository instructions, status, history, ignore rules, licenses, secrets,
  generated artifacts, package metadata, tests, and release configuration first.
- Treat secret removal and history rewriting as separate security-sensitive work; deleting
  a current file does not remove it from history.
- Prefer existing build and release tooling over a parallel release system.
- Preserve package identity and compatibility unless the release request changes them.
- Use dry runs, temporary outputs, and explicit destination checks before copying,
  deleting, tagging, publishing, or creating external resources.

## Reference routing

Always read [public repository guidance](references/public-repo.md) for public-release
curation. Then read only the relevant ecosystem guidance:

- [Python and PyPI](references/python.md)
- [Rust and Cargo](references/rust.md)
- [Mojo and Pixi](references/mojo-pixi.md)

For multi-package repositories, load each applicable guide and keep shared release policy
at the repository boundary rather than duplicating it in every package.

## Workflow

1. Define release source, destination, included packages, excluded private/legacy material,
   version, and required publication targets.
2. Inventory tracked and untracked content, credentials, licenses, generated files,
   package manifests, tests, and current automation.
3. Classify each material item as publish, generate, ignore, archive separately, or stop for
   user direction.
4. Make the smallest changes needed for a reproducible build and clean source artifact.
5. Validate metadata, package contents, documentation links, licenses, builds, tests, and
   clean-environment installation where practical.
6. Preview release or repository operations before executing authorized external actions.
7. Report artifacts, commands, omissions, approvals still needed, and residual risks.

## Approval-gated actions

Require explicit authorization for destructive cleanup, history rewriting, creating or
replacing a public repository, pushing, tagging, creating releases, and publishing to a
registry. Confirm the exact target and version immediately before an irreversible action.

## Non-goals

- Do not modernize unrelated implementation code.
- Do not publish secrets, private data, internal-only docs, or unclear-license material.
- Do not delete legacy code merely because it is excluded from the release.
- Do not claim reproducibility without running the documented build path.

## Stop conditions

Stop when ownership or licensing is unclear, secrets may remain in history, the destination
could overwrite existing work, package identity/version conflicts exist, validation cannot
be reproduced, or required publication authority is absent.

## Expected output

Report release boundaries, files or automation changed, validation and package inspection
results, external actions taken, deferred approvals, and remaining security or compatibility
risks.
