---
name: certbot
description: Certbot Let's Encrypt certificates. Use for SSL/TLS.
---

# Certbot

Certbot is a free, open-source software tool for automatically using Let's Encrypt certificates on manually-administrated websites to enable HTTPS.

## When to Use

- **VPS Hosting**: Running Nginx/Apache on a VM (EC2, DigitalOcean) and need SSL.
- **Homelab**: Securing local services exposed via DDNS.
- **Wildcards**: Issuing `*.example.com` certificates (requires DNS plugin).

## Quick Start (Nginx on Ubuntu)

```bash
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

# Auto-configure Nginx
sudo certbot --nginx
```

## Core Concepts

### ACME Protocol

Automatic Certificate Management Environment. The protocol Certbot uses to talk to the Let's Encrypt CA.

### Challenges

To prove you own the domain:

- **HTTP-01**: Certbot puts a file in `.well-known/acme-challenge`. (Requires port 80 open).
- **DNS-01**: Certbot creates a TXT record. (Required for Wildcards).

### Renewal

Let's Encrypt certs last 90 days. Certbot installs a timer (`systemd`) to check twice daily and renew any cert expiring in <30 days.

## Best Practices (2025)

**Do**:

- **Use DNS plugins**: If using Cloudflare/Route53, use `certbot-dns-cloudflare`. It's robust and supports wildcards.
- **Test with Staging**: Use `--dry-run` or `--test-cert` to differentiate testing from production (Rate limits apply).
- **Reload Web Server**: Ensure the renewal hook (`--deploy-hook`) reloads Nginx/Apache so it picks up the new cert.

**Don't**:

- **Don't Run as Root (custom)**: The default runs as root, but for custom hooks, drop privileges if possible.
- **Don't Hardcode IP**: ACME verification usually requires a Domain Name.

## Troubleshooting

| Error        | Cause              | Solution                                                      |
| :----------- | :----------------- | :------------------------------------------------------------ |
| `Timeout`    | Port 80 blocked.   | Open Firewall/Security Group for Port 80 (HTTP-01 challenge). |
| `Rate Limit` | Too many failures. | Wait 1 hour or use `--test-cert`.                             |

## References

- [Certbot Instructions](https://certbot.eff.org/)
