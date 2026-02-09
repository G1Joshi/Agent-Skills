---
name: firebase-auth
description: Firebase Authentication for web and mobile apps. Use for Google-backed auth.
---

# Firebase Auth

Authentication service with multiple providers.

## When to Use

- Mobile app authentication
- Social login (Google, Apple, etc.)
- Phone number auth
- Anonymous users

## Quick Start

```typescript
import {
  getAuth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
} from "firebase/auth";

const auth = getAuth();

// Sign up
await createUserWithEmailAndPassword(auth, email, password);

// Sign in
await signInWithEmailAndPassword(auth, email, password);

// Current user
const user = auth.currentUser;
```

## Core Concepts

### Auth State

```typescript
import { onAuthStateChanged } from "firebase/auth";

onAuthStateChanged(auth, (user) => {
  if (user) {
    console.log("Signed in:", user.uid);
  } else {
    console.log("Signed out");
  }
});
```

### Social Login

```typescript
import { GoogleAuthProvider, signInWithPopup } from "firebase/auth";

const provider = new GoogleAuthProvider();
const result = await signInWithPopup(auth, provider);
const user = result.user;
```

### ID Tokens

```typescript
const token = await user.getIdToken();

// Verify on server
import { getAuth } from "firebase-admin/auth";
const decoded = await getAuth().verifyIdToken(token);
```

## Best Practices

**Do**: Use onAuthStateChanged for state, verify tokens server-side
**Don't**: Trust client claims without verification

## References

- [Firebase Auth Docs](https://firebase.google.com/docs/auth)
