---
name: actix
description: >-
  Build REST endpoints, configure middleware, set up routing, and manage
  application state with actix-web in Rust. Use when building Rust web
  servers, HTTP services, REST APIs with actix-web, or when the user
  mentions Actix, actix-web, extractors, or high-performance Rust web
  applications.
---

# Actix Web

## When to Use

- **Raw Speed**: When req/sec is the primary metric (TechEmpower benchmarks).
- **Microservices**: Low footprint, high throughput services.
- **WebSockets**: Efficient handling of millions of connections (actix-web-actors).

## Workflow

1. Create project: `cargo new my-api && cd my-api`
2. Add `actix-web = "4"`, `serde`, `tokio` to `Cargo.toml`
3. Write handlers with extractors (`web::Json`, `web::Path`, `web::Query`)
4. Register routes via `App::new().route(...)` or `web::scope(...)`
5. Wrap with middleware (`Logger`, `Compress`, `DefaultHeaders`)
6. Run: `cargo run` and test: `curl http://127.0.0.1:8080/health`

## Quick Reference

| Concept | Pattern |
|---|---|
| Shared state | `web::Data<T>` wrapping `Mutex` or pool |
| JSON body | `web::Json<T>` extractor (T: Deserialize) |
| Path param | `web::Path<T>` extractor |
| Query string | `web::Query<T>` extractor |
| Route groups | `web::scope("/api/v1").route(...)` |
| Blocking work | `web::block(move \|\| ...)` to offload CPU-bound tasks |
| Custom errors | Implement `error::ResponseError` trait |
| Entry macro | `#[actix_web::main]` on async main |

## Error Recovery

| Problem | Fix |
|---|---|
| Thread blocking stalls workers | Move to `web::block()` or spawn on dedicated runtime |
| State not shared across workers | Wrap in `web::Data::new()` before `HttpServer::new` |
| Extractor fails silently | Configure `JsonConfig::error_handler` for custom error responses |
| Port already in use | Check for running processes or use `.bind("0.0.0.0:0")` for random port |

## References

- [Actix Web Documentation](https://actix.rs/docs)
- [Actix Web API Reference](https://docs.rs/actix-web/latest/actix_web/)
