---
name: trivy
description: Trivy container security scanner. Use for container security.
---

# Trivy

Trivy (by Aqua Security) is a comprehensive and versatile security scanner. It is famous for being incredibly fast, easy to install (single binary), and covering a wide range of targets (Containers, Filesystem, Git repos, AWS).

## When to Use

- **Docker Image Scanning**: The gold standard for fast image scanning in CI.
- **Kubernetes Scanning**: Scanning a running cluster for vulnerabilities.
- **SBOM Generation**: Creating a Software Bill of Materials (CycloneDX/SPDX).

## Quick Start

```bash
# Scan a container image
trivy image python:3.4-alpine

# Scan local filesystem (dependencies + secrets + misconfigs)
trivy fs .

# Scan a git repo
trivy repo https://github.com/knqyf263/trivy
```

## Core Concepts

### Scanners

Trivy runs multiple scanners in parallel:

- **Vuln**: CVEs in OS packages (apk, deb, rpm) and language deps (npm, pip, go.mod).
- **Misconfig**: IaC scans (Terraform, CloudFormation, K8s manifests).
- **Secret**: Hardcoded passwords/keys.
- **License**: License compliance.

### Client/Server Mode

Trivy can run standalone (Download DB -> Scan) or in Client/Server mode (Server holds DB, Client connects) for faster CI runs.

## Best Practices (2025)

**Do**:

- **Use `.trivyignore`**: To suppress false positives or accepted risks.
- **Scan Base Images**: Ensure your `FROM` image is clean (e.g., use `alpine` or `distroless`).
- **Generate SBOM**: Run `trivy image --format cyclonedx` to export an SBOM for compliance.

**Don't**:

- **Don't run full scans on every commit**: It might be slow on huge repos. Scan on Push/PR and nightly.
- **Don't ignore Misconfigurations**: Trivy creates alerts for running as root in Docker; fix these.

## Troubleshooting

| Error               | Cause                    | Solution                                                                             |
| :------------------ | :----------------------- | :----------------------------------------------------------------------------------- |
| `DB Download Error` | Rate limiting / Network. | Use `TRIVY_OFFLINE_SCAN=true` if using --skip-db-update inside a restricted network. |
| `API Rate Limit`    | GitHub API limit.        | Set `GITHUB_TOKEN` env var for Trivy to use.                                         |

## References

- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
