---
name: crystal
description: Crystal Ruby-like syntax with static typing. Use for .cr files.
---

# Crystal

Crystal compiles to native code (using LLVM) but looks exactly like Ruby. v1.12 continues improving **Windows support** and parallelism.

## When to Use

- **Performance sensitive Rubyists**: Porting heavy Ruby scripts to Crystal for 50x speedup.
- **Microservices**: Low memory footprint compared to JVM/Ruby.
- **CLI Tools**: Fast startup and execution.

## Core Concepts

### Fibers

Lightweight concurrency (like Go routines). `spawn { ... }`.

### Macros

Generate code at compile time (like Zig/Lisp).

### Union Types

`String | Int32`. The compiler handles the branching.

## Best Practices (2025)

**Do**:

- **Use strict types in APIs**: Help the compiler with `def foo(x : Int32)`.
- **Use `shards`**: Dependency manager.
- **Use `-Dpreview_mt`**: To test multithreading capabilities.

**Don't**:

- **Don't use `eval`**: Crystal is compiled, there is no runtime eval.

## References

- [Crystal Lang](https://crystal-lang.org/)
