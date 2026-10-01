---
name: jetpack-compose
description: Expert Jetpack Compose assistance covering declarative Android UI, state hoisting, remember/mutableStateOf, composition lifecycles, and Material 3 theming. Use when developing native Android user interfaces, creating smooth UI animations, or optimizing Compose recomposition performance.
---

# Jetpack Compose

Jetpack Compose is Android's modern toolkit for building native UIs. It simplifies and accelerates UI development on Android with less code, powerful tools, and intuitive Kotlin APIs.

## When to Use

- **Modern Android Native Development**: Google's official, recommended declarative UI toolkit for native Android applications.
- **Dynamic Theming & Animations**: Building rich, fluid UI designs with Material 3, dynamic color theming, and spring animations.
- **Custom Design Systems**: Composing reusable UI building blocks with clean state hoisting and automated previews.
- **Interoperability with Existing Code**: Integrating declarative Compose views seamlessly inside legacy Android XML layouts or ViewGroups.

## Quick Start

```kotlin
// build.gradle.kts needs composed enabled

// MainActivity.kt
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.lifecycle.viewmodel.compose.viewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                MyApp()
            }
        }
    }
}

@Composable
fun MyApp(viewModel: CounterViewModel = viewModel()) {
    // Collecting state from ViewModel
    val count by viewModel.uiState.collectAsState()

    Scaffold(
        floatingActionButton = {
            FloatingActionButton(onClick = { viewModel.increment() }) {
                Text("+")
            }
        }
    ) { padding ->
        Text(
            text = "Count: $count",
            modifier = Modifier.padding(padding)
        )
    }
}
```

## Core Concepts

### Declarative UI & Recomposition Lifecycle

Compose functions describe UI directly in Kotlin. Recomposition skips functions whose inputs have not changed:

```kotlin
@Composable
fun OrderStatusBadge(status: String, modifier: Modifier = Modifier) {
    val backgroundColor = when (status) {
        "COMPLETED" -> Color(0xFF10B981)
        "PENDING" -> Color(0xFFF59E0B)
        else -> Color(0xFF6B7280)
    }

    Box(
        modifier = modifier
            .background(backgroundColor, shape = RoundedCornerShape(8.dp))
            .padding(horizontal = 12.dp, vertical = 6.dp)
    ) {
        Text(text = status, color = Color.White, style = MaterialTheme.typography.labelMedium)
    }
}
```

### State Hoisting with `remember` & `mutableStateOf`

State flows down to composables through parameters; events flow up through lambda callbacks:

```kotlin
@Composable
fun SearchBar(
    query: String,
    onQueryChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    OutlinedTextField(
        value = query,
        onValueChange = onQueryChange,
        placeholder = { Text("Search transactions...") },
        leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
        singleLine = true,
        modifier = modifier.fillMaxWidth()
    )
}
```

### Side-Effects & Coroutine Scopes (LaunchedEffect)

Manages side-effects that execute outside the composition lifecycle safely without restarting on irrelevant recompositions:

```kotlin
@Composable
fun UserSessionTracker(userId: String, analytics: AnalyticsTracker) {
    // Only restarts when userId changes
    LaunchedEffect(userId) {
        analytics.trackUserSession(userId)
    }
}
```

## Common Patterns

### State Hoisting and ViewModel Integration

**Problem**: Tight coupling of state management inside composable functions prevents UI previews and testing.  
**Solution**: Hoist state into ViewModel and pass state down with event callbacks up.

```kotlin
@Composable
fun CounterScreen(viewModel: CounterViewModel = viewModel()) {
    val count by viewModel.count.collectAsStateWithLifecycle()
    CounterContent(count = count, onIncrement = viewModel::increment)
}

@Composable
fun CounterContent(count: Int, onIncrement: () -> Unit) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text(text = "Current: $count", style = MaterialTheme.typography.headlineMedium)
        Button(onClick = onIncrement) {
            Text("Increment")
        }
    }
}
```

## Best Practices

**Do**:

- Use `@Stable` and `@Immutable` Annotations: Mark domain model classes to enable Compose compiler smart recomposition optimizations.
- Always Pass `modifier: Modifier = Modifier`: Allow parent composables to specify sizing, padding, and constraints.
- Collect State with Lifecycle Awareness: Use `collectAsStateWithLifecycle()` from Kotlin Flow to prevent background state emissions.
- Provide `@Preview` Annotations: Create previews with light and dark mode variants to validate designs without deploying to devices.

**Don't**:

- Instantiate heavy objects inside composables: Wrap object allocations in `remember { ... }` to prevent reinstantiation on every frame.
- Perform I/O in Composable functions: Keep composables pure; delegate data fetching to ViewModels and Coroutine dispatchers.
- Hardcode color values: Reference `MaterialTheme.colorScheme` tokens to ensure seamless dark theme support.

## Troubleshooting

| Error                                                     | Cause                                                                | Solution                                                          |
| :-------------------------------------------------------- | :------------------------------------------------------------------- | :---------------------------------------------------------------- |
| `@Composable invocations can only happen from context...` | Calling a composable from a standard function.                       | Add `@Composable` annotation to the caller.                       |
| Infinite Recomposition                                    | Updating state inside the composition without a side-effect wrapper. | Move update logic to a callback or `SideEffect`/`LaunchedEffect`. |
| `ViewModel` state not updating UI                         | Using a non-observable type or forgetting `collectAsState`.          | Use `StateFlow`/`MutableState` and collect it properly.           |

## References

- [Jetpack Compose Documentation](https://developer.android.com/jetpack/compose)
- [Compose Material 3](https://developer.android.com/jetpack/compose/designsystems/material3)
- [Accompanist Libraries](https://google.github.io/accompanist/)
