---
name: digitalocean
description: Expert DigitalOcean cloud assistance covering Droplets, App Platform, Managed Kubernetes (DOKS), Spaces (S3-compatible), and VPC. Use when deploying, scaling, and managing cloud workloads on DigitalOcean.
---

# DigitalOcean

DigitalOcean provides developer-centric cloud infrastructure, offering Droplets, managed Kubernetes (DOKS), App Platform PaaS, and S3-compatible Spaces storage.

## When to Use

- **Cost-Effective Cloud Infrastructure**: Simple, transparent pricing for Droplets, Managed Databases, and Volumes.
- **Managed Kubernetes (DOKS)**: Running containerized workloads without control-plane management charges.
- **App Platform PaaS Deployments**: Deploying web applications directly from GitHub/GitLab repositories with zero server configuration.
- **S3-Compatible Object Storage (Spaces)**: Storing media, backups, and static assets with built-in CDN.

## Quick Start

```bash
# Authenticate doctl CLI
doctl auth init

# Create Droplet with SSH key
doctl compute droplet create web-prod-01 \
  --region nyc3 \
  --size s-2vcpu-4gb \
  --image ubuntu-24-04-x64 \
  --ssh-keys "<ssh-key-fingerprint>"
```

## Core Concepts

### Declarative App Platform Specification (.do/app.yaml)

Deploying full-stack applications with managed PostgreSQL:

```yaml
name: saas-platform-prod
region: nyc
services:
  - name: web-api
    github:
      repo: org/saas-backend
      branch: main
      deploy_on_push: true
    build_command: npm run build
    run_command: npm start
    http_port: 3000
    instance_count: 2
    instance_size_slug: basic-m
    routes:
      - path: /api
    envs:
      - key: DATABASE_URL
        scope: RUN_TIME
        value: ${prod-db.DATABASE_URL}

databases:
  - name: prod-db
    engine: PG
    version: "16"
    production: true
    num_nodes: 1
    size: db-s-1vcpu-1gb
```

### DigitalOcean CLI (doctl) Scripting

Automating Droplet and Kubernetes cluster provisioning:

```bash
# Authenticate doctl with API token
doctl auth init --access-token "$DIGITALOCEAN_TOKEN"

# Provision a production Kubernetes cluster (DOKS)
doctl kubernetes cluster create k8s-prod-nyc \
  --region nyc3 \
  --version latest \
  --node-pool "name=worker-pool;size=s-2vcpu-4gb;count=3;auto-scale=true;min-nodes=3;max-nodes=8"

# Fetch kubeconfig credentials
doctl kubernetes cluster kubeconfig save k8s-prod-nyc
```

### Managed Spaces S3-Compatible Uploads with Boto3

Uploading backups to DigitalOcean Spaces:

```python
import boto3

session = boto3.session.Session()
client = session.client(
    's3',
    region_name='nyc3',
    endpoint_url='https://nyc3.digitaloceanspaces.com',
    aws_access_key_id='DO_SPACES_KEY',
    aws_secret_access_key='DO_SPACES_SECRET'
)

client.upload_file('backup.tar.gz', 'company-backups', '2026/backup-03-27.tar.gz')
```

## Common Patterns

### App Platform Specification (app.yaml) for Monorepos

**Problem**: Deploying both frontend SPA and backend API services from a single repository.

**Solution**:
Define unified DigitalOcean App Platform spec:

```yaml
name: ecommerce-app
region: nyc
services:
  - name: api-service
    github:
      repo: myorg/app
      branch: main
      deploy_on_push: true
    source_dir: backend
    run_command: npm start
    envs:
      - key: DATABASE_URL
        scope: RUN_TIME
        value: ${db.DATABASE_URL}
static_sites:
  - name: frontend
    source_dir: frontend
    build_command: npm run build
    output_dir: dist
```

## Best Practices

**Do**:

- Enable Cloud Firewalls on all Droplets, restricting SSH access to trusted VPN IP ranges.
- Use VPC networks to isolate private traffic between Droplets, Managed Databases, and DOKS nodes.
- Enable automated weekly backups and monitoring alerts on production Droplets.
- Leverage App Platform for microservices to offload OS patching, TLS certificates, and deployments.

**Don't**:

- Run stateful databases inside ephemeral Droplets without persistent Block Storage volumes.
- Use root passwords for Droplet access; strictly enforce SSH key authentication.
- Store unencrypted database backups in public Spaces buckets.

## Troubleshooting

| Error                                      | Cause                                                                    | Solution                                                                   |
| :----------------------------------------- | :----------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `doctl: Error: POST ...: 401 Unauthorized` | DigitalOcean API personal access token expired or revoked.               | Re-generate token in DO Console > API and re-run `doctl auth init`.        |
| `Droplet locked / action in progress`      | Previous resize, backup, or snapshot still executing.                    | Wait for active event to complete before executing subsequent mutations.   |
| `App Platform build failed: Out of memory` | Build process (e.g. large Webpack compile) exceeded build container RAM. | Upgrade instance size or build artifacts in external CI before deployment. |

## References

- [DigitalOcean Documentation](https://docs.digitalocean.com/)
