---
name: nativescript
description: Expert NativeScript assistance covering direct native API access from JavaScript/TypeScript, XML layouts, custom native wrappers, and cross-platform app deployment. Use when building truly native mobile apps without WebViews using JavaScript or TypeScript.
---

# NativeScript

NativeScript allows you to write native mobile apps using JavaScript/TypeScript, Angular, Vue, or Svelte. Unlike hybrid apps (WebView), it renders **native UI components** and provides **direct access** to all iOS and Android APIs without boilerplate wrappers.

## When to Use

- **Direct Native API Access**: Invoking 100% of native iOS (Objective-C/Swift) and Android (Java/Kotlin) APIs directly from TypeScript/JavaScript.
- **True Native Views without WebViews**: Building apps that render native UIKit/SwiftUI and Android View/Compose hierarchies without WebView overhead.
- **Familiar Web Framework Tooling**: Writing native mobile apps using modern Angular, Vue, React, or Svelte frameworks.
- **High-Performance Hardware Interop**: Interfacing directly with native device hardware libraries and third-party iOS CocoaPods or Android AARs.

## Quick Start

```bash
npm install -g nativescript
ns create my-app
# Choose flavor: Angular, Vue, React, Svelte, or TypeScript
cd my-app
ns run android
```

```typescript
// Accessing Native APIs directly (Android)
const time = new android.text.format.Time();
time.setToNow();
console.log(time.format("%d.%m.%Y"));
```

## Core Concepts

### Direct Native Runtime Bridge

NativeScript generates JavaScript runtime bindings for all platform APIs at compile time, allowing direct native instantiation:

```typescript
import { isIOS, isAndroid } from "@nativescript/core";

export function showNativeNotification(title: string, message: string) {
  if (isIOS) {
    const alert =
      UIAlertController.alertControllerWithTitleMessagePreferredStyle(
        title,
        message,
        UIAlertControllerStyle.Alert,
      );
    alert.addAction(
      UIAlertAction.actionWithTitleStyleHandler(
        "OK",
        UIAlertActionStyle.Default,
        null,
      ),
    );
    UIApplication.sharedApplication.keyWindow.rootViewController.presentViewControllerAnimatedCompletion(
      alert,
      true,
      null,
    );
  } else if (isAndroid) {
    const context = android.app.Application;
    android.widget.Toast.makeText(
      context,
      message,
      android.widget.Toast.LENGTH_SHORT,
    ).show();
  }
}
```

### Declarative Native Layout Containers

NativeScript layouts translate directly into native ViewGroup components:

```xml
<!-- app-main.xml -->
<Page xmlns="http://schemas.nativescript.org/tns.xsd" navigatingTo="onNavigatingTo">
    <ActionBar title="Inventory Manager" class="action-bar" />
    <GridLayout rows="auto, *" columns="*">
        <SearchBar row="0" hint="Search items..." text="{{ searchQuery }}" />
        <ListView row="1" items="{{ inventoryItems }}">
            <ListView.itemTemplate>
                <StackLayout class="item-card">
                    <Label text="{{ name }}" class="item-title" />
                    <Label text="{{ stockCount }}" class="item-subtitle" />
                </StackLayout>
            </ListView.itemTemplate>
        </ListView>
    </GridLayout>
</Page>
```

### Native Plugin Integration via CocoaPods & Gradle

Seamlessly bundles third-party native libraries:

```ruby
# App_Resources/iOS/Podfile
pod 'Lottie', '~> 4.0'
```

## Common Patterns

### Platform-Specific Code Splitting

**Problem**: Writing distinct native implementations for iOS and Android without polluting UI files with runtime branching.

**Solution**:
Use file suffix convention (`.ios.ts` and `.android.ts`) or conditional platform checks:

```typescript
import { isAndroid, isIOS, Application } from "@nativescript/core";

export function showToast(message: string): void {
  if (isAndroid) {
    android.widget.Toast.makeText(
      Application.android.context,
      message,
      android.widget.Toast.LENGTH_SHORT,
    ).show();
  } else if (isIOS) {
    // Present native UIAlertController on root view controller
    const alert =
      UIAlertController.alertControllerWithTitleMessagePreferredStyle(
        null,
        message,
        UIAlertControllerStyle.Alert,
      );
    Application.ios.rootController.presentViewControllerAnimatedCompletion(
      alert,
      true,
      null,
    );
  }
}
```

## Best Practices

**Do**:

- Use Modern Framework Flavors: Prefer `@nativescript/angular` or `@nativescript/vue` for modern component architectures.
- Cache Native Object Lookups: Store repeated native references instead of constantly traversing the JS-to-native reflection bridge.
- Implement Virtualized Lists: Always use `ListView` or `CollectionView` rather than repeating items inside a `ScrollView`.
- Test on Physical Devices: Native bridge behavior and memory performance differ significantly between simulators and actual devices.

**Don't**:

- Use HTML/DOM APIs: There is no browser DOM in NativeScript; do not reference `document.getElementById` or `window`.
- Block the Native UI Thread: Offload heavy computational algorithms to background Web Workers.
- Ignore Platform Differences: Account for distinct iOS navigation controllers versus Android activity back-stack lifecycles.

## Troubleshooting

| Error               | Cause                                     | Solution                                                     |
| :------------------ | :---------------------------------------- | :----------------------------------------------------------- |
| `Marshalling Error` | Passing wrong type to native interaction. | Check native docs and cast types if needed.                  |
| `Out of Memory`     | Large images or memory leaks.             | Use `image-cache-it` or proper GC disposal management.       |
| `Build Failed`      | Native dependency issues.                 | `ns clean`, remove `platforms/` and `node_modules/`, re-run. |

## References

- [NativeScript Docs](https://docs.nativescript.org/)
- [NativeScript Plugins](https://market.nativescript.org/)
