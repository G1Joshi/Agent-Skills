---
name: cqrs
description: CQRS command query responsibility segregation. Use for complex domains.
---

# CQRS (Command Query Responsibility Segregation)

CQRS is a pattern that separates read and update operations for a data store. Instead of using a single model for both, you have a **Command Model** (Write) and a **Query Model** (Read).

## When to Use

- **High Disparity**: Read load is 1000x higher than Write load (or vice versa).
- **Complex UI**: The UI needs data shaped differently than the way it's stored (e.g., Dashboard aggregation).
- **Event Sourcing**: CQRS is almost mandatory for Event Sourcing.

## Quick Start (Conceptual)

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

### Separation

- **Commands**: Intent to change state. Void return type (or Ack). Strict validation.
- **Queries**: Request for data. No side effects. Returns DTOs.

### Synchronization

The Read DB is eventually consistent with the Write DB. Logic (Projectors) syncs them via Events.

## Best Practices

**Do**:

- Start with **Logical CQRS** (Separate classes, same DB) before Physical CQRS (Separate DBs).
- accept **Eventual Consistency** in the UI (Optimistic UI updates).

**Don't**:

- Don't use CQRS for simple CRUD (It adds massive complexity).
- Don't try to make the Read side fully real-time synchronized (You'll lose the scaling usage).

## Troubleshooting

| Error        | Cause                                           | Solution                                                              |
| :----------- | :---------------------------------------------- | :-------------------------------------------------------------------- |
| `Stale Data` | Lag between Command execution and Query update. | UI design updates (spinners/optimistic updates); Check projector lag. |
| `Complexity` | Over-engineering.                               | Revert to simple CRUD if the domain doesn't warrant separation.       |

## References

- [MSDN CQRS Guide](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs)
- [Greg Young - CQRS Documents](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf)
