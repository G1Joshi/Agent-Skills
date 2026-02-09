---
name: nginx
description: NGINX web server and reverse proxy with load balancing and SSL. Use for web server configuration.
---

# NGINX

High-performance web server and reverse proxy.

## When to Use

- Reverse proxy for applications
- Load balancing
- SSL termination
- Static file serving

## Quick Start

```nginx
# Basic reverse proxy
server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Core Concepts

### SSL Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000" always;

    location / {
        proxy_pass http://app;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### Load Balancing

```nginx
upstream app {
    least_conn;
    server 127.0.0.1:3001 weight=3;
    server 127.0.0.1:3002;
    server 127.0.0.1:3003 backup;

    keepalive 32;
}

server {
    location / {
        proxy_pass http://app;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

## Common Patterns

### Caching

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=app_cache:10m max_size=1g;

server {
    location /api {
        proxy_cache app_cache;
        proxy_cache_valid 200 10m;
        proxy_cache_key "$scheme$request_method$host$request_uri";
        add_header X-Cache-Status $upstream_cache_status;

        proxy_pass http://app;
    }

    location /static {
        alias /var/www/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Rate Limiting

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

server {
    location /api {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://app;
    }
}
```

## Best Practices

**Do**:

- Enable gzip compression
- Set proper timeouts
- Use connection keepalive
- Configure proper logging

**Don't**:

- Expose server version
- Use weak SSL ciphers
- Skip security headers
- Ignore log rotation

## Troubleshooting

| Issue             | Cause            | Solution                    |
| ----------------- | ---------------- | --------------------------- |
| 502 Bad Gateway   | Backend down     | Check upstream health       |
| 504 Timeout       | Slow backend     | Increase proxy_read_timeout |
| Permission denied | File permissions | Check nginx user perms      |

## References

- [NGINX Documentation](https://nginx.org/en/docs/)
- [NGINX Config Generator](https://nginxconfig.io/)
