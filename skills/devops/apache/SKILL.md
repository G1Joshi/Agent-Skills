---
name: apache
description: Expert Apache HTTP Server assistance covering virtual hosts, mod_rewrite, reverse proxying, SSL/TLS, and .htaccess. Use when configuring Apache web servers, URL redirection, or legacy web hosts.
---

# Apache HTTP Server (httpd)

Apache is a robust, modular web server. While Nginx leads in raw performance, Apache leads in **flexibility** via `.htaccess`. v2.4 remains the stable standard in 2025.

## When to Use

- **Enterprise HTTP Reverse Proxy & Web Serving**: Serving dynamic applications and static assets with Apache HTTP Server (httpd).
- **PHP & Mod_Security WAF Deployments**: Deploying PHP applications (WordPress, Drupal) and Web Application Firewalls (OWASP CRS).
- **Fine-Grained Access Control & .htaccess**: Delegating directory-level access rules and rewrites to non-root developers.
- **Complex URL Rewriting & Reverse Proxying**: Utilizing `mod_rewrite` and `mod_proxy` for intricate request routing.

## Quick Start

```apache
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    DocumentRoot /var/www/html

    <Directory /var/www/html>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/example_error.log
    CustomLog ${APACHE_LOG_DIR}/example_access.log combined
</VirtualHost>
```

## Core Concepts

#VirtualHost Configuration with TLS and HTTP/2

Production VirtualHost configuration with modern TLS parameters:

```apache
<VirtualHost *:443>
    ServerName api.example.com
    ServerAdmin sysadmin@example.com
    DocumentRoot /var/www/api/public

    Protocols h2 http/1.1
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/api.example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/api.example.com/privkey.pem

    # Modern TLS Security Headers
    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"

    <Directory /var/www/api/public>
        Options -Indexes +FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    CustomLog /var/log/apache2/api_access.log combined
    ErrorLog /var/log/apache2/api_error.log
</VirtualHost>
```

#Reverse Proxy with mod_proxy & Load Balancing

Forwarding traffic to backend microservices with health checks:

```apache
<Proxy balancer://appcluster>
    BalancerMember http://10.0.1.10:3000 route=node1 retry=10
    BalancerMember http://10.0.1.11:3000 route=node2 retry=10
    ProxySet lbmethod=byrequests
</Proxy>

<Location /api>
    ProxyPass balancer://appcluster/api
    ProxyPassReverse balancer://appcluster/api
    ProxyPreserveHost On
    RequestHeader set X-Forwarded-Proto "https"
</Location>
```

#URL Rewriting with mod_rewrite

Handling Single Page Application routing:

```apache
<Directory /var/www/spa/dist>
    RewriteEngine On
    RewriteBase /
    RewriteRule ^index\.html$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.html [L]
</Directory>
```

## Common Patterns

### Reverse Proxy with SSL Termination and WebSocket Upgrade

**Problem**: Forwarding external HTTPS traffic to an internal Node/Go service while supporting WebSockets.

**Solution**:
Enable `proxy` and `proxy_wstunnel` modules:

```apache
<VirtualHost *:443>
    ServerName api.example.com
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/api.crt
    SSLCertificateKeyFile /etc/ssl/private/api.key

    # WebSocket forwarding
    RewriteEngine on
    RewriteCond %{HTTP:Upgrade} websocket [NC]
    RewriteCond %{HTTP:Connection} upgrade [NC]
    RewriteRule ^/?(.*) "ws://127.0.0.1:3000/$1" [P,L]

    # HTTP API proxying
    ProxyPass / http://127.0.0.1:3000/
    ProxyPassReverse / http://127.0.0.1:3000/
</VirtualHost>
```

## Best Practices (2026)

- **Do** disable `AllowOverride All` in production to prevent performance hits from filesystem `.htaccess` lookups.
- **Do** enable `Protocols h2 http/1.1` to take advantage of HTTP/2 multiplexing.
- **Do** hide server signatures by setting `ServerTokens Prod` and `ServerSignature Off`.
- **Do** test configuration syntax with `apachectl configtest` before reloading the service.
- **Don't** use the prefork MPM for high-concurrency modern workloads; use the `event` MPM (`mpm_event`).
- **Don't** leave directory listings enabled (`Options +Indexes`); always use `Options -Indexes`.
- **Don't** run Apache as root; ensure worker processes run under dedicated unprivileged users (`www-data`).

## Troubleshooting

| Error                                                              | Cause                                                                   | Solution                                                                           |
| :----------------------------------------------------------------- | :---------------------------------------------------------------------- | :--------------------------------------------------------------------------------- |
| `AH00072: make_sock: could not bind to address [::]:80`            | Port 80 occupied by Nginx, another Apache, or Docker container.         | Kill conflicting process: `sudo fuser -k 80/tcp`.                                  |
| `403 Forbidden: You don't have permission to access this resource` | Directory permissions too restrictive or missing `Require all granted`. | Check filesystem ownership (`chown -R www-data:www-data`) and `<Directory>` block. |
| `Invalid command 'RewriteEngine'`                                  | `mod_rewrite` module not enabled.                                       | Run `sudo a2enmod rewrite && sudo systemctl restart apache2`.                      |

## References

- [Apache HTTP Server Documentation](https://httpd.apache.org/docs/2.4/)
