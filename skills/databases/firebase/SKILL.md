---
name: firebase
description: Expert Firebase & Cloud Firestore assistance covering collection/document models, real-time listeners, security rules, and offline caching. Use when building mobile/web apps with real-time sync and client auth.
---

# Firebase (Firestore & Realtime Database)

Firebase provides two NoSQL databases:

1.  **Cloud Firestore**: The newer, recommended scalable database.
2.  **Realtime Database**: The original low-latency JSON tree sync.

## When to Use

- **Real-Time Client Synchronization**: Pushing document and collection updates instantly to mobile and web clients via Firestore snapshot listeners.
- **Rapid Prototyping & MVPs**: Building complete web and mobile apps with drop-in Auth, Firestore, Cloud Functions, and Hosting.
- **Offline-First Mobile Apps**: Native offline caching and latency compensation out of the box in mobile and web SDKs.
- **Client-Direct Database Access**: Allowing client applications to query databases directly while enforcing access via declarative Security Rules.

## Quick Start

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

### Document & Collection Hierarchy (Firestore)

Data is organized into documents containing fields, nested inside collections and subcollections:

```text
users (Collection)
  └── user_101 (Document)
        ├── name: "Alex"
        └── orders (Subcollection)
              └── order_99 (Document)
```

### Real-Time Snapshot Listeners

Subscribes to live document updates with zero polling boilerplate:

```typescript
import { doc, onSnapshot } from "firebase/firestore";
import { db } from "./firebase-config";

const unsub = onSnapshot(doc(db, "projects", "proj_415"), (docSnap) => {
  if (docSnap.exists()) {
    console.log("Current Project Data:", docSnap.data());
  }
});
```

### Declarative Security Rules Architecture

Enforces authorization and schema validation at the database layer:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    match /posts/{postId} {
      allow read: if resource.data.isPublished == true;
      allow create: if request.auth != null && request.resource.data.authorId == request.auth.uid;
    }
  }
}
```

## Common Patterns

### Atomic Counter Increment with Firestore Transactions

**Problem**: Concurrent client clicks reading and updating the same counter cause race condition data corruption.

**Solution**:
Use `FieldValue.increment` for atomic database updates:

```javascript
import { doc, updateDoc, increment } from "firebase/firestore";
import { db } from "./firebaseConfig";

async function upvotePost(postId) {
  const postRef = doc(db, "posts", postId);
  await updateDoc(postRef, {
    upvotes: increment(1),
    lastActivity: new Date(),
  });
}
```

## Best Practices

**Do**:

- Write Strict Security Rules: Never ship rules with `allow read, write: if true;`; validate user auth and required fields.
- Always Unsubscribe from Listeners: Call the returned unsubscribe function (`unsub()`) when UI components unmount to prevent memory leaks.
- Use Composite Indexes for Complex Queries: Define composite indexes in `firestore.indexes.json` for queries with multiple filters and sort orders.
- Batch Writes with `writeBatch()`: Execute up to 500 document writes atomically to ensure consistency and minimize network roundtrips.

**Don't**:

- Store large collections in single documents: Avoid unbounded document arrays; single documents cannot exceed 1MB.
- Query without limits in mobile apps: Always append `.limit(20)` to prevent consuming excessive read quotas.
- Write sensitive secrets in client Firebase config: Firebase API keys in client code identify projects; protect data via Security Rules.

## Troubleshooting

| Error                                 | Cause                                                                | Solution                                                                                    |
| :------------------------------------ | :------------------------------------------------------------------- | :------------------------------------------------------------------------------------------ |
| `Missing or insufficient permissions` | Firestore Security Rules rejecting the request.                      | Check `request.auth` in `firestore.rules` and verify client authentication token.           |
| `The query requires an index`         | Query filters across multiple fields or orders on a different field. | Click the generated index link in the Firebase error console to create the composite index. |
| `Resource Exhausted: Quota exceeded`  | Daily free tier document read/write limits exceeded.                 | Upgrade to Blaze plan or optimize listener queries with `limit()` clauses.                  |

## References

- [Firebase Documentation](https://firebase.google.com/docs)
