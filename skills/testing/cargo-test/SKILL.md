---
name: cargo-test
description: Cargo test for Rust testing. Use for Rust testing.
---

# Cargo Test

Rust treats testing as a first-class citizen. `cargo test` runs unit tests (in the same file), integration tests (in `tests/`), and uniquely, Documentation Tests (code blocks in your doc comments).

## When to Use

- **Rust Projects**: The standard.
- **Library Design**: Doc tests ensure your examples in README/Docs actually compile and work.

## Quick Start

```rust
// lib.rs
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(add(2, 2), 4);
    }
}
```

## Core Concepts

### Unit vs Integration

- **Unit**: Inside `src/lib.rs` (or same file). Can test private functions.
- **Integration**: Inside `tests/*.rs`. Can only use the public API (like a real user).

### Doc Tests

Code blocks in `///` comments are run as tests.

````rust
/// Adds two numbers.
/// ```
/// let result = my_crate::add(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn add...
````

### Assertions

`assert!`, `assert_eq!`, `assert_ne!`. `#[should_panic]` for testing errors.

## Best Practices (2025)

**Do**:

- **Use `insta`**: For snapshot testing in Rust (`cargo-insta`).
- **Use `rstest`**: For fixture-based and parameterized testing (Pytest style).
- **Test concurrency**: Rust's ownership model makes testing concurrent code safer, but still verify with `loom` for atomics.

**Don't**:

- **Don't test implementation details in integration tests**: Keep `tests/` folder for Public API contracts only.

## References

- [Rust Book - Testing](https://doc.rust-lang.org/book/ch11-01-writing-tests.html)
