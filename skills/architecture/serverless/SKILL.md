---
name: serverless
description: Serverless architecture with FaaS and managed services. Use for event-driven compute.
---

# Serverless

Function-as-a-Service and managed cloud services.

## When to Use

- Event-driven workloads
- Variable traffic patterns
- Reduced operations overhead
- Microservices functions

## Quick Start

```typescript
// AWS Lambda
import { APIGatewayProxyHandler } from "aws-lambda";

export const handler: APIGatewayProxyHandler = async (event) => {
  const body = JSON.parse(event.body || "{}");

  return {
    statusCode: 200,
    body: JSON.stringify({ message: "Hello", data: body }),
  };
};
```

## Core Concepts

### Function Patterns

```typescript
// Request-response
export const apiHandler = async (event: APIGatewayProxyEvent) => {
  const { pathParameters, body } = event;
  const result = await processRequest(
    pathParameters?.id,
    JSON.parse(body || "{}"),
  );
  return { statusCode: 200, body: JSON.stringify(result) };
};

// Event processing
export const sqsHandler = async (event: SQSEvent) => {
  for (const record of event.Records) {
    const message = JSON.parse(record.body);
    await processMessage(message);
  }
};

// Scheduled
export const cronHandler = async (event: ScheduledEvent) => {
  await performDailyCleanup();
};
```

### Cold Start Optimization

```typescript
// Initialize outside handler
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';

const dynamodb = new DynamoDBClient({});

export const handler = async (event: APIGatewayProxyEvent) => {
  // Client reused across invocations
  const result = await dynamodb.send(new GetItemCommand({...}));
  return { statusCode: 200, body: JSON.stringify(result) };
};
```

## Common Patterns

### Serverless Framework

```yaml
# serverless.yml
service: my-api
provider:
  name: aws
  runtime: nodejs20.x

functions:
  getUser:
    handler: src/users.get
    events:
      - http:
          path: users/{id}
          method: get

  processOrder:
    handler: src/orders.process
    events:
      - sqs:
          arn: !GetAtt OrderQueue.Arn
```

### Error Handling

```typescript
export const handler = async (event: APIGatewayProxyEvent) => {
  try {
    const result = await processRequest(event);
    return { statusCode: 200, body: JSON.stringify(result) };
  } catch (error) {
    console.error("Error:", error);
    return {
      statusCode: error.statusCode || 500,
      body: JSON.stringify({ error: error.message }),
    };
  }
};
```

## Best Practices

**Do**:

- Initialize clients outside handler
- Use environment variables
- Implement proper logging
- Set appropriate timeouts

**Don't**:

- Ignore cold starts
- Use synchronous operations
- Skip error handling
- Hardcode configuration

## Troubleshooting

| Issue           | Cause          | Solution                    |
| --------------- | -------------- | --------------------------- |
| Cold start slow | Heavy init     | Use provisioned concurrency |
| Timeout         | Long operation | Increase timeout or async   |
| Memory error    | Large payloads | Increase memory             |

## References

- [AWS Lambda Docs](https://docs.aws.amazon.com/lambda/)
- [Serverless Framework](https://www.serverless.com/framework/docs/)
