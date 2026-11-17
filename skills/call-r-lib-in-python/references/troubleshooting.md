# rpy2 troubleshooting

Use the same interpreter and environment as the application:

```sh
R --version
R RHOME
python -c 'from importlib.metadata import version; print(version("rpy2"))'
python -m rpy2.situation
python -c 'from rpy2.robjects import r; print(r("R.version.string")[0])'
```

The last command verifies embedded R actually initializes. For loader errors, check that R and Python architectures agree and follow the [rpy2 installation guidance](https://rpy2.github.io/doc/latest/html/overview.html) for the host. Set `R_HOME` only when discovery needs an override. If rpy2 reports a failed API-mode import and then loads in ABI mode, verify which mode the application actually uses before diagnosing package code.

If a package is missing, check `.libPaths()` inside embedded R and compare its libraries with those of the R shell. For malformed conversion, reduce the failing input to a representative column or scalar and inspect type, missingness, and attributes on each side.
