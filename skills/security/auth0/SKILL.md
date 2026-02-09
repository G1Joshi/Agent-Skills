---
name: auth0
description: Auth0 identity platform for authentication and authorization. Use for managed auth.
---

# Auth0

Identity platform for authentication and authorization.

## When to Use

- Managed authentication
- Social login integration
- Enterprise SSO
- Multi-factor authentication

## Quick Start

```typescript
import { Auth0Client } from "@auth0/auth0-spa-js";

const auth0 = new Auth0Client({
  domain: "your-tenant.auth0.com",
  clientId: "your-client-id",
  authorizationParams: {
    redirect_uri: window.location.origin,
  },
});

await auth0.loginWithRedirect();
```

## Core Concepts

### React Integration

```tsx
import { Auth0Provider, useAuth0 } from "@auth0/auth0-react";

function App() {
  return (
    <Auth0Provider
      domain="your-tenant.auth0.com"
      clientId="your-client-id"
      authorizationParams={{
        redirect_uri: window.location.origin,
        audience: "https://api.example.com",
      }}
    >
      <MainApp />
    </Auth0Provider>
  );
}

function Profile() {
  const { user, isAuthenticated, loginWithRedirect, logout } = useAuth0();

  if (!isAuthenticated) {
    return <button onClick={loginWithRedirect}>Log In</button>;
  }

  return (
    <div>
      <img src={user?.picture} alt={user?.name} />
      <p>{user?.name}</p>
      <button onClick={() => logout()}>Log Out</button>
    </div>
  );
}
```

### API Protection

```typescript
import { auth } from "express-oauth2-jwt-bearer";

const checkJwt = auth({
  audience: "https://api.example.com",
  issuerBaseURL: "https://your-tenant.auth0.com/",
});

app.get("/api/protected", checkJwt, (req, res) => {
  res.json({ message: "Protected data", user: req.auth?.payload });
});
```

## Common Patterns

### Get Access Token

```typescript
const { getAccessTokenSilently } = useAuth0();

async function callApi() {
  const token = await getAccessTokenSilently({
    authorizationParams: {
      audience: "https://api.example.com",
    },
  });

  const response = await fetch("/api/data", {
    headers: { Authorization: `Bearer ${token}` },
  });

  return response.json();
}
```

### Role-Based Access

```typescript
// Check user roles from ID token
const { user } = useAuth0();
const roles = user?.["https://example.com/roles"] as string[];

if (roles?.includes("admin")) {
  // Show admin features
}
```

## Best Practices

**Do**:

- Use refresh token rotation
- Configure MFA
- Set up rules for custom claims
- Use correct audience for APIs

**Don't**:

- Store tokens in localStorage
- Skip token validation
- Use implicit flow
- Ignore session management

## Troubleshooting

| Issue         | Cause              | Solution               |
| ------------- | ------------------ | ---------------------- |
| Login loop    | Callback URL       | Check allowed URLs     |
| Token expired | Silent auth failed | Use refresh tokens     |
| CORS error    | Wrong origin       | Add to allowed origins |

## References

- [Auth0 Documentation](https://auth0.com/docs)
- [Auth0 React SDK](https://auth0.com/docs/libraries/auth0-react)
