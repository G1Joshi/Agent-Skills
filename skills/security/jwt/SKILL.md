---
name: jwt
description: Expert JSON Web Token (JWT) assistance covering RS256/HS256 signing, claims validation, expiration, and refresh token rotation. Use when securing APIs, signing auth tokens, or debugging invalid signature errors.
---

# JSON Web Token (JWT)

JWT is a compact, URL-safe means of representing claims to be transferred between two parties. The claims are encoded as a JSON object that is used as the payload of a JSON Web Signature (JWS) or JSON Web Encryption (JWE).

## When to Use

- **Stateless Authorization Tokens**: Transmitting verified user identity and permission claims between microservices without database session lookups.
- **OAuth 2.0 / OpenID Connect Bearer Tokens**: Serving signed access and ID tokens across distributed web and mobile applications.
- **Short-Lived Temporary Access Grants**: Generating signed, time-limited tokens for password resets, email verification, or file downloads.
- **Decoupled Microservice Verification**: Allowing independent microservices to verify token signatures locally using shared public keys (JWKS).

## Quick Start

`Header.Payload.Signature`

```json
// Header
{
  "alg": "RS256",
  "typ": "JWT"
}

// Payload (Claims)
{
  "sub": "1234567890", // Subject (User ID)
  "name": "John Doe",
  "iat": 1516239022,    // Issued At
  "exp": 1516242622,    // Expiration
  "role": "admin"
}

// Signature
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```

## Core Concepts

### JWT Structure (Header.Payload.Signature)

A compact, URL-safe base64url-encoded string consisting of three cryptographic segments:

```text
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiZXhwIjoxNzI3NDIwNDAwfQ.XwG...
───────────────────────────────────── ────────────────────────────────────────────────────────────────────────── ───────
                │                                                         │                                         │
             Header                                                    Payload                                  Signature
   (Algorithm & Token Type)                                       (Registered & Custom Claims)              (Cryptographic Proof)
```

### Asymmetric RS256 Signing (Private Key Signs, Public Key Verifies)

Authentication servers sign tokens with a private key; downstream microservices verify with the public key:

```typescript
import jwt from "jsonwebtoken";
import fs from "fs";

const privateKey = fs.readFileSync("private.key");
const publicKey = fs.readFileSync("public.key");

// Sign token (Auth Server)
const token = jwt.sign(
  { sub: "usr_415", role: "admin", orgId: "org_99" },
  privateKey,
  {
    algorithm: "RS256",
    expiresIn: "15m",
    issuer: "https://auth.example.com",
    audience: "https://api.example.com",
  },
);

// Verify token (Resource Server / API)
const claims = jwt.verify(token, publicKey, {
  algorithms: ["RS256"],
  issuer: "https://auth.example.com",
  audience: "https://api.example.com",
});
```

### JSON Web Key Sets (JWKS) Automated Key Rotation

Resource servers dynamically fetch verified public keys without hardcoding static files:

```typescript
import { createRemoteJWKSet, jwtVerify } from "jose";

const JWKS = createRemoteJWKSet(
  new URL("https://auth.example.com/.well-known/jwks.json"),
);

const { payload } = await jwtVerify(token, JWKS, {
  issuer: "https://auth.example.com",
  audience: "https://api.example.com",
});
```

## Common Patterns

### Asymmetric Token Verification with Key Rotation (JWKS)

**Problem**: Hardcoding symmetric HMAC secrets creates key leakage risks across microservices.

**Solution**:
Use RS256 asymmetric signing with `jwks-rsa` public key retrieval:

```javascript
import jwt from "jsonwebtoken";
import jwksClient from "jwks-rsa";

const client = jwksClient({
  jwksUri: "https://auth.example.com/.well-known/jwks.json",
  cache: true,
  rateLimit: true,
});

function getKey(header, callback) {
  client.getSigningKey(header.kid, (err, key) => {
    callback(null, key ? key.getPublicKey() : null);
  });
}

export function verifyToken(token) {
  return new Promise((resolve, reject) => {
    jwt.verify(token, getKey, { algorithms: ["RS256"] }, (err, decoded) => {
      if (err) reject(err);
      else resolve(decoded);
    });
  });
}
```

## Best Practices

**Do**:

- Keep Access Token Expiration Brief (5-15 Minutes): Pair short-lived access tokens with secure refresh token rotation to minimize leakage windows.
- Always Validate `iss`, `aud`, and `exp` Claims: Never verify signature alone; ensure the token is targeted for your API and not expired.
- Use Asymmetric RS256 or EdDSA Algorithms: Never use symmetric HS256 for multi-service architectures where sharing secrets is a liability.
- Explicitly Whitelist Expected Algorithms: Enforce `algorithms: ['RS256']` in verification options to prevent algorithm confusion attacks (`none` or HS256).

**Don't**:

- Put sensitive PII or secrets in the payload: JWT payloads are merely base64 encoded and can be read by anyone with access to the token.
- Store JWTs in browser localStorage: Store auth tokens in HttpOnly, Secure, SameSite cookies to protect against XSS token theft.
- Create unbounded token sizes: Keep claims minimal; large tokens bloat every HTTP header and degrade network latency.

## Troubleshooting

| Error               | Cause                            | Solution                                     |
| :------------------ | :------------------------------- | :------------------------------------------- |
| `TokenExpiredError` | `exp` time passed.               | Refresh the token using a Refresh Token.     |
| `JsonWebTokenError` | Malformed or Signature mismatch. | Check secret/public key and token integrity. |

## References

- [jwt.io](https://jwt.io/)
- [RFC 7519](https://tools.ietf.org/html/rfc7519)
