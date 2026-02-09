---
name: react-native
description: React Native cross-platform mobile with native modules and Expo. Use for .tsx mobile apps.
---

# React Native

Cross-platform mobile development with React.

## When to Use

- Cross-platform iOS/Android apps
- Teams with React experience
- Apps requiring native modules
- Rapid mobile development

## Quick Start

```tsx
import React from "react";
import { View, Text, StyleSheet } from "react-native";

export default function App() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Hello React Native!</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  title: { fontSize: 24, fontWeight: "bold" },
});
```

## Core Concepts

### Components & State

```tsx
import { useState } from "react";
import { View, Text, TouchableOpacity } from "react-native";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <View>
      <Text>Count: {count}</Text>
      <TouchableOpacity onPress={() => setCount((c) => c + 1)}>
        <Text>Increment</Text>
      </TouchableOpacity>
    </View>
  );
}
```

### Navigation

```tsx
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

const Stack = createNativeStackNavigator<RootStackParamList>();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Profile" component={ProfileScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Navigate
navigation.navigate("Profile", { userId: "123" });
```

## Common Patterns

### Styling

```tsx
import { StyleSheet, useColorScheme } from "react-native";

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  card: {
    backgroundColor: "white",
    borderRadius: 8,
    padding: 16,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3, // Android
  },
});

// Dynamic theming
function ThemedView() {
  const colorScheme = useColorScheme();
  const isDark = colorScheme === "dark";

  return (
    <View style={{ backgroundColor: isDark ? "#000" : "#fff" }}>
      <Text style={{ color: isDark ? "#fff" : "#000" }}>Themed content</Text>
    </View>
  );
}
```

### Expo Router

```tsx
// app/_layout.tsx
export default function Layout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: "Home" }} />
      <Stack.Screen name="[id]" options={{ title: "Details" }} />
    </Stack>
  );
}

// app/index.tsx
import { Link } from "expo-router";

export default function Home() {
  return <Link href="/123">Go to Details</Link>;
}
```

## Best Practices

**Do**:

- Use TypeScript for type safety
- Use React Query for server state
- Implement proper error boundaries
- Test on both platforms

**Don't**:

- Use inline styles extensively
- Ignore platform differences
- Skip accessibility props
- Use deprecated APIs

## Troubleshooting

| Issue               | Cause         | Solution                |
| ------------------- | ------------- | ----------------------- |
| Metro bundler error | Cache issue   | Clear cache, restart    |
| Native module error | Linking issue | Run pod install         |
| Style not applied   | Platform diff | Check platform-specific |

## References

- [React Native Docs](https://reactnative.dev/)
- [Expo Documentation](https://docs.expo.dev/)
