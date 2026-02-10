---
name: express
description: Express.js Node.js web framework for REST APIs and middleware. Use for Node.js backends.
---

# Express

Express is the standard web framework for Node.js. Express 5 (2025) finally stabilizes modern features like Promise support in middleware, removing the need for `express-async-errors`.

## When to Use

- **Microservices**: Lightweight and fast.
- **REST APIs**: The standard for building JSON APIs in Node.
- **Learning**: The best way to learn how HTTP works in Node.

## Quick Start (Express 5)

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

### Middleware

Functions that have access to `req`, `res`, and `next`. They form a pipeline.
`Log -> Auth -> BodyParse -> RouteHandler`.

### Routing

`app.get()`, `app.post()`. Simple regex-based routing.

## Best Practices (2025)

**Do**:

- **Upgrade to Express 5**: Native Promise support is a game changer for cleaner code.
- **Use `helmet`**: Security headers are mandatory.
- **Structure properly**: Don't put everything in `app.js`. Use `express.Router()`.

**Don't**:

- **Don't stick to CommonJS**: Express 5 supports ESM. Use `import`.
- **Don't use `body-parser` separate package**: Use `express.json()` (included since v4, standard in v5).

## References

- [Express 5 Migration Guide](https://expressjs.com/en/guide/migrating-5.html)
