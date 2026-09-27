---
name: awscli
description: Expert AWS CLI assistance covering command-line options, profiles, JMESPath output queries (--query), and scripting automation. Use when querying AWS resources, automating deployments, and managing cloud services.
---

# AWS CLI

The AWS CLI allows you to control AWS services from the command line. In 2025, usage is centered around **AWS IAM Identity Center** (formerly SSO) for secure, short-lived credentials.

## When to Use

- **Scripting & Automating AWS Operations**: Managing cloud resources from shell scripts and CI/CD runners via `aws`.
- **Querying AWS Resources with JMESPath**: Filtering and extracting precise JSON properties using `--query`.
- **High-Speed S3 File Synchronization**: Syncing gigabytes of assets with parallel multi-part transfers (`aws s3 sync`).
- **AssumeRole & Temporary Credential Management**: Generating STS temporary tokens for secure script execution.

## Quick Start

```bash
# Install v2
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Configure with SSO (Recommended 2025)
aws configure sso
# SSO session name: my-session
# SSO start URL: https://my-org.awsapps.com/start
# SSO region: us-east-1
# Registration scopes: sso:account:access
```

```bash
# Login daily
aws sso login --profile my-profile
```

## Core Concepts

#JMESPath Filtering & Formatting

Querying specific fields without installing jq:

```bash
# List EC2 instance IDs, private IPs, and states in a formatted table
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query "Reservations[*].Instances[*].{ID:InstanceId,IP:PrivateIpAddress,Type:InstanceType,Name:Tags[?Key=='Name']|[0].Value}" \
  --output table

# Extract single value as raw text
INSTANCE_ID=$(aws ec2 describe-instances \
  --filters "Name=tag:Environment,Values=production" \
  --query "Reservations[0].Instances[0].InstanceId" \
  --output text)
```

#High-Throughput S3 Synchronization

Syncing build artifacts with cache headers:

```bash
# Sync static website assets with immutable caching
aws s3 sync dist/ s3://production-static-assets-2026/ \
  --delete \
  --cache-control "public, max-age=31536000, immutable" \
  --exclude "*.html"

# Upload HTML entrypoints with no-cache header
aws s3 sync dist/ s3://production-static-assets-2026/ \
  --exclude "*" \
  --include "*.html" \
  --cache-control "no-cache, no-store, must-revalidate"
```

#AssumeRole with AWS STS

Assuming cross-account deployment roles securely:

```bash
# Assume production deployment role
CREDENTIALS=$(aws sts assume-role \
  --role-arn "arn:aws:iam::123456789012:role/ProductionDeployerRole" \
  --role-session-name "CICDDeploySession" \
  --output json)

export AWS_ACCESS_KEY_ID=$(echo $CREDENTIALS | jq -r .Credentials.AccessKeyId)
export AWS_SECRET_ACCESS_KEY=$(echo $CREDENTIALS | jq -r .Credentials.SecretAccessKey)
export AWS_SESSION_TOKEN=$(echo $CREDENTIALS | jq -r .Credentials.SessionToken)
```

## Common Patterns

### Advanced JMESPath Filtering and Table Formatting

**Problem**: Inspecting hundreds of EC2 instances or S3 buckets returns overwhelming JSON output.

**Solution**:
Use `--query` with JMESPath projections:

```bash
# Extract running instance IDs, types, and private IPs into a clean table
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query "Reservations[].Instances[].[InstanceId, InstanceType, PrivateIpAddress, Tags[?Key=='Name'].Value | [0]]" \
  --output table
```

## Best Practices (2026)

- **Do** target AWS CLI v2 (`aws --version`) which includes native SSO and Pager integration.
- **Do** use `--query` (JMESPath) for client-side filtering and `--filters` for server-side filtering.
- **Do** configure AWS IAM Identity Center (`aws configure sso`) instead of long-lived access keys.
- **Do** disable paging in automated shell scripts by setting `export AWS_PAGER=""`.
- **Don't** commit `~/.aws/credentials` or access keys to Git repositories.
- **Don't** use `aws s3 cp` in loops for multi-file transfers; use `aws s3 sync` for automated diffing.
- **Don't** parse AWS CLI JSON output with brittle `grep` or `awk`; use `--output text` with `--query` or `jq`.

## Troubleshooting

| Error                                         | Cause                                                                 | Solution                                                              |
| :-------------------------------------------- | :-------------------------------------------------------------------- | :-------------------------------------------------------------------- |
| `The config profile (...) could not be found` | Profile name not declared in `~/.aws/config` or `~/.aws/credentials`. | Run `aws configure --profile <name>` or verify `AWS_PROFILE` env var. |
| `An error occurred (RequestLimitExceeded)`    | Script calling AWS CLI in a tight loop without rate limiting.         | Add sleep delays or use AWS SDK with exponential backoff.             |
| `Invalid value for --query: Syntax error`     | JMESPath query has unescaped quotes or invalid projection syntax.     | Test query string incrementally: start with `Reservations[0]`.        |

## References

- [AWS CLI Documentation](https://aws.amazon.com/cli/)
