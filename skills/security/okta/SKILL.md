---
name: okta
description: Okta identity management. Use for enterprise SSO.
---

# Okta

Okta is the enterprise standard for Identity and Access Management (IAM). While Auth0 (owned by Okta) targets developers/B2C, "Okta Workforce Identity" targets employee access and large B2B integrations.

## When to Use

- **Workforce Identity**: Managing employee access to internal apps (Slack, Jira, AWS).
- **Deep Enterprise Integration**: Complex AD/LDAP syncs, provisioning, and SCIM.
- **Zero Trust**: Implementing device trust signals and context-based access policies.

## Quick Start (OIDC React)

```bash
npm install @okta/okta-react @okta/okta-auth-js
```

```javascript
import { Security, LoginCallback } from "@okta/okta-react";
import { OktaAuth } from "@okta/okta-auth-js";

const oktaAuth = new OktaAuth({
  issuer: "https://{yourOktaDomain}/oauth2/default",
  clientId: "{clientId}",
  redirectUri: window.location.origin + "/login/callback",
});

function App() {
  return (
    <Security oktaAuth={oktaAuth}>
      <Route path="/login/callback" component={LoginCallback} />
      <SecureRoute path="/protected" component={MyProtectedPage} />
    </Security>
  );
}
```

## Core Concepts

### Admin Console

A powerful dashboard for IT admins to manage users, groups, and applications assignments.

### SCIM (System for Cross-domain Identity Management)

Automated provisioning. When you create a user in Okta, it automatically creates the user in Salesforce/Slack.

### Inline Hooks

Customize the authorization flow (similar to Auth0 Actions) by calling out to external REST APIs during the token minting process.

## Best Practices (2025)

**Do**:

- Enforce **Phishing-Resistant MFA** (WebAuthn/FIDO2) for all admin accounts.
- Use **Terraform** Provider for Okta to manage configuration as code.
- Implement **Least Privilege** with granular admin roles.

**Don't**:

- Don't use "API Access Management" features if standard OIDC suffices (saves cost).
- Don't allow long-lived API tokens for sensitive operations.

## Troubleshooting

| Error           | Cause                      | Solution                                                       |
| :-------------- | :------------------------- | :------------------------------------------------------------- |
| `403 Forbidden` | User not appointed to App. | Assign the User or Group to the Application in Okta Console.   |
| `Clock Skew`    | Server time mismatch.      | Ensure servers utilize NTP; JWT validation allows ~2 min skew. |

## References

- [Okta Developer](https://developer.okta.com/)
- [Okta Terraform Provider](https://registry.terraform.io/providers/okta/okta/latest/docs)
