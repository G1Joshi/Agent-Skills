---
name: hono
description: Hono ultrafast web framework for edge computing. Use for edge APIs.
---

# Hono

Hono (Japanese for "Flame") is a small, simple, and ultrafast web framework built on Web Standards. It runs anywhere: Cloudflare Workers, Fastly, Deno, Bun, Node.js, and Vercel.

## When to Use

- **Edge Computing**: Explicitly designed for Cloudflare Workers / Edge runtimes.
- **Performance**: Uses `RegExpRouter`, making it significantly faster than Express.
- **Single File API**: Perfect for small microservices or proxy servers.

## Quick Start

```typescript
import { Hono } from "hono";
const app = new Hono();

app.get("/", (c) => c.text("Hello Hono!"));

app.get("/user/:name", (c) => {
  const name = c.req.param("name");
  return c.json({ message: `Hello ${name}!` });
});

export default app;
```

## Core Concepts

### Web Standards

Hono uses standard `Request` and `Response` objects. No proprietary API wrapper.

### Middleware

Similar to Express but `await next()`. Batteries included: CORS, JWT, Basic Auth, Cache.

### RPC (Hono RPC)

Share types between client and server for end-to-end type safety without GraphQL.

## Best Practices (2025)

**Do**:

- **Use Hono RPC**: If you control both client and server, the typed client is amazing.
- **Run on Bun**: Hono + Bun is currently one of the fastest combinations for JS backends.

**Don't**:

- **Don't use heavy Node.js dependencies**: If targeting Cloudflare Workers, avoid packages that rely on `fs` or native Node modules.

## References

- [Hono Documentation](https://hono.dev/)
