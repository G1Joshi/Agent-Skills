---
name: hono
description: Expert Hono framework assistance covering ultra-fast routing, Web Standards, multi-runtime support (Cloudflare Workers, Deno, Bun, Node), and RPC. Use when developing edge APIs and lightweight microservices.
---

# Hono

Hono (Japanese for "Flame") is a small, simple, and ultrafast web framework built on Web Standards. It runs anywhere: Cloudflare Workers, Fastly, Deno, Bun, Node.js, and Vercel.

## When to Use

- **Multi-Runtime Edge Web Applications**: Running seamlessly on Cloudflare Workers, Deno, Bun, Fastly, AWS Lambda, or Node.js.
- **Ultrafast Microservices**: Sub-millisecond routing with RegExpRouter and zero external dependencies.
- **End-to-End Type Safety (Hono RPC)**: Sharing API client types with frontend web applications without code generation.
- **Web Standard APIs**: Building on native `Request` and `Response` web standard interfaces.

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

### Multi-Runtime API with RegExpRouter

Lightweight REST API with path parameter extraction:

```typescript
import { Hono } from "hono";
import { logger } from "hono/logger";
import { cors } from "hono/cors";

const app = new Hono();

app.use("*", logger());
app.use("/api/*", cors());

app.get("/api/users/:id", (c) => {
  const id = c.req.param("id");
  const role = c.req.query("role") || "member";

  return c.json({
    id,
    role,
    runtime: "Cloudflare / Edge / Bun / Node",
    timestamp: Date.now(),
  });
});

export default app;
```

### Type-Safe Request Validation with Zod Validator

Validating request bodies, headers, and query strings:

```typescript
import { Hono } from "hono";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

const app = new Hono();

const userSchema = z.object({
  username: z.string().min(3),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

app.post("/api/users", zValidator("json", userSchema), (c) => {
  // c.req.valid('json') is fully typed according to userSchema
  const data = c.req.valid("json");
  return c.json({ success: true, user: data }, 201);
});
```

### Hono RPC: Type-Safe Client Sharing

Exporting API routes for direct consumption in frontend clients:

```typescript
// server.ts
import { Hono } from "hono";
const app = new Hono().get("/api/posts", (c) =>
  c.json([{ id: 1, title: "Hono Edge" }]),
);

export type AppType = typeof app;

// client.ts (In React / Next.js)
import { hc } from "hono/client";
import type { AppType } from "./server";

const client = hc<AppType>("https://api.example.com");
const res = await client.api.posts.$get();
const posts = await res.json(); // Fully typed!
```

## Common Patterns

### End-to-End Type-Safe RPC Client

**Problem**: Maintaining synchronized TypeScript API client contracts between edge backend and frontend.

**Solution**:
Export Hono AppType and consume with `hono/client`:

```typescript
// server.ts
import { Hono } from "hono";
const app = new Hono().get("/api/user/:id", (c) => {
  return c.json({ id: c.req.param("id"), name: "Alice" });
});
export type AppType = typeof app;

// client.ts
import { hc } from "hono/client";
import type { AppType } from "./server";

const client = hc<AppType>("https://api.example.com");
const res = await client.api.user[":id"].$get({ param: { id: "123" } });
const data = await res.json(); // Strictly typed { id: string, name: string }
```

## Best Practices

**Do**:

- Leverage Hono RPC (`hc<AppType>`) to achieve end-to-end type safety between backend and frontend without tRPC overhead.
- Use `@hono/zod-validator` or `@hono/valibot-validator` to enforce strict validation at edges.
- Target Web Standards so the same application code deploys to Cloudflare Workers, Bun, and Node.js without modification.
- Chain router routes (`new Hono().get().post()`) to preserve full RPC type inference.

**Don't**:

- Use Node-specific globals (`process.env`) without polyfills if targeting edge runtimes; use `c.env`.
- Instantiate heavy global state that assumes persistent memory across serverless edge invocations.
- Omit error boundary handlers (`app.onError`) in production apps.

## Troubleshooting

| Error                                                   | Cause                                                          | Solution                                                                    |
| :------------------------------------------------------ | :------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `TypeError: c.req.json is not a function`               | Accessing body parsing as method rather than awaiting promise. | Use `const body = await c.req.json()`.                                      |
| `Route not matching on sub-path`                        | Route prefix mismatch in `app.route('/prefix', subApp)`.       | Ensure subApp paths are relative to mount point (`/` instead of `/prefix`). |
| `Environment variables undefined on Cloudflare Workers` | Accessing `process.env` instead of `c.env`.                    | Extract bindings from context: `c.env.MY_KV_STORE`.                         |

## References

- [Hono Documentation](https://hono.dev/)
