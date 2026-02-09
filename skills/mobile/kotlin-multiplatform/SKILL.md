---
name: kotlin-multiplatform
description: Kotlin Multiplatform for shared code across iOS and Android. Use for cross-platform Kotlin.
---

# Kotlin Multiplatform

Shared Kotlin code across iOS, Android, and other platforms.

## When to Use

- Sharing business logic
- iOS and Android codesharing
- Multiplatform libraries
- Native UI per platform

## Quick Start

```kotlin
// shared/src/commonMain/kotlin/Greeting.kt
class Greeting {
    private val platform = getPlatform()

    fun greet(): String {
        return "Hello, ${platform.name}!"
    }
}

expect fun getPlatform(): Platform

interface Platform {
    val name: String
}
```

## Core Concepts

### Expected/Actual

```kotlin
// commonMain
expect class HttpClient() {
    suspend fun get(url: String): String
}

// androidMain
actual class HttpClient {
    actual suspend fun get(url: String): String {
        return OkHttpClient.newCall(Request.Builder().url(url).build())
            .await().body?.string() ?: ""
    }
}

// iosMain
actual class HttpClient {
    actual suspend fun get(url: String): String {
        return NSURLSession.sharedSession.dataTaskWithURL(NSURL(string = url)!!)
    }
}
```

### Architecture

```kotlin
// Shared ViewModel
class UserViewModel(private val repository: UserRepository) {
    private val _user = MutableStateFlow<User?>(null)
    val user: StateFlow<User?> = _user.asStateFlow()

    fun loadUser(id: String) {
        coroutineScope.launch {
            _user.value = repository.getUser(id)
        }
    }
}

// Repository
class UserRepository(private val api: ApiClient, private val db: Database) {
    suspend fun getUser(id: String): User {
        return db.getUser(id) ?: api.fetchUser(id).also {
            db.saveUser(it)
        }
    }
}
```

## Common Patterns

### Platform-Specific UI

```kotlin
// Android (Compose)
@Composable
fun UserScreen(viewModel: UserViewModel) {
    val user by viewModel.user.collectAsState()
    user?.let { UserCard(it) }
}

// iOS (SwiftUI)
struct UserScreen: View {
    @ObservedObject var viewModel: UserViewModelWrapper

    var body: some View {
        if let user = viewModel.user {
            UserCard(user: user)
        }
    }
}
```

### Build Configuration

```kotlin
// build.gradle.kts
kotlin {
    androidTarget()
    iosX64()
    iosArm64()
    iosSimulatorArm64()

    sourceSets {
        commonMain.dependencies {
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.8.0")
            implementation("io.ktor:ktor-client-core:2.3.0")
        }
        androidMain.dependencies {
            implementation("io.ktor:ktor-client-okhttp:2.3.0")
        }
        iosMain.dependencies {
            implementation("io.ktor:ktor-client-darwin:2.3.0")
        }
    }
}
```

## Best Practices

**Do**:

- Share business logic, not UI
- Use Ktor for networking
- Use SQLDelight for database
- Test in commonTest

**Don't**:

- Force UI sharing
- Ignore iOS memory model
- Skip platform testing
- Mix paradigms

## Troubleshooting

| Issue            | Cause               | Solution                 |
| ---------------- | ------------------- | ------------------------ |
| iOS memory issue | Freezing rules      | Check Kotlin/Native docs |
| Build error      | Version mismatch    | Align KMP versions       |
| Type mismatch    | Expect/actual issue | Check signature match    |

## References

- [KMP Documentation](https://kotlinlang.org/docs/multiplatform.html)
- [KMP Samples](https://github.com/JetBrains/kotlin-multiplatform-dev-docs)
