# Mojo

Use the project's pinned toolchain and check `mojo --version` before choosing syntax or commands. The [function reference](https://mojolang.org/docs/reference/function-declarations/) covers current `def` declarations and argument conventions.

- Use structs and traits for stable domain boundaries. Make reads, mutation, transfer, and aliasing explicit. Prefer local mutation for performance-sensitive work when it does not leak effects. Verify reference origins and ownership at the boundary.
- Keep Python calls, device selection, memory transfer, and synchronization at adapters. Pass typed values and explicit shapes or layouts into core logic when practical.
- Run configured Pixi tasks where present. With Mojo 1.2, use `mojo run path/to/test_file.mojo` for a test entry point using [TestSuite](https://mojolang.org/docs/tools/testing/). Use `mojo precompile path/to/package -o package.mojoc` to check a precompiled import package. The [precompiled artifact](https://mojolang.org/docs/cli/precompile/) is tied to the compiler version.
