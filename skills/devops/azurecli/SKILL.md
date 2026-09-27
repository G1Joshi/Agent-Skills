---
name: azurecli
description: Expert Azure CLI (az) assistance covering command automation, JMESPath queries, resource templates, and DevOps scripts. Use when scripting Azure management tasks and deploying cloud resources.
---

# Azure CLI (`az`)

The Azure CLI is the standard tool for managing Azure resources. 2025 brings deeper integration with **Bicep** (Azure's IaC language) and AI assistance.

## When to Use

- **Automating Azure Cloud Operations**: Scripting resource deployment, role assignments, and monitoring via `az`.
- **CI/CD Azure DevOps & GitHub Actions**: Deploying infrastructure and applications using service principals or OIDC.
- **JMESPath Querying of Azure Resources**: Extracting specific cloud parameters using `--query`.
- **Container Registry & AKS Cluster Management**: Authenticating Docker clients and managing Kubernetes credentials.

## Quick Start

```bash
# Login
az login

# Set Subscription
az account set --subscription "My Subscription"

# Create AKS Cluster
az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 1 --generate-ssh-keys
```

## Core Concepts

#Resource Group Creation & Infrastructure Deployment

Deploying resources with Bicep / ARM templates:

```bash
# Set default subscription and location
az account set --subscription "Production-Subscription"
az configure --defaults location=eastus

# Create Resource Group
az group create --name rg-production-platform --location eastus

# Deploy infrastructure via Bicep template
az deployment group create \
  --resource-group rg-production-platform \
  --template-file main.bicep \
  --parameters environment=prod adminEmail=sysadmin@example.com
```

#Querying and Filtering with JMESPath (--query)

Extracting resource properties without installing jq:

```bash
# List all running VMs with their private IPs and OS type
az vm list \
  --show-details \
  --query "[?powerState=='VM running'].{Name:name, IP:privateIps, OS:osType, Size:hardwareProfile.vmSize}" \
  --output table

# Get public IP address of an Application Gateway
APP_GATEWAY_IP=$(az network public-ip show \
  --resource-group rg-production-platform \
  --name pip-appgw \
  --query ipAddress \
  --output tsv)
```

#AKS Credential Injection & ACR Authentication

Connecting to container services seamlessly:

```bash
# Log in to Azure Container Registry via native Docker
az acr login --name myproductionacr

# Fetch kubectl credentials for AKS cluster
az aks get-credentials \
  --resource-group rg-production-platform \
  --name aks-prod-cluster \
  --overwrite-existing
```

## Common Patterns

### JMESPath Filtering with TSV Output for Scripting

**Problem**: Parsing complex JSON output in bash scripts without external dependencies like jq.

**Solution**:
Use `--query` with TSV output format:

```bash
# Extract the outbound IP addresses of an App Service as space-separated values
OUTBOUND_IPS=$(az webapp show \
  --resource-group rg-production \
  --name my-api-service \
  --query "outboundIpAddresses" \
  --output tsv)

echo "Allowlist IPs: $OUTBOUND_IPS"
```

## Best Practices (2026)

- **Do** authenticate GitHub Actions and pipelines using Workload Identity Federation (OIDC) rather than client secrets.
- **Do** use `--output tsv` with `--query` when capturing single strings into shell variables without quotes.
- **Do** test and validate deployments before execution with `az deployment group what-if`.
- **Do** use `az bicep` directly through the CLI for clean, modular infrastructure-as-code.
- **Don't** use interactive `az login` in automated headless scripts; use Service Principals or Managed Identities.
- **Don't** output sensitive keys in plain text; pipe outputs to secure files or masking variables.
- **Don't** run long operations synchronously without considering `--no-wait` and `az resource wait`.

## Troubleshooting

| Error                                    | Cause                                                               | Solution                                                                |
| :--------------------------------------- | :------------------------------------------------------------------ | :---------------------------------------------------------------------- |
| `Please run 'az login' to setup account` | Azure CLI session token expired or not logged in.                   | Run `az login` or use service principal `az login --service-principal`. |
| `az: error: unrecognized arguments`      | Passing parameters with wrong flag syntax or misplaced quotes.      | Verify argument names with `az <command> --help`.                       |
| `Subscription '...' does not exist`      | Trying to operate on a subscription not accessible to current user. | List available subscriptions with `az account list --output table`.     |

## References

- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)
