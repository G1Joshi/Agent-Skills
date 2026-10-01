---
name: saga
description: Expert Saga pattern implementation covering orchestration, choreography, and compensating transactions. Use when designing distributed transactions, multi-service workflows, or eventual consistency.
---

# Saga Pattern

The Saga pattern manages data consistency across microservices in distributed transaction scenarios without two-phase commit (2PC). A Saga coordinates a sequence of local transactions, executing compensating transactions backward if any intermediate step fails.

## When to Use

- **Distributed Transactions Across Microservices**: Coordinating multi-step business transactions without two-phase commit (2PC) locks.
- **E-Commerce Checkout & Fulfillment**: Managing sequences spanning inventory reservation, payment charging, order placement, and delivery dispatch.
- **Long-Running Business Processes**: Orchestrating processes that span seconds, minutes, or hours with explicit failure compensation.
- **Failure Recovery & State Reversal**: Rolling back partially completed distributed steps using compensating transactions.

## Quick Start

```typescript
// Minimal Orchestrator-based Saga Definition
interface SagaStep<TContext> {
  name: string;
  execute: (ctx: TContext) => Promise<void>;
  compensate: (ctx: TContext) => Promise<void>;
}

async function runSaga<T>(context: T, steps: SagaStep<T>[]) {
  const executedSteps: SagaStep<T>[] = [];
  try {
    for (const step of steps) {
      console.log(`Executing step: ${step.name}`);
      await step.execute(context);
      executedSteps.push(step);
    }
    console.log("Saga completed successfully.");
  } catch (err) {
    console.error(
      `Saga failed. Rolling back compensating transactions...`,
      err,
    );
    for (const step of executedSteps.reverse()) {
      try {
        await step.compensate(context);
      } catch (compErr) {
        console.error(`Compensation failed for ${step.name}:`, compErr);
      }
    }
    throw err;
  }
}
```

## Core Concepts

### Orchestration vs Choreography Sagas

Sagas coordinate multi-service transactions using either a centralized orchestrator or decentralized events:

```text
[ Orchestrator ] ──1. Reserve Stock──→ [ Inventory Service ]
                 ──2. Charge Card───→ [ Payment Service ] (FAILS!)
                 ──3. Compensate: Release Stock ──→ [ Inventory Service ]
```

### Compensating Transactions (Semantic Rollback)

Because local transactions commit at each step, failures must be undone semantically through compensating transactions:

| Forward Transaction            | Compensating Transaction       |
| :----------------------------- | :----------------------------- |
| `ReserveStock(orderId, items)` | `ReleaseStock(orderId, items)` |
| `ChargeCreditCard(amount)`     | `RefundCreditCard(amount)`     |
| `CreateShipmentLabel()`        | `CancelShipmentLabel()`        |

### Orchestrator State Machine Definition

Tracks workflow progression and triggers compensation on error:

```typescript
// sagas/order-saga-orchestrator.ts
export class OrderSagaOrchestrator {
  async execute(order: OrderPayload) {
    let stockReserved = false;
    try {
      await inventoryService.reserve(order.id, order.items);
      stockReserved = true;

      await paymentService.charge(order.id, order.total);
      await shippingService.schedule(order.id);
    } catch (err) {
      console.error("Saga failed! Initiating compensation...", err);
      if (stockReserved) {
        await inventoryService.compensateRelease(order.id, order.items);
      }
      throw new Error("Order processing failed; changes compensated.");
    }
  }
}
```

## Common Patterns

### Idempotent Step Execution

**Problem**: Network retries during step execution can result in duplicate orders or double charges.

**Solution**:
Pass an idempotency key with every saga step command:

```typescript
async function processPayment(orderId: string, idempotencyKey: string) {
  const existing = await paymentDb.findByKey(idempotencyKey);
  if (existing) {
    return existing.result; // Return previous outcome without recharging
  }
  const result = await paymentGateway.charge(orderId);
  await paymentDb.save({ idempotencyKey, orderId, result });
  return result;
}
```

## Best Practices

**Do**:

- Prefer Orchestration for Complex Multi-Step Sagas: Use workflow orchestrators (Temporal, AWS Step Functions) for complex multi-branch sagas.
- Make Compensating Transactions Idempotent: Ensure compensation actions can be safely retried multiple times without side effects.
- Record Saga State Persistently: Store the current step and execution state in a durable outbox/database before calling external services.
- Design for Forward Recovery: When possible, retry or alert operators to fix transient issues rather than compensating immediately.

**Don't**:

- Assume compensating transactions can never fail: Implement alerts and manual intervention queues for failed compensations.
- Use distributed locks across sagas: Avoid blocking local resources while waiting for distant service responses.
- Use choreography for sagas with > 4 services: Event-driven choreography becomes impossible to trace and reason about at scale.

## Troubleshooting

| Error                      | Cause                                                | Solution                                                                                      |
| :------------------------- | :--------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| `Saga stuck in PENDING`    | Orchestrator crashed or message dropped in queue.    | Use persistent state machines (e.g., Temporal/Step Functions) with automated timeout retries. |
| `Compensation Failed`      | Compensating action encountered non-retryable error. | Flag transaction for operator review and write to dead-letter queue (DLQ).                    |
| `Duplicate Step Execution` | Retry occurred without idempotency check.            | Enforce unique idempotency keys per saga step execution.                                      |

## References

- [Microservices.io - Saga Pattern](https://microservices.io/patterns/data/saga.html)
- [Temporal.io Workflow Engine](https://temporal.io/)
- [AWS Step Functions Saga Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/implement-the-saga-pattern-using-aws-step-functions.html)
