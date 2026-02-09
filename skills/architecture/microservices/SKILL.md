---
name: microservices
description: Microservices architecture with service mesh and communication patterns. Use for distributed systems.
---

# Microservices

Distributed architecture with independent services.

## When to Use

- Large-scale applications
- Independent team scaling
- Polyglot development
- Fault isolation

## Quick Start

```yaml
# docker-compose.yml
services:
  api-gateway:
    build: ./gateway
    ports: ["3000:3000"]

  user-service:
    build: ./services/user

  order-service:
    build: ./services/order

  notification-service:
    build: ./services/notification
```

## Core Concepts

### Service Communication

```typescript
// REST communication
async function getUser(userId: string): Promise<User> {
  const response = await fetch(`${USER_SERVICE_URL}/users/${userId}`);
  return response.json();
}

// gRPC client
const client = new UserServiceClient(
  "user-service:50051",
  grpc.credentials.createInsecure(),
);

// Message queue
import { Queue } from "bullmq";

const orderQueue = new Queue("orders");
await orderQueue.add("process", { orderId: "123" });
```

### Event-Driven Architecture

```typescript
// Producer
await kafka.producer.send({
  topic: "user-events",
  messages: [
    {
      key: userId,
      value: JSON.stringify({ type: "USER_CREATED", data: user }),
    },
  ],
});

// Consumer
await kafka.consumer.subscribe({ topic: "user-events" });
await kafka.consumer.run({
  eachMessage: async ({ message }) => {
    const event = JSON.parse(message.value.toString());
    if (event.type === "USER_CREATED") {
      await sendWelcomeEmail(event.data);
    }
  },
});
```

## Common Patterns

### Circuit Breaker

```typescript
import CircuitBreaker from "opossum";

const breaker = new CircuitBreaker(fetchUser, {
  timeout: 3000,
  errorThresholdPercentage: 50,
  resetTimeout: 30000,
});

breaker.fallback(() => ({ id: "unknown", name: "Guest" }));

const user = await breaker.fire(userId);
```

### Service Discovery

```yaml
# Kubernetes service
apiVersion: v1
kind: Service
metadata:
  name: user-service
spec:
  selector:
    app: user-service
  ports:
    - port: 80
      targetPort: 3000
```

## Best Practices

**Do**:

- Design for failure
- Implement retry logic
- Use async communication
- Monitor all services

**Don't**:

- Share databases
- Create tight coupling
- Ignore distributed transactions
- Skip health checks

## Troubleshooting

| Issue              | Cause             | Solution            |
| ------------------ | ----------------- | ------------------- |
| Service timeout    | Network/load      | Add circuit breaker |
| Data inconsistency | Distributed state | Use saga pattern    |
| Cascading failure  | No isolation      | Implement bulkhead  |

## References

- [Microservices.io](https://microservices.io/)
- [12-Factor App](https://12factor.net/)
