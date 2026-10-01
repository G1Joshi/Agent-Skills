---
name: serverless
description: Expert Serverless architecture assistance covering Function-as-a-Service (FaaS), event triggers, cold start mitigation, stateless execution, and cloud BaaS integration. Use when building AWS Lambda, Google Cloud Functions, or Cloudflare Workers systems with event-driven scale.
---

# Serverless

Serverless is a cloud-native development model for building and running applications without managing servers. The cloud provider handles the routine work of provisioning, maintaining, and scaling the server infrastructure.

## When to Use

- **Event-Driven Workloads**: Processing file uploads (S3), stream events (Kafka/Kinesis), and asynchronous queue workers.
- **Variable & Spiky Traffic**: Applications with unpredictable request volumes scaling automatically from 0 to thousands of instances.
- **Low-Maintenance Web APIs**: Deploying micro-APIs or webhook handlers without managing servers, operating systems, or patching.
- **Scheduled Background Tasks**: Running cron jobs, batch data transformations, and reporting tasks via EventBridge / CloudWatch.

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

### Ephemeral Stateless Execution

Instances spin up on demand and shut down after idle periods; in-memory state is destroyed when containers terminate:

```typescript
// AWS Lambda / Cloudflare Worker Handler
export const handler = async (
  event: APIGatewayProxyEvent,
): Promise<APIGatewayProxyResult> => {
  // Global variables persist across warm starts, but local handler state resets
  const result = await processItem(event.body);
  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(result),
  };
};
```

### Cold Start Lifecycle & Mitigation

Understanding initialization phases:

```text
[ Download Runtime ] ──→ [ Init Execution Context (Cold Start) ] ──→ [ Execute Handler (Warm) ]
```

```typescript
// Optimize Cold Starts: Initialize heavy clients outside the handler function
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";

const ddbClient = new DynamoDBClient({ region: "us-east-1" }); // Reused on warm starts
```

### Cloud BaaS Integration & Event Mappings

Connects functions directly to cloud managed services without polling:

```yaml
# serverless.yml event mapping
functions:
  processInvoice:
    handler: src/invoice.handler
    events:
      - s3:
          bucket: enterprise-invoices
          event: s3:ObjectCreated:*
          rules:
            - suffix: .pdf
```

## Common Patterns

### Connection Pool Management Outside Handler

**Problem**: Serverless functions initialize new database connections on every invocation, exhausting connection limits.  
**Solution**: Initialize database pools outside the lambda handler to reuse connections across warm invocations.

```typescript
import { Pool } from "pg";

// Initialized in global scope during cold start, reused across invocations
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 2, // Keep pool small for serverless instances
  idleTimeoutMillis: 30000,
});

export const handler = async (event: any) => {
  const client = await pool.connect();
  try {
    const { rows } = await client.query("SELECT * FROM items WHERE id = $1", [
      event.pathParameters.id,
    ]);
    return { statusCode: 200, body: JSON.stringify(rows[0]) };
  } finally {
    client.release();
  }
};
```

## Best Practices

**Do**:

- Keep Deployment Packages Compact: Minify JavaScript with esbuild; keep lambda zip files small to reduce cold start initialization times.
- Reuse Persistent Connections in Global Scope: Instantiate database connection pools, AWS SDK clients, and HTTP agents outside the handler.
- Enforce Fine-Grained IAM Permissions: Grant functions least-privilege access to only the specific database tables or S3 buckets needed.
- Implement Structured Logging with Correlation IDs: Inject invocation request IDs and tracing headers into every log output.

**Don't**:

- Run long-running monolithic services in Lambda: Functions exceeding 15-minute limits or requiring continuous memory belong in ECS/Kubernetes.
- Create unpooled relational database connections: Use RDS Proxy or HTTP-based database drivers (Neon, PlanetScale) to prevent connection exhaustion.
- Store files on local disk: The `/tmp` directory is ephemeral and shared only during warm invocations; store assets in S3.

## Troubleshooting

| Error                 | Cause                   | Solution                                                                             |
| :-------------------- | :---------------------- | :----------------------------------------------------------------------------------- |
| `Timeout`             | Function took too long. | Increase timeout setting; optimize code; move to async pattern.                      |
| `OOM (Out of Memory)` | Processing large files. | Increase RAM (allocates more CPU too); stream data instead of loading all in memory. |

## References

- [Serverless Land (AWS)](https://serverlessland.com/)
- [SST (Serverless Stack)](https://sst.dev/)
