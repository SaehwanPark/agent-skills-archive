# Mojo and Pixi

- Identify the project's pinned Mojo and Pixi versions, recipe, build backend, channels, and platforms. Use its configured tasks to exercise tests and builds. For Mojo 1.2, see the [test runner](https://mojolang.org/docs/tools/testing/) and [precompile command](https://mojolang.org/docs/cli/precompile/).
- A precompiled `.mojoc` is compiler-version-specific. For a Conda release, verify the recipe's source or binary payload and runtime constraints separately.
- In a buildable Pixi workspace, use [`pixi publish --target-dir <fresh-dir>`](https://pixi.prefix.dev/latest/reference/cli/pixi/publish/) to build and copy packages locally. The output directory is not indexed as a channel. Inspect and test the package before an authorized `pixi publish --target-channel <url>`. For a recipe-based distribution, follow the target channel's recipe submission process.
