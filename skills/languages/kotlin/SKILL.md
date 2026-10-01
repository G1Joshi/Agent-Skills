---
name: kotlin
description: Expert Kotlin assistance covering coroutines, Flow, null safety, extension functions, sealed classes/interfaces, and Kotlin Multiplatform. Use when developing Android applications, server-side Kotlin services with Ktor/Spring, or sharing cross-platform business logic.
---

# Kotlin

Modern Kotlin development with coroutines, null safety, and idiomatic patterns.

## When to Use

- **Modern Android Application Development**: Google's official, primary language for native Android and Jetpack Compose.
- **Server-Side Microservices (Ktor / Spring Boot)**: Writing expressive, concise, null-safe enterprise web backends.
- **Kotlin Multiplatform (KMP)**: Sharing business logic, data models, and networking across Android, iOS, Desktop, and Web.
- **Asynchronous Coroutines & Reactive Flows**: Managing concurrent background tasks and streams without callback hell.

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

### Kotlin Coroutines & Structured Concurrency

Lightweight cooperative multitasking with automated cancellation propagation:

```kotlin
import kotlinx.coroutines.*

suspend fun fetchUserProfile(userId: String): UserProfile = coroutineScope {
    // Run two network fetches in parallel
    val profileDeferred = async { api.getProfile(userId) }
    val ordersDeferred = async { api.getOrders(userId) }

    val profile = profileDeferred.await()
    val orders = ordersDeferred.await()
    profile.copy(orders = orders)
}
```

### Kotlin Flow (Asynchronous Cold Streams)

Reactive streams with built-in backpressure and transformation operators:

```kotlin
import kotlinx.coroutines.flow.*

fun streamStockPrices(symbol: String): Flow<Double> = flow {
    while (true) {
        emit(api.getCurrentPrice(symbol))
        delay(1000)
    }
}.map { it * 1.05 } // Apply transformation
 .flowOn(Dispatchers.IO)
```

### Extension Functions & Scope Functions

Extends existing classes without inheritance and scopes variable operations:

```kotlin
// Extension function on String
fun String.toSlug(): String = lowercase().replace(" ", "-").replace(Regex("[^a-z0-9-]"), "")

// Scope function (let, apply, run, also)
val user = User().apply {
    name = "Alex"
    role = "Lead"
}
```

## Common Patterns

### Parallel Coroutine Execution

**Problem**: Fetching multiple remote resources concurrently without blocking the main execution thread.

**Solution**:

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

**Problem**: Adding domain-specific utility operations to standard or library types without inheritance.

**Solution**:

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

- Leverage Kotlin Coroutines over Reactive Streams: Replace complex RxJava pipelines with clean coroutines and Flow.
- Use Sealed Interfaces for UI State: Model UI and domain state using `sealed interface` for exhaustive `when` expressions.
- Specify Dispatchers Explicitly: Use `Dispatchers.IO` for disk/network I/O, `Dispatchers.Default` for CPU math, and `Dispatchers.Main` for UI.
- Prefer Value Classes (`@JvmInline value class`): Create zero-allocation domain primitives for IDs and units of measure.

**Don't**:

- Use `GlobalScope.launch`: Always use structured concurrency with scoped lifecycles to prevent goroutine/coroutine leaks.
- Use the `!!` force-unwrap operator: Handle nullables cleanly using `?.let { ... }` or Elvis operator `?:`.
- Expose mutable collections: Expose read-only `List<T>` interfaces; keep `MutableList<T>` private inside classes.

## Troubleshooting

| Error                   | Cause                | Solution                  |
| ----------------------- | -------------------- | ------------------------- |
| `NullPointerException`  | Force unwrap on null | Use safe call `?.`        |
| `CancellationException` | Coroutine cancelled  | Handle or propagate       |
| `IllegalStateException` | Invalid state access | Check state before access |

## References

- [Kotlin Official Docs](https://kotlinlang.org/docs/)
- [Android Kotlin Guides](https://developer.android.com/kotlin)
