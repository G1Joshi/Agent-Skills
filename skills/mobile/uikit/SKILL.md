---
name: uikit
description: UIKit framework for iOS programmatic and storyboard UI. Use for traditional iOS development.
---

# UIKit

Traditional iOS UI framework with imperative patterns.

## When to Use

- Legacy iOS app maintenance
- Complex custom animations
- Low-level UI control
- Bridging with SwiftUI

## Quick Start

```swift
import UIKit

class ViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()

        let label = UILabel()
        label.text = "Hello UIKit!"
        label.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(label)

        NSLayoutConstraint.activate([
            label.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            label.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])
    }
}
```

## Core Concepts

### View Controllers

```swift
class ProfileViewController: UIViewController {
    private let nameLabel = UILabel()
    private let avatarImageView = UIImageView()

    private let user: User

    init(user: User) {
        self.user = user
        super.init(nibName: nil, bundle: nil)
    }

    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        configure(with: user)
    }

    private func setupUI() {
        view.backgroundColor = .systemBackground
        // Add subviews and constraints
    }

    private func configure(with user: User) {
        nameLabel.text = user.name
    }
}
```

### Table Views

```swift
class UsersViewController: UITableViewController {
    private var users: [User] = []

    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.register(UserCell.self, forCellReuseIdentifier: "UserCell")
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        users.count
    }

    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "UserCell", for: indexPath) as! UserCell
        cell.configure(with: users[indexPath.row])
        return cell
    }
}
```

## Common Patterns

### Navigation

```swift
// Push
navigationController?.pushViewController(detailVC, animated: true)

// Present
present(modalVC, animated: true)

// Coordinator pattern
protocol Coordinator {
    var navigationController: UINavigationController { get set }
    func start()
}

class AppCoordinator: Coordinator {
    var navigationController: UINavigationController

    func start() {
        let vc = HomeViewController()
        vc.onUserSelected = { [weak self] user in
            self?.showProfile(for: user)
        }
        navigationController.pushViewController(vc, animated: false)
    }
}
```

### Auto Layout

```swift
NSLayoutConstraint.activate([
    stackView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 16),
    stackView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16),
    stackView.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -16),
])
```

## Best Practices

**Do**:

- Use programmatic Auto Layout
- Implement Coordinator pattern
- Use composition over inheritance
- Support Dynamic Type

**Don't**:

- Force unwrap UI elements
- Block main thread
- Ignore retain cycles
- Mix storyboard and code

## Troubleshooting

| Issue               | Cause               | Solution                    |
| ------------------- | ------------------- | --------------------------- |
| Constraint conflict | Ambiguous layout    | Check constraint priorities |
| Memory leak         | Retain cycle        | Use weak references         |
| UI freeze           | Main thread blocked | Move work to background     |

## References

- [UIKit Documentation](https://developer.apple.com/documentation/uikit)
- [Human Interface Guidelines](https://developer.apple.com/design/)
