---
name: gcp
description: Google Cloud Platform with Cloud Run, GKE, and BigQuery. Use for GCP infrastructure.
---

# Google Cloud Platform

Google Cloud services for scalable applications and data analytics.

## When to Use

- Kubernetes workloads (GKE)
- Serverless containers (Cloud Run)
- Data analytics (BigQuery)
- Machine learning (Vertex AI)

## Quick Start

```typescript
// Cloud Function
import { HttpFunction } from "@google-cloud/functions-framework";

export const helloWorld: HttpFunction = (req, res) => {
  const name = req.query.name || "World";
  res.send(`Hello, ${name}!`);
};
```

## Core Concepts

### Cloud Storage

```typescript
import { Storage } from "@google-cloud/storage";

const storage = new Storage();
const bucket = storage.bucket("my-bucket");

// Upload
await bucket.upload("local-file.pdf", {
  destination: "files/document.pdf",
  metadata: { contentType: "application/pdf" },
});

// Download
await bucket.file("files/document.pdf").download({
  destination: "downloaded.pdf",
});

// Signed URL
const [url] = await bucket.file("files/document.pdf").getSignedUrl({
  action: "read",
  expires: Date.now() + 3600 * 1000,
});
```

### Firestore

```typescript
import { Firestore } from "@google-cloud/firestore";

const db = new Firestore();

// Write
await db.collection("users").doc("123").set({
  name: "John",
  email: "john@example.com",
});

// Query
const snapshot = await db
  .collection("users")
  .where("status", "==", "active")
  .orderBy("createdAt", "desc")
  .limit(10)
  .get();

snapshot.forEach((doc) => console.log(doc.data()));
```

## Common Patterns

### Cloud Run Deployment

```yaml
# cloudbuild.yaml
steps:
  - name: "gcr.io/cloud-builders/docker"
    args: ["build", "-t", "gcr.io/$PROJECT_ID/myapp", "."]

  - name: "gcr.io/cloud-builders/docker"
    args: ["push", "gcr.io/$PROJECT_ID/myapp"]

  - name: "gcr.io/cloud-builders/gcloud"
    args:
      - "run"
      - "deploy"
      - "myapp"
      - "--image=gcr.io/$PROJECT_ID/myapp"
      - "--region=us-central1"
      - "--platform=managed"
```

## Best Practices

**Do**:

- Use service accounts with minimal permissions
- Enable Cloud Audit Logs
- Use VPC Service Controls
- Implement proper IAM bindings

**Don't**:

- Use default service accounts
- Make buckets public
- Skip encryption
- Ignore billing alerts

## Troubleshooting

| Issue             | Cause         | Solution                    |
| ----------------- | ------------- | --------------------------- |
| Permission denied | IAM issue     | Check service account roles |
| Cold start slow   | First request | Use min instances           |
| Quota exceeded    | Rate limiting | Request quota increase      |

## References

- [GCP Documentation](https://cloud.google.com/docs)
- [Cloud Run](https://cloud.google.com/run/docs)
