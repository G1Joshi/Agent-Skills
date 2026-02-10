---
name: flask
description: Flask Python microframework with blueprints and extensions. Use for lightweight APIs.
---

# Flask

Flask is a lightweight WSGI web application framework. It is designed to make getting started quick and easy, with the ability to scale up to complex applications. Flask 3.0 (2025) fully supports async routes.

## When to Use

- **Microservices**: Minimal boilerplate makes it great for small services.
- **Flexibility**: You validly choose your ORM (SQLAlchemy, Peewee) and Auth provider.
- **Data Science APIs**: The standard for wrapping ML models (PyTorch/TensorFlow) in an API.

## Quick Start (Async)

```python
from flask import Flask
import asyncio

app = Flask(__name__)

@app.route("/")
async def hello():
    await asyncio.sleep(1)
    return "Hello form Async Flask!"
```

## Core Concepts

### The Application Context

Flask uses thread-locals (or context-vars in async) to make `request` and `g` globally accessible during a request.

### Blueprints

Organize a group of related views and other code. `auth_bp = Blueprint('auth', __name__)`.

## Best Practices (2025)

**Do**:

- **Use `Quart` or Flask 3.0+**: Ensure you are using modern async features if your app is I/O bound.
- **Use `pydantic`**: Use Pydantic for request validation (via libraries like `flask-pydantic` or just raw).
- **Application Factory Pattern**: Always use `create_app()` to ensure your app is testable.

**Don't**:

- **Don't use global state**: Use `current_app` or `g` to store request-scoped data.

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
