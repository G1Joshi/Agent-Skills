---
name: cqrs
description: Expert CQRS (Command Query Responsibility Segregation) assistance covering command handlers, read projections, event denormalization, and asymmetric scaling. Use when separating read and write models, optimizing read performance, or pairing with Event Sourcing.
---

# CQRS (Command Query Responsibility Segregation)

CQRS is a pattern that separates read and update operations for a data store. Instead of using a single model for both, you have a **Command Model** (Write) and a **Query Model** (Read).

## When to Use

- **Asymmetric Read/Write Workloads**: Systems where reads outnumber writes by 100:1 or 1000:1 and require independent horizontal scaling.
- **Complex Reporting & Search Views**: Aggregating data across multiple aggregates into denormalized read stores (Elasticsearch, Read Replicas).
- **Collaboration & High Concurrency**: Optimizing write performance and transactional consistency while delivering instant query responses.
- **Pairing with Event Sourcing**: When state changes are captured as events and read models are asynchronously projected from event streams.

## Quick Start

```typescript
// Command Side (Write) - Optimized for Integrity
class CreateOrderCommand { ... }
class OrderAggregate {
    create(cmd: CreateOrderCommand) {
        // Validate business rules
        // Save to DB (Normalized / Event Store)
    }
}

// Query Side (Read) - Optimized for Speed
class GetOrderSummaryQuery { ... }
class OrderSummaryProjector {
    // Listens to "OrderCreated" event
    on(event) {
        // Update a flat "Read DB" (e.g., ElasticSearch, Redis, Document DB)
        // optimized for the specific UI view
    }
}
```

## Core Concepts

#Separation of Command and Query Models

Commands represent intent to mutate state (void return or ID); Queries request data without side effects:

```
Client
  ├── Command: POST /orders (CreateOrderCommand) ──→ Command Handler ──→ Write DB (Postgres)
  │                                                                           │ (CDC / Events)
  └── Query:   GET /orders/summary (OrderSummary) ←── Read Handler   ←── Read DB (Elastic/Redis)
```

#Command Handlers with Explicit Domain Mutex

Validates permissions and business invariants before committing writes:

```typescript
// commands/cancel-order.command.ts
export interface CancelOrderCommand {
  orderId: string;
  reason: string;
  requestedByUserId: string;
}

export class CancelOrderCommandHandler {
  constructor(private readonly orderRepo: OrderRepositoryPort) {}

  async handle(cmd: CancelOrderCommand): Promise<void> {
    const order = await this.orderRepo.getById(cmd.orderId);
    if (!order) throw new Error("Order not found");
    order.cancel(cmd.reason, cmd.requestedByUserId);
    await this.orderRepo.save(order);
  }
}
```

#Materialized Read Projections

Updates optimized denormalized read views in response to domain events:

```typescript
// projections/order-dashboard.projection.ts
export class OrderDashboardProjection {
  async onOrderCancelled(event: OrderCancelledEvent): Promise<void> {
    await redis.hset(`dashboard:order:${event.orderId}`, {
      status: "CANCELLED",
      cancelledAt: event.timestamp,
      cancellationReason: event.reason,
    });
  }
}
```

## Common Patterns

### Read-Model Projection with Event Handlers

**Problem**: Queries require aggregated data from multiple write models, causing slow and complex database joins.

**Solution**:
Use an asynchronous projector to update a de-normalized, query-optimized document or key-value store:

```typescript
interface OrderCreatedEvent {
  orderId: string;
  customerId: string;
  total: number;
  createdAt: string;
}

class OrderReadModelProjector {
  async handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
    await searchIndex.upsert("orders_summary", event.orderId, {
      id: event.orderId,
      customerId: event.customerId,
      totalAmount: event.total,
      placedAt: event.createdAt,
      status: "PLACED",
    });
  }
}
```

## Best Practices (2026)

**Do**:

- **Make Queries Completely Side-Effect Free**: Ensure queries never mutate database state or trigger transactional locks.
- **Embrace Eventual Consistency**: Design client user experiences to anticipate small projection delays (optimistic UI updates).
- **Optimize Read Models for the UI**: Structure read tables/documents to match the exact view model needed by frontend clients.
- **Use Dedicated Read Replicas**: Direct query handlers to read replicas or fast key-value caches to protect the write primary.

**Don't**:

- **Don't apply CQRS globally to an entire system**: Apply CQRS only to bounded contexts with complex requirements; simple CRUD benefits from standard MVC.
- **Don't share entities between Command and Query pipelines**: Keep query handlers completely independent of domain aggregate classes.
- **Don't let read projections write back to the write store**: Keep the data pipeline unidirectional.

## Troubleshooting

| Error        | Cause                                           | Solution                                                              |
| :----------- | :---------------------------------------------- | :-------------------------------------------------------------------- |
| `Stale Data` | Lag between Command execution and Query update. | UI design updates (spinners/optimistic updates); Check projector lag. |
| `Complexity` | Over-engineering.                               | Revert to simple CRUD if the domain doesn't warrant separation.       |

## References

- [MSDN CQRS Guide](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [Greg Young - CQRS Documents](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
