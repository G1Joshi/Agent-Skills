---
name: consul
description: Expert HashiCorp Consul assistance covering service discovery, health checking, service mesh (Connect), and KV configuration. Use when building resilient service discovery and microservice networking.
---

# Consul

HashiCorp Consul is a service networking solution providing service discovery, secure service mesh with mutual TLS, dynamic traffic routing, and distributed key-value storage.

## When to Use

- **Service Discovery & Health Checking**: Dynamic registration and lookup of microservices across hybrid cloud networks.
- **Service Mesh & Mutual TLS (mTLS)**: Enforcing zero-trust encryption and authorization between microservices via Envoy sidecars.
- **Distributed Key-Value Store**: Centralized runtime configuration and dynamic feature flags.
- **Multi-Datacenter Federation**: Connecting and discovering services seamlessly across multiple cloud providers and regions.

## Quick Start

```hcl
# Service registration definition: /etc/consul.d/web.hcl
service {
  name = "web-api"
  port = 8080
  tags = ["v1", "production"]

  check {
    id       = "api-health"
    name     = "HTTP Health Check"
    http     = "http://localhost:8080/health"
    interval = "10s"
    timeout  = "2s"
  }
}
```

Reload Consul agent:

```bash
consul reload
```

## Core Concepts

### Declarative Service Registration with Health Checks

Registering a service with Consul agent:

```hcl
# /etc/consul.d/web-service.hcl
service {
  name = "payment-api"
  id   = "payment-api-01"
  port = 8080
  tags = ["v2", "production", "traefik.enable=true"]

  meta = {
    version = "2.1.0"
    owner   = "fintech-team"
  }

  check {
    id       = "payment-api-health"
    name     = "HTTP Health Check on Port 8080"
    http     = "http://127.0.0.1:8080/healthz"
    method   = "GET"
    interval = "10s"
    timeout  = "2s"

    # Automatically deregister dead instances after 5 minutes
    deregister_critical_service_after = "5m"
  }

  connect {
    sidecar_service {}
  }
}
```

### Service Discovery via DNS & HTTP API

Querying healthy service instances dynamically:

```bash
# Query healthy nodes via Consul DNS interface (port 8600)
dig @127.0.0.1 -p 8600 payment-api.service.consul SRV

# Query healthy instances via HTTP REST API
curl -s http://127.0.0.1:8500/v1/health/service/payment-api?passing=true | jq .
```

### Consul KV Configuration & Watchers with Consul-Template

Dynamic template rendering when configuration keys change:

```text
# nginx.ctmpl
upstream backend {
{{- range service "payment-api" }}
  server {{ .Address }}:{{ .Port }};
{{- end }}
}
```

```bash
# Automatically reload Nginx when Consul services or keys mutate
consul-template -template "nginx.ctmpl:/etc/nginx/conf.d/upstream.conf:systemctl reload nginx"
```

## Common Patterns

### Dynamic Configuration Watching with Consul Template

**Problem**: Nginx or HAProxy configurations must be dynamically updated whenever backend nodes scale up or down.

**Solution**:
Use Consul Template to re-render config files and reload services:

```text
# nginx.ctmpl
upstream app_servers {
{{ range service "web-api" }}
    server {{ .Address }}:{{ .Port }};
{{ else }}
    server 127.0.0.1:8080 backup;
{{ end }}
}
```

Run daemon: `consul-template -template "nginx.ctmpl:/etc/nginx/conf.d/upstream.conf:systemctl reload nginx"`

## Best Practices

**Do**:

- Configure `deregister_critical_service_after` to automatically prune dead service nodes from discovery.
- Use Consul Service Mesh with Connect to automate mutual TLS (mTLS) zero-trust encryption between pods/VMs.
- Deploy Consul server nodes in odd numbers (3 or 5) across distinct availability zones to maintain Raft consensus.
- Enable gossip encryption and TLS for all agent-to-server and agent-to-agent communications.

**Don't**:

- Use Consul KV as a high-throughput primary application database; it is designed for configuration and coordination.
- Run production Consul servers as single nodes without a quorum.
- Expose Consul HTTP API (8500) publicly without ACL tokens and TLS.

## Troubleshooting

| Error                                         | Cause                                                                | Solution                                                                           |
| :-------------------------------------------- | :------------------------------------------------------------------- | :--------------------------------------------------------------------------------- |
| `No cluster leader`                           | Consul servers cannot achieve Raft quorum.                           | Verify odd number of servers (3 or 5) and check network connectivity on port 8300. |
| `Critical health check failing`               | Health check endpoint returning non-2xx status code.                 | Check application logs on node and test health URL manually with curl.             |
| `RPC failed to server: ACL permission denied` | Consul token lacks read/write privileges on service or KV namespace. | Grant appropriate ACL policy in token definition.                                  |

## References

- [Consul Documentation](https://developer.hashicorp.com/consul)
