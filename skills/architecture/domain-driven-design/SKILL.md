---
name: domain-driven-design
description: Expert Domain-Driven Design (DDD) assistance covering strategic bounded contexts, ubiquitous language, aggregates, value objects, domain events, and repository patterns. Use when modeling complex business domains, decomposing monoliths into microservices, or implementing rich domain models.
---

# Domain-Driven Design (DDD)

DDD is a software design approach focusing on modeling software to match a domain according to input from that domain's experts. It is essential for tackling high complexity in the heart of software.

## When to Use

- **Complex Business Domains**: Healthcare, fintech, logistics, and enterprise systems with intricate operational rules and workflows.
- **Monolith Decomposition**: Establishing well-defined Bounded Contexts as boundaries for microservices or modular monoliths.
- **Cross-Functional Team Alignment**: Creating a shared Ubiquitous Language between domain experts and software engineers.
- **High-Change Core Software**: Managing business logic that evolves rapidly without introducing unexpected regressions.

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

### Strategic DDD: Bounded Contexts & Context Mapping

Divides a large organization into autonomous boundaries with distinct terminology and models:

```text
[ Sales Context ] ──(Customer = Buyer)──→ [ Context Map ] ──(Customer = Borrower)──→ [ Underwriting Context ]
```

### Value Objects vs Entities

Entities possess a persistent identity that endures across mutations; Value Objects are immutable and defined entirely by their attributes:

```typescript
// domain/value-objects/money.vo.ts
export class Money {
  constructor(
    public readonly amount: number,
    public readonly currency: "USD" | "EUR" | "GBP",
  ) {
    if (amount < 0) throw new Error("Amount cannot be negative");
    Object.freeze(this);
  }

  public add(other: Money): Money {
    if (this.currency !== other.currency) throw new Error("Currency mismatch");
    return new Money(this.amount + other.amount, this.currency);
  }

  public equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }
}
```

### Aggregate Roots & Transaction Boundaries

The Aggregate Root is the sole gateway through which external callers can interact with inner entities:

```typescript
// domain/aggregates/invoice.ts
export class Invoice {
  private readonly lineItems: InvoiceLineItem[] = [];

  constructor(
    public readonly id: string,
    public readonly customerId: string,
  ) {}

  public addLineItem(description: string, price: Money): void {
    if (this.lineItems.length >= 100)
      throw new Error("Maximum line items exceeded");
    this.lineItems.push(
      new InvoiceLineItem(crypto.randomUUID(), description, price),
    );
  }

  get total(): Money {
    return this.lineItems.reduce(
      (sum, item) => sum.add(item.price),
      new Money(0, "USD"),
    );
  }
}
```

## Common Patterns

### Aggregate Root with Encapsulated Business Invariants

**Problem**: Direct mutation of entity state bypasses business rules and produces inconsistent data.  
**Solution**: Protect invariants inside Aggregate Roots and emit Domain Events.

```typescript
// domain/aggregates/bank-account.ts
export class BankAccount {
  private _balance: number = 0;
  private readonly _domainEvents: any[] = [];

  constructor(
    public readonly id: string,
    initialDeposit: number,
  ) {
    if (initialDeposit < 25) throw new Error("Minimum opening balance is $25");
    this._balance = initialDeposit;
  }

  public withdraw(amount: number): void {
    if (amount <= 0) throw new Error("Withdrawal amount must be positive");
    if (this._balance - amount < 0) throw new Error("Insufficient funds");
    this._balance -= amount;
    this._domainEvents.push({
      type: "FUNDS_WITHDRAWN",
      accountId: this.id,
      amount,
    });
  }

  get balance(): number {
    return this._balance;
  }
  pullDomainEvents(): any[] {
    return this._domainEvents.splice(0);
  }
}
```

## Best Practices

**Do**:

- Co-Design with Domain Experts: Conduct Event Storming workshops to map domain workflows before writing code.
- Enforce Invariants Inside the Aggregate: Ensure invalid state can never exist within an entity or aggregate root.
- Reference Other Aggregates by ID Only: Never hold direct object references to other aggregate roots; use their unique IDs.
- Make Value Objects Immutable: Guarantee side-effect free equality checks and safe passing across concurrent threads.

**Don't**:

- Create massive aggregates: Keep aggregates small; large aggregates cause database lock contention and performance bottlenecks.
- Let technical database concerns leak into Domain logic: Design domain models for business behavior, not database normalization.
- Use DDD for generic CRUD contexts: Reserve DDD tactical patterns for the Core Domain where competitive advantage lies.

## Troubleshooting

| Error         | Cause                       | Solution                                                               |
| :------------ | :-------------------------- | :--------------------------------------------------------------------- |
| `God Class`   | Aggregate knowing too much. | Split Aggregates; use Domain Events to coordinate.                     |
| `Performance` | Loading huge Aggregates.    | Lazy load is tricky; prefer smaller Aggregates tailored to invariants. |

## References

- [Domain-Driven Design (Eric Evans)](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215)
- [Implementing Domain-Driven Design (Vaughn Vernon)](https://img.shields.io/badge/book-red)
