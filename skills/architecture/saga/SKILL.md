---
name: saga
description: Saga pattern for distributed transactions. Use for microservices transactions.
---

# Saga Pattern

The Saga pattern manages data consistency across microservices in distributed transaction scenarios. A Saga is a sequence of local transactions. Each local transaction updates the database and publishes a message or event to trigger the next local transaction in the saga.

## When to Use

- **Distributed Transactions**: e.g., "Book Flight" + "Book Hotel" + "Charge Card".
- Long-running processes where you can't hold a DB lock.
- Ensuring eventual consistency across Services A, B, and C.

## Core Concepts

### Compensating Transactions

If a step fails (e.g., Card Declined), the Saga must execute **compensating transactions** to undo the changes made by the preceding steps (e.g., "Cancel Hotel", "Cancel Flight").

### Choreography

Each service listens to events and decides what to do.

- Order Service -> `OrderCreated`
- Inventory Service -> listends to `OrderCreated` -> does work -> `InventoryReserved`

### Orchestration

A central coordinator (Orchestrator) tells each service what to do.

- Orchestrator -> Call Order Service
- Orchestrator -> Call Inventory Service
- Orchestrator -> Handle failure -> Call Compensation.

## Best Practices

**Do**:

- Prefer **Orchestration** for complex sagas (easier to visualize and trace).
- Ensure all steps are **Idempotent**.
- Design for failure (Everything that can fail, will fail).

**Don't**:

- Don't rely on synchronous HTTP calls for Sagas (What if the network drops in the middle?). Use Message Queues or Persistent Orchestrators (Temporal).

## Tools

- **Temporal.io**: Workflow engine for code-based orchestration.
- **MassTransit** (C#): Built-in Saga state machines.

## References

- [Microservices.io - Saga](https://microservices.io/patterns/data/saga.html)
- [Temporal](https://temporal.io/)
