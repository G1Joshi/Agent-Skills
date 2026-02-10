---
name: jetpack-compose
description: Jetpack Compose Android declarative UI. Use for Android.
---

# Jetpack Compose

Jetpack Compose is Android's modern toolkit for building native UIs. It simplifies and accelerates UI development on Android with less code, powerful tools, and intuitive Kotlin APIs.

## When to Use

- New Android application development (Grid/List content, complex layouts).
- Migrating existing View-based apps incrementally (Interoperability).
- Sharing UI logic with Kotlin Multiplatform (Compose Multiplatform).

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

### Composable Functions

Functions annotated with `@Composable` are the building blocks. They describe specialized UI widgets or layouts. They can call other Composables.

### Recomposition

When the state of a Composable changes, the framework re-executes the function to update the UI. Smart logic ensures only necessary parts are redrawn.

### Modifiers

The `Modifier` object allows you to decorate or augment a composable (layout, appearance, interactions, etc.). They are chainable and order-sensitive.

## Common Patterns

### State Hoisting

State should be moved up to the caller to make components stateless and reusable.

- **Stateful**: Owns state (`remember { mutableStateOf(...) }`).
- **Stateless**: Receives state as parameters and emits events via lambdas.

### ViewModel & StateFlow

Use `ViewModel` to hold business logic and expose screen state via `StateFlow` or `Compose State`. Collect it in the UI using `collectAsStateWithLifecycle()`.

### Navigation Compose

Define a `NavHost` with composable destinations. Pass arguments and navigate using a type-safe approach (library dependent) or string routes (default).

## Best Practices

**Do**:

- Use **Material 3** (`androidx.compose.material3`) for the latest design specs.
- Use `remember` and `derivedStateOf` to optimize performance.
- Use `LazyColumn` / `LazyRow` for lists (equivalent to RecyclerView).
- Use `Preview` annotations to visualize UI without running the app.

**Don't**:

- Don't perform expensive operations in the composition phase (use `LaunchedEffect` or `ViewModel`).
- Don't create state inside a loop.
- Don't ignore the `Modifier` parameter in reusable components (always allow caller to pass one).

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
