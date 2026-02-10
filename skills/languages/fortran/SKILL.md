---
name: fortran
description: Fortran for scientific and numerical computing. Use for .f90 files.
---

# Fortran

Fortran is not dead; it drives global weather forecasting and computational physics (MPI). **Fortran 2023** adds better C-interop and conditional expressions.

## When to Use

- **HPC**: High Performance Computing on supercomputers.
- **Legacy**: 50 years of tested scientific libraries (LAPACK, BLAS).
- **Arrays**: Native multi-dimensional array slicing is superior to C.

## Core Concepts

### Modules

Modern encapsulation. `USE my_module`.

### Coarrays

Native parallel programming syntax created for supercomputers.

### Implicit None

Always required to disable legacy variable typing.

## Best Practices (2025)

**Do**:

- **Use `fpm`**: The Fortran Package Manager (modern tooling!).
- **Use `iso_c_binding`**: To call Fortran from C/Python.
- **Use `do concurrent`**: To hint optimizations to the compiler.

**Don't**:

- **Don't use fixed form**: No `.f` (77). Use `.f90` (free form).

## References

- [Fortran Lang](https://fortran-lang.org/)
