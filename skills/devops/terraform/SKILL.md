---
name: terraform
description: Terraform infrastructure as code with providers and state management. Use for cloud provisioning.
---

# Terraform

Terraform is the world's most popular Infrastructure as Code (IaC) tool. It uses HCL to provision resources on any cloud. 2025 introduces **Terraform Stacks** for easier component management.

## When to Use

- **Provisioning**: Creating VPCs, Databases, K8s Clusters.
- **Multi-Cloud**: Learn one syntax (HCL), use it for AWS, Azure, GCP, Datadog, etc.
- **State Management**: It tracks resource state, allowing "Plan" (preview) and "Apply".

## Quick Start

```hcl
# main.tf
provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "b" {
  bucket = "my-tf-test-bucket"
  tags = {
    Name = "My bucket"
  }
}
```

## Core Concepts

### Providers

Plugins that talk to APIs (AWS, Azure, Kubernetes).

### State

`terraform.tfstate`. The source of truth mapping your code to real-world resource IDs. Must be stored remotely (S3 + DynamoDB Locking) in teams.

### Stacks (2025)

A new layer above Modules. Allows defined dependencies between deployments (e.g., Deploy VPC, _then_ Deploy K8s using VPC ID output).

## Best Practices (2025)

**Do**:

- **Use Remote State**: S3 backend or Terraform Cloud. Never local state.
- **Use Modules**: DRY. Write a "Company Standard Bucket" module and reuse it.
- **Use `tfsec` / `trivy`**: Scan HCL for misconfigurations (open security groups) before deploy.

**Don't**:

- **Don't hardcode secrets**: Use `variable "db_password" {}` and pass it via `TF_VAR_` or a secret manager.

## References

- [Terraform Documentation](https://developer.hashicorp.com/terraform)
