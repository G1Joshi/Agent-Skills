---
name: bun
description: Expert Bun runtime assistance covering high-performance JS/TS execution, built-in bundler, package manager, and test runner. Use when executing TypeScript natively, running fast scripts, or serving HTTP APIs.
---

# Bun

Bun is a drop-in replacement for Node.js, written in Zig. It is **fast**. v1.1 brings Windows support.

## When to Use

- **All-in-One JavaScript/TypeScript Runtime**: Ultra-fast alternative to Node.js for server-side apps, bundlers, and package managers.
- **High-Performance HTTP Services**: Building web APIs using `Bun.serve()` with native WebSocket and TLS support.
- **Rapid Package Management**: Executing `bun install` with 10x-30x speedups over legacy package managers.
- **Built-in SQLite & Testing**: Developing microservices with zero-dependency native SQLite (`bun:sqlite`) and `bun:test`.

## Quick Start

```typescript
// server.ts
const server = Bun.serve({
  port: 3000,
  fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === "/api/health") {
      return Response.json({ status: "ok", runtime: "bun" });
    }
    return new Response("Hello from Bun!", { status: 200 });
  },
});

console.log(`Listening on http://localhost:${server.port}`);
```

## Core Concepts

#High-Throughput HTTP Server with Bun.serve()

Native HTTP/1.1 and HTTP/2 web server with WebSockets:

```typescript
const server = Bun.serve({
  port: 3000,
  fetch(req, server) {
    const url = new URL(req.url);

    // WebSocket upgrade
    if (url.pathname === "/chat") {
      if (server.upgrade(req)) return;
      return new Response("Upgrade failed", { status: 400 });
    }

    if (url.pathname === "/api/health") {
      return Response.json({ status: "healthy", timestamp: Date.now() });
    }

    return new Response("Not Found", { status: 404 });
  },
  websocket: {
    message(ws, message) {
      ws.send(`Echo: ${message}`);
    },
    open(ws) {
      console.log("WebSocket client connected");
    },
    close(ws) {
      console.log("WebSocket client disconnected");
    },
  },
});

console.log(`Bun server running at http://localhost:${server.port}`);
```

#Native SQLite with bun:sqlite

High-speed zero-dependency embedded database:

```typescript
import { Database } from "bun:sqlite";

const db = new Database("app.db", { create: true });

// Execute schema creation
db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
`);

// Prepared statement
const insert = db.prepare("INSERT INTO users (email) VALUES ($email)");
insert.run({ $email: "alice@example.com" });

const query = db.prepare("SELECT * FROM users WHERE email = $email");
const user = query.get({ $email: "alice@example.com" });
console.log("Found user:", user);
```

#Fast Test Runner with bun:test

Jest-compatible testing without compilation overhead:

```typescript
import { describe, expect, test, beforeAll } from "bun:test";

describe("Math and Array Utilities", () => {
  test("calculates sum correctly", () => {
    const sum = [1, 2, 3, 4].reduce((a, b) => a + b, 0);
    expect(sum).toBe(10);
  });

  test("resolves async promises", async () => {
    const data = await Promise.resolve({ success: true });
    expect(data.success).toBeTrue();
  });
});
```

## Common Patterns

### High-Speed SQLite Ingestion with bun:sqlite

**Problem**: External SQLite packages require native compile toolchains and introduce overhead in Node.js.

**Solution**:
Use Bun's built-in zero-dependency SQLite module:

```typescript
import { Database } from "bun:sqlite";

const db = new Database("store.db");
db.run(
  "CREATE TABLE IF NOT EXISTS metrics (id INTEGER PRIMARY KEY, value REAL)",
);

const insert = db.prepare("INSERT INTO metrics (value) VALUES (?)");
db.transaction((values: number[]) => {
  for (const v of values) insert.run(v);
})([1.2, 3.4, 5.6]);

const results = db.query("SELECT * FROM metrics LIMIT 5").all();
console.log(results);
```

## Best Practices (2026)

- **Do** use `bun run` and `bunx` to avoid npm script execution overhead.
- **Do** leverage `Bun.file()` for high-performance zero-copy file streaming.
- **Do** run TypeScript files directly (`bun run index.ts`) without requiring `tsc` or `ts-node`.
- **Do** check Node.js API compatibility flags when porting legacy native C++ addons (`node-gyp`).
- **Don't** use `npm install` in Bun projects; stick to `bun install` to preserve `bun.lock`.
- **Don't** use external SQLite packages like `better-sqlite3`; use native `bun:sqlite`.
- **Don't** spawn child processes for simple shell tasks; use `Bun.$` shell scripting.

## Troubleshooting

| Error                                  | Cause                                              | Solution                                                        |
| :------------------------------------- | :------------------------------------------------- | :-------------------------------------------------------------- |
| `error: Cannot find package '...'`     | Dependency not installed in current directory.     | Run `bun add <package-name>` or verify `bun.lockb` integrity.   |
| `TypeError: Node.js API not supported` | Edge-case Node API not yet implemented in Bun.     | Check compatibility matrix or run with `NODE_OPTIONS` polyfill. |
| `Port 3000 is already in use`          | Another server instance already listening on port. | Specify custom port via `PORT=3001 bun run server.ts`.          |

## References

- [Bun Documentation](https://bun.sh/)
