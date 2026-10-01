---
name: python
description: Expert modern Python (3.11+) assistance covering type annotations, async/await, generators, dataclasses, context managers, and virtual environment tooling. Use when writing idiomatic Python, building web backends, structuring data science pipelines, or optimizing Python performance.
---

# Python

Modern Python development with type hints, async/await, and best practices.

## When to Use

- **Artificial Intelligence, Machine Learning & LLMs**: Developing AI models with PyTorch, TensorFlow, Hugging Face, LangChain, and vLLM.
- **High-Performance Web APIs (FastAPI / Django)**: Building async web backends, microservices, and enterprise applications.
- **Data Engineering & Analytics**: Processing data pipelines using Pandas, Polars, PySpark, and DuckDB.
- **Automation, Scripting & DevOps**: Writing robust infrastructure automation, system utilities, and CLI tools.

## Quick Start

```python
from typing import Optional, List

def process_items(
    items: list[str],
    transform: Optional[callable] = None,
) -> list[str]:
    if transform:
        return [transform(item) for item in items]
    return items
```

## Core Concepts

### Strict Type Hints & Runtime Validation (Pydantic / Mypy)

Modern Python (3.11/3.12+) features comprehensive type annotations and structural models:

```python
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field

class UserProfile(BaseModel):
    id: str
    email: EmailStr
    age: Annotated[int, Field(ge=18, le=120)]
    roles: list[str] = ["member"]

# Automatic validation and serialization
user = UserProfile(id="usr_415", email="alice@example.com", age=28)
print(user.model_dump_json())
```

### Asynchronous Event Loop & Asyncio Task Groups

Concurrent asynchronous I/O with modern exception handling:

```python
import asyncio
import httpx

async def fetch_metric(client: httpx.AsyncClient, metric_id: int) -> dict:
    resp = await client.get(f"https://api.example.com/metrics/{metric_id}")
    return resp.json()

async def main():
    async with httpx.AsyncClient() as client:
        # Python 3.11+ TaskGroup manages structured concurrency cleanly
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(fetch_metric(client, 1))
            task2 = tg.create_task(fetch_metric(client, 2))

    print("Results:", task1.result(), task2.result())

asyncio.run(main())
```

### Modern Dependency Management with `uv` / `poetry`

Replaces slow legacy pip and virtualenv workflows with lightning-fast Rust-based tooling:

```bash
# Instant package installation and lockfile management via uv
uv venv
uv pip install -r requirements.txt
```

## Common Patterns

### Structured Concurrency with Asyncio TaskGroups

**Problem**: Concurrent asynchronous operations risking dangling unhandled tasks or memory leaks on exceptions.

**Solution**:

```python
import asyncio

async def fetch_all(urls: list[str]) -> list[Response]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Use TaskGroup for structured concurrency (3.11+)
async def process_batch(items: list[Item]) -> list[Result]:
    results = []
    async with asyncio.TaskGroup() as tg:
        for item in items:
            tg.create_task(process_item(item, results))
    return results
```

### Context Managers

**Problem**: Safely managing acquisition and release of external resources (locks, files, sockets) in the face of unhandled exceptions.

**Solution**:

```python
from contextlib import contextmanager, asynccontextmanager

@contextmanager
def managed_resource() -> Iterator[Resource]:
    resource = Resource()
    try:
        yield resource
    finally:
        resource.cleanup()
```

## Best Practices

**Do**:

- Adopt `uv` for Package Management: Use `uv` (10-100x faster than pip) for virtual environments and dependency resolution.
- Lint and Format with Ruff: Replace Flake8, Black, and isort with the blazing-fast Rust-based `ruff` linter/formatter.
- Enforce Strict Static Typing with Mypy or Pyright: Catch type errors and missing attributes in CI before production.
- Use Context Managers for Resources: Always manage files, sockets, and locks using `with` and `async with` statements.

**Don't**:

- Use mutable default arguments in functions: Avoid `def append_to(item, target=[])`; use `target: list | None = None`.
- Catch generic `except Exception:` blindly: Catch specific exception classes to avoid masking unexpected programming errors.
- Install global packages directly: Always isolate project dependencies in dedicated virtual environments (`.venv`).

## Troubleshooting

| Error                        | Cause                  | Solution                           |
| ---------------------------- | ---------------------- | ---------------------------------- |
| `ModuleNotFoundError`        | Package not installed  | Run `pip install package`          |
| `IndentationError`           | Mixed tabs/spaces      | Use consistent 4-space indentation |
| `TypeError: unhashable type` | Using list as dict key | Use tuple instead                  |

## References

- [Python Official Docs](https://docs.python.org/3/)
- [Real Python](https://realpython.com/)
