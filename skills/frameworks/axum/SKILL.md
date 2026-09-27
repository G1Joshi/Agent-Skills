---
name: axum
description: Expert Axum web framework assistance covering routing, extractors, tower middleware, and hyper-powered Rust async microservices. Use when building idiomatic, type-safe, ergonomic REST APIs in Rust.
---

# Axum

Axum is the most popular web framework in the Rust ecosystem (tokio). v0.7 (2024/2025) is built on **Hyper 1.0** and standardizes the service trait.

## When to Use

- **Modern Asynchronous Rust Web Services**: Building RESTful APIs and microservices directly within the Tokio ecosystem.
- **Tower Middleware Integration**: Leveraging Tower's rich ecosystem of rate-limiting, timeouts, retries, and tracing.
- **Modular Type-Safe Route Handlers**: Combining extractors, route routers, and shared state seamlessly.
- **High-Performance WebSockets & SSE**: Real-time event streaming and live pub/sub endpoints in Rust.

## Quick Start

```rust
use axum::{routing::get, Json, Router};
use serde::Serialize;
use std::net::SocketAddr;

#[derive(Serialize)]
struct Status {
    healthy: bool,
}

async fn health_check() -> Json<Status> {
    Json(Status { healthy: true })
}

#[tokio::main]
async fn main() {
    let app = Router::new().route("/health", get(health_check));
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

## Core Concepts

#Type-Safe State & Modular Routers

Sharing dependency-injected state across route modules:

```rust
use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::IntoResponse,
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::net::TcpListener;

#[derive(Clone)]
struct AppState {
    db_pool: Arc<String>, // Mock connection pool
}

#[derive(Serialize, Deserialize)]
struct User {
    id: u64,
    username: String,
}

async fn get_user(
    Path(user_id): Path<u64>,
    State(state): State<AppState>,
) -> Result<Json<User>, StatusCode> {
    Ok(Json(User {
        id: user_id,
        username: format!("user_{user_id}"),
    }))
}

#[tokio::main]
async fn main() {
    let state = AppState {
        db_pool: Arc::new("postgres://localhost:5432/app".into()),
    };

    let app = Router::new()
        .route("/users/{id}", get(get_user))
        .with_state(state);

    let listener = TcpListener::bind("0.0.0.0:3000").await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
```

#Tower Middleware & Tracing Layers

Adding structured logging, timeouts, and CORS layers:

```rust
use axum::Router;
use tower_http::cors::{Any, CorsLayer};
use tower_http::trace::TraceLayer;
use tower::ServiceBuilder;
use std::time::Duration;

fn configure_middleware(app: Router) -> Router {
    let middleware_stack = ServiceBuilder::new()
        .layer(TraceLayer::new_for_http())
        .layer(
            CorsLayer::new()
                .allow_origin(Any)
                .allow_methods(Any)
                .allow_headers(Any),
        )
        .layer(tower_http::timeout::TimeoutLayer::new(Duration::from_secs(10)));

    app.layer(middleware_stack)
}
```

#Custom Extractor with Error Rejections

Validating custom headers or authentication tokens:

```rust
use axum::{
    async_trait,
    extract::FromRequestParts,
    http::{request::Parts, StatusCode},
};

struct AuthToken(String);

#[async_trait]
impl<S> FromRequestParts<S> for AuthToken
where
    S: Send + Sync,
{
    type Rejection = (StatusCode, &'static str);

    async fn from_request_parts(parts: &mut Parts, _state: &S) -> Result<Self, Self::Rejection> {
        let auth_header = parts
            .headers
            .get("Authorization")
            .and_then(|val| val.to_str().ok());

        match auth_header {
            Some(token) if token.starts_with("Bearer ") => {
                Ok(AuthToken(token[7..].to_string()))
            }
            _ => Err((StatusCode::UNAUTHORIZED, "Missing or invalid token")),
        }
    }
}
```

## Common Patterns

### Dependency Injection with State Extractor

**Problem**: Sharing connection pools and config structs across handlers safely in Axum.

**Solution**:
Use `Router::with_state` and `State` extractor:

```rust
use axum::{extract::State, routing::get, Router};
use std::sync::Arc;

#[derive(Clone)]
struct AppConfig {
    api_key: Arc<String>,
}

async fn show_config(State(config): State<AppConfig>) -> String {
    format!("Configured key: {}", config.api_key)
}

fn create_app() -> Router {
    let config = AppConfig { api_key: Arc::new("secret-token".into()) };
    Router::new().route("/config", get(show_config)).with_state(config)
}
```

## Best Practices (2026)

- **Do** use `axum::serve` and `tokio::net::TcpListener` for modern Axum 0.7+ applications.
- **Do** place `State` extractors as the last extractor argument in handler signatures.
- **Do** use `Router::with_state` to ensure compiler verification of matching state types across nested subrouters.
- **Do** implement `IntoResponse` for domain error enums to decouple error formatting from route handlers.
- **Don't** block async worker threads; offload blocking operations with `tokio::task::spawn_blocking`.
- **Don't** expose internal database error details directly in HTTP error responses.
- **Don't** create separate Tokio runtimes inside handlers; utilize the existing ambient runtime.

## Troubleshooting

| Error                                                  | Cause                                                                         | Solution                                                                             |
| :----------------------------------------------------- | :---------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| `the trait Bound '...: FromRef<...>' is not satisfied` | Sub-state extractor cannot be derived from global state.                      | Implement `FromRef` for child state fields or derive `Clone` on entire State struct. |
| `the trait 'Handler' is not implemented for fn ...`    | Handler signature has invalid parameter order; State/Body extractor not last. | Ensure `Json` or body extractor is the final parameter in the handler argument list. |
| `connection closed before message completed`           | Handler dropped response future without finishing write.                      | Check for panics in background tasks or Tokio runtime shutdown.                      |

## References

- [Axum Documentation](https://docs.rs/axum/latest/axum/)
