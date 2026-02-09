---
name: keycloak
description: Keycloak open-source identity and access management. Use for enterprise SSO.
---

# Keycloak

Open-source IAM for enterprise authentication.

## When to Use

- Enterprise SSO
- SAML/OIDC integration
- Self-hosted identity
- Multi-tenant applications

## Quick Start

```typescript
import Keycloak from "keycloak-js";

const keycloak = new Keycloak({
  url: "https://keycloak.example.com",
  realm: "my-realm",
  clientId: "my-app",
});

await keycloak.init({ onLoad: "login-required" });
console.log("Authenticated:", keycloak.authenticated);
```

## Core Concepts

### Token Management

```typescript
// Get access token
const token = keycloak.token;

// Refresh token
await keycloak.updateToken(30); // Refresh if expires in 30s

// API call with token
fetch("/api/data", {
  headers: { Authorization: `Bearer ${token}` },
});
```

### Protected Routes

```typescript
// Express middleware
function keycloakProtect(req, res, next) {
  const token = req.headers.authorization?.split(" ")[1];
  if (!token) return res.status(401).send("Unauthorized");
  // Verify with Keycloak
  next();
}
```

## Best Practices

**Do**: Use refresh token rotation, configure proper CORS
**Don't**: Store tokens insecurely, skip token validation

## References

- [Keycloak Documentation](https://www.keycloak.org/documentation)
