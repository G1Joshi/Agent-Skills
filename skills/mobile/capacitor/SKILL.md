---
name: capacitor
description: Expert Capacitor assistance covering web-to-native bridges, cross-platform plugins, iOS/Android project generation, and Progressive Web App (PWA) packaging. Use when wrapping React/Vue/Angular apps into native mobile binaries, writing custom native plugins, or managing Capacitor configurations.
---

# Capacitor

Capacitor by Ionic is a cross-platform native runtime that makes it easy to build web apps that run on iOS, Android, and the web as Progressive Web Apps (PWAs). It provides a bridge to native APIs.

## When to Use

- **Web to Native Transformation**: Deploying modern React, Vue, Svelte, or Angular web apps as native iOS and Android binaries.
- **Progressive Web App (PWA) Parity**: Maintaining a single shared web codebase that compiles to web, App Store, and Google Play Store simultaneously.
- **Native Device APIs**: Accessing device capabilities (Camera, Push Notifications, Secure Storage, Haptics) via unified TypeScript APIs.
- **Enterprise Web App Packaging**: Wrapping internal enterprise portals into managed mobile apps with biometric authentication and certificate pinning.

## Quick Start

```bash
npm install @capacitor/core @capacitor/cli
npx cap init MyMobileApp com.example.app
npm install @capacitor/android @capacitor/ios
npx cap add android
npx cap add ios
```

```javascript
import { Geolocation } from "@capacitor/geolocation";

const printCurrentPosition = async () => {
  const coordinates = await Geolocation.getCurrentPosition();
  console.log("Current position:", coordinates);
};
```

## Core Concepts

### Web-to-Native Bridge Architecture

Capacitor embeds web applications inside a hardware-accelerated native WebView (WKWebView on iOS, Android System WebView) and exposes a bi-directional JSON RPC bridge:

```typescript
// Web layer invokes native method via unified bridge
import { Geolocation } from "@capacitor/geolocation";

const printCurrentPosition = async () => {
  const coordinates = await Geolocation.getCurrentPosition({
    enableHighAccuracy: true,
    timeout: 10000,
  });
  console.log(
    "Current lat/lng:",
    coordinates.coords.latitude,
    coordinates.coords.longitude,
  );
};
```

### Custom Native Plugin Implementation

Custom plugins allow writing native Swift or Kotlin code that hooks directly into the Capacitor TypeScript interface:

```swift
// ios/App/App/CustomHapticsPlugin.swift
import Capacitor

@objc(CustomHapticsPlugin)
public class CustomHapticsPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "CustomHapticsPlugin"
    public let jsName = "CustomHaptics"
    public let pluginMethods: [CAPPluginMethod] = [CAPPluginMethod(name: "vibrate", returnType: CAPPluginReturnPromise)]

    @objc func vibrate(_ call: CAPPluginCall) {
        let generator = UINotificationFeedbackGenerator()
        generator.notificationOccurred(.success)
        call.resolve(["success": true])
    }
}
```

### Configuration & Environment Management

Capacitor configurations dictate bundle identifiers, plugins, server hosting modes, and security policies:

```typescript
// capacitor.config.ts
import type { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "com.example.enterpriseapp",
  appName: "EnterprisePortal",
  webDir: "dist",
  server: {
    androidScheme: "https",
    cleartext: false, // Disallow insecure HTTP in production
  },
  plugins: {
    SplashScreen: { launchShowDuration: 1500, backgroundColor: "#0f172a" },
  },
};
export default config;
```

## Common Patterns

### Custom Native Plugin Bridge

**Problem**: Need native platform functionality not provided by community plugins.  
**Solution**: Create a custom Capacitor plugin bridge.

```typescript
// src/plugins/haptics.ts
import { registerPlugin } from "@capacitor/core";

export interface CustomHapticsPlugin {
  vibratePattern(options: { pattern: number[] }): Promise<void>;
}

const CustomHaptics = registerPlugin<CustomHapticsPlugin>("CustomHaptics");
export default CustomHaptics;

// Trigger in React/Vue:
await CustomHaptics.vibratePattern({ pattern: [100, 200, 100] });
```

## Best Practices

**Do**:

- Use `npx cap sync`: Always run sync after web build to copy web assets and update native plugin dependencies.
- Use Secure Storage Plugins: Store auth tokens in iOS Keychain and Android Keystore via `@capacitor-community/secure-storage`.
- Implement Live Updates Carefully: Use platforms like Capgo or Ionic Appflow for OTA bugfixes while complying with Apple guidelines.
- Optimize Web Performance: Keep initial bundle sizes small and ensure UI responsiveness meets native 60fps standards.

**Don't**:

- Edit generated `public` web folders inside native projects: Modify the source web app and run `npx cap copy`.
- Leave debug live-reload URLs in production: Remove `server.url` from `capacitor.config.ts` prior to release builds.
- Ignore notch safe areas: Apply `viewport-fit=cover` and CSS `env(safe-area-inset-top)` to prevent status bar collisions.

## Troubleshooting

| Error                                  | Cause                                       | Solution                                                      |
| :------------------------------------- | :------------------------------------------ | :------------------------------------------------------------ |
| `Plugin not implemented`               | Plugin not installed or platform not added. | Run `npx cap sync` and check imports.                         |
| `Cleartext HTTP traffic not permitted` | Android security preventing http requests.  | Use HTTPS or update `network_security_config.xml` (dev only). |
| `Xcode build failed`                   | Pods out of sync or signing issue.          | `npx cap update ios` then check Signing in Xcode.             |

## References

- [Capacitor Documentation](https://capacitorjs.com/docs)
- [Capacitor Plugins](https://capacitorjs.com/docs/apis)
