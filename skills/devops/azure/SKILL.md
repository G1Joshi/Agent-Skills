---
name: azure
description: Microsoft Azure cloud platform with Functions, AKS, and DevOps. Use for Azure services.
---

# Azure

Microsoft Azure cloud platform for enterprise applications.

## When to Use

- Enterprise cloud deployment
- .NET application hosting
- Azure Functions (serverless)
- Azure Kubernetes Service (AKS)

## Quick Start

```typescript
// Azure Function
import {
  app,
  HttpRequest,
  HttpResponseInit,
  InvocationContext,
} from "@azure/functions";

app.http("hello", {
  methods: ["GET", "POST"],
  handler: async (
    request: HttpRequest,
    context: InvocationContext,
  ): Promise<HttpResponseInit> => {
    const name = request.query.get("name") || "World";
    return { body: `Hello, ${name}!` };
  },
});
```

## Core Concepts

### Blob Storage

```typescript
import { BlobServiceClient } from "@azure/storage-blob";

const blobService = BlobServiceClient.fromConnectionString(connectionString);
const container = blobService.getContainerClient("uploads");

// Upload
const blockBlob = container.getBlockBlobClient("file.pdf");
await blockBlob.uploadData(buffer, {
  blobHTTPHeaders: { blobContentType: "application/pdf" },
});

// Download
const download = await blockBlob.download();
const content = await streamToBuffer(download.readableStreamBody);

// Generate SAS URL
const sasUrl = await blockBlob.generateSasUrl({
  permissions: BlobSASPermissions.parse("r"),
  expiresOn: new Date(Date.now() + 3600 * 1000),
});
```

### Cosmos DB

```typescript
import { CosmosClient } from "@azure/cosmos";

const client = new CosmosClient(connectionString);
const container = client.database("mydb").container("items");

// Create
const { resource } = await container.items.create({
  id: "123",
  name: "John",
  category: "user",
});

// Query
const { resources } = await container.items
  .query("SELECT * FROM c WHERE c.category = @cat", [
    { name: "@cat", value: "user" },
  ])
  .fetchAll();
```

## Common Patterns

### Bicep (IaC)

```bicep
param location string = resourceGroup().location

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'mystorageaccount'
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}

resource functionApp 'Microsoft.Web/sites@2023-01-01' = {
  name: 'myfunctionapp'
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: appServicePlan.id
  }
}
```

## Best Practices

**Do**:

- Use Managed Identities
- Enable Azure Defender
- Use Key Vault for secrets
- Implement proper RBAC

**Don't**:

- Store secrets in code
- Use owner role broadly
- Skip network security
- Ignore cost management

## Troubleshooting

| Issue               | Cause            | Solution               |
| ------------------- | ---------------- | ---------------------- |
| 403 Forbidden       | RBAC issue       | Check role assignments |
| Function cold start | First invocation | Use Premium plan       |
| Connection failed   | Network/firewall | Check NSG rules        |

## References

- [Azure Documentation](https://docs.microsoft.com/azure/)
- [Azure Functions](https://docs.microsoft.com/azure/azure-functions/)
