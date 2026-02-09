---
name: clerk
description: Clerk authentication with React components and session management. Use for modern auth.
---

# Clerk

Drop-in authentication for React and Next.js.

## When to Use

- Next.js applications
- React SPA authentication
- Social login integration
- User management UI

## Quick Start

```tsx
// app/layout.tsx
import { ClerkProvider } from "@clerk/nextjs";

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html>
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}

// Protected page
import { auth } from "@clerk/nextjs/server";

export default async function Dashboard() {
  const { userId } = await auth();
  if (!userId) redirect("/sign-in");
  return <h1>Dashboard</h1>;
}
```

## Core Concepts

### Components

```tsx
import {
  SignInButton,
  SignOutButton,
  SignedIn,
  SignedOut,
  UserButton,
} from "@clerk/nextjs";

function Header() {
  return (
    <header>
      <SignedOut>
        <SignInButton />
      </SignedOut>
      <SignedIn>
        <UserButton />
      </SignedIn>
    </header>
  );
}
```

### Middleware

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isProtectedRoute = createRouteMatcher(["/dashboard(.*)"]);

export default clerkMiddleware((auth, req) => {
  if (isProtectedRoute(req)) auth().protect();
});
```

## Best Practices

**Do**: Use middleware for protection, leverage built-in components
**Don't**: Store sensitive data in user metadata

## References

- [Clerk Documentation](https://clerk.com/docs)
