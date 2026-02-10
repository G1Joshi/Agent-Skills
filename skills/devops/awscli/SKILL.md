---
name: awscli
description: AWS CLI command-line interface. Use for AWS automation.
---

# AWS CLI

The AWS CLI allows you to control AWS services from the command line. In 2025, usage is centered around **AWS IAM Identity Center** (formerly SSO) for secure, short-lived credentials.

## When to Use

- **Scripting**: Automate S3 uploads (`aws s3 sync`).
- **DevOps**: Debugging permissions or inspecting resources without the Console UI.
- **CI/CD**: Deploying CloudFormation/CDK stacks (though specialized tools are often better).

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

### Profiles

Managed in `~/.aws/config`. Allow switching between Prod, Staging, and Dev accounts easily.
`export AWS_PROFILE=prod`

### Query (`--query`)

Built-in JMESPath filtering. Use it instead of piping to `jq` for simple lookups.
`aws ec2 describe-instances --query "Reservations[*].Instances[*].PublicIpAddress"`

### S3 Web Viewer

`aws s3 presign s3://my-bucket/file.txt` generates a temporary public URL.

## Best Practices (2025)

**Do**:

- **Use AWS SSO**: Stop using long-lived `aws_access_key_id` CSVs. They are the #1 cause of hacks.
- **Use `aws-vault`**: If you _must_ use keys, wrap them in `aws-vault` to store them in the OS keychain.
- **Update v2**: Ensure you are on v2.x. v1 is deprecated.

**Don't**:

- **Don't parse text output**: Always use `--output json` and a parser (`jq` or `--query`). Text output format changes.

## References

- [AWS CLI Documentation](https://aws.amazon.com/cli/)
