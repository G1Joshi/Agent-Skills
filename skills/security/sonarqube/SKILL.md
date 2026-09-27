---
name: sonarqube
description: Expert SonarQube code quality and security scanning covering Quality Gates, static analysis (SAST), and test coverage tracking. Use when configuring SonarQube/SonarCloud, measuring code debt, or enforcing quality gates.
---

# SonarQube

SonarQube is the leading tool for continuous inspection of code quality. It detects bugs, vulnerabilities (SAST), and code smells in over 30 programming languages.

## When to Use

- **Continuous Code Quality & Clean Code Auditing**: Analyzing codebases for bugs, vulnerabilities, security hotspots, and code smells.
- **Quality Gates in Pull Requests**: Enforcing that new code meets strict quality standards (test coverage, zero new bugs) before merging.
- **Technical Debt & Maintainability Tracking**: Measuring duplication percentage, complexity scores, and estimated remediation time.
- **Enterprise Security Compliance**: Ensuring codebases comply with security standards (OWASP Top 10, CWE, SANS Top 25).

## Quick Start

```bash
docker run -d --name sonarqube -p 9000:9000 sonarqube:lts
# Login: admin/admin at http://localhost:9000
```

```yaml
# sonar-project.properties
sonar.projectKey=my-project
sonar.sources=src
sonar.host.url=http://localhost:9000
sonar.login=...
```

## Core Concepts

#The "Clean as You Code" Methodology

Focuses quality gate enforcement on "New Code" (modified in the PR) rather than legacy debt:

```
[ Developer Branch ] ──Pull Request──→ [ CI Scanner ] ──Analyze New Code──→ [ Quality Gate PASS / FAIL ]
```

#sonar-project.properties Configuration

Defines source paths, exclusions, test execution reports, and lcov coverage targets:

```ini
# sonar-project.properties
sonar.projectKey=enterprise-api-service
sonar.projectName=Enterprise API Service
sonar.sources=src
sonar.tests=tests
sonar.exclusions=**/node_modules/**,**/dist/**,**/*.spec.ts
sonar.javascript.lcov.reportPaths=coverage/lcov.info
sonar.qualitygate.wait=true
```

#SonarScanner CLI Execution

Runs static analysis and uploads results to SonarQube Server or SonarCloud:

```bash
sonar-scanner \
  -Dsonar.host.url=https://sonarqube.internal.corp \
  -Dsonar.token=$SONAR_TOKEN
```

## Common Patterns

### Maven / Gradle Sonar Scanner Pipeline

**Problem**: Code smells and security hotspots merge to main branch unnoticed.

**Solution**:
Run Sonar analysis during standard build jobs:

```bash
# Analyze with Maven passing project key and token
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=my_enterprise_app \
  -Dsonar.host.url=https://sonarqube.internal.net \
  -Dsonar.token=$SONAR_TOKEN \
  -Dsonar.qualitygate.wait=true
```

## Best Practices (2026)

**Do**:

- **Enforce the Quality Gate on Pull Requests**: Block merges if code coverage on new code is under 80% or if new security vulnerabilities are found.
- **Upload Real Code Coverage Reports**: Ensure unit test runs output valid LCOV or JaCoCo XML reports consumed by SonarQube.
- **Review Security Hotspots Interactively**: Investigate flagged security hotspots to confirm safe usage of cryptography and deserialization.
- **Use SonarLint in IDEs**: Run instant local analysis in VS Code/JetBrains to fix code smells before committing.

**Don't**:

- **Don't attempt to fix all legacy technical debt at once**: Adopt the Clean as You Code strategy; fix debt incrementally as files are modified.
- **Don't disable rules to bypass failing Quality Gates**: Address underlying architectural smells rather than weakening inspection rules.
- **Don't run SonarScanner on untested code**: Run tests and generate coverage reports before executing the Sonar scanner step.

## Troubleshooting

| Error                                              | Cause                                                                   | Solution                                                                           |
| :------------------------------------------------- | :---------------------------------------------------------------------- | :--------------------------------------------------------------------------------- |
| `Quality Gate failed: Coverage is below threshold` | New code lacks adequate unit tests or report file missing.              | Ensure coverage reports (lcov, jacoco) are generated and path specified in config. |
| `You are not authorized to run the analysis`       | Invalid or expired `SONAR_TOKEN`.                                       | Regenerate user/project token in SonarQube user security settings.                 |
| `Task failed: SonarQube server unreachable`        | Network firewall or proxy blocking connection to internal Sonar server. | Verify server status and ensure runner has network egress to host URL.             |

## References

- [SonarQube Documentation](https://docs.sonarqube.org/)
- [Clean Code Principles](https://www.sonarsource.com/clean-code/)
