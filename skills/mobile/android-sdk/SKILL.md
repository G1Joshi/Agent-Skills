---
name: android-sdk
description: Android SDK development tools. Use for native Android.
---

# Android SDK

The traditional Android development toolkit (Views, Activities, Fragments, XML) using Kotlin/Java. Essential for maintaining the vast ecosystem of pre-Compose applications.

## When to Use

- Maintaining legacy Android applications (Views/XML).
- Building features requiring low-level system interactions not yet wrapped by Compose.
- Using libraries that strictly require Fragment/View interoperability.

## Quick Start

```kotlin
// build.gradle.kts: viewBinding = true

class MainActivity : AppCompatActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.myButton.setOnClickListener {
            Toast.makeText(this, "Clicked!", Toast.LENGTH_SHORT).show()
        }
    }
}
```

## Core Concepts

### Lifecycle

Understanding the complex lifecycle of Activities (`onCreate`, `onPause`, `onDestroy`) and Fragments is the hardest but most important part of legacy Android dev to prevent crashes and data loss.

### Intents

The messaging object used to request an action from another app component (starting activities, services, broadcasting).

### XML Layouts

Defining UI structure in XML files (`res/layout/activity_main.xml`).

## Common Patterns

### View Binding

Replaces `findViewById`. Generates type-safe binding classes for XML layouts.

- **Null Safety**: View references are nullable if they verify across configs.
- **Type Safety**: No casting required.

### Repository Pattern (Clean Architecture)

separating data sources (Room, Retrofit) from UI logic (ViewModel).

### Coroutines (Structured Concurrency)

Replacing `AsyncTask` and `Threads`.

- Use `lifecycleScope` and `viewModelScope` to automatically cancel tasks when the UI is destroyed.

## Best Practices

**Do**:

- Use **ViewBinding** instead of `findViewById` or Kotlin Synthetics (Deprecated).
- Use **Coroutines** for background tasks.
- Use **Dependency Injection** (Hilt) to manage complex graphs.
- Handle **Configuration Changes** (Rotation) using ViewModels.

**Don't**:

- Don't block the **Main Thread** (ANR Risk).
- Don't put business logic in Activities/Fragments (God Class anti-pattern).
- Don't ignore Fragment lifecycle (don't access views in `onDestroyView`).

## Troubleshooting

| Error                                          | Cause                                               | Solution                                    |
| :--------------------------------------------- | :-------------------------------------------------- | :------------------------------------------ |
| `ANR (App Not Responding)`                     | Blocking main thread for >5s.                       | Move work to `Dispatchers.IO` (Coroutines). |
| `IllegalStateException: Fragment not attached` | Accessing context after detachment.                 | Check `isAdded` or use `MainScope` safely.  |
| `Memory Leak`                                  | Holding Activity reference in Singleton/Background. | Use `WeakReference` or Application Context. |

## References

- [Android Developer Guides](https://developer.android.com/guide)
- [Guide to App Architecture](https://developer.android.com/topic/architecture)
