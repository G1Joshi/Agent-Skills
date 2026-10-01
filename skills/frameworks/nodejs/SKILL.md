---
name: nodejs
description: Expert Node.js assistance covering asynchronous event loop, streams, worker threads, buffer manipulation, and ESM. Use when building scalable backend services, CLI utilities, or network servers.
---

# Node.js

Node.js is a cross-platform asynchronous event-driven JavaScript runtime, featuring a built-in Test Runner, native WebSocket client, and modern ESM module execution.

## When to Use

- **Scalable Asynchronous Microservices**: Building event-driven I/O-intensive web APIs on Node.js 22 LTS.
- **Real-Time Data Streaming & WebSockets**: Processing streaming data using native `node:stream` and `Transform` streams.
- **CLI Development & Build Tooling**: Building developer tools, linters, and deployment automations with npm.
- **Worker Threads & CPU-Bound Offloading**: Offloading cryptographic hashing, compression, and image manipulation.

## Quick Start

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

### Modern Native HTTP Server & Fetch

Zero-dependency HTTP server utilizing Node.js modern standard APIs:

```javascript
import { createServer } from "node:http";

const server = createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  if (url.pathname === "/api/health" && req.method === "GET") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ status: "ok", nodeVersion: process.version }));
    return;
  }

  res.writeHead(404, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ error: "Route not found" }));
});

server.listen(3000, () => {
  console.log("Node.js server listening on http://localhost:3000");
});
```

### Stream Pipelines with node:stream/promises

Safe, backpressure-managed file and network streaming:

```javascript
import { createReadStream, createWriteStream } from "node:fs";
import { pipeline } from "node:stream/promises";
import { createGzip } from "node:zlib";

async function compressFile(sourcePath, destPath) {
  try {
    await pipeline(
      createReadStream(sourcePath),
      createGzip(),
      createWriteStream(destPath),
    );
    console.log(`Successfully compressed ${sourcePath} -> ${destPath}`);
  } catch (err) {
    console.error("Pipeline compression failed:", err);
  }
}
```

### Native Test Runner with node:test

Fast, zero-dependency testing built directly into the runtime:

```javascript
import test, { describe, it } from "node:test";
import assert from "node:assert/strict";

describe("User Authentication", () => {
  it("validates password minimum length", () => {
    const password = "supersecretpass";
    assert.ok(password.length >= 8, "Password must be >= 8 chars");
  });

  it("verifies async promise resolution", async () => {
    const token = await Promise.resolve("jwt-token-xyz");
    assert.equal(token, "jwt-token-xyz");
  });
});
```

## Common Patterns

### High-Throughput Stream Pipeline with Backpressure

**Problem**: Reading large files directly into memory with `fs.readFile` causes OOM crashes under load.

**Solution**:
Use `stream.pipeline` for automatic backpressure management:

```javascript
import { pipeline } from "node:stream/promises";
import fs from "node:fs";
import zlib from "node:zlib";

async function compressLogFile(inputPath, outputPath) {
  await pipeline(
    fs.createReadStream(inputPath),
    zlib.createGzip(),
    fs.createWriteStream(outputPath),
  );
  console.log("Compression pipeline completed successfully.");
}
```

## Best Practices

**Do**:

- Target Node.js 22 LTS or newer with native fetch, web streams, and native test runner.
- Use the `node:` protocol prefix (`import fs from 'node:fs'`) for all built-in modules.
- Use `node:stream/promises` and `pipeline` to handle stream backpressure and error propagation.
- Handle uncaught exceptions (`process.on('uncaughtException')`) and trigger graceful shutdown.

**Don't**:

- Block the single-threaded Event Loop with heavy synchronous calls (`fs.readFileSync`, long regex).
- Use CommonJS (`require()`) in greenfield applications; adopt ECMAScript Modules (`"type": "module"`).
- Ignore unhandled promise rejections; configure `--unhandled-rejections=strict`.

## Troubleshooting

| Error                                                                      | Cause                                                 | Solution                                                                                    |
| :------------------------------------------------------------------------- | :---------------------------------------------------- | :------------------------------------------------------------------------------------------ |
| `ERR_REQUIRE_ESM: Must use import to load ES Module`                       | Using `require()` on a modern ESM-only package.       | Use `import` or dynamic `await import('...')` in CommonJS.                                  |
| `MaxListenersExceededWarning: Possible EventEmitter memory leak`           | Adding event listeners in loop without removing them. | Remove listeners with `emitter.off()` or increase limit using `emitter.setMaxListeners(n)`. |
| `FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed` | Node.js process exceeded default 1.4GB memory limit.  | Start with expanded heap: `node --max-old-space-size=4096 app.js`.                          |

## References

- [Node.js Documentation](https://nodejs.org/docs/latest/api/)
