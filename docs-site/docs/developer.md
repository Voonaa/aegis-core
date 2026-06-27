# Developer Guide

This guide details the coding standards, monorepo directory tree structure, Git development branch flow, automated testing strategies, static analysis checkers, and CI/CD coverage pipelines for Aegis Core Platform.

---

## Directory Structure

Aegis is developed as a modular monorepo:

-   `apps/desktop/` — CustomTkinter presentation layer and UI page controllers.
-   `packages/core/` — Core business logic, event dispatchers, and WMI hardware harvesters.
-   `packages/sdk/` — Public developer interface classes.
-   `plugins/` — Dynamic extension modules.
-   `scripts/` — Automated build scripts, benchmark suites, and compliance checks.
-   `tests/` — Unified Pytest suites.

---

## Local Development Setup

To configure a local developer environment, follow the steps on the [💾 Installation Guide](installation.md#1-developer-source-setup).

---

## Git Flow & Branch Strategy

Aegis utilizes a structured **Git Flow** strategy to coordinate feature development, releases, and hotfixes:

```text
  main (Stable Production) ───[Tag v1.0.0]────────────────────────────────
                                 ▲
                                 │ Release Merge
  develop (Active Integration) ──┴───[Merge Feature]───[Compile Release]──
                                         ▲
                                         │ Feature Merge
  feature/* (Independent Task) ──────────┴────────────────────────────────
```

-   **`main` Branch**: Contains official production-ready stable releases. Every commit to `main` corresponds to a compiled biner release tag (e.g. `v1.0.0`).
-   **`develop` Branch**: Main active integration branch for developers. Daily pull requests from task branches are merged here after passing all unit testing and compliance pipelines.
-   **`feature/*` Branches**: Independent workspace branches used by developers to build features or write unit test improvements (e.g. `feature/cov-hardening` or `feature/ui-settings-fix`).

---

## Coding Conventions

Developers must adhere to the following standards to keep the codebase clean:

### Formatting Rules
We use **Ruff** for style checks and PEP 8 compliance.
-   **Indentation**: 4 spaces (no tabs allowed).
-   **Line Limits**: Maximum line width set to **120 characters**.
-   **Quotes**: Use double quotes (`"`) for all strings unless single quotes are needed to prevent escaping.

### Code Style (PEP 8) & Static Analysis
Run the Ruff linter check:
```powershell
ruff check packages/ apps/ tests/
```

### Static Type Annotations (PEP 484)
We enforce static typing. Use type hints for all function arguments and return signatures:
```python
def gather_telemetry(self) -> TelemetryReport:
    # Logic
```
Run type analysis:
```powershell
mypy packages/ apps/ --ignore-missing-imports
```

---

## Testing & Coverage Policy

Aegis enforces a strict quality gate policies before code can be merged into `develop`.

### Testing Strategy
1.  **Isolated Mocks**: All HAL tests must mock WMI calls (`win32com` / `winreg` / `ctypes` handles) so they can run safely in non-privileged local developer environments and headless Linux CI containers.
2.  **Service Container Registries**: Test cases must utilize a freshly instantiated `ServiceContainer` instance reset inside fixtures to prevent memory leaks and database file locks.

### Running Tests
Execute Pytest verbosely from the project root:
```powershell
# Set PYTHONPATH path
$env:PYTHONPATH = "."

# Run full test suite verbosely
pytest tests/ -v
```

### Coverage Policy (70%+ Threshold)
All core engine and SDK files must maintain a minimum target code coverage of **70%**. Commits dropping the coverage average below this target will fail the build checks gate.
To run tests and export coverage reports:
```powershell
pytest tests/ --cov=packages --cov-report=term --cov-report=xml:reports/coverage/coverage.xml --cov-report=html:reports/coverage/htmlcov
```
View the interactive HTML report at `reports/coverage/htmlcov/index.html`.

---

## CI/CD Pipeline

Aegis uses GitHub Actions for continuous integration and automated testing.

### Workflow: `ci.yml`
-   **Trigger**: Fires on any push or pull request to the `develop` or `main` branches.
-   **Tasks**:
    1. Sets up the Python matrix across test platforms.
    2. Installs requirements.
    3. Runs Ruff linter checks.
    4. Runs MyPy type checks.
    5. Executes the test suite and exports coverage results.
