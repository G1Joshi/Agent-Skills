---
name: burpsuite
description: Burp Suite web security testing. Use for penetration testing.
---

# Burp Suite

Burp Suite is an integrated platform for performing security testing of web applications. It ranges from mapping and analyzing an application's attack surface to finding and exploiting vulnerabilities.

## When to Use

- **Penetration Testing**: The #1 tool for manual security assessments.
- **Advanced Attack Simulation**: When you need to intercept, modify, and replay requests manually.
- **Fuzzing**: Sending thousands of payloads to find SQLi, XSS, or logic bugs (Intruder).

## Core Concepts

### Proxy

Intersects HTTP/S traffic between your browser and the target app. Allows you to pause, inspect, and modify requests on the fly.

### Repeater

Lets you manually modify a request and resend it over and over to test how the server responds to different inputs.

### Intruder

Automated fuzzing tool. You define payload positions (e.g., a query param), and Burp iterates through a list of payloads (SQL injection strings, XSS vectors).

## Best Practices (2025)

**Do**:

- **Install the CA Certificate**: Essential for intercepting HTTPS traffic.
- **Scope Your Target**: STRICTLY define the scope to avoid accidentally attacking 3rd party services (Google Analytics, CDNs).
- **Use Extensions**: Determine usage of the "BApp Store" (e.g., Turbo Intruder, Logger++).

**Don't**:

- **Don't Scan Production** without permission/backup. Automated scanners can trigger "Delete All" endpoints or flood databases.
- **Don't Ignore CSRF**: Burp's macros can handle CSRF tokens during automated scans; configure them properly.

## Troubleshooting

| Error                  | Cause                     | Solution                                                             |
| :--------------------- | :------------------------ | :------------------------------------------------------------------- |
| `SSL Handshake Failed` | Burp CA cert not trusted. | Import Burp's CA cert into your browser/OS trust store.              |
| `Infinite Loading`     | Intercept is ON.          | Turn "Intercept" to OFF in the Proxy tab if you just want to browse. |

## References

- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [Burp Suite Documentation](https://portswigger.net/burp/documentation)
