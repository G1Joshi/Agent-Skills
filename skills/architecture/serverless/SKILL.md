---
name: serverless
description: Serverless architecture with FaaS and BaaS. Use for cloud functions.
---

# Serverless

Serverless is a cloud-native development model for building and running applications without managing servers. The cloud provider handles the routine work of provisioning, maintaining, and scaling the server infrastructure.

## When to Use

- Event-driven background tasks (Image processing, Cron jobs).
- APIs with spiky or unpredictable traffic (Auto-scales instantly).
- Startup/MVP where "Scale to Zero" (Zero cost when idle) is critical.
- Glue code between cloud services (e.g., S3 trigger -> Lambda -> DynamoDB).

## Quick Start

```javascript
// AWS Lambda Handler (Node.js)
export const handler = async (event) => {
  console.log("Event received:", JSON.stringify(event));

  const name = event.queryStringParameters?.name || "World";

  return {
    statusCode: 200,
    body: JSON.stringify({ message: `Hello, ${name}!` }),
  };
};
```

```yaml
# serverless.yml (Serverless Framework)
service: my-api
provider:
  name: aws
  runtime: nodejs20.x

functions:
  hello:
    handler: handler.hello
    events:
      - httpApi:
          path: /hello
          method: get
```

## Core Concepts

### FaaS (Function as a Service)

Upload code (Function), define triggers (HTTP, Queue, DB, Timer). Run only when triggered.

### Cold Start

The latency incurred when a function is invoked after being idle (container spinning up).

### Statelessness

Functions are ephemeral. Store state in external managed services (Redis, DynamoDB, S3).

## Common Patterns

### Fan-out

One event triggers multiple parallel functions (e.g., Upload -> [Resize, Analyze, Back up]).

### Strangler Fig

Migrating a monolith by gradually replacing endpoints with serverless functions routed via API Gateway.

## Best Practices

**Do**:

- Use **Frameworks** (SST, Serverless Framework, SAM) for IaC.
- optimize **Cold Starts** (keep functions small, use provisioned concurrency if needed).
- Use **Managed Services** (DynamoDB, EventBridge) instead of custom code logic.

**Don't**:

- Don't use Serverless for Long-Running tasks (Gateways timeout at ~30s, Lambdas at 15m). Use Fargate/Batch for that.
- Don't ignore **vendor lock-in** (though often the speed creates enough value to justify it).

## Troubleshooting

| Error                 | Cause                   | Solution                                                                             |
| :-------------------- | :---------------------- | :----------------------------------------------------------------------------------- |
| `Timeout`             | Function took too long. | Increase timeout setting; optimize code; move to async pattern.                      |
| `OOM (Out of Memory)` | Processing large files. | Increase RAM (allocates more CPU too); stream data instead of loading all in memory. |

## References

- [Serverless Land (AWS)](https://serverlessland.com/)
- [SST (Serverless Stack)](https://sst.dev/)
