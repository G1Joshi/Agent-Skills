---
name: vault
description: HashiCorp Vault secrets management. Use for secrets.
---

# HashiCorp Vault

Vault is a tool for securely accessing secrets. A secret is anything that you want to tightly control access to, such as API keys, passwords, or certificates. Vault provides a unified interface to any secret while providing tight access control and recording a detailed audit log.

## When to Use

- **Dynamic Secrets**: Generating temporary AWS credentials (TTL 15m) for a specific task.
- **Encryption as a Service**: Encrypting application data (Credit Cards) without the app managing the keys (Transit Engine).
- **Kubernetes Secrets**: Injecting secrets into pods securely without Etcd.

## Quick Start (Dev Mode)

```bash
vault server -dev
export VAULT_ADDR='http://127.0.0.1:8200'

# Write a secret
vault kv put secret/hello foo=world

# Read a secret
vault kv get secret/hello
```

## Core Concepts

### Sealing

Vault data is encrypted at rest. When Vault starts, it is "Sealed". Unsealing requires a threshold of keys (Shamir's Secret Sharing) to reconstruct the master key.

### Engines

Modules that handle different types of secrets:

- `kv`: Key-Value storage (static).
- `aws`: Dynamic AWS IAM users.
- `pki`: Dynamic x.509 Certificates.

### Auth Methods

How you log in to Vault: Token, AppRole (Machines), Kubernetes (Pods), GitHub (Humans).

## Best Practices (2025)

**Do**:

- **Use Auto-Unseal**: Integrate with AWS KMS / Azure Key Vault to unseal automatically (Manual unsealing is painful for uptime).
- **Inject via Sidecar**: In K8s, use the Vault Agent Injector to drop secrets into `/vault/secrets/config` rather than calling the API directly.
- **Enable Audit Logs**: Essential for knowing "Who read the database password?".

**Don't**:

- **Don't use Root Token**: Generate it, configure auth methods, then revoke it.
- **Don't store huge files**: Vault is for secrets (KB), not files (MB).

## References

- [Vault Documentation](https://developer.hashicorp.com/vault/docs)
- [Vault Kubernetes Tutorial](https://developer.hashicorp.com/vault/tutorials/kubernetes/kubernetes-sidecar)
