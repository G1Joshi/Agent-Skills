---
name: digitalocean
description: DigitalOcean cloud platform with droplets. Use for simple cloud.
---

# DigitalOcean

DigitalOcean (DO) focuses on simplicity and developer experience. In 2025, it has expanded into **Managed AI** (GenAI Platform) and robust PaaS offerings (App Platform).

## When to Use

- **Startups / SMBs**: Predictable pricing, simple UI, no "cloud shock" bills.
- **Simple VM Hosting**: Droplets are the gold standard for "Just give me a VPS".
- **Managed K8s**: DOKS is a very affordable compliant Kubernetes service.

## Core Concepts

### Droplets

Virtual Private Servers (Linux VMs).

### App Platform

PaaS (Platform as a Service). Point it to a GitHub repo, and it builds/deploys/scales your app.

### Spaces

S3-compatible Object Storage with a built-in CDN.

## Best Practices (2025)

**Do**:

- **Use VPC**: Isolate your Droplets and Managed Databases in a private network (enabled by default in new projects).
- **Use Cloud Firewalls**: Block all ports except what you need.
- **Use App Platform**: For web apps, avoid managing Droplets. Let DO handle the OS patching and scaling.

**Don't**:

- **Don't ignore backups**: Enable automatic backups for Droplets and Databases.

## References

- [DigitalOcean Documentation](https://docs.digitalocean.com/)
