---
name: intellij
description: Expert IntelliJ IDEA assistance covering Java/Kotlin, project SDKs, debugging, refactoring, run configurations, and plugins. Use when building enterprise JVM applications with maximum productivity.
---

# IntelliJ IDEA

IntelliJ IDEA is the premier IDE for Java and Kotlin. v2025.1 introduces **Java 24** support, **K2 Mode** (Beta/Stable), and a unified **AI Assistant**.

## When to Use

- **Enterprise JVM Development**: Building Java, Kotlin, Scala, and Groovy applications with unmatched code intelligence.
- **Spring Boot & Microservice Tooling**: Visualizing bean dependencies, endpoint mappings, and Spring Data repositories.
- **Advanced Automated Refactoring**: Safe across-the-board method extraction, interface implementation, and symbol renaming.
- **Integrated Profiler & Debugger**: Memory snapshots, async stack traces, thread dump analysis, and CPU profiling.

## Quick Start

```bash
# Run Maven or Gradle build using wrapper
./gradlew bootRun

# Useful keyboard shortcuts:
# Shift+Shift: Search Everywhere
# Ctrl+Alt+L / Cmd+Option+L: Reformat Code
# Shift+F10 / Ctrl+R: Run Application
```

## Core Concepts

### Run / Debug Configuration with VM Options

Configuring production-grade local execution:

```xml
<!-- .run/ApiApplication.run.xml -->
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="ApiApplication" type="SpringBootApplicationConfigurationType" factoryName="Spring Boot">
    <module name="api-service.main" />
    <option name="SPRING_BOOT_MAIN_CLASS" value="com.company.api.ApiApplication" />
    <option name="VM_PARAMETERS" value="-Xms512m -Xmx2048m -XX:+UseG1GC -Dspring.profiles.active=local" />
    <extension name="coverage" />
    <method v="2">
      <option name="Make" enabled="true" />
    </method>
  </configuration>
</component>
```

### Inspecting Memory & Thread Dumps with IntelliJ Profiler

Diagnosing memory leaks and deadlocks:

- Click **Run with IntelliJ Profiler** or attach to running JVM process.
- Open **Memory** tab to inspect heap allocation by class.
- Click **Capture Memory Snapshot** (`.hprof`) to find instances retaining large byte arrays.
- Inspect **Threads** view to detect thread synchronization bottlenecks.

### Structural Search & Replace (SSR)

Finding and modifying patterns across entire codebases:

```text
// Search Template: Catch blocks catching raw generic Exception
catch ($ExceptionType$ $e$) {
    $Statements$;
}
// Constraint: $ExceptionType$ = java.lang.Exception
// Replace Template: Narrow to specific checked domain exceptions
```

## Common Patterns

### JVM Memory Profiling and Heap Dump Analysis

**Problem**: Diagnose memory leaks and high GC overhead in Spring Boot applications.  
**Solution**: Launch app with JVM profiling arguments.

```bash
# JVM options for heap profiling
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/var/log/heapdump.hprof
-XX:+UseG1GC
-Xms2g -Xmx4g
```

## Best Practices

**Do**:

- Share standardized team run configurations by checking **Store as project file** (`.run/*.run.xml`).
- Use IntelliJ's built-in Git client with visual 3-way merge conflict resolution.
- Allocate sufficient memory to the IDE in `Help -> Change Memory Settings` (typically 3GB-4GB).
- Use IntelliJ inspections and run **Analyze Code -> Inspect Code...** before merging PRs.

**Don't**:

- Commit the entire `.idea/` folder; maintain a proper `.gitignore` excluding `workspace.xml` and user caches.
- Disable annotation processing when using Lombok or MapStruct; enable in **Settings -> Annotation Processors**.
- Ignore yellow inspection warnings in Java/Kotlin code; address warnings to keep code maintainable.

## Troubleshooting

| Error                                            | Cause                                                               | Solution                                                                                                            |
| :----------------------------------------------- | :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------ |
| `Cannot resolve symbol '...' in editor`          | Project SDK not configured or Maven/Gradle dependencies not loaded. | Open Project Structure > SDKs and ensure JDK is selected, then sync Gradle.                                         |
| `OutOfMemoryError: Java heap space during build` | IntelliJ build process allocated insufficient memory.               | Increase memory: **Settings > Build, Execution, Deployment > Compiler > Shared build process heap size (2048 MB)**. |
| `Red code everywhere after git pull`             | Indices corrupted.                                                  | Click **File > Invalidate Caches... > Invalidate and Restart**.                                                     |

## References

- [IntelliJ IDEA Documentation](https://www.jetbrains.com/idea/documentation/)
