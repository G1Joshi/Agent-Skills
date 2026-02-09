---
name: express
description: Express.js Node.js web framework for REST APIs and middleware. Use for Node.js backends.
---

# Express.js

Minimal and flexible Node.js web framework for building APIs.

## When to Use

- Building REST APIs
- Middleware-based request processing
- Backend for SPAs
- Microservices

## Quick Start

```javascript
import express from "express";
import cors from "cors";

const app = express();

app.use(cors());
app.use(express.json());

app.get("/api/users", async (req, res) => {
  const users = await db.users.findAll();
  res.json(users);
});

app.listen(3000);
```

## Core Concepts

### Middleware

```javascript
// Logger middleware
const logger = (req, res, next) => {
  console.log(`${req.method} ${req.path}`);
  next();
};

// Auth middleware
const auth = async (req, res, next) => {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) return res.status(401).json({ error: "Unauthorized" });

  try {
    req.user = await verifyToken(token);
    next();
  } catch {
    res.status(401).json({ error: "Invalid token" });
  }
};

app.use(logger);
app.use("/api/protected", auth);
```

### Route Organization

```javascript
// routes/users.js
import { Router } from "express";
const router = Router();

router.get("/", async (req, res) => {
  res.json(await User.findAll());
});

router.get("/:id", async (req, res) => {
  const user = await User.findById(req.params.id);
  if (!user) return res.status(404).json({ error: "Not found" });
  res.json(user);
});

router.post("/", async (req, res) => {
  const user = await User.create(req.body);
  res.status(201).json(user);
});

export default router;

// app.js
app.use("/api/users", usersRouter);
```

## Common Patterns

### Error Handling

```javascript
// Custom error class
class ApiError extends Error {
  constructor(message, statusCode = 500) {
    super(message);
    this.statusCode = statusCode;
  }
}

// Async wrapper
const asyncHandler = (fn) => (req, res, next) =>
  Promise.resolve(fn(req, res, next)).catch(next);

// Global error handler (must be last)
app.use((err, req, res, next) => {
  console.error(err);
  res.status(err.statusCode || 500).json({
    error: err.message || "Internal server error",
  });
});

// Usage
app.get(
  "/users/:id",
  asyncHandler(async (req, res) => {
    const user = await User.findById(req.params.id);
    if (!user) throw new ApiError("User not found", 404);
    res.json(user);
  }),
);
```

## Best Practices

**Do**:

- Use helmet for security headers
- Validate input with Zod/Joi
- Use async error handler wrapper
- Structure routes in separate files

**Don't**:

- Trust user input without validation
- Expose stack traces in production
- Mix business logic in routes
- Forget to handle async errors

## Troubleshooting

| Issue               | Cause                   | Solution               |
| ------------------- | ----------------------- | ---------------------- |
| 404 for all routes  | Router order            | Check middleware order |
| Unhandled rejection | Missing error handler   | Add async wrapper      |
| CORS error          | Missing CORS middleware | Add cors() middleware  |

## References

- [Express.js Documentation](https://expressjs.com/)
- [Express Best Practices](https://expressjs.com/en/advanced/best-practice-security.html)
