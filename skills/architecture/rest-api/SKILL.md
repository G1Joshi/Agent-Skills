---
name: rest-api
description: RESTful API design with HTTP methods and status codes. Use for HTTP API design.
---

# REST API

RESTful API design for web services.

## When to Use

- Web service APIs
- CRUD operations
- Resource-based endpoints
- Stateless communication

## Quick Start

```typescript
// Express REST endpoints
app.get("/api/users", getAllUsers);
app.get("/api/users/:id", getUserById);
app.post("/api/users", createUser);
app.put("/api/users/:id", updateUser);
app.delete("/api/users/:id", deleteUser);
```

## Core Concepts

### HTTP Methods

```typescript
// GET - Retrieve resource
app.get("/api/users/:id", async (req, res) => {
  const user = await db.users.findUnique({ where: { id: req.params.id } });
  if (!user) return res.status(404).json({ error: "User not found" });
  res.json(user);
});

// POST - Create resource
app.post("/api/users", async (req, res) => {
  const user = await db.users.create({ data: req.body });
  res.status(201).json(user);
});

// PUT - Replace resource
app.put("/api/users/:id", async (req, res) => {
  const user = await db.users.update({
    where: { id: req.params.id },
    data: req.body,
  });
  res.json(user);
});

// PATCH - Partial update
app.patch("/api/users/:id", async (req, res) => {
  const user = await db.users.update({
    where: { id: req.params.id },
    data: req.body,
  });
  res.json(user);
});

// DELETE - Remove resource
app.delete("/api/users/:id", async (req, res) => {
  await db.users.delete({ where: { id: req.params.id } });
  res.status(204).send();
});
```

### Status Codes

```typescript
// 2xx Success
res.status(200).json(data); // OK
res.status(201).json(created); // Created
res.status(204).send(); // No Content

// 4xx Client Error
res.status(400).json({ error: "Bad request" }); // Bad Request
res.status(401).json({ error: "Unauthorized" }); // Unauthorized
res.status(403).json({ error: "Forbidden" }); // Forbidden
res.status(404).json({ error: "Not found" }); // Not Found
res.status(422).json({ error: "Validation failed" }); // Unprocessable

// 5xx Server Error
res.status(500).json({ error: "Internal error" }); // Internal Error
```

## Common Patterns

### Pagination

```typescript
app.get("/api/users", async (req, res) => {
  const page = parseInt(req.query.page as string) || 1;
  const limit = parseInt(req.query.limit as string) || 20;
  const skip = (page - 1) * limit;

  const [users, total] = await Promise.all([
    db.users.findMany({ skip, take: limit }),
    db.users.count(),
  ]);

  res.json({
    data: users,
    meta: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  });
});
```

### Error Handling

```typescript
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(err);
  res.status(500).json({
    error: "Internal server error",
    message: process.env.NODE_ENV === "development" ? err.message : undefined,
  });
});
```

## Best Practices

**Do**:

- Use nouns for resources
- Return proper status codes
- Implement pagination
- Version your API

**Don't**:

- Use verbs in URLs
- Return 200 for errors
- Expose internal errors
- Skip input validation

## Troubleshooting

| Issue              | Cause               | Solution          |
| ------------------ | ------------------- | ----------------- |
| 404 on valid route | Wrong method        | Check HTTP method |
| CORS error         | Missing headers     | Configure CORS    |
| 500 error          | Unhandled exception | Add error handler |

## References

- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
