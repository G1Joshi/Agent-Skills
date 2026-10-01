---
name: burpsuite
description: Expert Burp Suite web penetration testing covering proxy interception, repeater, intruder fuzzing, and scan automation. Use when auditing web vulnerabilities, inspecting HTTP traffic, or testing web security.
---

# Burp Suite

Burp Suite is an integrated platform for performing security testing of web applications. It ranges from mapping and analyzing an application's attack surface to finding and exploiting vulnerabilities.

## When to Use

- **Web Application Penetration Testing**: Auditing web applications for OWASP Top 10 vulnerabilities (SQLi, XSS, SSRF, IDOR).
- **HTTP Traffic Interception & Modification**: Inspecting and tampering with web and mobile app API requests in real time.
- **Automated Vulnerability Scanning**: Running active and passive scans using Burp Scanner against staging environments.
- **Custom Security Automation**: Writing custom security extensions via the Montoya API or Python/Java extensions.

## Quick Start

```bash
# Configure local browser to forward traffic through Burp Proxy
# Default proxy listener: 127.0.0.1:8080

# 1. Start Burp Suite and verify Proxy Listener is active on 8080
# 2. Export Burp CA Certificate from http://burp and install into OS trust store
# 3. Launch target browser with custom proxy:
chromium --proxy-server="http://127.0.0.1:8080" --ignore-certificate-errors
```

## Core Concepts

### Intercepting Proxy Architecture

Burp Suite positions itself as a man-in-the-middle (MitM) HTTP/HTTPS proxy between client browsers and backend targets:

```text
[ Browser / Mobile Device ] ──(Proxy: 127.0.0.1:8080)──→ [ Burp Proxy (Intercept ON/OFF) ] ──→ [ Target API Server ]
```

### Burp Repeater & Manual Request Crafting

Allows isolating individual requests and replaying modified payloads to analyze server responses:

```http
POST /api/v1/user/update-email HTTP/1.1
Host: staging.example.com
Authorization: Bearer <test_token>
Content-Type: application/json

{"email": "attacker@exploit.com", "user_id": 415}
```

### Burp Intruder Parameter Fuzzing

Automates payload injection across specified positions to discover injection flaws and hidden endpoints:

```http
GET /api/v1/documents/§doc_id§ HTTP/1.1
Host: staging.example.com
Cookie: session=§session_token§
```

## Common Patterns

### Automated Request Fuzzing with Match/Replace

**Problem**: Testing parameter tampering across repetitive API flows manually is slow and prone to oversights.

**Solution**:
Configure Proxy Match & Replace rules or Intruder sniper attacks to test injection payloads across designated parameters:

```http
POST /api/v1/checkout HTTP/1.1
Host: target.example.com
Authorization: Bearer §TOKEN§
Content-Type: application/json

{"coupon": "§PROMO§", "quantity": 1}
```

## Best Practices

**Do**:

- Install Burp CA Certificate Safely: Trust the PortSwigger CA certificate only in dedicated testing browser profiles, never system-wide.
- Scope Target URLs Strictly: Add target hostnames to **Target > Scope** and toggle "Show only in-scope items" to prevent scanning out-of-scope third parties.
- Rate-Limit Automated Intruder Attacks: Throttle requests per second to avoid triggering WAF blocks or taking down staging databases.
- Leverage Burp Match and Replace: Automatically replace authorization headers or user agents across all proxied traffic.

**Don't**:

- Run active scans against production environments without authorization: Automated scanning can trigger destructive mutations or account lockouts.
- Leave Burp proxy listening on public interfaces (`0.0.0.0`): Bind proxy listeners strictly to `127.0.0.1` to prevent unauthorized proxy relay.
- Ignore Burp Logger / Event Log: Monitor the event log to identify upstream connection timeouts and SSL negotiation failures.

## Troubleshooting

| Error                  | Cause                     | Solution                                                             |
| :--------------------- | :------------------------ | :------------------------------------------------------------------- |
| `SSL Handshake Failed` | Burp CA cert not trusted. | Import Burp's CA cert into your browser/OS trust store.              |
| `Infinite Loading`     | Intercept is ON.          | Turn "Intercept" to OFF in the Proxy tab if you just want to browse. |

## References

- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [Burp Suite Documentation](https://portswigger.net/burp/documentation)
