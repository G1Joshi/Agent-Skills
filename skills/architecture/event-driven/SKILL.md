---
name: event-driven
description: Event-driven architecture with queues and event sourcing. Use for async systems.
---

# Event-Driven Architecture

Asynchronous communication through events and messages.

## When to Use

- Decoupled systems
- Async processing
- Real-time notifications
- Audit trails

## Quick Start

```typescript
import { EventEmitter } from "events";

const eventBus = new EventEmitter();

// Subscribe
eventBus.on("user:created", (user) => {
  sendWelcomeEmail(user);
});

// Publish
eventBus.emit("user:created", { id: "123", email: "user@example.com" });
```

## Core Concepts

### Message Queue (RabbitMQ)

```typescript
import amqp from "amqplib";

// Producer
const channel = await connection.createChannel();
await channel.assertQueue("orders");
channel.sendToQueue("orders", Buffer.from(JSON.stringify(order)));

// Consumer
await channel.consume("orders", async (msg) => {
  const order = JSON.parse(msg.content.toString());
  await processOrder(order);
  channel.ack(msg);
});
```

### Kafka Streams

```typescript
import { Kafka } from "kafkajs";

const kafka = new Kafka({ brokers: ["localhost:9092"] });
const producer = kafka.producer();
const consumer = kafka.consumer({ groupId: "order-service" });

// Produce
await producer.send({
  topic: "orders",
  messages: [{ key: orderId, value: JSON.stringify(event) }],
});

// Consume
await consumer.subscribe({ topic: "orders" });
await consumer.run({
  eachMessage: async ({ topic, partition, message }) => {
    const event = JSON.parse(message.value!.toString());
    await handleEvent(event);
  },
});
```

## Common Patterns

### Event Sourcing

```typescript
interface Event {
  type: string;
  data: unknown;
  timestamp: Date;
  aggregateId: string;
}

class OrderAggregate {
  private events: Event[] = [];
  private state: OrderState = { status: "pending" };

  apply(event: Event) {
    this.events.push(event);
    this.state = this.reducer(this.state, event);
  }

  private reducer(state: OrderState, event: Event): OrderState {
    switch (event.type) {
      case "ORDER_PLACED":
        return { ...state, status: "placed" };
      case "ORDER_SHIPPED":
        return { ...state, status: "shipped" };
      default:
        return state;
    }
  }
}
```

### Dead Letter Queue

```typescript
await channel.assertQueue("orders.dlq");
await channel.assertQueue("orders", {
  deadLetterExchange: "",
  deadLetterRoutingKey: "orders.dlq",
});

// Handle failed messages
await channel.consume("orders.dlq", async (msg) => {
  await notifyAdmin(msg);
  channel.ack(msg);
});
```

## Best Practices

**Do**:

- Use idempotent consumers
- Implement dead letter queues
- Add correlation IDs
- Monitor queue depth

**Don't**:

- Rely on message order
- Skip error handling
- Ignore backpressure
- Forget acknowledgments

## Troubleshooting

| Issue                | Cause          | Solution              |
| -------------------- | -------------- | --------------------- |
| Message loss         | No persistence | Enable durable queues |
| Duplicate processing | No idempotency | Add idempotency keys  |
| Queue buildup        | Slow consumers | Scale consumers       |

## References

- [Event-Driven Microservices](https://www.oreilly.com/library/view/building-event-driven/9781492057888/)
- [Kafka Documentation](https://kafka.apache.org/documentation/)
