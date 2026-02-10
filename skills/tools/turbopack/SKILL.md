---
name: turbopack
description: Turbopack Rust-powered bundler. Use for fast builds.
---

# Turbopack

Turbopack is the build engine built by Vercel. In 2025, it is **Stable** in Next.js and powers the fastest dev server in the ecosystem.

## When to Use

- **Next.js**: It's the default dev engine (`next dev --turbo`).
- **Scale**: Designed for monorepos with thousands of pages.

## Core Concepts

### Incremental Computation

Turbopack never does the same work twice. It caches function results at a granular level (the "Function Level Caching").

### Lazy Bundling

It only bundles the dynamic imports and pages you actually visit.

### Request Level Compilation

Compiles code only when a request hits the server.

## Best Practices (2025)

**Do**:

- **Use `--turbo`**: Enable it in Next.js for instant HMR.
- **Trust the Cache**: Turbopack handles invalidation correctly.

**Don't**:

- **Don't configure it manually**: In 2025, it's mostly configured via framework adapters (Next.js).

## References

- [Turbopack Documentation](https://turbo.build/pack)
