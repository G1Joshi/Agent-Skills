---
name: kotlin
description: Kotlin programming for Android, coroutines, and JVM development. Use for .kt files.
---

# Kotlin

Modern Kotlin development with coroutines, null safety, and idiomatic patterns.

## When to Use

- Working with `.kt` files
- Android app development
- JVM backend with Spring Boot/Ktor
- Multiplatform projects (KMP)

## Quick Start

```kotlin
data class User(
    val id: String,
    val name: String,
    val email: String,
    val createdAt: Instant = Clock.System.now()
)

suspend fun fetchUser(id: String): User? {
    return apiService.getUser(id)
}
```

## Core Concepts

### Null Safety

```kotlin
// Nullable types
val name: String? = null

// Safe calls
val length = name?.length

// Elvis operator
val len = name?.length ?: 0

// Smart casts
if (name != null) {
    println(name.length) // Smart cast to String
}

// Not-null assertion (use sparingly)
val len = name!!.length
```

### Data Classes & Sealed Classes

```kotlin
data class User(
    val id: String,
    val name: String,
    val email: String
)

sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val message: String) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

// Exhaustive when
fun handleResult(result: Result<User>) = when (result) {
    is Result.Success -> println(result.data)
    is Result.Error -> println(result.message)
    Result.Loading -> println("Loading...")
}
```

## Common Patterns

### Coroutines

```kotlin
// Suspend function
suspend fun fetchData(): List<Item> {
    return withContext(Dispatchers.IO) {
        api.fetchItems()
    }
}

// Parallel execution
suspend fun loadDashboard(): Dashboard {
    return coroutineScope {
        val user = async { fetchUser() }
        val orders = async { fetchOrders() }
        Dashboard(user.await(), orders.await())
    }
}

// Flow for streams
fun observeUsers(): Flow<List<User>> = flow {
    while (true) {
        emit(fetchUsers())
        delay(5000)
    }
}.flowOn(Dispatchers.IO)
```

### Extension Functions

```kotlin
fun String.isValidEmail(): Boolean {
    return Regex("^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}\$").matches(this)
}

fun <T> List<T>.secondOrNull(): T? = getOrNull(1)

inline fun <T> Result<T>.onSuccess(action: (T) -> Unit): Result<T> {
    if (this is Result.Success) action(data)
    return this
}
```

## Best Practices

**Do**:

- Use data classes for DTOs
- Prefer immutability (`val` over `var`)
- Use sealed classes for state
- Use coroutines for async work

**Don't**:

- Use `!!` without null check
- Create utility classes (use extensions)
- Block main thread with `runBlocking`
- Ignore cancellation in coroutines

## Troubleshooting

| Error                   | Cause                | Solution                  |
| ----------------------- | -------------------- | ------------------------- |
| `NullPointerException`  | Force unwrap on null | Use safe call `?.`        |
| `CancellationException` | Coroutine cancelled  | Handle or propagate       |
| `IllegalStateException` | Invalid state access | Check state before access |

## References

- [Kotlin Official Docs](https://kotlinlang.org/docs/)
- [Android Kotlin Guides](https://developer.android.com/kotlin)
