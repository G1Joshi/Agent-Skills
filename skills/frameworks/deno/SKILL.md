---
name: deno
description: Expert Deno runtime assistance covering secure defaults, TypeScript out-of-the-box, standard library, and Deno Deploy. Use when building modern web backends, edge functions, or serverless scripts.
---

# Deno

Deno is a modern runtime for JavaScript, TypeScript, and WebAssembly with secure defaults, built-in developer tooling, and direct npm package compatibility.

## When to Use

- **Secure TypeScript/JavaScript Server Runtime**: Default-secure environment requiring explicit file, network, and environment permissions.
- **Edge Functions & Cloudflare/Deno Deploy**: Sub-millisecond cold start serverless endpoints and web APIs.
- **Zero-Config Scripting & Tooling**: Running scripts directly without `npm install`, `tsconfig.json`, or bundlers.
- **Standard Web APIs & Deno 2 Ecosystem**: Utilizing standard `fetch`, WebSockets, and seamless npm package compatibility.

## Quick Start

```typescript
// main.ts - Native TypeScript, zero config
Deno.serve({ port: 8000 }, (_req) => {
  return new Response("Hello from Deno!", {
    headers: { "content-type": "text/plain" },
  });
});
```

Run with network permission:

```bash
deno run --allow-net main.ts
```

## Core Concepts

### Modern HTTP Server with Deno.serve()

Built-in high-performance HTTP server using Web Standard `Request` and `Response`:

```typescript
// server.ts
Deno.serve({ port: 8000 }, (req: Request) => {
  const url = new URL(req.url);

  if (url.pathname === "/api/health") {
    return Response.json({
      status: "ok",
      uptime: performance.now(),
      denoVersion: Deno.version.deno,
    });
  }

  if (req.method === "POST" && url.pathname === "/api/echo") {
    return new Response(req.body, {
      headers: { "Content-Type": "application/json" },
    });
  }

  return new Response("Not Found", { status: 404 });
});
```

### Fine-Grained Permission Model

Explicit security sandbox permissions:

```bash
# Run with explicit network and read permissions
deno run --allow-net=api.github.com:443 --allow-read=/data main.ts

# Deno 2 workspace task execution
deno task start
```

### Deno KV Key-Value Database

Native ACID key-value store built into the runtime:

```typescript
// kv_store.ts
const kv = await Deno.openKv();

// Atomic transaction
const userKey = ["users", "user_101"];
const userCountKey = ["analytics", "total_users"];

const res = await kv
  .atomic()
  .set(userKey, { name: "Alice", role: "admin" })
  .sum(userCountKey, 1n)
  .commit();

if (res.ok) {
  const entry = await kv.get(userKey);
  console.log("Stored user:", entry.value);
}
```

## Common Patterns

### Granular Permission Flags in Production

**Problem**: Over-granting permissions (`--allow-all`) compromises zero-trust server environments.

**Solution**:
Specify restricted read/write and network allowlists:

```bash
# Allow read only from ./config and network only to specific domain
deno run   --allow-read=./config   --allow-net=api.stripe.com,auth.mycompany.com   --allow-env=PORT,DATABASE_URL   server.ts
```

## Best Practices

**Do**:

- Target Deno 2 with native `deno.json` workspace and dependency management.
- Run scripts with minimal permissions (`--allow-net=api.domain.com`) rather than `--allow-all` in production.
- Use `deno fmt` and `deno lint` to enforce formatting and static analysis across projects.
- Utilize `Deno.serve()` instead of legacy `std/http` server modules.

**Don't**:

- Grant `--allow-all` (-A) in production deployment scripts; adhere to least privilege.
- Use Node.js proprietary modules (`fs`, `http`) when Web Standard APIs (`fetch`, `ReadableStream`) are available.
- Commit untracked remote URLs without lockfiles; use `deno.lock` for reproducible dependency graphs.

## Troubleshooting

| Error                                                        | Cause                                                              | Solution                                                              |
| :----------------------------------------------------------- | :----------------------------------------------------------------- | :-------------------------------------------------------------------- |
| `PermissionDenied: Requires net access to ...`               | Script attempted network connection without `--allow-net` flag.    | Add `--allow-net` or `--allow-net=<host>` flag when launching script. |
| `Module not found: Relative import path "..." not supported` | Missing explicit `.ts` or `.js` file extension in import path.     | Append explicit `.ts` extension to all relative file imports.         |
| `error: TS2304 [ERROR]: Cannot find name 'Deno'`             | Editor TypeScript language server configured for standard Node.js. | Enable Deno LSP extension in VS Code (`deno.enable: true`).           |

## References

- [Deno Documentation](https://deno.com/)
