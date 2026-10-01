---
name: groovy
description: Expert Apache Groovy assistance covering dynamic typing, closures, AST transformations, and Gradle/Jenkins scripting. Use when writing Gradle build scripts, Jenkins pipelines, or JVM scripting utilities.
---

# Groovy

Groovy v4 adds **Switch Expressions**, Records, and Sealed Types. It remains the key to **Gradle** and Jenkins Pipelines.

## When to Use

- **CI/CD Pipeline Automation (Jenkinsfile)**: Writing declarative and scripted Jenkins CI/CD automation pipelines.
- **Gradle Build Scripts**: Authoring and maintaining Gradle build scripts for Java, Kotlin, and Android projects.
- **JVM Scripting & Prototyping**: Writing concise scripting automation with full access to the Java ecosystem.
- **Spock Testing Framework**: Writing expressive, readable BDD unit and integration tests for Java and Groovy apps.

## Quick Start

```groovy
// Dynamic collection operations with closures
def users = [
    [name: 'Alice', role: 'admin'],
    [name: 'Bob', role: 'developer'],
    [name: 'Charlie', role: 'admin']
]

def adminNames = users.findAll { it.role == 'admin' }.collect { it.name }
println "Admins: ${adminNames.join(', ')}"
```

## Core Concepts

### Dynamic Typing with Optional Static Compilation (`@CompileStatic`)

Blends dynamic scripting with high-performance static bytecode compilation:

```groovy
import groovy.transform.CompileStatic

@CompileStatic
class Calculator {
    int add(int a, int b) {
        return a + b // Compiles to direct Java bytecode without dynamic dispatch
    }
}
```

### Closures & Builder Pattern

First-class executable code blocks powering Gradle and Jenkins DSLs:

```groovy
// Jenkinsfile Pipeline syntax
pipeline {
    agent any
    stages {
        stage('Build & Test') {
            steps {
                sh 'gradle clean check'
            }
        }
    }
    post {
        failure {
            echo "Build failed! Triggering alert notification."
        }
    }
}
```

### Collections & GPath Navigation

Manipulates lists, maps, and nested data with concise expressions:

```groovy
def users = [
    [name: 'Alice', role: 'admin', active: true],
    [name: 'Bob', role: 'member', active: false],
    [name: 'Charlie', role: 'admin', active: true]
]

// GPath: Find names of active admins
def activeAdminNames = users.findAll { it.active && it.role == 'admin' }*.name
println activeAdminNames // ["Alice", "Charlie"]
```

## Common Patterns

### Declarative Jenkinsfile Pipeline

**Problem**: Complex CI/CD workflows hard to maintain in imperative shell scripts.

**Solution**:
Use declarative Groovy pipeline syntax with stages and post actions:

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'gradle build'
            }
        }
        stage('Test') {
            steps {
                sh 'gradle test'
            }
        }
    }
    post {
        always {
            junit '**/build/test-results/**/*.xml'
        }
    }
}
```

## Best Practices

**Do**:

- Use `@CompileStatic` on Production Services: Enable static compilation on performance-critical backend classes to match pure Java speed.
- Leverage the Spock Framework: Use Spock (`given:`, `when:`, `then:`) for highly readable testing of Java applications.
- Use the Safe Navigation Operator (`?.`): Prevent `NullPointerException` errors using Groovy's null-safe navigation (`user?.profile?.email`).
- Keep Jenkinsfiles Declarative: Prefer Declarative Pipelines over complex, untestable Scripted Pipelines.

**Don't**:

- Write complex business backends without static typing: Dynamic dispatch without type checks introduces runtime bugs.
- Use `def` everywhere in large codebases: Declare explicit parameter and return types to aid readability and IDE autocompletion.
- Mix closures with unmanaged global state: Keep closures pure to prevent thread race conditions in concurrent pipelines.

## Troubleshooting

| Error                                                  | Cause                                                        | Solution                                                                           |
| :----------------------------------------------------- | :----------------------------------------------------------- | :--------------------------------------------------------------------------------- |
| `groovy.lang.MissingMethodException`                   | Method called with wrong name or argument types dynamically. | Verify method name and consider adding `@CompileStatic` for compile-time checking. |
| `NullPointerException on property access`              | Attempting to access property on null reference.             | Use safe navigation operator: `person?.address?.city`.                             |
| `Script Security: Scripts not permitted to use method` | Jenkins sandbox blocking unapproved method invocation.       | Approve method in Jenkins In-process Script Approval settings.                     |

## References

- [Apache Groovy](https://groovy-lang.org/)
