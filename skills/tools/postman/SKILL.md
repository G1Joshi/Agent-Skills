---
name: postman
description: Postman API testing with collections, environments, and automation. Use for API development.
---

# Postman

API development and testing platform.

## When to Use

- Testing REST APIs
- API documentation
- Automated testing
- Team API collaboration

## Quick Start

```javascript
// GET request with params
// URL: {{baseUrl}}/users?status=active

// POST request body (JSON)
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

## Core Concepts

### Environment Variables

```javascript
// Environments: Development, Staging, Production

// Variables
{
  {
    baseUrl;
  }
} // https://api.example.com
{
  {
    apiKey;
  }
} // your-api-key
{
  {
    userId;
  }
} // 123

// Pre-request Script
pm.environment.set("timestamp", Date.now());
```

### Tests & Assertions

```javascript
// Response status
pm.test("Status is 200", () => {
  pm.response.to.have.status(200);
});

// Response JSON
pm.test("User has correct email", () => {
  const json = pm.response.json();
  pm.expect(json.email).to.equal("test@example.com");
});

// Response time
pm.test("Response time < 500ms", () => {
  pm.expect(pm.response.responseTime).to.be.below(500);
});

// Save data for next request
const token = pm.response.json().token;
pm.environment.set("authToken", token);
```

## Common Patterns

### Authentication

```javascript
// Pre-request Script for OAuth
const tokenUrl = pm.environment.get("tokenUrl");
const clientId = pm.environment.get("clientId");
const clientSecret = pm.environment.get("clientSecret");

pm.sendRequest(
  {
    url: tokenUrl,
    method: "POST",
    header: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: {
      mode: "urlencoded",
      urlencoded: [
        { key: "grant_type", value: "client_credentials" },
        { key: "client_id", value: clientId },
        { key: "client_secret", value: clientSecret },
      ],
    },
  },
  (err, res) => {
    pm.environment.set("accessToken", res.json().access_token);
  },
);
```

### Collection Runner

```javascript
// Run collection with Newman (CLI)
npx newman run collection.json \
  -e environment.json \
  --reporters cli,htmlextra \
  --iteration-count 5
```

## Best Practices

**Do**:

- Use environments for different stages
- Write tests for critical responses
- Version control collections
- Use collection variables

**Don't**:

- Hardcode secrets
- Skip response validation
- Create duplicate requests
- Ignore collection organization

## Troubleshooting

| Issue                 | Cause               | Solution                            |
| --------------------- | ------------------- | ----------------------------------- |
| Variable not resolved | Wrong scope         | Check environment selection         |
| SSL error             | Certificate issue   | Disable SSL verification (dev only) |
| CORS error            | Browser restriction | Use Postman desktop app             |

## References

- [Postman Documentation](https://learning.postman.com/)
- [Newman CLI](https://www.npmjs.com/package/newman)
