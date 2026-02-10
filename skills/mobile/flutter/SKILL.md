---
name: flutter
description: Flutter cross-platform UI toolkit with Dart. Use for mobile/web/desktop.
---

# Flutter

Flutter is Google's UI toolkit for building natively compiled applications for mobile, web, and desktop from a single codebase. It uses the Dart programming language and the Skia/Impeller graphics engine to render high-performance, pixel-perfect UIs.

## When to Use

- Building high-performance Android and iOS apps with a single codebase.
- Creating custom, branded UI designs that need to look identical across platforms.
- Developing prototypes or MVPs quickly with Hot Reload.
- needing a solution that compiles to native code (ARM/x86) and WebAssembly.

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

### Widget Tree & Element Tree

Flutter uses a reactive style where the UI is built from a tree of immutable Widgets.

- **Widget**: A configuration for an Element. Immutable description of part of the UI.
- **Element**: An instantiation of a Widget at a particular location in the tree. Mutable manager of state and lifecycle.
- **RenderObject**: The actual object that gets painted on the screen.

### State Management (Bloc)

Modern Flutter apps often use the **Bloc** (Business Logic Component) pattern for separation of concerns and predictable state.

- **Events**: Inputs to the Bloc (e.g., button pressed).
- **States**: Outputs from the Bloc (e.g., loading, data loaded).
- **Bloc/Cubit**: The class that receives events and emits new states.
- **BlocBuilder**: Widget that rebuilds in response to new states.

### Asynchronous Programming (Isolates)

Dart is single-threaded but event-driven. Heavy computations should be moved to background **Isolates** to avoid blocking the UI thread (jank).

## Common Patterns

### Feature-First Architecture

Organize files by feature rather than by layer.

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

- **Data Layer**: Repositories, API clients (Dio/Http), DTOs.
- **Domain Layer**: Entities, business logic (pure Dart).
- **Presentation Layer**: Widgets, Blocs/Cubits.

## Best Practices

**Do**:

- **Use `const` constructors** everywhere possible to optimize rebuilds.
- **Use `GoRouter`** for deep linking and declarative navigation.
- **Use `flutter_bloc`** to separate business logic from UI.
- **Use `ThemeData`** and `TextTheme` for consistent styling.

**Don't**:

- **Don't put complex logic** inside `build()` methods.
- **Don't misuse `setState`** for complex global state.
- **Don't block the main thread**; use `compute()` for heavy JSON parsing or calculations.

## Troubleshooting

| Error | Cause | Solution |
140: | :--------------------------------------------- | :--------------------------------------------- | :----------------------------------------------------------- |
141: | `RenderFlex overflowed by ... pixels` | Content is too wide/tall for the parent. | Wrap in `Expanded`, `Flexible`, or `SingleChildScrollView`. |
142: | `ProviderNotFoundException` | Reading a Bloc without a provider up the tree. | Ensure `BlocProvider` wraps the widget trying to access it. |
143: | `LateInitializationError` | Accessing a `late` variable before assignment. | Ensure generic initialization or use nullable types locally. |
144: | `Vertical viewport was given unbounded height` | ListView inside Column without constraints. | Wrap ListView in `Expanded` or `SizedBox`. |

## References

- [Official Flutter Docs](https://docs.flutter.dev)
- [Bloc Library Documentation](https://bloclibrary.dev)
- [Flutter Engineering](https://medium.com/flutter)
