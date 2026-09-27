---
name: httpie
description: Expert HTTPie assistance covering CLI and GUI HTTP client usage, JSON formatting, authentication, sessions, and headers. Use when testing, debugging, and querying RESTful APIs from terminal.
---

# HTTPie

HTTPie started as a CLI (`http get example.com`) and now includes a beautiful **Desktop** app (2025). It is famous for its **human-friendly** syntax.

## When to Use

- **Human-Friendly CLI API Testing**: Intuitive, colorized HTTP client alternative to curl with concise JSON syntax.
- **Session & Authentication Management**: Persisting auth headers, cookies, and tokens across requests using `--session`.
- **Form Data & File Uploads**: Uploading multi-part forms and files with progress bars and MIME type detection.
- **API Prototyping & Scripting**: Testing GraphQL, REST, and streaming SSE endpoints from the terminal.

## Quick Start

```bash
# Intuitive JSON POST request with automatic formatting and colorization
http POST api.example.com/users \
  Authorization:"Bearer $TOKEN" \
  name="Alice" \
  email="alice@example.com" \
  age:=30 \
  active:=true
```

## Core Concepts

#Intuitive JSON Request & Header Syntax

Sending structured JSON payloads without escaping quotes:

```bash
# POST request with JSON body (string vs number vs boolean syntax)
http POST https://api.example.com/v1/orders \
  Authorization:"Bearer $API_TOKEN" \
  customer_id="cust_1029" \
  amount:=149.50 \
  is_gift:=true \
  items:='["item_1", "item_2"]'

# GET request with query parameters (using ==)
http GET https://api.example.com/v1/orders \
  status==active \
  limit==10 \
  sort==desc
```

#Persistent Sessions for Authenticated Workflows

Saving authentication tokens and session cookies:

```bash
# 1. Log in and save session cookies/tokens to 'staging' session
http --session=staging POST https://api.example.com/auth/login \
  username="admin@example.com" \
  password="SecretPassword2026"

# 2. Subsequent requests automatically reuse session state
http --session=staging GET https://api.example.com/dashboard/kpi
```

#Form Submissions & File Uploads

Uploading files with multi-part encoding:

```bash
# Upload document with progress bar
http --form POST https://api.example.com/upload \
  title="Financial Report" \
  document@./annual_report.pdf
```

## Common Patterns

### Session Persistence for Authenticated API Testing

**Problem**: Re-specifying headers, tokens, and cookies across repeated curl requests during debugging.

**Solution**:
Use HTTPie named sessions:

```bash
# Log in and automatically persist session cookies and headers
http --session=admin-session POST api.example.com/login username=admin password=secret

# Subsequent requests automatically use saved authentication state
http --session=admin-session GET api.example.com/dashboard/stats
```

## Best Practices (2026)

- **Do** use `:=` for non-string JSON values (numbers, booleans, arrays) and `=` for string values.
- **Do** use `--session` to avoid repeating authentication headers across sequential CLI requests.
- **Do** use `--print=HhBb` to control which headers and body elements are printed to terminal output.
- **Do** pipe output to `jq` using `--json` flag when combining with shell scripts.
- **Don't** include plain text passwords in shell history; supply via environment variables or prompt.
- **Don't** forget `==` when specifying URL query parameters (single `=` defines request body properties).
- **Don't** use HTTPie in resource-constrained container images if minimal `/bin/sh` with curl suffices.

## Troubleshooting

| Error                                                | Cause                                                          | Solution                                                         |
| :--------------------------------------------------- | :------------------------------------------------------------- | :--------------------------------------------------------------- |
| `http: error: ConnectionError: Connection refused`   | Target local server port down or firewall blocking connection. | Verify local service is listening on targeted port.              |
| `Invalid JSON type: string passed instead of number` | Used `=` instead of `:=` for non-string JSON values.           | Use `:=` for numbers/booleans: `count:=10` (vs `name="string"`). |
| `SSL: CERTIFICATE_VERIFY_FAILED`                     | Local dev server using self-signed SSL certificate.            | Add `--verify=no` flag for development testing.                  |

## References

- [HTTPie Documentation](https://httpie.io/docs)
