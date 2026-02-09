---
name: oauth
description: OAuth 2.0 and OpenID Connect for authentication flows. Use for secure authentication.
---

# OAuth 2.0

Authorization framework for secure delegated access.

## When to Use

- Third-party authentication
- API authorization
- Single sign-on (SSO)
- Social login integration

## Quick Start

```typescript
// Authorization Code Flow
const authUrl = new URL("https://auth.example.com/authorize");
authUrl.searchParams.set("client_id", CLIENT_ID);
authUrl.searchParams.set("redirect_uri", REDIRECT_URI);
authUrl.searchParams.set("response_type", "code");
authUrl.searchParams.set("scope", "openid profile email");
authUrl.searchParams.set("state", generateState());
authUrl.searchParams.set("code_challenge", generateCodeChallenge());
authUrl.searchParams.set("code_challenge_method", "S256");

window.location.href = authUrl.toString();
```

## Core Concepts

### Authorization Code with PKCE

```typescript
// 1. Generate PKCE verifier and challenge
function generateCodeVerifier(): string {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return base64UrlEncode(array);
}

async function generateCodeChallenge(verifier: string): Promise<string> {
  const hash = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(verifier),
  );
  return base64UrlEncode(new Uint8Array(hash));
}

// 2. Exchange code for tokens
async function exchangeCodeForTokens(code: string, verifier: string) {
  const response = await fetch("https://auth.example.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      code,
      redirect_uri: REDIRECT_URI,
      client_id: CLIENT_ID,
      code_verifier: verifier,
    }),
  });
  return response.json();
}
```

### Token Refresh

```typescript
async function refreshTokens(refreshToken: string) {
  const response = await fetch("https://auth.example.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "refresh_token",
      refresh_token: refreshToken,
      client_id: CLIENT_ID,
    }),
  });
  return response.json();
}
```

## Common Patterns

### Protected API Calls

```typescript
async function fetchWithAuth(url: string, accessToken: string) {
  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  if (response.status === 401) {
    // Token expired, refresh and retry
    const newTokens = await refreshTokens(getRefreshToken());
    saveTokens(newTokens);
    return fetchWithAuth(url, newTokens.access_token);
  }

  return response.json();
}
```

## Best Practices

**Do**:

- Use PKCE for all public clients
- Store tokens securely
- Implement token refresh
- Validate state parameter

**Don't**:

- Store tokens in localStorage
- Use implicit flow
- Skip HTTPS
- Ignore token expiration

## Troubleshooting

| Issue          | Cause          | Solution              |
| -------------- | -------------- | --------------------- |
| Invalid grant  | Code expired   | Retry auth flow       |
| CORS error     | Wrong redirect | Check allowed origins |
| Token rejected | Clock skew     | Sync server time      |

## References

- [OAuth 2.0 RFC](https://datatracker.ietf.org/doc/html/rfc6749)
- [PKCE RFC](https://datatracker.ietf.org/doc/html/rfc7636)
