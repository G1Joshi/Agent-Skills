---
name: modular-monolith
description: Expert Modular Monolith architecture assistance covering bounded module boundaries, internal public APIs, decoupled package structures, and single-deployment velocity. Use when scaling monolith development teams, preventing spaghetti code, or preparing for future microservice extraction.
---

# Modular Monolith

A Modular Monolith is a single deployable unit (Monolith) where the code is structured into independent modules (like Microservices) with strict boundaries. In 2025, this is the **recommended default** architecture for most startups and medium-scale apps.

## When to Use

- **Medium-to-Large Engineering Teams**: Scaling a codebase across multiple teams without the operational overhead of microservices.
- **Single-Deployment Velocity**: Retaining simple CI/CD pipelines, single-transaction database migrations, and local Docker setups.
- **Clear Domain Boundaries**: Preventing spaghetti code by enforcing strict module encapsulation and public API boundaries at compile-time.
- **Pre-Microservice Preparation**: Architecting systems that can be cleanly sliced into separate microservices later if scaling demands it.

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

#Strict Module Encapsulation & Public API Facades

Modules interact exclusively through explicit public facades; internal repositories, models, and helpers are unexported:

```
src/modules/
  ├── billing/
  │   ├── internal/        # Private tables, services, entities
  │   └── index.ts         # Public Interface & Facade ONLY
  └── shipping/
      ├── internal/
      └── index.ts
```

#In-Process Domain Events

Modules communicate asynchronously across boundaries using in-memory event buses:

```typescript
// modules/common/event-bus.ts
import EventEmitter from "events";
export const inProcessBus = new EventEmitter();

// modules/orders/internal/order.service.ts
inProcessBus.emit("order.created", { orderId: "123", customerId: "456" });

// modules/notifications/internal/notification.listener.ts
inProcessBus.on("order.created", (payload) => {
  // Executes in same process, decoupled from order module code
});
```

#Architecture Linter Boundary Enforcement

Enforces boundary rules in CI using tools like `eslint-plugin-boundaries` or ArchUnit:

```javascript
// .eslintrc.js
rules: {
  "boundaries/element-types": [2, {
    default: "disallow",
    rules: [
      { from: "module:billing", allow: ["module:billing", "module:common"] },
      { from: "module:shipping", allow: ["module:shipping", "module:common"] },
    ]
  }]
}
```

## Common Patterns

#Internal Module Public API Facade
**Problem**: Modules access each other's private tables, destroying encapsulation and preventing future service extraction.  
**Solution**: Expose an explicit Public API interface per module.

```typescript
// modules/billing/index.ts (Billing Module Public Boundary)
export interface BillingModuleApi {
  chargeCustomer(
    customerId: string,
    amountCents: number,
  ): Promise<PaymentReceipt>;
  getSubscriptionStatus(customerId: string): Promise<SubscriptionStatus>;
}

// Internal billing tables, services, and repositories are NOT exported.
export class BillingFacade implements BillingModuleApi {
  constructor(private readonly paymentService: InternalPaymentService) {}
  async chargeCustomer(id: string, amount: number) {
    return this.paymentService.processCharge(id, amount);
  }
  async getSubscriptionStatus(id: string) {
    return this.paymentService.checkSubscription(id);
  }
}
```

## Best Practices (2026)

**Do**:

- **Enforce Boundaries with Build Tools**: Use ESLint rules, TypeScript project references, or ArchUnit to prevent illegal module cross-imports.
- **Isolate Module Schemas**: Use separate database schemas (`billing.*`, `users.*`) within the same database to prevent illicit SQL joins.
- **Communicate Across Modules via Facades or Events**: Disallow direct access to another module's internal classes or database repositories.
- **Keep Deployment Pipeline Unified**: Enjoy the speed of atomic single-binary deployments and coordinated database migrations.

**Don't**:

- **Don't execute direct cross-module foreign key joins**: Reference entities from foreign modules by ID only; do not write `LEFT JOIN shipping.parcels`.
- **Don't share mutable memory state across modules**: Pass immutable DTOs or primitive values through public facade methods.
- **Don't prematurely split into microservices**: Extract a module into a microservice only when deployment frequency or scaling demands it.

## Advantages over Microservices

- **Zero Latency** communication.
- **Transactional Consistency** (ACID) is easier (though ideally, avoid cross-module transactions).
- **Refactoring** is cheap (IDE "Rename" works globally).

## Troubleshooting

| Error                              | Cause                                                          | Solution                                                                         |
| :--------------------------------- | :------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| `Cyclic module dependency`         | Modules directly importing internal classes across boundaries. | Expose strictly typed public APIs/facades and enforce boundary linting.          |
| `Accidental shared database table` | Cross-module queries joining tables across domains.            | Isolate schemas per module or access data exclusively through module interfaces. |
| `Leaky module abstractions`        | Direct access to internal database entities instead of DTOs.   | Return immutable Data Transfer Objects (DTOs) from module public services.       |

## References

- [Modular Monoliths (Kamil Grzybek)](https://github.com/kgrzybek/modular-monolith-with-ddd)
- [The Majestic Monolith](https://m.signalvnoise.com/the-majestic-monolith/)
