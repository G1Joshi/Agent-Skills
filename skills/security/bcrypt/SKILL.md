---
name: bcrypt
description: bcrypt password hashing for secure credential storage. Use for password hashing.
---

# bcrypt

Password hashing algorithm with adaptive cost factor.

## When to Use

- User password storage
- Authentication systems
- Credential verification
- Legacy system support

## Quick Start

```typescript
import bcrypt from "bcrypt";

const SALT_ROUNDS = 12;

// Hash password
const hash = await bcrypt.hash(password, SALT_ROUNDS);

// Verify password
const isValid = await bcrypt.compare(password, hash);
```

## Core Concepts

### Hashing

```typescript
async function hashPassword(password: string): Promise<string> {
  const salt = await bcrypt.genSalt(12);
  return bcrypt.hash(password, salt);
}

async function verifyPassword(
  password: string,
  hash: string,
): Promise<boolean> {
  return bcrypt.compare(password, hash);
}
```

### Cost Factor

```typescript
// Adjust cost based on hardware (2^cost iterations)
const COST = 12; // ~250ms on modern hardware

// Benchmark to find optimal cost
async function benchmarkCost() {
  for (let cost = 10; cost <= 14; cost++) {
    const start = Date.now();
    await bcrypt.hash("test", cost);
    console.log(`Cost ${cost}: ${Date.now() - start}ms`);
  }
}
```

## Best Practices

**Do**: Use cost factor 12+, store full hash string
**Don't**: Use cost below 10, implement custom bcrypt

## References

- [bcrypt npm](https://www.npmjs.com/package/bcrypt)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
