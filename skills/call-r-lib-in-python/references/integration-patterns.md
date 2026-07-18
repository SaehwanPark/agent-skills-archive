# rpy2 integration patterns

Verify imports against the installed rpy2 version because converter APIs can evolve.

## Project-local package library

Configure a writable library before checking packages:

```python
from pathlib import Path
from rpy2.robjects import globalenv, r

local_lib = Path(".r-lib").resolve()
local_lib.mkdir(parents=True, exist_ok=True)
globalenv["local_lib"] = str(local_lib)
r("dir.create(local_lib, recursive = TRUE, showWarnings = FALSE)")
r(".libPaths(c(local_lib, .libPaths()))")
```

Keep package installation in an explicit setup command or function. Check availability
with `requireNamespace` and use an explicitly chosen CRAN mirror and library.

## Scoped data conversion

```python
from rpy2.robjects import conversion, default_converter, numpy2ri, pandas2ri

converter = default_converter + pandas2ri.converter + numpy2ri.converter

def pandas_to_r(frame):
  with converter.context():
    return conversion.get_conversion().py2rpy(frame)

def r_to_python(value):
  with converter.context():
    return conversion.get_conversion().rpy2py(value)
```

Do not construct a pandas frame directly from an arbitrary R data frame. Check column
types, categories/factors, missing values, dates, and index behavior after conversion.

## R-native fitting and extraction

Pass R data frames directly to formula-based R functions. Assign a fitted object into an R
environment only when later R-side extraction requires it. Prefer named package functions
or `r["function_name"]` over fragile attribute assumptions.

Normalize optional results before conversion:

```r
messages <- slot(model, "optinfo")$conv$lme4$messages
if (is.null(messages)) character(0) else as.character(messages)
```

Use documented accessors before reaching into S3/S4 internals. Convert final tables,
scalars, strings, and named vectors rather than exposing opaque R objects unintentionally.
