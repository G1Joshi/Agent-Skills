---
name: kotlin-multiplatform
description: Expert Kotlin Multiplatform (KMP) assistance covering expect/actual declarations, shared business logic across iOS/Android, Compose Multiplatform, and Ktor client integration. Use when sharing domain models, networking, or persistence across platforms while retaining native UI.
---

# Kotlin Multiplatform (KMP)

Kotlin Multiplatform (KMP) allows you to share code between Android, iOS, Web, and Desktop. It emphasizes sharing logic (Business, Data, Networking) while allowing for native or shared (Compose Multiplatform) UIs.

## When to Use

- **Cross-Platform Shared Logic**: Sharing core business logic, data models, networking, and validation across Android and iOS apps.
- **Native UI Independence**: Retaining 100% native UI performance (SwiftUI on iOS, Jetpack Compose on Android) while sharing domain code.
- **Compose Multiplatform**: Building shared user interfaces across Android, iOS, Desktop (JVM), and Web using Kotlin Compose.
- **SDK & Library Development**: Authoring multiplatform mobile libraries published to Maven Central and CocoaPods/Swift Package Manager.

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

### Source Sets Hierarchy (commonMain vs Platform Sets)

Shared code lives in `commonMain`; platform-specific source sets bridge native OS features:

```text
shared/src/
  ├── commonMain/kotlin/     # Shared business logic, Ktor, SQLDelight
  ├── androidMain/kotlin/    # Android-specific APIs & Context
  └── iosMain/kotlin/        # iOS Objective-C / Swift interop
```

### `expect` / `actual` Platform Declarations

Defines a common contract that must be implemented by each target platform:

```kotlin
// commonMain: Contract declaration
expect class PlatformSecureStorage() {
    fun store(key: String, value: String)
    fun retrieve(key: String): String?
}

// iosMain: Actual implementation using iOS Keychain
actual class PlatformSecureStorage actual constructor() {
    actual fun store(key: String, value: String) { /* iOS SecItemAdd */ }
    actual fun retrieve(key: String): String? { /* iOS SecItemCopyMatching */ return null }
}
```

### Shared Persistence with SQLDelight / Room KMP

Compiles SQL queries into type-safe Kotlin data classes shared across platforms:

```kotlin
// commonMain: Shared Database driver setup
class DatabaseDriverFactory(private val driver: SqlDriver) {
    fun createDatabase(): AppDatabase = AppDatabase(driver)
}
// Android uses AndroidSqliteDriver; iOS uses NativeSqliteDriver
```

## Common Patterns

### Shared Ktor Client Across iOS and Android

**Problem**: Duplicating HTTP request logic and deserialization schemas across platforms.  
**Solution**: Define shared Ktor HttpClient in `commonMain`.

```kotlin
// commonMain/src/ApiClient.kt
class ApiClient(engine: HttpClientEngine) {
    private val client = HttpClient(engine) {
        install(ContentNegotiation) { json(Json { ignoreUnknownKeys = true }) }
    }

    suspend fun getItems(): List<Item> = client.get("https://api.example.com/items").body()
}

// androidMain: ApiClient(OkHttp.create())
// iosMain: ApiClient(Darwin.create())
```

## Best Practices

**Do**:

- Export Swift-Friendly Frameworks: Configure `shared.podspec` or Swift Package export with transitive dependencies enabled.
- Use SKIE for Coroutines & Flow Interop: Generate native Swift `async/await` and `@Observable` wrappers for Kotlin coroutines.
- Keep UI Frameworks Decoupled: Share domain and network logic in `commonMain` while letting iOS teams use native SwiftUI idioms.
- Automate Multiplatform CI/CD: Run Gradle builds on macOS runners to validate both Android and iOS targets in CI pipelines.

**Don't**:

- Leak Android `Context` into `commonMain`: Keep domain logic pure and dependency-injected.
- Expose raw Kotlin coroutine Job types to Swift: Wrap shared flows with SKIE or custom cancellation tokens.
- Ignore iOS memory management (ARC): Be mindful of reference cycles when sharing objects across the Kotlin/Native boundary.

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
