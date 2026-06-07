# Rust Cargo Release

Use this reference for Rust crates or workspaces that publish to crates.io or another
Cargo registry.

## Discovery

Inspect:

- root and member `Cargo.toml` manifests
- `Cargo.lock`, workspace membership, `workspace.package`, and `workspace.dependencies`
- crate names, package selection rules, features, examples, and build scripts
- `package.include`, `package.exclude`, and files ignored by version control
- existing release tools such as `cargo-release`, `release-plz`, or `xtask`

If a workspace has multiple publishable crates, define the release order and package
selection explicitly before editing.

## Version and Metadata

Find the canonical version source in `Cargo.toml` or workspace metadata. Preserve an
existing version higher than `1.0.0`; otherwise set the release version to `1.0.0` when
the user requested a stable release.

Review public crate metadata:

- `name`, `version`, `description`, `license` or `license-file`
- `repository`, `homepage`, `documentation`, and `readme`
- `keywords`, `categories`, `rust-version`, and edition
- `include`, `exclude`, and `publish` registry restrictions
- workspace dependency versions and path dependencies that cannot publish as-is

Cargo publish is permanent for a given version on crates.io: versions cannot be
overwritten or deleted. Treat name availability and version reuse as approval-gated.

## Build and Publish Script

Create a project-local build/publish script, usually under `deployment/`, that:

- verifies `cargo`, `rustc`, and any project release tooling are installed
- verifies registry auth without printing secrets
- supports `CARGO_REGISTRY_TOKEN` and existing Cargo auth config
- accepts package/workspace selection explicitly for multi-crate repositories
- runs formatting, linting, tests, and package dry-run before publishing
- checks package contents with `cargo package --list`
- publishes with `cargo publish` only after approval
- fails clearly when metadata, version, registry, or token prerequisites are missing

Respect `package.publish` restrictions and explicit `--registry` or `--index` settings
when the project does not publish to the default crates.io registry.

## Validation

Use the project conventions first. Common checks:

```bash
cargo fmt --check
cargo clippy --all-targets --all-features -- -D warnings
cargo test --all-features
cargo publish --dry-run
cargo package --list
```

For workspaces, add `--package`, `--workspace`, or `--exclude` exactly as required by
the release plan.
