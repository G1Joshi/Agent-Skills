---
name: pip
description: Expert Python pip package manager assistance covering requirements.txt, wheels, virtual environments, constraints, and pip-tools. Use when installing, locking, and managing Python dependencies.
---

# pip

pip is the standard package manager for Python. v24+ (2025) focuses on performance and standard compliance (PEP 668).

## When to Use

- **Python Package Installation & Management**: Installing, updating, and isolating Python dependencies from PyPI.
- **Deterministic Dependency Pinning**: Enforcing exact versions with `pip-tools` and constraints files (`-c constraints.txt`).
- **Modern Packaging Standards (PEP 517/621)**: Installing projects built with `pyproject.toml` without legacy `setup.py`.
- **Security & Integrity Verification**: Installing packages with cryptographic SHA256 hashes (`--require-hashes`).

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate

pip install requests
pip freeze > requirements.txt
```

## Core Concepts

#Deterministic Installation with Constraints Files

Separating direct top-level requirements from strictly pinned transitive constraints:

```text
# requirements.txt (Direct dependencies)
fastapi
pydantic
uvicorn[standard]
sqlalchemy
```

```text
# constraints.txt (Pinned transitive tree with hashes)
annotated-types==0.7.0 --hash=sha256:3bf9499874a...
fastapi==0.115.0 --hash=sha256:91823746198...
pydantic==2.9.2 --hash=sha256:d8912374691...
```

```bash
# Install direct requirements locked to verified constraint hashes
pip install --no-deps --require-hashes -r constraints.txt
pip install --no-cache-dir -r requirements.txt -c constraints.txt
```

#Editable Development Installation with pyproject.toml

Installing local development libraries into virtual environments:

```bash
# Editable install adhering to modern PEP 660
pip install -e .[dev,test]
```

#Auditing Installed Packages for Vulnerabilities

Checking dependencies against known security advisories:

```bash
# Check installed packages against PyPI Advisory Database using pip-audit
pip install pip-audit
pip-audit --desc
```

## Common Patterns

### Deterministic Dependency Pinning with pip-tools

**Problem**: Unpinned transitive dependencies in `requirements.txt` cause builds to break unexpectedly.

**Solution**:
Compile pinned dependency locks from abstract requirements:

```bash
# 1. Define top-level dependencies in requirements.in:
echo "fastapi>=0.110.0
uvicorn[standard]
pydantic" > requirements.in

# 2. Compile fully pinned lockfile with exact hashes:
pip-compile --generate-hashes requirements.in -o requirements.txt

# 3. Synchronize environment strictly matching lockfile:
pip-sync requirements.txt
```

## Best Practices (2026)

- **Do** always install packages into an isolated virtual environment (`python -m venv .venv`), never into the global system Python.
- **Do** use `pip install --no-cache-dir` in Dockerfiles to minimize container image sizes.
- **Do** enforce `--require-hashes` in production deployments to prevent supply-chain package tampering.
- **Do** use `pip-audit` in CI to detect vulnerable dependencies before merging pull requests.
- **Don't** run `sudo pip install`; modifying the system Python environment can break OS packages.
- **Don't** maintain unpinned `requirements.txt` in production; use `pip-compile` (pip-tools) to generate locked files.
- **Don't** use legacy `setup.py install`; use `pip install .` adhering to modern `pyproject.toml` standards.

## Troubleshooting

| Error                                                     | Cause                                                                    | Solution                                                                                         |
| :-------------------------------------------------------- | :----------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------- |
| `error: externally-managed-environment`                   | PEP 668 preventing direct pip install into system Python on Linux/macOS. | Create and activate a virtual environment: `python3 -m venv .venv && source .venv/bin/activate`. |
| `Could not find a version that satisfies the requirement` | Package name typo or incompatible Python version constraints.            | Verify package name on PyPI and check supported Python versions.                                 |
| `Failed building wheel for ...`                           | Missing C compiler, header files, or python development headers.         | Install `build-essential` and `python3-dev` packages.                                            |

## References

- [pip Documentation](https://pip.pypa.io/)
