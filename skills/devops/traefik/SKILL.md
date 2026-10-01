---
name: traefik
description: Expert Traefik edge router assistance covering dynamic configuration, Docker/Kubernetes providers, Let's Encrypt TLS, and middlewares. Use when building dynamic reverse proxies and microservice ingress routing.
---

# Traefik

Traefik is a modern HTTP reverse proxy and load balancer designed for microservices, featuring automatic service discovery, dynamic configuration, and Kubernetes Gateway API support.

## When to Use

- **Cloud-Native Edge Router & Reverse Proxy**: Automatically discovering and routing microservice traffic in Docker and Kubernetes.
- **Automated Let's Encrypt TLS Certificates**: Issuing and renewing SSL/TLS certificates with zero manual intervention.
- **Middleware-Based Request Transformation**: Chaining middlewares (rate limiting, auth, header manipulation, stripprefix).
- **Canary & Weighted Round Robin Routing**: Splitting traffic across service versions dynamically.

## Quick Start

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.my-app.rule=Host(`example.com`)"
  - "traefik.http.routers.my-app.entrypoints=websecure"
  - "traefik.http.routers.my-app.tls.certresolver=myresolver"
```

## Core Concepts

### Docker Compose Automatic Service Discovery

Exposing containers to Traefik via container labels:

```yaml
services:
  traefik:
    image: traefik:v3.1
    command:
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.myresolver.acme.tlschallenge=true"
      - "--certificatesresolvers.myresolver.acme.email=admin@example.com"
      - "--certificatesresolvers.myresolver.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock:ro"
      - "acme_data:/letsencrypt"

  billing-api:
    image: myregistry/billing-api:v2.0
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.billing.rule=Host(`billing.example.com`)"
      - "traefik.http.routers.billing.entrypoints=websecure"
      - "traefik.http.routers.billing.tls.certresolver=myresolver"
      - "traefik.http.routers.billing.middlewares=ratelimit@docker"
      # Middleware: Rate limit 100 req/s
      - "traefik.http.middlewares.ratelimit.ratelimit.average=100"
      - "traefik.http.middlewares.ratelimit.ratelimit.burst=20"
      - "traefik.http.services.billing.loadbalancer.server.port=8080"

volumes:
  acme_data:
```

### Kubernetes IngressRoute Custom Resource (CRD)

Modern Kubernetes routing with Traefik CRDs:

```yaml
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: api-ingressroute
  namespace: default
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`api.example.com`) && PathPrefix(`/v2`)
      kind: Rule
      services:
        - name: api-service
          port: 8080
      middlewares:
        - name: stripprefix-v2
  tls:
    certResolver: myresolver
```

### Static Configuration (traefik.yml)

Core startup parameters:

```yaml
entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https

  websecure:
    address: ":443"

api:
  dashboard: true
  insecure: false
```

## Common Patterns

### Docker Labels Dynamic Routing with Rate Limiting and Automatic TLS

**Problem**: Manually updating reverse proxy configuration every time a container restarts or changes ports.

**Solution**:
Configure routing dynamically via Docker container labels:

```yaml
version: "3.8"

services:
  api:
    image: myorg/api:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.example.com`)"
      - "traefik.http.routers.api.entrypoints=websecure"
      - "traefik.http.routers.api.tls.certresolver=myresolver"
      - "traefik.http.routers.api.middlewares=api-ratelimit"
      - "traefik.http.middlewares.api-ratelimit.ratelimit.average=50"
      - "traefik.http.services.api.loadbalancer.server.port=8080"
```

## Best Practices

**Do**:

- Target Traefik v3+ with native support for HTTP/3, OpenTelemetry, and modern Kubernetes Gateway API.
- Set `--providers.docker.exposedbydefault=false` to prevent accidental public exposure of unlabelled containers.
- Persist the ACME storage file (`/letsencrypt/acme.json`) on durable volumes with `0600` file permissions.
- Configure automated HTTP-to-HTTPS redirections at the entrypoint level.

**Don't**:

- Expose the Traefik dashboard publicly without authenticating middlewares (e.g. BasicAuth or OAuth2).
- Grant read-write access to the Docker socket; mount `/var/run/docker.sock:ro` in read-only mode.
- Run Traefik in production without rate-limiting and connection-timeout middlewares.

## Troubleshooting

| Error                                 | Cause                                                                        | Solution                                                                             |
| :------------------------------------ | :--------------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| `404 Not Found on routed host`        | `Host(...)` rule does not match request header or router entrypoint missing. | Verify Host header and check Traefik dashboard (`http://localhost:8080/dashboard/`). |
| `Cannot obtain ACME certificate`      | Port 80 not reachable from internet for Let's Encrypt HTTP challenge.        | Verify DNS points to Traefik public IP and firewall allows incoming port 80.         |
| `Skipping container: port is missing` | Multiple ports exposed in Docker image without explicit `server.port` label. | Add `traefik.http.services.<name>.loadbalancer.server.port=<port>`.                  |

## References

- [Traefik Documentation](https://doc.traefik.io/traefik/)
