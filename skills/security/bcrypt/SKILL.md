---
name: bcrypt
description: bcrypt password hashing. Use for password security.
---

# Bcrypt

Bcrypt is a password-hashing function designed to be slow, protecting against brute-force attacks. It incorporates a salt to protect against rainbow table attacks.

## When to Use

- **User Passwords**: Storing passwords in a database. NEVER store them in plain text.
- **API Keys**: Hashing API keys before storage (if you only show them once).

## Quick Start (Node.js)

```javascript
import bcrypt from "bcrypt";

const saltRounds = 10;
const myPlaintextPassword = "s0m3password";

// Hashing
const hash = await bcrypt.hash(myPlaintextPassword, saltRounds);
// Store 'hash' in DB: $2b$10$EpIxT98h....

// Verifying
const match = await bcrypt.compare("s0m3password", hash);
if (match) {
  // Login successful
}
```

## Core Concepts

### Salt

Random data added to the password input before hashing. Ensures that two users with the same password have different hashes. Bcrypt handles this automatically.

### Work Factor (Cost)

The `saltRounds` (e.g., 10 or 12). Determines how slow the hashing is. As computers get faster, you increase the cost to keep brute-forcing expensive.

## Best Practices (2025)

**Do**:

- **Use Cost 10-12**: A good balance between security (slow for attackers) and UX (fast enough for login).
- **Consider Argon2id**: For new high-security projects, **Argon2id** is the modern winner (OWASP recommendation) as it resists GPU cracking better than Bcrypt. But Bcrypt is still "secure enough" for most web apps.
- **Async**: Always use the async version to avoid blocking the Event Loop in Node.js.

**Don't**:

- **Don't Roll Your Own Crypto**: Never use SHA-256 or MD5 for passwords.
- **Don't pre-hash**: Don't MD5 the password on the client before sending it. Send via HTTPS, then Bcrypt on server.

## References

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
