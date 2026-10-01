---
name: ionic
description: Expert Ionic Framework assistance covering responsive mobile UI components, Ionic Vue/React/Angular integrations, mobile navigation, and Capacitor deployment. Use when designing mobile-first web applications, building hybrid apps, or standardizing cross-platform UI components.
---

# Ionic

Ionic Framework is an open-source UI toolkit for building performant, high-quality mobile and desktop apps using web technologies (HTML, CSS, JavaScript) with integrations for Angular, React, and Vue.

## When to Use

- **Web-First Cross-Platform Apps**: Building mobile-optimized applications using standard web frameworks (Vue, React, Angular) with Ionic UI components.
- **Design System Consistency**: Ensuring UI components adapt automatically to iOS (Cupertino) and Android (Material Design) design guidelines.
- **Hybrid PWA + Mobile Store Deployment**: Serving a production Progressive Web App that compiles directly to iOS/Android via Capacitor.
- **Enterprise CRUD Applications**: Delivering business applications rapidly with prebuilt form controls, virtual scrollers, and adaptive navigation.

## Quick Start

```bash
# Install CLI
npm install -g @ionic/cli

# Start a React app with tabs
ionic start myApp tabs --type=react --capacitor
cd myApp
ionic serve
```

```tsx
// src/pages/Home.tsx (Ionic React)
import {
  IonContent,
  IonHeader,
  IonPage,
  IonTitle,
  IonToolbar,
  IonButton,
  IonIcon,
  IonList,
  IonItem,
  IonLabel,
} from "@ionic/react";
import { camera } from "ionicons/icons";
import { Camera, CameraResultType } from "@capacitor/camera";

const Home: React.FC = () => {
  const takePhoto = async () => {
    const image = await Camera.getPhoto({
      quality: 90,
      allowEditing: false,
      resultType: CameraResultType.Uri,
    });
    console.log("Photo URI", image.webPath);
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Ionic Camera</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <div style={{ padding: 20 }}>
          <IonButton expand="block" onClick={takePhoto}>
            <IonIcon slot="start" icon={camera} />
            Take Photo
          </IonButton>
        </div>
      </IonContent>
    </IonPage>
  );
};
export default Home;
```

## Core Concepts

### Platform-Adaptive UI (Material vs Cupertino)

Ionic components automatically detect host operating systems and adjust styling, typography, ripple effects, and icon placements:

```tsx
import React from "react";
import {
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButton,
  IonIcon,
} from "@ionic/react";
import { arrowForwardOutline } from "ionicons/icons";

export const DashboardScreen: React.FC = () => (
  <>
    <IonHeader>
      <IonToolbar color="primary">
        <IonTitle>Enterprise Dashboard</IonTitle>
      </IonToolbar>
    </IonHeader>
    <IonContent className="ion-padding">
      <IonButton expand="block" shape="round">
        Continue <IonIcon slot="end" icon={arrowForwardOutline} />
      </IonButton>
    </IonContent>
  </>
);
```

### Mobile Navigation with IonRouterOutlet

Maintains separate page navigation stacks for iOS and Android, caching previous pages in the DOM to preserve scroll positions:

```tsx
import { IonReactRouter } from "@ionic/react-router";
import { IonRouterOutlet } from "@ionic/react";
import { Route, Redirect } from "react-router-dom";

export const AppRouter: React.FC = () => (
  <IonReactRouter>
    <IonRouterOutlet>
      <Route exact path="/dashboard" component={DashboardScreen} />
      <Route exact path="/details/:id" component={DetailScreen} />
      <Redirect exact from="/" to="/dashboard" />
    </IonRouterOutlet>
  </IonReactRouter>
);
```

### Ionic Lifecycle Events

Ionic provides component lifecycle hooks that trigger when views enter and leave the active navigation stack (complementing React/Vue lifecycles):

```typescript
import { useIonViewDidEnter, useIonViewDidLeave } from "@ionic/react";

const AnalyticsView: React.FC = () => {
  useIonViewDidEnter(() => {
    // Triggers when page finishes animating into view
    fetchLatestMetrics();
  });

  useIonViewDidLeave(() => {
    // Triggers when navigated away (page remains cached in DOM)
    cancelActiveTimers();
  });

  return <div>Analytics Active</div>;
};
```

## Common Patterns

### Native Biometric Authentication with Capacitor

**Problem**: Secure mobile app access using FaceID / TouchID on iOS and Android.  
**Solution**: Integrate `@capacitor-community/biometric-auth`.

```typescript
import { BiometricAuth } from "@capacitor-community/biometric-auth";

async function authenticateUser(): Promise<boolean> {
  const available = await BiometricAuth.checkBiometry();
  if (!available.isAvailable) return false;

  const result = await BiometricAuth.verify({
    reason: "Authenticate to view sensitive account details",
    title: "Biometric Login",
  });
  return result.verified;
}
```

## Best Practices

**Do**:

- Pair with Modern Capacitor: Always use Capacitor (not Cordova) for native device access and plugin capabilities.
- Use Ionic CSS Variables: Customize themes globally using CSS custom properties (`--ion-color-primary`, `--ion-background-color`).
- Implement Virtual Scrolling: Use `@ionic/react` virtual scroller or TanStack Virtual for long item feeds to prevent DOM bloat.
- Respect Native Back Navigation: Handle hardware Android back buttons and iOS swipe-to-go-back gestures gracefully.

**Don't**:

- Place heavy animations in WebViews: Use CSS transforms and hardware-accelerated transitions; avoid expensive DOM mutations.
- Ignore notch safe areas: Ensure header and footer toolbars leverage Ionic's built-in safe area insets.
- Mix non-Ionic modal systems: Use `IonModal` to ensure focus management and native hardware dismiss events work predictably.

## Troubleshooting

| Error                   | Cause                            | Solution                                                     |
| :---------------------- | :------------------------------- | :----------------------------------------------------------- |
| `White Screen of Death` | JavaScript error during startup. | Check remote debugging console (Chrome/Safari).              |
| `CORS Error` on device  | Web View calling external API.   | Configure server CORS or use `@capacitor-community/http`.    |
| `Keyboard covers input` | Scroll view not resizing.        | Ensure `<ion-content>` is used; check `windowSoftInputMode`. |

## References

- [Ionic Framework Docs](https://ionicframework.com/docs)
- [Capacitor Documentation](https://capacitorjs.com/docs)
- [Ionic UI Components](https://ionicframework.com/docs/components)
