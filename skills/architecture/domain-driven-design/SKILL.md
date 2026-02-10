---
name: domain-driven-design
description: DDD tactical and strategic patterns. Use for complex domains.
---

# Domain-Driven Design (DDD)

DDD is a software design approach focusing on modeling software to match a domain according to input from that domain's experts. It is essential for tackling high complexity in the heart of software.

## When to Use

- Complex business domains (e.g., Insurance, Banking, Logistics) where logic is intricate.
- When there is a communication gap between developers and business experts.
- decomposing a Monolith into Microservices (defining boundaries).

## Quick Start

```java
// Aggregate Root
public class Order {
    private OrderId id;
    private Money totalAmount;
    private OrderStatus status;
    private List<OrderItem> items; // Aggregates items

    // Behaviors (Rich Model), not just Getters/Setters
    public void addItem(Product product, int quantity) {
        if (this.status != OrderStatus.DRAFT) {
            throw new DomainException("Cannot modify confirmed order");
        }
        this.items.add(new OrderItem(product, quantity));
        recalculateTotal();
    }

    public void confirm() {
        if (items.isEmpty()) throw new DomainException("Order empty");
        this.status = OrderStatus.CONFIRMED;
        // Raise Domain Event
        DomainEvents.publish(new OrderConfirmed(this.id));
    }
}
```

## Core Concepts

### Ubiquitous Language

A common, rigorous language shared by developers and domain experts. If the expert calls it a "Policy", the code must call it `Policy`, not `UserPlan` or `Subscription`.

### Bounded Context

The specific boundary within which a particular domain model is defined and applicable. Ideally maps to a Microservice or a Module.

### Aggregates

A cluster of associated objects treated as a unit for data changes. External objects can only hold references to the **Aggregate Root**.

## Common Patterns

### Value Objects

Immutable objects defined by their attributes, not identity (e.g., `Money`, `Address`, `Email`). Two `Money(5)` objects are equal.

### Domain Events

Something that happened in the domain that domain experts care about (`OrderShipped`, `AccountDebited`). Used to decouple side effects.

### Anti-Corruption Layer (ACL)

A layer that translates models from an external system (or legacy subsystem) into the model of the current Bounded Context to prevent pollution.

## Best Practices

**Do**:

- Focus on **Behaviors**, not just Data (Anemic Domain Model vs Rich Domain Model).
- Use **Event Storming** sessions to discover the domain events and boundaries.
- Ensure **Transactional Consistency** within an Aggregate, and **Eventual Consistency** between Aggregates.

**Don't**:

- Don't apply DDD to simple CRUD domains (it's overkill).
- Don't let Aggregates reference each other by Object Pointer; use IDs.

## Troubleshooting

| Error         | Cause                       | Solution                                                               |
| :------------ | :-------------------------- | :--------------------------------------------------------------------- |
| `God Class`   | Aggregate knowing too much. | Split Aggregates; use Domain Events to coordinate.                     |
| `Performance` | Loading huge Aggregates.    | Lazy load is tricky; prefer smaller Aggregates tailored to invariants. |

## References

- [Domain-Driven Design (Eric Evans)](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)
- [Implementing Domain-Driven Design (Vaughn Vernon)](https://img.shields.io/badge/book-red)
