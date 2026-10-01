---
name: nextauth
description: Expert NextAuth.js / Auth.js assistance covering OAuth providers, credentials auth, database adapters, and session callbacks. Use when implementing authentication in Next.js, securing pages, or managing user sessions.
---

# NextAuth.js (Auth.js)

NextAuth (evolving into **Auth.js**) is a complete open-source authentication solution. It is designed to work with any OAuth service, supports email/passwordless, and owns your data (Database Adapters).

## When to Use

- **Next.js Full-Stack Authentication**: The standard, official authentication solution (Auth.js) for Next.js App Router and Pages Router.
- **Universal Provider Integrations**: Supporting GitHub, Google, Apple, and corporate OIDC/SAML providers in minutes.
- **Database Session Storage with Adapters**: Syncing user profiles and accounts to PostgreSQL, MySQL, or MongoDB via Prisma, Drizzle, or TypeORM.
- **Lightweight JWT Cookie Sessions**: Running serverless, zero-database session verification entirely through encrypted cookies.

## Quick Start

```typescript
// auth.ts
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [GitHub],
});

// app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/auth";
export const { GET, POST } = handlers;
```

## Core Concepts

### Auth.js Configuration Structure (v5)

Unified server configuration declared in `auth.ts`:

```typescript
// auth.ts (NextAuth v5 / Auth.js)
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";
import { DrizzleAdapter } from "@auth/drizzle-adapter";
import { db } from "@/db";

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: DrizzleAdapter(db),
  providers: [GitHub, Google],
  session: { strategy: "jwt" },
  callbacks: {
    jwt({ token, user }) {
      if (user) token.role = user.role;
      return token;
    },
    session({ session, token }) {
      session.user.role = token.role as string;
      return session;
    },
  },
});
```

### Route Handler Integration (App Router)

Exports GET and POST handlers directly in the catch-all API route:

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/auth";
export const { GET, POST } = handlers;
```

### Server Component Authentication (`auth()`)

Inspects user session directly inside Server Components without client-side hooks:

```tsx
// app/dashboard/page.tsx
import { auth } from "@/auth";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth();
  if (!session?.user) redirect("/api/auth/signin");

  return (
    <div>
      Welcome back, {session.user.name}! (Role: {session.user.role})
    </div>
  );
}
```

## Common Patterns

### Session Enrichment via JWT Callbacks

**Problem**: The frontend session object misses custom user fields like roles or database IDs.

**Solution**:
Populate custom claims in `jwt` and forward them to the `session` callback:

```typescript
export const authOptions: NextAuthOptions = {
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role;
        token.userId = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.role = token.role as string;
        session.user.id = token.userId as string;
      }
      return session;
    },
  },
};
```

## Best Practices

**Do**:

- Adopt Auth.js v5: Migrate from legacy v4 `getServerSession` to modern unified `auth()` methods in Next.js 14/15.
- Set a Cryptographically Secure `AUTH_SECRET`: Generate using `openssl rand -base64 33` and store in `.env.local`.
- Enforce Edge Middleware Route Protection: Protect private routes in `middleware.ts` before requests reach Server Components.
- Use TypeScript Module Augmentation: Extend `next-auth` types to ensure custom session fields (`role`, `id`) are strongly typed.

**Don't**:

- Fetch session data using client hooks in Server Components: Use server-side `await auth()` to avoid client waterfall delays.
- Store sensitive database credentials in session callbacks: The session object is transmitted to client browsers; keep it lightweight.
- Forget to configure production trust host: Set `AUTH_TRUST_HOST=true` when hosting on Docker, Kubernetes, or AWS behind reverse proxies.

## Troubleshooting

| Error                 | Cause                     | Solution                                                 |
| :-------------------- | :------------------------ | :------------------------------------------------------- |
| `JWEDecryptionFailed` | Wrong `AUTH_SECRET`.      | Ensure `AUTH_SECRET` is set and consistent.              |
| `OAuthCallbackError`  | Provider config mismatch. | Check Authorised Redirect URIs in GitHub/Google console. |

## References

- [Auth.js Documentation](https://authjs.dev/)
- [NextAuth v4 vs v5](https://authjs.dev/guides/upgrade-to-v5)
