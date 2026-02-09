---
name: pytest
description: Pytest testing framework with fixtures and parametrization. Use for Python tests.
---

# Pytest

Python testing framework with powerful fixtures.

## When to Use

- Python unit testing
- Integration testing
- Fixture-based setup
- Parametrized tests

## Quick Start

```python
# test_math.py
import pytest
from math_utils import add

def test_add():
    assert add(1, 2) == 3

def test_add_negative():
    assert add(-1, 1) == 0
```

## Core Concepts

### Fixtures

```python
import pytest
from database import Database

@pytest.fixture
def db():
    """Create database connection."""
    database = Database()
    database.connect()
    yield database
    database.disconnect()

@pytest.fixture
def sample_user(db):
    """Create test user."""
    user = db.create_user(name="Test User")
    yield user
    db.delete_user(user.id)

def test_user_name(sample_user):
    assert sample_user.name == "Test User"
```

### Parametrization

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
    (-1, -2),
])
def test_double(input, expected):
    assert double(input) == expected

@pytest.mark.parametrize("a,b,result", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, -1, -2),
])
def test_add(a, b, result):
    assert add(a, b) == result
```

## Common Patterns

### Mocking

```python
from unittest.mock import Mock, patch

def test_with_mock():
    mock_api = Mock()
    mock_api.get_user.return_value = {"id": 1, "name": "John"}

    result = service.fetch_user(mock_api, 1)

    assert result["name"] == "John"
    mock_api.get_user.assert_called_once_with(1)

@patch('module.external_api')
def test_with_patch(mock_api):
    mock_api.return_value = {"data": "test"}
    result = function_under_test()
    assert result == {"data": "test"}
```

### Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch_data()
    assert result is not None

# With pytest-asyncio
@pytest.fixture
async def async_client():
    async with AsyncClient() as client:
        yield client

@pytest.mark.asyncio
async def test_api(async_client):
    response = await async_client.get("/api/users")
    assert response.status_code == 200
```

## Best Practices

**Do**:

- Use fixtures for setup/teardown
- Parametrize similar tests
- Use `conftest.py` for shared fixtures
- Mark slow tests with `@pytest.mark.slow`

**Don't**:

- Share state between tests
- Use unittest-style classes
- Skip cleanup in fixtures
- Hardcode test data

## Troubleshooting

| Issue              | Cause        | Solution          |
| ------------------ | ------------ | ----------------- |
| Fixture not found  | Wrong scope  | Check conftest.py |
| Test not collected | Wrong naming | Use test\_ prefix |
| Import error       | Wrong path   | Check PYTHONPATH  |

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
