---
name: bcrypt
description: Expert bcrypt hashing assistance covering secure password hashing, salt rounds, and timing attack prevention. Use when hashing passwords, verifying credentials, or managing authentication state.
---

# Bcrypt

Bcrypt is a password-hashing function designed to be slow, protecting against brute-force attacks. It incorporates a salt to protect against rainbow table attacks.

## When to Use

- **User Password Hashing**: Hashing user passwords securely before storing them in database tables.
- **Authentication Verification**: Verifying incoming plaintext passwords against hashed records during login attempts.
- **Legacy Credential Protection**: Maintaining established authentication backends using the proven, battle-tested bcrypt algorithm.
- **Adaptive Cost Factor Tuning**: Adjusting computational work factors over time to counter advances in hardware cracking performance.

## Quick Start

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

#The Modular Crypt Format ($2b$ Cost $ Salt + Hash)

Bcrypt outputs a standardized 60-character string encoding the algorithm revision, work factor, 128-bit salt, and 184-bit hash:

```
$2b$12$e8Y5W5t2KqfO.oXWf1NfTeu4GZ7hJ2xM.wKzV8L8T7p6Q9r8S1t2u
 ── ── ────────────────────── ──────────────────────────────
 │  │             │                         │
 │  │             │                         └── 31-character checksum/hash
 │  │             └──────────────────────────── 22-character base64 salt
 │  └────────────────────────────────────────── Work Factor (2^12 = 4,096 iterations)
 └───────────────────────────────────────────── Algorithm Identifier (2b)
```

#Salting & Adaptive Work Factor

Salting prevents rainbow table attacks; the cost factor dictates exponential computation time:

```typescript
import bcrypt from "bcrypt";

// Cost factor of 12 takes ~200-300ms on modern server CPUs
const SALT_ROUNDS = 12;

export async function hashPassword(plainText: string): Promise<string> {
  const salt = await bcrypt.genSalt(SALT_ROUNDS);
  return await bcrypt.hash(plainText, salt);
}
```

#Constant-Time Password Verification

Prevents side-channel timing attacks by performing comparisons in constant time:

```typescript
export async function verifyCredentials(
  plainText: string,
  hash: string,
): Promise<boolean> {
  // Constant-time execution ensures identical response latency regardless of match index
  return await bcrypt.compare(plainText, hash);
}
```

## Common Patterns

### Password Hashing and Constant-Time Verification

**Problem**: Storing plaintext or unsalted hashes allows rainbow table and timing-attack exploitation.

**Solution**:
Hash with optimal cost factor (12-14 rounds) and verify asynchronously:

```javascript
import bcrypt from "bcrypt";

const SALT_ROUNDS = 12;

export async function hashPassword(plainPassword) {
  return await bcrypt.hash(plainPassword, SALT_ROUNDS);
}

export async function verifyPassword(plainPassword, hashedPassword) {
  return await bcrypt.compare(plainPassword, hashedPassword);
}
```

## Best Practices (2026)

**Do**:

- **Use a Work Factor of at least 12**: Benchmark hashing time on production servers aiming for 250ms per hash.
- **Re-Hash Passwords on Login**: Check if legacy hashes have lower cost factors (`bcrypt.getRounds(hash) < 12`) and upgrade them dynamically upon successful login.
- **Handle the 72-Byte Truncation Limit**: Pre-hash passwords with SHA-256 before bcrypt if users are permitted to submit arbitrarily long passphrases.
- **Offload Hashing from Event Loops**: Always use asynchronous `bcrypt.hash()` rather than blocking `bcrypt.hashSync()`.

**Don't**:

- **Don't use MD5, SHA-1, or plain SHA-256 for passwords**: Fast general-purpose hashing functions allow billions of guesses per second on consumer GPUs.
- **Don't generate salts manually without cryptographically secure random sources**: Use `bcrypt.genSalt()` which taps `/dev/urandom`.
- **Don't log or print plaintext passwords**: Sanitize incoming request bodies in logging middleware before persisting access logs.

## Troubleshooting

| Error                                  | Cause                                                           | Solution                                                                            |
| :------------------------------------- | :-------------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| `Illegal arguments: undefined, string` | Plaintext password or hash passed as null/undefined to compare. | Validate that both arguments are non-empty strings before calling `bcrypt.compare`. |
| `High CPU usage / slow responses`      | Salt rounds set too high (>15) blocking event loop.             | Benchmark work factor; recommended value is 12 (approx ~250ms).                     |
| `data and hash arguments required`     | Parameter ordering reversed in compare function.                | Use `bcrypt.compare(candidatePassword, storedHash)`.                                |

## References

- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
