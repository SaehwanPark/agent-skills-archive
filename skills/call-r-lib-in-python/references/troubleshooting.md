# rpy2 troubleshooting

## R is not found

- Run `which R` and `R --version` in the shell that launches Python.
- Print the active rpy2 and R versions.
- Check architecture and dynamic-library compatibility before changing bridge code.

## Package installation fails

- Confirm the selected library is writable and first in `.libPaths()`.
- Inspect missing compilers and system libraries separately from R package errors.
- Do not fall back to global installation without explicit authorization.

## Conversion is malformed

- Confirm conversion occurs inside the intended scoped converter.
- Inspect R classes, dimensions, names, factors, missing values, and dates before conversion.
- Reduce the failing value to one column or object type rather than changing all conversion
  behavior at once.

## Formula or factor behavior is wrong

- Keep modeling data R-native.
- Inspect factor levels, contrasts, response encoding, and the formula environment in R.
- Compare the call with a minimal R-only reproduction.

## Results or diagnostics are missing

- Prefer documented accessors.
- Normalize `NULL` and package-specific structures in R.
- Preserve warnings and convergence messages instead of treating a returned object as
  proof of a successful fit.
