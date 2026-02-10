---
name: axum
description: Axum ergonomic Rust web framework with tower. Use for Rust APIs.
---

# Axum

Axum is the most popular web framework in the Rust ecosystem (tokio). v0.7 (2024/2025) is built on **Hyper 1.0** and standardizes the service trait.

## When to Use

- **High Performance**: When you need millisecond latency (e.g., ad tech, gaming).
- **Rust Backend**: The default choice for new Rust web projects.
- **Type Safety**: Extractor pattern guarantees types at compile time.

## Core Concepts

### Extractors

Declarative data parsing: `async fn handler(Json(body): Json<CreateUser>)`.

### Middleware (Tower)

Axum uses `tower` middleware, meaning you can use any middleware from the ecosystem (timeout, tracing, rate-limit).

### Handlers

Async functions that implementation `IntoResponse`.

## Best Practices (2025)

**Do**:

- **Use `axum::serve`**: v0.7 replacement for `Server::bind`.
- **Use `sqlx`**: The standard async SQL query builder for Axum.
- **Use `tracing`**: For structured logging.

**Don't**:

- **Don't unwrap**: Handle errors with `Result<impl IntoResponse, AppError>`.

## References

- [Axum Documentation](https://docs.rs/axum/latest/axum/)
