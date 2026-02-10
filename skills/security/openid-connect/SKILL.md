---
name: openid-connect
description: OpenID Connect identity layer. Use for SSO.
---

# OpenID Connect (OIDC)

OIDC extends OAuth 2.0 to provide **Identity**. While OAuth handles "Access" (Authorization), OIDC handles "Who are you?" (Authentication).

## When to Use

- **Single Sign-On (SSO)**: One login for multiple apps.
- **User Profile**: Getting `name`, `email`, `picture` from a provider.
- **Enterprise Identity**: Connecting to Active Directory via OIDC.

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

### ID Token

A JSON Web Token (JWT) that contains claims (assertions) about the authentication event and the user.

### UserInfo Endpoint

A standard OAuth protected endpoint (`/userinfo`) where you can send the Access Token to get more user details.

### Scopes

- `openid`: Required to use OIDC.
- `profile`: Request access to name, picture, etc.
- `email`: Request access to email.

## Common Patterns

### Discovery Endpoint

`/.well-known/openid-configuration`. A JSON file that lists the issuer, authorization endpoint, token endpoint, and public keys (JWKS) automatically.

## Best Practices

**Do**:

- Validate the **ID Token Signature** (using JWKS).
- Check the **Audience** (`aud`) claim matches your Client ID.
- Check the **Issuer** (`iss`) claim matches the provider.
- Use **Nonce** to prevent replay attacks.

**Don't**:

- Don't treat the Access Token as an ID Token (Access Tokens are opaque strings in standard OAuth, though often JWTs in practice).
- Don't accept unsigned ID tokens (algorithm `none`).

## Troubleshooting

| Error               | Cause                         | Solution                                  |
| :------------------ | :---------------------------- | :---------------------------------------- |
| `id_token missing`  | Scope `openid` not requested. | Add `openid` to scopes.                   |
| `Signature Invalid` | Wrong Public Key.             | Refresh JWKS from the discovery endpoint. |

## References

- [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html)
- [OIDC Playground](https://openidconnect.net/)
