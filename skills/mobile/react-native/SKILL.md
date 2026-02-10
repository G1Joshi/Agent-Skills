---
name: react-native
description: React Native cross-platform mobile with JavaScript. Use for iOS/Android.
---

# React Native

React Native allows you to build native mobile apps using React and JavaScript/TypeScript. It renders veritable native UI components (not webviews), offering performance close to native apps while maintaining the React developer experience.

## When to Use

- Building iOS and Android apps with a shared codebase.
- Teams with existing React/Web expertise.
- Apps requiring Over-the-Air (OTA) updates (via Expo Updates or CodePush).
- Prototyping cross-platform mobile experiences rapidly.

## Quick Start

Using **Expo** (Recommended for 2024/2025):

```bash
npx create-expo-app@latest my-app
cd my-app
npx expo start
```

```tsx
// app/index.tsx (Expo Router)
import { useState } from "react";
import { View, Text, Button, StyleSheet } from "react-native";
import { Link } from "expo-router";

export default function Home() {
  const [count, setCount] = useState(0);

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Count: {count}</Text>
      <Button title="Increment" onPress={() => setCount((c) => c + 1)} />

      <Link href="/details" style={styles.link}>
        Go to Details
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  text: { fontSize: 24, marginBottom: 20 },
  link: { marginTop: 20, color: "blue" },
});
```

## Core Concepts

### Native Components vs Web

React Native works by bridging JavaScript to Native UI components.

- `<View>` maps to `UIView` (iOS) / `android.view.View` (Android).
- `<Text>` maps to `UITextView` / `TextView`.
- **New Architecture (Fabric/TurboModules)**: Removes the async bridge for synchronous, direct C++ communication (JSI), improving performance.

### Flexbox Layout

Layouts use Flexbox (like CSS), but defaults to `flexDirection: 'column'` (unlike row on web). Everything needs strict dimensions or flex grow capabilities.

### Fast Refresh

React Native preserves local state while reloading components instantly on file save, significantly speeding up the dev loop.

## Common Patterns

### Expo Router (File-based Routing)

Modern React Native apps use `expo-router` which mimics Next.js.

- `app/index.tsx` -> Home screen
- `app/(tabs)/_layout.tsx` -> Tab navigation
- `app/[id].tsx` -> Dynamic routes

### Server State (React Query)

Avoid Redux for API state. Use `TanStack Query` (React Query).

- Caches data, handles loading/error states, and manages refetching.

### Client State (Zustand)

For global app state (theme, auth token), `Zustand` is preferred over Redux/Context for its simplicity and performance (selectors).

## Best Practices

**Do**:

- Use **Expo** for new projects unless you have strict native code dependency needs that Config Plugins can't handle.
- Use **TypeScript** for type safety.
- Use **FlashList** (by Shopify) instead of `FlatList` for long lists performance.
- Use **Reanimated** for complex animations (runs on UI thread).

**Don't**:

- Don't leave `console.log` in production builds (it slows down the bridge).
- Don't do heavy calculations in the JS thread during animations/gestures.
- Don't define styles inside the render function (recreates objects every render).

## Troubleshooting

| Error                                                     | Cause                                   | Solution                               |
| :-------------------------------------------------------- | :-------------------------------------- | :------------------------------------- |
| `Metro Bundler process exited with code 1`                | Port in use or bad cache.               | `npx expo start -c` (clear cache).     |
| `Invariant Violation: View config not found`              | Import issues or upgrading RN versions. | Check node_modules, clear watchman.    |
| `CocoaPods could not find compatible versions`            | iOS dependency conflict.                | `cd ios && pod install --repo-update`. |
| `Text strings must be rendered within a <Text> component` | Raw text directly inside View.          | Wrap all strings in `<Text>`.          |

## References

- [React Native Docs](https://reactnative.dev)
- [Expo Documentation](https://docs.expo.dev)
- [React Native Directory (Libraries)](https://reactnative.directory)
