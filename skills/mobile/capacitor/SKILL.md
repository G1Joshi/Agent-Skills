---
name: capacitor
description: Capacitor for web-to-native mobile apps with plugins. Use for hybrid mobile apps.
---

# Capacitor

Web-native runtime for building cross-platform mobile apps.

## When to Use

- Convert web apps to mobile
- Access native device features
- Single codebase for web/mobile
- Progressive Web App enhancement

## Quick Start

```bash
# Add to existing web project
npm install @capacitor/core @capacitor/cli
npx cap init

# Add platforms
npm install @capacitor/ios @capacitor/android
npx cap add ios
npx cap add android
```

## Core Concepts

### Plugin Usage

```typescript
import { Camera, CameraResultType } from "@capacitor/camera";
import { Geolocation } from "@capacitor/geolocation";
import { LocalNotifications } from "@capacitor/local-notifications";

async function takePicture() {
  const image = await Camera.getPhoto({
    resultType: CameraResultType.Uri,
    quality: 90,
  });
  return image.webPath;
}

async function getLocation() {
  const position = await Geolocation.getCurrentPosition();
  return {
    lat: position.coords.latitude,
    lng: position.coords.longitude,
  };
}

async function scheduleNotification() {
  await LocalNotifications.schedule({
    notifications: [
      {
        title: "Reminder",
        body: "Check your tasks!",
        id: 1,
        schedule: { at: new Date(Date.now() + 3600 * 1000) },
      },
    ],
  });
}
```

### Configuration

```typescript
// capacitor.config.ts
import type { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "com.example.app",
  appName: "My App",
  webDir: "dist",
  server: {
    androidScheme: "https",
  },
  plugins: {
    SplashScreen: {
      launchAutoHide: false,
    },
    Keyboard: {
      resize: "body",
    },
  },
};

export default config;
```

## Common Patterns

### Native Bridge

```typescript
import { registerPlugin } from "@capacitor/core";

interface MyPluginPlugin {
  echo(options: { value: string }): Promise<{ value: string }>;
}

const MyPlugin = registerPlugin<MyPluginPlugin>("MyPlugin");

// Usage
const result = await MyPlugin.echo({ value: "Hello" });
```

### Build & Deploy

```bash
# Sync web code to native
npx cap sync

# Open in IDE
npx cap open ios
npx cap open android

# Live reload during dev
npx cap run ios --livereload --external
```

## Best Practices

**Do**:

- Use official Capacitor plugins
- Run `cap sync` after web builds
- Handle permissions gracefully
- Test on real devices

**Don't**:

- Forget to sync after changes
- Ignore platform differences
- Skip error handling
- Use deprecated Cordova plugins

## Troubleshooting

| Issue             | Cause           | Solution               |
| ----------------- | --------------- | ---------------------- |
| Plugin not found  | Not installed   | Install and sync       |
| White screen      | Web build issue | Check webDir path      |
| Permission denied | Not requested   | Add permission prompts |

## References

- [Capacitor Documentation](https://capacitorjs.com/docs)
- [Capacitor Plugins](https://capacitorjs.com/docs/plugins)
