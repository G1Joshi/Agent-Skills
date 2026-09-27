---
name: gcp
description: Expert Google Cloud Platform (GCP) assistance covering Cloud Run, GKE, Cloud Functions, BigQuery, Pub/Sub, and IAM. Use when architecting and operating scalable, enterprise cloud applications on Google Cloud.
---

# Google Cloud Platform (GCP)

GCP is known for its data analytics (BigQuery) and being the home of Kubernetes. 2025 highlights **Vertex AI** for rapid model deployment and **Cloud Run** for serverless everywhere.

## When to Use

- **Enterprise Google Cloud Infrastructure**: Compute Engine (GCE), Google Kubernetes Engine (GKE), and Cloud Run.
- **Big Data Analytics & AI/ML**: BigQuery data warehousing, Vertex AI foundation models, and Cloud Pub/Sub streaming.
- **Global Anycast Networking & CDN**: Google Cloud Armor, Cloud CDN, and Cloud Load Balancing with single global anycast IPs.
- **Serverless Event-Driven Microservices**: Cloud Run, Cloud Functions, and Eventarc.

## Quick Start

```bash
# Deploy container directly to serverless Cloud Run
gcloud run deploy web-service \
  --image us-docker.pkg.dev/cloudrun/container/hello \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Core Concepts

#Cloud Run Container Service Architecture

Deploying containerized microservices that scale to zero and scale up dynamically:

```yaml
# cloud-run-service.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: order-service
  labels:
    cloud.googleapis.com/location: us-central1
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "50"
        run.googleapis.com/cpu-throttling: "true"
    spec:
      containerConcurrency: 80
      timeoutSeconds: 300
      containers:
        - image: us-central1-docker.pkg.dev/my-project/apps/order-service:v2.1
          resources:
            limits:
              cpu: "1000m"
              memory: "1Gi"
          env:
            - name: DB_USER
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: username
```

#Pub/Sub Event Streaming with Python

Publishing and subscribing to real-time events with high throughput:

```python
from google.cloud import pubsub_v1
import json

project_id = "my-gcp-project"
topic_id = "telemetry-events"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

data = json.dumps({"sensor_id": 401, "temp": 24.5, "status": "OK"}).encode("utf-8")
future = publisher.publish(topic_path, data, origin="edge-gateway")
message_id = future.result()
print(f"Published message ID: {message_id}")
```

#Zero-Trust VPC Service Controls & IAM

Restricting access to GCP APIs within secure service perimeters:

```text
[Internet Client] ──► [Global External HTTPS Load Balancer] (Cloud Armor WAF)
                             │
                             ▼
                    [GKE / Cloud Run] (Private VPC)
                             │ (Private Google Access)
                             ▼
                    [VPC Service Controls Perimeter]
                       ├── BigQuery Datasets
                       └── Cloud Storage Buckets
```

## Common Patterns

### Event-Driven Architecture with Cloud Pub/Sub and Cloud Run

**Problem**: Decoupling synchronous service dependencies to absorb traffic surges without dropping requests.

**Solution**:
Publish events to Pub/Sub and consume via Cloud Run push subscriptions:

```bash
# 1. Create Pub/Sub Topic
gcloud pubsub topics create order-events

# 2. Create Cloud Run push subscription targeting invoice worker service
gcloud pubsub subscriptions create order-events-sub \
  --topic order-events \
  --push-endpoint https://invoice-service-xyz-uc.a.run.app/events \
  --push-auth-service-account invoice-invoker@my-project.iam.gserviceaccount.com
```

## Best Practices (2026)

- **Do** deploy serverless workloads to Cloud Run for automated scale-to-zero and high concurrency per container.
- **Do** protect applications with Google Cloud Armor security policies to neutralize DDoS and OWASP Top 10 exploits.
- **Do** configure VPC Service Controls to prevent data exfiltration from BigQuery and Cloud Storage.
- **Do** enable Secret Manager integration directly into Cloud Run and GKE pods rather than passing raw env strings.
- **Don't** use standard service account keys; use Workload Identity for GKE pods and Cloud Run services.
- **Don't** assign `roles/editor` or `roles/owner` to service accounts; adhere strictly to least-privilege IAM roles.
- **Don't** expose BigQuery datasets publicly without explicit authorized views.

## Troubleshooting

| Error                                                                           | Cause                                                                      | Solution                                                                               |
| :------------------------------------------------------------------------------ | :------------------------------------------------------------------------- | :------------------------------------------------------------------------------------- |
| `Cloud Run: The user-provided container failed to start and listen on the port` | Container listening on localhost or ignoring `$PORT` environment variable. | Ensure web server binds to `0.0.0.0` and listens on `process.env.PORT` (default 8080). |
| `403 Forbidden: Caller does not have required permission`                       | Service account lacks IAM role on target resource.                         | Grant appropriate IAM role: `roles/run.invoker` or `roles/storage.objectViewer`.       |
| `Cloud Build: Step failed with code 1`                                          | Build failure inside container build step.                                 | Inspect build logs in GCP Console under Cloud Build > History.                         |

## References

- [Google Cloud Documentation](https://cloud.google.com/docs)
