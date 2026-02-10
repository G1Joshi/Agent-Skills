---
name: event-driven
description: Event-driven architecture with pub/sub and message queues. Use for reactive systems.
---

# Event-Driven Architecture (EDA)

EDA is a software architecture paradigm promoting the production, detection, consumption of, and reaction to events. In 2025, it is the backbone of real-time, scalable, and decoupled systems.

## When to Use

- When strict decoupling is required (Producer doesn't know Consumer).
- High-volume, bursty traffic (using buffering queues).
- Asynchronous workflows (e.g., "User Signed Up" -> Send Email, Create Wallet, Analytics).
- Real-time updates (WebSockets/Push).

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

### Event

A significant change in state (Immutable fact). "OrderCreated" not "CreateOrder".

### Broker (Event Bus)

The middleware (Kafka, RabbitMQ, SNS/SQS) that receives, stores, and routes events.

### Pub/Sub

Pattern where publishers send messages to a topic, and multiple subscribers receive them independently.

## Common Patterns

### Event Sourcing

Storing the state of an entity as a sequence of state-changing events rather than the current snapshot.

### CQRS (Command Query Responsibility Segregation)

Separating the Read and Write models. Writes publish events; Reads update a denormalized view based on those events.

### Transactional Outbox

Ensuring data consistency. Write the event to a DB table _in the same transaction_ as the business logic, then a background worker pushes it to the broker.

## Best Practices

**Do**:

- Use **Schemas** (Avro, Protobuf, JSON Schema) to govern event structure (Schema Registry).
- Ensure **Idempotency** in consumers (handling the same message twice safely).
- Monitor **Lag** (how far behind consumers are).

**Don't**:

- Don't use events for synchronous queries (Request/Response via queues is painful).
- Don't put huge payloads in events (Pass ID + Metadata, reference Blob Storage if needed).

## Tools

- **Kafka / Redpanda**: High throughput, log-based (replayable).
- **RabbitMQ / ActiveMQ**: Queue-based, complex routing.
- **AWS SNS/SQS / Google PubSub**: Cloud native.

## References

- [Event-Driven Architecture](https://aws.amazon.com/event-driven-architecture/)
- [AsyncAPI Specification](https://www.asyncapi.com/)
