---
name: vercel
description: Vercel deployment platform for Next.js and frontend with serverless functions. Use for frontend hosting.
---

# Vercel

Frontend deployment platform optimized for Next.js and serverless.

## When to Use

- Next.js deployments
- Static site hosting
- Serverless functions
- Edge functions

## Quick Start

```json
// vercel.json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "env": {
    "DATABASE_URL": "@database-url"
  }
}
```

## Core Concepts

### Serverless Functions

```typescript
// api/users/[id].ts
import type { VercelRequest, VercelResponse } from "@vercel/node";

export default async function handler(req: VercelRequest, res: VercelResponse) {
  const { id } = req.query;

  if (req.method === "GET") {
    const user = await db.users.findUnique({ where: { id: String(id) } });
    return res.json(user);
  }

  res.status(405).json({ error: "Method not allowed" });
}
```

### Edge Functions

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export const config = {
  matcher: "/api/:path*",
};

export function middleware(request: NextRequest) {
  const authHeader = request.headers.get("authorization");

  if (!authHeader) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  return NextResponse.next();
}
```

## Common Patterns

### Environment Variables

```bash
# Link project
vercel link

# Add secret
vercel env add DATABASE_URL production

# Pull env locally
vercel env pull .env.local
```

### Preview Deployments

```yaml
# vercel.json
{
  "git": { "deploymentEnabled": { "main": true, "feature/*": true } },
  "redirects": [{ "source": "/old", "destination": "/new" }],
  "headers":
    [
      {
        "source": "/api/(.*)",
        "headers": [{ "key": "Cache-Control", "value": "no-store" }],
      },
    ],
}
```

## Best Practices

**Do**:

- Use Edge Functions for low-latency
- Configure proper caching headers
- Use preview deployments for PRs
- Set up environment per branch

**Don't**:

- Expose secrets in client bundles
- Skip function timeout configuration
- Ignore build output size
- Deploy without preview testing

## Troubleshooting

| Issue            | Cause            | Solution                           |
| ---------------- | ---------------- | ---------------------------------- |
| Build failed     | Missing env      | Check env variables                |
| Function timeout | Slow execution   | Optimize or increase limit         |
| Large bundle     | Unoptimized code | Analyze with @next/bundle-analyzer |

## References

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js on Vercel](https://vercel.com/docs/frameworks/nextjs)
