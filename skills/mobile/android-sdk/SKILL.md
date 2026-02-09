---
name: android-sdk
description: Android SDK for native Android development with Activities and Services. Use for native Android.
---

# Android SDK

Native Android development with Kotlin and Java.

## When to Use

- Native Android apps
- System-level integrations
- Background services
- Performance-critical features

## Quick Start

```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val textView = findViewById<TextView>(R.id.text_view)
        textView.text = "Hello Android!"
    }
}
```

## Core Concepts

### Activity Lifecycle

```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Initialize UI
    }

    override fun onStart() {
        super.onStart()
        // Visible to user
    }

    override fun onResume() {
        super.onResume()
        // Interactive
    }

    override fun onPause() {
        super.onPause()
        // Save state
    }

    override fun onStop() {
        super.onStop()
        // Release resources
    }

    override fun onDestroy() {
        super.onDestroy()
        // Cleanup
    }
}
```

### Intents

```kotlin
// Start activity
val intent = Intent(this, DetailActivity::class.java).apply {
    putExtra("USER_ID", userId)
}
startActivity(intent)

// Get result
val launcher = registerForActivityResult(
    ActivityResultContracts.StartActivityForResult()
) { result ->
    if (result.resultCode == RESULT_OK) {
        val data = result.data
    }
}
```

## Common Patterns

### ViewModel

```kotlin
class UserViewModel(
    private val repository: UserRepository
) : ViewModel() {

    private val _user = MutableStateFlow<User?>(null)
    val user: StateFlow<User?> = _user.asStateFlow()

    fun loadUser(id: String) {
        viewModelScope.launch {
            _user.value = repository.getUser(id)
        }
    }
}
```

### Permissions

```kotlin
private val permissionLauncher = registerForActivityResult(
    ActivityResultContracts.RequestPermission()
) { isGranted ->
    if (isGranted) {
        // Permission granted
    }
}

fun requestCameraPermission() {
    when {
        ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
            == PackageManager.PERMISSION_GRANTED -> {
            // Already granted
        }
        else -> {
            permissionLauncher.launch(Manifest.permission.CAMERA)
        }
    }
}
```

## Best Practices

**Do**:

- Use ViewModel for UI state
- Handle configuration changes
- Request permissions at runtime
- Use Coroutines for async

**Don't**:

- Block the main thread
- Hardcode strings
- Ignore lifecycle
- Skip null checks

## Troubleshooting

| Issue             | Cause               | Solution            |
| ----------------- | ------------------- | ------------------- |
| ANR               | Main thread blocked | Move to background  |
| Memory leak       | Context reference   | Use lifecycle-aware |
| Crash on rotation | State not saved     | Use ViewModel       |

## References

- [Android Developer Docs](https://developer.android.com/docs)
- [Android Architecture](https://developer.android.com/topic/architecture)
