---
name: passport
description: Passport.js authentication middleware. Use for Node.js auth.
---

# Passport.js

Passport is authentication middleware for Node.js. It is designed to serve a unique purpose: authenticate requests. It delegates all other details (user handling, sessions) to the application.

## When to Use

- **Node.js/Express Apps**: The de-facto standard for Express auth.
- **Multiple Strategies**: Supporting Local (Username/Password), Google, Facebook, and Twitter login all in one app.
- **Legacy/Established Codebases**: widely used in existing Mean/Mern stacks.

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

### Strategies

Modules that allow you to authenticate with a specific provider (`passport-local`, `passport-google-oauth20`, `passport-jwt`).

### Serialize/Deserialize

How Passport maintains the user session.

- `serializeUser`: Saves User ID to the session.
- `deserializeUser`: Uses User ID to fetch the full User object on subsequent requests.

## Best Practices (2025)

**Do**:

- **Use `passport-jwt`** for stateless APIs (Microservices).
- **Limit Session size**: Only serialize the User ID, not availability entire object.
- **Maintenance Check**: Some strategies are unmaintained. Check the GitHub repo activity before picking a strategy.

**Don't**:

- **Don't mix Logic**: Keep the Strategy config separate from your Route logic.
- **Don't rely solely on it**: Passport handles _Authentication_. You still need to handle _Authorization_ (Roles/Permissions) separately.

## References

- [Passport.js Documentation](https://www.passportjs.org/)
