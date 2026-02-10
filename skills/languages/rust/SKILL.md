---
name: rust
description: Rust programming with ownership, borrowing, lifetimes, and zero-cost abstractions. Use for .rs files.
---

# Rust

A language empowering everyone to build reliable and efficient software.

## When to Use

- Systems programming (drivers, OS)
- WebAssembly
- Performance-critical applications
- Command-line tools (great developer experience)

## Quick Start

```rust
fn main() {
    println!("Hello, World!");

    let mut x = 5; // mutable
    x = 6;

    let y = 10; // immutable by default
}
```

## Core Concepts

### Ownership & Borrowing

The borrow checker ensures rules are followed at compile time.

- Each value has a single **owner**.
- You can have multiple **immutable borrows** OR one **mutable borrow**, but not both simultaneously.

### Lifetimes

Ensuring references remain valid for as long as they are used.

### Traits

Similar to interfaces, defining shared behavior.

## Best Practices

**Do**:

- Embrace the borrow checker (it's your friend)
- Use `Result<T, E>` and `Option<T>` for error handling
- Use `cargo clippy` for linting
- Use `match` for exhaustive pattern matching

**Don't**:

- Use `unsafe` unless absolutely necessary
- `unwrap()` in production code (use proper error handling)

## References

- [The Rust Programming Language Book](https://doc.rust-lang.org/book/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
