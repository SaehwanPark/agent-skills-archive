---
name: call-r-lib-in-python
description: Use when Python code needs to call R packages through rpy2 with reproducible package management, robust data conversion, and reliable model execution and inspection patterns.
---

# call-r-lib-in-python

Use this skill when Python must call R libraries (for example `lme4`, `glmmTMB`, `survival`, `mgcv`) through `rpy2`.

The goal is to keep R package installs reproducible, avoid fragile conversion bugs, and make R model fitting and diagnostics predictable from Python.

## Use this skill when

- A Python workflow needs an R-only package or model implementation.
- You need to pass data between Python and R and consume R outputs in Python.
- You need to debug `rpy2` environment, package loading, or conversion behavior.

## Do not use this skill when

- A maintained Python-native implementation already satisfies the requirement.
- You need strict process isolation or independent runtime execution (prefer `Rscript` subprocess patterns in that case).

## Preflight checklist

Run these checks before deep debugging:

```console
which R
R --version
python -c "import rpy2; print(rpy2.__version__)"
```

If `rpy2` cannot find R, fix PATH or `R_HOME` first. Do not debug conversion or package code until R discovery works.

## Recommended integration workflow

### 1) Put R packages in a project-local library

System libraries are often read-only in sandboxes and managed environments. Prefer a repo-local path like `.r-lib`.

```python
from pathlib import Path
from rpy2.robjects import r

local_lib = Path(".r-lib").resolve()
local_lib.mkdir(parents=True, exist_ok=True)

r(f'''
local_lib <- "{local_lib.as_posix()}"
dir.create(local_lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(local_lib, .libPaths()))
''')
```

### 2) Check and install packages without attaching them

Use `requireNamespace(..., quietly = TRUE)` for availability checks. Install only missing packages, and install into the project-local library.

```python
from rpy2.robjects import r

required = ["lme4", "broom.mixed", "performance"]
r_required = ", ".join([f'"{pkg}"' for pkg in required])

r(f'''
required <- c({r_required})
missing <- required[!vapply(required, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing) > 0) {{
  install.packages(missing, repos = "https://cloud.r-project.org", lib = .libPaths()[1])
}}
''')
```

Notes:

- First install for packages like `lme4` can be slow because dependencies may compile from source (`Rcpp`, `RcppEigen`, `minqa`, `nloptr`, etc.).
- Long compiler output on the first run is normal.

### 3) Load namespaces explicitly

Attach only what you need; use namespace-qualified calls in programmatic contexts.

```python
r('library(lme4)')
```

For many functions, direct lookup is more reliable than assuming availability as a Python attribute:

```python
fixef = r["fixef"]
```

### 4) Convert data explicitly at boundaries

Do not rely on implicit conversion or `pd.DataFrame(r_obj)` for R data frames.

```python
import pandas as pd
from rpy2.robjects import conversion, default_converter, numpy2ri, pandas2ri
from rpy2.robjects.conversion import localconverter

def r_to_pandas(r_df):
  with localconverter(default_converter + pandas2ri.converter + numpy2ri.converter):
    return conversion.get_conversion().rpy2py(r_df)

def pandas_to_r(df: pd.DataFrame):
  with localconverter(default_converter + pandas2ri.converter + numpy2ri.converter):
    return conversion.get_conversion().py2rpy(df)
```

Keep an R-native data frame for R model fitting. Convert a copy to pandas only for Python-side preview or downstream Python processing.

### 5) Fit models in R with R-native objects

For formula evaluation and factor handling, pass the R data frame directly to R modeling functions.

```python
from rpy2.robjects import Formula, globalenv
from rpy2.robjects.packages import importr

lme4 = importr("lme4")

formula = Formula("cbind(incidence, size - incidence) ~ period + (1 | herd)")
model = lme4.glmer(formula, data=r_dataframe, family="binomial")
globalenv["model"] = model
```

For grouped-binomial logistic regression, use successes/failures (`cbind(successes, trials - successes)`), not a raw proportion response.

### 6) Pull diagnostics with stable R-side coercions

R `NULL` values can behave awkwardly in Python. Coerce optional outputs in R first.

```python
from rpy2.robjects import r

conv_messages = r('''
msgs <- slot(model, "optinfo")$conv$lme4$messages
if (is.null(msgs)) character(0) else as.character(msgs)
''')

random_var = float(r("as.data.frame(VarCorr(model))$vcov[1]")[0])
fixed_effects = r["fixef"](model)
```

Assigning `model` into `globalenv` helps follow-up R snippets inspect the same fitted object without brittle interpolation.

## Reusable implementation pattern

When possible, organize Python wrappers into four layers:

1. `runtime`: verify R availability and print versions.
2. `deps`: manage `.r-lib`, check/install packages with `requireNamespace`.
3. `bridge`: explicit `pandas <-> R` conversion helpers using `localconverter`.
4. `analysis`: model fit and extraction functions that accept/return typed Python objects.

This keeps environment logic separate from analysis logic and makes failures easier to diagnose.

## Troubleshooting guide

- `rpy2` import works but R is not found:
  - Re-check `which R` and `R --version`.
  - Verify PATH and `R_HOME` in the same shell used to launch Python.
- Package install fails in sandboxed or managed environments:
  - Confirm `.libPaths()[1]` points to a writable project-local directory.
  - Avoid relying on system-wide R library paths.
- Conversion output is malformed or transposed:
  - Confirm all dataframe conversions happen inside `localconverter(...)`.
  - Replace direct `pd.DataFrame(r_object)` calls.
- Formula or factor behavior looks wrong:
  - Keep model input as R data frame.
  - Ensure categorical columns are explicitly factors in R when needed.
- Later R snippets cannot find fitted model:
  - Assign `globalenv["model"] = model` immediately after fit.

## Completion checklist

- R runtime discovery validated (`which R`, `R --version`).
- Project-local R library configured and first in `.libPaths()`.
- Required packages checked via `requireNamespace` and installed if missing.
- Conversion helpers implemented with `localconverter` and used consistently.
- Models fit on R-native data, not pandas-converted copies.
- Optional R outputs (`NULL`-prone fields) coerced to stable R types before Python conversion.
