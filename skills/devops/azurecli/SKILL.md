---
name: azurecli
description: Azure CLI command-line interface. Use for Azure automation.
---

# Azure CLI (`az`)

The Azure CLI is the standard tool for managing Azure resources. 2025 brings deeper integration with **Bicep** (Azure's IaC language) and AI assistance.

## When to Use

- **Management**: Quickly creating Resource Groups or AKS clusters.
- **Automation**: CI/CD pipelines targeting Azure.
- **Querying**: Using JMESPath to find resources.

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

### Command Groups

Hierarchical structure: `az group`, `az vm`, `az network`.

### Interactive Mode

`az interactive`. Provides auto-completion, examples, and descriptions in the terminal.

### Extensions

The CLI is extensible.
`az extension add --name aks-preview`

## Best Practices (2025)

**Do**:

- **Use `az upgrade`**: Keep the CLI and extensions auto-updated.
- **Use Managed Identity**: When running on Azure VMs/Functions, use `az login --identity` to avoid credentials.
- **Use `--no-wait`**: For long operations (creating VMs), fire and forget.

**Don't**:

- **Don't hardcode Service Principals**: Use Workload Identity Federation (OIDC) in GitHub Actions instead of secrets.

## References

- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)
