---
name: call-r-lib-in-python
description: Use when Python must call an R package through rpy2, exchange pandas or NumPy data with R, fit R-native models, or diagnose R discovery, package-library, conversion, and result-extraction failures.
---

# Call R Libraries from Python

Use rpy2 when an R-only implementation is required in-process. Prefer a maintained
Python-native implementation when it satisfies the requirement; prefer an `Rscript`
subprocess when strict process or dependency isolation is necessary.

## Preflight

Before debugging bridge code, verify the same environment that launches Python can run:

```console
which R
R --version
python -c "import rpy2; print(rpy2.__version__)"
```

Resolve R discovery, compatible R/rpy2 versions, and native build prerequisites before
investigating packages or conversion. Do not set `R_HOME` unless the installed rpy2/R
configuration requires it.

## Integration workflow

1. Choose and document a reproducible R dependency strategy. If packages are installed at
   runtime, use a writable project-local library and configure `.libPaths()` before package
   lookup. Do not silently mutate a global R installation.
2. Check packages with `requireNamespace(..., quietly = TRUE)` and use namespace-qualified
   calls where practical. Installation is an explicit environment/setup action, not an
   incidental model-fitting side effect.
3. Convert data explicitly at the Python/R boundary with a scoped rpy2 converter. Keep the
   original R object when R semantics such as factors, formulas, attributes, or classes
   matter.
4. Fit models with R-native inputs. Represent domain responses correctly—for example,
   grouped binomial models use successes and failures rather than an unexplained raw
   proportion.
5. Extract stable, named results at the R boundary. Coerce optional `NULL` values and
   complex S3/S4 structures in R before converting them to Python.
6. Return typed Python-facing values and retain version, warning, convergence, and failure
   evidence needed to interpret the result.

Read [integration patterns](references/integration-patterns.md) for concrete rpy2 code.
Read [troubleshooting](references/troubleshooting.md) only when diagnosing a failure.

## Design boundaries

Separate runtime discovery, dependency setup, conversion, and analysis. Keep R evaluation
small and parameterized; do not interpolate untrusted values into R source strings. Prefer
rpy2 objects, function calls, and explicit assignment over constructing executable code.

Treat these as public boundary concerns:

- Missing R, packages, compilers, or system libraries.
- Data-frame column types, missing values, factors, dates, and index semantics.
- R warnings, convergence messages, `NULL`, S3/S4 objects, and scalar/vector shape.
- Reproducible package versions and repositories.

## Stop conditions

Stop and report when:

- R and rpy2 compatibility cannot be established from the active environment.
- Package installation needs system changes, credentials, or network access not authorized
  by the user.
- Conversion would discard domain-significant R attributes or classes.
- A model result cannot be extracted without relying on an undocumented package structure.

## Completion checklist

- R discovery and relevant versions were recorded.
- Dependency setup is explicit and reproducible.
- Conversions are scoped and tested in both directions where required.
- R-native semantics are preserved during fitting and extraction.
- Warnings, optional values, and failures have stable Python representations.
- Tests cover representative data, missing/empty input, and at least one failure boundary.
