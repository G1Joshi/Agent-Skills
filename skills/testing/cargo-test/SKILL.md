---
name: cargo-test
description: Expert Cargo test assistance covering Rust unit tests, integration tests, and benchmarks. Use when running `cargo test`, writing unit tests in Rust, or debugging test failures.
---

# Cargo Test

Rust treats testing as a first-class citizen. `cargo test` runs unit tests (in the same file), integration tests (in `tests/`), and uniquely, Documentation Tests (code blocks in your doc comments).

## When to Use

- **Rust Unit & Integration Testing**: The official, built-in test runner for Rust crates, libraries, and binaries.
- **Doc-Tests Verification**: Compiling and testing code examples written inside `///` documentation comments automatically.
- **Benchmark & Micro-Optimizations**: Measuring algorithmic performance and allocations using `cargo bench` and criterion.
- **Concurrency & Parallel Test Execution**: Running hundreds of test threads safely with thread isolation by default.

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

### Unit Tests vs Integration Tests Layout

Unit tests live inside `src/` adjacent to source modules with `#[cfg(test)]`; integration tests live in root `tests/`:

```text
my_crate/
  ├── src/
  │   └── parser.rs          # Contains #[cfg(test)] mod tests { ... }
  └── tests/
      └── integration_test.rs # Compiles as an external crate consuming public API
```

### Test Attributes & Failure Assertions

Rust provides idiomatic test macros and expected failure annotations:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_transaction() {
        let account = Account::new("Alice", 100);
        assert_eq!(account.balance(), 100);
        assert!(account.is_active());
    }

    #[test]
    #[should_panic(expected = "insufficient funds")]
    fn test_overdraw_panics() {
        let mut account = Account::new("Bob", 20);
        account.withdraw(50); // triggers panic
    }
}
```

### Filtering & Concurrency Flags

Targeting specific tests and controlling execution threads:

```bash
# Run only tests matching substring "auth"
cargo test auth

# Run tests serially to prevent database race conditions
cargo test -- --test-threads=1

# Show stdout print output from passing tests
cargo test -- --nocapture
```

## Common Patterns

### Integration Testing in Separate Directory

**Problem**: Testing public crate APIs as an external consumer without access to internal private members.

**Solution**:
Place integration test suites in the top-level `tests/` directory:

```rust
// tests/integration_test.rs
use my_crate::{add, calculate_total};

#[test]
fn test_public_api_flow() {
    let result = add(2, 3);
    assert_eq!(result, 5);
    assert!(calculate_total(&[1, 2, 3]) > 0);
}
```

## Best Practices

**Do**:

- Annotate Test Modules with `#[cfg(test)]`: Prevent test code and mock dependencies from being compiled into release production binaries.
- Use `cargo-nextest` in CI: Adopt Nextest (`cargo install cargo-nextest`) for faster parallel test execution and cleaner failure summaries.
- Write Instructive Doc-Tests: Use `///` code examples on public structs to keep documentation verified and up to date.
- Leverage Test Fixtures with Tempdir: Use crates like `tempfile` for testing filesystem mutations in isolated temporary folders.

**Don't**:

- Share mutable global state across parallel tests: Tests run in parallel by default; shared static variables cause intermittent test flakiness.
- Ignore compiler warnings in tests: Run `cargo clippy --tests` to enforce identical code quality on test suites.
- Ignore `--release` test runs: Test critical numerical code with `cargo test --release` to catch overflow behavior.

## Troubleshooting

| Error                                      | Cause                                                      | Solution                                                                   |
| :----------------------------------------- | :--------------------------------------------------------- | :------------------------------------------------------------------------- |
| `test failed, to rerun use -- --nocapture` | Standard output swallowed during passing or failing tests. | Run `cargo test -- --nocapture` to stream stdout and tracing logs.         |
| `cannot find module in tests/`             | Missing `pub` visibility on crate modules.                 | Expose target helper functions with `pub` or `pub(crate)` in `src/lib.rs`. |
| `failed to link or test threads panic`     | Shared state race condition across parallel test runners.  | Run sequentially using `cargo test -- --test-threads=1`.                   |

## References

- [Rust Book - Testing](https://doc.rust-lang.org/book/ch11-01-writing-tests.html)
