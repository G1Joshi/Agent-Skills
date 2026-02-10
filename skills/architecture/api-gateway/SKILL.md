---
name: api-gateway
description: API Gateway pattern for routing. Use for microservices entry.
---

# API Gateway

An API Gateway sits between clients (Mobile, Web) and services. It acts as a reverse proxy, accepting all API calls, aggregating the various services required to fulfill them, and returning the appropriate result.

## When to Use

- **Microservices**: Essential to hide the complexity of backend services (Service Discovery).
- **Cross-Cutting Concerns**: Centralizing Authentication, SSL Termination, Rate Limiting, and Logging.
- **Protocol Translation**: Converting HTTP (Client) to gRPC (Internal).

## Core Functionality

### Routing

`GET /users` -> User Service
`GET /orders` -> Order Service

### Aggregation (BFF - Backend for Frontend)

Combining results. One request to Gateway -> Calls User Service + Order Service -> Returns combined JSON.

### Offloading

- **Auth**: Validating JWT tokens at the edge.
- **Cache**: Serving static or cached responses.

## Common Patterns

### Backend for Frontend (BFF)

Creating specific gateways for different clients (e.g., one for Mobile with small payloads, one for Web with rich payloads).

## Best Practices

**Do**:

- Use mature tools: **Kong**, **Traefik**, **AWS API Gateway**, **Nginx**.
- Implement **Rate Limiting** to prevent DoS.
- Use **Correlation IDs** for tracing requests across services.

**Don't**:

- Don't put business logic in the Gateway (It's not a service).
- Don't let it become a Single Point of Failure (High Availability is key).

## Troubleshooting

| Error                 | Cause                                 | Solution                                          |
| :-------------------- | :------------------------------------ | :------------------------------------------------ |
| `502 Bad Gateway`     | Upstream service down or unreachable. | Check internal service health and firewall rules. |
| `504 Gateway Timeout` | Upstream taking too long.             | Optimize service or increase timeout (carefully). |

## References

- [Microservices.io - API Gateway](https://microservices.io/patterns/apigateway.html)
- [Kong Gateway](https://konghq.com/)
