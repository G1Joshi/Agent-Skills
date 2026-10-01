---
name: pycharm
description: Expert PyCharm assistance covering Python interpreters, virtualenv/Poetry/Conda management, scientific notebooks, remote debugging, and database integrations. Use when configuring PyCharm interpreters, setting up pytest test configurations, tuning IDE performance, or debugging Python applications.
---

# PyCharm

PyCharm is the best IDE for serious Python development. It excels in **Django** support, **Data Science** (Jupyter), and virtualenv management.

## When to Use

- **Professional Python Development**: Full-stack Django, FastAPI, Flask, and scientific computing with PyTorch and NumPy.
- **Interactive Visual Debugging**: Inspecting threads, evaluation expressions, and profiling CPU/Memory bottlenecks.
- **Remote Interpreter & Docker Execution**: Running and debugging Python processes inside Docker containers and remote SSH servers.
- **Database & Data Science Tooling**: Exploring relational databases, Jupyter notebooks, and Pandas dataframes interactively.

## Quick Start

### 1. Launch via Terminal

```bash
# Open directory in PyCharm
pycharm .
```

### 2. Configure Poetry / Virtualenv Interpreter

```bash
# Ensure local virtualenv exists
poetry install
poetry env info --path
# Point PyCharm to .venv/bin/python
```

## Core Concepts

### Configuring Poetry / Conda Remote Virtual Environments

Setting up modern Python packaging and interpreter synchronization via `pyproject.toml`:

```toml
[tool.poetry]
name = "enterprise-api"
version = "0.1.0"
description = "FastAPI Enterprise Service"
authors = ["Engineering Team <eng@example.com>"]

[tool.poetry.dependencies]
python = "^3.12"
fastapi = "^0.111.0"
uvicorn = {extras = ["standard"], version = "^0.30.0"}
pydantic = "^2.7.0"
sqlalchemy = "^2.0.30"

[tool.poetry.group.dev.dependencies]
pytest = "^8.2.0"
ruff = "^0.4.0"
mypy = "^1.10.0"
```

Configure PyCharm Interpreter:

1. Open **Settings -> Project -> Python Interpreter**.
2. Click **Add Interpreter -> Add Local Interpreter...** -> Select **Poetry Environment**.
3. Select Python 3.12 executable path.

### Programmatic PyCharm Remote Debugger Setup

Connecting headless Python scripts or Docker containers to PyCharm's visual debugger:

```python
# Install pydevd-pycharm in container: pip install pydevd-pycharm~=241.14494.241
import pydevd_pycharm

def enable_remote_debugging():
    try:
        pydevd_pycharm.settrace(
            'host.docker.internal',
            port=5678,
            stdoutToServer=True,
            stderrToServer=True,
            suspend=False
        )
        print("Connected to PyCharm Remote Debugger!")
    except ConnectionRefusedError:
        print("PyCharm Debugger not listening. Continuing normal execution.")
```

### Fast Code Quality Inspections with Ruff Integration

Configuring Ruff as the primary linter and formatter inside PyCharm:

```json
// External Tools or Ruff Plugin configuration
// Settings -> Tools -> File Watchers -> Add Ruff
{
  "program": "$ProjectFileDir$/.venv/bin/ruff",
  "arguments": "check --fix $FilePath$",
  "workingDir": "$ProjectFileDir$"
}
```

## Common Patterns

### Remote Docker Compose Interpreter

**Problem**: Application dependencies require system libraries or services running inside Docker.  
**Solution**: Configure Docker Compose as remote interpreter in PyCharm Professional.

```yaml
# docker-compose.yml
services:
  app:
    build: .
    volumes:
      - .:/app
    environment:
      - PYTHONUNBUFFERED=1
    ports:
      - "8000:8000"
```

### Automated File Watcher Configuration

**Problem**: Automatically format and lint Python files on save with Ruff.  
**Solution**: Define File Watcher configuration in PyCharm.

```bash
# Arguments for Ruff File Watcher
format --stdin-filename $FilePath$ -
```

## Best Practices

**Do**:

- Configure **Ruff** plugin or file watcher for sub-second linting and auto-formatting.
- Use PyCharm's built-in **HTTP Client** (`.http` files) with environment support for testing REST APIs.
- Set up Docker Compose interpreters to maintain identical runtime environments across teams.
- Use **Python Profiler** (`Run -> Profile 'App'`) to locate algorithmic CPU and memory bottlenecks.

**Don't**:

- Commit `.idea/` directory without adding `.idea/workspace.xml` to `.gitignore`.
- Leave PyCharm indexing large data directories; right-click data folders -> **Mark Directory as -> Excluded**.
- Run untrusted Jupyter notebooks with elevated host permissions.

## Troubleshooting

| Error                                             | Cause                                                           | Solution                                                                                                         |
| ------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `No module named '...'` inside PyCharm terminal   | PyCharm internal terminal opened outside the project virtualenv | Verify `Settings > Tools > Terminal > Activate virtualenv` is checked; manually run `source .venv/bin/activate`. |
| Unresolved reference inspection on local packages | Root source directories not marked as Sources Root              | Right-click `src` or root folder > **Mark Directory as > Sources Root**.                                         |
| PyCharm sluggish during large indexing            | Indexing `.venv`, `node_modules`, or data directories           | Right-click cache or data directory > **Mark Directory as > Excluded**.                                          |

## References

- [PyCharm Documentation](https://www.jetbrains.com/pycharm/documentation/)
