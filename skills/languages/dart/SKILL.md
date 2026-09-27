---
name: dart
description: Expert Dart programming assistance covering sound null safety, async/await futures, streams, pattern matching, records, and class constructors. Use when writing Dart logic, developing Flutter mobile/web apps, or building Dart CLI applications.
---

# Dart

Modern Dart development with null safety, pattern matching, and Flutter integration.

## When to Use

- **Cross-Platform Flutter Development**: The primary language powering Flutter applications across iOS, Android, Web, and Desktop.
- **Command-Line & Backend Services**: Writing fast CLI utilities, build scripts, and server-side Dart services with Shelf.
- **Ahead-of-Time (AOT) & Just-in-Time (JIT) Compilation**: Rapid development via Stateful Hot Reload (JIT) and high-speed native release binaries (AOT).
- **Multiplatform Code Sharing**: Sharing models, validation, and domain logic across mobile apps and web consoles.

## Quick Start

```dart
class User {
  final String id;
  final String name;
  final String email;

  const User({required this.id, required this.name, required this.email});

  factory User.fromJson(Map<String, dynamic> json) => User(
    id: json['id'] as String,
    name: json['name'] as String,
    email: json['email'] as String,
  );
}
```

## Core Concepts

#Sound Null Safety

Variables cannot contain `null` unless explicitly declared with `?`; static analysis guarantees zero runtime null pointer crashes:

```dart
String formatGreeting(String name, String? title) {
  // title is nullable, name is strictly non-nullable
  final prefix = title != null ? '$title ' : '';
  return 'Hello, $prefix$name!';
}
```

#Records and Pattern Matching (Dart 3)

Returns multiple strongly-typed values and destructures patterns cleanly:

```dart
// Multi-return via Records
(double lat, double lng) getCoordinates() {
  return (40.7128, -74.0060);
}

void processLocation() {
  final (lat, lng) = getCoordinates();
  print('Latitude: $lat, Longitude: $lng');
}
```

#Asynchronous Streams & Reactive Pipelines

Generates and consumes asynchronous streams of events:

```dart
Stream<int> countStream(int max) async* {
  for (int i = 1; i <= max; i++) {
    await Future.delayed(const Duration(milliseconds: 100));
    yield i;
  }
}
```

## Common Patterns

### Async/Await

```dart
Future<User> fetchUser(String id) async {
  final response = await http.get(Uri.parse('$baseUrl/users/$id'));
  if (response.statusCode != 200) {
    throw Exception('Failed to load user');
  }
  return User.fromJson(jsonDecode(response.body));
}

// Parallel execution
Future<void> loadData() async {
  final results = await Future.wait([
    fetchUser('1'),
    fetchOrders('1'),
  ]);
}

// Streams
Stream<int> countStream(int max) async* {
  for (int i = 0; i < max; i++) {
    await Future.delayed(Duration(seconds: 1));
    yield i;
  }
}
```

### Extensions

```dart
extension StringExtension on String {
  String capitalize() =>
    isEmpty ? this : '${this[0].toUpperCase()}${substring(1)}';

  bool get isValidEmail =>
    RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(this);
}
```

## Best Practices (2026)

**Do**:

- **Mark Immutable Widgets and Constants with `const`**: Allow the Flutter compiler to skip rebuilds for constant subtrees.
- **Enforce Strict Linter Rules**: Configure `flutter_lints` or `very_good_analysis` in `analysis_options.yaml`.
- **Use Sealed Classes for State Modeling**: Leverage `sealed class` to ensure exhaustive switch statements across UI states.
- **Close Stream Controllers**: Always invoke `.close()` on `StreamController` instances inside dispose methods.

**Don't**:

- **Don't use the `!` null-assertion operator carelessly**: Unchecked `!` throws runtime exceptions; handle nulls with `??` or pattern matching.
- **Don't execute heavy synchronous parsing in the main isolate**: Offload heavy JSON parsing or crypto to background isolates via `Isolate.run()`.
- **Don't declare variables as `dynamic`**: Avoid `dynamic`; use `Object?` or explicit generic types to preserve compile-time safety.

## Troubleshooting

| Error                              | Cause                          | Solution                 |
| ---------------------------------- | ------------------------------ | ------------------------ |
| `Null check operator used on null` | Using `!` on null value        | Add null check first     |
| `LateInitializationError`          | Accessing late var before init | Initialize before access |
| `type 'Null' is not a subtype`     | Type mismatch with null        | Check nullable types     |

## References

- [Dart Official Docs](https://dart.dev/guides)
- [Effective Dart](https://dart.dev/effective-dart)
