---
name: android-sdk
description: Expert Android SDK assistance covering Android architecture components, Activity/Fragment lifecycles, permissions, background work with WorkManager, and Gradle build optimizations. Use when building native Android applications, configuring ProGuard/R8, or interacting with platform SDK APIs.
---

# Android SDK

The traditional Android development toolkit (Views, Activities, Fragments, XML) using Kotlin/Java. Essential for maintaining the vast ecosystem of pre-Compose applications.

## When to Use

- **Native Android Development**: Building high-performance, platform-specific Android applications using Java or Kotlin.
- **Hardware & Sensor Access**: Interfacing with Bluetooth Low Energy, camera hardware, biometric sensors, and NFC directly.
- **Background Task Scheduling**: Managing deferred, periodic, or guaranteed background jobs using WorkManager and foreground services.
- **Deep System Integration**: Implementing custom launcher widgets, notification channels, accessibility services, and device admin policies.

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

#Activity & Fragment Lifecycles

Activities represent single screens with user interfaces; lifecycle callbacks manage resource acquisition and release to prevent memory leaks during configuration changes:

```kotlin
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
    }

    override fun onStart() {
        super.onStart()
        // Connect sensors, start location listener
    }

    override fun onStop() {
        super.onStop()
        // Release heavy sensor streams to preserve battery
    }
}
```

#Dependency Injection with Hilt

Hilt standardizes Dagger dependency injection across Android components with predefined scopes tied to Android lifecycles:

```kotlin
@HiltAndroidApp
class MainApplication : Application()

@AndroidEntryPoint
class UserProfileFragment : Fragment() {
    @Inject lateinit var analyticsTracker: AnalyticsTracker
    private val viewModel: UserViewModel by viewModels()
}
```

#Permissions Architecture & Runtime Requests

Modern Android requires fine-grained runtime permission requests before accessing sensitive hardware or user records:

```kotlin
val requestPermissionLauncher = registerForActivityResult(
    ActivityResultContracts.RequestPermission()
) { isGranted: Boolean ->
    if (isGranted) {
        openCamera()
    } else {
        showPermissionRationaleDialog()
    }
}

// Request permission when user triggers action
requestPermissionLauncher.launch(Manifest.permission.CAMERA)
```

## Common Patterns

#Background Processing with WorkManager
**Problem**: Long-running background sync operations get terminated by modern Android battery optimization (Doze mode).  
**Solution**: Schedule persistent background jobs with WorkManager and constraints.

```kotlin
class SyncWorker(ctx: Context, params: WorkerParameters) : CoroutineWorker(ctx, params) {
    override suspend fun doWork(): Result {
        return try {
            repository.syncData()
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }
}

// Enqueue with network constraint
val constraints = Constraints.Builder()
    .setRequiredNetworkType(NetworkType.CONNECTED)
    .setRequiresBatteryNotLow(true)
    .build()

val syncRequest = PeriodicWorkRequestBuilder<SyncWorker>(1, TimeUnit.HOURS)
    .setConstraints(constraints)
    .build()

WorkManager.getInstance(context).enqueueUniquePeriodicWork(
    "DataSync", ExistingPeriodicWorkPolicy.KEEP, syncRequest
)
```

## Best Practices (2026)

**Do**:

- **Adopt Edge-to-Edge Display**: Target Android 15+ edge-to-edge system bars using WindowInsetsCompat.
- **Use WorkManager for Background Tasks**: Never spawn unmanaged background threads that get killed by battery optimizations (Doze).
- **Enforce ViewBinding / Compose**: Eliminate error-prone `findViewById` lookups by using ViewBinding or modern Jetpack Compose.
- **Validate Scoped Storage**: Store application files in private app storage (`context.filesDir`) or use the Storage Access Framework for public files.

**Don't**:

- **Don't block the Main (UI) Thread**: Keep networking, JSON parsing, and database transactions strictly on IO coroutine dispatchers.
- **Don't hardcode dimensions or text**: Always use `res/values/strings.xml` for localization and `res/values/dimens.xml` or density-independent pixels (`dp`).
- **Don't hold static references to Context**: Retaining an Activity context in static singletons causes permanent memory leaks.

## Troubleshooting

| Error                                          | Cause                                               | Solution                                    |
| :--------------------------------------------- | :-------------------------------------------------- | :------------------------------------------ |
| `ANR (App Not Responding)`                     | Blocking main thread for >5s.                       | Move work to `Dispatchers.IO` (Coroutines). |
| `IllegalStateException: Fragment not attached` | Accessing context after detachment.                 | Check `isAdded` or use `MainScope` safely.  |
| `Memory Leak`                                  | Holding Activity reference in Singleton/Background. | Use `WeakReference` or Application Context. |

## References

- [Android Developer Guides](https://developer.android.com/guide)
- [Guide to App Architecture](https://developer.android.com/topic/architecture)
