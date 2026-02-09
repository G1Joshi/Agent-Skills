---
name: jwt
description: JSON Web Tokens for stateless authentication and claims. Use for token-based auth.
---

# JWT

JSON Web Tokens for stateless authentication.

## When to Use

- API authentication
- Stateless sessions
- Claims-based authorization
- Cross-service authentication

## Quick Start

```typescript
import jwt from "jsonwebtoken";

// Create token
const token = jwt.sign(
  { userId: "123", role: "admin" },
  process.env.JWT_SECRET!,
  { expiresIn: "1h" },
);

// Verify token
const payload = jwt.verify(token, process.env.JWT_SECRET!);
```

## Core Concepts

### Token Structure

```javascript
// Header.Payload.Signature
// eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
// eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4ifQ.
// Signature

// Decoded payload
{
  "sub": "1234567890",       // Subject (user ID)
  "name": "John Doe",        // Custom claim
  "iat": 1516239022,         // Issued at
  "exp": 1516242622,         // Expiration
  "iss": "https://auth.example.com",  // Issuer
  "aud": "https://api.example.com"    // Audience
}
```

### Token Generation

```typescript
interface TokenPayload {
  userId: string;
  email: string;
  role: string;
}

function generateTokens(user: User) {
  const accessToken = jwt.sign(
    { userId: user.id, email: user.email, role: user.role },
    process.env.JWT_SECRET!,
    { expiresIn: "15m", issuer: "my-app" },
  );

  const refreshToken = jwt.sign(
    { userId: user.id, tokenVersion: user.tokenVersion },
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: "7d" },
  );

  return { accessToken, refreshToken };
}
```

## Common Patterns

### Middleware Verification

```typescript
import { Request, Response, NextFunction } from "express";

interface AuthRequest extends Request {
  user?: TokenPayload;
}

function authMiddleware(req: AuthRequest, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith("Bearer ")) {
    return res.status(401).json({ error: "No token provided" });
  }

  const token = authHeader.slice(7);

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as TokenPayload;
    req.user = payload;
    next();
  } catch (error) {
    return res.status(401).json({ error: "Invalid token" });
  }
}
```

### Role-Based Access

```typescript
function requireRole(...roles: string[]) {
  return (req: AuthRequest, res: Response, next: NextFunction) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ error: "Forbidden" });
    }
    next();
  };
}

// Usage
app.get("/admin", authMiddleware, requireRole("admin"), adminHandler);
```

## Best Practices

**Do**:

- Use short expiration for access tokens
- Implement refresh token rotation
- Store secrets securely
- Validate all claims

**Don't**:

- Store sensitive data in payload
- Use weak secrets
- Skip expiration validation
- Store tokens in localStorage

## Troubleshooting

| Issue             | Cause           | Solution           |
| ----------------- | --------------- | ------------------ |
| Invalid signature | Wrong secret    | Check secret match |
| Token expired     | Clock skew      | Allow tolerance    |
| jwt malformed     | Corrupted token | Regenerate token   |

## References

- [JWT.io](https://jwt.io/)
- [JWT RFC](https://datatracker.ietf.org/doc/html/rfc7519)
