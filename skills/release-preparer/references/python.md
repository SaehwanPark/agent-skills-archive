# Python PyPI/TestPyPI Release

Use this reference for Python projects that publish wheels and source distributions to
TestPyPI or PyPI.

## Discovery

Inspect:

- `pyproject.toml`, setup files, package `__init__`, and dynamic version tooling
- `uv.lock`, requirements files, build backend, and package inclusion settings
- existing release scripts, CI, tags, changelog, and published package name

If the project has multiple version sources, stop and ask which one is canonical.

## Version and Metadata

Find the canonical version source and make release references consistent. Preserve an
existing version higher than `1.0.0`; otherwise set the release version to `1.0.0` when
the user requested a stable release.

Review public package metadata:

- project name, description, readme, license, authors, maintainers, URLs
- Python version requirement and classifiers
- runtime dependencies and optional dependency groups
- build backend and source distribution/wheel outputs
- package data and files that should not ship in distributions

## Build and Publish Script

Create a project-local build/publish script, usually under `deployment/`, that:

- verifies `uv` is installed
- verifies tokens without printing values
- supports TestPyPI and PyPI modes
- supports `UV_PUBLISH_TOKEN`, `UV_PUBLISH_TOKEN_PYPI`, and
  `UV_PUBLISH_TOKEN_TESTPYPI` according to the target index
- cleans or isolates build outputs to avoid partial or stale artifacts
- runs `uv build`
- validates the wheel and source distribution before publishing
- publishes with `uv publish` only after approval
- fails clearly when metadata, version, or token prerequisites are missing

Publishing scripts run from the development repo but should publish the intended public
package artifacts.

## Validation

Use the project conventions first. Common checks:

```bash
uv run pytest
uv build
uv publish --dry-run
```

If `uv publish --dry-run` is unavailable or unsuitable for the target, run the closest
available metadata and artifact validation and clearly report the gap.
