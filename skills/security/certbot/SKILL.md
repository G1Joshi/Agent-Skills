---
name: certbot
description: Expert Certbot SSL/TLS certificate assistance covering Let's Encrypt, ACME DNS/HTTP validation, and auto-renewal. Use when provisioning SSL certificates, setting up HTTPS, or troubleshooting cert renewals.
---

# Certbot

Certbot is a free, open-source software tool for automatically using Let's Encrypt certificates on manually-administrated websites to enable HTTPS.

## When to Use

- **Automated SSL/TLS Certificate Issuance**: Provisioning free, trusted Let's Encrypt certificates for web servers.
- **Automatic Certificate Renewal**: Configuring cron or systemd timers to renew expiring certificates without downtime.
- **Wildcard Certificate Provisioning**: Generating wildcard certificates (`*.example.com`) via automated DNS-01 challenges.
- **Web Server Configuration Automation**: Automatically configuring HTTPS directives, ciphers, and redirects in Nginx and Apache.

## Quick Start

```bash
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

# Auto-configure Nginx
sudo certbot --nginx
```

## Core Concepts

#Automated Certificate Management Environment (ACME)

Certbot proves domain ownership to the Let's Encrypt Certificate Authority through challenge-response protocols:

```
[ Web Server (Certbot) ] ──1. Request Certificate──→ [ Let's Encrypt CA ]
                         ←─2. Challenge (HTTP-01)───
[ Let's Encrypt CA ]     ──3. Fetch /.well-known/acme-challenge/<token>──→ [ Web Server ]
[ Let's Encrypt CA ]     ──4. Issue Signed Certificate (90 Days)─────────→ [ Web Server ]
```

#HTTP-01 vs DNS-01 Challenge Types

- **HTTP-01**: Serves a challenge file over port 80 at `/.well-known/acme-challenge/`. Simple, but cannot issue wildcard certificates.
- **DNS-01**: Creates a TXT record `_acme-challenge.example.com`. Required for wildcard certificates and internal/private servers:

```bash
# Issue Wildcard Certificate via Cloudflare DNS-01 Challenge
certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials ~/.secrets/cloudflare.ini \
  -d "example.com" -d "*.example.com"
```

#Non-Interactive Standalone Mode

Spins up a temporary standalone web server to validate domain control on machines without existing web servers:

```bash
certbot certonly --standalone -d api.example.com --non-interactive --agree-tos -m admin@example.com
```

## Common Patterns

### Automated Nginx Wildcard Certificate via DNS Challenge

**Problem**: HTTP-01 challenges fail on private services, firewalled servers, or wildcard subdomains.

**Solution**:
Use the DNS-01 validation plugin for automated wildcard provisioning:

```bash
certbot certonly \
  --dns-cloudflare \
  --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini \
  -d "*.example.com" -d "example.com" \
  --agree-tos --email security@example.com --non-interactive
```

## Best Practices (2026)

**Do**:

- **Test with `--dry-run` First**: Always test issuance and renewal against the Let's Encrypt staging environment to avoid hitting production rate limits.
- **Automate Service Reloads with Deploy Hooks**: Use `--deploy-hook "systemctl reload nginx"` so web servers reload new certificates upon renewal.
- **Retain Port 80 Open**: Keep HTTP port 80 open to allow HTTP-01 renewal challenges to succeed smoothly.
- **Monitor Expiration Dates with Prometheus / Datadog**: Set up alerts if certificates have fewer than 20 days remaining.

**Don't**:

- **Don't forget to configure renewal timers**: Verify that `systemctl list-timers | grep certbot` is active and running twice daily.
- **Don't hardcode DNS provider API tokens with global write access**: Restrict cloud DNS API tokens to modify only the `_acme-challenge` TXT records.
- **Don't delete `/etc/letsencrypt/` files manually**: Use `certbot delete --cert-name <domain>` to remove decommissioned certificate configs.

## Troubleshooting

| Error        | Cause              | Solution                                                      |
| :----------- | :----------------- | :------------------------------------------------------------ |
| `Timeout`    | Port 80 blocked.   | Open Firewall/Security Group for Port 80 (HTTP-01 challenge). |
| `Rate Limit` | Too many failures. | Wait 1 hour or use `--test-cert`.                             |

## References

- [Certbot Instructions](https://certbot.eff.org/)
