---
name: auth0
description: Expert Auth0 authentication assistance covering OAuth2, OpenID Connect, JWT validation, and RBAC. Use when integrating Auth0 into web/mobile apps, configuring Universal Login, or securing APIs.
---

# Auth0

Auth0 is a platform for authentication and authorization. It provides a Universal Login page that handles the complexity of authentication protocols (SAML, OIDC, OAuth) and identity providers (Google, Enterprise, Database).

## When to Use

- **Enterprise Universal Login**: Outsourcing authentication, MFA, and social/enterprise federated logins to managed Auth0 infrastructure.
- **B2B Multi-Tenant Identity**: Managing distinct organizational customer portals with custom domains, SAML/WS-Fed, and SCIM provisioning.
- **Fine-Grained Role-Based Access Control**: Defining custom roles, permissions, and claims enforced across APIs and frontends.
- **Machine-to-Machine (M2M) Authorization**: Securing daemon background services using OAuth 2.0 Client Credentials grants.

## Quick Start

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

#Auth0 Universal Login & OIDC Handshake

Clients redirect to centralized Auth0 login pages, preventing direct credential exposure to frontend applications:

```typescript
// Next.js App Router Auth0 SDK (v3)
import { handleAuth, handleLogin } from "@auth0/nextjs-auth0";

export const GET = handleAuth({
  login: handleLogin({
    authorizationParams: {
      audience: "https://api.myenterprise.com",
      scope: "openid profile email read:reports",
    },
    returnTo: "/dashboard",
  }),
});
```

#Auth0 Actions (Extensibility Pipeline)

Node.js event handlers executed during the authentication pipeline to enrich claims, enforce MFA, or check blocklists:

```javascript
// Auth0 Post-Login Action
exports.onExecutePostLogin = async (event, api) => {
  const namespace = "https://myenterprise.com/claims";
  // Add custom roles to the ID and Access Tokens
  if (event.authorization?.roles) {
    api.idToken.setCustomClaim(`${namespace}/roles`, event.authorization.roles);
    api.accessToken.setCustomClaim(
      `${namespace}/roles`,
      event.authorization.roles,
    );
  }

  // Conditionally trigger MFA for external networks
  if (!event.request.ip.startsWith("10.0.")) {
    api.multifactor.enable("any");
  }
};
```

#Machine-to-Machine JWT Verification in Backend APIs

Validates JWT access tokens against the Auth0 JWKS endpoint:

```typescript
import { expressjwt as jwt } from "express-jwt";
import jwksRsa from "jwks-rsa";

export const checkJwt = jwt({
  secret: jwksRsa.expressJwtSecret({
    cache: true,
    rateLimit: true,
    jwksRequestsPerMinute: 5,
    jwksUri: `https://my-tenant.us.auth0.com/.well-known/jwks.json`,
  }),
  audience: "https://api.myenterprise.com",
  issuer: `https://my-tenant.us.auth0.com/`,
  algorithms: ["RS256"],
});
```

## Common Patterns

### Express JWT Verification Middleware

**Problem**: Securing backend API routes against unauthorized or tampered Auth0 access tokens.

**Solution**:
Use `express-oauth2-jwt-bearer` with audience and issuer verification:

```javascript
import { auth } from "express-oauth2-jwt-bearer";

export const checkJwt = auth({
  audience: "https://api.mycompany.com",
  issuerBaseURL: "https://mytenant.us.auth0.com/",
  tokenSigningAlg: "RS256",
});

// Protect routes
app.get("/api/private", checkJwt, (req, res) => {
  res.json({
    message: "Protected endpoint access granted",
    user: req.auth.payload,
  });
});
```

## Best Practices (2026)

**Do**:

- **Always Verify the `audience` and `issuer` Claims**: Never validate token signatures without verifying that the audience matches your specific API identifier.
- **Use Auth0 Actions instead of Legacy Rules/Hooks**: Actions provide modern TypeScript runtimes, secret management, and version history.
- **Rotate Signing Secrets Regularly**: Use RS256 asymmetric keys with automated JWKS rotation rather than static HS256 shared secrets.
- **Enable Anomaly Detection**: Turn on brute-force protection, credential stuffing guards, and breached password detection in the Auth0 console.

**Don't**:

- **Don't store sensitive user data in client-side localStorage**: Store tokens in secure HttpOnly cookies or use the Auth0 refresh token rotation flow.
- **Don't hardcode client secrets in frontend or mobile apps**: Use the Authorization Code Flow with PKCE for single-page and mobile apps.
- **Don't use Auth0 Management API tokens in client code**: Keep Management API tokens strictly within secure backend servers.

## Troubleshooting

| Error                   | Cause                          | Solution                                                                |
| :---------------------- | :----------------------------- | :---------------------------------------------------------------------- |
| `Callback URL mismatch` | Redirect URI not in dashboard. | Add `http://localhost:3000/api/auth/callback` to Allowed Callback URLs. |
| `CORS`                  | Calling API from SPA.          | Configure Allowed Origins and Web Origins.                              |

## References

- [Auth0 Documentation](https://auth0.com/docs)
- [Auth0 Next.js SDK](https://github.com/auth0/nextjs-auth0)
