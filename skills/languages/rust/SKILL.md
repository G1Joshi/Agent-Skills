---
name: rust
description: Expert Rust systems programming assistance covering ownership, borrowing, lifetimes, async/await, and error handling. Use when building high-performance CLI tools, network services, WebAssembly, or safe systems software.
---

# Rust

A language empowering everyone to build reliable and efficient software.

## When to Use

- **High-Performance Systems Programming**: Game engines, operating system kernels, databases, and network proxies requiring deterministic execution.
- **Memory-Safe Concurrency Without Garbage Collection**: Eliminating data races and null-pointer dereferences at compile time via the borrow checker.
- **High-Throughput Asynchronous Network Services**: Building backends with Tokio, Axum, Actix-web, or Tower.
- **WebAssembly (Wasm) Micro-Modules**: Compiling ultra-fast, small-footprint binaries for edge runtimes and browsers.

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

### Ownership, Borrowing & Lifetimes

Rust guarantees memory safety without a GC using compile-time affine type systems:

```rust
// Ownership transfer vs borrowing
fn process_buffer(mut data: Vec<u8>) -> usize {
    data.push(0xFF);
    data.len()
} // data deallocated here

fn inspect_slice(slice: &[u8]) {
    for byte in slice {
        print!("{byte:02X} ");
    }
}

// Explicit lifetime annotation on struct holding references
struct TokenView<'a> {
    raw: &'a str,
    prefix: &'a str,
}

impl<'a> TokenView<'a> {
    fn from_token(token: &'a str) -> Option<Self> {
        let (prefix, _) = token.split_once(':')?;
        Some(Self { raw: token, prefix })
    }
}
```

### Robust Error Handling with Result & Thiserror

Idiomatic domain error modeling without runtime exceptions:

```rust
use std::io;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ServiceError {
    #[error("network I/O failed: {0}")]
    Io(#[from] io::Error),
    #[error("invalid header value: {key}")]
    InvalidHeader { key: String },
    #[error("resource not found with ID {0}")]
    NotFound(u64),
}

pub type Result<T> = std::result::Result<T, ServiceError>;

pub fn validate_and_parse(id: u64, header: &str) -> Result<String> {
    if header.is_empty() {
        return Err(ServiceError::InvalidHeader {
            key: "Authorization".into(),
        });
    }
    if id == 0 {
        return Err(ServiceError::NotFound(id));
    }
    Ok(format!("Authorized: {header} for user {id}"))
}
```

### Asynchronous Concurrency with Tokio & Channels

Structured async tasks communicating over bounded multi-producer, single-consumer channels:

```rust
use tokio::sync::mpsc;
use tokio::task;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let (tx, mut rx) = mpsc::channel::<String>(32);

    let producer = task::spawn(async move {
        for i in 1..=5 {
            tx.send(format!("event-{i}")).await.unwrap();
        }
    });

    let consumer = task::spawn(async move {
        while let Some(msg) = rx.recv().await {
            println!("Processed: {msg}");
        }
    });

    let _ = tokio::join!(producer, consumer);
    Ok(())
}
```

## Common Patterns

### Custom Error Types with `thiserror` and `Result`

**Problem**: Returning string errors or unstructured panics makes error handling brittle for API consumers.

**Solution**:
Define domain error enums using `thiserror`:

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ApiError {
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("User not found with ID {0}")]
    NotFound(i64),
    #[error("Unauthorized access")]
    Unauthorized,
}

pub type Result<T> = std::result::Result<T, ApiError>;

pub fn get_user(id: i64) -> Result<String> {
    if id <= 0 {
        return Err(ApiError::NotFound(id));
    }
    Ok(format!("User #{}", id))
}
```

## Best Practices

**Do**:

- Leverage Clippy lints (`cargo clippy -- -D warnings`) and automated formatting in CI pipelines.
- Favor custom `enum` errors with `thiserror` for libraries, and `anyhow` for top-level binaries and CLIs.
- Use `Arc<tokio::sync::RwLock<T>>` or actor channels rather than standard blocking mutexes in asynchronous code.
- Prefer iterator combinators (`map`, `filter`, `fold`) over explicit index loops for zero-cost performance optimization.

**Don't**:

- Use `.unwrap()` in production paths; use `.expect("descriptive context")` or the `?` question mark operator.
- Default to `.clone()` to satisfy the borrow checker; restructure ownership or borrow references whenever possible.
- Write `unsafe` blocks without documented `// SAFETY:` invariants explaining why undefined behavior cannot occur.

## Troubleshooting

| Error                                                   | Cause                                                                       | Solution                                                                                       |
| :------------------------------------------------------ | :-------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| `cannot borrow ... as mutable more than once at a time` | Rust borrow checker preventing data races with multiple mutable references. | Narrow the scope of the borrow or clone data if necessary.                                     |
| `value borrowed here after move`                        | Variable ownership transferred to another function or scope.                | Pass a reference `&val` instead of transferring ownership, or implement `Clone`.               |
| `lifetime may not live long enough`                     | Reference returned from function lacks sufficient lifetime specifier.       | Return owned data (e.g. `String` instead of `&str`) or add explicit lifetime annotations `'a`. |

## References

- [The Rust Programming Language Book](https://doc.rust-lang.org/book/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
