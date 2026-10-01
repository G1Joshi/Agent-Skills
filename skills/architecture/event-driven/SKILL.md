---
name: event-driven
description: Expert Event-Driven Architecture assistance covering message brokers, pub/sub topologies, event stream processing, asynchronous workflows, and eventual consistency. Use when designing decoupled microservices, integrating Apache Kafka or RabbitMQ, or managing outbox patterns.
---

# Event-Driven Architecture (EDA)

Event-Driven Architecture (EDA) is a distributed systems paradigm decoupling producers and consumers through asynchronous event streams, enabling horizontal scalability and fault-tolerant processing.

## When to Use

- **Decoupled Microservice Architectures**: Connecting distributed services through asynchronous events rather than fragile synchronous HTTP chains.
- **High-Volume Asynchronous Processing**: Ingesting IoT telemetry, analytics events, and user activity logs with buffer-backed queues.
- **Complex Cross-Service Workflows**: Coordinating order processing, inventory reservations, and notifications asynchronously.
- **Zero-Downtime Resilience**: Ensuring systems continue functioning and queuing events even when consumer services are temporarily offline.

## Quick Start

```typescript
// Producer (Order Service)
await messageBroker.publish("order.created", {
  orderId: "123",
  userId: "456",
  timestamp: Date.now(),
});

// Consumer (Shipping Service)
// Doesn't need to be online when order is created
messageBroker.subscribe("order.created", async (event) => {
  await shippingService.schedulePickup(event.orderId);
  console.log("Shipping scheduled");
});

// Consumer (Analytics Service)
// New feature added later? No changes to Order Service!
messageBroker.subscribe("order.created", async (event) => {
  await analytics.trackRevenue(event);
});
```

## Core Concepts

### Pub/Sub Topology & Fan-Out

Producers publish events without knowing consumers; brokers fan out events to multiple subscriber queues:

```text
[ Order Service ] ──Publish(OrderPlaced)──→ [ Topic: orders.events ]
                                                     ├──→ [ Queue: Inventory ] ──→ [ Inventory Service ]
                                                     ├──→ [ Queue: Billing ]   ──→ [ Payment Service ]
                                                     └──→ [ Queue: Email ]     ──→ [ Notification Service ]
```

### CloudEvents Specification Standard

Standardizes event metadata across distributed platforms:

```json
{
  "specversion": "1.0",
  "type": "com.ecommerce.order.placed.v1",
  "source": "/orders/service",
  "id": "A234-1234-1234",
  "time": "2026-09-27T10:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "orderId": "ord_91823",
    "customerId": "cust_481",
    "totalCents": 4999
  }
}
```

### Idempotent Event Consumer Pattern

Guarantees safety against message broker duplicate deliveries:

```typescript
// consumers/order-placed.consumer.ts
export async function handleOrderPlaced(event: CloudEvent) {
  const isProcessed = await redis.set(
    `processed_event:${event.id}`,
    "true",
    "NX",
    "EX",
    86400,
  );
  if (!isProcessed) {
    console.log(`Event ${event.id} already processed. Skipping.`);
    return; // Idempotent exit
  }

  // Execute actual business logic
  await processPayment(event.data);
}
```

### Event Broker Tooling Matrix

- **Kafka / Redpanda**: High throughput, log-based event streaming and replayable message logs.
- **RabbitMQ / ActiveMQ**: AMQP message broker with complex topic and header routing.
- **AWS SNS/SQS / Google Cloud Pub/Sub**: Cloud-native managed pub/sub and distributed queuing.

## Common Patterns

### Transactional Outbox Pattern

**Problem**: Dual-write hazard: saving database entity succeeds, but message broker publish fails.  
**Solution**: Write outgoing domain events to an outbox table within the same database transaction.

```sql
-- Outbox Table definition
CREATE TABLE outbox_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  aggregate_type VARCHAR(64) NOT NULL,
  aggregate_id VARCHAR(64) NOT NULL,
  event_type VARCHAR(64) NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  processed_at TIMESTAMPTZ NULL
);
```

```typescript
// Atomic database write + event staging
await db.transaction(async (tx) => {
  await tx.insert(orders).values(orderData);
  await tx.insert(outboxEvents).values({
    aggregateType: "Order",
    aggregateId: orderData.id,
    eventType: "OrderCreated",
    payload: JSON.stringify(orderData),
  });
});
```

## Best Practices

**Do**:

- Use the Transactional Outbox Pattern: Prevent dual-write anomalies by saving domain entities and outbox events in one database transaction.
- Design Every Consumer to be Idempotent: Always record processed message IDs to handle at-least-once message broker retries safely.
- Version Your Event Schemas: Evolve schemas using backwards-compatible additions; use Protobuf or JSON Schema registries.
- Implement Dead Letter Queues (DLQ): Route malformed or persistently failing messages to a DLQ for operational inspection.

**Don't**:

- Use events for RPC / Request-Response queries: Do not simulate synchronous HTTP calls using two-way event streams.
- Broadcast massive binary payloads in events: Send lightweight event notifications with a resource URL/ID (Claim Check pattern).
- Ignore message ordering limitations: Remember that partition keys determine ordering in Kafka/Kinesis; global ordering is not guaranteed.

## Troubleshooting

| Error                         | Cause                                                    | Solution                                                                             |
| :---------------------------- | :------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| `Out-of-order event delivery` | Partition key missing or concurrent consumer processing. | Assign consistent partition keys (e.g. `order_id`) and enforce monotonic sequencing. |
| `Duplicate event consumption` | Consumer retries after network timeout before ack.       | Implement idempotency checks using unique event IDs in a deduplication store.        |
| `Poison pill message block`   | Unhandled payload serialization or validation failure.   | Route malformed messages to a Dead Letter Queue (DLQ) after retry limit.             |

## References

- [Event-Driven Architecture](https://aws.amazon.com/event-driven-architecture/)
- [AsyncAPI Specification](https://www.asyncapi.com/)
