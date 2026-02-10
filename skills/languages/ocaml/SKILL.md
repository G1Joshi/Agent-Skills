---
name: ocaml
description: OCaml functional programming with type inference. Use for .ml files.
---

# OCaml

OCaml v5 brings **Multicore** support to the language, removing the Global Interpreter Lock (GIL). It combines functional safety with imperative speed.

## When to Use

- **Compilers**: Rust, Haxe, and Flow are written in OCaml.
- **Financial Trading**: Jane Street uses OCaml for everything.
- **Formal Verification**: Coq proof assistant is OCaml.

## Core Concepts

### Strong Static Types

Inference is so good you rarely write types.

### Modules (Functors)

Parametrized modules (functions that return modules).

### Effects (v5)

Algebraic Effects for concurrency (e.g., `Eio`).

## Best Practices (2025)

**Do**:

- **Use `dune`**: The standard build system.
- **Use `opam`**: The package manager.
- **Use `Eio`**: The modern async I/O library for OCaml 5.

**Don't**:

- **Don't use `Threads` directly**: Use domains/effects for parallelism.

## References

- [OCaml.org](https://ocaml.org/)
