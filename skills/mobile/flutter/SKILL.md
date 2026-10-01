---
name: flutter
description: Expert Flutter assistance covering declarative widget trees, state management (Bloc/Riverpod/Provider), custom painters, platform channels, and cross-platform compilation. Use when building iOS, Android, web, and desktop applications using Flutter and Dart.
---

# Flutter

Flutter is Google's UI toolkit for building natively compiled applications for mobile, web, and desktop from a single codebase. It uses the Dart programming language and the Skia/Impeller graphics engine to render high-performance, pixel-perfect UIs.

## When to Use

- **High-Fidelity Cross-Platform Apps**: Building pixel-perfect, hardware-accelerated applications for iOS, Android, Web, and Desktop from a single Dart codebase.
- **Custom Brand & Animation Experiences**: Creating bespoke UI widgets, smooth transitions, and complex interactive canvases using Impeller rendering engine.
- **Fast Prototyping & Iteration**: Utilizing sub-second Stateful Hot Reload to iterate rapidly on UI components and application logic.
- **Unified Enterprise Applications**: Maintaining unified multi-screen architectures spanning mobile tablets, point-of-sale systems, and web consoles.

## Quick Start

```dart
// main.dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';

void main() {
  runApp(const MyApp());
}

// Router configuration
final _router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomePage(),
    ),
  ],
);

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => CounterCubit(),
      child: MaterialApp.router(
        routerConfig: _router,
        theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.blue),
      ),
    );
  }
}

// Bloc/Cubit Logic
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);

  void increment() => emit(state + 1);
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    // Access state via context.read/watch or BlocBuilder
    final count = context.select((CounterCubit cubit) => cubit.state);

    return Scaffold(
      appBar: AppBar(title: const Text('Flutter & Bloc')),
      body: Center(
        child: Text(
          'Count: $count',
          style: Theme.of(context).textTheme.headlineMedium,
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => context.read<CounterCubit>().increment(),
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

## Core Concepts

### Widget Tree, Element Tree & RenderObject Architecture

Flutter bypasses platform WebViews and OEM widgets, rendering directly via the Impeller graphics engine:

```dart
// Declarative immutable widget tree
class MetricCard extends StatelessWidget {
  final String label;
  final double value;

  const MetricCard({super.key, required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: Theme.of(context).colorScheme.surfaceVariant,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: Theme.of(context).textTheme.bodySmall),
          const SizedBox(height: 4),
          Text('\$${value.toStringAsFixed(2)}', style: Theme.of(context).textTheme.headlineMedium),
        ],
      ),
    );
  }
}
```

### Predictable State Management with Bloc / Cubit

Decouples UI layout from reactive business logic via event-driven streams:

```dart
// State Definition
sealed class CounterState {}
class CounterValue extends CounterState { final int count; CounterValue(this.count); }

// Cubit Logic
class CounterCubit extends Cubit<CounterState> {
  CounterCubit() : super(CounterValue(0));
  void increment() {
    final current = (state as CounterValue).count;
    emit(CounterValue(current + 1));
  }
}

// Consumed in UI via BlocBuilder
BlocBuilder<CounterCubit, CounterState>(
  builder: (context, state) {
    return Text('Count: ${(state as CounterValue).count}');
  },
)
```

### Platform Channels for Native Integration

Bidirectional asynchronous message passing between Dart and platform-native Swift/Kotlin:

```dart
class BatteryService {
  static const _channel = MethodChannel('com.example.app/battery');

  static Future<int> getBatteryLevel() async {
    try {
      final int level = await _channel.invokeMethod('getBatteryLevel');
      return level;
    } on PlatformException catch (e) {
      return -1;
    }
  }
}
```

## Common Patterns

### Feature-First Architecture

**Problem**: Layer-first project organization (`controllers/`, `views/`) becoming unmaintainable as apps scale.

**Solution**:
Organize files into cohesive domain feature modules:

```text
lib/
  src/
    features/
      auth/
        data/
        domain/
        presentation/
          bloc/
          views/
      products/
    shared/
      components/
      constants/
    app.dart
    main.dart
```

### Clean Architecture with Repositories

**Problem**: Directly coupling UI widget code to HTTP clients or database drivers breaks modularity and makes unit testing difficult.

**Solution**:

```dart
abstract interface class UserRepository {
  Future<User> getUser(String id);
}

class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;

  UserRepositoryImpl({required this.remoteDataSource, required this.localDataSource});

  @override
  Future<User> getUser(String id) async {
    try {
      final userModel = await remoteDataSource.fetchUser(id);
      await localDataSource.cacheUser(userModel);
      return userModel.toEntity();
    } catch (_) {
      return await localDataSource.getCachedUser(id);
    }
  }
}
```

## Best Practices

**Do**:

- Leverage `const` Constructors Everywhere: Mark immutable widgets with `const` to allow Flutter to skip unnecessary widget rebuilds.
- Rely on the Impeller Engine: Ensure modern Impeller rendering is active on iOS and Android to prevent shader compilation jank.
- Split Large Build Methods into Subwidgets: Extract deep widget hierarchies into dedicated `StatelessWidget` classes for clean rebuild scopes.
- Implement Strict Lint Rules: Enforce `flutter_lints` or `very_good_analysis` in `analysis_options.yaml`.

**Don't**:

- Perform async operations directly inside `build()`: Never call HTTP requests or database operations in build methods.
- Overuse `setState` in Root Widgets: Keep state local; triggering top-level `setState` forces excessive full-tree recomposition.
- Hardcode fixed pixel sizes for layouts: Use `LayoutBuilder`, `MediaQuery`, and Flexible/Expanded widgets for responsive scaling.

## Troubleshooting

| Error                                          | Cause                                          | Solution                                                     |
| :--------------------------------------------- | :--------------------------------------------- | :----------------------------------------------------------- |
| `RenderFlex overflowed by ... pixels`          | Content is too wide/tall for the parent.       | Wrap in `Expanded`, `Flexible`, or `SingleChildScrollView`.  |
| `ProviderNotFoundException`                    | Reading a Bloc without a provider up the tree. | Ensure `BlocProvider` wraps the widget trying to access it.  |
| `LateInitializationError`                      | Accessing a `late` variable before assignment. | Ensure generic initialization or use nullable types locally. |
| `Vertical viewport was given unbounded height` | ListView inside Column without constraints.    | Wrap ListView in `Expanded` or `SizedBox`.                   |

## References

- [Official Flutter Docs](https://docs.flutter.dev)
- [Bloc Library Documentation](https://bloclibrary.dev)
- [Flutter Engineering](https://medium.com/flutter)
