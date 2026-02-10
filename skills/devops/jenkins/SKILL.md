---
name: jenkins
description: Jenkins automation server with pipelines and plugins. Use for CI/CD pipelines.
---

# Jenkins

Jenkins is the grandfather of CI, but still widely used in enterprise. In 2025, it runs primarily as **Code** (Jenkinsfile) and often on Kubernetes.

## When to Use

- **Legacy/Enterprise**: You have massive, complex, custom requirements that only Jenkins plugins can handle.
- **Fineness of Control**: You need absolute control over the build environment.
- **On-Premise**: You cannot use Cloud CI.

## Quick Start (Declarative Pipeline)

```groovy
// Jenkinsfile
pipeline {
    agent { docker { image 'node:20' } }
    stages {
        stage('Build') {
            steps {
                sh 'npm ci'
                sh 'npm run build'
            }
        }
    }
}
```

## Core Concepts

### Master / Agent

Master (Controller) orchestrates. Agents (Executors) run the jobs. 2025 Best Practice: Ephemeral Agents on Kubernetes.

### Plugins

The ecosystem is huge. Blue Ocean, Credentials Binding, Git.

### CasC (Configuration as Code)

Configure the Jenkins Master itself using YAML, not the UI.

## Best Practices (2025)

**Do**:

- **Use Declarative Pipelines**: Avoid Scripted Pipelines unless absolutely necessary.
- **Use Ephemeral Agents**: Spin up a Pod for each build, destroy it after. No "Snowflake" build servers.
- **Use Shared Libraries**: For reusable Groovy logic across pipelines.

**Don't**:

- **Don't configure jobs in UI**: Always use `Jenkinsfile`.
- **Don't overload the Master**: Run **zero** builds on the built-in controller node.

## References

- [Jenkins Documentation](https://www.jenkins.io/)
