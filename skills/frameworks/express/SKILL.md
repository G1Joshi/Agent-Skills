---
name: express
description: Expert Express.js assistance covering routing, middleware pipelines, error handling, and REST API design. Use when building Node.js backend services and web APIs.
---

# Express

Express is the standard web framework for Node.js. Express 5 (2025) finally stabilizes modern features like Promise support in middleware, removing the need for `express-async-errors`.

## When to Use

- **Fast Node.js REST API Development**: Building flexible, lightweight HTTP microservices and web backends.
- **Established Node.js Ecosystem Services**: Leveraging thousands of battle-tested npm middleware packages.
- **Web App Routing & Server-Side Rendering**: Serving dynamic server-side templates with EJS, Pug, or Handlebars.
- **API Gateways & Proxy Layers**: Routing, inspecting, and transforming inbound microservice requests.

## Quick Start

```javascript
import express from "express";
const app = express();

// Express 5 handles async errors automatically!
app.get("/", async (req, res) => {
  const user = await db.getUser(); // If this throws, Express catches it.
  res.json(user);
});

app.listen(3000);
```

## Core Concepts

#Modular Route Handlers & Express Router

Structuring scalable APIs with decoupled sub-routers:

```typescript
import express, { Request, Response, NextFunction } from "express";

const userRouter = express.Router();

interface UserPayload {
  username: string;
  email: string;
}

userRouter.get(
  "/:id",
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const userId = req.params.id;
      res.json({ id: userId, username: `user_${userId}`, status: "active" });
    } catch (error) {
      next(error);
    }
  },
);

userRouter.post(
  "/",
  async (
    req: Request<{}, {}, UserPayload>,
    res: Response,
    next: NextFunction,
  ) => {
    try {
      const { username, email } = req.body;
      if (!username || !email) {
        res.status(400).json({ error: "Username and email are required" });
        return;
      }
      res.status(201).json({ id: Date.now(), username, email });
    } catch (error) {
      next(error);
    }
  },
);

export default userRouter;
```

#Custom Middleware & Security Pipeline

Hardening Express with Helmet, CORS, and compression:

```typescript
import express from "express";
import helmet from "helmet";
import cors from "cors";
import compression from "compression";
import userRouter from "./userRouter";

const app = express();

app.use(helmet());
app.use(cors({ origin: "https://trusted-domain.com" }));
app.use(compression());
app.use(express.json({ limit: "1mb" }));
app.use(express.urlencoded({ extended: true }));

app.use("/api/v1/users", userRouter);

app.listen(3000, () => {
  console.log("Express API listening on port 3000");
});
```

#Centralized Error Handling Middleware

Uniform error trapping conforming to 4-argument signature:

```typescript
import { Request, Response, NextFunction } from "express";

interface AppError extends Error {
  statusCode?: number;
}

export function errorHandler(
  err: AppError,
  req: Request,
  res: Response,
  next: NextFunction,
): void {
  const statusCode = err.statusCode || 500;
  console.error(`[Error] ${req.method} ${req.path}:`, err.message);

  res.status(statusCode).json({
    error: {
      message: err.message || "Internal Server Error",
      status: statusCode,
      timestamp: new Date().toISOString(),
    },
  });
}
```

## Common Patterns

### Centralized Async Error Handling Middleware

**Problem**: Unhandled promise rejections inside async route handlers cause server crashes or hanging requests.

**Solution**:
Use an async handler wrapper and centralized error middleware:

```javascript
const asyncHandler = (fn) => (req, res, next) => {
  Promise.resolve(fn(req, res, next)).catch(next);
};

app.get(
  "/api/users/:id",
  asyncHandler(async (req, res) => {
    const user = await db.findUser(req.params.id);
    if (!user) throw new NotFoundError("User not found");
    res.json(user);
  }),
);

// Centralized error handler (must have 4 arguments)
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(err.statusCode || 500).json({ error: err.message });
});
```

## Best Practices (2026)

- **Do** always mount the 4-argument error-handling middleware (`(err, req, res, next)`) at the very end of the middleware stack.
- **Do** use `helmet()` to secure HTTP headers (HSTS, CSP, X-Frame-Options) against common exploits.
- **Do** wrap async handler functions or use Express 5 to catch rejected promises automatically.
- **Do** limit request body payload size (`express.json({ limit: '100kb' })`) to defend against DoS attacks.
- **Don't** use synchronous I/O operations (`fs.readFileSync`) inside route handlers.
- **Don't** omit `return` after sending responses (`res.json(...)`) inside conditional branches.
- **Don't** expose stack traces in production error responses (`NODE_ENV === 'production'`).

## Troubleshooting

| Error                                                  | Cause                                                                     | Solution                                                                             |
| :----------------------------------------------------- | :------------------------------------------------------------------------ | :----------------------------------------------------------------------------------- |
| `Cannot set headers after they are sent to the client` | Attempted to call `res.json()` or `res.send()` multiple times in handler. | Add `return` before response calls: `return res.status(400).send(...)`.              |
| `req.body is undefined`                                | Missing body-parsing middleware in application pipeline.                  | Add `app.use(express.json())` and `app.use(express.urlencoded({ extended: true }))`. |
| `EADDRINUSE: address already in use :::3000`           | Port 3000 occupied by previous node process.                              | Kill process with `npx kill-port 3000` or change listening port.                     |

## References

- [Express 5 Migration Guide](https://expressjs.com/en/guide/migrating-5.html)
