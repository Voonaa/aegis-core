# Aegis Core Platform — Developer Guide

> Panduan untuk menyiapkan environment pengembangan, menjalankan test suite, dan berkontribusi ke codebase.

---

## Prerequisites

| Tool | Minimum Version | Purpose |
|:---|:---:|:---|
| Python | 3.11+ | Runtime |
| Git | 2.40+ | Version control |
| Windows | 10 / 11 | Target OS (WMI dependency) |
| PowerShell | 5.1+ | Scripts & release tooling |

---

## 1. Initial Setup

```powershell
# Clone the repository
git clone https://github.com/Voonaa/aegis-core.git
cd aegis-core

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (test tools, linters)
pip install -r requirements-dev.txt
```

---

## 2. Running the Application

```powershell
# Set PYTHONPATH to project root (required for monorepo imports)
$env:PYTHONPATH = "."

# Launch the desktop application
python apps/desktop/main.py
```

---

## 3. Running Tests

Aegis uses **Pytest** for all unit tests. Test coverage is measured with `pytest-cov`.

```powershell
# Run full test suite
$env:PYTHONPATH = "."
pytest tests/ -v

# Run with coverage report (HTML output)
pytest tests/ -v --cov=packages --cov-report=html

# Coverage HTML report output: reports/htmlcov/index.html
```

### Current Test Status

| Metric | Value |
|:---|:---:|
| Total tests | 99 |
| Passing | 99 |
| Failing | 0 |
| Coverage target | 80%+ |

---

## 4. Static Analysis

### Ruff (Linter)

```powershell
# Run Ruff linter
ruff check packages/ apps/ tests/

# Auto-fix safe issues
ruff check packages/ apps/ tests/ --fix
```

### MyPy (Type Checker)

```powershell
# Run MyPy type checking
mypy packages/ apps/ --ignore-missing-imports
```

### Run All Quality Checks (One Command)

```powershell
.\\scripts\\lint.ps1
```

---

## 5. Project Structure & Conventions

### Naming Conventions

| Context | Convention | Example |
|:---|:---|:---|
| Modules / files | `snake_case` | `health_service.py` |
| Classes | `PascalCase` | `HardwareService` |
| Functions / methods | `snake_case` | `get_snapshot()` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| DI Container keys | `"snake_case"` string | `"hardware_service"` |

### Code Standards

- All public methods must have **type annotations**.
- All classes must have **docstrings**.
- No bare `except` clauses — always catch specific exceptions.
- Logging via the project's `LoggingService`, not `print()`.
- Services registered in `packages/core/bootstrap.py` only.

---

## 6. Git Workflow

```text
main        ← production-ready code only
develop     ← active development branch
feature/*   ← feature branches (merge into develop)
bugfix/*    ← bugfix branches (merge into develop)
```

### Commit Message Format

```text
<type>(<scope>): <short description>

Examples:
feat(hal): add GPU temperature query
fix(bootstrap): correct profile_mgr DI key
docs(readme): restructure as landing page
test(services): add coverage for telemetry export
```

---

## 7. Debugging Common Issues

### WMI Permission Errors

```text
Error: wmi.x_wmi: <x_wmi error>
```

**Solution**: Run IDE or terminal as **Administrator** to allow WMI queries.

---

### Import Errors (`ModuleNotFoundError`)

```text
ModuleNotFoundError: No module named 'packages'
```

**Solution**: Ensure `PYTHONPATH` is set to the project root:

```powershell
$env:PYTHONPATH = "."
```

---

### CustomTkinter Display Issues

**Solution**: Update CustomTkinter to the latest version:
```powershell
pip install --upgrade customtkinter
```

---

## 8. Contributing

Please read [CONTRIBUTING.md](../CONTRIBUTING.md) for the full contribution guidelines, including:
- How to open an issue
- Pull request checklist
- Code review standards

---

## Further Reading

- [Architecture](architecture.md) — System design and data flow
- [SDK Reference](sdk.md) — Public API for external integrations
- [Plugin System](plugins.md) — Extension plugin development
