---
name: monolith
description: Expert Monolithic architecture assistance covering single-deployment architectures, vertical slice organization, database migrations, and operational simplicity. Use when bootstrapping greenfield applications, optimizing delivery velocity for small teams, or scaling monolithic applications.
---

# Monolith (Traditional)

A Monolithic architecture is built as a single unit. All functional components (UI, Business Logic, Data Access) are tightly integrated using a shared database and running in the same process.

## When to Use

- **Greenfield Startup Development**: Prioritizing rapid product discovery, iteration speed, and developer onboarding above all else.
- **Small-to-Medium Engineering Teams**: Teams of 1-30 developers where overhead from microservices infrastructure would divert from product building.
- **ACID Transaction Guarantees**: Applications requiring absolute transactional consistency across financial or relational operations.
- **Low Operational Overhead**: Deploying to single PaaS platforms (Render, Fly.io, Railway) or unified Kubernetes clusters with minimal DevOps complexity.

## Quick Start

```python
# Django/Rails/Laravel Style
# Everything in one place:
# - models/
# - views/
# - controllers/
# - utils/

def create_order(request):
    user = User.objects.get(id=request.user_id) # Direct DB access
    product = Product.objects.get(id=request.product_id) # Direct DB access

    order = Order.create(user=user, product=product)

    # Direct sync call within same transaction
    EmailService.send_confirmation(user)

    return Response("Order Created")
```

## Core Concepts

### Unified Codebase & Atomic Deployments

All features share a single repository, database connection, and deployment lifecycle:

```text
[ Monolithic Application (Next.js / Rails / Django / Spring) ]
              │
              ▼
    ( Unified Database )
```

### Vertical Slice Architecture

Organizes code by business feature rather than technical layer:

```text
src/features/
  ├── authentication/
  │   ├── auth.controller.ts
  │   ├── auth.service.ts
  │   └── auth.schema.ts
  └── checkout/
      ├── checkout.controller.ts
      ├── checkout.service.ts
      └── checkout.schema.ts
```

### In-Memory Transactions & Locks

Executes multi-table updates within native database transactions without distributed coordinator complexity:

```typescript
await db.transaction(async (tx) => {
  const [order] = await tx.insert(orders).values(orderData).returning();
  await tx
    .update(inventory)
    .set({ stock: sql`stock - 1` })
    .where(eq(inventory.itemId, itemId));
  await tx.insert(payments).values({ orderId: order.id, amount: order.total });
});
```

## Common Patterns

### Vertical Slice Architecture in Monoliths

**Problem**: Layered architecture (Controllers, Services, Repositories) scatters single-feature code across dozens of folders.  
**Solution**: Group by business capability (feature folder contains handler, model, schema, and UI).

```text
src/features/
  ├── auth/
  │   ├── login.command.ts
  │   ├── login.validator.ts
  │   └── auth.router.ts
  └── invoicing/
      ├── create-invoice.command.ts
      ├── invoice.entity.ts
      └── invoice.router.ts
```

## Best Practices

**Do**:

- Structure Code by Features (Vertical Slices): Avoid flat technical folders (`controllers/`, `models/`) with hundreds of unrelated files.
- Use Feature Flags for Continuous Deployment: Deploy code dark behind feature toggles to uncouple deployment from feature release.
- Automate Comprehensive Test Suites: Invest heavily in automated integration tests to catch unintended regressions across features.
- Scale Horizontally with Stateless Replicas: Run multiple identical stateless application instances behind an Nginx or ALB load balancer.

**Don't**:

- Store session state in local server memory: Store sessions in Redis or encrypted cookies to allow painless multi-instance scaling.
- Allow circular dependencies between feature directories: Keep dependency flow hierarchical and clean.
- Write blocking long-running background jobs in HTTP threads: Offload background jobs to BullMQ/Sidekiq queues.

## Troubleshooting

| Error                                | Cause                                                          | Solution                                                                             |
| :----------------------------------- | :------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| `Slow deployment pipelines`          | Monolithic test suites running sequentially on single runner.  | Parallelize test execution and modularize build caching across test suites.          |
| `Database connection exhaustion`     | Multiple app instances exhausting max database connections.    | Place an enterprise connection pooler (e.g. PgBouncer/ProxySQL) in front of the DB.  |
| `Deployment regression blast radius` | One failing sub-feature crashes entire application deployment. | Implement feature flags and canary deployment strategies to safely isolate new code. |

## References

- [Martin Fowler - MonolithFirst](https://martinfowler.com/bliki/MonolithFirst.html)
