---
name: vault
description: HashiCorp Vault for secrets management and encryption. Use for enterprise secrets.
---

# HashiCorp Vault

Secrets management and data protection platform.

## When to Use

- Centralized secrets management
- Dynamic credentials
- Encryption as a service
- PKI/certificate management

## Quick Start

```bash
# Start dev server
vault server -dev

# Set address
export VAULT_ADDR='http://127.0.0.1:8200'

# Store secret
vault kv put secret/myapp username=admin password=secret

# Read secret
vault kv get secret/myapp
```

## Core Concepts

### API Access

```typescript
import vault from "node-vault";

const client = vault({
  apiVersion: "v1",
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN,
});

// Read secret
const { data } = await client.read("secret/data/myapp");
console.log(data.data.password);

// Write secret
await client.write("secret/data/myapp", {
  data: { username: "admin", password: "new-secret" },
});
```

### Dynamic Secrets

```bash
# Enable database engine
vault secrets enable database

# Configure connection
vault write database/config/mydb \
  plugin_name=mysql-database-plugin \
  connection_url="{{username}}:{{password}}@tcp(localhost:3306)/"

# Get dynamic credentials
vault read database/creds/my-role
```

## Best Practices

**Do**: Use AppRole for apps, enable audit logging, rotate tokens
**Don't**: Use root token in production, store vault token in code

## References

- [Vault Documentation](https://developer.hashicorp.com/vault/docs)
