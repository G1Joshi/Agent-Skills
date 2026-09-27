---
name: jenkins
description: Expert Jenkins automation server assistance covering declarative Jenkinsfiles, shared libraries, multi-branch pipelines, and plugins. Use when managing enterprise CI/CD build automation.
---

# Jenkins

Jenkins is the grandfather of CI, but still widely used in enterprise. In 2025, it runs primarily as **Code** (Jenkinsfile) and often on Kubernetes.

## When to Use

- **Self-Hosted Enterprise CI/CD Orchestration**: Highly customizable build pipelines behind corporate firewalls.
- **Declarative Jenkinsfile Pipelines**: Version-controlled pipelines with stages, environments, and automated rollback gates.
- **Distributed Agent Fleets**: Running parallel builds across dynamic Kubernetes pods, Docker containers, and VMs.
- **Legacy Migration & Complex Tooling Integrations**: Leveraging thousands of established community plugins.

## Quick Start

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

#Declarative Jenkinsfile with Docker Agents & Parallel Stages

Modern pipeline structure running in parallel stages:

```groovy
// Jenkinsfile
pipeline {
    agent {
        docker {
            image 'node:22-alpine'
            args '-u root:root'
        }
    }
    options {
        timeout(time: 1, unit: 'HOURS')
        disableConcurrentBuilds()
        ansiColor('xterm')
    }
    environment {
        CI = 'true'
        NPM_CONFIG_CACHE = "${WORKSPACE}/.npm"
    }
    stages {
        stage('Install') {
            steps {
                sh 'npm ci'
            }
        }
        stage('Quality Gates') {
            parallel {
                stage('Lint & Typecheck') {
                    steps {
                        sh 'npm run lint'
                        sh 'npm run typecheck'
                    }
                }
                stage('Unit Tests') {
                    steps {
                        sh 'npm test -- --coverage'
                    }
                    post {
                        always {
                            junit 'junit.xml'
                        }
                    }
                }
            }
        }
        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                withCredentials([string(credentialsId: 'STAGING_API_KEY', variable: 'API_KEY')]) {
                    sh 'npm run deploy:staging'
                }
            }
        }
    }
    post {
        failure {
            slackSend(channel: '#ci-alerts', color: 'danger', message: "Pipeline Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}")
        }
    }
}
```

#Kubernetes Dynamic Cloud Agents

Spawning ephemeral build pods dynamically in Kubernetes:

```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
metadata:
  labels:
    some-label: build-agent
spec:
  containers:
  - name: maven
    image: maven:3.9-eclipse-temurin-21
    command: ['cat']
    tty: true
'''
        }
    }
    stages {
        stage('Build') {
            steps {
                container('maven') {
                    sh 'mvn clean package -DskipTests'
                }
            }
        }
    }
}
```

#Jenkins Configuration as Code (JCasC)

Managing Jenkins master controller configuration declaratively:

```yaml
# jenkins.yaml
jenkins:
  systemMessage: "Enterprise Production CI/CD Controller - Managed via JCasC"
  numExecutors: 0 # Master runs zero builds; all work on agents
  mode: EXCLUSIVE
security:
  queueItemAuthenticator:
    authenticators:
      - global:
          strategy: triggeringUsersAuthorizationStrategy
```

## Common Patterns

### Declarative Pipeline with Docker Agent and Post-Build Notifications

**Problem**: Build environment drift across physical Jenkins worker nodes.

**Solution**:
Use isolated container execution in declarative Jenkinsfile:

```groovy
pipeline {
    agent {
        docker {
            image 'node:20-alpine'
            args '-u root'
        }
    }
    stages {
        stage('Install & Test') {
            steps {
                sh 'npm ci'
                sh 'npm test'
            }
        }
    }
    post {
        failure {
            slackSend channel: '#ci-alerts', message: "Job ${env.JOB_NAME} failed!"
        }
    }
}
```

## Best Practices (2026)

- **Do** always use Declarative Pipeline syntax (`pipeline {}`) rather than legacy Scripted Pipeline syntax.
- **Do** run builds exclusively on ephemeral agents (Kubernetes Pods or Docker containers); set `numExecutors: 0` on the master controller.
- **Do** store all secrets in Jenkins Credential Store and inject them using `withCredentials()`.
- **Do** manage master controller configuration using Jenkins Configuration as Code (JCasC).
- **Don't** install unverified third-party plugins; audit and minimize plugin counts to prevent security vulnerabilities.
- **Don't** hardcode sensitive API tokens or passwords directly inside `Jenkinsfile`.
- **Don't** run long-running builds directly on the Jenkins controller node.

## Troubleshooting

| Error                                         | Cause                                                          | Solution                                                                    |
| :-------------------------------------------- | :------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `java.lang.OutOfMemoryError: Java heap space` | Master/controller JVM heap limit exhausted by build history.   | Increase `-Xmx` parameter in Jenkins JVM options and discard old builds.    |
| `Scripts not permitted to use method`         | Groovy script attempting restricted method call under sandbox. | Navigate to Manage Jenkins > In-process Script Approval and approve method. |
| `Cannot connect to Docker daemon in agent`    | Docker socket not mounted into the executor container.         | Mount socket: `args '-v /var/run/docker.sock:/var/run/docker.sock'`.        |

## References

- [Jenkins Documentation](https://www.jenkins.io/)
