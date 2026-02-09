---
name: aws
description: Amazon Web Services cloud platform with Lambda, EC2, S3, and RDS. Use for AWS infrastructure.
---

# AWS

Amazon Web Services cloud platform for building scalable infrastructure.

## When to Use

- Cloud infrastructure deployment
- Serverless applications (Lambda)
- Managed databases (RDS)
- Object storage (S3)

## Quick Start

```typescript
// Lambda function
import { APIGatewayProxyHandler } from "aws-lambda";

export const handler: APIGatewayProxyHandler = async (event) => {
  const body = JSON.parse(event.body || "{}");

  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: "Hello", data: body }),
  };
};
```

## Core Concepts

### S3 Operations

```typescript
import {
  S3Client,
  PutObjectCommand,
  GetObjectCommand,
} from "@aws-sdk/client-s3";
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";

const s3 = new S3Client({ region: "us-east-1" });

// Upload
await s3.send(
  new PutObjectCommand({
    Bucket: "my-bucket",
    Key: "files/document.pdf",
    Body: buffer,
    ContentType: "application/pdf",
  }),
);

// Generate presigned URL
const url = await getSignedUrl(
  s3,
  new GetObjectCommand({
    Bucket: "my-bucket",
    Key: "files/document.pdf",
  }),
  { expiresIn: 3600 },
);
```

### DynamoDB

```typescript
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import {
  DynamoDBDocumentClient,
  PutCommand,
  QueryCommand,
} from "@aws-sdk/lib-dynamodb";

const client = DynamoDBDocumentClient.from(new DynamoDBClient({}));

// Write
await client.send(
  new PutCommand({
    TableName: "Users",
    Item: { pk: "USER#123", sk: "PROFILE", name: "John" },
  }),
);

// Query
const { Items } = await client.send(
  new QueryCommand({
    TableName: "Users",
    KeyConditionExpression: "pk = :pk",
    ExpressionAttributeValues: { ":pk": "USER#123" },
  }),
);
```

## Common Patterns

### Infrastructure as Code (CDK)

```typescript
import * as cdk from "aws-cdk-lib";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as apigateway from "aws-cdk-lib/aws-apigateway";

export class ApiStack extends cdk.Stack {
  constructor(scope: cdk.App, id: string) {
    super(scope, id);

    const fn = new lambda.Function(this, "Handler", {
      runtime: lambda.Runtime.NODEJS_20_X,
      handler: "index.handler",
      code: lambda.Code.fromAsset("lambda"),
    });

    new apigateway.LambdaRestApi(this, "Api", {
      handler: fn,
    });
  }
}
```

## Best Practices

**Do**:

- Use IAM roles with least privilege
- Enable CloudTrail logging
- Use VPC for network isolation
- Implement proper tagging

**Don't**:

- Hardcode credentials
- Use root account for daily tasks
- Leave S3 buckets public
- Skip encryption at rest

## Troubleshooting

| Issue              | Cause           | Solution                  |
| ------------------ | --------------- | ------------------------- |
| Access Denied      | IAM permissions | Check IAM policy          |
| Lambda timeout     | Long execution  | Increase timeout/optimize |
| Connection timeout | VPC/SG issue    | Check security groups     |

## References

- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS CDK](https://docs.aws.amazon.com/cdk/)
