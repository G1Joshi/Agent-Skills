---
name: oauth
description: OAuth 2.0 authorization framework. Use for authorization.
---

# OAuth 2.1

OAuth 2.1 is the consolidation of OAuth 2.0 and its best practices into a single standard. It allows third-party applications to grant limited access to an HTTP service through an authorization server.

## When to Use

- **Social Login**: "Log in with Google/Facebook".
- **Third-Party Access**: Giving a budgeting app access to your bank APIs.
- **Microservices**: Service A accessing Service B on behalf of a user.

## Quick Start (Authorization Code Flow with PKCE)

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

### Roles

- **Resource Owner**: The User.
- **Client**: The App (Web, Mobile, Server).
- **Authorization Server**: The Identity Provider (Auth0, Okta, Google).
- **Resource Server**: The API holding the data.

### PKCE (Proof Key for Code Exchange)

Now **Mandatory** in OAuth 2.1 for all clients (public and confidential). Prevents authorization code interception attacks.

### Grants (Flows)

- **Authorization Code**: The standard flow (Web/Mobile).
- **Client Credentials**: Machine-to-Machine (No user).
- **Device Code**: TV/Input-constrained devices.
- **Implicit Grant**: **REMOVED** (Insecure). Do not use.
- **Password Grant**: **REMOVED** (Insecure). Do not use.

## Best Practices (2025)

**Do**:

- Use **Authorization Code Flow with PKCE** for everything.
- Validate **Exact Redirect URIs** (No wildcards).
- Use **Sender-Constrained Tokens** (DPoP or mTLS) to prevent token replay/theft.

**Don't**:

- Don't use the Implicit Grant (access token in URL fragment).
- Don't store Access Tokens in `localStorage` (XSS risk). Use HttpOnly cookies or memory.

## Troubleshooting

| Error                   | Cause                        | Solution                          |
| :---------------------- | :--------------------------- | :-------------------------------- |
| `invalid_grant`         | Code expired or reused.      | Get a new authorization code.     |
| `redirect_uri_mismatch` | URI doesn't match allowlist. | Check dashboard settings exactly. |

## References

- [OAuth 2.1 Draft](https://oauth.net/2.1/)
- [OAuth 2.0 Simplified](https://aaronparecki.com/oauth-2-simplified/)
