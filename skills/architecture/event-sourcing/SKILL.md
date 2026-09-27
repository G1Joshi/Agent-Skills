---
name: event-sourcing
description: Expert Event Sourcing assistance covering immutable append-only event logs, state reconstruction, snapshotting, event versioning, and temporal queries. Use when building audit-compliant persistence systems, financial ledgers, or historical state tracking.
---

# Event Sourcing

Event Sourcing ensures that all changes to application state are stored as a sequence of events. We don't just store the current state; we store "what happened".

## When to Use

- **Complete Audit & Compliance Trails**: Financial ledgers, healthcare records, and legal systems where historical state cannot be overwritten.
- **Temporal Queries & Time Travel**: Reconstructing the exact state of an entity as of any specific timestamp in history.
- **Complex Domain Debugging**: Replaying production incident events in local environments to pinpoint exact logic flaws.
- **High-Velocity Append-Only Ingestion**: Maximizing write throughput by appending immutable events without updates or delete locks.

## Quick Start

```typescript
// Append-only domain event structure and aggregate reconstruction
interface DomainEvent {
  eventId: string;
  aggregateId: string;
  type: string;
  payload: Record<string, any>;
  timestamp: number;
}

class OrderAggregate {
  public id: string = "";
  public status: "PENDING" | "PAID" | "SHIPPED" = "PENDING";

  apply(event: DomainEvent): void {
    switch (event.type) {
      case "ORDER_CREATED":
        this.id = event.aggregateId;
        this.status = "PENDING";
        break;
      case "ORDER_PAID":
        this.status = "PAID";
        break;
      case "ORDER_SHIPPED":
        this.status = "SHIPPED";
        break;
    }
  }

  static reconstruct(events: DomainEvent[]): OrderAggregate {
    const aggregate = new OrderAggregate();
    for (const event of events) {
      aggregate.apply(event);
    }
    return aggregate;
  }
}
```

## Core Concepts

#Immutable Event Stream Architecture

State is derived purely by folding historical events sequentially over an initial empty state:

```
Stream: Account-42
Event 1: AccountOpened(initialDeposit: 100)  -> Balance = 100
Event 2: MoneyDeposited(amount: 50)          -> Balance = 150
Event 3: MoneyWithdrawn(amount: 30)          -> Balance = 120 (Current State)
```

#State Reconstruction via Aggregate Replay

```typescript
// domain/aggregates/account.ts
export class Account {
  public balance: number = 0;
  public version: number = 0;

  apply(event: DomainEvent): void {
    switch (event.type) {
      case "ACCOUNT_OPENED":
        this.balance = event.data.initialDeposit;
        break;
      case "MONEY_DEPOSITED":
        this.balance += event.data.amount;
        break;
      case "MONEY_WITHDRAWN":
        this.balance -= event.data.amount;
        break;
    }
    this.version++;
  }

  static fromHistory(events: DomainEvent[]): Account {
    const account = new Account();
    events.forEach((e) => account.apply(e));
    return account;
  }
}
```

#Snapshotting for High-Volume Streams

Stores periodic state checkpoints to prevent replaying millions of events on every read:

```typescript
// Snapshot pattern
async function getAccount(accountId: string): Promise<Account> {
  const snapshot = await snapshotStore.getLatest(accountId);
  const fromVersion = snapshot ? snapshot.version : 0;

  const events = await eventStore.getEvents(accountId, fromVersion);
  const account = snapshot ? Account.fromSnapshot(snapshot) : new Account();
  events.forEach((e) => account.apply(e));
  return account;
}
```

## Common Patterns

### Snapshotting Aggregates

**Problem**: Replaying thousands of past events to rebuild state for an aggregate causes severe read latency.

**Solution**:
Persist periodic aggregate state snapshots (e.g., every 100 events) and replay events only from the snapshot forward:

```typescript
class AccountAggregate {
  private balance: number = 0;
  private version: number = 0;

  loadFromSnapshot(
    snapshot: { balance: number; version: number },
    eventsSince: DomainEvent[],
  ) {
    this.balance = snapshot.balance;
    this.version = snapshot.version;
    for (const event of eventsSince) {
      this.apply(event);
      this.version++;
    }
  }

  apply(event: DomainEvent) {
    if (event.type === "DEPOSITED") this.balance += event.amount;
  }
}
```

## Best Practices (2026)

**Do**:

- **Treat Events as Immutable Facts**: Never edit, mutate, or delete events; record compensating events (e.g. `PaymentReversed`) to fix mistakes.
- **Snapshot Long-Lived Streams**: Create snapshots every 100-500 events to keep hydration latency under 10ms.
- **Enforce Optimistic Concurrency Control**: Pass expected stream version on append; reject write if version has changed.
- **Pair with CQRS**: Separate read query views from the event store to provide fast query responses.

**Don't**:

- **Don't change past event structures**: Maintain backwards compatibility when updating schemas; use upcasters for migration.
- **Don't put PII in unencrypted event streams**: If subject to GDPR Right to be Forgotten, use Crypto-Shredding (encrypt PII with disposable keys).
- **Don't use Event Sourcing for everything**: Simple CRUD entities without audit requirements incur massive complexity under Event Sourcing.

## Troubleshooting

| Error              | Cause                             | Solution                                                  |
| :----------------- | :-------------------------------- | :-------------------------------------------------------- |
| `Slow Replay`      | Too many events for an aggregate. | Implement Snapshots or check Aggregate boundaries.        |
| `Schema Evolution` | Old events don't match new code.  | Implement "Upcasters" to transform old events on the fly. |

## References

- [EventStoreDB](https://www.eventstore.com/)
- [Martin Fowler - Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
