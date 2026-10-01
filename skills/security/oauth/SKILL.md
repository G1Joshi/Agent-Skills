---
name: oauth
description: Expert OAuth 2.0 / 2.1 protocol assistance covering Authorization Code Flow with PKCE, Client Credentials, and token exchange. Use when implementing third-party logins, securing API endpoints, or configuring OAuth servers.
---

# OAuth 2.1

OAuth 2.1 is the consolidation of OAuth 2.0 and its best practices into a single standard. It allows third-party applications to grant limited access to an HTTP service through an authorization server.

## When to Use

- **Delegated Authorization Framework**: Permitting third-party applications to access user resources without exposing user passwords.
- **Single Sign-On (SSO) Architectures**: Authorizing cross-application access tokens across interconnected enterprise platforms.
- **Securing Public and Mobile APIs**: Implementing standards-compliant token issuance, verification, and revocation.
- **Machine-to-Machine Service Accounts**: Granting automated microservice background daemons scoped API access.

## Quick Start

```javascript
// Client (Frontend) - redirect to Auth Server
const authUrl = `https://auth.example.com/authorize?
  response_type=code&
  client_id=${CLIENT_ID}&
  redirect_uri=${REDIRECT_URI}&
  scope=read:profile&
  code_challenge=${pkceChallenge}&
  code_challenge_method=S256`;

window.location.href = authUrl;

// Callback (Handling the redirect)
const code = new URLSearchParams(window.location.search).get("code");
const tokenResponse = await fetch("https://auth.example.com/token", {
  method: "POST",
  body: JSON.stringify({
    grant_type: "authorization_code",
    code,
    client_id: CLIENT_ID,
    redirect_uri: REDIRECT_URI,
    code_verifier: pkceVerifier, // Proof Key
  }),
});
```

## Core Concepts

### The 4 OAuth 2.0 / 2.1 Grant Types

| Grant Type                       | Client Type                                      | Use Case                                        |
| :------------------------------- | :----------------------------------------------- | :---------------------------------------------- |
| **Authorization Code with PKCE** | Public (SPA, Mobile) & Confidential (Web Server) | Standard user login and authorization           |
| **Client Credentials**           | Confidential (Backend Daemons)                   | Machine-to-machine background communication     |
| **Refresh Token**                | Confidential & Public                            | Renewing expired access tokens without re-login |
| **Device Authorization**         | Input-constrained (Smart TV, CLI)                | Authenticating via secondary browser screen     |

### Proof Key for Code Exchange (PKCE) Protocol Flow

Protects authorization codes from interception on public clients:

```text
[ Client ] ──1. Generate Verifier & Challenge (SHA256)──→ Local
[ Client ] ──2. GET /authorize?code_challenge=xyz───────→ [ Auth Server ]
[ Client ] ←─3. Receive Authorization Code─────────────── [ Auth Server ]
[ Client ] ──4. POST /token?code=123&code_verifier=abc──→ [ Auth Server ]
[ Client ] ←─5. Receive Access Token & Refresh Token───── [ Auth Server ]
```

### Scopes & Consent Management

Defines granular operational permissions approved by the resource owner:

```http
POST /oauth/token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=service_analytics
&client_secret=supersecret
&scope=read:reports%20export:csv
```

## Common Patterns

### Authorization Code Flow with PKCE (Proof Key for Code Exchange)

**Problem**: Public clients (SPAs, mobile apps) cannot safely store client secrets, making authorization codes vulnerable to interception.

**Solution**:
Generate cryptographic code verifier and code challenge on the client before initiating authorization:

```javascript
// Generate Code Verifier and S256 Challenge
const verifier = generateRandomString(64);
const challenge = base64UrlEncode(sha256(verifier));

// Redirect user to authorization endpoint
const authUrl =
  `https://auth.example.com/oauth/authorize?` +
  `response_type=code&client_id=spa-client&` +
  `redirect_uri=${encodeURIComponent(redirectUri)}&` +
  `code_challenge=${challenge}&code_challenge_method=S256`;
```

## Best Practices

**Do**:

- Enforce OAuth 2.1 Recommendations: Deprecate legacy Implicit Grant and Resource Owner Password Credentials (ROPC) completely.
- Mandate PKCE for All Authorization Code Flows: Require PKCE for confidential clients as well as public clients.
- Implement Refresh Token Rotation: Invalidate previous refresh tokens upon each exchange to detect token reuse and theft immediately.
- Validate Redirect URIs Strictly: Use exact string matching against registered redirect URIs; never use wildcard regular expressions.

**Don't**:

- Use OAuth 2.0 for Authentication without OpenID Connect: OAuth provides authorization (access tokens); OIDC adds authentication (ID tokens).
- Pass access tokens in URL query strings: Query parameters leak into browser histories, server access logs, and referrer headers.
- Grant broad wildcard scopes: Enforce least privilege by issuing fine-grained scopes tailored to the application's actual needs.

## Troubleshooting

| Error                   | Cause                        | Solution                          |
| :---------------------- | :--------------------------- | :-------------------------------- |
| `invalid_grant`         | Code expired or reused.      | Get a new authorization code.     |
| `redirect_uri_mismatch` | URI doesn't match allowlist. | Check dashboard settings exactly. |

## References

- [OAuth 2.1 Draft](https://oauth.net/2.1/)
- [OAuth 2.0 Simplified](https://aaronparecki.com/oauth-2-simplified/)
