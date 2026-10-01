---
name: vault
description: Expert HashiCorp Vault assistance covering secret engines, dynamic secrets, transit encryption, and AppRole auth. Use when managing secrets, rotating database credentials, or securing cloud infrastructure.
---

# HashiCorp Vault

Vault is a tool for securely accessing secrets. A secret is anything that you want to tightly control access to, such as API keys, passwords, or certificates. Vault provides a unified interface to any secret while providing tight access control and recording a detailed audit log.

## When to Use

- **Centralized Secrets Management**: Securely storing and accessing API keys, database credentials, certificates, and encryption keys.
- **Dynamic On-Demand Credentials**: Generating short-lived, unique database credentials that expire automatically after task completion.
- **Data Encryption as a Service (Transit Engine)**: Encrypting sensitive data in transit and at rest without exposing cryptographic keys to applications.
- **PKI & Certificate Authority Automation**: Issuing short-lived X.509 certificates for microservices and internal domains.

## Quick Start

```bash
vault server -dev
export VAULT_ADDR='http://127.0.0.1:8200'

# Write a secret
vault kv put secret/hello foo=world

# Read a secret
vault kv get secret/hello
```

## Core Concepts

### Secret Engines & Path-Based Access

Vault organizes capabilities under hierarchical mount paths:

```text
secret/data/my-app/config     -> Key-Value (KV v2) persistent secrets
database/creds/readonly-user  -> Dynamic on-demand temporary database roles
transit/encrypt/customer-pii  -> Encryption-as-a-Service without key export
pki/issue/internal-domain     -> Dynamic TLS certificate generation
```

### Dynamic Database Credential Generation

Vault connects to PostgreSQL/MySQL and creates unique users on the fly with automatic lease expiration:

```bash
# Application requests temporary credentials
vault read database/creds/readonly-role

# Output:
# lease_id: database/creds/readonly-role/h712398
# lease_duration: 1h
# username: v-token-readonly-1727420400
# password: A1b2C3d4E5f6G7h8
```

### Application Authentication via Kubernetes Auth

Applications running in Kubernetes authenticate using their native ServiceAccount tokens:

```typescript
import vault from "node-vault";
import fs from "fs";

const jwt = fs.readFileSync(
  "/var/run/secrets/kubernetes.io/serviceaccount/token",
  "utf8",
);

const client = vault({ endpoint: "https://vault.internal.corp:8200" });
const result = await client.kubernetesLogin({
  role: "billing-service-role",
  jwt: jwt,
});

// Read secret using authenticated client token
client.token = result.auth.client_token;
const secret = await client.read("secret/data/billing/api-keys");
console.log("Stripe Secret:", secret.data.data.STRIPE_KEY);
```

## Common Patterns

### Dynamic PostgreSQL Database Credential Generation

**Problem**: Long-lived, shared database passwords hardcoded in application config leak over time.

**Solution**:
Request short-lived dynamic credentials with automatic TTL revocation:

```bash
# Read dynamic database credentials with 1-hour lease
vault read database/creds/readonly-app

# Key-Value v2 secret read with JSON output
vault kv get -format=json secret/data/payments/stripe | jq '.data.data.api_key'
```

## Best Practices

**Do**:

- Use Dynamic Database Credentials: Never share static database passwords across services; let Vault issue short-lived credentials.
- Authenticate via Cloud / Platform Identity: Use Kubernetes Auth, AWS IAM Auth, or Azure Managed Identity instead of static root tokens.
- Enable Transit Secret Engine for Sensitive PII: Offload encryption and key rotation to Vault; keep private keys out of application memory.
- Automate Lease Renewal: Ensure background tasks renew long-running leases or re-authenticate prior to token expiration.

**Don't**:

- Store the Vault Root Token: Revoke the root token immediately after initial setup and cluster unsealing.
- Disable TLS on the Vault API: Never communicate with Vault over unencrypted HTTP.
- Grant broad wildcard policies: Follow least privilege; grant read access only to specific secret paths needed by each microservice.

## Troubleshooting

| Error                                 | Cause                                                           | Solution                                                                                                |
| :------------------------------------ | :-------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `Error: Vault is sealed`              | Vault restarted or initialized without unsealing keys.          | Run `vault operator unseal` with threshold Shamir key shards or use auto-unseal.                        |
| `permission denied (403)`             | Token or AppRole policy lacks read permission on specific path. | Inspect associated HCL policy and ensure `path "secret/data/*" { capabilities = ["read"] }` is granted. |
| `token expired and cannot be renewed` | Lease duration reached maximum TTL limit.                       | Re-authenticate client AppRole to obtain a fresh token.                                                 |

## References

- [Vault Documentation](https://developer.hashicorp.com/vault/docs)
- [Vault Kubernetes Tutorial](https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-sidecar)
