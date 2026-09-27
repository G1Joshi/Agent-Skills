---
name: expo
description: Expert Expo assistance covering EAS Build, file-based routing via Expo Router, prebuild workflows, config plugins, and OTA updates. Use when bootstrapping React Native applications, managing native dependencies without Xcode/Android Studio, or deploying via EAS.
---

# Expo

Expo is an open-source framework for apps that run natively on Android, iOS, and the web. It builds on top of React Native, providing a curated set of tools and libraries (SDK) to simplify the development lifecycle.

## When to Use

- **Modern React Native Development**: The official, recommended foundation for building React Native applications on iOS, Android, and Web.
- **Cloud Build Automation (EAS)**: Compiling native application packages in the cloud without local Xcode or Android Studio installations.
- **File-Based Routing**: Designing deeply linkable mobile navigation structures with Expo Router matching web URL semantics.
- **Over-The-Air (OTA) Updates**: Shipping critical JavaScript bugfixes instantly to end users without App Store review cycles.

## Quick Start

```bash
# Create a new app with Expo Router (default in 2025)
npx create-expo-app@latest my-safe-app
cd my-safe-app
npx expo start
```

```tsx
// app/_layout.tsx
import { Stack } from "expo-router";

export default function Layout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: "Home" }} />
    </Stack>
  );
}

// app/index.tsx
import { View, Text, StyleSheet } from "react-native";
import { Link } from "expo-router";
import { Image } from "expo-image";

export default function Index() {
  return (
    <View style={styles.container}>
      <Image
        source="https://picsum.photos/200"
        style={{ width: 100, height: 100, marginBottom: 20 }}
        contentFit="cover"
      />
      <Text style={styles.text}>Welcome to Expo!</Text>
      <Link href="/details/123" style={styles.link}>
        Go to Details
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  text: { fontSize: 20, fontWeight: "bold" },
  link: { marginTop: 15, color: "#007AFF" },
});
```

## Core Concepts

#Continuous Native Generation (Prebuild)

Expo manages native `ios/` and `android/` directories as generated build artifacts via `app.json` config plugins, eliminating fragile manual native code edits:

```json
// app.json
{
  "expo": {
    "name": "MarketPulse",
    "slug": "market-pulse",
    "version": "1.0.0",
    "plugins": [
      [
        "expo-camera",
        {
          "cameraPermission": "Allow MarketPulse to access camera for barcode scanning."
        }
      ],
      ["expo-secure-store"]
    ]
  }
}
```

```bash
# Generate or update ios/ and android/ based on config plugins
npx expo prebuild --clean
```

#Expo Router File-Based Navigation

Screens and nested navigation stacks correspond directly to directory structures in `app/`:

```tsx
// app/(tabs)/profile/[id].tsx
import { useLocalSearchParams, Stack } from "expo-router";
import { View, Text } from "react-native";

export default function UserProfile() {
  const { id } = useLocalSearchParams<{ id: string }>();

  return (
    <View style={{ flex: 1, padding: 16 }}>
      <Stack.Screen
        options={{ title: `User: ${id}`, headerBackTitle: "Back" }}
      />
      <Text style={{ fontSize: 18 }}>Viewing Profile ID: {id}</Text>
    </View>
  );
}
```

#Secure Storage & Native APIs

Expo provides production-hardened cross-platform APIs designed with TypeScript first:

```typescript
import * as SecureStore from "expo-secure-store";
import * as Haptics from "expo-haptics";

export async function persistAuthToken(token: string) {
  await SecureStore.setItemAsync("auth_jwt_token", token, {
    keychainAccessible: SecureStore.WHEN_UNLOCKED,
  });
  await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
}
```

## Common Patterns

#Dynamic File-Based Routing (Expo Router)
**Problem**: Managing complex mobile navigation stacks with manual navigator components.  
**Solution**: Use Expo Router with file-based routing and deep linking out of the box.

```tsx
// app/user/[id].tsx
import { useLocalSearchParams, Stack } from "expo-router";
import { View, Text } from "react-native";

export default function UserScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();

  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Stack.Screen options={{ title: `User #${id}` }} />
      <Text>User Profile Details for: {id}</Text>
    </View>
  );
}
```

## Best Practices (2026)

**Do**:

- **Use Expo Config Plugins**: Customize native project properties via config plugins rather than directly modifying `ios/` or `android/`.
- **Adopt Expo Router v3+**: Leverage type-safe routes, layout routes (`_layout.tsx`), and automated deep linking.
- **Use EAS Build for Remote CI/CD**: Build production `.ipa` and `.aab` packages with automated credential and certificate management.
- **Implement Hermes Engine**: Run the Hermes JavaScript engine (default) for fast startup times and minimal memory footprints.

**Don't**:

- **Don't hardcode sensitive secrets in `app.json`**: Store API secrets in EAS Secrets or runtime environment variables.
- **Don't use legacy `expo publish`**: Migrate to modern EAS Update (`eas update`) with rollout channels.
- **Don't bypass Apple Privacy Manifests**: Ensure all third-party native libraries declare appropriate data collection reasons.

## Troubleshooting

| Error                          | Cause                                     | Solution                                            |
| :----------------------------- | :---------------------------------------- | :-------------------------------------------------- |
| `Native module cannot be null` | Library installed but not in the runtime. | Rebuild the Development Build (`npx expo run:ios`). |
| `EAS Build failed`             | Configuration error or build timeout.     | Check logs on expo.dev; run `npx expo-doctor`.      |
| `Expo Go crashes on launch`    | Incompatible SDK version or native code.  | Update Expo Go or switch to Development Build.      |

## References

- [Expo Documentation](https://docs.expo.dev)
- [EAS Documentation](https://docs.expo.dev/eas)
- [Expo Core Libraries](https://docs.expo.dev/versions/latest/)
