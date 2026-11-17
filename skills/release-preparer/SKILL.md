---
name: release-preparer
description: Use when preparing a private repository for public release, curating legacy content, or packaging Python, Rust, or Mojo projects for publication.
---

# Release Preparer

1. Identify the source revision, destination, intended artifacts, canonical version, and existing release automation. Inspect package inclusion, licensing, generated files, and private or sensitive content in the surface being released.
2. Reuse the project's release path. Stage public output separately when curation is needed. Add repeatable automation only where the release requires it.
3. Verify the actual staged tree or built artifacts, including metadata, contents, and install or import behavior where practical. Use a fresh output directory so stale files cannot be published.
4. Check the destination, account, version, and artifact list before any authorized push, tag, or upload. Follow the user's authorization and applicable release rules. Report verified artifacts, publication status, and blockers.

Read [public repository curation](references/public-repo.md) when publishing source. Load the applicable package guide only: [Python/PyPI](references/python.md), [Rust/Cargo](references/rust.md), or [Mojo/Pixi](references/mojo-pixi.md).
