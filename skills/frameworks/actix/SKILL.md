---
name: actix
description: Expert Actix Web assistance covering async actors, routing, extractors, middleware, and high-performance Rust web services. Use when building blazing fast REST APIs or microservices in Rust.
---

# Actix Web

Actix Web is one of the fastest web frameworks in the world (TechEmpower benchmarks). It uses the **Actor Model** (though less visible in v4) for concurrency.

## When to Use

- **Ultra-High Throughput Rust Microservices**: Systems demanding sub-millisecond response times and millions of requests per second.
- **Actor-Based Asynchronous Workloads**: Applications utilizing the Actix actor model alongside HTTP routing.
- **Low-Latency WebSockets & Streaming**: Real-time telemetry, chat engines, and financial quote tickers.
- **Resource-Constrained Edge Services**: Zero-cost abstraction web services requiring minimal resident memory.

## Quick Start

```rust
use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize)]
struct User {
    id: u32,
    name: String,
}

#[get("/api/users/{id}")]
async fn get_user(path: web::Path<u32>) -> impl Responder {
    let user_id = path.into_inner();
    HttpResponse::Ok().json(User { id: user_id, name: "Alice".into() })
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    HttpServer::new(|| App::new().service(get_user))
        .bind(("127.0.0.1", 8080))?
        .run()
        .await
}
```

## Core Concepts

### Application State & Scoped Handlers

Thread-safe shared mutable and immutable state injected via extractors:

```rust
use actix_web::{web, App, HttpResponse, HttpServer, Responder};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

struct AppState {
    request_counter: Arc<AtomicUsize>,
    app_version: &'static str,
}

async fn metrics_handler(data: web::Data<AppState>) -> impl Responder {
    let count = data.request_counter.fetch_add(1, Ordering::SeqCst);
    HttpResponse::Ok().json(serde_json::json!({
        "version": data.app_version,
        "total_requests": count + 1
    }))
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let state = web::Data::new(AppState {
        request_counter: Arc::new(AtomicUsize::new(0)),
        app_version: "2026.1.0",
    });

    HttpServer::new(move || {
        App::new()
            .app_data(state.clone())
            .route("/metrics", web::get().to(metrics_handler))
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}
```

### Custom Middleware Pipeline

Intercepting requests and responses with Actix transform middleware:

```rust
use actix_web::dev::{Service, ServiceRequest, ServiceResponse, Transform};
use actix_web::Error;
use futures::future::{ok, LocalBoxFuture, Ready};

pub struct RequestTiming;

impl<S, B> Transform<S, ServiceRequest> for RequestTiming
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type InitError = ();
    type Transform = RequestTimingMiddleware<S>;
    type Future = Ready<Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future {
        ok(RequestTimingMiddleware { service })
    }
}

pub struct RequestTimingMiddleware<S> {
    service: S,
}

impl<S, B> Service<ServiceRequest> for RequestTimingMiddleware<S>
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type Future = LocalBoxFuture<'static, Result<Self::Response, Self::Error>>;

    fn poll_ready(&self, cx: &mut std::task::Context<'_>) -> std::task::Poll<Result<(), Self::Error>> {
        self.service.poll_ready(cx)
    }

    fn call(&self, req: ServiceRequest) -> Self::Future {
        let fut = self.service.call(req);
        Box::pin(async move {
            let res = fut.await?;
            Ok(res)
        })
    }
}
```

### Type-Safe Request Extraction & Validation

Validating incoming JSON payloads using extractor guards:

```rust
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct CreateUserRequest {
    username: String,
    email: String,
}

#[derive(Serialize)]
struct UserResponse {
    id: u64,
    username: String,
    status: &'static str,
}

async fn create_user(payload: web::Json<CreateUserRequest>) -> impl Responder {
    if payload.username.is_empty() {
        return HttpResponse::BadRequest().body("Username cannot be empty");
    }
    HttpResponse::Created().json(UserResponse {
        id: 42,
        username: payload.username.clone(),
        status: "active",
    })
}
```

## Common Patterns

### Shared State with Arc and Mutex (Data Extractor)

**Problem**: Safely sharing database pools or in-memory caches across multi-threaded Actix worker threads.

**Solution**:
Use `web::Data` to wrap application state:

```rust
use actix_web::{web, App, HttpServer, Responder};
use std::sync::Mutex;

struct AppState {
    counter: Mutex<i32>,
}

async fn count(data: web::Data<AppState>) -> impl Responder {
    let mut counter = data.counter.lock().unwrap();
    *counter += 1;
    format!("Request count: {}", *counter)
}

// In main: App::new().app_data(web::Data::new(AppState { counter: Mutex::new(0) }))
```

## Best Practices

**Do**:

- Wrap heavy CPU-bound or blocking operations in `web::block()` to prevent starving the Actix event loop.
- Share state using `web::Data<T>` (which uses internal `Arc`) rather than cloning heavy heap resources per worker thread.
- Enable compression middleware (`actix_web::middleware::Compress`) and default structured JSON logging (`tracing-actix-web`).
- Define route scopes (`web::scope("/api/v1")`) to group route hierarchies and auth middlewares.

**Don't**:

- Use synchronous `std::fs` or `std::net` inside handlers; use Tokio async equivalents.
- Use `unwrap()` inside async handler bodies; return `Result<HttpResponse, actix_web::Error>`.
- Store thread-local storage if handlers need to yield across `.await` points.

## Troubleshooting

| Error                                                   | Cause                                                                          | Solution                                                                         |
| :------------------------------------------------------ | :----------------------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| `the trait Bound '...: ResponseError' is not satisfied` | Returning custom error type from handler without implementing `ResponseError`. | Derive `thiserror::Error` and implement `actix_web::ResponseError`.              |
| `App data is not configured for type ...`               | Extractor requesting type not registered in `app_data(web::Data::new(...))`.   | Register the exact type wrapped in `web::Data` inside `HttpServer::new` closure. |
| `Cannot bind address: Address already in use`           | Port 8080 already bound by another process.                                    | Change port or kill blocking process with `fuser -k 8080/tcp`.                   |

## References

- [Actix Web Documentation](https://actix.rs/)
