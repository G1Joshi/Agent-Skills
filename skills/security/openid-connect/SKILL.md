---
name: openid-connect
description: Expert OpenID Connect (OIDC) assistance covering ID tokens, UserInfo endpoints, discovery documents, and claims. Use when implementing single sign-on (SSO), verifying ID tokens, or configuring OIDC providers.
---

# OpenID Connect (OIDC)

OIDC extends OAuth 2.0 to provide **Identity**. While OAuth handles "Access" (Authorization), OIDC handles "Who are you?" (Authentication).

## When to Use

- **User Authentication Layer on OAuth 2.0**: Verifying user identity through standardized ID tokens alongside OAuth authorization.
- **Federated Social & Corporate Logins**: Enabling "Sign in with Google, Apple, Microsoft, GitHub" across web and mobile applications.
- **Decentralized User Profile Ingestion**: Fetching standard profile attributes (email, name, picture) via the `/userinfo` endpoint.
- **Identity Provider Interoperability**: Ensuring client libraries communicate with any OIDC-compliant identity provider seamlessly.

## Quick Start

```http
// Request
GET /authorize?
  response_type=code&
  scope=openid profile email&  <-- 'openid' scope triggers OIDC
  client_id=...&
  redirect_uri=...

// Token Response
{
  "access_token": "SlAV32hkKG...", // For API access
  "id_token": "eyJ0eXKiOiJK...",   // JWT containing User Profile
  "expires_in": 3600
}
```

## Core Concepts

### The OIDC Layer on OAuth 2.0

OIDC adds an identity layer on top of OAuth 2.0 by introducing the cryptographic ID Token and UserInfo endpoint:

```text
[ OAuth 2.0 (Authorization) ] ──+ OpenID Scope ──→ [ OpenID Connect (Authentication) ]
                                                     ├── ID Token (JWT with user claims)
                                                     ├── Discovery Endpoint (/.well-known/openid-configuration)
                                                     └── UserInfo Endpoint (/userinfo)
```

### The OIDC Discovery Document (`/.well-known/openid-configuration`)

Allows clients to discover authorization, token, JWKS, and userinfo endpoints dynamically:

```json
{
  "issuer": "https://accounts.google.com",
  "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
  "token_endpoint": "https://oauth2.googleapis.com/token",
  "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
  "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
  "response_types_supported": ["code", "token", "id_token"]
}
```

### The ID Token & Core Standard Claims

A signed JWT containing identity assertion claims:

```json
{
  "iss": "https://accounts.google.com",
  "sub": "109823481230912",
  "aud": "my-client-app-id",
  "exp": 1727420400,
  "iat": 1727416800,
  "email": "user@example.com",
  "email_verified": true,
  "name": "Alex Mercer"
}
```

## Common Patterns

### Authorization Code Flow with PKCE

**Problem**: Public clients (SPAs, Mobile Apps) cannot securely store client secrets.  
**Solution**: Generate dynamic code verifier and code challenge (Proof Key for Code Exchange).

```typescript
import crypto from "crypto";

// 1. Generate Code Verifier & Challenge
function generatePkceCodes() {
  const verifier = crypto.randomBytes(32).toString("base64url");
  const challenge = crypto
    .createHash("sha256")
    .update(verifier)
    .digest("base64url");
  return { verifier, challenge };
}

// 2. Redirect to Auth URL with Challenge
const { verifier, challenge } = generatePkceCodes();
const authUrl =
  `https://auth.example.com/oauth/authorize?response_type=code` +
  `&client_id=my-spa&redirect_uri=https://app.com/callback` +
  `&code_challenge=${challenge}&code_challenge_method=S256&scope=openid profile email`;
```

## Best Practices

**Do**:

- Always Verify the Nonce Claim: Include a cryptographic `nonce` parameter in the authorization request and verify it matches in the ID token.
- Verify `at_hash` When Present: Ensure the access token hash matches `at_hash` in the ID token to prevent access token injection.
- Consume Identity Attributes from ID Token Claims: Avoid unnecessary network roundtrips to `/userinfo` when claims exist in the ID token.
- Support Dynamic Discovery: Point OIDC client libraries to the issuer URL to load endpoints automatically via `/.well-known/openid-configuration`.

**Don't**:

- Use ID tokens as API Access Tokens: ID tokens assert identity to the client app; APIs must receive Access Tokens.
- Store ID tokens without signature verification: Validate the signature against the provider's JWKS before trusting claims.
- Neglect the `sub` claim: The Subject (`sub`) claim is the only stable, immutable user identifier; emails can change.

## Troubleshooting

| Error               | Cause                         | Solution                                  |
| :------------------ | :---------------------------- | :---------------------------------------- |
| `id_token missing`  | Scope `openid` not requested. | Add `openid` to scopes.                   |
| `Signature Invalid` | Wrong Public Key.             | Refresh JWKS from the discovery endpoint. |

## References

- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html)
- [OIDC Playground](https://openidconnect.net/)
