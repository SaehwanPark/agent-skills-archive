# Public repository curation

- Identify what can be public, what must stay private, and which docs need a public counterpart. Stage a separate checkout or export and inspect its exact contents. Exclude credentials, private data, internal material, and files whose redistribution rights are unclear.
- If the release preserves history, review the refs that will be pushed. Deleting a file from the current tree does not remove it from history. Handle credential rotation and history rewriting under their own authorization.
- Isolate legacy content only within scope and verify imports and tests after moving it. For repeatable releases, keep one maintained list of inclusion and replacement rules and validate each staged output.
- Verify repository owner, name, visibility, and Git remotes before creating or updating the destination. For GitHub, see [gh repo create](https://cli.github.com/manual/gh_repo_create) and [gh release create](https://cli.github.com/manual/gh_release_create). Use `--verify-tag` to require an existing Git tag when publishing a GitHub release.
