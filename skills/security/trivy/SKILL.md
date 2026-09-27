---
name: trivy
description: Expert Trivy security scanner assistance covering container image scanning, filesystem CVEs, git repositories, and IaC misconfigs. Use when scanning Docker images, auditing Kubernetes manifests, or running security checks in CI.
---

# Trivy

Trivy (by Aqua Security) is a comprehensive and versatile security scanner. It is famous for being incredibly fast, easy to install (single binary), and covering a wide range of targets (Containers, Filesystem, Git repos, AWS).

## When to Use

- **Comprehensive Security Scanner for Containers**: Scanning container images for OS package vulnerabilities (Debian, Alpine, RedHat) and language packages.
- **Kubernetes Cluster Misconfiguration Scanning**: Auditing live Kubernetes workloads against CIS benchmarks and security standards.
- **Git Repository & Secrets Auditing**: Scanning codebases for hardcoded credentials, API keys, and sensitive tokens.
- **Software Bill of Materials (SBOM) Generation**: Generating CycloneDX and SPDX format SBOMs for software supply chain compliance.

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

#Multi-Target Scanning Architecture

Trivy scans container images, filesystems, Git repositories, AWS accounts, and Kubernetes clusters using a unified engine:

```bash
# 1. Scan Container Image
trivy image --severity HIGH,CRITICAL node:20-alpine

# 2. Scan Local Filesystem & Dependencies
trivy fs --scanners vuln,secret,misconfig .

# 3. Scan Kubernetes Cluster
trivy k8s --report summary cluster
```

#Software Bill of Materials (SBOM) Export

Generates standardized inventory of all components and licenses in container images:

```bash
# Export CycloneDX JSON SBOM
trivy image --format cyclonedx --output sbom.json my-org/api:latest
```

#GitHub Actions CI Security Gate

Blocks container builds containing unpatched critical CVEs:

```yaml
# .github/workflows/container-scan.yml
- name: Run Trivy Vulnerability Scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: "my-org/api:${{ github.sha }}"
    format: "sarif"
    output: "trivy-results.sarif"
    severity: "CRITICAL,HIGH"
    exit-code: "1"
```

## Common Patterns

### Container Image Vulnerability Scanning with Exit Code Gates

**Problem**: Unvetted base images introduce known Remote Code Execution (RCE) flaws into cloud deployments.

**Solution**:
Execute Trivy container scans in CI with automated blocking on critical vulnerabilities:

```bash
# Scan container image and exit with error code 1 if CRITICAL CVEs exist
trivy image \
  --severity CRITICAL,HIGH \
  --exit-code 1 \
  --ignore-unfixed \
  myapp:latest
```

## Best Practices (2026)

**Do**:

- **Use Distroless / Chainguard Minimal Images**: Reduce container vulnerabilities by 90%+ by stripping out package managers and shells.
- **Integrate Trivy in Container Build Pipelines**: Run Trivy immediately after `docker build` before pushing images to container registries.
- **Generate SBOMs for Releases**: Attach SPDX or CycloneDX SBOMs to GitHub releases for supply chain transparency.
- **Leverage `.trivyignore` Conservatively**: Document justifiable reasons and expiration dates when ignoring specific CVEs.

**Don't**:

- **Don't scan without updating vulnerability DBs**: Ensure Trivy has access to download the latest vulnerability database cache before scanning.
- **Don't ignore hardcoded secret alerts**: Treat leaked API keys flagged by Trivy secret scanning as compromised immediately.
- **Don't allow unmitigated Critical CVEs into production**: Patch base images or update libraries when active exploits exist.

## Troubleshooting

| Error               | Cause                    | Solution                                                                             |
| :------------------ | :----------------------- | :----------------------------------------------------------------------------------- |
| `DB Download Error` | Rate limiting / Network. | Use `TRIVY_OFFLINE_SCAN=true` if using --skip-db-update inside a restricted network. |
| `API Rate Limit`    | GitHub API limit.        | Set `GITHUB_TOKEN` env var for Trivy to use.                                         |

## References

- [Trivy Documentation](https://aquasecurity.github.io/trivy/)
