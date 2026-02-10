---
name: modular-monolith
description: Modular monolith with bounded contexts. Use for scalable monoliths.
---

# Modular Monolith

A Modular Monolith is a single deployable unit (Monolith) where the code is structured into independent modules (like Microservices) with strict boundaries. In 2025, this is the **recommended default** architecture for most startups and medium-scale apps.

## When to Use

- Starting a new project (Greenfield).
- Domain boundaries are not yet fully clear.
- Wanting the speed of simple deployment (one CI pipeline, one DB instance) but preventing "spaghetti code".
- Precursor to Microservices.

## Quick Start

```
/src
  /Modules
    /Catalog       <-- Public Interface defined here
      /Core        <-- Internals (Classes, Logic) hidden
      /API         <-- Public Contracts (DTOs)
    /Ordering
      /Core
    /Shipping
      /Core
  /Shared          <-- Infrastructure, Event Bus
```

```csharp
// Communication via In-Process Interfaces or Events
public class OrderService {
    private readonly ICatalogModule _catalog; // In-memory reference, but strict contract

    public async Task Checkout(string productId) {
        var product = await _catalog.GetProduct(productId); // Fast 0ms call
        // ...
    }
}
```

## Core Concepts

### Module Boundaries

Code in Module A cannot access internal classes of Module B. It can only use Module B's "Public API" (Interfaces/DTOs). Enforced by compiler tools (ArchUnit, NetArchTest).

### Single Deployment

Modules are compiled together into one binary/container and deployed to one server/cluster. Simplifies Ops.

### Data Isolation (Virtual)

Ideally, each module has its own DB schema (or at least different tables). Cross-module Joins are forbidden.

## Common Patterns

### In-Memory Events

Using a mediator (like MediatR in .NET or Spring Events) to decouple modules. Module A publishes `OrderCreated`, Module B listens. No Kafka needed (yet).

### Internal APIs

Defining strict interfaces that act as "Gateways" between modules. Changing the internals of Module A doesn't break Module B as long as the interface holds.

## Best Practices

**Do**:

- Force **Architecture Tests** (e.g., "Classes in `Ordering` cannot depend on `Shipping`").
- Separate **Data Schemas** logically (different schemas in Postgres).
- Treat it as "Microservices ready to be extracted".

**Don't**:

- Don't bypass boundaries "just this once".
- Don't share Domain Entities across modules (use integration DTOs).

## Advantages over Microservices

- **Zero Latency** communication.
- **Transactional Consistency** (ACID) is easier (though ideally, avoid cross-module transactions).
- **Refactoring** is cheap (IDE "Rename" works globally).

## References

- [Modular Monoliths (Kamil Grzybek)](https://github.com/kgrzybek/modular-monolith-with-ddd)
- [The Majestic Monolith](https://m.signalvnoise.com/the-majestic-monolith/)
