---
name: xcode
description: Expert Xcode assistance covering Swift/SwiftUI development, iOS/macOS simulators, Xcode Cloud CI/CD, Instruments profiling, and Swift Package Manager (SPM). Use when configuring Xcode projects, debugging iOS apps with LLDB, profiling with Instruments, or managing Apple Developer signing.
---

# Xcode

Xcode is the only IDE for native Apple platforms. 2025 (Xcode 17) brings **Swift Assist** and **Predictive Code Completion** running locally on Apple Silicon.

## When to Use

- **Native Apple Platform Engineering**: Building iOS, iPadOS, macOS, watchOS, and visionOS applications using Swift and SwiftUI.
- **Instruments Performance Profiling**: Profiling memory leaks, CPU spikes, energy usage, and Time Profiler traces.
- **Automated CI/CD Build Packaging**: Building, signing, and releasing apps to TestFlight using Fastlane and `xcodebuild`.
- **Swift Package Manager (SPM) Dependency Resolution**: Managing native modular libraries and cross-platform Swift packages.

## Quick Start

### 1. Build and Test via xcodebuild CLI

```bash
# Build for iOS Simulator
xcodebuild -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16,OS=latest' \
  clean build

# Run unit tests
xcodebuild test -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16,OS=latest'
```

### 2. Core Xcode Shortcuts

- `Cmd + B`: Build
- `Cmd + R`: Run
- `Cmd + U`: Run Unit Tests
- `Cmd + .`: Stop Running
- `Cmd + Shift + O`: Open Quickly (search symbol or file)

## Core Concepts

### Modular Swift Package Architecture (`Package.swift`)

Defining modular application packages with explicit dependencies and targets:

```swift
// swift-tools-version: 5.10
import PackageDescription

let package = Package(
    name: "CoreNetworking",
    platforms: [
        .iOS(.v17),
        .macOS(.v14)
    ],
    products: [
        .library(name: "CoreNetworking", targets: ["CoreNetworking"]),
    ],
    dependencies: [
        .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.9.0"),
    ],
    targets: [
        .target(
            name: "CoreNetworking",
            dependencies: ["Alamofire"],
            swiftSettings: [
                .enableExperimentalFeature("StrictConcurrency")
            ]
        ),
        .testTarget(
            name: "CoreNetworkingTests",
            dependencies: ["CoreNetworking"]
        ),
    ]
)
```

### Automated CI/CD Build & Test with `xcodebuild`

Executing headless builds and test runs in continuous integration:

```bash
# Clean, build, and test application for iOS Simulator
xcodebuild clean test \
  -workspace "EnterpriseApp.xcworkspace" \
  -scheme "EnterpriseApp" \
  -destination "platform=iOS Simulator,name=iPhone 16 Pro,OS=latest" \
  -resultBundlePath "./build/TestResults.xcresult" \
  CODE_SIGN_IDENTITY="" \
  CODE_SIGNING_REQUIRED=NO \
  CODE_SIGNING_ALLOWED=NO
```

### Declarative Build Settings (`Config.xcconfig`)

Extracting signing, bundle identifiers, and compiler flags from `.xcodeproj` into versioned files:

```ini
// Release.xcconfig
PRODUCT_BUNDLE_IDENTIFIER = com.company.enterpriseapp
SWIFT_VERSION = 5.10
SWIFT_STRICT_CONCURRENCY = complete
IPHONEOS_DEPLOYMENT_TARGET = 17.0
ENABLE_BITCODE = NO
DEBUG_INFORMATION_FORMAT = dwarf-with-dsym
SWIFT_OPTIMIZATION_LEVEL = -O
```

## Common Patterns

### LLDB Debugging Commands

**Problem**: Inspect memory, modify variables at runtime, and view view-hierarchy during breakpoints.  
**Solution**: Use LLDB console commands.

```lldb
# Print object description
po myViewModel.userProfile

# Print view hierarchy
po [[UIWindow keyWindow] recursiveDescription]

# Modify variable in memory during breakpoint
expr isFeatureFlagEnabled = true

# Continue execution
c
```

### Instruments Memory Leak Profiling

**Problem**: Identify retain cycles and memory leaks in SwiftUI/UIKit navigation flows.  
**Solution**: Profile with Leaks instrument.

1. In Xcode: **Product > Profile** (`Cmd + I`).
2. Select **Leaks** template.
3. Record app interactions.
4. Inspect red leak markers and trace cycle reference graph to pinpoint unweakened closures (`[weak self]`).

## Best Practices (2026)

- **Do** enable **Complete Strict Concurrency Checking** (`SWIFT_STRICT_CONCURRENCY = complete`) for Swift 6 safety.
- **Do** manage build configuration flags using `.xcconfig` files rather than modifying `.xcodeproj` project files directly.
- **Do** profile memory leaks, retain cycles, and allocation graphs using **Xcode Instruments** (`Cmd + I`).
- **Do** automate archiving and TestFlight distribution using `fastlane gym` and `fastlane pilot`.
- **Don't** commit `xcuserdata/` directories inside `.xcodeproj` or `.xcworkspace` to Git.
- **Don't** store private distribution certificates or provisioning profile passwords in plaintext CI scripts.
- **Don't** force-unwrap optionals (`!`) or ignore Swift Concurrency compiler warnings.

## Troubleshooting

| Error / Symptom                                     | Cause                                                                       | Solution                                                                                              |
| --------------------------------------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `Code Signing Error: No signing certificate found`  | Apple Developer account credentials expired or provisioning profile missing | Check **Signing & Capabilities** tab; select your team and enable **Automatically manage signing**.   |
| DerivedData corruption causing phantom build errors | Stale module cache or build artifacts                                       | Run `rm -rf ~/Library/Developer/Xcode/DerivedData` and restart Xcode.                                 |
| Simulator fails to boot or hangs on black screen    | Corrupted simulator state                                                   | Open Simulator menu > **Device > Erase All Content and Settings...** or run `xcrun simctl erase all`. |

## References

- [Xcode Documentation](https://developer.apple.com/xcode/)
