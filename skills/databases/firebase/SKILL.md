---
name: firebase
description: Firebase Realtime Database and Firestore for mobile/web sync. Use for real-time apps.
---

# Firebase (Firestore & Realtime Database)

Firebase provides two NoSQL databases:

1.  **Cloud Firestore**: The newer, recommended scalable database.
2.  **Realtime Database**: The original low-latency JSON tree sync.

## When to Use

- **Mobile Apps**: Best-in-class integration with Android/iOS/Flutter.
- **Realtime Sync**: Chat apps, live dashboards.
- **Offline Support**: Outstanding offline SDK capabilities.

## Quick Start (Firestore)

```javascript
import { getFirestore, collection, addDoc } from "firebase/firestore";

const db = getFirestore(app);

// Add document
await addDoc(collection(db, "users"), {
  first: "Ada",
  last: "Lovelace",
  born: 1815,
});
```

## Core Concepts

### Security Rules

Since you access Firebase from the client, you write JSON-like rules to secure it.

```javascript
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
  }
}
```

### Realtime Updates

Listeners (`onSnapshot`) keep UI in sync automatically.

## Best Practices (2025)

**Do**:

- **Use Firestore Preferentially**: It queries and scales better than Realtime DB.
- **Use Cloud Functions**: For backend logic (sending emails, sanitizing text) triggered by DB events.
- **Denormalize**: Duplicate data to avoid excessive reads (No joins in Firestore).

**Don't**:

- **Don't use sequential keys**: Use auto-generated IDs.
- **Don't ignore index limits**: Firestore requires composite indexes for sorting/filtering on multiple fields.

## References

- [Firebase Documentation](https://firebase.google.com/docs)
