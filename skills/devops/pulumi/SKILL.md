---
name: pulumi
description: Pulumi infrastructure as code with programming languages. Use for IaC.
---

# Pulumi

Pulumi lets you define infrastructure using TypeScript, Python, Go, or C#. It offers the power of a real language (loops, functions, classes) for IaC. 2025 highlights include **Pulumi ESC** for secret management.

## When to Use

- **Developers**: You prefer TypeScript over HCL YAML.
- **Complexity**: You need genuine logic (if/else, loops, external API calls) during infrastructure definition.
- **Testing**: You want to unit test your infrastructure code using standard test runners (Jest, Pytest).

## Quick Start (TypeScript)

```typescript
import * as pulum from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("my-bucket", {
  acl: "private",
});

export const bucketName = bucket.id;
```

## Core Concepts

### Programming Model

Unlike Terraform's declarative HCL, Pulumi executes your program to build a resource graph.

### Pulumi ESC (Environments, Secrets, Config)

Centralized secret management. Retrieve dynamic secrets (AWS temp creds) at runtime.

### Automation API

Embed infrastructure creation inside your own software. "Click to Deploy" features in SaaS products often use this.

## Best Practices (2025)

**Do**:

- **Use ComponentResources**: Abstract complexity into reusable Classes (e.g., `class MyMicroservice extends ComponentResource`).
- **Use Secrets Provider**: Don't store secrets in plaintext config. Pulumi encrypts config values by default.
- **Unit Test**: Use mocks to test that your Security Groups don't allow 0.0.0.0/0.

**Don't**:

- **Don't mix logic and state**: Keep side-effects (API calls) predictable.

## References

- [Pulumi Documentation](https://www.pulumi.com/docs/)
