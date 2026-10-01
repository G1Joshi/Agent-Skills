---
name: android-studio
description: Expert Android Studio IDE assistance covering Gradle sync, Logcat, Layout Inspector, SDK Manager, and virtual devices (AVD). Use when developing native Android applications with Kotlin or Java.
---

# Android Studio

Android Studio is the official integrated development environment (IDE) for Android application development, built on IntelliJ IDEA with rich profiling and emulator tools.

## When to Use

- **Native Android & Jetpack Compose Development**: Official Google IDE with visual layout editor, Compose preview, and Profiler.
- **Gradle Build Script Optimization**: Configuring multi-module build logic with Kotlin DSL (`build.gradle.kts`).
- **Android Emulator & Device Management**: Running virtual and physical devices via ADB and headless emulator CLI.
- **App Performance & Memory Profiling**: Diagnosing frame drops, memory leaks, and CPU spikes using Android Studio Profiler.

## Quick Start

```bash
# Launch Android Studio or build project from command line
./gradlew assembleDebug

# Install and run on connected device/emulator
./gradlew installDebug
adb shell am start -n "com.example.app/.MainActivity"
```

## Core Concepts

### Jetpack Compose Preview & UI Inspection

Authoring declarative UI with multi-device previews:

```kotlin
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

@Composable
fun MetricCard(title: String, value: String, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier.padding(8.dp),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = title, style = MaterialTheme.typography.labelMedium)
            Spacer(modifier = Modifier.height(4.dp))
            Text(text = value, style = MaterialTheme.typography.headlineMedium)
        }
    }
}

// Interactive Preview for Android Studio Design Canvas
@Preview(name = "Light Mode", showBackground = true)
@Preview(name = "Dark Mode", uiMode = android.content.res.Configuration.UI_MODE_NIGHT_YES)
@Composable
fun MetricCardPreview() {
    MaterialTheme {
        MetricCard(title = "Network Throughput", value = "1.2 GB/s")
    }
}
```

### Modern Gradle Build Configuration (build.gradle.kts)

Multi-module build setup with version catalogs:

```kotlin
// app/build.gradle.kts
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.compose.compiler)
}

android {
    namespace = "com.company.enterpriseapp"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.company.enterpriseapp"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "2026.1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
}
```

### Headless Emulator & ADB Operations

Managing testing devices from command line:

```bash
# List available Android Virtual Devices (AVDs)
emulator -list-avds

# Launch AVD headlessly in CI runner
emulator -avd Pixel_8_API_35 -no-window -no-audio -no-boot-anim &

# Wait for device to complete boot
adb wait-for-device shell 'while [[ -z $(getprop sys.boot_completed) ]]; do sleep 1; done;'
```

## Common Patterns

### Gradle Build Cache and Memory Optimization

**Problem**: Slow Gradle build and sync times inside Android Studio.

**Solution**:
Configure build properties in `gradle.properties`:

```properties
org.gradle.jvmargs=-Xmx4096m -XX:+UseParallelGC
org.gradle.parallel=true
org.gradle.caching=true
org.gradle.configuration-cache=true
android.useAndroidX=true
```

## Best Practices

**Do**:

- Migrate build scripts to Kotlin DSL (`build.gradle.kts`) and Gradle Version Catalogs (`libs.versions.toml`).
- Enable R8 code shrinking and resource minification (`isMinifyEnabled = true`) on release builds.
- Utilize Android Studio Profiler (CPU, Memory, Energy) before pushing production releases.
- Allocate sufficient heap memory to the Gradle daemon in `gradle.properties` (`org.gradle.jvmargs=-Xmx4096m`).

**Don't**:

- Leave debug signing credentials in open repositories; inject keystores via environment variables.
- Run heavy unit tests on the Android Emulator if pure JVM unit tests (`src/test`) suffice.
- Ignore Lint warnings; configure `lint { abortOnError = true }` in CI.

## Troubleshooting

| Error                                          | Cause                                                                 | Solution                                                                 |
| :--------------------------------------------- | :-------------------------------------------------------------------- | :----------------------------------------------------------------------- |
| `Gradle sync failed: Connection timed out`     | Proxy, firewall, or Gradle wrapper downloading over slow network.     | Check offline work in Gradle settings or use pre-downloaded wrapper.     |
| `Installed Build Tools revision is corrupted`  | Incomplete download of Android SDK Build Tools.                       | Open SDK Manager, uninstall affected Build-Tools version, and reinstall. |
| `Emulator: Process crashed with exit code 139` | Hardware acceleration (HAXM/Hypervisor) conflict or GPU driver issue. | Change Emulator settings > Emulated Performance: Graphics to 'Software'. |

## References

- [Android Studio User Guide](https://developer.android.com/studio/intro)
