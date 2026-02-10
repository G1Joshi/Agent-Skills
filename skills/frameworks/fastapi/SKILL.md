---
name: fastapi
description: FastAPI Python async framework with Pydantic and automatic OpenAPI. Use for Python APIs.
---

# FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints. It is one of the fastest Python frameworks available.

## When to Use

- **APIs**: The default choice for modern Python APIs.
- **Machine Learning**: Native integration with Pydantic makes JSON <-> Model interaction seamless.
- **Performance**: Built on Starlette and Pydantic v2, it rivals Node.js and Go in benchmarks.

## Quick Start

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item):
    return {"name": item.name, "price": item.price}
```

## Core Concepts

### Pydantic Models

Define data shape using Python classes. Validation and JSON serialization happen automatically.

### Dependency Injection

FastAPI has a powerful DI system.
`async def read_users(db: Session = Depends(get_db)):`.

### OpenAPI (Swagger)

Automatically generates interactive API documentation at `/docs`.

## Best Practices (2025)

**Do**:

- **Use Pydantic v2**: Ensure you are on v2 for the massive Rust-based performance boost.
- **Use `lifespan`**: Use the new `lifespan` context manager for startup/shutdown events instead of deprecated `on_event`.
- **Type Everything**: The more you type, the better the auto-generated docs and validation.

**Don't**:

- **Don't block the loop**: Run CPU bound code (image processing, heavy math) in `def` endpoints (threadpool), not `async def` (event loop), or use background tasks.

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
