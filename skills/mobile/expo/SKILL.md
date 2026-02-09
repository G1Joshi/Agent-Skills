---
name: expo
description: Expo React Native development with managed workflow. Use for rapid mobile development.
---

# Expo

Managed React Native development platform.

## When to Use

- Rapid mobile prototyping
- React Native without native code
- Over-the-air updates
- Cross-platform from single codebase

## Quick Start

```bash
# Create new project
npx create-expo-app my-app
cd my-app
npx expo start
```

```tsx
import { Text, View } from "react-native";

export default function App() {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text>Hello Expo!</Text>
    </View>
  );
}
```

## Core Concepts

### Expo Router

```tsx
// app/_layout.tsx
import { Stack } from "expo-router";

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
  return (
    <View>
      <Link href="/user/123">Go to User</Link>
    </View>
  );
}

// app/user/[id].tsx
import { useLocalSearchParams } from "expo-router";

export default function User() {
  const { id } = useLocalSearchParams();
  return <Text>User: {id}</Text>;
}
```

### Expo SDK

```tsx
import * as ImagePicker from "expo-image-picker";
import * as Location from "expo-location";

async function pickImage() {
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    quality: 1,
  });

  if (!result.canceled) {
    return result.assets[0].uri;
  }
}

async function getLocation() {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== "granted") return null;

  return await Location.getCurrentPositionAsync({});
}
```

## Common Patterns

### EAS Build

```json
// eas.json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal"
    },
    "production": {}
  }
}
```

```bash
# Build
eas build --platform all
eas build --profile development

# Submit to stores
eas submit --platform ios
eas submit --platform android
```

### Environment Variables

```bash
# .env
EXPO_PUBLIC_API_URL=https://api.example.com
```

```tsx
const apiUrl = process.env.EXPO_PUBLIC_API_URL;
```

## Best Practices

**Do**:

- Use Expo Router for navigation
- Leverage EAS for builds
- Use EXPO*PUBLIC* for env vars
- Test on real devices

**Don't**:

- Eject unnecessarily
- Ignore SDK versions
- Skip OTA update testing
- Use incompatible libraries

## Troubleshooting

| Issue            | Cause                | Solution            |
| ---------------- | -------------------- | ------------------- |
| Module not found | SDK version mismatch | Check compatibility |
| Build failed     | Native dependency    | Use dev client      |
| Metro error      | Cache issue          | Clear cache         |

## References

- [Expo Documentation](https://docs.expo.dev/)
- [Expo Router](https://docs.expo.dev/router/introduction/)
