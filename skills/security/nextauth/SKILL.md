---
name: nextauth
description: NextAuth.js authentication for Next.js. Use for Next.js auth.
---

# NextAuth.js (Auth.js)

NextAuth (evolving into **Auth.js**) is a complete open-source authentication solution. It is designed to work with any OAuth service, supports email/passwordless, and owns your data (Database Adapters).

## When to Use

- **Data Ownership**: You want to own the User/Session data in your own Database (Postgres, Prisma) rather than an external provider.
- **Cost**: It's free/open-source. No MAU limits.
- **Flexibility**: You need custom providers or complex session strategies.

## Quick Start (Next.js App Router - v5 Beta)

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

### Database Adapters

NextAuth can persist users and sessions to your DB using adapters (Prisma, Drizzle, MongoDB).

### Strategies

- **JWT (Stateless)**: Default. Session data stored in an encrypted cookie. Good for scale.
- **Database (Stateful)**: Session stored in DB. Good if you need to revoke sessions server-side immediately.

## Best Practices (2025)

**Do**:

- Use the **Prisma Adapter** (or Drizzle) if you have a database.
- Set a strong `AUTH_SECRET` (auto-generated in Vercel, manual elsewhere).
- Use **Middleware** to protect routes at the edge.

**Don't**:

- Don't store large objects in the Session (The JWT cookie has a 4kb limit).
- Don't commit provider secrets (Client ID/Secret) to Git.

## Troubleshooting

| Error                 | Cause                     | Solution                                                 |
| :-------------------- | :------------------------ | :------------------------------------------------------- |
| `JWEDecryptionFailed` | Wrong `AUTH_SECRET`.      | Ensure `AUTH_SECRET` is set and consistent.              |
| `OAuthCallbackError`  | Provider config mismatch. | Check Authorised Redirect URIs in GitHub/Google console. |

## References

- [Auth.js Documentation](https://authjs.dev/)
- [NextAuth v4 vs v5](https://authjs.dev/guides/upgrade-to-v5)
