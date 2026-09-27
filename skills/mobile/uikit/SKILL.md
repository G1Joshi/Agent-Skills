---
name: uikit
description: Expert UIKit assistance covering UIViewController lifecycles, Auto Layout programmatically, UITableView/UICollectionView architectures, delegates, and view hierarchies. Use when maintaining production iOS applications, writing custom UIKit components, or bridging UIKit with SwiftUI.
---

# UIKit

UIKit is the traditional, imperative framework for building iOS user interfaces. While SwiftUI is the future, UIKit remains essential for maintaining existing apps and unrestricted access to the OS.

## When to Use

- **Production iOS Codebase Maintenance**: Maintaining and extending established enterprise iOS applications built on UIKit.
- **Fine-Grained Touch & Gesture Control**: Implementing bespoke drag-and-drop, gesture recognizers, and custom touch tracking.
- **Complex UICollectionView Layouts**: Building high-performance custom layouts with `UICollectionViewCompositionalLayout` and Diffable Data Sources.
- **SwiftUI Interoperability**: Hosting complex UIKit view controllers inside SwiftUI via `UIViewControllerRepresentable`.

## Quick Start

```swift
// Programmatic UIKit (No Storyboards) in SceneDelegate
func scene(_ scene: UIScene, willConnectTo session: UISceneSession, options: UIScene.ConnectionOptions) {
    guard let windowScene = (scene as? UIWindowScene) else { return }
    window = UIWindow(windowScene: windowScene)
    window?.rootViewController = UINavigationController(rootViewController: HomeViewController())
    window?.makeKeyAndVisible()
}

class HomeViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBackground
        title = "UIKit Home"

        let button = UIButton(type: .system)
        button.setTitle("Tap Me", for: .normal)
        button.translatesAutoresizingMaskIntoConstraints = false
        view.addSubview(button)

        NSLayoutConstraint.activate([
            button.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            button.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])
    }
}
```

## Core Concepts

#UICollectionView Diffable Data Sources & Compositional Layout

Eliminates index-path calculation bugs by managing list state through unique hashable identifiers and snapshots:

```swift
final class FeedViewController: UIViewController {
    enum Section { case main }
    struct Post: Hashable { let id: UUID; let title: String }

    private var collectionView: UICollectionView!
    private var dataSource: UICollectionViewDiffableDataSource<Section, Post>!

    override func viewDidLoad() {
        super.viewDidLoad()
        configureLayout()
        configureDataSource()
    }

    private func configureLayout() {
        var config = UICollectionLayoutListConfiguration(appearance: .insetGrouped)
        collectionView = UICollectionView(frame: view.bounds, collectionViewLayout: UICollectionViewCompositionalLayout.list(using: config))
        view.addSubview(collectionView)
    }

    private func configureDataSource() {
        let registration = UICollectionView.CellRegistration<UICollectionViewListCell, Post> { cell, _, item in
            var content = cell.defaultContentConfiguration()
            content.text = item.title
            cell.contentConfiguration = content
        }
        dataSource = UICollectionViewDiffableDataSource<Section, Post>(collectionView: collectionView) { cv, ip, item in
            cv.dequeueConfiguredReusableCell(using: registration, for: ip, item: item)
        }
    }
}
```

#UIViewController Lifecycle Flow

Strictly isolates setup, layout, and appearance phases to ensure optimal memory and rendering performance:

```swift
class OrderDetailViewController: UIViewController {
    override func loadView() {
        // Instantiate and assign custom root view (bypassing storyboard)
        self.view = OrderDetailRootView()
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        // One-time data binding, notification registration
    }

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        // Refresh lightweight view state
    }
}
```

#Programmatic Layout Anchor Constraints

Constructs responsive layouts programmatically without external dependencies:

```swift
NSLayoutConstraint.activate([
    headerView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor),
    headerView.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 16),
    headerView.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -16),
    headerView.heightAnchor.constraint(equalToConstant: 64)
])
```

## Common Patterns

#Programmatic Auto Layout with NSLayoutConstraint
**Problem**: Storyboard merge conflicts and fragile constraint debugging in team repositories.  
**Solution**: Construct view hierarchies and constraints purely in Swift.

```swift
final class ProfileViewController: UIViewController {
    private let titleLabel: UILabel = {
        let label = UILabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        label.font = .systemFont(ofSize: 20, weight: .bold)
        return label
    }()

    override func viewDidLoad() {
        super.viewDidLoad()
        view.backgroundColor = .systemBackground
        view.addSubview(titleLabel)

        NSLayoutConstraint.activate([
            titleLabel.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            titleLabel.centerYAnchor.constraint(equalTo: view.centerYAnchor)
        ])
    }
}
```

## Best Practices (2026)

**Do**:

- **Adopt Diffable Data Sources**: Replace error-prone `reloadData()` and `performBatchUpdates()` with atomic `NSDiffableDataSourceSnapshot`.
- **Use `translatesAutoresizingMaskIntoConstraints = false`**: Always disable autotranslation on programmatically created views before activating constraints.
- **Bridge with SwiftUI**: Wrap new feature views in `UIHostingController` rather than rebuilding everything in UIKit.
- **Audit Retain Cycles in Closures**: Capture `[weak self]` in completion handlers and event closures to prevent ViewController leaks.

**Don't**:

- **Don't trigger expensive layout inside `draw(_:)`**: Keep custom core graphics rendering strictly inside draw methods; avoid layout passes.
- **Don't hardcode frame coordinates**: Avoid explicit `CGRect(x: ..., y: ...)` math; use Auto Layout or safe area layout guides.
- **Don't block the main thread**: Perform data decoding and persistence asynchronously and update UIKit views on `MainActor`.

## Troubleshooting

| Error                       | Cause                          | Solution                                                                   |
| :-------------------------- | :----------------------------- | :------------------------------------------------------------------------- |
| `Unsatisfiable Constraints` | Conflicting Auto Layout rules. | Check console log for breaking constraint IDs; simplify rules.             |
| `TableView Updates Crash`   | Inconsistent data vs rows.     | Use Diffable Data Source or ensure data model updates before `insertRows`. |
| `Retain Cycle`              | Strong reference loop.         | Use Memory Graph Debugger; verify `[weak self]`.                           |

## References

- [Apple UIKit Documentation](https://developer.apple.com/documentation/uikit)
- [Modern UIKit Patterns](https://developer.apple.com/videos/play/wwdc2020/10097/)
