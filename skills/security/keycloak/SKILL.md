---
name: keycloak
description: Expert Keycloak IAM assistance covering OpenID Connect realms, identity brokering, user federation, and client adapters. Use when configuring enterprise SSO, managing Keycloak realms, or securing microservices.
---

# Keycloak

Keycloak is an open-source Identity and Access Management solution aimed at modern applications and services. It makes it easy to secure applications and services with little to no code.

## When to Use

- **Self-Hosted Open-Source Identity Management**: Deploying an enterprise IAM solution on Kubernetes without commercial vendor lock-in.
- **Enterprise Federation (Active Directory / LDAP)**: Syncing users, groups, and credentials from corporate LDAP and Active Directory domains.
- **Identity Brokering & Social Logins**: Centralizing authentication across Google, GitHub, SAML 2.0, and OIDC identity providers.
- **Fine-Grained Authorization Services**: Defining attribute-based access control (ABAC) and resource permission policies.

## Quick Start

```bash
docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev
```

## Core Concepts

### Realm Architecture & Multi-Tenancy

Realms isolate groups of users, credentials, roles, and client applications completely:

```text
[ Master Realm (Administer Keycloak) ]
       ├── [ Realm: EnterpriseA ] ── (Users, Roles, Clients, LDAP Provider)
       └── [ Realm: EnterpriseB ] ── (Users, Roles, Clients, Google Provider)
```

### OIDC Client Registration (Public vs Confidential)

- **Confidential Clients**: Backend servers that maintain a `client_secret` securely.
- **Public Clients**: SPAs and mobile apps that authenticate via PKCE without secrets:

```json
{
  "clientId": "frontend-spa",
  "publicClient": true,
  "standardFlowEnabled": true,
  "redirectUris": ["https://app.example.com/*"],
  "webOrigins": ["https://app.example.com"],
  "pkceCodeChallengeMethod": "S256"
}
```

### Docker Deployment with Production Database

Running Keycloak in production mode connected to PostgreSQL:

```yaml
# docker-compose.yml
services:
  keycloak:
    image: quay.io/keycloak/keycloak:24.0
    command: start --optimized
    environment:
      KC_DB: postgres
      KC_DB_URL: jdbc:postgresql://postgres:5432/keycloak
      KC_DB_USERNAME: keycloak
      KC_DB_PASSWORD: secretpassword
      KC_HOSTNAME: auth.example.com
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: adminpassword
    ports:
      - "8080:8080"
```

## Common Patterns

### Client Credentials Flow for Service-to-Service Auth

**Problem**: Backend microservices calling other microservices require automated machine-to-machine authentication.

**Solution**:
Authenticate using Keycloak Client Credentials grant:

```bash
curl -X POST "http://keycloak:8080/realms/enterprise/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=order-service" \
  -d "client_secret=YOUR_CLIENT_SECRET"
```

## Best Practices

**Do**:

- Run Keycloak with `start --optimized`: Build container images with `kc.sh build` ahead of time to minimize container boot time in Kubernetes.
- Never Use the `master` Realm for Application Users: Create custom dedicated realms for applications; reserve `master` strictly for Keycloak admin.
- Enable PKCE on All Public Clients: Enforce S256 code challenge method on all single-page and mobile applications.
- Use Distributed Cache Replication (Infinispan): Configure Infinispan clustering when deploying multi-replica Keycloak pods to synchronize sessions.

**Don't**:

- Expose Keycloak administration console to the public internet: Protect `/admin` endpoints behind private VPNs or IP whitelists.
- Use embedded H2 database in production: Always use external, managed PostgreSQL or MySQL with automated backups.
- Neglect database migration planning during upgrades: Major Keycloak version updates require coordinated database schema migrations.

## Troubleshooting

| Error                                  | Cause                                                               | Solution                                                            |
| :------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------------------------ |
| `Invalid parameter: redirect_uri`      | Target redirect URI not listed in client's Valid Redirect URIs.     | Add exact scheme, host, and port to Keycloak client configuration.  |
| `KC-SERVICES0093: Invalid credentials` | Secret mismatch or user locked out by brute-force protection.       | Verify client secret and check user unlock status in Admin Console. |
| `Token signature verification failed`  | Microservice validating token against outdated Keycloak realm keys. | Flush JWKS public key cache in the resource server.                 |

## References

- [Keycloak Documentation](https://www.keycloak.org/documentation)
