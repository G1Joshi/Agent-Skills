---
name: cloudflare
description: Expert Cloudflare assistance covering Workers, Pages, DNS records, CDN caching rules, and DDoS protection. Use when deploying edge applications, configuring DNS, and optimizing web performance.
---

# Cloudflare

Cloudflare provides global edge networking, DDoS protection, edge serverless compute (Workers), and S3-compatible zero-egress object storage (R2).

## When to Use

- **Global Edge Compute with Cloudflare Workers**: Executing serverless TypeScript/Rust code across 300+ global data centers with 0ms cold starts.
- **Edge Storage (KV, R2, D1, Vectorize)**: Distributed key-value, S3-compatible object storage, serverless SQL, and vector indexing.
- **DDoS Mitigation & Web Application Firewall (WAF)**: Protecting origins against layer 3/4/7 DDoS attacks and bots.
- **Zero Trust Network Access (ZTNA) & Tunnels**: Securely routing traffic to private services without opening public ports via `cloudflared`.

## Quick Start

```bash
# Initialize and deploy a Cloudflare Worker using Wrangler
npm create cloudflare@latest my-edge-app -- --type hello-world
cd my-edge-app
npx wrangler dev    # Run locally with edge simulation
npx wrangler deploy # Deploy globally to 300+ edge locations
```

## Core Concepts

### Modern Cloudflare Worker with Fetch Handler

Sub-millisecond edge API handling requests:

```typescript
// src/index.ts
export interface Env {
  CACHE_KV: KVNamespace;
  API_SECRET: string;
}

export default {
  async fetch(
    request: Request,
    env: Env,
    ctx: ExecutionContext,
  ): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/api/geoip") {
      const country = request.cf?.country || "Unknown";
      const city = request.cf?.city || "Unknown";

      return Response.json({
        ip: request.headers.get("cf-connecting-ip"),
        country,
        city,
        colo: request.cf?.colo, // Cloudflare data center airport code
      });
    }

    // Check edge KV cache
    const cacheKey = `content:${url.pathname}`;
    const cached = await env.CACHE_KV.get(cacheKey);
    if (cached) {
      return new Response(cached, {
        headers: { "X-Cache": "HIT", "Content-Type": "application/json" },
      });
    }

    const payload = JSON.stringify({
      message: "Generated at edge",
      timestamp: Date.now(),
    });
    ctx.waitUntil(env.CACHE_KV.put(cacheKey, payload, { expirationTtl: 300 }));

    return new Response(payload, {
      headers: { "X-Cache": "MISS", "Content-Type": "application/json" },
    });
  },
};
```

### Wrangler Configuration (wrangler.jsonc)

Declarative configuration of bindings and environments:

```json
{
  "name": "edge-gateway",
  "main": "src/index.ts",
  "compatibility_date": "2026-01-01",
  "compatibility_flags": ["nodejs_compat"],
  "kv_namespaces": [{ "binding": "CACHE_KV", "id": "f8a03c20..." }],
  "r2_buckets": [
    { "binding": "MEDIA_BUCKET", "bucket_name": "prod-media-assets" }
  ]
}
```

### Secure Origin Access with Cloudflare Tunnels (cloudflared)

Exposing internal services to the edge without opening firewall ports:

```yaml
# ~/.cloudflared/config.yml
tunnel: 6ff398a8-3f8d-4f10-9111-923485720193
credentials-file: /etc/cloudflared/cert.json

ingress:
  - hostname: internal-dash.company.com
    service: http://localhost:8080
  - service: http_status:404
```

## Common Patterns

### Cloudflare Worker with KV Cache and Geo-Routing

**Problem**: Querying origin servers repeatedly for static JSON metadata adds unnecessary latency.

**Solution**:
Cache responses at the edge with Cloudflare Workers KV:

```typescript
export default {
  async fetch(request, env, ctx): Promise<Response> {
    const url = new URL(request.url);
    const country = request.cf?.country || "US";

    const cached = await env.MY_KV.get(`content:${country}`);
    if (cached) {
      return new Response(cached, {
        headers: { "content-type": "application/json" },
      });
    }

    const data = JSON.stringify({ message: `Hello from ${country}` });
    ctx.waitUntil(
      env.MY_KV.put(`content:${country}`, data, { expirationTtl: 3600 }),
    );
    return new Response(data, {
      headers: { "content-type": "application/json" },
    });
  },
};
```

## Best Practices

**Do**:

- Target `compatibility_date` with `nodejs_compat` enabled to access standard Node.js APIs at the edge.
- Offload asynchronous non-blocking work (e.g. analytics logging) to `ctx.waitUntil()` to avoid blocking user response.
- Use Cloudflare R2 for asset storage to eliminate egress bandwidth fees.
- Deploy Cloudflare Tunnels to connect private backends without opening public ports.

**Don't**:

- Store large relational datasets in KV; use Cloudflare D1 (SQL) or Hyperdrive for PostgreSQL connection pooling.
- Perform CPU-bound tasks exceeding the Worker CPU time limit; offload heavy jobs to standard containers.
- Commit `wrangler.jsonc` files containing unencrypted secret values; use `wrangler secret put`.

## Troubleshooting

| Error                                      | Cause                                                                                | Solution                                                                |
| :----------------------------------------- | :----------------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `Error 521: Web server is down`            | Cloudflare edge cannot connect to origin server port 80/443.                         | Verify origin web server is running and firewall allows Cloudflare IPs. |
| `Error 525: SSL handshake failed`          | Origin server SSL certificate invalid or SSL mode set to Full (strict) without cert. | Switch to Full mode or install valid SSL certificate on origin server.  |
| `10015: Workers KV key size exceeds limit` | Key length exceeds 512 bytes.                                                        | Hash long keys with SHA-256 before querying Workers KV.                 |

## References

- [Cloudflare Developers](https://developers.cloudflare.com/)
