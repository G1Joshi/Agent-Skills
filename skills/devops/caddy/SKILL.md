---
name: caddy
description: Expert Caddy web server assistance covering automatic HTTPS, Caddyfile configuration, reverse proxying, and load balancing. Use when deploying modern, zero-config HTTPS web servers.
---

# Caddy

Caddy 2 is a powerful, enterprise-ready web server with **automatic HTTPS** by default. v2.8 (2025) improves **HTTP/3** performance and certificate management.

## When to Use

- **Automated TLS & Reverse Proxying**: Instant HTTPS certificates issued via Let's Encrypt / ZeroSSL with zero manual setup.
- **Modern Microservice Edge Proxy**: HTTP/2 and HTTP/3 reverse proxying with clean, human-readable Caddyfiles.
- **Local Development HTTPS**: Issuing trusted local root certificates automatically for development environments.
- **Zero-Downtime Hot Reloading**: Updating configurations via REST API or `caddy reload` without dropping connections.

## Quick Start

```caddyfile
# Caddyfile
example.com {
    reverse_proxy localhost:3000
    encode zstd gzip
    file_server
}
```

## Core Concepts

#Production Reverse Proxy Caddyfile with Security Headers

Clean reverse proxy configuration with automatic HTTPS:

```caddyfile
# /etc/caddy/Caddyfile
api.example.com {
    # Automatic TLS enabled by default!

    # Reverse proxy to backend application cluster
    reverse_proxy 127.0.0.1:8080 {
        header_up Host {host}
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-Proto {scheme}

        # Health checks and failover
        lb_policy round_robin
        health_path /healthz
        health_interval 10s
    }

    # Security headers
    header {
        Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        -Server # Remove server fingerprint header
    }

    # Structured JSON access logging
    log {
        output file /var/log/caddy/access.log {
            roll_size 50mb
            roll_keep 10
        }
        format json
    }
}
```

#Static File Server with Gzip & Zstandard Compression

Serving high-performance frontends with fallback for Single Page Apps (SPAs):

```caddyfile
app.example.com {
    root * /var/www/app/dist
    encode zstd gzip

    # SPA routing: try file, then fallback to index.html
    try_files {path} /index.html
    file_server
}
```

#Live Configuration Updates via Admin API

Modifying configuration dynamically without server restarts:

```bash
# Validate Caddyfile syntax
caddy validate --config /etc/caddy/Caddyfile

# Zero-downtime configuration reload
caddy reload --config /etc/caddy/Caddyfile

# Query current running config via Admin API
curl http://localhost:2019/config/ | jq .
```

## Common Patterns

### Reverse Proxy with Automated Let's Encrypt and Security Headers

**Problem**: Tedious manual SSL certificate provisioning, renewal cron jobs, and complex Nginx configs.

**Solution**:
Use Caddy's declarative Caddyfile:

```caddyfile
api.example.com {
    # Automatic HTTPS via Let's Encrypt / ZeroSSL

    # Security headers
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
    }

    # Reverse proxy to internal microservice
    reverse_proxy 127.0.0.1:8080 {
        health_uri /health
        health_interval 10s
    }
}
```

## Best Practices (2026)

- **Do** use `encode zstd gzip` on static routes to reduce bandwidth and speed up client loading.
- **Do** use `try_files {path} /index.html` for client-side Single Page Application (SPA) routing.
- **Do** test configuration files with `caddy validate` before reloading in production pipelines.
- **Do** configure structured JSON logging with automated log rolling.
- **Don't** expose Caddy's internal Admin API port (`2019`) to public network interfaces.
- **Don't** use Caddy without persistent storage volumes for `/data` in containers; certificates will be re-requested on restart.
- **Don't** disable automatic HTTPS (`http://`) unless strictly operating behind an external cloud load balancer.

## Troubleshooting

| Error                                           | Cause                                                                       | Solution                                                                      |
| :---------------------------------------------- | :-------------------------------------------------------------------------- | :---------------------------------------------------------------------------- |
| `certificate obtained error: acme: error: 400`  | Domain DNS A/AAAA record does not point to Caddy server IP.                 | Verify DNS propagation and ensure ports 80 and 443 are reachable.             |
| `caddy.service: Failed with result 'exit-code'` | Syntax error in `/etc/caddy/Caddyfile`.                                     | Run `caddy validate --config /etc/caddy/Caddyfile` to identify syntax errors. |
| `502 Bad Gateway`                               | Upstream service port down or listening on localhost only inside container. | Verify upstream service is active: `curl http://127.0.0.1:8080`.              |

## References

- [Caddy Documentation](https://caddyserver.com/docs/)
