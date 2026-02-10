---
name: nim
description: Nim systems programming with Python-like syntax. Use for .nim files.
---

# Nim

Nim v2.0 (2023/2024) made **ORC** (Deterministic Memory Management) the default. It compiles to C/C++/JS and offers Python-like syntax with C-like speeds.

## When to Use

- **Game Development**: Hot reloading and performance.
- **Embedded**: Compiles to small C code requiring no runtime.
- **Scripting**: Compiles so fast it feels like a script (`nim r`).

## Core Concepts

### Metaprogramming

First-class support. You can rewrite the AST to create DSLs.

### ORC

Cycle-collecting ARC. Automatic memory management without pauses.

### Backends

Can compile to C, C++, Objective-C, or JavaScript.

## Best Practices (2025)

**Do**:

- **Use `ARC/ORC`**: The default in v2.0. Clean up is deterministic (destructors).
- **Use `f-strings`**: `fmt"Hello {name}"`.
- **Use `karax`**: For frontend (compiling Nim to JS).

**Don't**:

- **Don't mix styles**: Choose PascalCase or camelCase (Nim is style-insensitive but consistency matters).

## References

- [Nim Lang](https://nim-lang.org/)
