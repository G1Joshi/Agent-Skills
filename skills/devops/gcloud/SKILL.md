---
name: gcloud
description: Google Cloud SDK command-line tools. Use for GCP automation.
---

# Google Cloud CLI (`gcloud`)

The `gcloud` CLI is part of the Google Cloud SDK. It manages authentication, local configuration, and developer workflows for GCP.

## When to Use

- **App Engine / Cloud Run**: `gcloud app deploy` and `gcloud run deploy` are the standard ways to ship code.
- **Kubernetes**: `gcloud container clusters get-credentials` is essential for GKE access.
- **Auth**: `gcloud auth login` sets up Application Default Credentials (ADC).

## Quick Start

```bash
# Initialize
gcloud init

# Authenticate for local code (ADC)
gcloud auth application-default login

# Deploy to Cloud Run
gcloud run deploy my-service --source .
```

## Core Concepts

### Components

Installable modules. `kubectl`, `beta`, `gke-gcloud-auth-plugin`.
`gcloud components install kubectl`

### Configurations

Use named configurations to switch between accounts/projects.
`gcloud config configurations create dev`

### Alpha / Beta

GCP releases features rapidly. Many commands live under `gcloud beta`.

## Best Practices (2025)

**Do**:

- **Use ADC**: For local development, `application-default login` is the correct way to auth your local Python/Node scripts.
- **Use `gcloud config set project`**: Don't pass `--project` to every command. Set the context.
- **Scripting**: Use `--format="json"` and `jq` for reliable automation.

**Don't**:

- **Don't use Service Account Keys locally**: They are risky. Use User Credentials (ADC) for local dev.

## References

- [gcloud CLI Documentation](https://cloud.google.com/sdk/gcloud)
