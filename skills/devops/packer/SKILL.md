---
name: packer
description: Expert HashiCorp Packer assistance covering HCL2 templates, builders (AWS AMI, GCP, Azure, Docker), and provisioners. Use when automating immutable machine image creation for cloud and virtualization.
---

# Packer

HashiCorp Packer automates the generation of identical machine images across multiple cloud providers and hypervisors from a single declarative HCL configuration.

## When to Use

- **Automated Golden Image Creation**: Building standardized, hardened virtual machine images across AWS AMIs, Azure VMs, and GCP.
- **Immutable Infrastructure Pipelines**: Pre-baking operating systems, security patches, and application runtimes into images.
- **Multi-Cloud Image Synchronization**: Generating identical VM images for multiple clouds from a single HCL template.
- **Compliance & Security Hardening**: Running CIS benchmark Ansible playbooks during image build pipelines.

## Quick Start

```hcl
source "amazon-ebs" "ubuntu" {
  ami_name      = "my-app-{{timestamp}}"
  instance_type = "t3.micro"
  region        = "us-west-2"
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/*ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"] # Canonical
  }
  ssh_username = "ubuntu"
}

build {
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    inline = ["sudo apt-get update", "sudo apt-get install -y nginx"]
  }
}
```

## Core Concepts

### Modern HCL2 Template for AWS Golden AMI

Building an encrypted, hardened Ubuntu AMI:

```hcl
# ubuntu_ami.pkr.hcl
packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

source "amazon-ebs" "hardened_ubuntu" {
  ami_name      = "golden-ubuntu-24-04-{{timestamp}}"
  instance_type = "t3.medium"
  region        = var.aws_region
  encrypt_boot  = true

  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"] # Canonical
  }

  ssh_username = "ubuntu"
  tags = {
    OS          = "Ubuntu 24.04"
    Environment = "Golden-Images"
    BuildTime   = "{{timestamp}}"
  }
}

build {
  sources = ["source.amazon-ebs.hardened_ubuntu"]

  # Step 1: Update and install security packages
  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get upgrade -y",
      "sudo apt-get install -y fail2ban ufw unattended-upgrades"
    ]
  }

  # Step 2: Apply Ansible hardening playbook
  provisioner "ansible" {
    playbook_file = "./playbooks/cis_hardening.yml"
  }
}
```

### Validating, Formatting and Building Images

Executing Packer CLI build workflow:

```bash
# Format template
packer fmt ubuntu_ami.pkr.hcl

# Validate template syntax and credentials
packer validate ubuntu_ami.pkr.hcl

# Build golden AMI with variable override
packer build -var "aws_region=us-east-1" ubuntu_ami.pkr.hcl
```

## Common Patterns

### Automated AWS AMI Builder with Shell Provisioning

**Problem**: Manual server hardening creates configuration drift and slow auto-scaling boot times.

**Solution**:
Build pre-baked immutable AMIs with Packer HCL2:

```hcl
packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.0"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "ubuntu" {
  ami_name      = "hardened-ubuntu-24-04-{{timestamp}}"
  instance_type = "t3.small"
  region        = "us-east-1"
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd/ubuntu-noble-24.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"]
  }
  ssh_username = "ubuntu"
}

build {
  sources = ["source.amazon-ebs.ubuntu"]
  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y docker.io nginx",
      "sudo systemctl enable docker"
    ]
  }
}
```

## Best Practices

**Do**:

- Target modern HCL2 templates (`.pkr.hcl`) instead of legacy deprecated JSON Packer templates.
- Set `encrypt_boot = true` on EBS volumes to ensure golden images are encrypted at rest with KMS.
- Use `source_ami_filter` with `most_recent = true` and official owner IDs to build on verified vendor base images.
- Clean up temporary shell history and SSH host keys before the image is finalized.

**Don't**:

- Bake sensitive production secrets or private API tokens into golden images; inject secrets at runtime.
- Leave default administrative passwords set in base images.
- Run Packer without `packer validate` in continuous integration builds.

## Troubleshooting

| Error                                               | Cause                                                                             | Solution                                                       |
| :-------------------------------------------------- | :-------------------------------------------------------------------------------- | :------------------------------------------------------------- |
| `Error: Timeout waiting for SSH`                    | Security group blocks port 22 or SSH key pair mismatch during build.              | Verify subnet has public IP assignment and allows inbound SSH. |
| `Failed to initialize plugins`                      | Required plugin not installed on host.                                            | Run `packer init <config.pkr.hcl>` before executing build.     |
| `Amazon Elastic Block Store: UnauthorizedOperation` | IAM role running Packer lacks permissions to create EC2 keys, instances, or AMIs. | Grant required EC2 permissions in AWS IAM policy.              |

## References

- [Packer Documentation](https://developer.hashicorp.com/packer)
