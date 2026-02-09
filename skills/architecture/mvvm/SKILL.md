---
name: mvvm
description: Model-View-ViewModel pattern for reactive UI binding. Use for mobile and desktop apps.
---

# MVVM (Model-View-ViewModel)

Architectural pattern with two-way data binding.

## When to Use

- Mobile applications (SwiftUI, Compose)
- Desktop apps (WPF, macOS)
- Reactive UI frameworks
- Testable UI logic

## Quick Start

```swift
// SwiftUI MVVM
@Observable class UserViewModel {
    var user: User?
    var isLoading = false

    func loadUser(id: String) async {
        isLoading = true
        user = try? await userService.fetch(id)
        isLoading = false
    }
}

struct UserView: View {
    @State var viewModel = UserViewModel()

    var body: some View {
        if viewModel.isLoading {
            ProgressView()
        } else if let user = viewModel.user {
            Text(user.name)
        }
    }
}
```

## Core Concepts

### ViewModel

```kotlin
// Android Compose
class UserViewModel(
    private val repository: UserRepository
) : ViewModel() {
    private val _user = MutableStateFlow<User?>(null)
    val user: StateFlow<User?> = _user.asStateFlow()

    fun loadUser(id: String) {
        viewModelScope.launch {
            _user.value = repository.getUser(id)
        }
    }
}

@Composable
fun UserScreen(viewModel: UserViewModel = hiltViewModel()) {
    val user by viewModel.user.collectAsState()
    user?.let { Text(it.name) }
}
```

### Data Binding

```typescript
// Angular style
@Component({
  template: `<input [(ngModel)]="user.name" />`,
})
class UserComponent {
  user = { name: "" };
}
```

## Best Practices

**Do**: Keep View passive, ViewModel testable without UI
**Don't**: Reference View from ViewModel

## References

- [MVVM Pattern](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93viewmodel)
