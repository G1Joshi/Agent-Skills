---
name: vercel
description: Expert Vercel platform assistance covering Next.js deployment, Edge Middleware, Serverless Functions, Turborepo, and analytics. Use when deploying frontend frameworks and serverless backends globally.
---

# Vercel

Vercel is a frontend cloud platform providing automated CI/CD deployments, edge middleware, global content distribution, and serverless compute tailored for modern web frameworks.

## When to Use

- **Production Next.js & Frontend Deployment**: First-party platform optimized for Next.js, React, SvelteKit, and Nuxt.
- **Vercel Edge Functions & Middleware**: Sub-millisecond routing, A/B testing, and authentication at the global edge.
- **Instant Preview Deployments**: Automated unique URLs for every pull request branch with visual feedback and commenting.
- **Serverless Compute with Fluid Compute**: Scaling serverless execution transparently without cold start delays.

## Quick Start

```bash
npm i -g vercel

# Deploy (Preview)
vercel

# Deploy (Production)
vercel --prod
```

## Core Concepts

### Edge Middleware Configuration (middleware.ts)

Executing routing and authentication checks at the network edge:

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("auth_token")?.value;

  // Protect dashboard routes
  if (request.nextUrl.pathname.startsWith("/dashboard") && !token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("from", request.nextUrl.pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Geolocation header injection
  const response = NextResponse.next();
  const country = request.geo?.country || "US";
  response.headers.set("x-user-country", country);

  return response;
}

export const config = {
  matcher: ["/dashboard/:path*", "/api/secure/:path*"],
};
```

### Declarative Vercel Configuration (vercel.json)

Configuring custom headers, rewrites, and function memory:

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "cleanUrls": true,
  "trailingSlash": false,
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ],
  "functions": {
    "api/export-pdf.ts": {
      "memory": 1024,
      "maxDuration": 30
    }
  }
}
```

### Vercel CLI Deployment Operations

Deploying and pulling remote environments:

```bash
# Link local repository to Vercel project
vercel link

# Pull production environment variables to local .env
vercel env pull .env.local

# Deploy preview build to Vercel edge network
vercel

# Deploy to production domain
vercel --prod
```

## Common Patterns

### Geolocation Edge Middleware with Custom Rewrites

**Problem**: Personalizing content by visitor country without server-side rendering latency.

**Solution**:
Use Vercel Edge Middleware with geolocation:

```typescript
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const country = request.geo?.country || "US";

  if (country === "GB") {
    return NextResponse.rewrite(new URL("/uk", request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/"],
};
```

## Best Practices

**Do**:

- Leverage Vercel's native Next.js 15 App Router optimizations (RSC, Server Actions, streaming).
- Pull environment variables securely using `vercel env pull` rather than manually copying secrets.
- Use Edge Middleware for lightweight tasks (redirects, header injection); offload heavy computation to Serverless Functions.
- Configure `maxDuration` in `vercel.json` if background operations require more than default serverless timeout.

**Don't**:

- Perform long-running background tasks inside Vercel Edge Middleware; it has strict CPU runtime limits.
- Commit `.vercel` or `.env.local` directories to source control.
- Bypass Vercel deployment preview gates for production merges.

## Troubleshooting

| Error                           | Cause                                                                                 | Solution                                                                                  |
| :------------------------------ | :------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------- |
| `FUNCTION_INVOCATION_TIMEOUT`   | Serverless Function execution exceeded plan duration limit (15s hobby, 60s pro).      | Optimize slow external queries or split into background task.                             |
| `Build Cache Miss on Turborepo` | Environment variables changing between builds without being declared in `turbo.json`. | Add cache-invalidating env vars to `globalEnv` in `turbo.json`.                           |
| `404 Not Found on static asset` | Asset path missing leading slash or output directory misconfigured.                   | Verify `outputDirectory` setting matches framework build output (e.g. `dist` or `.next`). |

## References

- [Vercel Documentation](https://vercel.com/docs)
