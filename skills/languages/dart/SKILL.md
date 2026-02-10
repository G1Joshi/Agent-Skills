---
name: dart
description: Dart programming for Flutter mobile and web development. Use for .dart files.
---

# Dart

Modern Dart development with null safety, pattern matching, and Flutter integration.

## When to Use

- Working with `.dart` files
- Building Flutter mobile/web/desktop apps
- Server-side Dart development
- Creating packages for pub.dev

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

### Null Safety

```dart
// Non-nullable by default
String name = 'John';

// Nullable with ?
String? maybeNull;

// Late initialization
late final String lazyInit;

// Null-aware operators
String greeting = person?.name ?? 'Guest';
person?.address?.city;
```

### Records & Pattern Matching (Dart 3)

```dart
// Records
(String, int) getPerson() => ('John', 25);

// Destructuring
final (name, age) = getPerson();

// Switch expressions with patterns
String describe(Object obj) => switch (obj) {
  int i when i < 0 => 'negative',
  int i => 'positive: $i',
  String s => 'string: $s',
  _ => 'unknown',
};

// Sealed classes
sealed class Result<T> {}
class Success<T> extends Result<T> { final T value; Success(this.value); }
class Failure<T> extends Result<T> { final String error; Failure(this.error); }
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

## Best Practices

**Do**:

- Use `const` constructors when possible
- Prefer `final` for immutable variables
- Use named parameters with `required`
- Follow effective_dart lints

**Don't**:

- Use `dynamic` when type is known
- Force unwrap with `!` unnecessarily
- Create God classes (keep small)
- Ignore `late` initialization errors

## Troubleshooting

| Error                              | Cause                          | Solution                 |
| ---------------------------------- | ------------------------------ | ------------------------ |
| `Null check operator used on null` | Using `!` on null value        | Add null check first     |
| `LateInitializationError`          | Accessing late var before init | Initialize before access |
| `type 'Null' is not a subtype`     | Type mismatch with null        | Check nullable types     |

## References

- [Dart Official Docs](https://dart.dev/guides)
- [Effective Dart](https://dart.dev/effective-dart)
