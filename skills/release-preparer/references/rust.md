# Rust and Cargo

- Review package identity, version, license, MSRV, features, dependencies, and include/exclude rules. For a workspace, identify publishable crates and dependency order. Respect each manifest's `publish` setting.
- Use project checks and `cargo package --list -p <crate>` to inspect the selected crate. Run `cargo publish --dry-run -p <crate>` against the intended registry as appropriate. Dry runs may need network access and cannot resolve dependencies that have yet to be published unless the configured Cargo workflow supports staging them.
- Publish the approved version to the intended registry. crates.io versions cannot be overwritten. [Yanking](https://doc.rust-lang.org/cargo/commands/cargo-yank.html) affects new dependency resolution and does not remove files already published. See [Cargo publish](https://doc.rust-lang.org/cargo/commands/cargo-publish.html) for package and registry options.
