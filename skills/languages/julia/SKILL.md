---
name: julia
description: Julia scientific computing for numerical analysis and data science. Use for .jl files.
---

# Julia

Julia looks like Python but runs like C. v1.11 (2025) introduces a specialized **Memory type** and faster array operations. It is widely used in scientific computing.

## When to Use

- **Scientific Computing**: Simulations, physics, differential equations.
- **Data Science**: Heavily optimized DataFrame operations.
- **Performance**: Multiple Dispatch system allows extreme optimization.

## Core Concepts

### Multiple Dispatch

Functions implementation is chosen based on ALL argument types.

### JIT Compilation

LLVM-based Just-In-Time compilation.

### Macros

Lisp-like metaprogramming. `@time`, `@threads`.

## Best Practices (2025)

**Do**:

- **Use `Revise.jl`**: For hot code reloading.
- **Type Stability**: Ensure variables don't change types in loops.
- **Use `Pkg`**: Native package manager with environments.

**Don't**:

- **Don't use for small scripts**: The startup time (TTFX) can be slow, though v1.10+ improved it.

## References

- [Julia Lang](https://julialang.org/)
