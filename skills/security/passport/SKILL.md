---
name: passport
description: Expert Passport.js authentication assistance covering Local, JWT, and OAuth strategies for Node.js / Express. Use when structuring Express authentication middleware, session handling, or multi-provider logins.
---

# Passport.js

Passport is authentication middleware for Node.js. It is designed to serve a unique purpose: authenticate requests. It delegates all other details (user handling, sessions) to the application.

## When to Use

- **Node.js Express Authentication Middleware**: Integrating authentication into Node.js Express, Koa, or NestJS backend services.
- **Pluggable Multi-Strategy Authentication**: Combining Local username/password, JWT bearer tokens, and OAuth2 strategies under one interface.
- **Established Express Monoliths**: Adding authentication to existing enterprise Express codebases with mature session infrastructures.
- **Custom Authentication Protocols**: Authoring tailored authentication strategies using Passport's clean middleware contract.

## Quick Start

```javascript
import passport from "passport";
import LocalStrategy from "passport-local";

// Configure Strategy
passport.use(
  new LocalStrategy(async (username, password, done) => {
    const user = await User.findOne({ username });
    if (!user) return done(null, false);
    if (!user.verifyPassword(password)) return done(null, false);
    return done(null, user);
  }),
);

// Middleware in Route
app.post(
  "/login",
  passport.authenticate("local", {
    successRedirect: "/",
    failureRedirect: "/login",
  }),
);
```

## Core Concepts

### Pluggable Strategy Architecture

Passport delegates credential verification to specialized Strategy plugins (`passport-local`, `passport-jwt`, `passport-google-oauth20`):

```typescript
import passport from "passport";
import { Strategy as LocalStrategy } from "passport-local";
import bcrypt from "bcrypt";

passport.use(
  new LocalStrategy(
    { usernameField: "email" },
    async (email, password, done) => {
      try {
        const user = await db.findUserByEmail(email);
        if (!user) return done(null, false, { message: "Invalid credentials" });

        const isValid = await bcrypt.compare(password, user.passwordHash);
        if (!isValid)
          return done(null, false, { message: "Invalid credentials" });

        return done(null, user);
      } catch (err) {
        return done(err);
      }
    },
  ),
);
```

### Session Serialization & Deserialization

Coordinates storing minimal user identifiers in session cookies and hydrating full user entities on subsequent requests:

```typescript
// Serialize: Store only user ID in session store (Redis)
passport.serializeUser((user: any, done) => {
  done(null, user.id);
});

// Deserialize: Fetch user record on each incoming request
passport.deserializeUser(async (id: string, done) => {
  try {
    const user = await db.findUserById(id);
    done(null, user);
  } catch (err) {
    done(err);
  }
});
```

### Stateless JWT Strategy for APIs

Validates bearer tokens without maintaining server-side session state:

```typescript
import { Strategy as JwtStrategy, ExtractJwt } from "passport-jwt";

passport.use(
  new JwtStrategy(
    {
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      secretOrKey: process.env.JWT_SECRET!,
    },
    async (payload, done) => {
      return done(null, { id: payload.sub, role: payload.role });
    },
  ),
);
```

## Common Patterns

### Modular JWT Strategy Configuration

**Problem**: Replicating authentication middleware logic across multiple microservices.

**Solution**:
Configure standard Passport JWT extraction from authorization headers:

```javascript
import passport from "passport";
import { Strategy as JwtStrategy, ExtractJwt } from "passport-jwt";

const opts = {
  jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
  secretOrKey: process.env.JWT_SECRET,
};

passport.use(
  new JwtStrategy(opts, async (jwtPayload, done) => {
    try {
      const user = await findUserById(jwtPayload.sub);
      if (user) return done(null, user);
      return done(null, false);
    } catch (err) {
      return done(err, false);
    }
  }),
);
```

## Best Practices

**Do**:

- Store Only the User ID in `serializeUser`: Keep session store payloads tiny; fetch updated permissions on deserialization.
- Use Stateless JWT Strategy for REST APIs: Avoid heavy cookie-based session stores when servicing stateless mobile and frontend clients.
- Handle Async Errors Gracefully: Always wrap database lookups in try/catch blocks and pass exceptions to `done(err)`.
- Combine with Express Session Stores (Redis): Use `connect-redis` to share session state horizontally across Node.js replicas.

**Don't**:

- Store full user objects in sessions: Outdated permissions or changed passwords won't take effect until sessions expire.
- Use `passport.authenticate('local')` without rate limiting: Protect authentication endpoints with `express-rate-limit` against brute-force attacks.
- Forget to call `done()`: Failing to invoke `done()` leaves HTTP requests hanging until client connection timeouts.

## Troubleshooting

| Error                                                | Cause                                                                             | Solution                                                                 |
| :--------------------------------------------------- | :-------------------------------------------------------------------------------- | :----------------------------------------------------------------------- |
| `TypeError: passport.initialize() is not a function` | Incorrect import syntax or calling initialize before middleware stack is ready.   | Use `app.use(passport.initialize())` after body parsers.                 |
| `Unauthorized: 401 on protected route`               | Authorization header missing `Bearer ` prefix or token expired.                   | Inspect inbound request header: must be `Authorization: Bearer <token>`. |
| `Unknown authentication strategy`                    | Route attempting to authenticate with a strategy before calling `passport.use()`. | Initialize and register all strategy instances before mounting routes.   |

## References

- [Passport.js Documentation](https://www.passportjs.org/)
