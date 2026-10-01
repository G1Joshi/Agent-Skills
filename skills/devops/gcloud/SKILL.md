---
name: gcloud
description: Expert Google Cloud CLI (gcloud) assistance covering configurations, service accounts, IAM impersonation, and Cloud SDK scripting. Use when automating GCP resources and deploying Google Cloud services.
---

# Google Cloud CLI (`gcloud`)

The `gcloud` CLI is part of the Google Cloud SDK. It manages authentication, local configuration, and developer workflows for GCP.

## When to Use

- **Google Cloud Platform Automation & Scripting**: Managing GCP resources, clusters, IAM roles, and deployments via `gcloud`.
- **GKE Cluster & Workload Management**: Connecting kubectl credentials and managing GKE node pools.
- **Cloud Run & Serverless Deployment**: Building and deploying serverless containers with one CLI command.
- **Filtering & Formatting GCP Assets**: Extracting resource data using `--filter` and `--format`.

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

### Advanced Filtering and Formatting with --filter & --format

Extracting precise JSON/table projections from GCP:

```bash
# List all running GCE instances with name, zone, and internal IP
gcloud compute instances list \
  --filter="status=RUNNING AND zone:us-central1" \
  --format="table(name,zone,networkInterfaces[0].networkIP:label=INTERNAL_IP)"

# Export single property as unquoted string
PROJECT_NUMBER=$(gcloud projects describe my-prod-project \
  --format="value(projectNumber)")
```

### One-Command Serverless Deployment with Cloud Run

Building from source and deploying containerized apps:

```bash
# Build and deploy directly to Cloud Run
gcloud run deploy customer-api \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --min-instances 1 \
  --max-instances 20 \
  --memory 1Gi \
  --cpu 1 \
  --set-env-vars "NODE_ENV=production"
```

### Workload Identity Federation for CI/CD

Configuring GitHub Actions or GitLab to authenticate without JSON service account keys:

```bash
# Create Workload Identity Pool
gcloud iam workload-identity-pools create "github-pool" \
  --location="global" \
  --description="Pool for GitHub Actions"

# Authorize GitHub repository to impersonate service account
gcloud iam service-accounts add-iam-policy-binding "deployer-sa@my-prod.iam.gserviceaccount.com" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/github-pool/attribute.repository/my-org/my-repo"
```

## Common Patterns

### Service Account Impersonation Without Exporting JSON Keys

**Problem**: Exporting static service account JSON keys creates credential leak risks.

**Solution**:
Use short-lived token generation via service account impersonation:

```bash
# Impersonate deployer service account dynamically
gcloud config set auth/impersonate_service_account deployer@my-project.iam.gserviceaccount.com

# Deploy Cloud Run service using impersonated credentials
gcloud run deploy api-service \
  --image gcr.io/my-project/api:latest \
  --region us-central1 \
  --platform managed
```

## Best Practices

**Do**:

- Authenticate CI/CD pipelines using Workload Identity Federation instead of downloading exported JSON service account keys.
- Use server-side `--filter` parameters to reduce payload size when querying large fleets of resources.
- Use `--format="value(field)"` when capturing output into shell variables.
- Manage multiple GCP accounts and projects cleanly using `gcloud config configurations`.

**Don't**:

- Download and store long-lived service account key files (`.json`); they are a major source of credential leaks.
- Deploy Cloud Run services with `--allow-unauthenticated` for internal-only microservices.
- Hardcode project IDs in scripts; use `gcloud config get-value project`.

## Troubleshooting

| Error                                                                          | Cause                                                  | Solution                                                          |
| :----------------------------------------------------------------------------- | :----------------------------------------------------- | :---------------------------------------------------------------- |
| `ERROR: (gcloud) The project [x] does not exist or you do not have permission` | Project ID typo or user lacks Viewer role on project.  | Set valid project: `gcloud config set project <PROJECT_ID>`.      |
| `ACCESS_TOKEN_SCOPE_INSUFFICIENT`                                              | User authenticated with limited OAuth scopes.          | Re-authenticate: `gcloud auth login --enable-gdrive-access`.      |
| `Quota exceeded for metric ...`                                                | Target region reached GCP quota limit for compute/IPs. | Request quota increase in GCP Console under IAM & Admin > Quotas. |

## References

- [gcloud CLI Documentation](https://cloud.google.com/sdk/gcloud)
