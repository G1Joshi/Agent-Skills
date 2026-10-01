---
name: terraform
description: Expert HashiCorp Terraform assistance covering HCL, providers, modules, state locking, workspaces, and plan/apply workflows. Use when provisioning and managing cloud infrastructure declaratively.
---

# Terraform

HashiCorp Terraform is an Infrastructure as Code (IaC) engine allowing declarative provisioning and lifecycle management of cloud resources across multi-cloud environments using HCL.

## When to Use

- **Multi-Cloud Declarative Infrastructure as Code (IaC)**: Provisioning and managing resources across AWS, Azure, GCP, and Kubernetes.
- **State Management & Team Collaboration**: Tracking real-world cloud resources via remote state backends with locking.
- **Modular Infrastructure Architecture**: Writing reusable, version-controlled modules for standard cloud topologies.
- **Pre-Deployment Execution Planning**: Auditing infrastructure changes with `terraform plan` before applying.

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

### Modular Architecture with Remote State & Locking

Configuring S3 remote backend with DynamoDB state locking:

```hcl
# versions.tf
terraform {
  required_version = ">= 1.9.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
  }

  backend "s3" {
    bucket         = "corp-terraform-state-prod"
    key            = "platform/network/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = "CoreInfrastructure"
    }
  }
}
```

### Reusable VPC Module with Inputs & Outputs

Encapsulating network resources:

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "${var.environment}-vpc"
  }
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.environment}-public-${count.index + 1}"
  }
}

output "vpc_id" {
  description = "The ID of the provisioned VPC"
  value       = aws_vpc.main.id
}
```

### Terraform CLI Workflow

Planning and applying changes safely:

```bash
# Initialize providers and remote backend
terraform init

# Validate configuration syntax and variables
terraform validate

# Generate and save execution plan
terraform plan -out=tfplan.binary

# Apply verified plan atomically
terraform apply tfplan.binary
```

## Common Patterns

### S3 Backend with DynamoDB State Locking

**Problem**: Concurrent `terraform apply` executions from CI pipelines corrupting state files.

**Solution**:
Configure remote backend with distributed state locking:

```hcl
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

## Best Practices

**Do**:

- Always store Terraform state in a remote backend (S3/GCS) with encryption and state locking (DynamoDB).
- Always generate an execution plan (`terraform plan -out=tfplan`) and apply the saved plan file in CI.
- Use `default_tags` at the provider level to ensure consistent tagging across all cloud resources.
- Isolate environments using separate state files or directories (`environments/prod`, `environments/stage`), not workspaces.

**Don't**:

- Commit `.tfstate` files or files containing secrets to version control.
- Use `terraform apply --auto-approve` in production without review and approval gates.
- Modify cloud resources manually via web consoles; out-of-band changes cause state drift.

## Troubleshooting

| Error                                          | Cause                                                                         | Solution                                                                          |
| :--------------------------------------------- | :---------------------------------------------------------------------------- | :-------------------------------------------------------------------------------- |
| `Error: Error acquiring the state lock`        | Previous apply was interrupted, leaving lock active in DynamoDB.              | Unlock after verifying no process is running: `terraform force-unlock <LOCK-ID>`. |
| `Error: Resource already managed by Terraform` | Importing resource without configuration block or duplicate resource address. | Ensure unique resource label and run `terraform import <addr> <id>`.              |
| `Provider configuration not present`           | Module using provider configuration not inherited from parent root.           | Pass providers explicitly: `providers = { aws = aws.west }`.                      |

## References

- [Terraform Documentation](https://developer.hashicorp.com/terraform)
