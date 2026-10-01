---
name: snyk
description: Expert Snyk security platform assistance covering SCA (open-source dependencies), SAST (code), container images, and IaC. Use when scanning repositories for CVEs, remediating vulnerabilities, or securing CI/CD.
---

# Snyk

Snyk is a developer security platform. It finds and fixes vulnerabilities in your code (SAST), open source dependencies (SCA), container images, and infrastructure as code (IaC).

## When to Use

- **Developer-First Security Scanning**: Detecting vulnerabilities in open-source dependencies (Snyk Open Source) directly in IDEs and CI/CD.
- **Static Application Security Testing (SAST)**: Scanning source code for security flaws and code quality issues (Snyk Code).
- **Container Image Vulnerability Scanning**: Inspecting Docker and OCI container images for OS package CVEs and base image upgrade advice.
- **Infrastructure as Code (IaC) Scanning**: Identifying misconfigurations in Terraform, Kubernetes, Helm, and CloudFormation files.

## Quick Start

```bash
# Install CLI
npm install -g snyk

# Authenticate
snyk auth

# Test dependencies
snyk test

# Monitor (Continuous watching for new vulns)
snyk monitor
```

## Core Concepts

### Snyk CLI Dependency Auditing

Scans project manifest files against Snyk's proprietary vulnerability intelligence database:

```bash
# Scan npm / pip / Cargo dependencies for vulnerabilities
snyk test --severity-threshold=high

# Generate automated fix advice and upgrade dependencies
snyk fix
```

### Container Image Vulnerability Analysis

Analyzes base images and package managers, suggesting secure base image alternatives:

```bash
# Scan local Docker image
snyk container test my-org/api:latest --file=Dockerfile
```

### GitHub Actions CI/CD Integration

Blocks pull requests containing critical vulnerabilities:

```yaml
# .github/workflows/security.yml
- name: Run Snyk Security Scan
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    args: --severity-threshold=high --sarif-file-output=snyk.sarif
```

## Common Patterns

### Automated Snyk Container and Dependency Scan in CI

**Problem**: Deploying container images with critical OS or library vulnerabilities into Kubernetes clusters.

**Solution**:
Integrate Snyk testing into CI build steps with severity thresholds:

```bash
# Test Node dependencies and fail only on high/critical issues
snyk test --severity-threshold=high

# Test built Docker container image before pushing to registry
snyk container test myapp:latest --severity-threshold=critical --fail-on=upgradable
```

## Best Practices

**Do**:

- Integrate Snyk in Pre-Commit and IDEs: Catch vulnerabilities while authoring code using the Snyk VS Code / JetBrains extensions.
- Enforce Severity Thresholds in CI: Fail pull requests only on `high` or `critical` vulnerabilities to prevent pipeline gridlock.
- Scan Container Base Images Regularly: Leverage minimal base images like Alpine or Chainguard to minimize attack surfaces.
- Scan Infrastructure as Code: Run `snyk iac test` on Terraform and Kubernetes configs to prevent open security groups.

**Don't**:

- Ignore transitive dependencies: Vulnerabilities frequently live in nested child dependencies; use Snyk's automated PR fixes.
- Blindly ignore vulnerabilities with `.snyk` files: Require security team approval before adding temporary expiration ignores.
- Leave Snyk tokens unrotated: Rotate CI API tokens periodically in your Snyk organization settings.

## Troubleshooting

| Error             | Cause                  | Solution                                                            |
| :---------------- | :--------------------- | :------------------------------------------------------------------ |
| `Auth Failed`     | Token expired/missing. | Run `snyk auth` again or set `SNYK_TOKEN` env var.                  |
| `Too many issues` | Legacy codebase.       | Use `.snyk` file to ignore known/wont-fix issues or set a baseline. |

## References

- [Snyk Documentation](https://docs.snyk.io/)
- [Snyk CLI](https://docs.snyk.io/snyk-cli)
