---
name: terraform
description: Terraform infrastructure as code with providers and state management. Use for cloud provisioning.
---

# Terraform

Infrastructure as Code for provisioning cloud resources.

## When to Use

- Multi-cloud infrastructure
- Reproducible environments
- Infrastructure versioning
- Team collaboration on infra

## Quick Start

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "WebServer"
  }
}
```

## Core Concepts

### Variables & Outputs

```hcl
# variables.tf
variable "environment" {
  type        = string
  description = "Environment name"
  default     = "dev"
}

variable "instance_config" {
  type = object({
    type  = string
    count = number
  })
  default = {
    type  = "t3.micro"
    count = 1
  }
}

# outputs.tf
output "instance_ip" {
  value       = aws_instance.web.public_ip
  description = "Public IP of the instance"
}
```

### Modules

```hcl
# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block = var.cidr_block

  tags = {
    Name        = var.name
    Environment = var.environment
  }
}

# main.tf
module "vpc" {
  source      = "./modules/vpc"
  name        = "production"
  cidr_block  = "10.0.0.0/16"
  environment = "prod"
}
```

## Common Patterns

### Remote State

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Common Commands

```bash
# Initialize
terraform init

# Plan changes
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# Destroy
terraform destroy

# Format
terraform fmt -recursive

# Validate
terraform validate
```

## Best Practices

**Do**:

- Use remote state with locking
- Use modules for reusability
- Pin provider versions
- Use workspaces for environments

**Don't**:

- Store secrets in state
- Commit .tfstate files
- Skip plan before apply
- Use hardcoded values

## Troubleshooting

| Issue          | Cause            | Solution           |
| -------------- | ---------------- | ------------------ |
| State lock     | Concurrent apply | Check/force-unlock |
| Drift detected | Manual changes   | Import or refresh  |
| Provider error | Version mismatch | Pin versions       |

## References

- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Terraform Registry](https://registry.terraform.io/)
