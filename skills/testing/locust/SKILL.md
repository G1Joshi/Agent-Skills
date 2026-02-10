---
name: locust
description: Locust load testing in Python. Use for load testing.
---

# Locust

Locust is an easy-to-use, scriptable, and scalable performance testing tool. You define the behavior of your users in regular Python code.

## When to Use

- **Python Teams**: Scripting complexity is zero if you know Python.
- **Distributed Testing**: Easy to scale out using a Master/Worker architecture to simulate millions of users.
- **Web UI**: Comes with a nice web interface to start tests and view graphs in real-time.

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

### User Class

Represents a user. Attributes like `wait_time` simulate "think time" between actions.

### Tasks

Decorator `@task` marks methods as user actions. You can weight them (`@task(3)` runs 3x more often than `@task(1)`).

### Web UI

Accessible at `http://localhost:8089`. Allows you to set the user count and spawn rate dynamically.

## Best Practices (2025)

**Do**:

- **Use `FastHttpUser`**: Locust's standard `HttpUser` uses `requests` (slow). `FastHttpUser` uses `geventhttpclient` which is much faster for load generation.
- **Group Requests**: Use the `name` argument in `client.get(url, name="my-endpoint")`. Otherwise, every unique URL (with differing IDs) shows as a separate entry in reports.

**Don't**:

- **Don't block the Greenlet**: Locust uses Gevent. Do not perform CPU-intensive work or blocking IO (standard `time.sleep`) in your tasks, or you pause the whole user runner.

## References

- [Locust Documentation](https://locust.io/)
