---
name: aws
description: Expert Amazon Web Services (AWS) cloud assistance covering IAM, EC2, S3, ECS/EKS, Lambda, VPC, and CloudWatch. Use when designing, deploying, and managing scalable AWS cloud architectures.
---

# AWS

Amazon Web Services (AWS) is the dominant cloud platform. In 2025, the focus is heavily on **Generative AI** (Bedrock, Q, Trainium chips) and **Serverless Data** (Aurora Limitless).

## When to Use

- **Enterprise Cloud Infrastructure**: Global compute (EC2, ECS, EKS), storage (S3), and database (Aurora, DynamoDB) solutions.
- **Serverless & Event-Driven Applications**: AWS Lambda, EventBridge, SQS, SNS, and API Gateway for zero-idle cost scaling.
- **High-Security Multi-Account Architectures**: AWS Organizations, IAM Identity Center, Control Tower, and KMS.
- **Edge Computing & Global Content Delivery**: CloudFront CDN, Route 53 DNS, and AWS WAF.

## Quick Start

```bash
# Verify credentials and caller identity
aws sts get-caller-identity

# List S3 buckets
aws s3 ls

# Sync local assets directory to private S3 bucket
aws s3 sync ./dist s3://my-app-assets-bucket/ --delete
```

## Core Concepts

#Serverless Architecture with AWS Lambda & SQS

Event-driven microservice processing incoming messages:

```python
import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ORDERS_TABLE'])

def handler(event, context):
    processed_count = 0

    for record in event['Records']:
        body = json.loads(record['body'])
        order_id = body['order_id']
        amount = body['amount']

        # Persist transaction to DynamoDB
        table.put_item(Item={
            'PK': f"ORDER#{order_id}",
            'amount': str(amount),
            'status': 'CONFIRMED',
            'timestamp': record['attributes']['ApproximateFirstReceiveTimestamp']
        })
        processed_count += 1

    return {
        'statusCode': 200,
        'body': json.dumps({'processed': processed_count})
    }
```

#Least-Privilege IAM Policy

Scoping permissions strictly to resource ARNs:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3InvoiceBucketAccess",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::corporate-invoices-prod/*"
    },
    {
      "Sid": "AllowKMSDecryption",
      "Effect": "Allow",
      "Action": "kms:Decrypt",
      "Resource": "arn:aws:kms:us-east-1:123456789012:key/abc-123",
      "Condition": {
        "StringEquals": {
          "kms:CallerAccount": "123456789012"
        }
      }
    }
  ]
}
```

#High-Availability VPC Network Architecture

Subnet layout for zero-trust network segregation:

```text
[Internet Gateway]
       │
[Public Subnets (NAT Gateway, ALB)] ──► 10.0.1.0/24, 10.0.2.0/24
       │
[Private Application Subnets (ECS, EKS, Lambda)] ──► 10.0.10.0/24, 10.0.11.0/24
       │
[Isolated Database Subnets (Aurora, Redis)] ──► 10.0.20.0/24, 10.0.21.0/24
```

## Common Patterns

### Least-Privilege IAM Policy for Application Service Roles

**Problem**: Granting wildcard `*` permissions exposes AWS accounts to severe compromise.

**Solution**:
Scoped IAM policy restricting actions to specific resources:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::my-production-bucket/uploads/*"
    },
    {
      "Effect": "Allow",
      "Action": "dynamodb:GetItem",
      "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/UserSessions"
    }
  ]
}
```

## Best Practices (2026)

- **Do** organize workloads into multi-account architectures using AWS Organizations and AWS Control Tower.
- **Do** enforce least-privilege IAM policies without wildcard actions (`"Action": "*"`) or wildcard resources.
- **Do** enable S3 Block Public Access and Default KMS Encryption across all storage buckets.
- **Do** deploy databases and application containers into private subnets with egress via NAT Gateways.
- **Don't** use AWS root account credentials for daily management or API tasks; lock with hardware MFA.
- **Don't** leave CloudWatch log groups with indefinite retention; configure explicit retention policies (e.g. 30 days).
- **Don't** hardcode AWS credentials; use IAM Roles for EC2/ECS/Lambda or OIDC for GitHub Actions.

## Troubleshooting

| Error                                                                 | Cause                                                             | Solution                                                                         |
| :-------------------------------------------------------------------- | :---------------------------------------------------------------- | :------------------------------------------------------------------------------- |
| `AccessDenied (Service: Amazon S3; Status Code: 403)`                 | IAM user/role lacks permission or S3 Bucket Policy blocks access. | Verify IAM policy permissions and check bucket Block Public Access settings.     |
| `ExpiredToken: The security token included in the request is expired` | Temporary STS credentials (AWS SSO or assumed role) have expired. | Re-authenticate: `aws sso login` or refresh STS tokens.                          |
| `VPC Resource Timeout / No internet access in Lambda`                 | Lambda placed in private subnet without NAT Gateway.              | Route private subnet 0.0.0.0/0 traffic through a NAT Gateway in a public subnet. |

## References

- [AWS Documentation](https://docs.aws.amazon.com/)
