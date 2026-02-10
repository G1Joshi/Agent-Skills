---
name: pytest
description: pytest Python testing framework with fixtures. Use for Python testing.
---

# Pytest

Pytest is the dominant testing framework for Python. It is loved for its no-boilerplate syntax (`assert x == y`), powerful fixture system, and rich plugin ecosystem.

## When to Use

- **Python Projects**: The standard for 99% of new Python projects.
- **Complex Setup**: Use Fixtures to handle database connections, API clients, or mock data.
- **Parametrization**: Running the same test with different inputs.

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

### Fixtures

Functions that run before tests to set up state. They are injected via argument name matching.

```python
import pytest

@pytest.fixture
def database():
    db = connect_db()
    yield db
    db.close()

def test_insert(database):
    database.insert("user")
    assert database.count() == 1
```

### Parametrization

Decorating a test to run multiple times.

```python
@pytest.mark.parametrize("input,expected", [
    ("3+5", 8),
    ("2+4", 6),
])
def test_eval(input, expected):
    assert eval(input) == expected
```

## Best Practices (2025)

**Do**:

- **Use `conftest.py`**: Place shared fixtures here. Pytest discovers them automatically.
- **Use `pytest-cov`**: For coverage reports (`pytest --cov=src`).
- **Use Markers**: Tag slow tests (`@pytest.mark.slow`) and exclude them during dev (`pytest -m "not slow"`).

**Don't**:

- **Don't use `unittest.TestCase`**: Unless migrating legacy code. Functional tests are cleaner.
- **Don't use global state**: Fixtures should return fresh instances.

## References

- [Pytest Documentation](https://docs.pytest.org/)
