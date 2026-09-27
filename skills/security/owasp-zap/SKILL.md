---
name: owasp-zap
description: Expert OWASP ZAP (Zed Attack Proxy) assistance covering automated vulnerability scanning, spidering, and DAST in CI/CD. Use when scanning web apps for OWASP Top 10 vulnerabilities, automating scans, or penetration testing.
---

# OWASP ZAP (Zed Attack Proxy)

OWASP ZAP is the world's most widely used free web app scanner. It is perfect for developers and functional testers who are new to penetration testing, as well as automated CI/CD pipelines.

## When to Use

- **Automated DAST in CI/CD Pipelines**: Running automated Dynamic Application Security Testing against deployed staging applications.
- **Passive Traffic Security Auditing**: Analyzing HTTP traffic for missing security headers, insecure cookies, and information disclosure.
- **Automated Spidering & API Fuzzing**: Crawling web applications and parsing OpenAPI/Swagger specs to discover unlinked endpoints.
- **Open-Source Penetration Testing**: Providing a zero-cost, open-source alternative to commercial web vulnerability scanners.

## Quick Start

```bash
# Run a quick scan against a URL
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://www.example.com
```

## Core Concepts

#Active vs Passive Scanning

- **Passive Scan**: Inspects proxied requests and responses without mutating data (safe for production; detects missing CSP, cookie flags).
- **Active Scan**: Injects malicious payloads (SQLi, XSS, Path Traversal) to find exploitable vulnerabilities (mutates data; staging only):

```bash
# Run ZAP Docker Baseline Scan (Passive Security Audit)
docker run -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py \
  -t https://staging.example.com -r zap_report.html
```

#ZAP Automation Framework (YAML)

Declarative configuration for running complex automated security workflows in CI/CD:

```yaml
# zap-automation.yaml
env:
  contexts:
    - name: "Staging App"
      urls: ["https://staging.example.com"]
jobs:
  - type: spider
    parameters:
      maxDuration: 5
  - type: activeScan
    parameters:
      maxScanDurationInMins: 15
  - type: report
    parameters:
      template: traditional-html
      reportDir: /zap/wrk/
      reportFile: zap-active-report.html
```

#Automated API Scanning from OpenAPI Specification

Imports OpenAPI / Swagger endpoints and tests each parameter for injection vulnerabilities:

```bash
docker run -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-api-scan.py \
  -t https://staging.example.com/api/v1/swagger.json -f openapi -r api_security_report.html
```

## Common Patterns

### Baseline DAST Scan in GitHub Actions

**Problem**: Vulnerabilities like SQL injection or XSS are only detected after release to production.

**Solution**:
Run automated ZAP baseline container scans in CI/CD:

```yaml
- name: Run OWASP ZAP Baseline Scan
  uses: zaproxy/action-baseline@v0.12.0
  with:
    target: "https://staging.example.com"
    rules_file_name: ".zap/rules.tsv"
    fail_action: true
```

## Best Practices (2026)

**Do**:

- **Incorporate ZAP Baseline Scan into Pull Request CI**: Fail builds if high-confidence vulnerabilities (e.g. SQLi) or critical missing headers appear.
- **Authenticate Scans with Script-Based Authentication**: Provide ZAP with credentials to spider and scan authenticated user routes.
- **Configure Scan Rulesets**: Ignore non-critical warnings or third-party tracking scripts by tuning ZAP alert thresholds.
- **Archive HTML and SARIF Reports as CI Artifacts**: Upload SARIF scan results directly into GitHub Security Code Scanning alerts.

**Don't**:

- **Don't run Active Scans against live production environments**: Active testing submits random payloads that can corrupt real database records.
- **Don't rely solely on DAST**: Combine ZAP dynamic testing with SAST (Semgrep, SonarQube) and dependency scanning (Trivy).
- **Don't scan external third-party services**: Constrain scanning strictly to your verified staging domain context.

## Troubleshooting

| Error                   | Cause                | Solution                                                         |
| :---------------------- | :------------------- | :--------------------------------------------------------------- |
| `Scan takes forever`    | Spider got stuck.    | Exclude logout URLs or calendar/looping paths from the context.  |
| `Authentication Failed` | ZAP couldn't log in. | Use the ZAP Desktop UI to record a Login Sequence (Zest Script). |

## References

- [OWASP ZAP](https://www.zaproxy.org/)
- [ZAP Docker Docs](https://www.zaproxy.org/docs/docker/)
