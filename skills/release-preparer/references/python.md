# Python and PyPI

- Find the authoritative version through the configured build backend and existing release tooling. Check the wheel and sdist for expected modules, data, license, dependencies, entry points, and Python requirements.
- In a uv project, build with `uv build --out-dir <fresh-dir>`. Inspect the archives and smoke-test the wheel in a clean environment. For README rendering, use the project's Twine check or `uvx twine check --strict <fresh-dir>/*`.
- Use the [uv publish guide](https://docs.astral.sh/uv/guides/publish/) to configure the intended index. [`uv publish --dry-run`](https://docs.astral.sh/uv/reference/cli/#uv-publish) checks distributions without uploading on versions that support it. For an authorized upload, pass only the verified artifacts and choose the intended index explicitly when testing. TestPyPI and PyPI have separate credentials and [Trusted Publisher configuration](https://docs.pypi.org/trusted-publishers/).
