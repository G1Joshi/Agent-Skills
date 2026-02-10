---
name: kotlin-multiplatform
description: Kotlin Multiplatform for shared code. Use for cross-platform.
---

# Kotlin Multiplatform (KMP)

Kotlin Multiplatform (KMP) allows you to share code between Android, iOS, Web, and Desktop. It emphasizes sharing logic (Business, Data, Networking) while allowing for native or shared (Compose Multiplatform) UIs.

## When to Use

- Sharing complex business logic and data layers between mobile platforms.
- Building a "Super App" SDK to be used by other native apps.
- Teams with strong Kotlin expertise wanting to target iOS.
- Sharing UI code via Compose Multiplatform (stable for iOS in 2025).

## Quick Start

```kotlin
// commonMain/kotlin/Platform.kt
interface Platform {
    val name: String
}
expect fun getPlatform(): Platform

// androidMain/kotlin/Platform.kt
actual fun getPlatform(): Platform = object : Platform {
    override val name = "Android ${android.os.Build.VERSION.SDK_INT}"
}

// iosMain/kotlin/Platform.kt
import platform.UIKit.UIDevice
actual fun getPlatform(): Platform = object : Platform {
    override val name = UIDevice.currentDevice.systemName() + " " + UIDevice.currentDevice.systemVersion
}

// commonMain/kotlin/Greeting.kt
class Greeting {
    fun greet(): String = "Hello, ${getPlatform().name}!"
}
```

## Core Concepts

### Expect / Actual

Mechanism to define an interface in common code (`expect`) and provide platform-specific implementations (`actual`) in platform modules.

### Shared Module

A Gradle module usually named `shared` or `composeApp`. This compiles to an `.aar` for Android and a `.framework` (or XCFramework) for iOS.

### Compose Multiplatform

Google's declarative UI framework (Jetpack Compose) ported to iOS, Web, and Desktop by JetBrains. Allows sharing UI code 100%.

## Common Patterns

### Ktor + Kotlinx.Serialization

Use **Ktor** for multiplatform networking and **kotlinx.serialization** for JSON parsing. Both are pure Kotlin and work on all targets.

### SQLDelight / Room

Use **SQLDelight** or **Room** (KMP support active) for type-safe database access shared across platforms.

### Dependency Injection (Koin)

**Koin** is a popular pure Kotlin dependency injection framework that works seamlessly in KMP to manage singletons and factories.

## Best Practices

**Do**:

- Share **Business Logic**, **Data Models**, and **Networking Code**.
- Use **Compose Multiplatform** for UI if pixel-perfect native compliance isn't critical or for custom branded apps.
- Use **Coroutines** (Flow/Suspend) for all async operations.
- Test shared code in `commonTest`.

**Don't**:

- Don't try to share 100% of code if it degrades the user experience.
- Don't use Java-dependent libraries in `commonMain` (only pure Kotlin).
- Don't force `expect/actual` usage if a library (like KMP-NativeCoroutines) can solve the bridging better.

## Troubleshooting

| Error                                | Cause                                                                | Solution                                                     |
| :----------------------------------- | :------------------------------------------------------------------- | :----------------------------------------------------------- |
| `Unresolved reference` in commonMain | Using platform-specific API (java.util, android.\*).                 | Use KMP-compatible libraries (kotlinx-datetime).             |
| `C-interop` build errors             | iOS build configuration or missing headers.                          | Check `cocoapods` or `framework` config in build.gradle.kts. |
| `Memory Leaks` on iOS                | Circular references or freezing (mostly solved in new memory model). | Ensure newer Kotlin version (1.9+) is used.                  |

## References

- [Kotlin Multiplatform Wizard](https://kmp.jetbrains.com/)
- [Compose Multiplatform](https://www.jetbrains.com/lp/compose-multiplatform/)
- [Ktor Documentation](https://ktor.io/)
