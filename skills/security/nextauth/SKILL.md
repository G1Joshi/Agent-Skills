---
name: nextauth
description: NextAuth.js (Auth.js) for Next.js authentication. Use for Next.js auth.
---

# NextAuth.js (Auth.js)

Authentication for Next.js applications.

## When to Use

- Next.js applications
- OAuth provider integration
- Session-based auth
- Database-backed sessions

## Quick Start

```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    GitHub({
      clientId: process.env.GITHUB_ID!,
      clientSecret: process.env.GITHUB_SECRET!,
    }),
  ],
});

export const { GET, POST } = handlers;
```

## Core Concepts

### Session Access

```typescript
// Server Component
import { auth } from '@/auth';

export default async function Page() {
  const session = await auth();
  if (!session) redirect('/api/auth/signin');
  return <h1>Hello {session.user?.name}</h1>;
}

// Client Component
'use client';
import { useSession } from 'next-auth/react';

export function Profile() {
  const { data: session, status } = useSession();
  if (status === 'loading') return <p>Loading...</p>;
  return <p>{session?.user?.name}</p>;
}
```

### Middleware

```typescript
// middleware.ts
export { auth as middleware } from "@/auth";

export const config = {
  matcher: ["/dashboard/:path*"],
};
```

## Best Practices

**Do**: Use middleware for protection, extend session with callbacks
**Don't**: Expose sensitive data in session

## References

- [Auth.js Documentation](https://authjs.dev/)
