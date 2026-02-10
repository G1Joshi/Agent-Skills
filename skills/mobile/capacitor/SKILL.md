---
name: capacitor
description: Capacitor cross-platform native runtime. Use for web to native.
---

# Capacitor

Capacitor by Ionic is a cross-platform native runtime that makes it easy to build web apps that run on iOS, Android, and the web as Progressive Web Apps (PWAs). It provides a bridge to native APIs.

## When to Use

- Converting existing React/Angular/Vue web apps to mobile apps.
- Need specific native functionality (Camera, Haptics, Push) in a web app.
- Building plugins that need to work across iOS, Android, and Web consistent APIs.

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

### Native Bridge

Capacitor injects a native bridge into the WebView, allowing JavaScript to call Native Code (Java/Kotlin/Swift/Obj-C) asynchronously.

### Plugins

Modular blocks of code that provide interface to native functionality.

- **Official Plugins**: Maintained by Ionic team (Camera, Filesystem).
- **Community Plugins**: Maintained by the community.

### Native Project Management

Capacitor treats native projects (`android/`, `ios/`) as "source artifacts", meaning you commit them to git and use native tooling (Android Studio/Xcode) to build and configure them (permissions, icons).

## Common Patterns

### Secure Storage

Use `@capacitor-community/http` for secure requests (bypassing CORS) and secure storage plugins for tokens (Keychain/Keystore) instead of `localStorage`.

### Deep Linking

Handle custom URL schemes (`myapp://`) for authentication redirects or opening specific content.

## Best Practices

**Do**:

- Use **official plugins** whenever possible for long-term maintenance.
- Sync your project frequently: `npx cap sync`.
- Handle **Permissions** gracefully in your UI before calling native APIs.
- Use **Live Reload** during development: `npx cap run android -l --external`.

**Don't**:

- Don't store sensitive data (API Keys) in JS code; use environment variables or native config.
- Don't ignore platform differences; test on real iOS and Android devices.
- Don't rely on `alert()`/`confirm()`; use Capacitor Dialog plugin or UI framework modals.

## Troubleshooting

| Error                                  | Cause                                       | Solution                                                      |
| :------------------------------------- | :------------------------------------------ | :------------------------------------------------------------ |
| `Plugin not implemented`               | Plugin not installed or platform not added. | Run `npx cap sync` and check imports.                         |
| `Cleartext HTTP traffic not permitted` | Android security preventing http requests.  | Use HTTPS or update `network_security_config.xml` (dev only). |
| `Xcode build failed`                   | Pods out of sync or signing issue.          | `npx cap update ios` then check Signing in Xcode.             |

## References

- [Capacitor Documentation](https://capacitorjs.com/docs)
- [Capacitor Plugins](https://capacitorjs.com/docs/apis)
