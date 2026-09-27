---
name: locust
description: Expert Locust load testing assistance covering Python user classes, task sets, and distributed testing. Use when writing Python performance tests, simulating user behaviors, or running web stress tests.
---

# Locust

Locust is an easy-to-use, scriptable, and scalable performance testing tool. You define the behavior of your users in regular Python code.

## When to Use

- **Python-Based Load & Performance Testing**: Authoring complex, dynamic load test scenarios using standard Python code.
- **Distributed Master/Worker Scaling**: Scaling load generation across dozens of distributed worker machines easily.
- **Real-Time Web Dashboard Monitoring**: Inspecting request per second, response latency charts, and failures live in the Locust browser UI.
- **Custom Protocol Testing**: Load testing gRPC, WebSockets, or proprietary TCP protocols alongside standard HTTP.

## Quick Start

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get("/")

    @task(3)
    def view_item(self):
        item_id = randint(1, 10000)
        self.client.get(f"/item?id={item_id}", name="/item")
```

Run `locust -f locustfile.py`.

## Core Concepts

#User Classes & Task Hierarchy

Defines virtual user behaviors using Python methods annotated with `@task`:

```python
# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3) # Wait 1-3 seconds between tasks

    def on_start(self):
        # Executed when virtual user spawns (e.g. login)
        res = self.client.post("/api/login", json={"user": "test", "pass": "secret"})
        self.token = res.json().get("token")
        self.client.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3) # Weight 3: executed 3x more often
    def view_catalog(self):
        self.client.get("/api/catalog")

    @task(1) # Weight 1
    def place_order(self):
        self.client.post("/api/checkout", json={"itemId": 42})
```

#Headless CI/CD Execution with Thresholds

Runs headlessly in build pipelines, exiting with non-zero status codes if criteria fail:

```bash
locust --headless \
  -u 200 -r 20 -t 5m \
  --host https://staging.example.com \
  --csv=results \
  --exit-code-on-error 1
```

#Distributed Master / Worker Architecture

Coordinates load across multiple machines:

```bash
# Start Master node
locust --master

# Start Worker nodes (across cluster)
locust --worker --master-host=10.0.1.5
```

## Common Patterns

### Weighted Task Set with User Session Management

**Problem**: Real users perform actions with variable frequencies and stateful session contexts.

**Solution**:
Use `@task(weight)` with `HttpUser`:

```python
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task(5)
    def browse_catalog(self):
        self.client.get("/products")

    @task(1)
    def checkout_cart(self):
        self.client.post("/cart/checkout", json={"items": [1, 2]})
```

## Best Practices (2026)

**Do**:

- **Use Weights on `@task(weight)`**: Reflect realistic user activity ratios (e.g. 10 browsing actions for every 1 checkout action).
- **Run Headless in CI/CD**: Use `--headless` mode to automate performance checks in GitHub Actions or GitLab CI.
- **Group Dynamic URLs with `name` Parameters**: Group `/users/1` and `/users/2` under a single endpoint name: `self.client.get("/users/1", name="/users/[id]")`.
- **Use `FastHttpUser` for High Concurrency**: Inherit from `FastHttpUser` (geventhttpclient) for 5-6x higher throughput per worker CPU.

**Don't**:

- **Don't perform heavy computational blocking in tasks**: Keep task code lean to prevent starving the gevent cooperative thread loop.
- **Don't run single-process tests for heavy loads**: Spawn multiple worker processes (`--processes 4`) to leverage multi-core CPUs.
- **Don't forget SSL verification options**: Pass `verify=False` only in isolated dev environments; never bypass security in prod.

## Troubleshooting

| Error                                           | Cause                                                         | Solution                                                               |
| :---------------------------------------------- | :------------------------------------------------------------ | :--------------------------------------------------------------------- |
| `ConnectionRefusedError / Max retries exceeded` | Target server port closed or refused incoming connections.    | Ensure target application is running and accessible on specified host. |
| `Too many open files (OSError)`                 | OS file descriptor limit exceeded on Locust worker.           | Increase file limit using `ulimit -n 65536`.                           |
| `CatchResponseError: status 500`                | Target server throwing internal server exceptions under load. | Check application error logs and stack traces on target server.        |

## References

- [Locust Documentation](https://locust.io/)
