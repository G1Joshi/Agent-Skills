---
name: cloudflare
description: Cloudflare CDN, Workers, Pages, and security features. Use for edge computing and CDN.
---

# Cloudflare

Edge computing platform with CDN, Workers, and security.

## When to Use

- CDN and caching
- Edge computing (Workers)
- Static site hosting (Pages)
- DDoS protection and WAF

## Quick Start

```typescript
// Cloudflare Worker
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/api/hello") {
      return Response.json({ message: "Hello from the edge!" });
    }

    return new Response("Not found", { status: 404 });
  },
};
```

## Core Concepts

### Workers with KV

```typescript
export interface Env {
  MY_KV: KVNamespace;
  MY_DO: DurableObjectNamespace;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    // Read from KV
    const cached = await env.MY_KV.get("key", "json");
    if (cached) return Response.json(cached);

    // Fetch and cache
    const data = await fetchData();
    await env.MY_KV.put("key", JSON.stringify(data), {
      expirationTtl: 3600,
    });

    return Response.json(data);
  },
};
```

### Durable Objects

```typescript
export class Counter implements DurableObject {
  state: DurableObjectState;

  constructor(state: DurableObjectState) {
    this.state = state;
  }

  async fetch(request: Request): Promise<Response> {
    let count = (await this.state.storage.get<number>("count")) || 0;

    if (request.method === "POST") {
      count++;
      await this.state.storage.put("count", count);
    }

    return Response.json({ count });
  }
}
```

## Common Patterns

### Pages Deployment

```yaml
# wrangler.toml
name = "my-app"
compatibility_date = "2024-01-01"

[site]
bucket = "./dist"

[[kv_namespaces]]
binding = "CACHE"
id = "abc123"
```

```bash
# Deploy
npx wrangler deploy

# Pages
npx wrangler pages deploy dist
```

## Best Practices

**Do**:

- Use KV for caching
- Implement proper error handling
- Use Durable Objects for state
- Configure proper cache headers

**Don't**:

- Block the event loop
- Make too many subrequests
- Store large data in KV values
- Ignore execution time limits

## Troubleshooting

| Issue             | Cause                | Solution                   |
| ----------------- | -------------------- | -------------------------- |
| CPU time exceeded | Long computation     | Optimize or use DO         |
| KV stale          | Eventual consistency | Use metadata for freshness |
| CORS error        | Missing headers      | Add CORS headers           |

## References

- [Cloudflare Workers Docs](https://developers.cloudflare.com/workers/)
- [Cloudflare Pages](https://pages.cloudflare.com/)
