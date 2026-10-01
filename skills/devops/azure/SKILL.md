---
name: azure
description: Expert Microsoft Azure cloud assistance covering Entra ID, App Services, AKS, Azure SQL, Blob Storage, and Resource Manager. Use when designing, deploying, and managing enterprise Azure cloud infrastructure.
---

# Azure

Microsoft Azure is an enterprise cloud computing platform featuring managed container services, Azure Arc hybrid management, and unified identity governance.

## When to Use

- **Enterprise Microsoft Cloud Infrastructure**: Hybrid cloud environments, Microsoft Entra ID (Azure AD), and Windows/Linux VMs.
- **Containerized Apps with Azure Container Apps (ACA) & AKS**: Microservices with managed KEDA autoscaling and Envoy routing.
- **Serverless Event-Driven Workloads**: Azure Functions, Event Grid, Service Bus, and Logic Apps.
- **AI & OpenAI Integration**: Enterprise Azure OpenAI Service endpoints with private networking and VNet endpoints.

## Quick Start

```bash
# Login to Azure subscription
az login

# Create a resource group
az group create --name rg-production --location eastus

# Deploy Azure App Service plan and web app
az appservice plan create --name plan-prod --resource-group rg-production --sku B1 --is-linux
az webapp create --name app-service-prod-1234 --resource-group rg-production --plan plan-prod --runtime "NODE:20-lts"
```

## Core Concepts

### Azure Container Apps Declarative Deployment

Deploying scalable microservices with KEDA scaling:

```yaml
# container-app.yaml
apiVersion: Microsoft.App/containerApps@2024-03-01
type: Microsoft.App/containerApps
metadata:
  name: billing-service
  location: eastus
properties:
  managedEnvironmentId: /subscriptions/.../managedEnvironments/prod-env
  configuration:
    ingress:
      external: true
      targetPort: 8080
      transport: auto
    secrets:
      - name: db-connection
        keyVaultUrl: https://prod-vault.vault.azure.net/secrets/db-conn
        identity: system
  template:
    containers:
      - image: myacr.azurecr.io/billing-service:v2.1.0
        name: billing
        resources:
          cpu: 0.5
          memory: 1.0Gi
    scale:
      minReplicas: 2
      maxReplicas: 10
      rules:
        - name: http-scaling
          http:
            metadata:
              concurrentRequests: "100"
```

### Managed Identities & Key Vault Integration

Accessing secrets without code credentials using Azure SDK:

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# DefaultAzureCredential automatically checks Managed Identity, Azure CLI, or env
credential = DefaultAzureCredential()
vault_url = "https://corp-production-vault.vault.azure.net/"

client = SecretClient(vault_url=vault_url, credential=credential)
db_password = client.get_secret("database-master-password").value
print("Retrieved secret securely via Managed Identity.")
```

### Azure Private Endpoints & Virtual Networks

Securing database traffic from public internet exposure:

```text
[Virtual Network (VNet)]
  ├── Application Subnet ──► Azure Container Apps / App Service
  │     │ (Private VNet Traffic)
  │     ▼
  └── Private Endpoint Subnet ──► Azure Cosmos DB / SQL Database (Public access: Disabled)
```

## Common Patterns

### Managed Identity for Secure Azure Resource Access

**Problem**: Storing database passwords or Azure Storage keys in application config files.

**Solution**:
Assign System-Assigned Managed Identity and grant RBAC:

```bash
# Enable Managed Identity on App Service
az webapp identity assign --name my-web-app --resource-group rg-production

# Grant Storage Blob Data Contributor role to the App Service identity
APP_SP_ID=$(az webapp identity show --name my-web-app --resource-group rg-production --query principalId -o tsv)

az role assignment create \
  --assignee $APP_SP_ID \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-production/providers/Microsoft.Storage/storageAccounts/mystorage"
```

## Best Practices

**Do**:

- Use Managed Identities (System-assigned or User-assigned) for service-to-service authentication instead of passwords.
- Store all certificates and connection strings in Azure Key Vault.
- Deploy resources inside Virtual Networks with Private Endpoints, disabling public network access on databases.
- Leverage Azure Container Apps (ACA) for microservices that do not require full Kubernetes cluster management overhead.

**Don't**:

- Store plain text secrets in App Settings or environment variables.
- Assign broad `Contributor` or `Owner` roles at subscription scopes; scope RBAC to resource groups.
- Leave diagnostic logging disabled; route Azure Monitor logs to Log Analytics Workspaces.

## Troubleshooting

| Error                                                                               | Cause                                                                            | Solution                                                                      |
| :---------------------------------------------------------------------------------- | :------------------------------------------------------------------------------- | :---------------------------------------------------------------------------- |
| `AuthorizationFailed: The client ... does not have authorization to perform action` | User or service principal lacks RBAC role on target resource group/subscription. | Request Contributor or specific RBAC role assignment from subscription owner. |
| `ResourceNotFound: The Resource '...' could not be found`                           | Typo in resource name or querying wrong subscription/resource group.             | Verify active subscription with `az account show` and check resource group.   |
| `QuotaExceeded: Operation could not be completed`                                   | Regional VM vCPU quota exceeded on Azure subscription.                           | Request quota increase in Azure Portal under Help + Support.                  |

## References

- [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)
