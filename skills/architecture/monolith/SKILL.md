---
name: monolith
description: Monolithic architecture single deployment. Use for simple systems.
---

# Monolith (Traditional)

A Monolithic architecture is built as a single unit. All functional components (UI, Business Logic, Data Access) are tightly integrated using a shared database and running in the same process.

## When to Use

- Proof of Concept (PoC) or MVP.
- Very small teams (< 5 developers).
- Simple CRUD applications with low complexity.
- When latency must be absolute zero and throughput is not the bottleneck.

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

### Single Process

The entire app runs in one memory space. Scaling means "Vertical Scaling" (bigger server) or "Horizontal Scaling" (cloning the entire monolith behind a load balancer).

### Shared Database

All components read/write to the same massive database. JOINs across any domains are easy and performant.

### Simplicity

One repo, one build pipeline, one deploy script. Infinite ease of debugging (step through everything).

## Common Patterns

### Layered Architecture

Even in a monolith, organize by technical layers (Presentation, Business, Data) to prevent spaghetti code.

### "Big Ball of Mud" (Anti-pattern)

The chaotic state a monolith reaches without discipline, where everything depends on everything else.

## Best Practices

**Do**:

- Keep code clean and modular (files/folders) even if deployment is monolithic.
- Use **Feature Flags** to manage releases.
- Optimize **Database Queries** early, as the single DB is the bottleneck.

**Don't**:

- Don't let the build time exceed 10-15 minutes (split if it does).
- Don't allow "Spaghetti Coupling" (Circular dependencies).

## References

- [Martin Fowler - MonolithFirst](https://martinfowler.com/bliki/MonolithFirst.html)
