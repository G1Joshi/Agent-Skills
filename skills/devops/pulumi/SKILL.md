---
name: pulumi
description: Expert Pulumi Infrastructure as Code (IaC) assistance covering real programming languages (TypeScript, Python, Go, C#), state management, and component resources. Use when managing cloud infrastructure with full language power.
---

# Pulumi

Pulumi lets you define infrastructure using TypeScript, Python, Go, or C#. It offers the power of a real language (loops, functions, classes) for IaC. 2025 highlights include **Pulumi ESC** for secret management.

## When to Use

- **Modern Programming Languages for Infrastructure as Code (IaC)**: TypeScript, Python, Go, and C# instead of domain-specific languages (DSL).
- **Modular Component Resources**: Encapsulating complex cloud topologies into reusable, typed classes and libraries.
- **Real-Time Integration & Unit Testing**: Writing standard unit tests for infrastructure using Vitest, Jest, or PyTest.
- **Kubernetes & Multi-Cloud Native**: Provisioning AWS, Azure, GCP, and Kubernetes workloads in a single unified language.

## Quick Start

```typescript
import * as pulum from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

const bucket = new aws.s3.Bucket("my-bucket", {
  acl: "private",
});

export const bucketName = bucket.id;
```

## Core Concepts

#Modular Infrastructure Component with TypeScript

Creating an encapsulated, reusable microservice infrastructure component:

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

interface MicroserviceArgs {
  vpcId: pulumi.Input<string>;
  subnetIds: pulumi.Input<string[]>;
  imageTag: string;
}

export class ContainerMicroservice extends pulumi.ComponentResource {
  public readonly url: pulumi.Output<string>;

  constructor(
    name: string,
    args: MicroserviceArgs,
    opts?: pulumi.ComponentResourceOptions,
  ) {
    super("custom:cloud:ContainerMicroservice", name, {}, opts);

    // ECR Repository
    const repo = new aws.ecr.Repository(
      `${name}-repo`,
      {
        imageScanningConfiguration: { scanOnPush: true },
      },
      { parent: this },
    );

    // Application Load Balancer
    const alb = new aws.lb.LoadBalancer(
      `${name}-alb`,
      {
        internal: false,
        subnets: args.subnetIds,
      },
      { parent: this },
    );

    this.url = alb.dnsName;
    this.registerOutputs({ url: this.url });
  }
}

// In index.ts:
const service = new ContainerMicroservice("billing", {
  vpcId: "vpc-0123456789",
  subnetIds: ["subnet-a", "subnet-b"],
  imageTag: "v2.1.0",
});
export const endpoint = service.url;
```

#Secret Management & Stack Configuration

Encrypting sensitive credentials automatically:

```bash
# Configure encrypted secret in stack configuration
pulumi config set --secret dbPassword "SuperSecurePassword2026!"

# Read secret in Pulumi program
```

```typescript
const config = new pulumi.Config();
const dbPassword = config.requireSecret("dbPassword"); // Returned as Output<string> (masked)
```

#Pulumi CLI Operations

Previewing and applying infrastructure changes:

```bash
# Preview proposed changes with detailed diff
pulumi preview

# Deploy infrastructure to cloud stack
pulumi up --yes

# Destroy stack resources cleanly
pulumi destroy
```

## Common Patterns

### Typed ComponentResource for Reusable Infrastructure Modules

**Problem**: Copy-pasting raw cloud resource definitions across staging and production stacks.

**Solution**:
Encapsulate resources into reusable Pulumi ComponentResources:

```typescript
import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";

interface MicroserviceArgs {
  vpcId: pulumi.Input<string>;
  imageUri: pulumi.Input<string>;
  port: number;
}

export class Microservice extends pulumi.ComponentResource {
  public readonly url: pulumi.Output<string>;

  constructor(
    name: string,
    args: MicroserviceArgs,
    opts?: pulumi.ComponentResourceOptions,
  ) {
    super("custom:app:Microservice", name, {}, opts);

    const sg = new aws.ec2.SecurityGroup(
      `${name}-sg`,
      {
        vpcId: args.vpcId,
        ingress: [
          {
            protocol: "tcp",
            fromPort: args.port,
            toPort: args.port,
            cidrBlocks: ["0.0.0.0/0"],
          },
        ],
      },
      { parent: this },
    );

    // Output URL
    this.url = pulumi.interpolate`http://service.${name}.internal:${args.port}`;
    this.registerOutputs({ url: this.url });
  }
}
```

## Best Practices (2026)

- **Do** encapsulate related infrastructure into custom `ComponentResource` classes for reusability.
- **Do** treat secret values strictly as `pulumi.Output<string>` to ensure automated masking in console logs.
- **Do** run unit tests against infrastructure mocks before executing deployments in CI/CD pipelines.
- **Do** configure Pulumi Cloud or an S3/GCS backend for reliable stack state locking and auditing.
- **Don't** call `.get()` on Pulumi Outputs during resource declaration; use `.apply()` to chain asynchronous outputs.
- **Don't** commit plaintext secrets to `Pulumi.<stack>.yaml` files; use `--secret` flag.
- **Don't** mix side-effects (e.g. database schema migrations) directly inside Pulumi IaC definitions.

## Troubleshooting

| Error                                         | Cause                                                               | Solution                                                              |
| :-------------------------------------------- | :------------------------------------------------------------------ | :-------------------------------------------------------------------- |
| `Diagnostics: Resource '...' already exists`  | Attempting to create resource that exists outside of Pulumi state.  | Import resource into state: `pulumi import <type> <name> <id>`.       |
| `Stack locked by another operation`           | Previous update interrupted or crashed before releasing state lock. | Cancel lock after verifying no operation is running: `pulumi cancel`. |
| `Error: Output<T> cannot be passed to string` | Accessing `.apply()` outputs as plain synchronous strings.          | Wrap dependent values with `pulumi.interpolate` or use `.apply()`.    |

## References

- [Pulumi Documentation](https://www.pulumi.com/docs/)
