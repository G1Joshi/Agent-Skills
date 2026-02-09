---
name: flutter
description: Flutter cross-platform development with widgets, state management, and navigation. Use for .dart mobile apps.
---

# Flutter

Cross-platform UI framework for mobile, web, and desktop.

## When to Use

- Cross-platform mobile apps
- Single codebase for iOS/Android
- Custom UI with animations
- Rapid prototyping

## Quick Start

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('My App')),
        body: const Center(child: Text('Hello Flutter!')),
      ),
    );
  }
}
```

## Core Concepts

### Widgets & State

```dart
class Counter extends StatefulWidget {
  const Counter({super.key});

  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int _count = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $_count'),
        ElevatedButton(
          onPressed: () => setState(() => _count++),
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
```

### Riverpod State Management

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

final counterProvider = StateNotifierProvider<CounterNotifier, int>(
  (ref) => CounterNotifier(),
);

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);

  void increment() => state++;
}

// Usage
class MyWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Text('Count: $count');
  }
}
```

## Common Patterns

### Navigation with GoRouter

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'user/:id',
          builder: (context, state) => UserScreen(
            id: state.pathParameters['id']!,
          ),
        ),
      ],
    ),
  ],
);

// Navigate
context.go('/user/123');
context.push('/user/123');
```

### Async Data

```dart
final userProvider = FutureProvider.autoDispose.family<User, String>(
  (ref, userId) async {
    return ref.read(apiProvider).fetchUser(userId);
  },
);

// In widget
ref.watch(userProvider(userId)).when(
  data: (user) => UserCard(user: user),
  loading: () => const CircularProgressIndicator(),
  error: (error, stack) => Text('Error: $error'),
);
```

## Best Practices

**Do**:

- Use const constructors
- Prefer StatelessWidget
- Use Riverpod for state
- Follow widget composition

**Don't**:

- Put logic in build methods
- Use setState for global state
- Create deep widget trees
- Ignore key parameters

## Troubleshooting

| Issue               | Cause            | Solution                    |
| ------------------- | ---------------- | --------------------------- |
| Widget not updating | Missing setState | Use proper state management |
| Overflow error      | Unbounded size   | Add constraints             |
| Hot reload fails    | State corruption | Hot restart                 |

## References

- [Flutter Documentation](https://flutter.dev/docs)
- [Riverpod Documentation](https://riverpod.dev/)
