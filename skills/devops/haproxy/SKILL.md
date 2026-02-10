---
name: haproxy
description: HAProxy load balancer and proxy. Use for high-availability.
---

# HAProxy

HAProxy is the standard for high-performance load balancing. HAProxy 3.0 (2025) adds **Syslog Load Balancing** and improved HTTP/3 QUIC support.

## When to Use

- **High Traffic**: Handling millions of requests per second.
- **L4 Balancing**: TCP proxying for Database replicas, Redis, or non-HTTP protocols.
- **Advanced Logic**: Complex ACLs, rate limiting, and sticky sessions.

## Quick Start

```haproxy
frontend http_front
   bind *:80
   default_backend web_servers

backend web_servers
   balance roundrobin
   server web1 10.0.0.1:80 check
   server web2 10.0.0.2:80 check
```

## Core Concepts

### Frontend / Backend

Frontend defines how requests enter (ports, certs). Backend defines where they go and how (algorithms, health checks).

### ACLs

Access Control Lists. Powerful conditionals.
`acl is_api path_beg /api`
`use_backend api_servers if is_api`

### Stick Tables

In-memory storage for tracking events (e.g. rate limiting by IP).

## Best Practices (2025)

**Do**:

- **Use Data Plane API**: For dynamic configuration without reloads.
- **Enable Prometheus Exporter**: Built-in metrics endpoint.
- **Tune `maxconn`**: Critical for preventing resource exhaustion.

**Don't**:

- **Don't use as Web Server**: It is a proxy. Use Nginx/Caddy for serving static files.

## References

- [HAProxy Documentation](https://www.haproxy.org/)
