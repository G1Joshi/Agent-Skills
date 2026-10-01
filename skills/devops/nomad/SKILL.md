---
name: nomad
description: Expert HashiCorp Nomad assistance covering job specifications (HCL), task drivers (Docker, exec), scheduling, and scaling. Use when running containers and non-containerized legacy apps with minimal operational overhead.
---

# Nomad

HashiCorp Nomad is a lightweight, flexible workload orchestrator capable of managing containerized, non-containerized, and virtualized applications across bare metal and multi-cloud environments.

## When to Use

- **Simple & Flexible Workload Orchestration**: Deploying containers, non-containerized binaries, and batch jobs across clouds and bare metal.
- **Lightweight Alternative to Kubernetes**: Single-binary cluster management with significantly lower operational complexity.
- **HashiCorp Ecosystem Integration**: Native interoperability with Consul (service discovery) and Vault (secret management).
- **Hybrid Multi-Region Workloads**: Scheduling Windows and Linux jobs seamlessly across distributed datacenters.

## Quick Start

```hcl
job "example" {
  datacenters = ["dc1"]

  group "cache" {
    task "redis" {
      driver = "docker"

      config {
        image = "redis:7"
      }

      resources {
        cpu    = 500 # 500 MHz
        memory = 256 # 256 MB
      }
    }
  }
}
```

## Core Concepts

### Production Job Specification (job.nomad)

Deploying a containerized service with Consul and Vault:

```hcl
job "api-service" {
  datacenters = ["dc1"]
  type        = "service"

  group "web" {
    count = 3

    update {
      max_parallel     = 1
      min_healthy_time = "30s"
      healthy_deadline = "3m"
      auto_revert      = true # Automatic rollback on deployment failure
    }

    network {
      port "http" {
        to = 8080
      }
    }

    service {
      name     = "api-service"
      port     = "http"
      provider = "consul"

      check {
        type     = "http"
        path     = "/healthz"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "server" {
      driver = "docker"

      config {
        image = "registry.example.com/api-service:v2.1.0"
        ports = ["http"]
      }

      resources {
        cpu    = 500 # MHz
        memory = 512 # MB
      }

      vault {
        policies = ["api-service-policy"]
      }

      template {
        data        = "DATABASE_URL={{ with secret \"secret/data/db\" }}{{ .Data.data.url }}{{ end }}"
        destination = "secrets/file.env"
        env         = true
      }
    }
  }
}
```

### Batch Job Scheduling for Cron and Analytics

Running one-off or scheduled batch computation:

```hcl
job "nightly-cleanup" {
  datacenters = ["dc1"]
  type        = "batch"

  periodic {
    cron             = "0 2 * * *" # Daily at 2 AM
    prohibit_overlap = true
  }

  group "cleanup" {
    task "run-cleanup" {
      driver = "docker"
      config {
        image   = "myregistry/cleanup-task:latest"
        command = ["python", "cleanup.py"]
      }
    }
  }
}
```

### Nomad CLI Operations

Planning and deploying jobs from terminal:

```bash
# Preview allocation changes before deploying
nomad job plan job.nomad

# Run job with dry-run verification
nomad job run job.nomad

# Inspect running job allocations and status
nomad job status api-service
nomad alloc logs -f <ALLOC_ID>
```

## Common Patterns

### Production Docker Job Specification

**Problem**: Need container orchestration without the operational complexity of Kubernetes.

**Solution**:
Define Nomad job with resource limits and service registration:

```hcl
job "api-service" {
  datacenters = ["dc1"]
  type        = "service"

  group "web" {
    count = 3

    network {
      port "http" {
        to = 8080
      }
    }

    service {
      name = "api"
      port = "http"
      check {
        type     = "http"
        path     = "/health"
        interval = "10s"
        timeout  = "2s"
      }
    }

    task "server" {
      driver = "docker"
      config {
        image = "myorg/api:latest"
        ports = ["http"]
      }
      resources {
        cpu    = 500
        memory = 256
      }
    }
  }
}
```

## Best Practices

**Do**:

- Always run `nomad job plan` to inspect allocation changes and dry-run outputs before updating jobs.
- Set `auto_revert = true` in update blocks to trigger automated rollbacks when health checks fail.
- Leverage Nomad's native Vault and Consul integrations for secret rendering and service discovery.
- Deploy an odd number of server nodes (3 or 5) for Raft consensus across availability zones.

**Don't**:

- Allocate unbounded resources; always specify explicit `cpu` and `memory` limits in task definitions.
- Store plaintext passwords in job files; use the `template` block with Vault secrets.
- Run Nomad servers without TLS and mutual authentication enabled.

## Troubleshooting

| Error                                                     | Cause                                                                   | Solution                                                                    |
| :-------------------------------------------------------- | :---------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `Job placement failed: 0/N nodes available`               | No cluster nodes have enough free CPU, memory, or matching constraints. | Scale nomad client nodes or reduce job resource allocations.                |
| `Task failed: driver "docker" failed to create container` | Docker daemon unreachable or image pull failure on client node.         | Verify Docker service status on client node and check registry credentials. |
| `No cluster leader`                                       | Nomad servers cannot achieve quorum.                                    | Verify network connectivity on port 4648 and ensure odd number of servers.  |

## References

- [Nomad Documentation](https://developer.hashicorp.com/nomad)
