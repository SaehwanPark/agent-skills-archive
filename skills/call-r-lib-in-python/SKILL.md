---
name: call-r-lib-in-python
description: Use when calling R from Python with rpy2, exchanging pandas or NumPy data, fitting R-native models, or troubleshooting the bridge.
---

# Call R Libraries from Python

Use rpy2 for an in-process R dependency. Use an existing subprocess boundary when isolation is required.

1. Check R and rpy2 in the interpreter environment that will run the code. For discovery or dynamic-library failures, use [troubleshooting](references/troubleshooting.md).
2. Resolve R dependencies during setup. Check packages with `requireNamespace` and use the project's managed library. Keep installation out of model fitting.
3. Scope conversion to the Python/R boundary. Keep formula inputs and fitted objects R-native when classes, contrasts, or attributes matter. Check factor levels, missing values, and shape on representative inputs.
4. Extract named results using documented accessors. Normalize optional `NULL` values and return diagnostics that affect interpretation, such as warnings or convergence. See [integration patterns](references/integration-patterns.md) for library, conversion, and extraction details.
