---
name: fsharp
description: F# functional-first programming on .NET. Use for .fs files.
---

# F#

F# is the functional sibling of C# on .NET. v9.0 (2025) brings **Nullable Reference Types** integration and better performance for list comprehensions.

## When to Use

- **Financial Tech**: Correctness and domain modeling.
- **Data Processing**: Pipeline operator `|>` and immutability by default.
- **Interpro**: Seamlessly use any NuGet package.

## Core Concepts

### Discriminated Unions

`type Shape = Circle of float | Rect of float * float`.

### Pipe Operator

`data |> filter |> map`.

### Computation Expressions

`async { ... }`, `task { ... }`.

## Best Practices (2025)

**Do**:

- **Use Records**: Immutable data containers.
- **Use Pattern Matching**: `match x with ...`.
- **Use `SAFE Stack`**: For full-stack F# web apps (Saturn, Azure, Fable, Elmish).

**Don't**:

- **Don't mimic C#**: Avoid classes/inheritance unless interoperating.

## References

- [F# Guide](https://fsharp.org/)
