---
name: sonarqube
description: SonarQube code quality and security. Use for code analysis.
---

# SonarQube

SonarQube is the leading tool for continuous inspection of code quality. It detects bugs, vulnerabilities (SAST), and code smells in over 30 programming languages.

## When to Use

- **Code Quality Gates**: "Block the merge if Code Coverage < 80%".
- **Technical Debt Management**: Tracking "Code Smells" and duplication over time.
- **Vulnerability Detection**: Finding SQL Injection, XSS, and hardcoded secrets in source code.

## Quick Start (Docker)

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

### Quality Gate

A set of conditions the project must meet (e.g., "No new Critical issues", "Coverage on New Code > 80%"). If failed, the CI pipeline fails.

### Clean Code

Sonar methodology: Attributes code as being Consistent, Intentional, Adaptable, and Responsible.

### SonarLint

IDE extension that runs Sonar rules locally _while you type_, fixing issues before commit.

## Best Practices (2025)

**Do**:

- **Focus on "New Code"**: It's hard to fix 5,000 old issues. Enforce strict gates on _New Code_ to stop the leak.
- **Use SonarLint**: Shift left. Fix it in the IDE.
- **Integrate with PRs**: Decorate Pull Requests (GitHub/GitLab) with comments on specific lines.

**Don't**:

- **Don't ignore "Info" or "Minor" smells**: They accumulate into a maintenance nightmare.
- **Don't include generated code**: Exclude `dist/`, `build/`, and generated clients from the scan.

## References

- [SonarQube Documentation](https://docs.sonarqube.org/)
- [Clean Code Principles](https://www.sonarsource.com/clean-code/)
