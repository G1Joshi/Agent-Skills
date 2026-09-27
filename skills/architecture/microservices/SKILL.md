---
name: microservices
description: Expert Microservices architecture assistance covering service decomposition, service discovery, distributed tracing, circuit breakers, and database-per-service isolation. Use when refactoring monoliths, designing distributed microservice systems, or orchestrating service communications.
---

# Microservices

Microservices architecture structures an application as a collection of loosely coupled, independently deployable services. Ideally, each service corresponds to a **Bounded Context** (DDD).

## When to Use

- **Independent Scaling & Deployment**: Different business capabilities (e.g. video processing vs user authentication) require independent scaling.
- **Autonomous Multi-Team Velocity**: Large engineering organizations where decoupled cross-functional teams need to deploy without stepping on each other.
- **Polyglot Technology Requirements**: Leveraging specific runtimes for specific workloads (Python for ML, Go/Rust for networking, Node for APIs).
- **Fault Domain Isolation**: Preventing an out-of-memory crash in a non-critical feature from bringing down the core payment pipeline.

## Quick Start

```yaml
# docker-compose.yml (Simulated Microservices)
services:
  order-service:
    build: ./services/order
    ports: ["3001:3000"]
    environment:
      - DB_HOST=order-db

  inventory-service:
    build: ./services/inventory
    ports: ["3002:3000"]

  api-gateway:
    image: nginx
    ports: ["80:80"]
    depends_on:
      - order-service
      - inventory-service
```

## Core Concepts

#Database-Per-Service Isolation

Each microservice owns its private database. No service can directly query another service's database tables:

```
[ Orders Service ] ──→ ( Orders DB )
        │ (Async Events / gRPC)
        ▼
[ Customers Service ] ──→ ( Customers DB )
```

#Distributed Tracing (W3C Trace Context)

Correlates requests across multiple network hops using standardized trace IDs:

```typescript
// Injected into outgoing HTTP/gRPC calls
headers: {
  "traceparent": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01"
}
```

#Circuit Breakers & Graceful Degradation

Fails fast when downstream services become unresponsive, preventing cascading thread exhaustion:

```typescript
import CircuitBreaker from "opossum";

const breaker = new CircuitBreaker(callRecommendationService, {
  timeout: 1000,
  errorThresholdPercentage: 50,
  resetTimeout: 10000,
});

breaker.fallback(() => [/* Fallback cached generic recommendations */]);
const recommendations = await breaker.fire(userId);
```

## Common Patterns

#Circuit Breaker Pattern
**Problem**: Cascading failures when a downstream dependency experiences degraded response times.  
**Solution**: Wrap external calls in a circuit breaker to fail fast and shed load.

```typescript
import CircuitBreaker from "opossum";

async function fetchPaymentGateway(payload: PaymentPayload) {
  return await http.post("https://payment.example.com/charge", payload);
}

const breaker = new CircuitBreaker(fetchPaymentGateway, {
  timeout: 3000, // 3s timeout
  errorThresholdPercentage: 50, // Open breaker if 50% calls fail
  resetTimeout: 10000, // Wait 10s before attempting half-open state
});

breaker.fallback(() => ({ status: "QUEUED_FOR_RETRY", cached: true }));
const result = await breaker.fire(paymentData);
```

## Best Practices (2026)

**Do**:

- **Enforce Database-per-Service**: Never share a database instance between microservices; communicate via APIs or events.
- **Implement Comprehensive Observability**: Instrument all services with OpenTelemetry traces, Prometheus metrics, and structured JSON logs.
- **Use Contract Testing (Pact)**: Validate API compatibility between consumer and provider services in CI/CD without running end-to-end clusters.
- **Adopt Service Meshes for Mesh Security**: Leverage Envoy / Istio for automated mTLS encryption and traffic steering.

**Don't**:

- **Don't start with microservices on day one**: Start with a well-structured Modular Monolith until organizational scale warrants extraction.
- **Don't build distributed monoliths**: Avoid deep synchronous HTTP chains (Service A calls B, which calls C, which calls D).
- **Don't ignore distributed transactions**: Use Saga patterns or eventual consistency rather than two-phase commits.

## Troubleshooting

| Error                | Cause                                          | Solution                                                               |
| :------------------- | :--------------------------------------------- | :--------------------------------------------------------------------- |
| `Cascading Failure`  | One service down takes down others.            | Use Circuit Breakers and Timeouts.                                     |
| `Data inconsistency` | Async updates failed.                          | Implement Sagas and Idempotent consumers.                              |
| `Latency`            | Too many hops (service -> service -> service). | Use Caching, Aggregation at Gateway, or Event-Driven data replication. |

## References

- [Building Microservices (Sam Newman)](https://samnewman.io/books/building_microservices/)
- [Microservices Patterns (Chris Richardson)](https://microservices.io/)
