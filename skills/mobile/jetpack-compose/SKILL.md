---
name: jetpack-compose
description: Jetpack Compose Android UI toolkit with Kotlin. Use for modern Android development.
---

# Jetpack Compose

Modern declarative UI toolkit for Android.

## When to Use

- New Android development
- Kotlin-based UI
- Material Design 3
- Reactive UI patterns

## Quick Start

```kotlin
import androidx.compose.material3.*
import androidx.compose.runtime.*

@Composable
fun Greeting(name: String) {
    Text(text = "Hello, $name!")
}

@Preview
@Composable
fun GreetingPreview() {
    Greeting("Android")
}
```

## Core Concepts

### State Management

```kotlin
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }

    Column(
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Count: $count", style = MaterialTheme.typography.headlineMedium)
        Button(onClick = { count++ }) {
            Text("Increment")
        }
    }
}

// ViewModel integration
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {
    val users = repository.observeUsers()
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())
}

@Composable
fun UserList(viewModel: UserViewModel = hiltViewModel()) {
    val users by viewModel.users.collectAsState()
    LazyColumn {
        items(users) { user ->
            UserCard(user)
        }
    }
}
```

### Layouts

```kotlin
@Composable
fun UserCard(user: User) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            AsyncImage(
                model = user.avatarUrl,
                contentDescription = null,
                modifier = Modifier.size(48.dp).clip(CircleShape)
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(user.name, style = MaterialTheme.typography.titleMedium)
                Text(user.email, style = MaterialTheme.typography.bodySmall)
            }
        }
    }
}
```

## Common Patterns

### Navigation

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            HomeScreen(onUserClick = { userId ->
                navController.navigate("user/$userId")
            })
        }
        composable(
            "user/{userId}",
            arguments = listOf(navArgument("userId") { type = NavType.StringType })
        ) { backStackEntry ->
            val userId = backStackEntry.arguments?.getString("userId")
            UserScreen(userId = userId!!)
        }
    }
}
```

### Theming

```kotlin
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) darkColorScheme() else lightColorScheme()

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
```

## Best Practices

**Do**:

- Use remember for local state
- Use ViewModel for screen state
- Follow unidirectional data flow
- Use LazyColumn for lists

**Don't**:

- Put heavy logic in composables
- Use mutableStateOf without remember
- Forget key parameter in lists
- Skip preview annotations

## Troubleshooting

| Issue              | Cause                       | Solution                |
| ------------------ | --------------------------- | ----------------------- |
| Recomposition loop | State change in composition | Move to side effect     |
| Preview crash      | Missing dependencies        | Add preview parameters  |
| Slow scroll        | Heavy list items            | Use LazyColumn properly |

## References

- [Compose Documentation](https://developer.android.com/jetpack/compose)
- [Compose Samples](https://github.com/android/compose-samples)
