---
name: fiber
description: Fiber Express-inspired Go web framework. Use for Go APIs.
---

# Fiber

Fiber is an **Express.js** inspired framework for Go, running on `fasthttp` (the fastest HTTP engine for Go). v3 brings generic support and better middleware.

## When to Use

- **Benchmarks**: You need the absolute highest raw throughput.
- **Node.js Background**: The API (`app.Get("/", ...)` feels like Express).
- **Zero Allocation**: Obsessive memory optimization.

## Core Concepts

### Fasthttp

Doesn't use `net/http`. Much faster but incompatible with some standard library middlewares.

### Prefork

Spawn multiple processes (SO_REUSEPORT) to utilize all cores.

## Best Practices (2025)

**Do**:

- **Use `v3`**: For stable generic support.
- **Be careful with Prefork**: Can cause issues with socket connections if not handled.
- **Use Built-in Middleware**: Cache, Compress, CORS are highly optimized.

**Don't**:

- **Don't hold references**: `fasthttp` reuses context objects. Copy strings if you need them after handler returns.

## References

- [Fiber Documentation](https://gofiber.io/)
