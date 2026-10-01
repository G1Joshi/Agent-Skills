---
name: clerk
description: Expert Clerk authentication assistance covering Next.js middleware, React user components, webhooks, and session tokens. Use when integrating Clerk auth, protecting routes, or handling user management.
---

# Clerk

Clerk is a comprehensive user management and authentication service built specifically for the modern web (React, Next.js, Remix). It focuses on providing "Drop-in" UI components (`<SignIn />`, `<UserProfile />`) rather than just APIs.

## When to Use

- **Modern React & Next.js Authentication**: Adding drop-in, beautifully designed authentication components to modern frontend stacks.
- **B2B SaaS Multi-Tenancy & Organizations**: Managing team invites, role assignments, seat limits, and organization switching.
- **Passwordless & Passkey Auth**: Enabling WebAuthn passkeys, biometric logins, and magic links out of the box.
- **Edge-Ready Middleware Verification**: Validating JWT session tokens at the network edge (Cloudflare Workers, Next.js Middleware).

## Quick Start

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

### Drop-in Component Architecture (<SignIn />, <UserButton />)

Provides prebuilt, accessible, themed UI components that handle complete auth lifecycles:

```tsx
// app/layout.tsx
import {
  ClerkProvider,
  SignInButton,
  SignedIn,
  SignedOut,
  UserButton,
} from "@clerk/nextjs";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <header className="flex justify-between p-4 border-b">
            <h1>Enterprise SaaS</h1>
            <SignedOut>
              <SignInButton mode="modal" />
            </SignedOut>
            <SignedIn>
              <UserButton afterSignOutUrl="/" />
            </SignedIn>
          </header>
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
```

### Edge Middleware Session Protection

Protects routes and extracts authenticated user claims at the edge before rendering:

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isProtectedRoute = createRouteMatcher([
  "/dashboard(.*)",
  "/api/protected(.*)",
]);

export default clerkMiddleware((auth, req) => {
  if (isProtectedRoute(req)) {
    auth().protect();
  }
});

export const config = {
  matcher: ["/((?!.*\..*|_next).*)", "/", "/(api|trpc)(.*)"],
};
```

### Multi-Tenant Organizations & Role Checks

Manages multi-organization contexts with granular RBAC permissions:

```typescript
import { auth } from "@clerk/nextjs/server";

export async function POST() {
  const { orgId, orgRole } = auth();
  if (!orgId) throw new Error("Unauthorized: Select an organization");
  if (orgRole !== "org:admin")
    throw new Error("Forbidden: Admin privileges required");

  // Execute admin organization mutations
}
```

## Common Patterns

### Next.js App Router Route Protection with Clerk Middleware

**Problem**: Public API endpoints inadvertently exposed without explicit session verification.

**Solution**:
Enforce route matcher guards in Next.js `middleware.ts`:

```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isProtectedRoute = createRouteMatcher([
  "/dashboard(.*)",
  "/api/protected(.*)",
]);

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) await auth.protect();
});

export const config = {
  matcher: ["/((?!.*\\..*|_next).*)", "/", "/(api|trpc)(.*)"],
};
```

## Best Practices

**Do**:

- Verify Webhook Signatures with Svix: Always verify incoming Clerk user lifecycle webhooks using `svix` before updating local databases.
- Use Server-Side `auth()` in App Router: Extract `userId` and `orgId` via `auth()` in Server Components to eliminate client-side waterfall fetches.
- Theme Components with Tailored CSS: Match application design systems using Clerk's `appearance` prop and Tailwind utility variables.
- Enable Passkeys by Default: Encourage users to register biometric passkeys to eliminate credential phishing risks.

**Don't**:

- Expose `CLERK_SECRET_KEY` in frontend code: Keep secret keys strictly in server environment variables.
- Store database IDs in client state: Treat Clerk's JWT session claims as the single source of truth for the active request.
- Bypass route protection: Always enforce server-side protection in route handlers and middleware; do not rely on UI hiding alone.

## Troubleshooting

| Error              | Cause                      | Solution                                                  |
| :----------------- | :------------------------- | :-------------------------------------------------------- |
| `401 Unauthorized` | Middleware not configured. | Ensure `middleware.ts` matches all routes (`/((?!...))`). |
| `Hydration Error`  | HTML mismatch.             | Wrap app in `<ClerkProvider>`.                            |

## References

- [Clerk Documentation](https://clerk.com/docs)
- [Clerk vs Auth0](https://clerk.com/vs/auth0)
