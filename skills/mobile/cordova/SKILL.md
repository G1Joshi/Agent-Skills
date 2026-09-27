---
name: cordova
description: Expert Apache Cordova assistance covering hybrid WebView architectures, config.xml configuration, custom plugin authoring, and platform CLI tooling. Use when maintaining or migrating legacy Cordova apps, managing device hardware plugins, or building cross-platform web shells.
---

# Cordova

Apache Cordova (formerly PhoneGap) wraps HTML/CSS/JS apps in a native WebView container. While largely superseded by Capacitor and React Native, it remains active (CLI 13.x) for specific legacy use cases.

## When to Use

- **Legacy Hybrid App Maintenance**: Maintaining existing enterprise Cordova / PhoneGap codebases.
- **Migrating to Capacitor**: Modernizing legacy Cordova projects into modern Capacitor runtimes with minimal friction.
- **Cross-Platform Plugin Integration**: Utilizing long-standing Cordova plugins for specialized industrial hardware (barcode scanners, thermal printers).
- **Zero-Native Mobile Builds**: Compiling HTML/JS into mobile binaries using command line build scripts without touching native IDEs.

## Quick Start

```bash
npm install -g cordova
cordova create hello com.example.hello HelloWorld
cd hello
cordova platform add android
cordova platform add ios
cordova run android
```

## Core Concepts

#Declarative config.xml Schema

The central manifest orchestrates app metadata, permissions, preferences, and plugin parameters across platforms:

```xml
<?xml version='1.0' encoding='utf-8'?>
<widget id="com.example.logistics" version="2.4.0" xmlns="http://www.w3.org/ns/widgets" xmlns:cdv="http://cordova.apache.org/ns/1.0">
    <name>LogisticsTracker</name>
    <description>Enterprise warehouse scanning application.</description>
    <preference name="Orientation" value="portrait" />
    <preference name="DisallowOverscroll" value="true" />
    <platform name="android">
        <preference name="AndroidXEnabled" value="true" />
    </platform>
</widget>
```

#deviceready Lifecycle Event

Cordova requires waiting for native bridge initialization before invoking any hardware plugin APIs:

```javascript
document.addEventListener("deviceready", onDeviceReady, false);

function onDeviceReady() {
  console.log("Running cordova-" + cordova.platformId + "@" + cordova.version);
  // Safe to invoke native plugins
  navigator.splashscreen.hide();
}
```

#Native Plugin Hook Architecture

Hooks execute arbitrary Node.js scripts during the build lifecycle (e.g. copying release Google Services JSON, injecting Gradle properties):

```javascript
// hooks/after_prepare.js
const fs = require("fs");
const path = require("path");

module.exports = function (context) {
  const root = context.opts.projectRoot;
  const src = path.join(root, "config/google-services.json");
  const dest = path.join(root, "platforms/android/app/google-services.json");
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, dest);
    console.log("Injected google-services.json into Android platform.");
  }
};
```

## Common Patterns

### Migration to Capacitor

Many teams use Capacitor as a drop-in replacement runner for Cordova apps to modernize the buildstack while keeping the frontend code.

```bash
npm install @capacitor/cli @capacitor/core
npx cap init
# Capacitor automatically reads config.xml and supports most Cordova plugins
```

## Best Practices (2026)

**Do**:

- **Enable AndroidX**: Ensure `AndroidXEnabled` preference is true in `config.xml` to prevent build failures with modern Android SDKs.
- **Plan Migration to Capacitor**: Treat Cordova as maintenance-only; transition new features to modern tools like Capacitor.
- **Pin Exact Plugin Versions**: Avoid dynamic plugin versions (`latest`) in `config.xml` to ensure reproducible CI/CD builds.
- **Check for Plugin Deprecations**: Audit plugins against current iOS WKWebView and Android 14+ target SDK requirements.

**Don't**:

- **Don't commit `platforms/` or `plugins/`**: Keep them in `.gitignore` and regenerate them from `config.xml` and `package.json`.
- **Don't use synchronous file I/O**: Heavy synchronous web operations inside Cordova WebViews freeze UI rendering.
- **Don't rely on obsolete plugins**: Discard abandoned plugins that lack 64-bit binaries or modern privacy manifests.

## Troubleshooting

| Error                    | Cause                                        | Solution                                                      |
| :----------------------- | :------------------------------------------- | :------------------------------------------------------------ |
| `deviceready not firing` | JS error before event or missing cordova.js. | Check console; ensure `cordova.js` is included in index.html. |
| `White Screen`           | CSP blocking scripts or syntax error.        | Check `Content-Security-Policy` and remote debugging.         |
| `Gradle build failed`    | Java/Gradle version mismatch.                | Check `cordova requirements android` output.                  |

## References

- [Apache Cordova Docs](https://cordova.apache.org/docs/en/latest/)
- [Migrating from Cordova to Capacitor](https://capacitorjs.com/docs/cordova/migrating)
