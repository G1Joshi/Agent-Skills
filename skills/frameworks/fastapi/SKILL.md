---
name: fastapi
description: Expert FastAPI assistance covering Pydantic models, async endpoints, dependency injection, and OpenAPI generation. Use when developing high-performance Python REST APIs and microservices.
---

# FastAPI

FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python type hints. It is one of the fastest Python frameworks available.

## When to Use

- **High-Performance Python Web APIs**: Developing modern async APIs built on Starlette and Pydantic.
- **AI & Machine Learning Model Serving**: Serving PyTorch, TensorFlow, Scikit-learn, and Hugging Face inference endpoints.
- **Automatic OpenAPI & Swagger Documentation**: Generating interactive documentation with zero manual configuration.
- **Data Validation & Type-Safe Payloads**: Validating query parameters, paths, headers, and request bodies with Pydantic v2.

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

### Async Route Handlers & Pydantic v2 Models

Strict payload parsing and serialization:

```python
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import List

app = FastAPI(title="Catalog API", version="2.0.0")

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0, description="Price in USD")
    tags: List[str] = []

class ProductResponse(ProductCreate):
    id: int
    is_active: bool = True

@app.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    # Process and persist product
    return {
        "id": 101,
        "name": product.name,
        "price": product.price,
        "tags": product.tags,
        "is_active": True
    }
```

### Dependency Injection System with Depends

Reusing database sessions, authentication, and service clients:

```python
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != "secret-internal-key":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return x_api_key

@app.get("/secure-metrics")
async def get_metrics(api_key: str = Depends(verify_api_key)):
    return {"status": "authorized", "system_load": 0.42}
```

### Lifespan Events & Async Resource Management

Initializing ML models, database connection pools, and Redis caches:

```python
from contextlib import asynccontextmanager

class ResourceState:
    db_pool = None

state = ResourceState()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize connections
    print("Connecting to database pool...")
    state.db_pool = "connected_pool_instance"
    yield
    # Shutdown: Clean up connections
    print("Closing database pool...")
    state.db_pool = None

app = FastAPI(lifespan=lifespan)
```

## Common Patterns

### Dependency Injection with Database Session

**Problem**: Replicating database connection creation and teardown across every API route.

**Solution**:
Use `Depends()` with generator context management:

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from . import models, schemas

app = FastAPI()

@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
```

## Best Practices

**Do**:

- Migrate to FastAPI lifespan handlers (`@asynccontextmanager`) instead of deprecated `@app.on_event("startup")`.
- Leverage Pydantic v2 for up to 5x-10x faster schema serialization and parsing.
- Define synchronous `def` (instead of `async def`) for blocking operations so FastAPI executes them in the worker threadpool.
- Structure routes with `APIRouter` to maintain clean domain separation.

**Don't**:

- Perform blocking CPU or I/O calls directly inside `async def` handlers; use `asyncio.to_thread`.
- Return raw database entities; map them through Pydantic `response_model` schemas.
- Hardcode CORS origins to `["*"]` when authentication credentials are allowed.

## Troubleshooting

| Error                                                     | Cause                                                                     | Solution                                                                                     |
| :-------------------------------------------------------- | :------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------- |
| `422 Unprocessable Entity`                                | Inbound request payload failed Pydantic schema validation.                | Inspect response body details to see field validation failures.                              |
| `RuntimeError: Task attached to a different loop`         | Blocking synchronous database driver used in async `async def` route.     | Use `def` instead of `async def` for sync I/O, or switch to async driver (asyncpg/aiomysql). |
| `AttributeError: 'NoneType' object has no attribute 'id'` | Query returned None and code attempted to access attribute without check. | Guard with `if not item: raise HTTPException(404)`.                                          |

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
