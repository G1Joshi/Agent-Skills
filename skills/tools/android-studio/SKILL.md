---
name: android-studio
description: Android Studio IDE for Android development with Gradle and emulator. Use for Android projects.
---

# Android Studio

IDE for Android app development based on IntelliJ IDEA.

## When to Use

- Android app development
- Kotlin/Java mobile projects
- Jetpack Compose development
- APK building and debugging

## Quick Start

```kotlin
// MainActivity.kt
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MyApp()
        }
    }
}
```

## Core Concepts

### Gradle Configuration

```kotlin
// build.gradle.kts (app)
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.example.myapp"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.example.myapp"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    buildFeatures {
        compose = true
    }
}

dependencies {
    implementation(platform("androidx.compose:compose-bom:2024.01.00"))
    implementation("androidx.compose.material3:material3")
}
```

### Debugging

```kotlin
// Logcat filtering
// Tag: MyActivity Level: Debug

Log.d("MyActivity", "Debug message")
Log.e("MyActivity", "Error message", exception)

// Breakpoint conditions
// Right-click breakpoint -> Condition: userId == "123"
```

## Common Patterns

### Device Management

```bash
# ADB commands
adb devices
adb install app-debug.apk
adb logcat | grep MyApp
adb shell am start -n com.example.myapp/.MainActivity

# Emulator
emulator -list-avds
emulator -avd Pixel_6_API_34
```

### Build Variants

```kotlin
android {
    flavorDimensions += "version"
    productFlavors {
        create("free") {
            dimension = "version"
            applicationIdSuffix = ".free"
        }
        create("paid") {
            dimension = "version"
            applicationIdSuffix = ".paid"
        }
    }
}
```

## Best Practices

**Do**:

- Use version catalogs for dependencies
- Enable R8 for release builds
- Configure ProGuard rules
- Test on multiple API levels

**Don't**:

- Commit local.properties
- Ignore lint warnings
- Skip signed release builds
- Use deprecated APIs

## Troubleshooting

| Issue              | Cause            | Solution                    |
| ------------------ | ---------------- | --------------------------- |
| Gradle sync failed | Dependency issue | Check version compatibility |
| Emulator slow      | Low memory       | Increase RAM allocation     |
| Build error        | SDK missing      | Install via SDK Manager     |

## References

- [Android Developers](https://developer.android.com/)
- [Android Studio Guide](https://developer.android.com/studio)
