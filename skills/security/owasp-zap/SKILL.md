---
name: owasp-zap
description: OWASP ZAP security testing proxy. Use for security testing.
---

# OWASP ZAP (Zed Attack Proxy)

OWASP ZAP is the world's most widely used free web app scanner. It is perfect for developers and functional testers who are new to penetration testing, as well as automated CI/CD pipelines.

## When to Use

- **CI/CD Automation**: "DAST in the pipeline". Run a baseline scan on every PR.
- **Budget constraints**: It's free and open-source (vs Burp Pro's license).
- **Headless Scanning**: Controlling the scanner via API or CLI (Docker).

## Quick Start (Docker)

```bash
# Run a quick scan against a URL
docker run -t owasp/zap2docker-stable zap-baseline.py -t https://www.example.com
```

## Core Concepts

### Active Scan (Attack)

ZAP modifies requests to attack the application (SQLi, XSS, Command Injection). Use with caution.

### Passive Scan

ZAP watches traffic (via Proxy) and reports alerts without modifying requests (e.g., missing headers, cookie flags). Safe for production.

### HUD (Heads Up Display)

Injects the ZAP UI directly into your browser, allowing you to control the scan while browsing the target site.

## Best Practices (2025)

**Do**:

- **Automate Baseline Scans**: integrate `zap-baseline.py` in GitHub Actions for quick sanity checks.
- **Authenticate**: Configure ZAP to handle login (Authentication Context) so it can scan authenticated routes.
- **Filter False Positives**: DAST tools are noisy. Create a Context file to ignore irrelevant alerts.

**Don't**:

- **Don't Attack Unauthorized Targets**: ZAP is a weapon. Ensure you have permission.
- **Don't rely solely on DAST**: Combine with SAST (SonarQube) and SCA (Snyk).

## Troubleshooting

| Error                   | Cause                | Solution                                                         |
| :---------------------- | :------------------- | :--------------------------------------------------------------- |
| `Scan takes forever`    | Spider got stuck.    | Exclude logout URLs or calendar/looping paths from the context.  |
| `Authentication Failed` | ZAP couldn't log in. | Use the ZAP Desktop UI to record a Login Sequence (Zest Script). |

## References

- [OWASP ZAP](https://www.zaproxy.org/)
- [ZAP Docker Docs](https://www.zaproxy.org/docs/docker/)
