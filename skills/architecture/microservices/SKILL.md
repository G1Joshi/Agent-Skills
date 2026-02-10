---
name: microservices
description: Microservices distributed architecture pattern. Use for scalable systems.
---

# Microservices

Microservices architecture structures an application as a collection of loosely coupled, independently deployable services. Ideally, each service corresponds to a **Bounded Context** (DDD).

## When to Use

- Large teams (50+ devs) where coordination on a monolith slows down deployment.
- Modules have conflicting resource requirements (e.g., one needs huge RAM, another needs GPU).
- Need to scale specific parts of the system independently.
- **2025 Reality check**: Don't start with Microservices. Start with a Modular Monolith.

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

### Independence

Each service owns its own data. Service A cannot query Service B's database directly; it must ask Service B via API.

### Inter-Service Communication

- **Synchronous**: HTTP/REST or gRPC (Request/Response). Tightly coupled in time.
- **Asynchronous**: Message Queues (RabbitMQ, Kafka, SQS). Decoupled in time.

### Database per Service

Ensures loose coupling. If a service needs data from another, use data replication (Events) or API composition.

## Common Patterns

### API Gateway

A single entry point for all clients. Handles routing, auth, rate limiting, and aggregation.

### Circuit Breaker

Detects failures and prevents the application from trying to perform the action that is doomed to fail (e.g., external service down), protecting the system.

### Saga Pattern

Managing distributed transactions. Since you can't have ACID across services, use Sagas (sequence of local transactions) with compensating actions for rollbacks.

## Best Practices

**Do**:

- Automate **CI/CD** and **Infrastructure as Code** (Terraform/K8s). You can't manage 50 services manually.
- Implement **Distributed Tracing** (OpenTelemetry) immediately.
- Define clear **Service Boundaries** (use DDD).

**Don't**:

- Don't share code libraries for domain logic (leads to "Distributed Monolith"). Share utils only.
- Don't use synchronous calls for everything (cascading failures).
- Don't underestimate the **Operational Complexity** (Logging, Monitoring, Auth).

## Troubleshooting

| Error                | Cause                                          | Solution                                                               |
| :------------------- | :--------------------------------------------- | :--------------------------------------------------------------------- |
| `Cascading Failure`  | One service down takes down others.            | Use Circuit Breakers and Timeouts.                                     |
| `Data inconsistency` | Async updates failed.                          | Implement Sagas and Idempotent consumers.                              |
| `Latency`            | Too many hops (service -> service -> service). | Use Caching, Aggregation at Gateway, or Event-Driven data replication. |

## References

- [Building Microservices (Sam Newman)](https://samnewman.io/books/building_microservices/)
- [Microservices Patterns (Chris Richardson)](https://microservices.io/)
