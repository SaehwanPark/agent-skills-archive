# rpy2 integration patterns

Create a writable project R library during setup and set `R_LIBS_USER` before starting R, or prepend the resolved directory via `.libPaths()`. Call R functions with typed arguments rather than interpolating values into R source strings.

Use the [pandas converter](https://rpy2.github.io/doc/latest/html/pandas.html) only at the boundary:

```python
from rpy2.robjects import conversion, default_converter, pandas2ri

pandas_converter = default_converter + pandas2ri.converter

with pandas_converter.context():
    r_frame = conversion.get_conversion().py2rpy(frame)

fit = model_package.fit(formula, data=r_frame)
```

Here `model_package.fit` stands for the R package's fitting function. Use `numpy2ri.converter` for a direct NumPy boundary. Avoid global converter activation, and avoid appending NumPy rules after the pandas converter where they can override pandas dispatch. Set the index, factor levels, and time zone intentionally where the model relies on them.

Use documented R accessors and extract simple named values before converting results back. Test against an R-only fit if contrasts, grouped response encoding, or the formula environment can affect interpretation. Check warnings and convergence separately from the existence of a fitted object.
