---
name: auth0
description: Auth0 identity platform. Use for authentication.
---

# Auth0

Auth0 is a platform for authentication and authorization. It provides a Universal Login page that handles the complexity of authentication protocols (SAML, OIDC, OAuth) and identity providers (Google, Enterprise, Database).

## When to Use

- **Enterprise Apps**: Application requiring intricate B2B Identity (SSO, SAML, AD).
- **Complex Rules**: When you need programmable pipelines (Actions) during login (e.g., "Add Role to ID Token if email ends in @corp.com").
- **Speed**: Wanting a login page working in 5 minutes.

## Quick Start (Next.js)

```bash
npm install @auth0/nextjs-auth0
```

```javascript
// page/api/auth/[...auth0].js
import { handleAuth } from '@auth0/nextjs-auth0';
export default handleAuth();

// Component
import { useUser } from '@auth0/nextjs-auth0/client';

export default function Profile() {
  const { user, error, isLoading } = useUser();
  if (isLoading) return <div>Loading...</div>;
  if (user) return <div>Welcome {user.name}</div>;
  return <a href="/api/auth/login">Login</a>;
}
```

## Core Concepts

### Universal Login

Redirects user to `your-tenant.auth0.com`. Secure, centralized, and hosted by Auth0. Avoids "Embedded Login" (inputs on your own page) for better security against credential stuffing.

### Actions (formerly Rules/Hooks)

Serverless functions that execute during the auth pipeline.

- _Post-Login_: Add claims, Call external API, Deny access.
- _Machine-to-Machine_: Enrich tokens.

## Best Practices (2025)

**Do**:

- Use **Universal Login**.
- Enable **Brute Force Protection** and **Breach Password Detection** (built-in).
- Use **Custom Domains** (`auth.myapp.com`) to avoid 3rd party cookie issues.

**Don't**:

- Don't use the Management API tokens in the frontend.
- Don't skip **MFA**. Enable Adaptive MFA for high-risk logins.

## Troubleshooting

| Error                   | Cause                          | Solution                                                                |
| :---------------------- | :----------------------------- | :---------------------------------------------------------------------- |
| `Callback URL mismatch` | Redirect URI not in dashboard. | Add `http://localhost:3000/api/auth/callback` to Allowed Callback URLs. |
| `CORS`                  | Calling API from SPA.          | Configure Allowed Origins and Web Origins.                              |

## References

- [Auth0 Documentation](https://auth0.com/docs)
- [Auth0 Next.js SDK](https://github.com/auth0/nextjs-auth0)
