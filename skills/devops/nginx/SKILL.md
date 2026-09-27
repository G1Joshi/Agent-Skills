---
name: nginx
description: Expert Nginx web server assistance covering reverse proxying, load balancing, caching, SSL/TLS, and HTTP/2/3 configuration. Use when deploying high-concurrency web servers and API gateways.
---

# Nginx

Nginx is the world's most popular web server. v1.25+ (2025) supports **HTTP/3 (QUIC)** natively.

## When to Use

- **High-Performance HTTP Reverse Proxy & Web Server**: Serving millions of requests per second with an asynchronous event-driven architecture.
- **SSL/TLS Termination & HTTP/2/HTTP/3**: Offloading cryptographic handshakes and managing Let's Encrypt certificates.
- **Upstream Load Balancing & Microservice Routing**: Distributing traffic across backend clusters with keepalive connection pools.
- **Rate Limiting & DDoS Defense**: Enforcing token-bucket rate limits (`limit_req_zone`) per IP address.

## Quick Start

```nginx
# nginx.conf
server {
    listen 443 quic reuseport;
    listen 443 ssl;
    http2 on;

    server_name example.com;
    ssl_certificate cert.pem;
    ssl_certificate_key key.pem;

    location / {
        proxy_pass http://localhost:3000;
        add_header Alt-Svc 'h3=":443"; ma=86400';
    }
}
```

## Core Concepts

#Hardened Reverse Proxy Configuration with HTTP/2 and Upstream Keepalive

Production server configuration with security headers:

```nginx
# /etc/nginx/nginx.conf
user nginx;
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 8192;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Performance optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Rate limiting zone: 10MB memory, 50 requests/second per IP
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=50r/s;

    upstream backend_nodes {
        server 10.0.1.10:8080 max_fails=3 fail_timeout=10s;
        server 10.0.1.11:8080 max_fails=3 fail_timeout=10s;
        keepalive 32; # Cache up to 32 idle connections to backends
    }

    server {
        listen 443 ssl http2;
        server_name api.example.com;

        ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
        ssl_prefer_server_ciphers off;

        # Security Headers
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
        add_header X-Frame-Options "DENY" always;
        add_header X-Content-Type-Options "nosniff" always;

        location / {
            limit_req zone=api_limit burst=20 nodelay;

            proxy_pass http://backend_nodes;
            proxy_http_version 1.1;
            proxy_set_header Connection ""; # Required for upstream keepalive
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            proxy_connect_timeout 5s;
            proxy_read_timeout 60s;
        }
    }
}
```

#Static Asset Caching & Single Page Application Routing

Serving static SPAs with browser caching:

```nginx
server {
    listen 80;
    server_name app.example.com;
    root /var/www/app/dist;
    index index.html;

    # Immutable caching for hashed assets
    location ~* \.(?:css|js|woff2?|png|jpg|webp)$ {
        expires 1y;
        add_header Cache-Control "public, max-age=31536000, immutable";
        access_log off;
    }

    # SPA route fallback
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

#Validating and Reloading Configuration

Testing syntax before reloading:

```bash
# Test configuration syntax
nginx -t

# Gracefully reload configuration without dropping connections
nginx -s reload
```

## Common Patterns

### Hardened Reverse Proxy with SSL and Rate Limiting

**Problem**: Slow APIs and vulnerability to brute-force DDoS attacks on login endpoints.

**Solution**:
Configure Nginx with connection limits and proxy buffering:

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/letsencrypt/live/api.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.example.com/privkey.pem;

    location / {
        limit_req zone=api_limit burst=20 nodelay;

        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Best Practices (2026)

- **Do** always test configuration syntax with `nginx -t` before issuing `nginx -s reload`.
- **Do** set `proxy_http_version 1.1` and `proxy_set_header Connection ""` when using `upstream` keepalive pools.
- **Do** enable `limit_req_zone` to protect login, payment, and search endpoints against abuse.
- **Do** enable `server_tokens off;` to prevent revealing Nginx version information to attackers.
- **Don't** use `if` directives inside `location` blocks (`if is evil` in Nginx); use `try_files` or maps.
- **Don't** run worker processes as root; use unprivileged `nginx` or `www-data` system users.
- **Don't** omit `Strict-Transport-Security` headers on production HTTPS endpoints.

## Troubleshooting

| Error                                                                     | Cause                                                                 | Solution                                                                   |
| :------------------------------------------------------------------------ | :-------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `502 Bad Gateway`                                                         | Upstream backend server offline or port unreachable.                  | Verify upstream application is listening on specified port.                |
| `nginx: [emerg] bind() to 0.0.0.0:80 failed (98: Address already in use)` | Another web server process already listening on port 80.              | Find conflicting process: `sudo lsof -i :80` and stop it.                  |
| `413 Request Entity Too Large`                                            | Client uploaded file larger than default `client_max_body_size` (1M). | Increase setting: `client_max_body_size 50M;` in `http` or `server` block. |

## References

- [Nginx Documentation](https://nginx.org/en/docs/)
