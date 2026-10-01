---
name: openshift
description: Expert Red Hat OpenShift assistance covering oc CLI, DeploymentConfigs, Routes, Security Context Constraints (SCC), and BuildConfigs. Use when deploying enterprise Kubernetes applications on Red Hat OpenShift.
---

# OpenShift

Red Hat OpenShift is an enterprise Kubernetes platform offering full-stack automated operations, integrated developer tooling, and OpenShift Virtualization for co-locating VMs and containers.

## When to Use

- **Enterprise Kubernetes Distribution**: Red Hat OpenShift providing turnkey security, developer tooling, and compliance.
- **Source-to-Image (S2I) & BuildConfigs**: Automatically building container images directly from Git repositories.
- **OpenShift Routes & Ingress**: Routing external traffic with automated Let's Encrypt or corporate certificates.
- **Security Context Constraints (SCC)**: Enforcing strict multi-tenant container isolation and user namespace policies.

## Quick Start

```bash
# Login
oc login -u developer -p developer https://api.crc.testing:6443

# Create Project (Namespace)
oc new-project my-app

# Deploy from Source (Source-to-Image)
oc new-app nodejs~https://github.com/sclorg/nodejs-ex.git
```

## Core Concepts

### OpenShift BuildConfig & ImageStream (S2I)

Building containers from Git inside the cluster:

```yaml
apiVersion: image.openshift.io/v1
kind: ImageStream
metadata:
  name: billing-api
  namespace: prod-apps
---
apiVersion: build.openshift.io/v1
kind: BuildConfig
metadata:
  name: billing-api-build
  namespace: prod-apps
spec:
  source:
    type: Git
    git:
      uri: https://github.com/my-org/billing-service.git
      ref: main
  strategy:
    type: Source
    sourceStrategy:
      from:
        kind: ImageStreamTag
        name: nodejs:20-ubi9
        namespace: openshift
  output:
    to:
      kind: ImageStreamTag
      name: billing-api:latest
  triggers:
    - type: GitHub
      github:
        secretReference:
          name: webhook-secret
    - type: ConfigChange
```

### OpenShift Route for External Traffic

Exposing services with edge TLS termination:

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: billing-api-route
  namespace: prod-apps
spec:
  host: billing.apps.cluster.example.com
  to:
    kind: Service
    name: billing-api-service
    weight: 100
  port:
    targetPort: 8080
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
```

### OpenShift CLI (oc) Operations

Logging in and managing cluster projects:

```bash
# Log in to OpenShift cluster via OAuth token
oc login https://api.cluster.domain.com:6443 --token="$OC_TOKEN"

# Switch to project namespace
oc project prod-apps

# Trigger a build and follow output logs
oc start-build billing-api-build --follow
```

## Common Patterns

### Declarative Route with Edge TLS Termination

**Problem**: Ingress resources in OpenShift requiring specialized router features and certificates.

**Solution**:
Use OpenShift Route custom resources:

```yaml
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: api-route
  namespace: prod-apps
spec:
  host: api.cloud.example.com
  to:
    kind: Service
    name: api-service
  port:
    targetPort: 8080
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
```

## Best Practices

**Do**:

- Use Red Hat Universal Base Images (`ubi9-minimal`) for enterprise security and CVE patching guarantees.
- Manage OpenShift resources declaratively via GitOps using OpenShift GitOps (Argo CD).
- Adhere strictly to OpenShift `restricted-v2` Security Context Constraints (SCC); never run containers as root.
- Use `insecureEdgeTerminationPolicy: Redirect` on Routes to force HTTPS.

**Don't**:

- Grant `anyuid` or `privileged` SCC permissions to service accounts unless strictly necessary.
- Hardcode external cluster hostnames; use OpenShift Route domain wildcards.
- Perform manual cluster modifications via OpenShift Web Console without tracking in Git.

## Troubleshooting

| Error                                                            | Cause                                                                    | Solution                                                                            |
| :--------------------------------------------------------------- | :----------------------------------------------------------------------- | :---------------------------------------------------------------------------------- |
| `CrashLoopBackOff: container cannot run as root (SCC violation)` | OpenShift default `restricted-v2` SCC prevents root container execution. | Build container image with non-root user (`USER 1001`) or assign custom SCC.        |
| `oc: command not found`                                          | OpenShift CLI tools not installed in system PATH.                        | Download and install OpenShift client tools from Red Hat mirror.                    |
| `Build failed in BuildConfig`                                    | S2I (Source-to-Image) build pod ran out of memory.                       | Increase build pod resources: `oc patch bc/<name> -p '{"spec":{"resources":...}}'`. |

## References

- [OpenShift Documentation](https://docs.openshift.com/)
