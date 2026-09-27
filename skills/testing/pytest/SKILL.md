---
name: pytest
description: Expert Pytest testing assistance covering fixtures, parametrization, marks, and test plugins. Use when writing Python tests, building test suites, or running `pytest` in CI/CD pipelines.
---

# Pytest

Pytest is the dominant testing framework for Python. It is loved for its no-boilerplate syntax (`assert x == y`), powerful fixture system, and rich plugin ecosystem.

## When to Use

- **Python Standard Testing Framework**: The most widely adopted, powerful testing framework for Python web backends, data science, and ML.
- **Clean Fixture Dependency Injection**: Managing test setup, database connections, and teardown cleanly with `@pytest.fixture`.
- **Parameterized Testing**: Running test functions across multi-dimensional input sets with `@pytest.mark.parametrize`.
- **Rich Plugin Ecosystem**: Extending capabilities via `pytest-asyncio`, `pytest-cov`, `pytest-xdist`, and `pytest-mock`.

## Quick Start

```python
# content of test_sample.py
def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 5
```

Running it:

```bash
pytest
```

## Core Concepts

#Dependency Injection with Fixtures

Fixtures provide modular, reusable dependencies with explicit lifecycle scopes:

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("sqlite:///:memory:")
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
```

#Parameterized Tests (`@pytest.mark.parametrize`)

Tests multiple input/output scenarios cleanly without loop boilerplate:

```python
import pytest

@pytest.mark.parametrize("email,expected_valid", [
    ("user@example.com", True),
    ("invalid-email", False),
    ("@missinguser.com", False),
    ("user.name+tag@sub.domain.co", True),
])
def test_email_validation(email, expected_valid):
    assert validate_email(email) == expected_valid
```

#Async Testing with `pytest-asyncio`

Tests async coroutines seamlessly:

```python
import pytest
import httpx

@pytest.mark.asyncio
async def test_async_fetch():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://httpbin.org/get")
        assert response.status_code == 200
```

## Common Patterns

### Scoped Fixtures with Teardown / Cleanup

**Problem**: Database or mock setup code repeated across dozens of test functions creates duplication and leftover state.

**Solution**:
Use `@pytest.fixture` with the `yield` statement:

```python
import pytest

@pytest.fixture(scope="function")
def db_session():
    # Setup test database session
    session = create_test_session()
    yield session
    # Cleanup and rollback after test completes
    session.rollback()
    session.close()

def test_user_creation(db_session):
    user = db_session.create_user("alice@example.com")
    assert user.id is not None
```

## Best Practices (2026)

**Do**:

- **Use Plain `assert` Statements**: Pytest provides detailed assertion introspection without requiring special assertion methods.
- **Use `conftest.py` for Shared Fixtures**: Place global fixtures and configuration hooks in `conftest.py` files.
- **Run Parallel Tests with `pytest-xdist`**: Accelerate test runs across all CPU cores with `pytest -n auto`.
- **Mark Tests by Category**: Use custom marks (`@pytest.mark.slow`, `@pytest.mark.integration`) and filter runs with `-m "not slow"`.

**Don't**:

- **Don't use `assert` with parentheses**: Writing `assert(a == b, "msg")` evaluates a non-empty tuple which is always truthy.
- **Don't mutate shared session-scoped fixtures**: Keep session fixtures read-only; use function-scoped fixtures for test-isolated mutations.
- **Don't create deep nested class hierarchies**: Pytest favors simple standalone test functions over unittest-style classes.

## Troubleshooting

| Error                                        | Cause                                                                   | Solution                                                                                             |
| :------------------------------------------- | :---------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'src'` | Current directory not in `sys.path` when running pytest.                | Run pytest as a module: `python -m pytest`, or configure `pythonpath = ["src"]` in `pyproject.toml`. |
| `FixtureNotFound: fixture '...' not found`   | Typo in fixture argument name or fixture defined outside `conftest.py`. | Move shared fixtures to root `conftest.py` file.                                                     |
| `Failed: DID NOT RAISE <class '...'>`        | Code did not raise the exception expected by `pytest.raises`.           | Inspect inputs to verify failure condition is actually triggered.                                    |

## References

- [Pytest Documentation](https://docs.pytest.org/)
