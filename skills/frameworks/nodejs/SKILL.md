---
name: nodejs
description: Node.js server-side JavaScript runtime with npm ecosystem. Use for backend development.
---

# Node.js

Node.js is a cross-platform JavaScript runtime environment. Node.js 22 (LTS 2025) brings native TypeScript support (experimental), a built-in Test Runner, and a native WebSocket client.

## When to Use

- **Real-time Apps**: Chat, Gaming, Collaboration (WebSockets).
- **API Servers**: High concurrency with non-blocking I/O.
- **Tooling**: The foundation of modern frontend toolchains (Vite, Next.js).

## Quick Start (Native Features)

```javascript
// Native Test Runner (No Jest needed)
import { test, assert } from "node:test";

test("synchronous passing test", (t) => {
  assert.strictEqual(1, 1);
});

// Native WebSocket
const ws = new WebSocket("ws://example.com/socket");
ws.onopen = () => console.log("Connected");
```

## Core Concepts

### Event Loop

Single-threaded, non-blocking I/O. Heavy CPU tasks block the loop (bad), but I/O tasks are offloaded to OS (good).

### Streams

Process huge files piece-by-piece without loading them into memory.

### Native APIs (2025)

Node now has `fetch`, `test`, `watch`, and `.env` support built-in. You need fewer dependencies than in 2020.

## Best Practices (2025)

**Do**:

- **Use `node:test`**: Drop Jest/Mocha for simple projects.
- **Use `node --env-file`**: Drop `dotenv` dependency.
- **Use Async/Await**: Callbacks are dead. Long live Promises.

**Don't**:

- **Don't block the Event Loop**: Don't run Crypto or Image processing on the main thread. Use Worker Threads.
- **Don't use `require`**: New projects should use ESM (`import`).

## References

- [Node.js Documentation](https://nodejs.org/docs/latest/api/)
