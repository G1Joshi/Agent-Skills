---
name: react-native
description: Expert React Native assistance covering the New Architecture (TurboModules, Fabric renderer, Bridgeless mode), Hermes JS engine, React Navigation, and native styling. Use when building cross-platform mobile apps for iOS and Android using React and TypeScript.
---

# React Native

React Native allows you to build native mobile apps using React and JavaScript/TypeScript. It renders veritable native UI components (not webviews), offering performance close to native apps while maintaining the React developer experience.

## When to Use

- **Universal Mobile Apps**: Building cross-platform iOS and Android applications using React and TypeScript.
- **The New Architecture**: Leveraging TurboModules, Fabric concurrent rendering, and Bridgeless mode for 60/120fps native performance.
- **Code Sharing Across Web & Mobile**: Sharing hooks, validation logic, and state stores between React web apps and React Native mobile apps.
- **Ecosystem Scale**: Accessing the massive ecosystem of React Native libraries, devtools, and component libraries.

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

#Fabric Renderer & TurboModules (New Architecture)

Replaces legacy JSON bridge serialization with direct C++ JSI (JavaScript Interface) calls for instant memory access and synchronous layout passes:

```tsx
// Modern TurboModule invocation runs synchronously without serialization penalty
import { TurboModuleRegistry } from "react-native";

export interface Spec extends TurboModule {
  multiply(a: number, b: number): Promise<number>;
  syncCalculation(x: number): number; // Synchronous C++ method
}

export default TurboModuleRegistry.getEnforcing<Spec>("CustomMathModule");
```

#High-Performance Layout with Flexbox (Yoga)

React Native uses Yoga C++ engine to implement CSS Flexbox layout calculations directly into native mobile views:

```tsx
import { StyleSheet, View, Text } from "react-native";

export const ProfileHeader = () => (
  <View style={styles.container}>
    <View style={styles.avatarPlaceholder} />
    <View style={styles.textColumn}>
      <Text style={styles.name}>Jane Doe</Text>
      <Text style={styles.role}>Principal Engineer</Text>
    </View>
  </View>
);

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    padding: 16,
    backgroundColor: "#ffffff",
  },
  avatarPlaceholder: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: "#6366f1",
  },
  textColumn: { marginLeft: 12 },
  name: { fontSize: 16, fontWeight: "600", color: "#111827" },
  role: { fontSize: 13, color: "#6b7280" },
});
```

#Concurrent Reanimated Animations

Executes fluid gestures and physics-based animations directly on the UI thread via worklets:

```tsx
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from "react-native-reanimated";

export const PulsingBadge = () => {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const triggerPulse = () => {
    scale.value = withSpring(scale.value === 1 ? 1.2 : 1);
  };

  return <Animated.View style={[styles.badge, animatedStyle]} />;
};
```

## Common Patterns

#High-Performance Animations with Reanimated
**Problem**: JavaScript thread frame drops cause jittery mobile gesture animations.  
**Solution**: Run animations on UI thread using `react-native-reanimated`.

```tsx
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from "react-native-reanimated";
import { GestureDetector, Gesture } from "react-native-gesture-handler";

export function DraggableBox() {
  const offset = useSharedValue({ x: 0, y: 0 });

  const panGesture = Gesture.Pan()
    .onChange((e) => {
      offset.value = {
        x: offset.value.x + e.changeX,
        y: offset.value.y + e.changeY,
      };
    })
    .onEnd(() => {
      offset.value = withSpring({ x: 0, y: 0 });
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: offset.value.x }, { translateY: offset.value.y }],
  }));

  return (
    <GestureDetector gesture={panGesture}>
      <Animated.View
        style={[
          { width: 80, height: 80, backgroundColor: "#6366f1" },
          animatedStyle,
        ]}
      />
    </GestureDetector>
  );
}
```

## Best Practices (2026)

**Do**:

- **Enable the New Architecture**: Ensure `newArchEnabled=true` is active in `android/gradle.properties` and CocoaPods.
- **Use FlashList Instead of FlatList**: Adopt Shopify's `@shopify/flash-list` for recycling cell views without memory spikes or blank cells.
- **Extract Styles with `StyleSheet.create`**: Prevent creating new style objects on every render pass.
- **Profile with React DevTools and Flipper/Chrome Inspector**: Measure layout passes and identify unnecessary component re-renders.

**Don't**:

- **Don't pass raw anonymous functions to FlatList items**: Memoize render items using `useCallback` or dedicated subcomponents.
- **Don't perform heavy work on the JavaScript thread**: Offload encryption, image compression, and heavy parsing to background threads or native modules.
- **Don't ignore Android BackHandler**: Always handle hardware back presses to avoid terminating user flows abruptly.

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
