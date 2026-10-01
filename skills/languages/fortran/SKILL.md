---
name: fortran
description: Expert modern Fortran (Fortran 90/2008/2018) assistance covering array operations, OpenMP, and numerical libraries. Use when writing scientific simulations, physics calculations, or high-performance linear algebra.
---

# Fortran

Modern Fortran is a high-performance compiled language engineered for numerical analysis, computational fluid dynamics, climate modeling, and large-scale parallel scientific computing (MPI/OpenMP).

## When to Use

- **High-Performance Numerical & Scientific Computing**: Weather forecasting, computational fluid dynamics (CFD), and physics simulations.
- **Supercomputing & HPC Clusters (MPI / OpenMP)**: Running petascale simulation workloads across thousands of distributed GPU/CPU nodes.
- **Linear Algebra BLAS/LAPACK Libraries**: Maximizing raw floating-point computation speed on multidimensional matrix operations.
- **Legacy Aerospace & Nuclear Engineering**: Maintaining and extending battle-tested mathematical modeling libraries.

## Quick Start

```fortran
program main
    implicit none
    integer, parameter :: dp = kind(1.0d0)
    real(dp) :: x = 2.0_dp, y = 3.0_dp, z

    z = x ** y
    print *, "Result of 2^3 is:", z
end program main
```

## Core Concepts

### Array Slicing & Pure Mathematical Syntax

Fortran treats multi-dimensional arrays as first-class primitives with native vector slicing:

```fortran
program matrix_ops
  implicit none
  real, dimension(3, 3) :: A, B, C

  ! Initialize array
  A = 2.0
  B = 3.0

  ! Element-wise matrix multiplication in single line
  C = A * B + 1.0

  print *, "Result Matrix (1,1):", C(1, 1)
end program matrix_ops
```

### Modern Fortran Modules (Fortran 2018/2023)

Encapsulates data, interfaces, and subroutines cleanly:

```fortran
module physics_engine
  implicit none
  private
  public :: calculate_kinetic_energy

contains

  pure function calculate_kinetic_energy(mass, velocity) result(energy)
    real, intent(in) :: mass, velocity
    real :: energy
    energy = 0.5 * mass * (velocity ** 2)
  end function calculate_kinetic_energy

end module physics_engine
```

### Coarray Parallelism for High-Performance Computing (HPC)

Built-in SPMD (Single Program, Multiple Data) parallel syntax without external MPI library calls:

```fortran
program coarray_demo
  implicit none
  integer :: val[*]

  val = this_image() ! Each parallel CPU core assigns its own image ID
  sync all

  if (this_image() == 1) then
    print *, "Image 1 read from Image 2:", val[2]
  end if
end program coarray_demo
```

## Common Patterns

### Vectorized Array Operations and Slicing

**Problem**: Writing nested DO loops for large matrix calculations is slow and error-prone.

**Solution**:
Use Fortran's native array syntax for automatic vectorization:

```fortran
program matrix_math
    implicit none
    real, dimension(100, 100) :: A, B, C

    call random_number(A)
    call random_number(B)

    ! Array-level element-wise operation (vectorized)
    C = A * B + sin(A)

    print *, "Sum of C matrix:", sum(C)
end program matrix_math
```

## Best Practices

**Do**:

- Always Declare `implicit none`: Eliminate dangerous legacy implicit typing by placing `implicit none` at the top of every module.
- Use Modern Fortran Standards (2008/2018/2023): Avoid obsolete fixed-format Fortran 77; write clean free-format code.
- Mark Side-Effect-Free Functions as `pure`: Enable aggressive compiler parallelization and optimization.
- Use `intent(in)`, `intent(out)`, and `intent(inout)`: Explicitly document and enforce parameter passing semantics.

**Don't**:

- Use common blocks (`COMMON`) or equivalence (`EQUIVALENCE`): Replace legacy shared memory with modern modules.
- Use fixed-form (column 7) syntax: Modern Fortran files should use `.f90`, `.f08`, or `.f18` extensions with free-format layout.
- Ignore array bounds checking during development: Compile with `-fcheck=all -Wall` during debugging.

## Troubleshooting

| Error                                              | Cause                                                                     | Solution                                                                                 |
| :------------------------------------------------- | :------------------------------------------------------------------------ | :--------------------------------------------------------------------------------------- |
| `Segmentation fault in array operation`            | Out of bounds array indexing or stack exhaustion from large local arrays. | Allocate large arrays on the heap using `allocatable` and compile with `-fcheck=bounds`. |
| `Type mismatch in argument '...'`                  | Passing default real/integer to function expecting double precision.      | Specify explicit precision kind (e.g. `1.0_dp`) on literals.                             |
| `implicit none error: symbol has no IMPLICIT type` | Undeclared variable used in program unit.                                 | Declare all variables explicitly with type and kind parameters.                          |

## References

- [Fortran Lang](https://fortran-lang.org/)
