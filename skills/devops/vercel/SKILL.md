---
name: vercel
description: Vercel frontend deployment with edge functions. Use for frontend hosting.
---

# Vercel

Vercel is the platform for the frontend cloud. In 2025, it has expanded beyond hosting to become a full AI and Storage platform (Vercel Blob/Postgres).

## When to Use

- **Next.js**: The best place to deploy Next.js apps.
- **Frontend-First**: Deploys from Git, automatic preview URLs for every PR.
- **AI Apps**: Native integration with Vercel AI SDK for streaming LLM responses.

## Quick Start (CLI)

```bash
npm i -g vercel

# Deploy (Preview)
vercel

# Deploy (Production)
vercel --prod
```

## Core Concepts

### Infrastructure as Code (Implicit)

`vercel.json` or framework defaults. Minimal config required.

### Serverless & Edge Functions

API routes in `app/api` are deployed as Serverless (Node.js) or Edge (WinterCG) functions automatically.

### Storage

Vercel now provides:

- **KV**: Redis (Upstash)
- **Postgres**: SQL (Neon)
- **Blob**: Object Storage (R2)

## Best Practices (2025)

**Do**:

- **Use Comments for Preview**: Vercel Toolbar allows stakeholders to comment directly on the Preview UI.
- **Use Vercel Postgres**: For new side projects, the tight integration is unbeatable.
- **Use `vercel env pull`**: Sync production env vars to local `.env`.

**Don't**:

- **Don't ignore region**: Ensure your Database and Function regions match (e.g., both `iad1`), otherwise latency kills performance.

## References

- [Vercel Documentation](https://vercel.com/docs)
