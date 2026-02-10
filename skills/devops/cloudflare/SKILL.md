---
name: cloudflare
description: Cloudflare CDN, Workers, and edge services. Use for CDN and edge.
---

# Cloudflare

Cloudflare is more than a CDN; it is a global super-cloud. In 2025, **Workers AI** (Edge GPU inference) and **R2** (Egress-free storage) are compelling reasons to build here.

## When to Use

- **Edge Compute**: Cloudflare Workers start in <5ms globally. Perfect for APIs and Middleware.
- **Storage**: R2 is S3-compatible but has **zero egress fees**. Massive cost savings for data-heavy apps.
- **Security**: Zero Trust (Access) replaces corporate VPNs.

## Core Concepts

### Workers

V8 Isolate-based serverless functions. No cold starts. Write code in TS/JS/Rust/Python.

### Durable Objects

Stateful storage at the edge. Allows coordination (e.g., waiting lists, chat rooms) globally without a central DB.

### Workers AI

Run open-source models (Llama 3, Whisper) on Cloudflare's network of GPUs with a simple API call.

## Best Practices (2025)

**Do**:

- **Use Wrangler**: The CLI is fantastic for local dev and deploy (`npx wrangler dev`).
- **Use R2**: Move high-bandwidth assets from AWS S3 to R2 to kill egress bills.
- **Use Pages**: For hosting static sites + functions (full stack JAMstack).

**Don't**:

- **Don't block good bots**: Configure WAF carefully. Use "Managed Rulesets" rather than writing brittle regex rules securely.

## References

- [Cloudflare Developers](https://developers.cloudflare.com/)
