---
name: postman
description: Expert Postman assistance covering API collection design, pre-request scripts, Newman CI/CD test automation, mock servers, and environment variable management. Use when creating automated API test suites, running collections via Newman CLI, managing environment secrets, or generating API documentation.
---

# Postman

Postman is the complete API lifecycle platform. 2025 features **AI Agent Builder** (orchestrating multi-step workflows) and **Postbot** (AI driven testing).

## When to Use

- **REST, GraphQL, & gRPC API Testing**: Designing requests, inspecting headers, and verifying streaming payloads.
- **Automated CI/CD API Regression Suites**: Running Postman Collections in automated pipelines using the Newman CLI.
- **Dynamic Authentication Handling**: Scripting OAuth 2.0 token refreshes, HMAC signatures, and AWS SigV4 in Pre-request scripts.
- **Mock Servers & API Documentation**: Creating instant mock endpoints and publishing interactive team API documentation.

## Quick Start

### 1. Test Script in Postman

```javascript
// Tests tab in Postman Request
pm.test("Status code is 200 OK", function () {
  pm.response.to.have.status(200);
});

pm.test("Response time is under 400ms", function () {
  pm.expect(pm.response.responseTime).to.be.below(400);
});

pm.test("Token returned and set in environment", function () {
  const jsonData = pm.response.json();
  pm.expect(jsonData.access_token).to.be.a("string");
  pm.environment.set("AUTH_TOKEN", jsonData.access_token);
});
```

### 2. Run via Newman CLI

```bash
npm install -g newman
newman run collection.json -e environment.json --reporters cli,junit
```

## Core Concepts

### Pre-Request Script: Automated JWT / HMAC Signature

Generating dynamic cryptographic signatures and injecting timestamps before request execution:

```javascript
// Pre-request Script (PM API)
const timestamp = Math.floor(Date.now() / 1000).toString();
const apiKey = pm.environment.get("API_KEY");
const apiSecret = pm.environment.get("API_SECRET");
const requestBody = pm.request.body.raw || "";

// Generate SHA256 HMAC
const message = `${pm.request.method}\n${pm.request.url.getPath()}\n${timestamp}\n${requestBody}`;
const signature = CryptoJS.HmacSHA256(message, apiSecret).toString(
  CryptoJS.enc.Hex,
);

pm.request.headers.add({ key: "X-Auth-Key", value: apiKey });
pm.request.headers.add({ key: "X-Auth-Timestamp", value: timestamp });
pm.request.headers.add({ key: "X-Auth-Signature", value: signature });
```

### Automated Response Assertions & Variable Extraction

Validating HTTP response code, schema, and saving output for downstream requests:

```javascript
// Tests Script
pm.test("Status code is 200 OK", function () {
  pm.response.to.have.status(200);
});

pm.test("Response contains valid user session", function () {
  const json = pm.response.json();
  pm.expect(json).to.have.property("access_token");
  pm.expect(json.expires_in).to.be.above(0);

  // Propagate access token to active environment
  pm.environment.set("AUTH_TOKEN", json.access_token);
});

pm.test("Response time is under 300ms", function () {
  pm.expect(pm.response.responseTime).to.be.below(300);
});
```

### Newman CLI Execution in CI/CD Pipeline

Executing collection tests headlessly and generating JUnit reports:

```bash
# Run Postman collection with environment and HTML/JUnit reports
npx newman run ./collections/auth-api-tests.json \
  -e ./environments/staging.postman_environment.json \
  --reporters cli,junit \
  --reporter-junit-export ./reports/newman-results.xml \
  --bail \
  --env-var "BASE_URL=https://staging-api.example.com"
```

## Common Patterns

### Pre-Request HMAC Signature Generation

**Problem**: API requests require timestamp and SHA-256 HMAC signature headers calculated per request.  
**Solution**: Generate headers dynamically in the **Pre-request Script** tab.

```javascript
const secret = pm.environment.get("API_SECRET");
const timestamp = Math.floor(Date.now() / 1000).toString();
const payload = pm.request.body.raw || "";

const message = `${timestamp}.${pm.request.method}.${payload}`;
const signature = CryptoJS.HmacSHA256(message, secret).toString();

pm.request.headers.add({ key: "X-Timestamp", value: timestamp });
pm.request.headers.add({ key: "X-Signature", value: signature });
```

### Chained API Testing (Login -> Create -> Delete)

**Problem**: Execute multi-step end-to-end user workflows using dynamically extracted identifiers.  
**Solution**: Set variables in `pm.collectionVariables` and trigger conditional next requests via `postman.setNextRequest()`.

```javascript
// Step 1: Capture created resource ID
const res = pm.response.json();
pm.collectionVariables.set("ITEM_ID", res.id);

// Conditionally skip to cleanup on error
if (pm.response.code !== 201) {
  postman.setNextRequest("Cleanup Endpoint");
}
```

## Best Practices (2026)

- **Do** parameterize environment URLs, tenant IDs, and credentials using `{{base_url}}` variables.
- **Do** store sensitive credentials in Environment variables with type **Secret** to mask values from UI and exports.
- **Do** run collections via Newman in CI/CD workflows to prevent regressions before deployment.
- **Do** organize collections by domain resource with clear folder-level authorization inheritance.
- **Don't** hardcode raw JWT tokens or passwords directly in request headers or body payloads.
- **Don't** commit environment files containing active production API keys to public repositories.
- **Don't** duplicate authentication headers manually; configure Auth at the Collection level.

## Troubleshooting

| Error / Symptom                                           | Cause                                                              | Solution                                                                                                         |
| --------------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `SSL Error: Self-signed certificate in certificate chain` | Target endpoint uses local dev or untrusted SSL certificate        | Turn off **SSL certificate verification** in Postman Settings > General, or pass `--insecure` to Newman.         |
| Variable not substituting (`{{API_URL}}` remains literal) | Active environment not selected in dropdown or variable misspelled | Ensure environment dropdown in top-right is selected and scope matches (`environment` vs `collectionVariables`). |
| Newman exit code failure in CI pipeline                   | Assertion failed in collection run                                 | Check test summary output; run Newman with `--bail` to stop on first failure or inspect JUnit XML report.        |

## References

- [Postman Documentation](https://learning.postman.com/docs/introduction/overview/)
