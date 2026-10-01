---
name: insomnia
description: Expert Insomnia REST/GraphQL/gRPC client assistance covering environment variables, request chaining, plugins, and test automation. Use when designing, testing, and debugging APIs.
---

# Insomnia

Insomnia is the lightweight alternative to Postman. v9.0+ focuses on **Local-First** philosophy (Local Vault) and **Git Sync**.

## When to Use

- **REST, GraphQL & gRPC API Design and Debugging**: Modern, lightweight desktop API client with environment chaining.
- **Inso CLI Automation for CI/CD**: Running automated API test suites and linting OpenAPI specifications in pipelines.
- **Environment & Variable Chaining**: Extracting tokens from login endpoints and injecting them into subsequent requests.
- **Git-Sync Team Collaboration**: Versioning API collections, design documents, and tests directly in Git repositories.

## Quick Start

```json
// Insomnia Base Environment Configuration
{
  "base_url": "https://api.staging.example.com/v1",
  "auth_token": "Bearer eyJhbGciOi...",
  "tenant_id": "tenant_1234"
}
```

## Core Concepts

### Environment Variables & Chained Request Responses

Extracting bearer token from authentication response:

```json
// In Sub-Environment configuration
{
  "base_url": "https://api.staging.example.com",
  "client_id": "app_client_prod",
  "auth_token": "{% response 'body', 'req_login_01', 'b64::JC5hY2Nlc3NfdG9rZW4=::46b', 'no-history', 60 %}"
}
```

Subsequent requests reference `{{ base_url }}/v1/users` with header `Authorization: Bearer {{ auth_token }}`.

### Inso CLI Test Execution in CI Pipelines

Running automated API test collections headlessly:

```bash
# Lint OpenAPI specification file
inso lint spec "Company API Spec"

# Run automated functional test suite against staging environment
inso run test "User Lifecycle Test Suite" --env "Staging" --ci
```

### gRPC Service Invocation

Calling gRPC methods with server reflection:

1. Create new request -> Select **gRPC**.
2. Enter server URL: `grpc.infra.internal:50051`.
3. Enable **Server Reflection** to auto-load Protobuf method definitions.
4. Input JSON payload and click **Send** to stream responses.

## Common Patterns

### Automated CI Collection Testing with Inso CLI

**Problem**: Run Insomnia API tests automatically inside CI/CD pipelines.  
**Solution**: Execute tests via `inso` CLI.

```bash
# Install inso CLI
npm install -g insomnia-inso

# Run test suite headlessly in CI
inso run test "User API Test Suite" --env "Staging" --ci
```

## Best Practices

**Do**:

- Sync Insomnia collections to Git repositories for version control and peer review of API changes.
- Use Inso CLI in CI/CD pipelines to validate OpenAPI specifications and run regression tests.
- Organize environments hierarchically (Base Environment -> Staging, Production sub-environments).
- Use response chaining (`{% response ... %}`) to eliminate manual copy-pasting of auth tokens.

**Don't**:

- Store plaintext production credentials in public Git-synced collections.
- Skip OpenAPI linting; maintain clean, valid specs that generate accurate SDKs.
- Duplicate request URLs across endpoints; reference `{{ base_url }}` consistently.

## Troubleshooting

| Error                                           | Cause                                             | Solution                                                               |
| :---------------------------------------------- | :------------------------------------------------ | :--------------------------------------------------------------------- |
| `SSL Certificate validation failed in Insomnia` | Self-signed SSL certificate in local development. | Uncheck "Validate SSL certificates" in Insomnia Preferences > General. |
| `Template tag failed: Request has no response`  | Chained request hasn't been executed yet.         | Execute the referenced upstream request (`req_login`) once.            |
| `CORS Error in Insomnia Web Client`             | Web version subject to browser CORS policies.     | Use desktop native Insomnia client or configure CORS proxy.            |

## References

- [Insomnia Documentation](https://docs.insomnia.rest/)
