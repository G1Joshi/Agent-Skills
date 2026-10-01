---
name: rest-api
description: Expert REST API architecture assistance covering HTTP semantics, OpenAPI/Swagger specifications, idempotent methods, hypermedia (HATEOAS), and pagination patterns. Use when designing web APIs, structuring resource endpoints, standardizing error formats, or implementing RESTful conventions.
---

# REST API

Representational State Transfer (REST) is the architectural style for distributed hypermedia systems. It relies on stateless, client-server, cacheable communications protocols (mostly HTTP).

## When to Use

- **Universal Public Web APIs**: Building open, standardized APIs intended for third-party developers, webhooks, and partner integrations.
- **HTTP Caching & CDN Optimization**: Maximizing cacheability using standard HTTP response headers (`Cache-Control`, `ETag`, `Last-Modified`).
- **Resource-Oriented CRUD Operations**: Designing intuitive resource hierarchies with standard HTTP semantics (GET, POST, PUT, PATCH, DELETE).
- **Stateless Integration**: Delivering scalable stateless APIs consumed effortlessly by any HTTP client on any platform.

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

### HTTP Semantics & Idempotency

Different HTTP verbs carry formal idempotency and safety guarantees:

| Method   | Safe | Idempotent | Usage                                 |
| :------- | :--- | :--------- | :------------------------------------ |
| `GET`    | Yes  | Yes        | Retrieve resource representation      |
| `POST`   | No   | No         | Create new resource or trigger action |
| `PUT`    | No   | Yes        | Replace resource entirely             |
| `PATCH`  | No   | No / Yes   | Partially update resource             |
| `DELETE` | No   | Yes        | Remove resource                       |

### Standardized Error Representations (RFC 7807 / 9457)

Returns machine-readable `application/problem+json` error responses:

```json
{
  "type": "https://api.example.com/errors/invalid-payment",
  "title": "Invalid Payment Source",
  "status": 422,
  "detail": "The payment card provided has expired.",
  "instance": "/orders/415/payments"
}
```

### Content Negotiation & ETag Caching

Validates whether cached client data is still fresh without resending full payloads:

```typescript
app.get("/api/v1/users/:id", async (req, res) => {
  const user = await db.getUser(req.params.id);
  const etag = crypto
    .createHash("md5")
    .update(JSON.stringify(user))
    .digest("hex");

  if (req.headers["if-none-match"] === etag) {
    return res.status(304).end(); // Not Modified
  }

  res.setHeader("ETag", etag);
  res.setHeader(
    "Cache-Control",
    "public, max-age=60, stale-while-revalidate=300",
  );
  res.json(user);
});
```

## Common Patterns

### Cursor-Based Pagination

**Problem**: Offset-based pagination (`OFFSET 10000`) degrades database performance and skips items on concurrent writes.  
**Solution**: Use monotonic cursor identifiers (e.g. `created_at` + `id`).

```typescript
// GET /api/v1/posts?cursor=2026-09-27T10:00:00Z&limit=20
app.get("/api/v1/posts", async (req, res) => {
  const { cursor, limit = 20 } = req.query;
  const posts = await db
    .select()
    .from(postsTable)
    .where(
      cursor ? lt(postsTable.createdAt, new Date(cursor as string)) : undefined,
    )
    .orderBy(desc(postsTable.createdAt))
    .limit(Number(limit) + 1);

  const hasMore = posts.length > Number(limit);
  const data = hasMore ? posts.slice(0, -1) : posts;
  const nextCursor = hasMore
    ? data[data.length - 1].createdAt.toISOString()
    : null;

  res.json({ data, pagination: { hasMore, nextCursor } });
});
```

## Best Practices

**Do**:

- Use Nouns for Resource URIs: Use `/api/v1/orders` rather than action verbs like `/api/v1/getOrders` or `/api/v1/createOrder`.
- Implement Idempotency Keys on Mutating Requests: Require `Idempotency-Key` headers on POST/PATCH requests to prevent duplicate charges.
- Document with OpenAPI 3.1: Generate automated Swagger docs, SDK clients, and request validation schemas from OpenAPI specs.
- Implement Monotonic Cursor Pagination: Use `limit` and `starting_after` cursor pagination for high-volume datasets.

**Don't**:

- Return HTTP 200 with `{ "error": "..." }`: Always return correct HTTP status codes (`400`, `401`, `403`, `404`, `422`, `500`).
- Break API contracts without versioning: Prefix endpoints with `/v1/` or use header versioning when introducing breaking changes.
- Expose raw internal database column names: Map private column names to clean, camelCased JSON fields.

## Troubleshooting

| Error                        | Cause                                  | Solution                                             |
| :--------------------------- | :------------------------------------- | :--------------------------------------------------- |
| `405 Method Not Allowed`     | Sending POST to a GET-only endpoint.   | Check HTTP verb.                                     |
| `415 Unsupported Media Type` | Sending XML when JSON expected.        | Set `Content-Type: application/json`.                |
| `CORS Error`                 | Browser blocking cross-origin request. | Set `Access-Control-Allow-Origin` headers on server. |

## References

- [Restful API Design (Microsoft)](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)
- [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html)
