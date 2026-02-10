---
name: event-sourcing
description: Event sourcing event-based persistence. Use for audit trails.
---

# Event Sourcing

Event Sourcing ensures that all changes to application state are stored as a sequence of events. We don't just store the current state; we store "what happened".

## When to Use

- **Audit Logs**: When you need to know exactly how you got to the current state (Banking, Legal).
- **Temporal Queries**: "What did the system look like last Tuesday?".
- **Intent Capture**: distinguishing between "Correction" vs "Update".

## Quick Start (Conceptual)

**Traditional (State Stored):**
`Order { id: 1, status: 'Shipped' }` -> Update to 'Delivered' -> `Order { id: 1, status: 'Delivered' }` (History lost)

**Event Sourcing (Events Stored):**

1. `OrderCreated(id=1)`
2. `PaymentReceived(id=1)`
3. `OrderShipped(id=1)`
4. `OrderDelivered(id=1)`

To get current state: Replay (1) + (2) + (3) + (4).

## Core Concepts

### Event Store

A database optimized for appending immutable events (e.g., EventStoreDB).

### Snapshots

To avoid replay performance issues for long histories (10,000 events), save a "Snapshot" every 100 events. Replay = Snapshot + subsequent events.

### Projections

Code that listens to events and builds a read-optimized view (The "R" in CQRS).

## Best Practices

**Do**:

- Keep Events **Immutable**. You can never change the past. To fix an error, append a "CorrectionEvent".
- Version your Events carefully (Upcasting) to handle schema changes over years.

**Don't**:

- Don't put logic in the Event Store. It's just a log.
- Don't query the Event Stream for complex searches (Use a Projection/Read Model).

## Troubleshooting

| Error              | Cause                             | Solution                                                  |
| :----------------- | :-------------------------------- | :-------------------------------------------------------- |
| `Slow Replay`      | Too many events for an aggregate. | Implement Snapshots or check Aggregate boundaries.        |
| `Schema Evolution` | Old events don't match new code.  | Implement "Upcasters" to transform old events on the fly. |

## References

- [EventStoreDB](https://www.eventstore.com/)
- [Martin Fowler - Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
