---
name: eclipse
description: Expert Eclipse IDE assistance covering Java development (JDT), Maven/Gradle m2e plugins, workspace configuration, and debugging. Use when building and debugging enterprise Java applications.
---

# Eclipse IDE

Eclipse was the dominant Java IDE for a decade. While IntelliJ has taken the lead, Eclipse remains critical for **legacy enterprise** projects and specific industries (Embedded, Auto).

## When to Use

- **Enterprise Java & Jakarta EE Development**: Developing large-scale legacy enterprise systems with Maven and Gradle.
- **OSGi Plugin Architecture**: Building modular desktop applications on the Eclipse Rich Client Platform (RCP).
- **Embedded C/C++ Development (CDT)**: Developing firmware and embedded systems with GNU toolchains.
- **Headless Eclipse JDT Language Server**: Powering Java LSP support in modern text editors (Neovim, VS Code, Helix).

## Quick Start

```bash
# Compile and run project using Maven wrapper outside Eclipse
./mvnw clean compile

# Import existing Maven project into Eclipse:
# File > Import... > Maven > Existing Maven Projects
```

## Core Concepts

### Maven Project Configuration (.classpath and pom.xml)

Standard Java 21 enterprise project structure:

```xml
<!-- pom.xml -->
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.company.enterprise</groupId>
    <artifactId>billing-engine</artifactId>
    <version>2026.1.0</version>
    <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
</project>
```

### Eclipse Memory Optimization (eclipse.ini)

Configuring JVM parameters for large codebases:

```ini
# eclipse.ini
-startup
plugins/org.eclipse.equinox.launcher_1.6.800.v20240513-1750.jar
--launcher.appendVmargs
-vm
/Library/Java/JavaVirtualMachines/temurin-21.jdk/Contents/Home/bin/java
-vmargs
-Xms1024m
-Xmx4096m
-XX:+UseG1GC
-XX:+UseStringDeduplication
-Dfile.encoding=UTF-8
```

### Headless Eclipse JDT.LS Language Server Integration

Connecting modern editors to Eclipse Java engine:

```bash
# Launch Eclipse JDT Language Server in background
java \
  -Declipse.application=org.eclipse.jdt.ls.core.id1 \
  -Dosgi.bundles.defaultStartLevel=4 \
  -Declipse.product=org.eclipse.jdt.ls.core.product \
  -Dlog.level=ALL \
  -Xmx2G \
  -jar ./plugins/org.eclipse.equinox.launcher_*.jar \
  -configuration ./config_mac \
  -data ~/.jdtls_workspace
```

## Common Patterns

### Maven Build Lifecycle Configuration (.project)

**Problem**: Synchronize Eclipse project dependencies with external Maven builds.  
**Solution**: Ensure M2E Maven buildCommand is present in `.project`.

```xml
<!-- .project -->
<projectDescription>
  <name>my-enterprise-app</name>
  <buildSpec>
    <buildCommand>
      <name>org.eclipse.m2e.core.maven2Builder</name>
    </buildCommand>
  </buildSpec>
  <natures>
    <nature>org.eclipse.jdt.core.javanature</nature>
    <nature>org.eclipse.m2e.core.maven2Nature</nature>
  </natures>
</projectDescription>
```

## Best Practices

**Do**:

- Tune `eclipse.ini` to allocate sufficient heap memory (`-Xmx4096m`) and use G1GC garbage collection.
- Import projects as Maven or Gradle projects rather than raw generic Eclipse projects.
- Configure Eclipse Code Formatter profiles (`formatter.xml`) in version control to enforce team consistency.
- Clean and rebuild projects (`Project -> Clean...`) if internal incremental compiler caches get out of sync.

**Don't**:

- Commit Eclipse workspace metadata folders (`.metadata/`) to version control.
- Use 32-bit JDKs; always run Eclipse on a modern 64-bit JDK (Temurin, Corretto, Zulu 21+).
- Install unverified third-party plugins that degrade IDE startup and editor performance.

## Troubleshooting

| Error                                                  | Cause                                                                   | Solution                                                                    |
| :----------------------------------------------------- | :---------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `Project configuration is not up-to-date with pom.xml` | Modified `pom.xml` without updating Eclipse project model.              | Right-click project > **Maven > Update Project... (Alt+F5)**.               |
| `Java compiler level does not match installed JDK`     | Project facet set to different Java version than workspace JRE.         | Open Project Properties > Java Compiler > Enable project specific settings. |
| `Eclipse OutOfMemoryError`                             | Default `-Xmx` in `eclipse.ini` too low for large enterprise workspace. | Increase heap in `eclipse.ini`: `-Xmx4096m`.                                |

## References

- [Eclipse Foundation](https://www.eclipse.org/)
