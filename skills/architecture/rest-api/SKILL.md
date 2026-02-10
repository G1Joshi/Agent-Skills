---
name: rest-api
description: REST API design with HTTP methods and status codes. Use for web APIs.
---

# REST API

Representational State Transfer (REST) is the architectural style for distributed hypermedia systems. It relies on stateless, client-server, cacheable communications protocols (mostly HTTP).

## When to Use

- **Public APIs**: The universal standard; easiest for 3rd parties to consume.
- **Simple Resource Access**: Perfect for CRUD (Create, Read, Update, Delete) operations.
- **Caching**: When you need to leverage HTTP caching (CDNs, Browsers).

## Quick Start

```typescript
// Express.js Example
app.get("/users/:id", async (req, res) => {
  const user = await db.find(req.params.id);
  if (!user) return res.status(404).json({ error: "Not Found" });

  // HATEOAS (Hypermedia As The Engine Of Application State) - optional but "True REST"
  res.json({
    ...user,
    links: {
      self: `/users/${user.id}`,
      orders: `/users/${user.id}/orders`,
    },
  });
});
```

## Core Concepts

### Resources

Everything is a resource identified by a URI (`/users/123`).

### HTTP Verbs

Use verbs to define actions, not URIs.

- `GET /orders` (List)
- `POST /orders` (Create)
- `PATCH /orders/1` (Update partial)
- `DELETE /orders/1` (Remove)

### Statelessness

Each request must contain all information necessary to understand the request. The server accepts no session state.

## Common Patterns

### Filtering, Sorting, Pagination

Standard query params: `?sort=-created_at&limit=10&page=2&status=active`.

### Versioning

- URI Versioning: `/v1/users` (Most common).
- Header Versioning: `Accept: application/vnd.myapi.v1+json`.

## Best Practices

**Do**:

- Use proper **HTTP Status Codes** (200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Server Error).
- Use **Snake Case** (`user_id`) in JSON responses (standard convention) or camelCase if consistent with JS ecosystem.
- Implement **Rate Limiting** to protect resources.

**Don't**:

- Don't use GET for state-changing operations.
- Don't return 200 OK for errors (e.g., `{ "error": "failed" }` with status 200).
- Don't expose database IDs if possible (use UUIDs).

## Troubleshooting

| Error                        | Cause                                  | Solution                                             |
| :--------------------------- | :------------------------------------- | :--------------------------------------------------- |
| `405 Method Not Allowed`     | Sending POST to a GET-only endpoint.   | Check HTTP verb.                                     |
| `415 Unsupported Media Type` | Sending XML when JSON expected.        | Set `Content-Type: application/json`.                |
| `CORS Error`                 | Browser blocking cross-origin request. | Set `Access-Control-Allow-Origin` headers on server. |

## References

- [Restful API Design (Microsoft)](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)
- [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html)
