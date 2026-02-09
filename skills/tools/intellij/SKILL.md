---
name: intellij
description: IntelliJ IDEA IDE for Java/Kotlin with refactoring and debugging. Use for JVM development.
---

# IntelliJ IDEA

IDE for JVM languages including Java, Kotlin, and Scala.

## When to Use

- Java/Kotlin development
- Spring Boot applications
- Gradle/Maven projects
- Android development (via Android Studio)

## Quick Start

```kotlin
// Create new project: File -> New -> Project
// Select: Kotlin, Gradle (Kotlin DSL)

fun main() {
    println("Hello, World!")
}
```

## Core Concepts

### Essential Shortcuts

```
# Navigation
Cmd/Ctrl + Shift + F    - Find in files
Cmd/Ctrl + E            - Recent files
Cmd/Ctrl + B            - Go to declaration
Cmd/Ctrl + Shift + O    - Go to file

# Refactoring
Shift + F6              - Rename
Cmd/Ctrl + Alt + M      - Extract method
Cmd/Ctrl + Alt + V      - Extract variable
Cmd/Ctrl + Alt + L      - Reformat code

# Running
Shift + F10             - Run
Shift + F9              - Debug
Cmd/Ctrl + Shift + F10  - Run current file
```

### Run Configurations

```xml
<!-- .idea/runConfigurations/Main.xml -->
<component name="ProjectRunConfigurationManager">
  <configuration name="Main" type="JetRunConfigurationType">
    <option name="MAIN_CLASS_NAME" value="com.example.MainKt" />
    <option name="VM_PARAMETERS" value="-Xmx512m" />
    <option name="PROGRAM_PARAMETERS" value="--debug" />
    <module name="myproject.main" />
  </configuration>
</component>
```

## Common Patterns

### Live Templates

```
# Create: Settings -> Editor -> Live Templates

# Template: logd
Log.d(TAG, "$END$")

# Template: sout
System.out.println($END$);

# Template: test (for JUnit)
@Test
fun `$NAME$`() {
    $END$
}
```

### Code Inspections

```xml
<!-- .idea/inspectionProfiles/Project_Default.xml -->
<component name="InspectionProjectProfileManager">
  <profile version="1.0">
    <inspection_tool class="KotlinDeprecation" enabled="true" level="WARNING" />
    <inspection_tool class="UnusedSymbol" enabled="true" level="WARNING" />
  </profile>
</component>
```

## Best Practices

**Do**:

- Use intention actions (Alt+Enter)
- Configure code style per project
- Use structural search & replace
- Learn keyboard shortcuts

**Don't**:

- Commit .idea files blindly
- Ignore code inspections
- Skip indexing process
- Disable type hints

## Troubleshooting

| Issue              | Cause               | Solution                                  |
| ------------------ | ------------------- | ----------------------------------------- |
| Slow IDE           | Low heap            | Increase in Help > Edit Custom VM Options |
| Red symbols        | Indexing incomplete | Wait or invalidate caches                 |
| Gradle sync failed | JDK mismatch        | Check Project Structure > SDKs            |

## References

- [IntelliJ Documentation](https://www.jetbrains.com/help/idea/)
- [IntelliJ Tips](https://www.jetbrains.com/idea/guide/)
