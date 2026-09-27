---
name: haproxy
description: Expert HAProxy load balancer assistance covering Layer 4 / Layer 7 routing, health checks, SSL termination, and rate limiting. Use when building high-availability, low-latency traffic proxies.
---

# HAProxy

HAProxy is the standard for high-performance load balancing. HAProxy 3.0 (2025) adds **Syslog Load Balancing** and improved HTTP/3 QUIC support.

## When to Use

- **High-Performance Layer 4 & Layer 7 Load Balancing**: Distributing millions of concurrent TCP/HTTP connections with low CPU overhead.
- **TLS Termination & SSL Offloading**: Offloading cryptographic handshakes at the edge before proxying to backend servers.
- **Advanced Rate Limiting & Stick Tables**: Tracking client IPs across sliding time windows to neutralize DDoS and brute force.
- **Health Checking & Circuit Breaking**: Detecting unhealthy backend servers and rerouting traffic instantaneously.

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

#Production HTTP Load Balancer Configuration

Configuring frontend and backend pools with health checks:

```haproxy
# /etc/haproxy/haproxy.cfg
global
    log /dev/log local0
    maxconn 50000
    user haproxy
    group haproxy
    daemon
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384
    ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000ms
    timeout client  50000ms
    timeout server  50000ms

frontend http_front
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/example.com.pem alpn h2,http/1.1
    redirect scheme https code 301 if !{ ssl_fc }

    # Rate limiting stick-table: 100 requests per 10 seconds per IP
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 100 }

    default_backend web_cluster

backend web_cluster
    balance roundrobin
    option httpchk GET /healthz
    http-check expect status 200
    cookie SERVERID insert indirect nocache

    server web1 10.0.1.10:8080 check cookie web1 fall 3 rise 2
    server web2 10.0.1.11:8080 check cookie web2 fall 3 rise 2
```

#TCP Layer 4 Load Balancing (Database Proxy)

Distributing MySQL or PostgreSQL connections across read replicas:

```haproxy
frontend db_in
    bind *:5432
    mode tcp
    option tcplog
    default_backend db_replicas

backend db_replicas
    mode tcp
    balance leastconn
    option tcp-check
    server db-replica-1 10.0.2.20:5432 check
    server db-replica-2 10.0.2.21:5432 check
```

#Statistics Dashboard Configuration

Enabling real-time traffic monitoring interface:

```haproxy
listen stats
    bind *:8404
    mode http
    stats enable
    stats uri /
    stats refresh 5s
    stats auth admin:SuperSecretPassword2026
```

## Common Patterns

### Layer 7 Round-Robin Backend with Active Health Checks

**Problem**: Distributing web traffic across backend workers while automatically evicting degraded instances.

**Solution**:
Configure `haproxy.cfg` frontend and backend:

```haproxy
frontend http_front
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/site.pem
    redirect scheme https if !{ ssl_fc }
    default_backend web_servers

backend web_servers
    balance roundrobin
    cookie SERVERID insert indirect nocache
    option httpchk GET /health
    http-check expect status 200
    server app01 10.0.0.10:8080 check cookie app01
    server app02 10.0.0.11:8080 check cookie app02
```

## Best Practices (2026)

- **Do** test HAProxy configuration files (`haproxy -c -f /etc/haproxy/haproxy.cfg`) before reloading.
- **Do** use `balance leastconn` for long-running connections (WebSockets, database pools) and `roundrobin` for short HTTP APIs.
- **Do** configure `stick-table` to defend endpoints against brute-force attacks and volumetric DDoS.
- **Do** configure `option httpchk` to verify that application backends are genuinely healthy before routing traffic.
- **Don't** run HAProxy with single-threaded defaults on multi-core servers; configure `nbthread` or multi-threading.
- **Don't** leave stats dashboards accessible without authentication or IP restrictions.
- **Don't** set excessively low client/server timeouts that sever legitimate long-polling or file upload connections.

## Troubleshooting

| Error                                                                    | Cause                                              | Solution                                                               |
| :----------------------------------------------------------------------- | :------------------------------------------------- | :--------------------------------------------------------------------- |
| `[ALERT] 085/120000 : parsing [haproxy.cfg:20] : syntax error`           | Indentation or syntax error in configuration line. | Run `haproxy -c -f /etc/haproxy/haproxy.cfg` to validate syntax.       |
| `503 Service Unavailable: No server is available to handle this request` | All backend servers failed health checks.          | Check backend server health logs and verify `option httpchk` endpoint. |
| `Cannot bind socket [0.0.0.0:80]`                                        | Port 80 bound by another service.                  | Kill conflicting service or configure HAProxy on custom port.          |

## References

- [HAProxy Documentation](https://www.haproxy.org/)
