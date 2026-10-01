---
name: api-gateway
description: Expert API Gateway architecture assistance covering reverse proxies, request routing, rate limiting, authentication offloading, and SSL termination. Use when designing API gateways, configuring Kong/Envoy/Traefik, securing microservice entrypoints, or managing edge routing.
---

# API Gateway

An API Gateway sits between clients (Mobile, Web) and services. It acts as a reverse proxy, accepting all API calls, aggregating the various services required to fulfill them, and returning the appropriate result.

## When to Use

- **Microservices Perimeter Security**: Centralizing authentication, rate limiting, and TLS termination before routing to private internal services.
- **Edge Request Routing & Transformation**: Rewriting URLs, transforming headers, and routing traffic dynamically to versioned upstream clusters.
- **Cross-Cutting Policy Enforcement**: Implementing uniform CORS, payload size limits, and audit logging across heterogeneous backend services.
- **API Modernization**: Facading legacy enterprise backends with modern REST/JSON or GraphQL interfaces without modifying existing codebases.

## Quick Start

```yaml
# Minimal Traefik / Envoy style API gateway routing configuration
http:
  routers:
    api-router:
      rule: "PathPrefix(`/api/v1`)"
      service: api-service
      middlewares:
        - rate-limit
        - auth-jwt
  services:
    api-service:
      loadBalancer:
        servers:
          - url: "http://user-service:8080"
          - url: "http://order-service:8081"
```

## Core Concepts

### Reverse Proxy & Dynamic Upstream Routing

The gateway accepts client requests and transparently forwards them to healthy backend upstream instances using dynamic discovery:

```yaml
# Envoy Gateway HTTPRoute configuration
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: billing-service-route
spec:
  parentRefs:
    - name: public-gateway
  rules:
    - matches:
        - path: { type: PathPrefix, value: /api/v1/billing }
      backendRefs:
        - name: billing-svc
          port: 8080
          weight: 90
        - name: billing-canary-svc
          port: 8080
          weight: 10
```

### Edge Authentication Offloading (JWT Validation)

Validates incoming bearer tokens and injects verified claims as internal headers, sparing internal microservices from repeating OAuth handshake verification:

```yaml
# Kong / Traefik JWT Verification Plugin
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: jwt-auth-validator
plugin: jwt
config:
  claims_to_verify:
    - exp
  key_claim_name: iss
```

### Distributed Rate Limiting & Quota Management

Protects downstream clusters from cascading overloads using sliding window or token bucket algorithms backed by Redis:

```typescript
// Fastify / Express Gateway sliding window limiter
import rateLimit from "@fastify/rate-limit";

await fastify.register(rateLimit, {
  max: 100,
  timeWindow: "1 minute",
  redis: redisClient,
  keyGenerator: (req) => (req.headers["x-api-key"] as string) || req.ip,
});
```

## Common Patterns

### Rate Limiting and Token Bucket Filter

**Problem**: Public endpoints are vulnerable to DoS attacks and noisy-neighbor quota exhaustion.  
**Solution**: Enforce rate limiting at gateway layer before requests reach downstream services.

```yaml
# Envoy Gateway rate limit configuration
apiVersion: gateway.envoyproxy.io/v1alpha1
kind: RateLimitFilter
metadata:
  name: global-api-rate-limit
spec:
  rules:
    - clientSelectors:
        - headers:
            - name: "X-API-Key"
      limit:
        requests: 100
        unit: Minute
```

### Request Decoupling and Token Exchange

**Problem**: Downstream microservices shouldn't handle public OAuth token exchanges and TLS termination.  
**Solution**:
Gateway validates public JWT and attaches internal user headers (`X-User-Id`, `X-User-Roles`):

```yaml
# Kong request-transformer plugin: attaches internal headers after validating JWT
apiVersion: configuration.konghq.com/v1
kind: KongPlugin
metadata:
  name: token-exchange-transformer
plugin: request-transformer
config:
  add:
    headers:
      - "X-User-Id:$(jwt_claims.sub)"
      - "X-User-Roles:$(jwt_claims.roles)"
```

## Best Practices

**Do**:

- Terminate TLS at the Edge: Free downstream microservices from CPU-intensive cryptographic handshakes.
- Propagate Distributed Tracing Headers: Forward `traceparent` (W3C standard) to correlate end-to-end logs across microservice hops.
- Implement Health Checks & Timeouts: Enforce aggressive connection and read timeouts on upstream routes to prevent gateway thread exhaustion.
- Use Canary Deployments: Route small percentages (5-10%) of traffic to canary versions via gateway weight configurations.

**Don't**:

- Embed heavy business logic in the Gateway: Keep the gateway thin; do not perform database queries or domain computations at the edge.
- Expose raw internal errors to clients: Sanitize upstream 500 stack traces and return RFC 7807 `ProblemDetails` JSON.
- Ignore DDoS protection: Pair the software API gateway with a cloud CDN / WAF (Cloudflare, AWS CloudFront/Shield).

## Troubleshooting

| Error                 | Cause                                 | Solution                                          |
| :-------------------- | :------------------------------------ | :------------------------------------------------ |
| `502 Bad Gateway`     | Upstream service down or unreachable. | Check internal service health and firewall rules. |
| `504 Gateway Timeout` | Upstream taking too long.             | Optimize service or increase timeout (carefully). |

## References

- [Microservices.io - API Gateway](https://microservices.io/patterns/apigateway.html)
- [Kong Gateway](https://konghq.com/)
