---
name: linode
description: Expert Akamai Linode cloud assistance covering Compute Instances, NodeBalancers, Block Storage, LKE (Kubernetes), and CLI automation. Use when deploying cost-effective Linux cloud infrastructure.
---

# Linode (Akamai Connected Cloud)

Now part of Akamai, Linode combines simple cloud computing with a massive edge network. 2025 focuses on **Distributed Compute** – running workloads closer to users.

## When to Use

- **Cost-Effective Cloud Compute (Akamai Cloud)**: Reliable, straightforward Linux virtual machines (Nanodes to High-Memory instances).
- **Linode Kubernetes Engine (LKE)**: Fully managed Kubernetes clusters with zero control-plane fee.
- **NodeBalancers & Object Storage**: Highly available layer 4/7 load balancers and S3-compatible bucket storage.
- **Akamai Global Edge Integration**: Combining compute with Akamai CDN and edge security services.

## Quick Start

```bash
# Configure Linode CLI
linode-cli configure

# Create Linode 2GB instance with Ubuntu 24.04
linode-cli linodes create \
  --type g6-standard-1 \
  --region us-east \
  --image linode/ubuntu24.04 \
  --label web-server-01 \
  --root_pass "$ROOT_PASSWORD"
```

## Core Concepts

#Infrastructure as Code with Terraform (Linode Provider)

Deploying a Linode instance with private networking:

```hcl
terraform {
  required_providers {
    linode = {
      source  = "linode/linode"
      version = "~> 2.15"
    }
  }
}

provider "linode" {
  token = var.linode_token
}

resource "linode_instance" "web_node" {
  label           = "production-web-01"
  image           = "linode/ubuntu24.04"
  region          = "us-east"
  type            = "g6-standard-2"
  authorized_keys = [var.ssh_public_key]
  tags            = ["production", "web"]

  private_ip = true
}

resource "linode_firewall" "web_firewall" {
  label = "web-node-firewall"

  inbound {
    label    = "allow-https"
    action   = "ACCEPT"
    protocol = "TCP"
    ports    = "443"
    ipv4     = ["0.0.0.0/0"]
  }

  inbound {
    label    = "allow-ssh"
    action   = "ACCEPT"
    protocol = "TCP"
    ports    = "22"
    ipv4     = ["198.51.100.0/24"] # Trusted office VPN only
  }

  inbound_policy  = "DROP"
  outbound_policy = "ACCEPT"
  linodes         = [linode_instance.web_node.id]
}
```

#Linode Kubernetes Engine (LKE) Provisioning via CLI

Creating an autoscaling Kubernetes cluster:

```bash
# Authenticate Linode CLI
linode-cli configure

# Create a managed LKE cluster
linode-cli lke cluster-create \
  --label prod-cluster \
  --region us-east \
  --k8s_version 1.30 \
  --node_pools.type g6-standard-2 \
  --node_pools.count 3 \
  --node_pools.autoscaler.enabled true \
  --node_pools.autoscaler.min 3 \
  --node_pools.autoscaler.max 8
```

#NodeBalancer Configuration for High Availability

Distributing traffic across backend nodes:

```bash
# Create NodeBalancer and HTTPS port 443 configuration
linode-cli nodebalancers create --region us-east --label prod-lb
linode-cli nodebalancers config-create <NB_ID> \
  --port 443 --protocol https --ssl_cert "$CERT" --ssl_key "$KEY" \
  --check http --check_path /healthz --check_interval 10
```

## Common Patterns

### NodeBalancer with SSL Termination

**Problem**: Distributing traffic across multiple compute instances with high availability and SSL offloading.

**Solution**:
Configure Linode NodeBalancer via CLI:

```bash
# Create NodeBalancer
NB_ID=$(linode-cli nodebalancers create --region us-east --label app-balancer --json | jq '.[0].id')

# Add HTTPS port 443 configuration
linode-cli nodebalancers configs-create $NB_ID \
  --port 443 \
  --protocol https \
  --ssl_cert "$CERT_PEM" \
  --ssl_key "$KEY_PEM" \
  --check_path "/health"
```

## Best Practices (2026)

- **Do** attach a Cloud Firewall to all Linode instances; drop all unsolicited inbound traffic by default.
- **Do** enable `private_ip = true` and use Linode VPC for private inter-node communication.
- **Do** leverage LKE (Linode Kubernetes Engine) for production containers; control planes are completely free.
- **Do** store automated database and system backups using Linode Backup Service or Object Storage.
- **Don't** expose SSH (port 22) publicly to `0.0.0.0/0`; restrict to known IP ranges or a bastion host.
- **Don't** use root passwords for instances; always inject authorized SSH keys during provisioning.
- **Don't** hardcode Linode API tokens in source code; supply via `LINODE_TOKEN` environment variable.

## Troubleshooting

| Error                                   | Cause                                                                  | Solution                                                                    |
| :-------------------------------------- | :--------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `Authentication failed / Token invalid` | Expired or incorrect Linode personal access token.                     | Re-generate token in Cloud Manager and run `linode-cli configure`.          |
| `Cannot connect to instance via SSH`    | Root password not set or instance still in booting/provisioning state. | Monitor job state with `linode-cli linodes list` until status is `running`. |
| `Disk space full on root volume`        | Logs or temp files filling small standard disk allocation.             | Resize disk volume in Cloud Manager or attach Linode Block Storage.         |

## References

- [Linode Documentation](https://www.linode.com/docs/)
