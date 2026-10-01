---
name: flask
description: Expert Flask assistance covering Blueprints, application factories, Jinja2 templating, and SQLAlchemy extensions. Use when developing lightweight Python web services and applications.
---

# Flask

Flask is a lightweight WSGI web framework for Python, offering modular blueprints, extensible request handling, and flexible integration with database ORMs and async handlers.

## When to Use

- **Lightweight Python Microservices**: Rapidly prototyping APIs and small-to-medium web services without boilerplate.
- **Machine Learning Inference Wrappers**: Wrapping data science pipelines and Scikit-learn/XGBoost models with minimal overhead.
- **Custom Architectures**: Projects requiring complete freedom to select ORMs, auth libraries, and database drivers.
- **Internal Scripting & Admin Utilities**: Embedding web dashboards inside automated Python operations tooling.

## Quick Start

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

### Application Factory & Blueprint Pattern

Structuring scalable Flask applications:

```python
# app/__init__.py
from flask import Flask
from .routes.users import user_bp
from .routes.orders import order_bp

def create_app(config_object="app.config.ProductionConfig"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Register modular blueprints
    app.register_blueprint(user_bp, url_prefix="/api/v1/users")
    app.register_blueprint(order_bp, url_prefix="/api/v1/orders")

    return app
```

### Type-Safe Request Handling & JSON Responses

Parsing payloads and handling route parameters:

```python
# app/routes/users.py
from flask import Blueprint, request, jsonify, abort

user_bp = Blueprint("users", __name__)

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if user_id <= 0:
        abort(404, description="User not found")
    return jsonify({
        "id": user_id,
        "name": f"User_{user_id}",
        "status": "active"
    }), 200

@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "email" not in data:
        return jsonify({"error": "Email is required"}), 400

    return jsonify({"id": 42, "email": data["email"]}), 201
```

### Centralized Error Handling & RFC 7807

Formatting consistent API exceptions:

```python
from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify({
            "error": "Not Found",
            "message": str(e.description),
            "status": 404
        }), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status": 500
        }), 500
```

## Common Patterns

### Modular Application Factory with Blueprints

**Problem**: Monolithic `app.py` script becoming unmaintainable as routes and extensions grow.

**Solution**:
Use Flask Application Factory pattern:

```python
# app/__init__.py
from flask import Flask
from .extensions import db
from .routes.api import api_bp

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")

    db.init_app(app)
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app
```

## Best Practices

**Do**:

- Always structure applications using the Application Factory pattern (`create_app()`) and Blueprints.
- Run Flask applications behind a production WSGI/ASGI server like Gunicorn or Uvicorn with Gevent workers.
- Use environment variables for `SECRET_KEY` and database credentials (`python-dotenv`).
- Use extensions like `Flask-SQLAlchemy` and `Flask-Migrate` for relational data management.

**Don't**:

- Use the built-in development server (`flask run`) in production environments.
- Commit default secret keys to version control; use cryptographically random secrets.
- Use global state variables to store request-specific user data; use Flask's `g` context object.

## Troubleshooting

| Error                                      | Cause                                                          | Solution                                                                 |
| :----------------------------------------- | :------------------------------------------------------------- | :----------------------------------------------------------------------- |
| `Working outside of application context`   | Accessing database or current_app outside request/app context. | Wrap code with `with app.app_context():`.                                |
| `RuntimeError: The session is unavailable` | `app.secret_key` not configured.                               | Set `app.secret_key = "strong-random-key"` in config.                    |
| `Method Not Allowed (405)`                 | Route does not explicitly permit request method.               | Add method to decorator: `@app.route('/path', methods=['GET', 'POST'])`. |

## References

- [Flask Documentation](https://flask.palletsprojects.com/)
