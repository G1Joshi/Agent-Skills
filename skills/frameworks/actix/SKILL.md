---
name: actix
description: Actix Rust web framework with actors and high performance. Use for Rust APIs.
---

# Actix Web

Actix Web is one of the fastest web frameworks in the world (TechEmpower benchmarks). It uses the **Actor Model** (though less visible in v4) for concurrency.

## When to Use

- **Raw Speed**: When req/sec is the primary metric.
- **Microservices**: Low footprint, high throughput services.
- **WebSockets**: Efficient handling of millions of connections (actix-web-actors).

## Core Concepts

### App Factory

`App::new()` is a factory called for each thread. State must be wrapped in `web::Data`.

### Extractors

Similar to Axum, but uses `web::Json`, `web::Path`.

### Actors (Actix)

The underlying system for async messages (optional in simple web apps but heavily used for WebSockets).

## Best Practices (2025)

**Do**:

- **Use `web::Data`**: For shared application state (DB pools).
- **Use `actix_web::main`**: The macro to run the async runtime.

**Don't**:

- **Don't block the thread**: Actix is single-threaded per worker. Blocking operations stop the world.

## References

- [Actix Web Documentation](https://actix.rs/)
