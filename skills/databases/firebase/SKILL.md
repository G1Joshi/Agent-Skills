---
name: firebase
description: Firebase Realtime Database and Firestore for mobile/web sync. Use for real-time apps.
---

# Firebase

Real-time database and backend services for mobile and web applications.

## When to Use

- Real-time data synchronization
- Mobile app backend
- Serverless applications
- Rapid prototyping

## Quick Start

```javascript
import { initializeApp } from "firebase/app";
import {
  getFirestore,
  collection,
  addDoc,
  onSnapshot,
} from "firebase/firestore";

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Add document
await addDoc(collection(db, "users"), {
  name: "John",
  email: "john@example.com",
  createdAt: new Date(),
});
```

## Core Concepts

### Firestore Queries

```javascript
import { query, where, orderBy, limit, getDocs } from "firebase/firestore";

// Complex query
const q = query(
  collection(db, "posts"),
  where("status", "==", "published"),
  where("authorId", "==", userId),
  orderBy("createdAt", "desc"),
  limit(10),
);

const snapshot = await getDocs(q);
snapshot.forEach((doc) => console.log(doc.data()));

// Real-time listener
const unsubscribe = onSnapshot(q, (snapshot) => {
  snapshot.docChanges().forEach((change) => {
    if (change.type === "added") console.log("New:", change.doc.data());
  });
});
```

### Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }

    // Public read, authenticated write
    match /posts/{postId} {
      allow read: if true;
      allow create: if request.auth != null;
      allow update, delete: if request.auth.uid == resource.data.authorId;
    }
  }
}
```

## Common Patterns

### Data Modeling

```javascript
// Subcollections for 1:many
// users/{userId}/posts/{postId}
await addDoc(collection(db, "users", userId, "posts"), postData);

// Denormalization for queries
const post = {
  title: "My Post",
  authorId: userId,
  authorName: user.name, // Denormalized
  createdAt: serverTimestamp(),
};

// Batched writes
const batch = writeBatch(db);
batch.set(doc(db, "users", id), userData);
batch.update(doc(db, "stats", "users"), { count: increment(1) });
await batch.commit();
```

## Best Practices

**Do**:

- Use security rules (never leave open)
- Design data for query patterns
- Use batched writes for atomicity
- Enable offline persistence

**Don't**:

- Store sensitive data without rules
- Create deeply nested data
- Over-fetch with listeners
- Ignore billing alerts

## Troubleshooting

| Issue             | Cause                   | Solution             |
| ----------------- | ----------------------- | -------------------- |
| Permission denied | Security rules          | Check auth and rules |
| Slow queries      | Missing composite index | Create in console    |
| High reads bill   | Real-time over-fetching | Use pagination       |

## References

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firestore Best Practices](https://firebase.google.com/docs/firestore/best-practices)
