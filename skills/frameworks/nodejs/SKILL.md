---
name: nodejs
description: Node.js server-side JavaScript runtime with npm ecosystem, async patterns, and best practices. Use for backend development.
---

# Node.js

Server-side JavaScript runtime for building scalable backend applications.

## When to Use

- Building REST APIs and web servers
- Real-time applications with WebSockets
- CLI tools and scripts
- Microservices architecture

## Quick Start

```javascript
import express from "express";

const app = express();
app.use(express.json());

app.get("/api/users/:id", async (req, res) => {
  const user = await db.findUser(req.params.id);
  res.json(user);
});

app.listen(3000, () => console.log("Server running on port 3000"));
```

## Core Concepts

### ES Modules

```javascript
// package.json: "type": "module"
import fs from "node:fs/promises";
import path from "node:path";
import { createServer } from "node:http";

// Named exports
export function helper() {
  /* ... */
}
export const config = { port: 3000 };

// Default export
export default class Server {
  /* ... */
}
```

### Async Patterns

```javascript
// Async/await with error handling
async function processFile(path) {
  try {
    const data = await fs.readFile(path, "utf-8");
    return JSON.parse(data);
  } catch (error) {
    if (error.code === "ENOENT") {
      return null;
    }
    throw error;
  }
}

// Parallel execution
const [users, orders] = await Promise.all([fetchUsers(), fetchOrders()]);

// AbortController for cancellation
const controller = new AbortController();
setTimeout(() => controller.abort(), 5000);

const response = await fetch(url, { signal: controller.signal });
```

## Common Patterns

### Error Handling

```javascript
// Custom error class
class AppError extends Error {
  constructor(message, statusCode = 500) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
  }
}

// Global error handler
app.use((error, req, res, next) => {
  console.error(error);
  res.status(error.statusCode || 500).json({
    error: error.message || "Internal server error",
  });
});

// Async route wrapper
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

app.get(
  "/users",
  asyncHandler(async (req, res) => {
    const users = await User.findAll();
    res.json(users);
  }),
);
```

### Environment Configuration

```javascript
import dotenv from "dotenv";
dotenv.config();

const config = {
  port: process.env.PORT || 3000,
  database: process.env.DATABASE_URL,
  nodeEnv: process.env.NODE_ENV || "development",
};
```

## Best Practices

**Do**:

- Use ES modules (type: module)
- Handle errors with try/catch
- Use environment variables
- Implement graceful shutdown

**Don't**:

- Block the event loop
- Use callback-style code (use async/await)
- Ignore unhandled rejections
- Store secrets in code

## Troubleshooting

| Error              | Cause               | Solution                     |
| ------------------ | ------------------- | ---------------------------- |
| `EADDRINUSE`       | Port in use         | Kill process or change port  |
| Memory leak        | Uncleared listeners | Use WeakMap, clear listeners |
| Event loop blocked | Sync CPU work       | Use worker threads           |

## References

- [Node.js Documentation](https://nodejs.org/docs/)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
