---
name: clerk
description: Clerk authentication for modern apps. Use for user management.
---

# Clerk

Clerk is a comprehensive user management and authentication service built specifically for the modern web (React, Next.js, Remix). It focuses on providing "Drop-in" UI components (`<SignIn />`, `<UserProfile />`) rather than just APIs.

## When to Use

- **Next.js / React Apps**: Best-in-class integration with App Router and Server Components.
- **SaaS B2B/B2C**: Built-in Organization (Multi-tenancy) management.
- **Speed**: You want the User Profile, Avatar upload, and Email management UI done for you.

## Quick Start (Next.js App Router)

```typescript
// middleware.ts
import { authMiddleware } from "@clerk/nextjs";
export default authMiddleware({});

// layout.tsx
import { ClerkProvider } from '@clerk/nextjs'
export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html><body>{children}</body></html>
    </ClerkProvider>
  )
}

// page.tsx (Protected)
import { UserButton, currentUser } from "@clerk/nextjs";
export default async function Page() {
  const user = await currentUser();
  if (!user) return <div>Not signed in</div>;
  return <header>Welcome {user.firstName} <UserButton /></header>;
}
```

## Core Concepts

### Pre-built Components

Clerk provides the full UI: Login, Register, Forgot Password, Managed MFA, User Profile (Change Password, 2FA, Sessions).

### Sessions vs Tokens

Clerk handles the complexity of short-lived JWTs (`__session` cookie) and keeps them fresh automatically via frontend SDKs.

## Best Practices (2025)

**Do**:

- Use **Server Components** (`currentUser()`) to fetch user data on the backend.
- Use **Organizations** feature for B2B SaaS apps (Tenant isolation).
- Enable **Passkeys** (Passwordless) in the dashboard (Clerk supports this natively).

**Don't**:

- Don't try to build custom UI unless necessary. The pre-built components handle edge cases (MFA, Captcha, Error states) perfectly.
- Don't expose Secret Keys in client-side env vars.

## Troubleshooting

| Error              | Cause                      | Solution                                                  |
| :----------------- | :------------------------- | :-------------------------------------------------------- |
| `401 Unauthorized` | Middleware not configured. | Ensure `middleware.ts` matches all routes (`/((?!...))`). |
| `Hydration Error`  | HTML mismatch.             | Wrap app in `<ClerkProvider>`.                            |

## References

- [Clerk Documentation](https://clerk.com/docs)
- [Clerk vs Auth0](https://clerk.com/vs/auth0)
