---
name: snyk
description: Snyk security scanning for vulnerabilities in code and dependencies. Use for security scanning.
---

# Snyk

Security platform for finding and fixing vulnerabilities.

## When to Use

- Dependency vulnerability scanning
- Container image scanning
- Infrastructure as code security
- CI/CD security gates

## Quick Start

```bash
# Install
npm install -g snyk

# Authenticate
snyk auth

# Test for vulnerabilities
snyk test

# Monitor project
snyk monitor
```

## Core Concepts

### CLI Commands

```bash
# Test dependencies
snyk test --all-projects

# Fix vulnerabilities
snyk fix

# Test container
snyk container test <image>

# Test IaC
snyk iac test terraform/
```

### CI/CD Integration

```yaml
# GitHub Actions
- name: Snyk Security Scan
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    args: --severity-threshold=high
```

## Best Practices

**Do**: Run in CI/CD, set severity thresholds, monitor continuously
**Don't**: Ignore critical vulnerabilities, skip container scans

## References

- [Snyk Documentation](https://docs.snyk.io/)
