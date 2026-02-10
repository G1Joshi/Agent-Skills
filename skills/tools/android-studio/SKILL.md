---
name: android-studio
description: Android Studio IDE with emulator and profiler. Use for Android development.
---

# Android Studio

Android Studio is built on IntelliJ IDEA. 2025 versions (Narwhal/Otter) feature **Gemini** for code generation and crash analysis.

## When to Use

- **Android Apps**: Native Android development (Kotlin/Java).
- **Compose**: "Live Edit" allows UI updates in real-time on devices/emulators.
- **Profiling**: Inspecting memory leaks and battery usage.

## Core Concepts

### Gradle

The build system. `build.gradle.kts` (Kotlin DSL) is the standard in 2025.

### Emulator

Virtual Android device. 2025 emulators are resizable and support foldable postures.

### Logcat v2

The logging window. Colored, filterable, and queryable logic.

## Best Practices (2025)

**Do**:

- **Use Gemini**: "Explain this crash" in Logcat sends the stack trace to Gemini for analysis.
- **Use Baseline Profiles**: Generate profiles to improve app startup time.
- **Use App Quality Insights**: View Crashlytics issues directly in the IDE code editor.

**Don't**:

- **Don't hardcode Strings**: Use `strings.xml`. The IDE warns you for a reason.

## References

- [Android Studio User Guide](https://developer.android.com/studio/intro)
